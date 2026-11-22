/* IIPCT website: the events lists follow what staff publish on the server.

   Home ("Up next" and "Coming up") and Events & Programs (the cards) are built from tools/generator/p_events.py.
   While LIVE_SITE in tools/generator/lib.py is set, those two pages load this file (defer) with that address in
   data-site. It asks the server's public events feed once (no cookies, at most 4 seconds, no retry) and checks the
   answer strictly. Then:
   - no answer, an answer that fails any check, or no events: nothing changes. The page stays as built, which is also
     what it shows with JavaScript off.
   - events: the server is the truth. A built card whose event is in the feed (the same title once case, spaces,
     dashes and quote marks are folded, and at least one common day) stays, with the server's status, or marked
     cancelled; a built card whose event is not in the feed is hidden; an event only the server lists gets a card
     from the page's <template>, in date order. Home's "Up next" and "Coming up" are the feed's next dates.
   Text from the feed goes in as text (textContent), never as markup. A link from the feed is used only after the
   checks (it must start with LIVE_SITE + "/events-programs/").
   Source: tools/generator/live-events.js, copied to assets/js/ by export_site.py. Never edit the copy. */
(function () {
  'use strict';
  var script = document.currentScript;
  var SITE = (script && script.getAttribute('data-site')) || '';
  if (!/^https:\/\/[a-z0-9.-]+$/.test(SITE) || !/^https?:$/.test(location.protocol)) return;   // a page opened from a file: no feed
  if (!window.fetch || !window.Intl || !Object.create || !('content' in document.createElement('template'))) return;

  var FEED = SITE + '/api/public/events', EVENT_PAGE = SITE + '/events-programs/';
  var WAIT_MS = 4000, MAX_BYTES = 1048576, MAX_EVENTS = 60, MAX_DATES = 12;
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];   // Date#getUTCDay order
  var TIME = /^(1[0-2]|[1-9]):([0-5][0-9]) (am|pm)$/;
  var HREF_REST = /^[A-Za-z0-9._~%!$&'()*+,;=:@\/?#-]+$/;
  var own = Object.prototype.hasOwnProperty;

  // ------------------------------------------------------------------ ask once
  var settled = false, applying = false, ctl = window.AbortController ? new AbortController() : null;
  var timer = setTimeout(function () { settled = true; if (ctl) ctl.abort(); done('unchanged'); }, WAIT_MS);
  fetch(FEED, { method: 'GET', credentials: 'omit', mode: 'cors', redirect: 'error', signal: ctl ? ctl.signal : undefined })
    .then(function (res) {
      if (settled || !res.ok || !/^application\/json\b/i.test(res.headers.get('content-type') || '')) throw new Error('feed');
      var size = res.headers.get('content-length');
      if (size && !(+size <= MAX_BYTES)) throw new Error('feed');
      return readCapped(res);
    })
    .then(function (body) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      var events = check(JSON.parse(body));
      if (!events.length) return done('unchanged');
      applying = true;
      apply(events);
      done('shown');
    })
    .catch(function () {
      settled = true;
      clearTimeout(timer);
      if (ctl) ctl.abort();
      done(applying ? 'error' : 'unchanged');
    });

  /** What happened, on <html data-live-events>, for anyone checking (and the tests): shown, unchanged or error. */
  function done(state) {
    var root = document.documentElement;
    if (!root.hasAttribute('data-live-events')) root.setAttribute('data-live-events', state);
  }

  /** The answer's text, read up to MAX_BYTES (anything longer is refused part way, not downloaded whole). */
  function readCapped(res) {
    if (!res.body || !res.body.getReader || !window.TextDecoder) {
      return res.text().then(function (t) { if (t.length > MAX_BYTES) throw new Error('feed'); return t; });
    }
    var reader = res.body.getReader(), dec = new TextDecoder('utf-8', { fatal: true }), got = 0, out = '';
    function next() {
      return reader.read().then(function (r) {
        if (r.done) return out + dec.decode();
        got += r.value.byteLength;
        if (got > MAX_BYTES || settled) { reader.cancel(); throw new Error('feed'); }
        out += dec.decode(r.value, { stream: true });
        return next();
      });
    }
    return next();
  }

  // ------------------------------------------------------------------ check everything before anything is used
  function fail() { throw new Error('feed'); }
  function isObj(x) { return x !== null && typeof x === 'object' && !Array.isArray(x); }
  function chars(s) { return Array.from ? Array.from(s).length : s.length; }
  function field(o, k) { return own.call(o, k) ? o[k] : undefined; }
  function text(o, k, max, min) {
    var v = field(o, k);
    if (typeof v !== 'string') fail();
    var n = chars(v);
    if (n > max || n < (min || 0)) fail();
    return v;
  }
  function dayInfo(day) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(day);
    if (!m) fail();
    var y = +m[1], mo = +m[2], d = +m[3], t = new Date(Date.UTC(y, mo - 1, d));
    if (y < 2000 || y > 2100 || t.getUTCFullYear() !== y || t.getUTCMonth() !== mo - 1 || t.getUTCDate() !== d) fail();
    return { y: y, m: mo, d: d, wd: t.getUTCDay(), utc: t.getTime() };
  }
  function check(feed) {
    if (!isObj(feed)) fail();
    text(feed, 'generatedAt', 40, 1);
    if (text(feed, 'site', 200) !== SITE) fail();
    var list = field(feed, 'events');
    if (!Array.isArray(list) || list.length > MAX_EVENTS) fail();
    var ids = Object.create(null);
    return list.map(function (ev, index) {
      if (!isObj(ev)) fail();
      var id = text(ev, 'id', 100, 1);
      if (ids[id]) fail();
      ids[id] = true;
      var title = text(ev, 'title', 200, 1).trim(), href = text(ev, 'href', 400), cancelled = field(ev, 'cancelled');
      if (!title || href.indexOf(EVENT_PAGE) !== 0 || !HREF_REST.test(href.slice(EVENT_PAGE.length)) || typeof cancelled !== 'boolean') fail();
      var status = text(ev, 'status', 100).trim(), program = text(ev, 'program', 100).trim(), summary = text(ev, 'summary', 300).trim();
      var dates = field(ev, 'dates');
      if (!Array.isArray(dates) || dates.length < 1 || dates.length > MAX_DATES) fail();
      dates = dates.map(function (dt, di) {
        if (!isObj(dt)) fail();
        var day = text(dt, 'day', 10), info = dayInfo(day), start = text(dt, 'start', 8), end = text(dt, 'end', 8);
        if (text(dt, 'weekday', 9) !== DAYS[info.wd] || !TIME.test(start) || (end && !TIME.test(end))) fail();
        return { day: day, info: info, start: start, end: end, place: text(dt, 'place', 200).trim(), key: day + 'T' + to24(start), di: di };
      }).sort(byKey);
      return { index: index, title: title, fold: fold(title), href: href, cancelled: cancelled, status: status, program: program, summary: summary, dates: dates };
    });
  }

  // ------------------------------------------------------------------ words and times (as tools/generator/p_events.py writes them)
  function fold(s) {
    if (s.normalize) s = s.normalize('NFC');
    return s.toLowerCase()
      .replace(/[\u2010-\u2015\u2212\ufe58\ufe63\uff0d]/g, '-')
      .replace(/[\u2018\u2019\u201a\u201b\u2032`\u00b4]/g, "'")
      .replace(/[\u201c\u201d\u201e\u201f\u2033]/g, '"')
      .replace(/\s+/g, '');
  }
  function to24(t) {   // "6:00 pm" -> "18:00"
    var m = TIME.exec(t), h = (+m[1] % 12) + (m[3] === 'pm' ? 12 : 0);
    return (h < 10 ? '0' : '') + h + ':' + m[2];
  }
  function trange(s, e) {   // "6:00–8:00 pm", "11:00 am–1:00 pm", or the start alone
    if (!e) return s;
    return (s.slice(-2) === e.slice(-2) ? s.slice(0, -3) : s) + '\u2013' + e;
  }
  function dlong(info) { return DAYS[info.wd] + ', ' + MONTHS[info.m - 1] + ' ' + info.d + ', ' + info.y; }
  function dayList(dates) {   // "December 9, 2026; January 13 and February 10, 2027"
    var years = [];
    dates.forEach(function (d) {
      var y = years[years.length - 1];
      if (!y || y.y !== d.info.y) years.push(y = { y: d.info.y, names: [] });
      y.names.push(MONTHS[d.info.m - 1] + ' ' + d.info.d);
    });
    return years.map(function (y) {
      var n = y.names;
      return (n.length > 1 ? n.slice(0, -1).join(', ') + ' and ' + n[n.length - 1] : n[0]) + ', ' + y.y;
    }).join('; ');
  }
  function sentence(s) { return /[.!?]$/.test(s) ? s : s + '.'; }
  function byKey(a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.di - b.di; }
  function torontoNow() {
    var p = {};
    new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var day = p.year + '-' + p.month + '-' + p.day;
    return { day: day, at: day + 'T' + p.hour + ':' + p.minute, utc: Date.UTC(+p.year, +p.month - 1, +p.day) };
  }
  function over(d, now) { return d.day + 'T' + (d.end ? to24(d.end) : '23:59') < now.at; }   // Home's rule for dates already over
  function shares(days, dates) { return dates.some(function (d) { return days.indexOf(d.day) !== -1; }); }

  // ------------------------------------------------------------------ the page's own markup
  function fromTemplate(id) {
    var t = document.getElementById(id), el = t && t.content && t.content.firstElementChild;
    return el ? el.cloneNode(true) : null;
  }
  function part(root, name) { return root.querySelector('[data-slot="' + name + '"]'); }
  function drop(el) { if (el && el.parentNode) el.parentNode.removeChild(el); }
  function hide(el) { el.style.setProperty('display', 'none', 'important'); }   // beats the phone layout's display rules
  function say(el, s) { el.textContent = s; el.hidden = false; }
  function rowText(row, s) { row.lastElementChild.textContent = s; }   // a when/where row: icon, then its text
  function tile(el, info) {
    var s = el.children;
    s[0].textContent = MONTHS[info.m - 1].slice(0, 3);
    s[1].textContent = String(info.d);
    s[2].textContent = DAYS[info.wd].slice(0, 3);
  }
  function link(a, href, outside) {
    a.setAttribute('href', href);
    if (outside) { a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener'); }
  }
  /** What the server says that the built text does not: "cancel", its status when it differs, or "" (leave as built). */
  function news(evs, builtStatus) {
    if (evs.every(function (ev) { return ev.cancelled; })) return 'cancel';
    for (var i = 0; i !== evs.length; i++) {
      if (!evs[i].cancelled && evs[i].status && fold(evs[i].status) !== fold(builtStatus)) return evs[i].status;
    }
    return '';
  }

  function apply(events) {
    var now = torontoNow();
    eventsPage(events, now);
    homePage(events, now);
  }

  // ------------------------------------------------------------------ Events & Programs: the cards
  function eventsPage(events, now) {
    var list = document.getElementById('ev-list');
    if (!list || !document.getElementById('ev-tpl-card')) return;
    var built = [].slice.call(list.querySelectorAll('article[data-ev-title]')).map(function (el, i) {
      return { el: el, order: i, fold: fold(el.getAttribute('data-ev-title') || ''), days: (el.getAttribute('data-ev-days') || '').split(' '),
               status: el.getAttribute('data-ev-status') || '', evs: [] };
    });
    var items = [];
    events.forEach(function (ev) {
      var found = false;
      built.forEach(function (b) { if (b.fold === ev.fold && shares(b.days, ev.dates)) { b.evs.push(ev); found = true; } });
      var ahead = ev.dates.filter(function (d) { return !over(d, now); });
      if (!found && ahead.length) items.push({ key: ahead[0].key, order: 1000 + ev.index, el: newCard(ev, ahead) });
    });
    built.forEach(function (b) {
      if (!b.evs.length) { hide(b.el); return; }   // staff took it down
      var dates = [];
      b.evs.forEach(function (ev) { dates = dates.concat(ev.dates); });
      dates.sort(byKey);
      var ahead = dates.filter(function (d) { return !over(d, now); }), first = (ahead[0] || dates[0]);
      items.push({ key: first.key, order: b.order, el: b.el });
      var s = news(b.evs, b.status), st = part(b.el, 'status');
      if (s && st) say(st, s === 'cancel' ? 'This event is cancelled.' : sentence(s));
      if (s === 'cancel') [].forEach.call(b.el.querySelectorAll('a.btn'), hide);   // no booking for a cancelled event
      if (first.day !== b.days[0]) tile(b.el.querySelector('.ev-d'), first.info);
      var box = part(b.el, 'when'), seen = {};
      ahead.forEach(function (d) {   // dates the server added
        if (b.days.indexOf(d.day) !== -1 || seen[d.key] || !box) return;
        seen[d.key] = true;
        var row = fromTemplate('ev-tpl-card');
        row = row && part(row, 'when-row');
        if (!row) return;
        rowText(row, 'Also on ' + dlong(d.info) + ' \u00b7 ' + trange(d.start, d.end) + (d.place ? ' \u00b7 ' + d.place : ''));
        box.appendChild(row);
      });
    });
    items.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.order - b.order; });
    items.forEach(function (it) { if (it.el) list.appendChild(it.el); });
  }

  function newCard(ev, dates) {
    var el = fromTemplate('ev-tpl-card');
    if (!el) return null;
    tile(el.querySelector('.ev-d'), dates[0].info);
    var tag = part(el, 'tag');
    if (ev.program) tag.textContent = ev.program; else drop(tag);
    part(el, 'title').textContent = ev.title;
    var whenRow = part(el, 'when-row'), whereRow = part(el, 'where-row'), first = dates[0], lines, where = '';
    var alike = dates.every(function (d) { return d.start === first.start && d.end === first.end && d.place === first.place; });
    if (dates.length === 1) {
      lines = [dlong(first.info) + ' \u00b7 ' + trange(first.start, first.end)];
      where = first.place;
    } else if (alike) {
      var oneDay = dates.every(function (d) { return d.info.wd === first.info.wd; });
      lines = [(oneDay ? DAYS[first.info.wd] + 's, ' : '') + trange(first.start, first.end) + ': ' + dayList(dates)];
      where = first.place;
    } else {
      lines = dates.map(function (d) { return dlong(d.info) + ' \u00b7 ' + trange(d.start, d.end) + (d.place ? ' \u00b7 ' + d.place : ''); });
    }
    lines.forEach(function (line, i) {
      var row = i ? whenRow.cloneNode(true) : whenRow;
      rowText(row, line);
      if (i) whereRow.parentNode.insertBefore(row, whereRow);
    });
    if (where) rowText(whereRow, where); else drop(whereRow);
    var sum = part(el, 'summary');
    if (ev.summary) sum.textContent = ev.summary; else drop(sum);
    var st = part(el, 'status');
    if (ev.cancelled) say(st, 'This event is cancelled.'); else if (ev.status) say(st, sentence(ev.status)); else drop(st);
    link(part(el, 'link'), ev.href, true);
    return el;
  }

  // ------------------------------------------------------------------ Home: "Up next" and "Coming up"
  function homePage(events, now) {
    var rowsBox = document.getElementById('ev-rows'), col = document.getElementById('ev-next-col');
    var head = document.getElementById('ev-list-head'), none = document.getElementById('ev-none');
    if (!rowsBox || !col || !head || !none || !fromTemplate('ev-tpl-next') || !fromTemplate('ev-tpl-group') || !fromTemplate('ev-tpl-row')) return;
    var byKeyAttr = Object.create(null), builtEvents = [];
    [].forEach.call(rowsBox.querySelectorAll('li[data-ev-key]'), function (r) {
      var k = r.getAttribute('data-ev-key'), b = byKeyAttr[k], a = r.querySelector('a[href]');
      if (!b) {
        b = byKeyAttr[k] = { key: k, fold: fold(r.getAttribute('data-ev-title') || ''), days: (r.getAttribute('data-ev-days') || '').split(' '),
                             status: r.getAttribute('data-ev-status') || '', rows: Object.create(null), href: a ? a.getAttribute('href') : '' };
        builtEvents.push(b);
      }
      b.rows[r.getAttribute('data-day')] = r;
    });
    var occ = [];
    events.forEach(function (ev) {
      ev.built = builtEvents.filter(function (b) { return b.fold === ev.fold && shares(b.days, ev.dates); });
      ev.dates.forEach(function (d) { if (!over(d, now)) occ.push({ ev: ev, d: d, key: d.key, order: ev.index * 100 + d.di }); });
    });
    occ.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.order - b.order; });
    var used = [];
    function builtFor(o) {   // the built event with a row (and an "Up next" card) for this date
      for (var i = 0; i !== o.ev.built.length; i++) {
        var b = o.ev.built[i], r = b.rows[o.d.day];
        if (r && used.indexOf(r) === -1) return b;
      }
      return null;
    }
    function target(ev) { return ev.built.length ? ev.built[0].href : ev.href; }   // the built card on Events & Programs, else the server's page

    // Up next: the first date still to come that is not cancelled
    var next = null, nextEl = null, i;
    for (i = 0; i !== occ.length; i++) if (!occ[i].ev.cancelled) { next = occ[i]; break; }
    if (next) {
      var nb = builtFor(next);
      nextEl = nb && document.getElementById('next-' + nb.key + '-' + next.d.day);
      if (nextEl) {
        used.push(nb.rows[next.d.day]);
        var ns = news([next.ev], nb.status), nst = part(nextEl, 'status');
        if (ns && nst) say(nst, sentence(ns));
      } else {
        nextEl = newNext(next, target(next.ev), !next.ev.built.length);
      }
    }

    // Coming up: the dates after it, at most five days, as the built list shows them
    var rest = occ.filter(function (o) { return o !== next; }), days = [], groups = [], group = null;
    rest.forEach(function (o) { if (days.length < 5 && days.indexOf(o.d.day) === -1) days.push(o.d.day); });
    rest.forEach(function (o) {
      if (days.indexOf(o.d.day) === -1) return;
      if (!group || group.day !== o.d.day) {
        var g = fromTemplate('ev-tpl-group');
        g.setAttribute('data-group', o.d.day);
        g.firstElementChild.textContent = dlong(o.d.info);
        groups.push(group = { day: o.d.day, el: g, list: g.querySelector('ul') });
      }
      var b = builtFor(o), row;
      if (b) {
        row = b.rows[o.d.day];
        used.push(row);
        row.style.display = '';   // the built script hides rows it showed as "Up next" or found over
        var s = news([o.ev], b.status), st = part(row, 'status');
        if (s && st) say(st, s === 'cancel' ? 'Cancelled' : s);
      } else {
        row = newRow(o, target(o.ev), !o.ev.built.length);
      }
      if (row) group.list.appendChild(row);
    });

    // put it on the page in one go
    [].forEach.call(col.children, function (c) { c.hidden = true; });
    if (nextEl) {
      var diff = Math.round((next.d.info.utc - now.utc) / 864e5);
      var label = diff === 0 ? 'Today' : diff === 1 ? 'Tomorrow' : diff > 1 && diff < 7 ? DAYS[next.d.info.wd] : '';
      var lab = nextEl.querySelector('.ev-when');
      if (lab) { lab.textContent = label; lab.parentNode.hidden = !label; }
      if (nextEl.parentNode !== col) col.appendChild(nextEl);
      nextEl.hidden = false;
    }
    col.hidden = !nextEl;
    var frag = document.createDocumentFragment();
    groups.forEach(function (g) { frag.appendChild(g.el); });
    rowsBox.textContent = '';
    rowsBox.appendChild(frag);
    head.style.display = groups.length ? '' : 'none';
    none.hidden = !!(nextEl || groups.length);
  }

  function newNext(o, href, outside) {
    var el = fromTemplate('ev-tpl-next');
    if (!el) return null;
    tile(el.querySelector('.ev-d'), o.d.info);
    part(el, 'title').textContent = o.ev.title;
    rowText(part(el, 'when-row'), dlong(o.d.info) + ' \u00b7 ' + trange(o.d.start, o.d.end));
    if (o.d.place) rowText(part(el, 'where-row'), o.d.place); else drop(part(el, 'where-row'));
    if (o.ev.status) say(part(el, 'status'), sentence(o.ev.status)); else drop(part(el, 'status'));
    if (o.ev.summary) part(el, 'summary').textContent = o.ev.summary; else drop(part(el, 'summary'));
    link(part(el, 'link'), href, outside);
    return el;
  }

  function newRow(o, href, outside) {
    var el = fromTemplate('ev-tpl-row');
    if (!el) return null;
    part(el, 'time').textContent = trange(o.d.start, o.d.end);
    part(el, 'title').textContent = o.ev.title;
    if (o.d.place) part(el, 'place').textContent = o.d.place; else part(el, 'place').hidden = true;
    var st = part(el, 'status');
    if (o.ev.cancelled) say(st, 'Cancelled'); else if (o.ev.status) say(st, o.ev.status); else drop(st);
    link(el.querySelector('a'), href, outside);
    return el;
  }
})();
