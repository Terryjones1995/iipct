/* IIPCT website: the events lists follow what staff publish on the server.

   Home ("Up next" and "Coming up") and Events & Programs (the cards) are built from tools/generator/p_events.py.
   While LIVE_SITE in tools/generator/lib.py is set, those two pages load this file (defer) with that address in
   data-site. It asks the server's public events feed once (no cookies, at most 4 seconds, no retry) and checks the
   answer strictly. Then:
   - no answer, an answer that fails any check, or no events: nothing changes. The page stays as built, which is also
     what it shows with JavaScript off.
   - events: the server is the truth. A built card whose event is in the feed (the same title once case, spaces,
     dashes and quote marks are folded, and at least one common day) stays, with the server's status (or none, when
     the server has none), or marked cancelled; its when and where lines are redrawn from the server's dates when the
     server's days, times or place differ from the built ones. A built card whose event is not in the feed is hidden;
     an event only the server lists gets a card from the page's <template>, in date order. Home's "Up next" and
     "Coming up" are the feed's next dates, with the server's times, places and statuses.
   Text from the feed goes in as text (textContent), never as markup. A link from the feed is used only after the
   checks (it must lead to a page under LIVE_SITE + "/events-programs/").
   Source: tools/generator/live-events.js, copied to assets/js/ by export_site.py. Never edit the copy. */
(function () {
  'use strict';
  var script = document.currentScript;
  var SITE = (script && script.getAttribute('data-site')) || '';
  if (!/^https:\/\/[a-z0-9.-]+$/.test(SITE) || !/^https?:$/.test(location.protocol)) return;   // a page opened from a file: no feed
  if (!window.fetch || !window.Intl || !window.URL || !Object.create || !('content' in document.createElement('template'))) return;

  var FEED = SITE + '/api/public/events', EVENT_PAGE = SITE + '/events-programs/';
  var WAIT_MS = 4000, MAX_BYTES = 1048576, MAX_EVENTS = 60, MAX_DATES = 12;
  // Longest text per field, in characters. The summary's 300 is the feed's contract. The others sit above what the
  // server can send (an event's and a program's title: at most 180; a place: a name of at most 180 plus ", " and its
  // street), so a real answer always passes. The server does not cap a status (the first sentence staff write after
  // "Status:"), so its limit is far above any sentence.
  var MAX = { id: 100, title: 200, program: 200, place: 500, status: 1000, summary: 300, href: 400 };
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];   // Date#getUTCDay order
  var TIME = /^(1[0-2]|[1-9]):([0-5][0-9]) (am|pm)$/;
  // An end as the server writes it: "8:00 pm"; "1:00 am" past midnight; "4:00 pm the next day" or "4:00 pm 2 days later"
  var END = /^((?:1[0-2]|[1-9]):[0-5][0-9] (?:am|pm))(?: (the next day|([2-9]|[1-9][0-9]{1,2}) days later))?$/;
  var STAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d{1,3})?)?Z$/;
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
      var feed = check(JSON.parse(body));
      if (!feed.events.length) return done('unchanged');
      applying = true;
      apply(feed);
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
  /** A link from the feed: a page under LIVE_SITE + "/events-programs/", also once the browser has resolved it
      ("../" and "%2e%2e" climb out of the folder, so the resolved path is checked too). Returns the resolved link. */
  function eventLink(href) {
    if (href.indexOf(EVENT_PAGE) !== 0 || !HREF_REST.test(href.slice(EVENT_PAGE.length))) fail();
    var u = new URL(href);
    if (u.origin !== SITE || u.username || u.password || u.pathname.indexOf('/events-programs/') !== 0 || u.pathname.length <= 17) fail();
    return u.href;
  }
  /** A date's times, as the server writes them: its end may fall on a later day ("later": how many days later). */
  function span(day, info, start, end) {
    var m = end ? END.exec(end) : null;
    if (end && !m) fail();
    var later = !m ? 0 : m[2] ? (m[3] ? +m[3] : 1) : (to24(m[1]) < to24(start) ? 1 : 0);   // "1:00 am" after "9:00 pm": the next day
    return { day: day, info: info, start: start, end: end, endTime: m ? m[1] : '', later: later, words: m && m[2] ? m[2] : '' };
  }
  function check(feed) {
    if (!isObj(feed)) fail();
    var stamp = text(feed, 'generatedAt', 40, 1);
    if (!STAMP.test(stamp) || isNaN(Date.parse(stamp))) fail();
    if (text(feed, 'site', 200) !== SITE) fail();
    var list = field(feed, 'events');
    if (!Array.isArray(list) || list.length > MAX_EVENTS) fail();
    var ids = Object.create(null);
    var events = list.map(function (ev, index) {
      if (!isObj(ev)) fail();
      var id = text(ev, 'id', MAX.id, 1);
      if (ids[id]) fail();
      ids[id] = true;
      var title = text(ev, 'title', MAX.title, 1).trim(), href = eventLink(text(ev, 'href', MAX.href)), cancelled = field(ev, 'cancelled');
      if (!title || typeof cancelled !== 'boolean') fail();
      var status = text(ev, 'status', MAX.status).trim(), program = text(ev, 'program', MAX.program).trim(), summary = text(ev, 'summary', MAX.summary).trim();
      var dates = field(ev, 'dates');
      if (!Array.isArray(dates) || dates.length < 1 || dates.length > MAX_DATES) fail();
      dates = dates.map(function (dt, di) {
        if (!isObj(dt)) fail();
        var day = text(dt, 'day', 10), info = dayInfo(day), start = text(dt, 'start', 8);
        if (text(dt, 'weekday', 9) !== DAYS[info.wd] || !TIME.test(start)) fail();
        var d = span(day, info, start, text(dt, 'end', 30));
        d.place = text(dt, 'place', MAX.place).trim();
        d.key = day + 'T' + to24(start);
        d.di = di;
        d.cancelled = cancelled;
        return d;
      }).sort(byKey);
      return { index: index, title: title, fold: fold(title), href: href, cancelled: cancelled, status: status, program: program, summary: summary, dates: dates };
    });
    return { events: events, at: toronto(new Date(stamp)) };
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
  /** A place's words, for comparing: case, accents' normal form and punctuation folded, "Rd" read as "Road". */
  var ABBR = { rd: 'road', st: 'street', ave: 'avenue', dr: 'drive', hwy: 'highway' };
  function words(s) {
    if (s.normalize) s = s.normalize('NFC');
    return s.toLowerCase().split(/[^0-9a-z\u00c0-\u024f\u1e00-\u1eff]+/).filter(Boolean).map(function (w) { return own.call(ABBR, w) ? ABBR[w] : w; });
  }
  /** The server's place says nothing the built place does not ("Shannonville Office" for "Shannonville Office, 14 York Road"). */
  function samePlace(place, known) { return words(place).every(function (w) { return known.indexOf(w) !== -1; }); }
  function to24(t) {   // "6:00 pm" -> "18:00"
    var m = TIME.exec(t), h = (+m[1] % 12) + (m[3] === 'pm' ? 12 : 0);
    return (h < 10 ? '0' : '') + h + ':' + m[2];
  }
  function trange(s, e) {   // "6:00–8:00 pm", "11:00 am–1:00 pm", or the start alone
    if (!e) return s;
    return (s.slice(-2) === e.slice(-2) ? s.slice(0, -3) : s) + '\u2013' + e;
  }
  /** A date's times as the server's pages say them: "6:00–8:00 pm", "9:00 pm–1:00 am", "10:00 am to 4:00 pm the next day". */
  function times(d) {
    if (!d.end) return d.start;
    if (d.words) return d.start + ' to ' + d.endTime + ' ' + d.words;
    if (d.later) return d.start + '\u2013' + d.endTime;
    return trange(d.start, d.endTime);
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
  /** The when lines of a card for these dates, and its one place (or "" when each line names its own). */
  function whenLines(dates, marks) {
    var first = dates[0];
    var alike = !marks && dates.every(function (d) { return d.start === first.start && d.end === first.end && d.place === first.place; });
    if (dates.length === 1 || alike) {
      var oneDay = dates.every(function (d) { return d.info.wd === first.info.wd; });
      return { where: first.place, placed: false,
               lines: [dates.length === 1 ? dlong(first.info) + ' \u00b7 ' + times(first) : (oneDay ? DAYS[first.info.wd] + 's, ' : '') + times(first) + ': ' + dayList(dates)] };
    }
    return { where: '', placed: dates.some(function (d) { return d.place; }),
             lines: dates.map(function (d) { return dlong(d.info) + ' \u00b7 ' + times(d) + (d.place ? ' \u00b7 ' + d.place : '') + (marks && d.cancelled ? ' \u00b7 Cancelled' : ''); }) };
  }
  function sentence(s) { return /[.!?]$/.test(s) ? s : s + '.'; }
  function byKey(a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.di - b.di; }
  /** Toronto's calendar day and clock at a moment ("at": "YYYY-MM-DDTHH:MM:SS", compared as text). */
  function toronto(when) {
    var p = {};
    new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' }).formatToParts(when).forEach(function (x) { p[x.type] = x.value; });
    var day = p.year + '-' + p.month + '-' + p.day;
    return { day: day, at: day + 'T' + p.hour + ':' + p.minute + ':' + p.second, utc: Date.UTC(+p.year, +p.month - 1, +p.day) };
  }
  /** A date is over once its end has passed (on a later day for an end past midnight; at 23:59 when no end is given). */
  function over(d, now) {
    if (!d.end) return d.day + 'T23:59:59' < now.at;
    var day = d.later ? new Date(d.info.utc + d.later * 864e5).toISOString().slice(0, 10) : d.day;
    return day + 'T' + to24(d.endTime) + ':00' < now.at;
  }
  function shares(days, dates) { return dates.some(function (d) { return days.indexOf(d.day) !== -1; }); }
  /** The same date listed twice (two records with the same title, one of them cancelled): keep one, the one that is on. */
  function dedupe(list, keyOf) {
    var out = [], at = Object.create(null);
    list.forEach(function (x) {
      var k = keyOf(x), i = at[k];
      if (i === undefined) { at[k] = out.length; out.push(x); } else if (out[i].cancelled && !x.cancelled) out[i] = x;
    });
    return out;
  }
  function dateKey(d) { return d.key + '|' + d.end + '|' + words(d.place).join(' '); }

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
  /** A built event as its data-ev-* attributes describe it (p_events.live_data). */
  function builtInfo(el) {
    var g = function (k) { return el.getAttribute('data-ev-' + k) || ''; };
    var start = TIME.test(g('start')) ? g('start') : '', end = END.test(g('end')) ? g('end') : '';
    return { el: el, fold: fold(g('title')), days: g('days').split(' '), status: g('status'), start: start, end: end,
             known: words(g('place') + ' ' + g('place-short')), evs: [] };
  }
  /** The built event's date on that day, in the shape check() gives the feed's dates. */
  function builtDate(b, day) { return b.start ? span(day, dayInfo(day), b.start, b.end) : { day: day, end: '' }; }
  function sameTimes(d, b) { return d.start === b.start && d.end === b.end; }
  /** What the server says about the status that the built text does not: CANCELLED; CLEAR (the server has no status
      where the built page shows one); its status when it differs; or "" (leave as built). */
  var CANCELLED = {}, CLEAR = {};
  function news(evs, builtStatus) {
    if (evs.every(function (ev) { return ev.cancelled; })) return CANCELLED;
    var on = evs.filter(function (ev) { return !ev.cancelled; });
    for (var i = 0; i !== on.length; i++) {
      if (on[i].status && fold(on[i].status) !== fold(builtStatus)) return on[i].status;
    }
    if (builtStatus && on.every(function (ev) { return !ev.status; })) return CLEAR;
    return '';
  }

  function apply(feed) {
    // a visitor who came to a card by its #anchor stays on it while cards are hidden or added above it
    var target = anchor(), top = target && target.getClientRects().length ? target.getBoundingClientRect().top : null;
    eventsPage(feed.events, feed.at);
    homePage(feed.events, toronto(new Date()));
    if (top !== null && target.getClientRects().length) {
      var moved = target.getBoundingClientRect().top - top;
      if (Math.abs(moved) >= 1) window.scrollBy(0, moved);
    }
  }
  function anchor() {
    var id = location.hash.slice(1);
    if (!id) return null;
    try { return document.getElementById(decodeURIComponent(id)); } catch (e) { return null; }
  }

  // ------------------------------------------------------------------ Events & Programs: the cards
  // The server lists upcoming dates only, so this list takes its dates as they come; whether a built date is over
  // is judged by the server's clock (the feed's generatedAt), never the visitor's (a wrong device clock changes nothing
  // here). Home keeps its rule that hides a date once it is over.
  function eventsPage(events, at) {
    var list = document.getElementById('ev-list');
    if (!list || !document.getElementById('ev-tpl-card')) return;
    var built = [].slice.call(list.querySelectorAll('article[data-ev-title]')).map(function (el, i) { var b = builtInfo(el); b.order = i; return b; });
    var items = [];
    events.forEach(function (ev) {
      var found = false;
      built.forEach(function (b) { if (b.fold === ev.fold && shares(b.days, ev.dates)) { b.evs.push(ev); found = true; } });
      if (!found) items.push({ key: ev.dates[0].key, order: 1000 + ev.index, el: newCard(ev, ev.dates) });
    });
    built.forEach(function (b) {
      if (!b.evs.length) { hide(b.el); return; }   // staff took it down
      var dates = [];
      b.evs.forEach(function (ev) { dates = dates.concat(ev.dates); });
      dates = dedupe(dates.sort(byKey), dateKey);
      var first = dates[0];
      items.push({ key: first.key, order: b.order, el: b.el });
      var s = news(b.evs, b.status), st = part(b.el, 'status');
      if (st && s === CLEAR) st.hidden = true;
      else if (st && s) say(st, s === CANCELLED ? 'This event is cancelled.' : sentence(s));
      if (s === CANCELLED) [].forEach.call(b.el.querySelectorAll('a.btn'), hide);   // no booking for a cancelled event
      if (first.day !== b.days[0]) tile(b.el.querySelector('.ev-d'), first.info);
      redrawWhen(b, dates, at);
    });
    items.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.order - b.order; });
    items.forEach(function (it) { if (it.el) list.appendChild(it.el); });
  }

  /** A built card's when and where lines, redrawn from the server's dates where they differ (the rest of the card's
      designed text stays). The clock line (doors open, a sensory-friendly hour, the November dates) describes the built
      times, so it goes when the days or times change; the flyer prints the built days, times and place, so it goes
      whenever they are redrawn (the Facebook post stays linked, as the source). */
  function redrawWhen(b, dates, at) {
    var mixed = dates.some(function (d) { return d.cancelled; }) && dates.some(function (d) { return !d.cancelled; });
    var live = b.days.filter(function (day) { return !over(builtDate(b, day), at); });   // built dates the server should still list
    var timesOk = !mixed && dates.length === live.length && dates.every(function (d, i) { return d.day === live[i] && sameTimes(d, b); });
    var placeOk = dates.every(function (d) { return !d.place || samePlace(d.place, b.known); });
    if (timesOk && placeOk) return;
    var flyer = b.el.querySelector('a.ev-f');
    if (flyer) hide(flyer);
    var w = whenLines(dates, mixed), whenRow = part(b.el, 'when-row'), noteRow = part(b.el, 'note-row'), whereRow = part(b.el, 'where-row');
    if (whenRow && (!timesOk || w.placed)) {
      rowText(whenRow, w.lines[0]);
      for (var i = 1, after = whenRow; i < w.lines.length; i++) {
        var row = whenRow.cloneNode(true);
        row.removeAttribute('data-slot');
        rowText(row, w.lines[i]);
        after.parentNode.insertBefore(row, after.nextSibling);
        after = row;
      }
    }
    if (noteRow && !timesOk) hide(noteRow);
    if (whereRow) {
      if (w.placed) hide(whereRow);   // each when line names its place
      else if (w.where && !samePlace(w.where, b.known)) rowText(whereRow, w.where);
    }
  }

  function newCard(ev, dates) {
    var el = fromTemplate('ev-tpl-card');
    if (!el) return null;
    tile(el.querySelector('.ev-d'), dates[0].info);
    var tag = part(el, 'tag');
    if (ev.program) tag.textContent = ev.program; else drop(tag);
    part(el, 'title').textContent = ev.title;
    var whenRow = part(el, 'when-row'), whereRow = part(el, 'where-row'), w = whenLines(dates, false);
    w.lines.forEach(function (line, i) {
      var row = i ? whenRow.cloneNode(true) : whenRow;
      if (i) row.removeAttribute('data-slot');
      rowText(row, line);
      if (i) whereRow.parentNode.insertBefore(row, whereRow);
    });
    if (w.where) rowText(whereRow, w.where); else drop(whereRow);
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
        b = byKeyAttr[k] = builtInfo(r);
        b.key = k;
        b.rows = Object.create(null);
        b.href = a ? a.getAttribute('href') : '';
        builtEvents.push(b);
      }
      b.rows[r.getAttribute('data-day')] = r;
    });
    var occ = [];
    events.forEach(function (ev) {
      ev.built = builtEvents.filter(function (b) { return b.fold === ev.fold && shares(b.days, ev.dates); });
      ev.dates.forEach(function (d) { if (!over(d, now)) occ.push({ ev: ev, d: d, key: d.key, order: ev.index * 100 + d.di, cancelled: ev.cancelled }); });
    });
    occ.sort(function (a, b) { return a.key < b.key ? -1 : a.key > b.key ? 1 : a.order - b.order; });
    occ = dedupe(occ, function (o) { return o.ev.fold + '|' + dateKey(o.d); });
    // each built row (and its "Up next" card) goes to one date on its day: the one at the built start time, else the first
    builtEvents.forEach(function (b) {
      Object.keys(b.rows).forEach(function (day) {
        var on = occ.filter(function (o) { return !o.row && o.d.day === day && o.ev.built.indexOf(b) !== -1; });
        var pick = on.filter(function (o) { return o.d.start === b.start; })[0] || on[0];
        if (pick) { pick.row = b.rows[day]; pick.b = b; }
      });
    });
    function target(ev) { return ev.built.length ? ev.built[0].href : ev.href; }   // the built card on Events & Programs, else the server's page

    // Up next: the first date still to come that is not cancelled
    var next = null, nextEl = null, i;
    for (i = 0; i !== occ.length; i++) if (!occ[i].ev.cancelled) { next = occ[i]; break; }
    if (next) {
      nextEl = next.row && document.getElementById('next-' + next.b.key + '-' + next.d.day);
      if (nextEl) refresh(nextEl, next, sentence, function (d) { return dlong(d.info) + ' \u00b7 ' + times(d); });
      else nextEl = newNext(next);   // its link: the event's page on the server
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
      var row = o.row;
      if (row) {
        row.style.display = '';   // the built script hides rows it showed as "Up next" or found over
        refresh(row, o, null, times);
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

  /** A built "Up next" card or row, brought up to the server's status, times and place for its date. On a card the
      when slot is "when-row" (day and times) and the place "where-row"; on a row they are "time" and "place". */
  function refresh(el, o, statusWords, whenWords) {
    var b = o.b, s = news([o.ev], b.status), st = part(el, 'status');
    if (st && s === CLEAR) st.hidden = true;
    else if (st && s) say(st, s === CANCELLED ? 'Cancelled' : statusWords ? statusWords(s) : s);
    var when = part(el, 'when-row') || part(el, 'time'), where = part(el, 'where-row') || part(el, 'place');
    if (when && !sameTimes(o.d, b)) {
      if (when.getAttribute('data-slot') === 'when-row') rowText(when, whenWords(o.d)); else when.textContent = whenWords(o.d);
    }
    if (where && o.d.place && !samePlace(o.d.place, b.known)) {
      if (where.getAttribute('data-slot') === 'where-row') rowText(where, o.d.place); else where.textContent = o.d.place;
      where.hidden = false;
    }
  }

  function newNext(o) {
    var el = fromTemplate('ev-tpl-next');
    if (!el) return null;
    tile(el.querySelector('.ev-d'), o.d.info);
    part(el, 'title').textContent = o.ev.title;
    rowText(part(el, 'when-row'), dlong(o.d.info) + ' \u00b7 ' + times(o.d));
    if (o.d.place) rowText(part(el, 'where-row'), o.d.place); else drop(part(el, 'where-row'));
    if (o.ev.status) say(part(el, 'status'), sentence(o.ev.status)); else drop(part(el, 'status'));
    if (o.ev.summary) part(el, 'summary').textContent = o.ev.summary; else drop(part(el, 'summary'));
    link(part(el, 'link'), o.ev.href, true);
    return el;
  }

  function newRow(o, href, outside) {
    var el = fromTemplate('ev-tpl-row');
    if (!el) return null;
    part(el, 'time').textContent = times(o.d);
    part(el, 'title').textContent = o.ev.title;
    if (o.d.place) part(el, 'place').textContent = o.d.place; else part(el, 'place').hidden = true;
    var st = part(el, 'status');
    if (o.ev.cancelled) say(st, 'Cancelled'); else if (o.ev.status) say(st, o.ev.status); else drop(st);
    link(el.querySelector('a'), href, outside);
    return el;
  }
})();
