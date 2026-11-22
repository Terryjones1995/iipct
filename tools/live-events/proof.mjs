// Proof for the live events reader (assets/js/live-events.js) against the local stand-in feed (standin.py).
// Run through tools/live-events/run-proof.sh (it starts the stand-in); never shipped.
// usage: node proof.mjs <out-dir> <port> <scenario-file>
// For each scenario and width: loads Home and Events & Programs at their published address (the stand-in serves
// them), waits for the reader to finish (<html data-live-events>), then records: what the reader did, console
// messages, page errors, failed requests, sideways overflow at that width (and at all 21 device widths for the
// scenarios that change the page), the bottom bar's box, document.title, and screenshots: the events block whole
// (for pixel comparison with the same block of 4fcfd8d, served from /base/) and window-sized tiles while scrolling.
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire('/home/terry/tasks/iipct/tools/');
const { chromium } = require('playwright-core');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');

const [OUT, PORT, SCEN_FILE] = process.argv.slice(2);
fs.mkdirSync(OUT, { recursive: true });
const SAME = ['down', 'empty', 'equal', 'seed', 'slow', 'bad-json', 'html-type', 'wrong-site', 'foreign-href', 'dotdot', 'dotdot-encoded', 'big', 'big-chunked', 'proto'];
const CHANGED = ['missing', 'cancelled', 'status', 'new', 'startonly', 'markup',
  'nextday', 'longfields', 'midnight', 'timechanged', 'datedropped', 'statuscleared', 'secondsession', 'duplicates'];
const TILES = new Set(['down', 'empty', 'equal', ...CHANGED]);         // window-sized tiles for these; the rest are proven by pixels
const HEIGHT = { 360: 800, 390: 844, 768: 1024, 820: 1180, 1440: 900 };
const ALL_WIDTHS = [[320, 568], [360, 800], [375, 667], [390, 844], [412, 915], [430, 932], [667, 375], [844, 390], [932, 430], [600, 960],
  [768, 1024], [820, 1180], [912, 1368], [1024, 768], [1180, 820], [1280, 720], [1366, 768], [1440, 900], [1536, 864], [1920, 1080], [2560, 1440]];
const PAGES = { 'index.html': '#ev-home', 'events-programs.html': '#upcoming' };

const browser = await chromium.launch({
  executablePath: '/usr/bin/google-chrome', headless: true,
  args: ['--no-sandbox', '--disable-gpu', `--host-resolver-rules=MAP iipct.pixelelite.ca 127.0.0.1:${PORT},MAP terryjones1995.github.io 127.0.0.1:${PORT}`],
});
const results = [];

// Fonts come from Google over the network. Two loads can be served font files that render a few glyph edges differently
// (seen: one capture of 4fcfd8d differing from every page of the run in antialiasing only), so every load in a run gets
// the same bytes: the first answer for each font address is kept and given to every later request.
const FONTS = new Map();
async function fontRoute(route) {
  const url = route.request().url();
  try {
    let hit = FONTS.get(url);
    if (!hit) {
      const resp = await route.fetch();
      const headers = Object.fromEntries(Object.entries(resp.headers()).filter(([k]) => !/^(content-encoding|content-length|transfer-encoding)$/i.test(k)));
      hit = { status: resp.status(), headers, body: await resp.body() };
      if (resp.ok()) FONTS.set(url, hit);
    }
    await route.fulfill(hit);
  } catch (e) {
    await route.abort().catch(() => {});
  }
}

async function load(url, w, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: w, height: HEIGHT[w] || 900 }, deviceScaleFactor: 1, ignoreHTTPSErrors: true,
    hasTouch: w < 1100, javaScriptEnabled: opts.js !== false });
  await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, fontRoute);
  const page = await ctx.newPage();
  const log = { console: [], pageerror: [], failed: [] };
  page.on('console', (m) => { if (['error', 'warning'].includes(m.type())) log.console.push(`${m.type()}: ${m.text().slice(0, 200)}`); });
  page.on('pageerror', (e) => log.pageerror.push(String(e).slice(0, 200)));
  page.on('requestfailed', (r) => log.failed.push(`${r.url().slice(0, 90)} ${r.failure() ? r.failure().errorText : ''}`));
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  // images below the first screen load lazily: load them all now, so every screenshot shows them (as devices.mjs does)
  await page.evaluate(async () => {
    const imgs = [...document.images];
    for (const im of imgs) if (im.loading === 'lazy') im.loading = 'eager';
    await Promise.all(imgs.map((im) => im.complete ? null : new Promise((res) => { im.addEventListener('load', res, { once: true }); im.addEventListener('error', res, { once: true }); setTimeout(res, 8000); })));
  });
  // a lazy image that was never requested can report complete=true: wait until every image has really arrived and decoded
  await page.waitForFunction(() => [...document.images].every((im) => im.complete && im.naturalWidth > 0), null, { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => Promise.all([...document.images].map((im) => im.decode().catch(() => {}))));
  let state = null;
  if (opts.js !== false && !url.includes('/base/')) {
    await page.waitForFunction(() => document.documentElement.hasAttribute('data-live-events'), null, { timeout: 15000 }).catch(() => {});
    state = await page.evaluate(() => document.documentElement.getAttribute('data-live-events'));
  }
  await page.waitForTimeout(300);
  return { ctx, page, log, state };
}

async function blockShot(page, sel, file) {
  const el = page.locator(sel);
  await el.screenshot({ path: file, animations: 'disabled' });
}

async function tiles(page, sel, prefix) {
  const box = await page.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return { top: r.top + scrollY, h: r.height }; }, sel);
  const vh = page.viewportSize().height;
  const files = [];
  for (let y = box.top, i = 0; y < box.top + box.h && i < 12; y += vh, i++) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(150);
    const f = `${prefix}-${String(i).padStart(2, '0')}.png`;
    await page.screenshot({ path: f });
    files.push(f);
  }
  return files;
}

function diff(a, b) {
  const A = PNG.sync.read(fs.readFileSync(a)), B = PNG.sync.read(fs.readFileSync(b));
  if (A.width !== B.width || A.height !== B.height) return { same: false, why: `size ${A.width}x${A.height} vs ${B.width}x${B.height}` };
  const n = pixelmatch(A.data, B.data, null, A.width, A.height, { threshold: 0 });
  return { same: n === 0, pixels: n };
}

async function facts(page) {
  return page.evaluate(() => {
    const bar = document.querySelector('.mbar'), r = bar && bar.getBoundingClientRect();
    const blk = document.querySelector('#ev-home') || document.querySelector('#upcoming');
    return {
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      title: document.title,
      bar: r && getComputedStyle(bar).display !== 'none' ? `${Math.round(r.top)},${Math.round(r.height)}` : 'hidden',
      imgsInBlock: blk ? blk.querySelectorAll('img').length : -1,
      scriptsInBlock: blk ? blk.querySelectorAll('script').length : -1,
      cards: [...document.querySelectorAll('#ev-list > article')].filter((a) => getComputedStyle(a).display !== 'none').map((a) => a.querySelector('h3').textContent),
      cardWhen: [...document.querySelectorAll('#ev-list > article')].filter((a) => getComputedStyle(a).display !== 'none').map((a) => a.querySelector('h3').textContent.slice(0, 40) + ' | '
        + [...a.querySelectorAll('[data-slot="when"] > span')].filter((r) => getComputedStyle(r).display !== 'none').map((r) => r.textContent.replace(/\s+/g, ' ').trim()).join(' / ')
        + ' | ' + [...a.querySelectorAll('[data-slot="status"]')].filter((x) => !x.hidden && getComputedStyle(x).display !== 'none').map((x) => x.textContent).join(' / ')),
      upNextWhen: (() => { const c = [...document.querySelectorAll('#ev-next-col > div')].find((d) => !d.hidden); return c ? [...c.querySelectorAll('.t-s, [data-slot="status"]')].filter((x) => !x.hidden && getComputedStyle(x).display !== 'none').map((x) => x.textContent.replace(/\s+/g, ' ').trim()).join(' / ') : null; })(),
      upNext: (() => { const c = [...document.querySelectorAll('#ev-next-col > div')].find((d) => !d.hidden); return c ? c.querySelector('h3').textContent + ' | ' + (c.querySelector('.ev-when') || {}).textContent : null; })(),
      rows: [...document.querySelectorAll('#ev-rows li[data-group]')].filter((g) => getComputedStyle(g).display !== 'none')
        .map((g) => g.firstElementChild.textContent + ': ' + [...g.querySelectorAll('li')].filter((r) => getComputedStyle(r).display !== 'none')
          .map((r) => r.querySelector('a').textContent.replace(/\s+/g, ' ').trim() + ' -> ' + r.querySelector('a').getAttribute('href')).join(' || ')),
      statuses: [...document.querySelectorAll('[data-slot="status"]')].filter((s) => !s.hidden && s.isConnected && s.closest('template') === null && getComputedStyle(s).display !== 'none').map((s) => s.textContent),
    };
  });
}

// 1. the page before the reader (4fcfd8d), JavaScript on and off
for (const [pg, sel] of Object.entries(PAGES)) {
  for (const w of [360, 390, 768, 820, 1440]) {
    const { ctx, page } = await load(`https://terryjones1995.github.io/base/${pg}`, w);
    fs.mkdirSync(`${OUT}/cmp/base`, { recursive: true });
    await blockShot(page, sel, `${OUT}/cmp/base/${pg}-${w}.png`);
    await ctx.close();
  }
  for (const w of [390, 1440]) {
    const { ctx, page } = await load(`https://terryjones1995.github.io/base/${pg}`, w, { js: false });
    fs.mkdirSync(`${OUT}/cmp/base-nojs`, { recursive: true });
    await blockShot(page, sel, `${OUT}/cmp/base-nojs/${pg}-${w}.png`);
    await ctx.close();
  }
}

// 2. the new pages with JavaScript off (the reader cannot run): must equal 4fcfd8d with JavaScript off
fs.writeFileSync(SCEN_FILE, 'equal');
for (const [pg, sel] of Object.entries(PAGES)) {
  for (const w of [390, 1440]) {
    const { ctx, page } = await load(`https://terryjones1995.github.io/iipct/${pg}`, w, { js: false });
    fs.mkdirSync(`${OUT}/cmp/nojs`, { recursive: true });
    const f = `${OUT}/cmp/nojs/${pg}-${w}.png`;
    await blockShot(page, sel, f);
    results.push({ scenario: 'javascript-off', page: pg, width: w, vsBase: diff(f, `${OUT}/cmp/base-nojs/${pg}-${w}.png`) });
    await ctx.close();
  }
}

// 3. every scenario
const ONLY = process.env.ONLY ? process.env.ONLY.split(',') : null;
for (const sc of [...SAME, ...CHANGED].filter((x) => !ONLY || ONLY.includes(x))) {
  fs.writeFileSync(SCEN_FILE, sc);
  const widths = CHANGED.includes(sc) ? [360, 390, 768, 820, 1440] : [390, 1440];
  for (const [pg, sel] of Object.entries(PAGES)) {
    for (const w of widths) {
      const { ctx, page, log, state } = await load(`https://terryjones1995.github.io/iipct/${pg}`, w);
      fs.mkdirSync(`${OUT}/cmp/${sc}`, { recursive: true });
      const f = `${OUT}/cmp/${sc}/${pg}-${w}.png`;
      await blockShot(page, sel, f);
      const r = { scenario: sc, page: pg, width: w, state, console: [...log.console], pageerror: [...log.pageerror], failed: [...log.failed], ...(await facts(page)), vsBase: diff(f, `${OUT}/cmp/base/${pg}-${w}.png`) };
      if (TILES.has(sc) && (w === 390 || w === 1440 || CHANGED.includes(sc))) {
        fs.mkdirSync(`${OUT}/shots/${sc}`, { recursive: true });
        r.tiles = (await tiles(page, sel, `${OUT}/shots/${sc}/${pg.replace('.html', '')}-${w}`)).length;
      }
      if (CHANGED.includes(sc) && w === 390) {   // all 21 device widths: no sideways scrolling
        r.overflow21 = [];
        for (const [vw, vh] of ALL_WIDTHS) {
          await page.setViewportSize({ width: vw, height: vh });
          await page.waitForTimeout(80);
          const o = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
          if (o > 1) r.overflow21.push(`${vw}:+${o}`);
        }
      }
      results.push(r);
      await ctx.close();
      console.log(`${sc.padEnd(13)} ${pg.padEnd(22)} ${String(w).padStart(4)}  reader=${state}  sameAsBase=${r.vsBase.same}${r.vsBase.pixels !== undefined ? ' (' + r.vsBase.pixels + ' px differ)' : ' (' + (r.vsBase.why || '') + ')'}  overflow=${r.overflow}  console=${r.console.length} pageerror=${r.pageerror.length} failed=${r.failed.length}${r.overflow21 ? ' overflow21=' + (r.overflow21.join(' ') || 'none') : ''}`);
    }
  }
}
await browser.close();
fs.writeFileSync(`${OUT}/proof.json`, JSON.stringify(results, null, 1));
console.log('wrote', `${OUT}/proof.json`);
