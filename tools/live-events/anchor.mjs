// Proof that a visitor who lands on a card by its #anchor stays on it while the reader hides or adds cards above it.
// Run through tools/live-events/run-anchor.sh (it starts the stand-in); never shipped.
// usage: node anchor.mjs <out.json> <port> <scenario-file> <site-path> [<site-path> ...]
// <site-path>: the folder the stand-in serves the pages from, under https://terryjones1995.github.io/ ("iipct" = this
// tree; "base" = the second folder given to the stand-in, here a copy with an older reader for the control).
// For each site, Chrome with its own scroll anchoring on (default) and off (as Safari has none): open
// events-programs.html#social-songs-dance, wait until the browser has scrolled there, let the feed answer 2 s late
// with a card hidden above (missing) or added above (new), then measure how far the card moved on screen.
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire('/home/terry/tasks/iipct/tools/');
const { chromium } = require('playwright-core');
const [OUT, PORT, SCEN, ...SITES] = process.argv.slice(2);
const results = [];
for (const anchoring of [true, false]) {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: true,
    args: ['--no-sandbox', '--disable-gpu', `--host-resolver-rules=MAP iipct.pixelelite.ca 127.0.0.1:${PORT},MAP terryjones1995.github.io 127.0.0.1:${PORT}`,
      ...(anchoring ? [] : ['--disable-features=ScrollAnchoring'])] });
  for (const site of SITES) {
    for (const sc of ['missing', 'new']) {
      for (const w of [390, 1440]) {
        fs.writeFileSync(SCEN, `${sc}@2000`);
        const ctx = await browser.newContext({ viewport: { width: w, height: w < 1000 ? 844 : 900 }, ignoreHTTPSErrors: true, hasTouch: w < 1000 });
        const page = await ctx.newPage();
        const errors = [];
        page.on('pageerror', (e) => errors.push(String(e).slice(0, 160)));
        await page.goto(`https://terryjones1995.github.io/${site}/events-programs.html#social-songs-dance`, { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(600);
        const before = await page.evaluate(() => ({ top: document.getElementById('social-songs-dance').getBoundingClientRect().top, y: scrollY, state: document.documentElement.getAttribute('data-live-events') }));
        await page.waitForFunction(() => document.documentElement.hasAttribute('data-live-events'), null, { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(400);
        const after = await page.evaluate(() => ({ top: document.getElementById('social-songs-dance').getBoundingClientRect().top, y: scrollY, state: document.documentElement.getAttribute('data-live-events'),
          cards: [...document.querySelectorAll('#ev-list > article')].filter((a) => getComputedStyle(a).display !== 'none').length }));
        const r = { site, anchoring, scenario: sc, width: w, stateBefore: before.state, stateAfter: after.state, cards: after.cards, topBefore: Math.round(before.top), topAfter: Math.round(after.top), moved: Math.round(after.top - before.top), errors };
        results.push(r);
        console.log(`${site.padEnd(6)} anchoring=${String(anchoring).padEnd(5)} ${sc.padEnd(8)} ${String(w).padStart(4)}  reader ${before.state}->${after.state}  cards=${after.cards}  card top ${r.topBefore} -> ${r.topAfter} (moved ${r.moved})  errors=${errors.length}`);
        await ctx.close();
      }
    }
  }
  await browser.close();
}
fs.writeFileSync(OUT, JSON.stringify(results, null, 1));
