// Hover and keyboard-focus check: every visible link, button and summary must answer the pointer (and keyboard focus)
// with a colour change.
// usage: node tools/hover-check.mjs <site-dir> [--width 1440] [--pages index.html,contact.html] [--json out.json] [--no-focus]
//
// In real Chrome, on every page of the site folder: for each visible <a>, <button> and <summary> (and the header's
// dropdown items, opened the way a visitor opens them), the pointer is put on a neutral spot and the control's colours
// are read, then the pointer is put on the control and they are read again. Colours = what a visitor can see: the
// text colour of every element that holds text, background colour and image, the colour of every border that is
// drawn, underlines (line and colour), and the stroke and fill of icon shapes. At least one must change. The same
// comparison is made for keyboard focus (:focus-visible). Transitions are switched off while measuring, so the
// end state is read, not a frame in between.
// Exit 0 = every control changes; 1 = at least one does not (each is listed); 2 = the check itself failed.
// Canary: tools/hover-canary.sh removes one hover rule from a copy of the stylesheet and expects this check to fail.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(process.env.PLAYWRIGHT_FROM || '/home/terry/tasks/iipct/tools/');
const { chromium } = require('playwright-core');

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const SITE = path.resolve(argv[0] || '.') + '/';
const WIDTH = +opt('--width', 1440), HEIGHT = 900;
const ONLY = opt('--pages', '') ? opt('--pages', '').split(',') : null;
const JSON_OUT = opt('--json', '');
const FOCUS = !argv.includes('--no-focus');

const pages = fs.readdirSync(SITE).filter(f => f.endsWith('.html') && (!ONLY || ONLY.includes(f))).sort();
if (!pages.length) { console.error('hover-check: no pages found in', SITE); process.exit(2); }

// ---- in the page
const PREP = () => {
  const VIS = (el) => {
    if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
    const dt = el.closest('details:not([open])'); if (dt && !(el.tagName === 'SUMMARY' && el.parentElement === dt)) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    const top = r.top + scrollY, left = r.left + scrollX;
    return top + r.height > 0 && left + r.width > 0 && left < document.documentElement.scrollWidth;   // off-screen (the skip link until focused) is not visible
  };
  const list = [];
  for (const el of document.querySelectorAll('a[href], button, summary')) {
    const inMenu = el.closest('.nvm');
    if (inMenu) continue;                       // dropdown items: tested with their menu open (below)
    if (!VIS(el)) continue;
    el.dataset.hv = list.length; list.push({ i: list.length, menu: null });
  }
  // header dropdown items: visible once a visitor points at the menu's own link
  document.querySelectorAll('.nvi').forEach((nvi, m) => {
    nvi.querySelectorAll('.nvm a[href]').forEach(a => { a.dataset.hv = list.length; list.push({ i: list.length, menu: m }); });
    nvi.dataset.nvi = m;
  });
  return list.length;
};

const SNAP = (i) => {
  const el = document.querySelector(`[data-hv="${i}"]`);
  const facts = [];
  const hasText = (e) => [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim());
  const drawn = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
  const box = (e, who) => {
    const c = getComputedStyle(e);
    if (!drawn(e)) return;
    facts.push([who, 'background', c.backgroundColor + ' ' + c.backgroundImage]);
    for (const s of ['Top', 'Right', 'Bottom', 'Left'])
      if (parseFloat(c['border' + s + 'Width']) > 0 && c['border' + s + 'Style'] !== 'none') facts.push([who, 'border-' + s.toLowerCase(), c['border' + s + 'Color']]);
    const textInside = hasText(e) || e.querySelector('*') && [...e.querySelectorAll('*')].some(hasText);
    if (textInside) facts.push([who, 'underline', c.textDecorationLine === 'none' ? 'none' : c.textDecorationLine + ' ' + c.textDecorationColor]);
    if (hasText(e)) facts.push([who, 'text', c.color]);
  };
  const name = (e) => e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).join('.') : '');
  box(el, 'self');
  for (const d of el.querySelectorAll('*')) {
    if (d instanceof SVGElement) {
      if (d.tagName === 'svg' || !drawn(d)) continue;
      const c = getComputedStyle(d);
      if (c.stroke !== 'none' && parseFloat(c.strokeWidth) > 0) facts.push([name(d), 'icon-stroke', c.stroke]);
      if (c.fill !== 'none' && c.fillOpacity !== '0') facts.push([name(d), 'icon-fill', c.fill]);
      continue;
    }
    box(d, name(d));
  }
  return { facts, fv: el.matches(':focus-visible'), hover: el.matches(':hover') };
};

const INFO = (i) => {
  const el = document.querySelector(`[data-hv="${i}"]`);
  const t = (el.innerText || el.getAttribute('aria-label') || el.querySelector('img')?.alt || el.getAttribute('href') || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '';
  return { el: el.tagName.toLowerCase() + cls, t, href: (el.getAttribute('href') || '').slice(0, 60) };
};

// a point inside the control that the pointer really reaches (not covered by something else)
const AIM = (i) => {
  const el = document.querySelector(`[data-hv="${i}"]`);
  el.scrollIntoView({ block: 'center', inline: 'nearest' });
  const r = el.getBoundingClientRect();
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  for (const fy of [0.5, 0.3, 0.7, 0.15, 0.85]) for (const fx of [0.5, 0.25, 0.75, 0.1, 0.9]) {
    const x = r.left + r.width * fx, y = r.top + r.height * fy;
    if (x < 0 || y < 0 || x >= W || y >= H) continue;
    const hit = document.elementFromPoint(x, y);
    if (hit && (hit === el || el.contains(hit))) return { x, y };
  }
  return null;
};

// a neutral spot: over nothing a visitor could point at, nor anything whose :hover could recolour the control
const NEUTRAL = (i) => {
  const el = document.querySelector(`[data-hv="${i}"]`);
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  const BUSY = 'a,button,summary,input,select,textarea,label,details,form,.card,.nvi,.mbar,[tabindex]';
  for (const x of [3, W - 4, Math.round(W / 2)]) for (let y = 3; y < H; y += 37) {
    const hit = document.elementFromPoint(x, y);
    if (!hit || hit.closest(BUSY) || el.contains(hit)) continue;
    return { x, y };
  }
  return null;
};

const diff = (a, b) => {
  const out = [];
  const n = Math.max(a.length, b.length);
  for (let k = 0; k < n; k++) {
    const x = a[k], y = b[k];
    if (!x || !y || x[0] !== y[0] || x[1] !== y[1]) { out.push('layout changed'); break; }
    if (x[2] !== y[2]) out.push(`${x[0]} ${x[1]}: ${x[2]} -> ${y[2]}`);
  }
  return out;
};

const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files'] });
const report = { width: WIDTH, pages: {}, totals: { controls: 0, hoverFail: 0, focusFail: 0, unreachable: 0, focusNotVisible: 0 } };
try {
  for (const f of pages) {
    const ctx = await browser.newContext({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1, hasTouch: false });
    // only the site's own files: no outside requests, so every run sees the same page (the events reader falls back
    // to what the page already shows)
    await ctx.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
    const page = await ctx.newPage();
    await page.goto('file://' + SITE + f, { waitUntil: 'load', timeout: 60000 });
    await page.addStyleTag({ content: '*,*::before,*::after{transition:none !important;animation:none !important}' });
    await page.waitForTimeout(150);
    const pr = report.pages[f] = { controls: 0, hoverFail: [], focusFail: [], unreachable: [], focusNotVisible: [] };
    // hover-capable pointer? (the page's pointer-only rules sit behind @media (hover: hover))
    if (!(await page.evaluate(() => matchMedia('(hover: hover)').matches))) throw new Error('this browser does not report (hover: hover): the check would prove nothing');
    const n = await page.evaluate(PREP);
    const items = await page.evaluate(() => [...document.querySelectorAll('[data-hv]')].map(e => ({ i: +e.dataset.hv, menu: e.closest('.nvi') && e.closest('.nvm') ? +e.closest('.nvi').dataset.nvi : null })));
    for (const it of items) {
      const info = await page.evaluate(INFO, it.i);
      let restAt;
      if (it.menu !== null) {
        // open the dropdown the way a visitor does: point at the menu's own link, then read the item at rest
        await page.evaluate(m => document.querySelector(`[data-nvi="${m}"]`).scrollIntoView({ block: 'center' }), it.menu);
        restAt = await page.evaluate(m => { const r = document.querySelector(`[data-nvi="${m}"] > .nv`).getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; }, it.menu);
        await page.mouse.move(restAt.x, restAt.y);
        const vis = await page.evaluate(i => { const e = document.querySelector(`[data-hv="${i}"]`); return e.checkVisibility(); }, it.i);
        if (!vis) { pr.unreachable.push({ ...info, why: 'dropdown did not open' }); continue; }
      } else {
        await page.mouse.move(3, 3);
        await page.evaluate(i => document.querySelector(`[data-hv="${i}"]`).scrollIntoView({ block: 'center', inline: 'nearest' }), it.i);
        restAt = await page.evaluate(NEUTRAL, it.i);
        if (!restAt) { pr.unreachable.push({ ...info, why: 'no neutral spot on screen' }); continue; }
        await page.mouse.move(restAt.x, restAt.y);
      }
      const aim = await page.evaluate(AIM, it.i);
      if (!aim) { pr.unreachable.push({ ...info, why: 'covered: the pointer cannot reach it' }); continue; }
      // the aim scrolled the page: put the pointer back on the rest spot before reading the resting colours
      if (it.menu === null) { restAt = await page.evaluate(NEUTRAL, it.i); if (!restAt) { pr.unreachable.push({ ...info, why: 'no neutral spot on screen' }); continue; } }
      await page.mouse.move(restAt.x, restAt.y);
      const rest = await page.evaluate(SNAP, it.i);
      if (rest.hover) { pr.unreachable.push({ ...info, why: 'still hovered at the rest spot' }); continue; }
      await page.mouse.move(aim.x, aim.y);
      const hov = await page.evaluate(SNAP, it.i);
      pr.controls++;
      if (!hov.hover) { pr.unreachable.push({ ...info, why: 'pointer on it but :hover did not match' }); continue; }
      const d = diff(rest.facts, hov.facts);
      if (!d.length || d.includes('layout changed') && d.length === 1) pr.hoverFail.push(info);
      if (FOCUS) {
        // keyboard focus: a key press first, so Chrome treats the focus as keyboard focus (:focus-visible)
        await page.mouse.move(restAt.x, restAt.y);
        if (it.menu !== null) await page.mouse.move(restAt.x, restAt.y);
        await page.keyboard.press('Shift');
        await page.evaluate(i => document.querySelector(`[data-hv="${i}"]`).focus({ preventScroll: true }), it.i);
        const foc = await page.evaluate(SNAP, it.i);
        await page.evaluate(i => document.querySelector(`[data-hv="${i}"]`).blur(), it.i);
        if (!foc.fv) pr.focusNotVisible.push(info);
        else { const fd = diff(rest.facts, foc.facts); if (!fd.length || fd.includes('layout changed') && fd.length === 1) pr.focusFail.push(info); }
      }
    }
    for (const k of ['hoverFail', 'focusFail', 'unreachable', 'focusNotVisible']) report.totals[k] += pr[k].length;
    report.totals.controls += pr.controls;
    console.log(`${f.padEnd(40)} controls=${String(pr.controls).padStart(4)}  no hover change=${pr.hoverFail.length}  no focus change=${pr.focusFail.length}  unreachable=${pr.unreachable.length}`);
    await ctx.close();
  }
} catch (e) {
  console.error('hover-check failed:', e.stack || e);
  await browser.close();
  process.exit(2);
}
await browser.close();
if (JSON_OUT) fs.writeFileSync(JSON_OUT, JSON.stringify(report, null, 1));

const list = (k, title) => {
  const rows = Object.entries(report.pages).flatMap(([f, p]) => p[k].map(x => ({ f, ...x })));
  if (!rows.length) return;
  console.log(`\n${title} (${rows.length}):`);
  const groups = new Map();
  for (const r of rows) { const g = `${r.el} | ${r.t}${r.why ? ' | ' + r.why : ''}`; groups.set(g, [...(groups.get(g) || []), r.f]); }
  for (const [g, fs_] of groups) console.log(`  ${String(fs_.length).padStart(3)}x ${g.slice(0, 150)}   (${[...new Set(fs_)].slice(0, 4).join(', ')}${new Set(fs_).size > 4 ? ', ...' : ''})`);
};
list('hoverFail', 'controls without a hover change');
list('focusFail', 'controls without a keyboard-focus change');
list('focusNotVisible', 'controls where keyboard focus did not register as :focus-visible');
list('unreachable', 'controls the pointer could not reach (not counted as tested)');
const t = report.totals;
console.log(`\nAT ${WIDTH}px: ${t.controls} controls pointed at on ${pages.length} pages; ${t.hoverFail} controls without a hover change; ${t.focusFail} without a focus change; ${t.focusNotVisible} focus not visible; ${t.unreachable} unreachable`);
process.exit(t.hoverFail || t.focusFail || t.focusNotVisible || t.unreachable ? 1 : 0);
