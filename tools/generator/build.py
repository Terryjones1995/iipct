"""Build the artboard files + local previews, render them, and make side-by-side comparison tiles.
usage: build.py [page ...]   (page keys: home who services events contact careers board bpso)"""
import sys, os, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from PIL import Image

OUT = '/home/claude/iipct/project/'
PREV = '/home/claude/iipct_work/preview/'
MOCK = '/home/claude/iipct_src/zip/IIPCT_Full_Desktop_Rebrand_Package/01_Desktop_Page_Mockups/'
PAGES = {
 'home': ('p_home', 'page', 'Main.dc.html', '01_Home.png', 'Home'),
 'who': ('p_who', 'page', 'WhoWeAre.dc.html', '02_Who_We_Are.png', 'Who We Are'),
 'team': ('p_team', 'page', 'Team.dc.html', None, 'Our Team'),
 'services': ('p_services', 'page', 'Services.dc.html', '03_Services.png', 'Services'),
 'events': ('p_events', 'page', 'Events.dc.html', '04_Events_Programs.png', 'Events & Programs'),
 'contact': ('p_contact', 'page', 'Contact.dc.html', '05_Contact_Us.png', 'Contact Us'),
 'careers': ('p_careers', 'page', 'Careers.dc.html', '06_Career_Opportunities.png', 'Career Opportunities'),
 'board': ('p_board', 'page', 'Board.dc.html', '07_Board_of_Directors.png', 'Board of Directors'),
 'bpso': ('p_bpso', 'page', 'BPSO.dc.html', '08_BPSO.png', 'BPSO'),
 'primary': ('p_sub', 'primary', 'PrimaryCare.dc.html', None, 'Primary Medical Care'),
 'immun': ('p_sub', 'immunization', 'Immunization.dc.html', None, 'Immunization Program'),
 'wellbaby': ('p_sub', 'wellbaby', 'WellBaby.dc.html', None, 'Well Baby & Well Child'),
 'tb': ('p_sub', 'tb', 'TBTesting.dc.html', None, 'TB Testing'),
 'foot': ('p_sub', 'foot', 'FootCare.dc.html', None, 'Advanced Foot Care'),
 'retino': ('p_sub', 'retino', 'Retinopathy.dc.html', None, 'Diabetic Retinopathy Screening'),
 'outreach': ('p_sub', 'outreach', 'Outreach.dc.html', None, 'Outreach & Community Support'),
 'booking': ('p_legal', 'booking', 'Booking.dc.html', None, 'Schedule Your Visit'),
 'news': ('p_news', 'news', 'News.dc.html', None, 'News & Updates'),
 'post1': ('p_news', 'post_awards', 'NewsIPHCCAwards.dc.html', None, 'News: IPHCC Awards'),
 'post2': ('p_news', 'post_breast', 'NewsBreastScreening.dc.html', None, 'News: Breast Cancer Screening Event'),
 'privacy': ('p_legal', 'privacy', 'Privacy.dc.html', None, 'Privacy Policy'),
 'access': ('p_legal', 'accessibility', 'Accessibility.dc.html', None, 'Accessibility'),
 'sitemap': ('p_legal', 'sitemap', 'SiteMap.dc.html', None, 'Site Map'),
}
FRAMES = {'tablet': 820, 'phone': 390}      # extra artboards: the same page held to a device width
os.makedirs(OUT, exist_ok=True); os.makedirs(PREV, exist_ok=True)
keys = [k for k in sys.argv[1:] if k in PAGES] or list(PAGES)
render = '--no-render' not in sys.argv
hpath = PREV + 'heights.json'
heights = json.load(open(hpath)) if os.path.exists(hpath) else {}

bodies = {}
for k in keys:
    mod, func, fn, mock, label = PAGES[k]
    title, body = getattr(importlib.import_module(mod), func)()
    bodies[k] = (title, body)
    open(PREV + k + '.html', 'w').write(lib.preview_document(title, body))

if render and bodies:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files'])
        for k in bodies:
            pg = br.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
            pg.goto('file://' + PREV + k + '.html'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(350)
            h = pg.evaluate('Math.ceil(document.documentElement.scrollHeight)')
            ov = pg.evaluate('document.documentElement.scrollWidth')
            heights[k] = h
            pg.screenshot(path=PREV + k + '.png', full_page=True)
            print(f'{k}: height {h}px, scrollWidth {ov}')
            pg.close()
            for fw in FRAMES.values():
                pg = br.new_page(viewport={'width': fw, 'height': 1000}, device_scale_factor=1)
                pg.goto('file://' + PREV + k + '.html'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
                heights[f'{k}@{fw}'] = pg.evaluate('Math.ceil(document.documentElement.scrollHeight)')
                pg.screenshot(path=f'{PREV}{k}_{fw}.png', full_page=True)
                pg.close()
            if not PAGES[k][3] or '--cmp' not in sys.argv:
                continue
            # side-by-side tiles: mockup (left) vs build (right)
            mock = Image.open(MOCK + PAGES[k][3]).convert('RGB')
            mock = mock.crop((0, 36, 1055, 1482)).resize((1440, round(1446 * 1440 / 1055)), Image.LANCZOS)
            mine = Image.open(PREV + k + '.png').convert('RGB')
            H = max(mock.height, mine.height)
            band = 740
            i = 0
            for y in range(0, H, band):
                t = Image.new('RGB', (2890, band), '#FF00FF')
                if y < mock.height: t.paste(mock.crop((0, y, 1440, min(y + band, mock.height))), (0, 0))
                if y < mine.height: t.paste(mine.crop((0, y, 1440, min(y + band, mine.height))), (1450, 0))
                t = t.resize((1568, round(band * 1568 / 2890)), Image.LANCZOS)
                t.save(f'{PREV}{k}_cmp{i}.png'); i += 1
            print('  tiles:', i)
        br.close()
    json.dump(heights, open(hpath, 'w'))

FILES = [v[2] for v in PAGES.values()]
def relink(body, suffix):
    for f in FILES:
        body = body.replace(f'href="{f}"', f'href="{f[:-8]}-{suffix}.dc.html"')
    return body
for k, (title, body) in bodies.items():
    h = heights.get(k, 2200)
    open(OUT + PAGES[k][2], 'w').write(lib.dc_document(title, body, h))
    for name, fw in FRAMES.items():
        open(OUT + PAGES[k][2][:-8] + f'-{name}.dc.html', 'w').write(lib.dc_document(f'{title} ({name})', relink(body, name), heights.get(f'{k}@{fw}', 4000), fw))
print('wrote', [PAGES[k][2] for k in bodies])
