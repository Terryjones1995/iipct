"""Render the exported static site (with local copies of the web fonts) and report page heights and broken images/links."""
import sys, os, re, json
from playwright.sync_api import sync_playwright
SITE = os.path.abspath(sys.argv[1]) + '/'
FDIR = '/home/claude/iipct_work/fonts/node_modules'
faces = ''
for fam, pkg in (('Newsreader', 'newsreader'), ('DM Sans', 'dm-sans')):
    for st in ('normal', 'italic'):
        faces += f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:100 1000;src:url('file://{FDIR}/@fontsource-variable/{pkg}/files/{pkg}-latin-opsz-{st}.woff2') format('woff2');}}\n"
faces += f"@font-face{{font-family:'Kaushan Script';src:url('file://{FDIR}/@fontsource/kaushan-script/files/kaushan-script-latin-400-normal.woff2') format('woff2');}}\n"
pages = sorted(f for f in os.listdir(SITE) if f.endswith('.html'))
ref = json.load(open('/home/claude/iipct_work/preview/heights.json'))
bad = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files'])
    ctx = br.new_context(viewport={'width': 1440, 'height': 900})
    ctx.route('**/fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=faces))
    for f in pages:
        row = []
        for w in (1440, 820, 390):
            pg = ctx.new_page(); pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto('file://' + SITE + f); pg.wait_for_load_state('load'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
            h = pg.evaluate('Math.ceil(document.documentElement.scrollHeight)')
            broken = pg.evaluate('[...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute("src"))')
            sw = pg.evaluate('document.documentElement.scrollWidth')
            row.append(h)
            if broken or sw > w + 1: bad += 1; print('  PROBLEM', f, w, broken[:3], 'scrollWidth', sw)
            if f == 'index.html' and w in (1440, 390): pg.screenshot(path=f'/home/claude/iipct_work/preview/_site_index_{w}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': 700})
            pg.close()
        print(f'{f:42s} {row}')
    br.close()
# links between pages
names = set(pages)
for f in pages:
    for h in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', open(SITE + f).read()):
        if not h.startswith('http') and h not in names: bad += 1; print('  missing link target', f, '->', h)
print('problems:', bad, '| canvas heights for index:', ref['home'], ref['home@820'], ref['home@390'])
