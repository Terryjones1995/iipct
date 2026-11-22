"""Export the pages as a plain static website (HTML + one stylesheet + images) into a repo folder.
usage: export_site.py <out_dir>"""
import sys, os, re, json, importlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib, seo
from PIL import Image

OUT = os.path.abspath(sys.argv[1]) + '/'
src = open(os.path.join(HERE, 'build.py')).read()
ns = {}
exec(src[src.index('PAGES = {'):src.index("FRAMES = {")], ns)
PAGES = ns['PAGES']

NAMES = {'Main.dc.html': 'index.html', 'WhoWeAre.dc.html': 'who-we-are.html', 'Team.dc.html': 'our-team.html', 'Services.dc.html': 'services.html', 'Events.dc.html': 'events-programs.html',
         'Contact.dc.html': 'contact.html', 'Careers.dc.html': 'careers.html', 'Board.dc.html': 'board-of-directors.html', 'BPSO.dc.html': 'bpso.html',
         'PrimaryCare.dc.html': 'primary-medical-care.html', 'Immunization.dc.html': 'immunization.html', 'WellBaby.dc.html': 'well-baby-well-child.html',
         'TBTesting.dc.html': 'tb-testing.html', 'FootCare.dc.html': 'advanced-foot-care.html', 'Retinopathy.dc.html': 'diabetic-retinopathy-screening.html',
         'Outreach.dc.html': 'outreach-community-support.html', 'Booking.dc.html': 'schedule-your-visit.html', 'News.dc.html': 'news.html',
         'NewsIPHCCAwards.dc.html': 'news-iphcc-awards.html', 'NewsBreastScreening.dc.html': 'news-breast-cancer-screening.html',
         'Privacy.dc.html': 'privacy-policy.html', 'Accessibility.dc.html': 'accessibility.html', 'SiteMap.dc.html': 'site-map.html',
         'NotFound.dc.html': '404.html'}
# Titles, descriptions and share images: seo.PAGES (tools/generator/seo.py), keyed by the file names above.
assert set(NAMES.values()) == set(seo.PAGES), f'pages without a row in seo.PAGES or rows without a page: {set(NAMES.values()) ^ set(seo.PAGES)}'

# ---------------------------------------------------------------- images: only the ones the pages use
os.makedirs(OUT + 'assets/img', exist_ok=True); os.makedirs(OUT + 'assets/css', exist_ok=True)
A = lib.A
IMG = {}          # blob url -> site path
def save_image(im, path, **kw):
    """Write an image only when its pixels differ from the file already there, so a regenerate that changes nothing
    leaves no changed files behind (PNG and JPEG encoders differ between Pillow versions)."""
    import io
    buf = io.BytesIO(); im.save(buf, format='PNG' if path.endswith('.png') else 'JPEG', **kw)
    new = buf.getvalue()
    if os.path.exists(path):
        old = open(path, 'rb').read()
        if old == new: return
        try:
            a, b = Image.open(io.BytesIO(old)), Image.open(io.BytesIO(new))
            if a.size == b.size and a.convert('RGBA').tobytes() == b.convert('RGBA').tobytes(): return
        except Exception:
            pass
    open(path, 'wb').write(new)
def image_for(name):
    url = lib.BLOB[name]
    if url in IMG: return IMG[url]
    im = Image.open(A + lib.META[name]['file'])
    if name in ('logo-emblem', 'feather-gold'):
        if name == 'logo-emblem' and im.width > 400: im = im.resize((400, round(400 * im.height / im.width)), Image.LANCZOS)
        fn = name + '.png'; save_image(im, OUT + 'assets/img/' + fn, optimize=True)
    else:
        fn = name + '.jpg'; save_image(im.convert('RGB'), OUT + 'assets/img/' + fn, quality=88, optimize=True, progressive=True)
    IMG[url] = 'assets/img/' + fn
    return IMG[url]
BLOB_NAME = {v: k for k, v in lib.BLOB.items() if k != 'logo-emblem-mock'}

# Real photographs (from IIPCT's own site and Facebook page) are ordinary files under tools/generator/site-img/.
# Pages point at them with lib.photo('people/name.jpg', ...); they are copied to assets/img/ as they are.
SITE_IMG = os.path.join(HERE, 'site-img') + '/'
SITE_USED = set()
def site_image(rel):
    src = SITE_IMG + rel
    assert os.path.isfile(src), f'lib.photo() names a file that is not in tools/generator/site-img/: {rel}'
    dst = OUT + 'assets/img/' + rel
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst) or open(dst, 'rb').read() != open(src, 'rb').read():
        shutil.copyfile(src, dst)
    SITE_USED.add(rel)
    return 'assets/img/' + rel

def to_site(body):
    html = lib.root(body)
    html = re.sub(r'src="(/_blob/[0-9a-f]+)"', lambda m: f'src="{image_for(BLOB_NAME[m.group(1)])}"', html)
    html = re.sub(r'(src|href)="/_site/([^"]+)"', lambda m: f'{m.group(1)}="{site_image(m.group(2))}"', html)
    html = re.sub(r'href="([A-Za-z0-9]+\.dc\.html)(#[^"]*)?"', lambda m: f'href="{NAMES[m.group(1)]}{m.group(2) or ""}"', html)
    assert '.dc.html' not in html and '/_blob/' not in html and '/_site/' not in html
    html = re.sub(r'<a ([^>]*?)href="(https?://[^"]+)"', r'<a \1href="\2" target="_blank" rel="noopener"', html)   # other sites open in a new tab
    assert html.count('</header>') == 1 and html.count('<footer ') == 1
    html = html.replace('</header>', '</header>\n<main id="main">', 1).replace('\n<footer ', '\n</main>\n<footer ', 1)
    assert '</main>' in html
    return html

# ---------------------------------------------------------------- speed basics search engines measure
# Every <img> gets its real width and height (so the page does not jump while images load), images below the first
# screen load lazily, and the first screen's hero image loads early (not lazy, preloaded, high priority).
SIZES = {}
def img_size(src):
    if src not in SIZES:
        with Image.open(OUT + src) as im:
            SIZES[src] = im.size
    return SIZES[src]

def _has(style, prop):
    return re.search(r'(?:^|;)\s*' + prop + r'\s*:', style) is not None

def speed(html):
    '''Returns (html, hero image path or None). "First screen" = the header and the first <section> of <main>.'''
    main_at = html.index('<main id="main">')
    end = re.search(r'</section>', html[main_at:])
    fold = main_at + end.end() if end else main_at
    first = [m for m in re.finditer(r'<img [^>]*>', html[main_at:fold])]
    hero = next((m for m in first if 'hero-photo' in m.group(0)), first[0] if first else None)
    hero_at = main_at + hero.start() if hero else -1
    hero_src = None
    def fix(m):
        nonlocal hero_src
        tag, at = m.group(0), m.start()
        src = re.search(r' src="([^"]+)"', tag).group(1)
        if ' width="' not in tag:
            w, h = img_size(src)
            # The width/height attributes act as CSS sizes for any side the inline style leaves out, which would change
            # how the image is drawn: keep that side automatic, as it was.
            sm = re.search(r' style="([^"]*)"', tag)
            style = sm.group(1).strip() if sm else ''
            keep = '; '.join(f'{p}: auto' for p in ('width', 'height') if not _has(style, p))
            if keep:
                style = (style.rstrip(';') + '; ' + keep) if style else keep
                tag = tag.replace(sm.group(0), f' style="{style}"', 1) if sm else tag[:-1] + f' style="{style}">'
            tag = tag.replace('<img ', f'<img width="{w}" height="{h}" ', 1)
        if at < fold:
            tag = tag.replace(' loading="lazy"', '')
            if at == hero_at:
                hero_src = src
                if 'fetchpriority=' not in tag:
                    tag = tag.replace('<img ', '<img fetchpriority="high" ', 1)
        elif 'loading=' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
        return tag
    html = re.sub(r'<img [^>]*>', fix, html)
    return html, hero_src

def mark_current(html, name):
    """The header's menu links to the page being shown get aria-current="page"; in the phone and tablet menu sheet
    (links with class ml) they also get class cur, which lib.RESP_CSS draws as a rust bar, so visitors see where they are."""
    end = html.index('</header>')
    def mark(m):
        tag = m.group(0)
        if 'aria-current=' in tag:
            return tag
        tag = tag.replace(' href=', ' aria-current="page" href=', 1)
        return tag.replace('class="ml ', 'class="ml cur ', 1)
    head = re.sub(r'<a class="(?:nv|ml )[^"]*" href="' + re.escape(name) + r'"[^>]*>', mark, html[:end])
    return head + html[end:]

HEAD = '''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{seo}
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{preload}<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{note}{html}
</body>
</html>
'''
count = 0
BODIES = {}
for k, (mod, func, fn, mock, label) in PAGES.items():
    title, body = getattr(importlib.import_module(mod), func)()
    name = NAMES[fn]
    html, hero = speed(to_site(body))
    html = mark_current(html, name)
    BODIES[name] = html
    preload = f'<link rel="preload" as="image" href="{hero}" fetchpriority="high">\n' if hero else ''
    ld = '\n'.join(seo.ld(b) for b in seo.structured(name, html))
    page = HEAD.format(seo=seo.head_tags(name), preload=preload, fonts=lib.FONT_HREF, ld=ld, html=html, note='')
    open(OUT + name, 'w').write(page); count += 1

# The Contact page's opening hours in the structured data come from facts.LOCATIONS; make sure the page prints the same.
_contact = seo.plain(BODIES['contact.html'])
for _loc in lib.LOCATIONS:
    for _d, _t in lib.hours_rows(_loc):
        assert f'{_d} {_t}' in _contact, f'contact.html does not show "{_d} {_t}" for {_loc["name"]}: the structured data would not match the page'

# favicon
logo = Image.open(A + lib.META['logo-emblem']['file']); save_image(logo.resize((96, round(96 * logo.height / logo.width)), Image.LANCZOS), OUT + 'assets/img/favicon.png', optimize=True)
# home-screen icon for phones (180 px): the emblem on the site's cream, since iOS fills transparent corners with black
touch = Image.new('RGBA', (180, 180), lib.CREAM)
emb = logo.convert('RGBA').resize((150, round(150 * logo.height / logo.width)), Image.LANCZOS)
touch.alpha_composite(emb, ((180 - emb.width) // 2, (180 - emb.height) // 2))
save_image(touch.convert('RGB'), OUT + 'assets/img/apple-touch-icon.png', optimize=True)

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
extra = ('\n/* Skip link */\n.skip {\n  position: absolute;\n  left: 12px;\n  top: -60px;\n  z-index: 100;\n  padding: 13px 16px;\n  border-radius: 8px;\n  background: #17402A;\n'
         '  color: #fff;\n  font: 600 14px/1 "DM Sans", system-ui, sans-serif;\n  text-decoration: none;\n}\n.skip:focus {\n  top: 12px;\n  color: #fff;\n}\n')
open(OUT + 'assets/css/site.css', 'w').write(head + pretty(css) + extra)
open(OUT + '.nojekyll', 'w').write('')
# ---------------------------------------------------------------- search engine files at the site root
import subprocess, datetime
TODAY = datetime.date.today().isoformat()
def last_changed(name):
    """The date the page last changed in git; today when it has changes not yet committed (or there is no git)."""
    try:
        run = lambda *a: subprocess.run(['git', '-C', OUT, *a], capture_output=True, text=True, timeout=30)
        if run('status', '--porcelain', '--', name).stdout.strip():
            return TODAY
        return run('log', '-1', '--format=%cs', '--', name).stdout.strip() or TODAY
    except Exception:
        return TODAY

def photos(html):
    """Real photographs on a page (lib.photo files, under assets/img/<folder>/); header and footer left out."""
    main = html[html.index('<main id="main">'):html.index('</main>')]
    seen = []
    for src in re.findall(r'<img [^>]*src="(assets/img/[^"/]+/[^"]+)"', main):
        if not src.startswith(seo.OG_DIR) and src not in seen:
            seen.append(src)
    return seen

def write_if_changed(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or open(path, encoding='utf-8').read() != text:
        open(path, 'w', encoding='utf-8').write(text)

public = [NAMES[fn] for (_, _, fn, _, _) in PAGES.values() if NAMES[fn] not in seo.NOT_PUBLIC]
write_if_changed(OUT + 'sitemap.xml', seo.sitemap([(n, last_changed(n), photos(BODIES[n])) for n in public]))
write_if_changed(OUT + 'robots.txt', seo.robots())
# The old site's addresses: a redirect page at each, the same list as nginx 301s, and the list publish-preview.sh copies.
redirects = []
for old, new in seo.OLD_URLS:
    assert new in seo.PAGES and re.fullmatch(r'([a-z0-9-]+/)+', old), (old, new)
    write_if_changed(OUT + old + 'index.html', seo.redirect_page(old, new))
    redirects.append(old + 'index.html')
write_if_changed(OUT + 'tools/redirects/nginx-old-urls.conf', seo.nginx_conf())
write_if_changed(OUT + 'tools/redirects/redirect-pages.txt',
                 '# Redirect pages at the old iipct.org addresses. Written by tools/generator/export_site.py;\n'
                 '# tools/publish-preview.sh publishes exactly these files.\n' + '\n'.join(redirects) + '\n')
missing_og = [n for n in seo.PAGES if not os.path.isfile(OUT + seo.og_image(n))]
if missing_og:
    print('NOTE: no share image yet for', ', '.join(missing_og), '- make them with: python3 tools/generator/og_cards.py', OUT)
off_page = [n for n, r in seo.PAGES.items() if r.get('photo') and f'src="assets/img/{r["photo"][0]}"' not in BODIES.get(n, '')]
if off_page:
    print('NOTE: the share-image photo in seo.PAGES is not shown on its page for', ', '.join(off_page),
          '- if the page\'s lead photograph changed, update the row and re-make its share image (og_cards.py)')

hashes = sum(len(re.findall(r'href="#"', open(OUT + n).read())) for n in NAMES.values())
print(count, 'pages,', len(IMG), 'images,', len(SITE_USED), 'photographs,', len(redirects), 'old-address redirects,',
      'placeholder links (href="#"):', hashes)
