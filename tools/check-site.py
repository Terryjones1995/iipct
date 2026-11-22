#!/usr/bin/env python3
"""Check the static site folder for broken things. No dependencies.

usage: python3 -I tools/check-site.py [site-dir] [--strict] [--online]

Always fails on: a link to a page or file that does not exist, a link to an anchor that is not on the target page,
an image or stylesheet that does not exist, duplicate ids on a page, an image with no alt attribute, two pages with
the same <title>, a page with no description.
--strict also fails on: placeholder links (href="#"), buttons that cannot do anything (the site has no JavaScript,
so a <button> outside a form that submits is dead), and bracketed placeholder text like "[Staff name]".
--online also requests every outside link once and reports the ones that do not answer 2xx/3xx (never fails the run:
other sites block scripted requests).
"""
import os, re, sys, collections
from html.parser import HTMLParser

args = [a for a in sys.argv[1:] if not a.startswith('--')]
SITE = os.path.abspath(args[0] if args else '.') + '/'
STRICT = '--strict' in sys.argv
ONLINE = '--online' in sys.argv


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = collections.Counter(); self.hrefs = []; self.srcs = []; self.noalt = 0
        self.title = ''; self.desc = None; self._in_title = False
        self.buttons = 0; self.dead_buttons = 0; self._form = 0; self._details = 0; self.text = []
        self.h1 = 0; self.lang = None; self._skip = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'html': self.lang = d.get('lang')
        if 'id' in d: self.ids[d['id']] += 1
        if tag == 'a' and 'href' in d: self.hrefs.append(d['href'])
        if tag == 'link' and d.get('href') and d.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon', 'manifest'): self.srcs.append(d['href'])
        if tag in ('img', 'script', 'source') and d.get('src'): self.srcs.append(d['src'])
        if tag == 'img' and 'alt' not in d: self.noalt += 1
        if tag == 'title': self._in_title = True
        if tag == 'meta' and d.get('name') == 'description': self.desc = d.get('content', '')
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
        if tag in ('script', 'style'): self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._in_title: self.title += data
        elif not self._skip: self.text.append(data)


pages = sorted(f for f in os.listdir(SITE) if f.endswith('.html'))
parsed = {}
for f in pages:
    p = Page(); p.feed(open(SITE + f, encoding='utf-8').read()); parsed[f] = p

errors, strict_errors, external = [], [], collections.defaultdict(list)
titles = collections.defaultdict(list)
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
        if not os.path.isfile(SITE + s.split('?')[0].split('#')[0]): errors.append(f'{f}: missing file {s}')
    hashes = 0
    for h in p.hrefs:
        if h == '#': hashes += 1; continue
        if h.startswith('#'):
            if h[1:] not in p.ids: errors.append(f'{f}: link to missing anchor {h}')
            continue
        if re.match(r'^(mailto:|tel:)', h): continue
        if re.match(r'^https?://', h): external[h].append(f); continue
        path, _, anchor = h.partition('#')
        path = path.split('?')[0]
        if not os.path.isfile(SITE + path):
            errors.append(f'{f}: link to missing page or file {h}'); continue
        if anchor and path in parsed and anchor not in parsed[path].ids:
            errors.append(f'{f}: link to missing anchor {h}')
    if hashes: strict_errors.append(f'{f}: {hashes} placeholder link(s) href="#"')
    if p.dead_buttons: strict_errors.append(f'{f}: {p.dead_buttons} button(s) that cannot do anything without JavaScript')
    brackets = re.findall(r'\[[A-Z][^\[\]]{2,90}\]', ' '.join(p.text))
    if brackets: strict_errors.append(f'{f}: {len(brackets)} bracketed placeholder(s), e.g. {brackets[0][:60]}')
for t, fs in titles.items():
    if t and len(fs) > 1: errors.append(f'same <title> "{t}" on {", ".join(fs)}')

print(f'{len(pages)} pages; {sum(len(p.hrefs) for p in parsed.values())} links; {len(external)} distinct outside links')
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
