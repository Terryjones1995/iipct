"""Check every artboard file against the format rules that fail silently."""
import sys, os, re, json
from html.parser import HTMLParser
OUT='/home/claude/iipct/project/'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class T(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.stack=[]; s.err=[]; s.ids={}; s.hrefs=[]
    def handle_starttag(s,tag,attrs):
        d=dict(attrs)
        if 'id' in d: s.ids[d['id']]=s.ids.get(d['id'],0)+1
        if tag=='a' and 'href' in d: s.hrefs.append(d['href'])
        if tag=='a' and any(t=='a' for t in s.stack): s.err.append('nested <a>')
        if tag in ('iframe','object','embed'): s.err.append('forbidden '+tag)
        if tag=='img':
            if not d.get('src','').startswith('/_blob/'): s.err.append('img src '+d.get('src','')[:40])
            if 'alt' not in d: s.err.append('img without alt')
        if tag not in VOID: s.stack.append(tag)
    def handle_endtag(s,tag):
        if tag in VOID: return
        if not s.stack or s.stack[-1]!=tag: s.err.append(f'close </{tag}> but open {s.stack[-3:]}')
        else: s.stack.pop()
emoji=re.compile('[\U0001F300-\U0001FAFF☀-➿]')
idx=json.load(open(OUT+'canvas.json')) if os.path.exists(OUT+'canvas.json') else {'boards':{}}
files=sorted(f for f in os.listdir(OUT) if f.endswith('.dc.html'))
bad=0
for f in files:
    s=open(OUT+f).read(); e=[]
    if '<script src="./support.js"></script>' not in s: e.append('support.js line')
    body=s[s.index('<x-dc>'):s.index('</x-dc>')]
    if '{{' in body: e.append('{{ in body')
    if 'data:' in body.replace('data-',''): e.append('data: uri?')
    if emoji.search(body): e.append('emoji '+repr(emoji.search(body).group()))
    t=T(); t.feed(body+'</x-dc>')
    if t.stack: e.append(f'unclosed {t.stack[-4:]}')
    e+=t.err[:4]
    dup=[i for i,n in t.ids.items() if n>1]
    if dup: e.append(f'dup ids {dup}')
    for h in t.hrefs:
        if h.endswith('.dc.html') and not os.path.exists(OUT+h): e.append('missing target '+h)
        if h.startswith('#') and len(h)>1 and h[1:] not in t.ids: e.append('missing anchor '+h)
    m=re.search(r'"\$preview":\{"width":(\d+),"height":(\d+)\}', s)
    b=idx['boards'].get(f)
    if b and m and (int(m.group(1))!=b['w'] or int(m.group(2))!=b['h']): e.append(f'preview {m.groups()} != index {b["w"]}x{b["h"]}')
    if e: bad+=1; print('FAIL', f, e)
print(len(files), 'files,', bad, 'with problems;', 'boards in index:', len(idx['boards']))
missing=[f for f in files if f not in idx['boards']]; extra=[b for b in idx['boards'] if b not in files]
print('not in index:', missing, '| index without file:', extra)
