#!/usr/bin/env python3
"""Check the static site folder for broken things. No dependencies.

usage: python3 -I tools/check-site.py [site-dir] [--strict] [--online] [--preview]

Always fails on: a link to a page or file that does not exist, a link to an anchor that is not on the target page,
an image or stylesheet that does not exist, duplicate ids on a page, an image with no alt attribute, two pages with
the same <title>, a page with no description.
Search engines and sharing (always on): every page has exactly one canonical address (the not-found page has none),
a title of 15-60 characters and a description of 70-160, both unique across pages; og:url matches the canonical;
og:image (and twitter:image) is a 1200 x 630 JPEG that exists and is under 300 KB; every JSON-LD block parses and has
@context and @type; every <img> has width and height; sitemap.xml lists exactly the public pages; robots.txt points
at the sitemap; no page carries a robots noindex (only the redirect pages at the old addresses may, and must); each
redirect page sends visitors to a page that exists.
--preview checks a test copy written by tools/publish-preview.sh instead: every page carries the noindex line, the
canonical / og:url / og:image / twitter:image tags use the test address and it appears nowhere else, robots.txt
disallows everything, and links that start at the site root (/iipct/...) are followed.
--strict also fails on: placeholder links (href="#"), buttons that cannot do anything (the site has no JavaScript,
so a <button> outside a form that submits is dead), and bracketed placeholder text like "[Staff name]"
(allowed on the two draft legal pages listed in DRAFTS, whose wording IIPCT must supply).
--online also requests every outside link once and reports the ones that do not answer 2xx/3xx (never fails the run:
other sites block scripted requests).
"""
import os, re, sys, json, collections
from html.parser import HTMLParser

args = [a for a in sys.argv[1:] if not a.startswith('--')]
SITE = os.path.abspath(args[0] if args else '.') + '/'
STRICT = '--strict' in sys.argv
ONLINE = '--online' in sys.argv
PREVIEW = '--preview' in sys.argv
# Pages whose wording IIPCT must still supply: their [bracketed] items are expected until launch.
DRAFTS = ('privacy-policy.html', 'accessibility.html')
REAL = 'https://iipct.org/'                                  # tools/generator/seo.py SITE_URL
TEST = 'https://terryjones1995.github.io/iipct/'             # tools/publish-preview.sh PREVIEW_URL
TEST_ROOT = '/iipct/'
BASE = TEST if PREVIEW else REAL
NOT_PUBLIC = ('404.html',)                                   # tools/generator/seo.py NOT_PUBLIC
OG_SIZE, OG_MAX = (1200, 630), 300_000
SKIP_DIRS = {'.git', 'assets', 'tools', 'node_modules', '.claude', '.worktrees'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = collections.Counter(); self.hrefs = []; self.srcs = []; self.noalt = 0
        self.title = ''; self.desc = None; self._in_title = False
        self.buttons = 0; self.dead_buttons = 0; self._form = 0; self._details = 0; self.text = []
        self.h1 = 0; self.lang = None; self._skip = 0
        self.canon = []; self.robots = []; self.meta = {}; self.ld = []; self._ld = None; self.refresh = None; self.nodim = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'html': self.lang = d.get('lang')
        if 'id' in d: self.ids[d['id']] += 1
        if tag == 'a' and 'href' in d: self.hrefs.append(d['href'])
        if tag == 'link' and d.get('href') and d.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon', 'manifest', 'preload'): self.srcs.append(d['href'])
        if tag == 'link' and d.get('rel') == 'canonical': self.canon.append(d.get('href', ''))
        if tag in ('img', 'script', 'source') and d.get('src'): self.srcs.append(d['src'])
        if tag == 'img' and 'alt' not in d: self.noalt += 1
        if tag == 'img' and not (d.get('width') and d.get('height')): self.nodim += 1
        if tag == 'title': self._in_title = True
        if tag == 'meta':
            if d.get('name') == 'description': self.desc = d.get('content', '')
            if d.get('name') == 'robots': self.robots.append(d.get('content', ''))
            if (d.get('http-equiv') or '').lower() == 'refresh': self.refresh = d.get('content', '')
            key = d.get('property') or d.get('name') or ''
            if key.startswith(('og:', 'twitter:', 'article:')): self.meta.setdefault(key, d.get('content', ''))
        if tag == 'script' and d.get('type') == 'application/ld+json': self._ld = []
        if tag == 'form': self._form += 1
        if tag == 'details': self._details += 1
        if tag == 'h1': self.h1 += 1
        if tag in ('script', 'style'): self._skip += 1
        if tag == 'button':
            self.buttons += 1
            # without JavaScript a button only does something as a form's submit/reset
            if not (self._form and d.get('type', 'submit') in ('submit', 'reset')): self.dead_buttons += 1

    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False
        if tag == 'form': self._form = max(0, self._form - 1)
        if tag == 'details': self._details = max(0, self._details - 1)
        if tag == 'script' and self._ld is not None: self.ld.append(''.join(self._ld)); self._ld = None
        if tag in ('script', 'style'): self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._ld is not None: self._ld.append(data)
        if self._in_title: self.title += data
        elif not self._skip: self.text.append(data)


def local(path):
    """A link or file path as a path inside SITE (in a test copy, /iipct/... starts at the site root)."""
    if PREVIEW and path.startswith(TEST_ROOT): path = path[len(TEST_ROOT):]
    return path.split('?')[0].split('#')[0]


def jpeg_size(path):
    """(width, height) from a JPEG's frame header, or None if the file is not a JPEG."""
    data = open(path, 'rb').read()
    if data[:2] != b'\xff\xd8': return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF: return None
        m = data[i + 1]
        if m == 0xFF: i += 1; continue
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7: i += 2; continue
        n = int.from_bytes(data[i + 2:i + 4], 'big')
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            return int.from_bytes(data[i + 7:i + 9], 'big'), int.from_bytes(data[i + 5:i + 7], 'big')
        i += 2 + n
    return None


def page_url(base, f):
    return base if f == 'index.html' else base + f


pages = sorted(f for f in os.listdir(SITE) if f.endswith('.html'))
parsed, raw = {}, {}
for f in pages:
    raw[f] = open(SITE + f, encoding='utf-8').read()
    p = Page(); p.feed(raw[f]); parsed[f] = p

errors, strict_errors, external = [], [], collections.defaultdict(list)
titles, descs = collections.defaultdict(list), collections.defaultdict(list)
for f, p in parsed.items():
    titles[p.title.strip()].append(f)
    if not p.title.strip(): errors.append(f'{f}: no <title>')
    if not p.desc: errors.append(f'{f}: no meta description')
    if p.lang is None: errors.append(f'{f}: <html> has no lang')
    if p.h1 != 1: errors.append(f'{f}: {p.h1} <h1> elements (want exactly 1)')
    for i, n in p.ids.items():
        if n > 1: errors.append(f'{f}: id "{i}" used {n} times')
    if p.noalt: errors.append(f'{f}: {p.noalt} image(s) without an alt attribute')
    for s in p.srcs:
        if re.match(r'^(https?:)?//|^data:', s): continue
        if not os.path.isfile(SITE + local(s)): errors.append(f'{f}: missing file {s}')
    hashes = 0
    for h in p.hrefs:
        if h == '#': hashes += 1; continue
        if h.startswith('#'):
            if h[1:] not in p.ids: errors.append(f'{f}: link to missing anchor {h}')
            continue
        if re.match(r'^(mailto:|tel:)', h): continue
        if re.match(r'^https?://', h): external[h].append(f); continue
        path, _, anchor = h.partition('#')
        path = local(path)
        if not os.path.isfile(SITE + path):
            errors.append(f'{f}: link to missing page or file {h}'); continue
        if anchor and path in parsed and anchor not in parsed[path].ids:
            errors.append(f'{f}: link to missing anchor {h}')
    if hashes: strict_errors.append(f'{f}: {hashes} placeholder link(s) href="#"')
    if p.dead_buttons: strict_errors.append(f'{f}: {p.dead_buttons} button(s) that cannot do anything without JavaScript')
    brackets = re.findall(r'\[[A-Za-z][^\[\]]{2,400}\]', ' '.join(p.text))
    if brackets and f not in DRAFTS: strict_errors.append(f'{f}: {len(brackets)} bracketed placeholder(s), e.g. {brackets[0][:60]}')

    # ---- search engines and sharing
    t = p.title.strip()
    if t and not 15 <= len(t) <= 60: errors.append(f'{f}: title is {len(t)} characters (want 15-60): {t}')
    if p.desc:
        descs[p.desc].append(f)
        if not 70 <= len(p.desc) <= 160: errors.append(f'{f}: description is {len(p.desc)} characters (want 70-160)')
    want = page_url(BASE, f)
    if f in NOT_PUBLIC:
        if p.canon: errors.append(f'{f}: the not-found page should have no canonical link')
    elif len(p.canon) != 1:
        errors.append(f'{f}: {len(p.canon)} canonical links (want exactly 1)')
    elif p.canon[0] != want:
        errors.append(f'{f}: canonical is {p.canon[0]} (want {want})')
    if f not in NOT_PUBLIC and p.meta.get('og:url') != want:
        errors.append(f'{f}: og:url is {p.meta.get("og:url")} (want {want})')
    for k in ('og:title', 'og:description', 'og:type', 'og:image:alt', 'twitter:title', 'twitter:description'):
        if not p.meta.get(k): errors.append(f'{f}: no {k}')
    if p.meta.get('twitter:card') != 'summary_large_image': errors.append(f'{f}: twitter:card is not summary_large_image')
    og = p.meta.get('og:image', '')
    if not og.startswith(BASE):
        errors.append(f'{f}: og:image "{og}" is not on {BASE}')
    else:
        img = SITE + og[len(BASE):]
        if not os.path.isfile(img): errors.append(f'{f}: og:image file missing: {og[len(BASE):]}')
        else:
            size = jpeg_size(img)
            if size != OG_SIZE: errors.append(f'{f}: og:image is {size} (want a {OG_SIZE[0]} x {OG_SIZE[1]} JPEG)')
            if os.path.getsize(img) > OG_MAX: errors.append(f'{f}: og:image is {os.path.getsize(img) // 1024} KB (want under 300 KB)')
    if p.meta.get('twitter:image') != og: errors.append(f'{f}: twitter:image differs from og:image')
    if (p.meta.get('og:image:width'), p.meta.get('og:image:height')) != ('1200', '630'): errors.append(f'{f}: og:image:width/height are not 1200/630')
    for i, block in enumerate(p.ld, 1):
        try:
            data = json.loads(block)
        except ValueError as ex:
            errors.append(f'{f}: JSON-LD block {i} does not parse: {ex}'); continue
        for item in (data if isinstance(data, list) else [data]):
            if not (isinstance(item, dict) and item.get('@context') and item.get('@type')):
                errors.append(f'{f}: JSON-LD block {i} has no @context or @type')
    if not p.ld: errors.append(f'{f}: no JSON-LD structured data')
    if p.nodim: errors.append(f'{f}: {p.nodim} image(s) without width and height')
    noindex = [r for r in p.robots if 'noindex' in r.lower()]
    body = raw[f][raw[f].find('<body'):]
    if PREVIEW:
        if p.robots != ['noindex, nofollow']: errors.append(f'{f}: test copy page without exactly one "noindex, nofollow" robots tag')
        tags = len(p.canon) + sum(1 for k in ('og:url', 'og:image', 'twitter:image') if p.meta.get(k, '').startswith(TEST))
        if raw[f].count(TEST) != tags: errors.append(f'{f}: the test address appears outside the canonical/og:url/og:image/twitter:image tags')
        if TEST in body: errors.append(f'{f}: the test address appears in the page body')
    else:
        if noindex: errors.append(f'{f}: robots noindex in the repo (only the test copy and redirect pages may carry it)')
        if TEST in raw[f]: errors.append(f'{f}: the test address appears in a repo page')
for t, fs in titles.items():
    if t and len(fs) > 1: errors.append(f'same <title> "{t}" on {", ".join(fs)}')
for d, fs in descs.items():
    if len(fs) > 1: errors.append(f'same description on {", ".join(fs)}')

# ---- sitemap.xml: exactly the public pages, on the real address (the test copy keeps the real sitemap)
public = {page_url(REAL, f) for f in pages if f not in NOT_PUBLIC}
if not os.path.isfile(SITE + 'sitemap.xml'):
    errors.append('no sitemap.xml')
else:
    sm = open(SITE + 'sitemap.xml', encoding='utf-8').read()
    locs = re.findall(r'<url>\s*<loc>([^<]+)</loc>', sm)
    for u in sorted(public - set(locs)): errors.append(f'sitemap.xml does not list {u}')
    for u in sorted(set(locs) - public): errors.append(f'sitemap.xml lists {u}, which is not a public page')
    if len(locs) != len(set(locs)): errors.append('sitemap.xml lists a page twice')
    for i in re.findall(r'<image:loc>([^<]+)</image:loc>', sm):
        if not (i.startswith(REAL) and os.path.isfile(SITE + i[len(REAL):])): errors.append(f'sitemap.xml lists a missing image {i}')

# ---- robots.txt
rb = open(SITE + 'robots.txt', encoding='utf-8').read() if os.path.isfile(SITE + 'robots.txt') else None
if rb is None: errors.append('no robots.txt')
elif PREVIEW:
    if not re.search(r'(?m)^Disallow:\s*/\s*$', rb): errors.append('test copy robots.txt does not say "Disallow: /"')
else:
    if not re.search(rf'(?m)^Sitemap:\s*{re.escape(REAL)}sitemap\.xml\s*$', rb): errors.append('robots.txt does not point at the sitemap')
    if re.search(r'(?m)^Disallow:\s*/\s*$', rb): errors.append('robots.txt blocks the whole site')

# ---- redirect pages at the old site's addresses (folder/index.html)
found = []
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
    if os.path.abspath(root) != os.path.abspath(SITE) and 'index.html' in files:
        found.append(os.path.relpath(os.path.join(root, 'index.html'), SITE))
for r in sorted(found):
    p = Page(); p.feed(open(SITE + r, encoding='utf-8').read())
    m = re.match(r'^\s*0\s*;\s*url=(\S+)$', p.refresh or '')
    if not m: errors.append(f'{r}: redirect page without an instant refresh'); continue
    target = os.path.normpath(os.path.join(os.path.dirname(r), m.group(1)))
    if target not in parsed: errors.append(f'{r}: redirects to {m.group(1)}, which is not a page'); continue
    if not any('noindex' in x for x in p.robots): errors.append(f'{r}: redirect page without noindex')
    if p.canon != [page_url(BASE, target)]: errors.append(f'{r}: canonical {p.canon} (want {page_url(BASE, target)})')
    if m.group(1) not in p.hrefs: errors.append(f'{r}: no plain link to {m.group(1)}')
manifest = SITE + 'tools/redirects/redirect-pages.txt'
if not PREVIEW and os.path.isfile(manifest):
    listed = [l.strip() for l in open(manifest, encoding='utf-8') if l.strip() and not l.startswith('#')]
    for r in sorted(set(listed) - set(found)): errors.append(f'redirect page listed in tools/redirects/redirect-pages.txt is missing: {r}')
    for r in sorted(set(found) - set(listed)): errors.append(f'{r}: not listed in tools/redirects/redirect-pages.txt (it would not be published)')

print(f'{len(pages)} pages; {len(found)} redirect pages; {sum(len(p.hrefs) for p in parsed.values())} links; {len(external)} distinct outside links'
      + ('  [test copy]' if PREVIEW else ''))
for e in errors: print('ERROR  ', e)
for e in strict_errors: print('STRICT ' if STRICT else 'note   ', e)

if ONLINE:
    import urllib.request
    for url in sorted(external):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (link check)'}, method='GET')
            with urllib.request.urlopen(req, timeout=20) as r: code = r.status
        except Exception as ex:
            code = getattr(ex, 'code', None) or type(ex).__name__
        if not (isinstance(code, int) and 200 <= code < 400):
            print(f'outside link answered {code}: {url}  (on {", ".join(sorted(set(external[url]))[:3])})')

bad = len(errors) + (len(strict_errors) if STRICT else 0)
print('RESULT:', 'OK' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
