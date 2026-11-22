"""Render pages at a given width and report elements that stick out past the viewport or are squeezed.
usage: rcheck.py <width> [page ...] [--shot]   (writes preview/<page>_<width>.png with --shot)"""
import sys, json
from playwright.sync_api import sync_playwright
P='/home/claude/iipct_work/preview/'
W=int(sys.argv[1]); keys=[a for a in sys.argv[2:] if not a.startswith('--')]; shot='--shot' in sys.argv
if not keys:
    import os
    keys=[f[:-5] for f in sorted(os.listdir(P)) if f.endswith('.html')]
JS='''() => {
  const W = document.documentElement.clientWidth, out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll('body *')) {
    if (el.closest('[aria-hidden="true"]') || el.closest('svg')) continue;
    const dt = el.closest('details:not([open])'); if (dt && !el.closest('summary')) continue;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    if (r.right > W + 1.5 || r.left < -1.5) {
      // report only the outermost offender in each subtree
      let p = el.parentElement, skip = false;
      while (p && p !== document.body) { if (seen.has(p)) { skip = true; break; } p = p.parentElement; }
      seen.add(el); if (skip) continue;
      out.push({t: el.tagName.toLowerCase(), c: (el.className||'').toString().slice(0,20), l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width),
                y: Math.round(r.top + scrollY), s: (el.innerText||'').replace(/\\s+/g,' ').slice(0,46)});
    }
  }
  // text clipped inside nowrap boxes
  const clip = [];
  for (const el of document.querySelectorAll('h1,h2,h3,p,a,span,li,button,label')) {
    if (el.closest('[aria-hidden="true"]')) continue;
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible' && el.clientWidth > 0)
      clip.push({t: el.tagName.toLowerCase(), s: (el.innerText||'').replace(/\\s+/g,' ').slice(0,40)});
  }
  // one-line headings and labels that run out of their box
  for (const el of document.querySelectorAll('.pg h2, .pg h3, .pg p, .pg li, .pg a, .pg span')) {
    if (el.closest('[aria-hidden="true"]') || el.closest('details:not([open])') || el.closest('svg')) continue;
    const cs = getComputedStyle(el); if (cs.whiteSpace !== 'nowrap' || cs.display === 'inline') continue;
    const par = el.parentElement.getBoundingClientRect(), r = el.getBoundingClientRect();
    if (r.width > 1 && (el.scrollWidth > el.clientWidth + 2 || r.right > par.right + 3)) clip.push({t: 'NOWRAP ' + el.tagName.toLowerCase(), s: (el.innerText||'').replace(/\s+/g,' ').slice(0,40)});
  }
  // content cut off by a box that hides its overflow (the page root is exempt: it clips decoration on purpose)
  for (const box of document.querySelectorAll('.pg *')) {
    const cs = getComputedStyle(box); if (cs.overflowX !== 'hidden' && cs.overflowX !== 'clip') continue;
    if (box.closest('[aria-hidden="true"]') || box.closest('details:not([open])')) continue;
    const br = box.getBoundingClientRect(); if (br.width < 1) continue;
    for (const el of box.querySelectorAll('h1,h2,h3,p,a,span,li,button,label,input,select,textarea,img')) {
      if (el.closest('[aria-hidden="true"]') || el.closest('svg')) continue;
      const pos = getComputedStyle(el).position; if (pos === 'absolute') continue;
      const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
      if (r.right > br.right + 1.5 || r.left < br.left - 1.5) { clip.push({t: 'CUT ' + el.tagName.toLowerCase(), s: (el.innerText||el.placeholder||el.alt||'').replace(/\s+/g,' ').slice(0,40)}); break; }
    }
  }
  return {W, h: Math.ceil(document.documentElement.scrollHeight), out: out.slice(0, 14), n: out.length, clip: clip.slice(0,8)};
}'''
res={}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--disable-gpu','--allow-file-access-from-files'])
    for k in keys:
        pg = br.new_page(viewport={'width':W,'height':900}, device_scale_factor=1)
        pg.goto('file://'+P+k+'.html'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        r = pg.evaluate(JS); res[k]=r
        print(f"{k:9s} w={W} h={r['h']:5d} offenders={r['n']}" + (f" clip={len(r['clip'])}" if r['clip'] else ''))
        for o in r['out']: print(f"     {o['t']}.{o['c']:<10s} l={o['l']:5d} r={o['r']:5d} w={o['w']:4d} y={o['y']:5d} | {o['s']}")
        for c in r['clip']: print(f"     CLIP {c['t']} | {c['s']}")
        if shot: pg.screenshot(path=f'{P}{k}_{W}.png', full_page=True)
        pg.close()
    br.close()
json.dump(res, open(f'{P}rcheck_{W}.json','w'))
