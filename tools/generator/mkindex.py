"""Update project/canvas.json from the live copy: keep every existing frame's x,y; refresh heights; add new frames in free rows.
usage: mkindex.py <live-index.json>"""
import sys, json, importlib
sys.path.insert(0, '/home/claude/iipct_work/gen')
OUT = '/home/claude/iipct/project/'
heights = json.load(open('/home/claude/iipct_work/preview/heights.json'))
src = open('/home/claude/iipct_work/gen/build.py').read()
ns = {}
exec(src[src.index('PAGES = {'):src.index("os.makedirs(OUT")], ns)
PAGES = ns['PAGES']
idx = json.load(open(sys.argv[1]))
boards, order, notes = idx['boards'], idx['order'], idx.setdefault('notes', {})
key_of = {v[2]: k for k, v in PAGES.items()}
for fn, b in boards.items():                      # frames that exist: only the height changes
    if fn in key_of: b['h'] = heights[key_of[fn]]
def bottom(page=None):
    return max(b['y'] + b['h'] for b in boards.values() if b.get('page') == page)
ROWS = [('row_primary', 'Primary medical care — pages from the live site', ['primary', 'immun', 'wellbaby', 'tb', 'foot', 'retino', 'outreach']),
        ('row_more', 'Booking, news and legal', ['booking', 'news', 'post1', 'post2', 'privacy', 'access', 'sitemap'])]
for nid, text, keys in ROWS:
    new = [k for k in keys if PAGES[k][2] not in boards]
    if not new: continue
    y = bottom() + 420                              # 120 row gap + room for the row title 300 above the frames
    xs = 0
    for k in keys:
        fn = PAGES[k][2]
        if fn in boards: xs = max(xs, boards[fn]['x'] + 1520); continue
        boards[fn] = {'x': xs, 'y': y, 'w': 1440, 'h': heights[k], 'title': PAGES[k][4], 'expand': 'fill', 'is_interactive': True}
        order.append(fn); xs += 1520
    notes[nid] = {'x': 0, 'y': y - 300, 'text': text, 'kind': 'title1', 'maxW': 7 * 1520 - 80}
# ---- tablet and phone versions live on their own canvas pages
FRAMES = [('tablet', 'Tablet', 820, 11, 'Tablet and iPad — 820 px wide'), ('phone', 'Phone', 390, 22, 'Phone — 390 px wide')]
ALL = ['home', 'who', 'services', 'events', 'contact', 'careers', 'board', 'bpso', 'primary', 'immun', 'wellbaby', 'tb', 'foot', 'retino', 'outreach',
       'booking', 'news', 'post1', 'post2', 'privacy', 'access', 'sitemap']
pages = idx.setdefault('pages', [])
if not pages: pages.append({'id': 'desktop', 'name': 'Desktop'})
for pid, pname, fw, per_row, text in FRAMES:
    if not any(p['id'] == pid for p in pages): pages.append({'id': pid, 'name': pname})
    step = fw + 80
    y = 0; row_max = 0
    for i, k in enumerate(ALL):
        fn = PAGES[k][2][:-8] + f'-{pid}.dc.html'
        h = heights[f'{k}@{fw}']
        if i and i % per_row == 0: y += row_max + 160; row_max = 0
        if fn in boards:
            boards[fn]['h'] = h                      # exists already: keep where it is, refresh the height
        else:
            boards[fn] = {'x': (i % per_row) * step, 'y': y, 'w': fw, 'h': h, 'title': PAGES[k][4], 'page': pid, 'expand': 'fill', 'is_interactive': True}
            order.append(fn)
        row_max = max(row_max, h)
    notes.setdefault(f'title_{pid}', {'x': 0, 'y': -300, 'text': text, 'kind': 'title1', 'maxW': per_row * step - 80, 'page': pid})
# overlap check
bs = list(boards.items())
for i, (a, A) in enumerate(bs):
    for b, B in bs[i + 1:]:
        if A.get('page') == B.get('page') and A['x'] < B['x'] + B['w'] and B['x'] < A['x'] + A['w'] and A['y'] < B['y'] + B['h'] and B['y'] < A['y'] + A['h']:
            raise SystemExit(f'overlap {a} {b}')
json.dump(idx, open(OUT + 'canvas.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for fn in order: print(f"{fn:32s} x={boards[fn]['x']:5d} y={boards[fn]['y']:5d} h={boards[fn]['h']}")
print({k: (v['x'], v['y']) for k, v in notes.items()})
