"""Export the pages as a plain static website (HTML + one stylesheet + images) into a repo folder.
usage: export_site.py <out_dir>"""
import sys, os, re, json, importlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib
from PIL import Image

OUT = os.path.abspath(sys.argv[1]) + '/'
src = open(os.path.join(HERE, 'build.py')).read()
ns = {}
exec(src[src.index('PAGES = {'):src.index("FRAMES = {")], ns)
PAGES = ns['PAGES']

NAMES = {'Main.dc.html': 'index.html', 'WhoWeAre.dc.html': 'who-we-are.html', 'Services.dc.html': 'services.html', 'Events.dc.html': 'events-programs.html',
         'Contact.dc.html': 'contact.html', 'Careers.dc.html': 'careers.html', 'Board.dc.html': 'board-of-directors.html', 'BPSO.dc.html': 'bpso.html',
         'PrimaryCare.dc.html': 'primary-medical-care.html', 'Immunization.dc.html': 'immunization.html', 'WellBaby.dc.html': 'well-baby-well-child.html',
         'TBTesting.dc.html': 'tb-testing.html', 'FootCare.dc.html': 'advanced-foot-care.html', 'Retinopathy.dc.html': 'diabetic-retinopathy-screening.html',
         'Outreach.dc.html': 'outreach-community-support.html', 'Booking.dc.html': 'schedule-your-visit.html', 'News.dc.html': 'news.html',
         'NewsIPHCCAwards.dc.html': 'news-iphcc-awards.html', 'NewsBreastScreening.dc.html': 'news-breast-cancer-screening.html',
         'Privacy.dc.html': 'privacy-policy.html', 'Accessibility.dc.html': 'accessibility.html', 'SiteMap.dc.html': 'site-map.html'}
DESC = {
 'home': 'Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (IIPCT): Indigenous-centred primary care for individuals, families and communities across southeastern Ontario.',
 'who': 'Who IIPCT is: an Indigenous-led, community-grounded primary care team serving Indigenous people and families across southeastern Ontario.',
 'services': 'IIPCT services: cultural services, primary medical care, mental health services and health support services.',
 'events': 'Events and programs from IIPCT: wellness, learning and community connection rooted in culture and care.',
 'contact': 'Contact IIPCT: phone, email and clinic locations in Tyendinaga, Deseronto, Kingston, Bancroft and Shannonville.',
 'careers': 'Career opportunities at IIPCT.',
 'board': 'The IIPCT Board of Directors.',
 'bpso': 'IIPCT is a Best Practice Spotlight Organization (BPSO).',
 'primary': 'Primary medical care at IIPCT: chronic disease care, same-day acute care, referrals, blood draws, screening and more.',
 'immun': 'The publicly funded immunization program at IIPCT, for infants, children and adults.',
 'wellbaby': 'Well baby and well child appointments at IIPCT, from two months to six years.',
 'tb': 'Tuberculosis (TB) skin testing at IIPCT.',
 'foot': 'Advanced foot care at IIPCT, from nurses with specialized certification.',
 'retino': 'Monthly diabetic retinopathy screening clinics at IIPCT.',
 'outreach': 'Outreach and community support from IIPCT: screening and care out in the community.',
 'booking': 'Schedule your visit with IIPCT: online booking for registered patients, or call your clinic.',
 'news': 'News and updates from Tsi Kanonhkhwatsheríyo IIPCT.',
 'post1': 'IIPCT staff received five of the 18 awards at the 2025 IPHCC Member Awards.',
 'post2': 'Nineteen mammograms completed at IIPCT’s breast cancer screening event.',
 'privacy': 'IIPCT privacy policy.',
 'access': 'Accessibility at IIPCT.',
 'sitemap': 'Every page on the IIPCT website.',
}

# ---------------------------------------------------------------- images: only the ones the pages use
os.makedirs(OUT + 'assets/img', exist_ok=True); os.makedirs(OUT + 'assets/css', exist_ok=True)
A = lib.A
IMG = {}          # blob url -> site path
def image_for(name):
    url = lib.BLOB[name]
    if url in IMG: return IMG[url]
    im = Image.open(A + lib.META[name]['file'])
    if name in ('logo-emblem', 'feather-gold'):
        if name == 'logo-emblem' and im.width > 400: im = im.resize((400, round(400 * im.height / im.width)), Image.LANCZOS)
        fn = name + '.png'; im.save(OUT + 'assets/img/' + fn, optimize=True)
    else:
        fn = name + '.jpg'; im.convert('RGB').save(OUT + 'assets/img/' + fn, quality=88, optimize=True, progressive=True)
    IMG[url] = 'assets/img/' + fn
    return IMG[url]
BLOB_NAME = {v: k for k, v in lib.BLOB.items() if k != 'logo-emblem-mock'}

def to_site(body):
    html = lib.root(body)
    html = re.sub(r'src="(/_blob/[0-9a-f]+)"', lambda m: f'src="{image_for(BLOB_NAME[m.group(1)])}"', html)
    for f, n in NAMES.items():
        html = html.replace(f'href="{f}"', f'href="{n}"')
    assert '.dc.html' not in html and '/_blob/' not in html
    html = re.sub(r'<a ([^>]*?)href="(https?://[^"]+)"', r'<a \1href="\2" target="_blank" rel="noopener"', html)   # other sites open in a new tab
    assert html.count('</header>') == 1 and html.count('<footer ') == 1
    html = html.replace('</header>', '</header>\n<main id="main">', 1).replace('\n<footer ', '\n</main>\n<footer ', 1)
    assert '</main>' in html
    return html

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{note}{html}
</body>
</html>
'''
BOOKING_NOTE = ('<!-- This form is a front-end mock of IIPCT\'s Ocean booking form. It does not submit anywhere.\n'
                '     Do not collect health numbers on this site: send patients to the Ocean portal instead (see README). -->\n')
count = 0
for k, (mod, func, fn, mock, label) in PAGES.items():
    title, body = getattr(importlib.import_module(mod), func)()
    page = HEAD.format(title=title.replace('IIPCT — ', '') + ' | IIPCT', desc=DESC[k], fonts=lib.FONT_HREF, html=to_site(body), note=BOOKING_NOTE if k == 'booking' else '')
    open(OUT + NAMES[fn], 'w').write(page); count += 1

# favicon
logo = Image.open(A + lib.META['logo-emblem']['file']); logo.resize((96, round(96 * logo.height / logo.width)), Image.LANCZOS).save(OUT + 'assets/img/favicon.png', optimize=True)

# ---------------------------------------------------------------- stylesheet: same rules, as ordinary media queries, laid out to be read
css = lib.BASE_CSS.replace('@container pg (', '@media (').replace('.pg{container-type:inline-size;container-name:pg;min-width:320px}', '.pg{min-width:320px}')
assert '@container' not in css and 'container-type' not in css
def pretty(css):
    out, depth, buf = [], 0, ''
    for ch in css.replace('\n', ''):
        if ch == '{':
            sel = buf.strip(); buf = ''
            if sel.startswith('@'): out.append('\n' + sel + ' {'); depth += 1; at = True
            else: out.append('  ' * depth + ', '.join(s.strip() for s in sel.split(',')) + ' {'); depth += 1; at = False
            stack.append(at)
        elif ch == '}':
            decl = buf.strip(); buf = ''
            if decl: out.extend('  ' * depth + d.strip().replace(':', ': ', 1) + ';' for d in decl.split(';') if d.strip())
            depth -= 1; out.append('  ' * depth + '}'); stack.pop()
        elif ch == ';':
            d = buf.strip(); buf = ''
            if d: out.append('  ' * depth + d.replace(':', ': ', 1) + ';')
        else:
            buf += ch
    return '\n'.join(out) + '\n'
stack = []
head = ('/* IIPCT website — shared stylesheet.\n'
        '   Layout and colour live inline on the elements (the pages were exported from the design canvas).\n'
        '   This file holds the base rules, hover states, dropdown menus and the narrow-screen rules.\n'
        '   Breakpoints: 1399 small laptops, 1199 menu button, 1099 tablets, 900, 760 phones, 480 small phones. */\n\n')
extra = ('\n/* Skip link */\n.skip {\n  position: absolute;\n  left: 12px;\n  top: -60px;\n  z-index: 100;\n  padding: 10px 16px;\n  border-radius: 8px;\n  background: #17402A;\n'
         '  color: #fff;\n  font: 600 14px/1 "DM Sans", system-ui, sans-serif;\n  text-decoration: none;\n}\n.skip:focus {\n  top: 12px;\n  color: #fff;\n}\n')
open(OUT + 'assets/css/site.css', 'w').write(head + pretty(css) + extra)
open(OUT + '.nojekyll', 'w').write('')
hashes = sum(len(re.findall(r'href="#"', open(OUT + n).read())) for n in NAMES.values())
print(count, 'pages,', len(IMG), 'images,', 'placeholder links (href="#"):', hashes)
