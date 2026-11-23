"""Make the share images ("link previews"): one 1200 x 630 JPEG per page, assets/img/og/<page>.jpg.

usage: og_cards.py <site_dir> [page.html ...]        (no page names = every page in seo.PAGES)
       og_cards.py <site_dir> --html <dir>           (only write the card HTML to <dir>, for a look in a browser)

Each card is a small HTML page in the site's look (cream panel, the emblem, "IIPCT", the page's heading in the heading
serif, the thin four-colour bar) with the page's own photograph beside it (seo.PAGES[...]['photo']) or, where the page
has no real photograph, the site's landscape artwork. Headless Chrome screenshots it; Pillow saves it as JPEG.

Needs Google Chrome (`google-chrome`, or set CHROME=/path/to/chrome), Pillow, and an internet connection for the site's
Google Fonts. The ordinary regenerate (export_site.py) never needs a browser: the cards are committed as files. Re-run
this when a row's heading or photo changes, or a page is added. On the IIPCT server, browser runs go through the lock:
    HOF_HEAVY_WAIT=1800 /home/terry/bin/hof-heavy python3 tools/generator/og_cards.py .
"""
import sys, os, io, html, shutil, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib, seo
from PIL import Image

MAX_BYTES = 300_000
CHROME = os.environ.get('CHROME') or shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium')

BAR = ''.join(f'<span style="flex: 1; background: {c}"></span>' for c in ['#FEFDFC', '#F7D80C', '#BA2B2C', '#0A8242'])
SITE_IMG = os.path.join(HERE, 'site-img') + '/'
EMBLEM = lib.A + lib.META['logo-emblem']['file']


def default_art():
    """The right-hand panel for pages without a real photograph: a dawn sky over the site's hills and pines (lib.landscape)."""
    art = lib.landscape(400, 1100, '', tall=True)      # main sun off to the right, out of view: only the tall stand's sun shows
    # show the left end of the landscape (the tall stand of pines and its sun), scaled to fill the panel
    for a, b in (('viewBox="0 0 1440 400" preserveAspectRatio="xMidYMax slice"', 'viewBox="0 0 330 400" preserveAspectRatio="xMinYMax slice"'),
                 ('style="display: block; width: 100%; height: 400px; "', 'style="position: absolute; left: 0; bottom: 0; width: 100%; height: 100%"')):
        assert a in art, 'lib.landscape() changed its markup: update default_art() in og_cards.py'
        art = art.replace(a, b)
    return ('<div class="pic" style="background: linear-gradient(180deg, #F8EEDC 0%, #F3DFBA 55%, #EBC994 100%)">'
            + art + '<div class="fade"></div></div>')


def photo_panel(photo):
    path, pos, fit, _ = photo
    src = 'file://' + SITE_IMG + path
    assert os.path.isfile(SITE_IMG + path), f'seo.PAGES names a photo that is not in site-img/: {path}'
    if fit == 'contain':      # the whole photograph, framed like the site's photo cards (a wide group photo keeps every face)
        return (f'<div class="pic framed"><img src="{src}" alt="" style="object-position: {pos}"></div>')
    return f'<div class="pic"><img src="{src}" alt="" style="object-fit: cover; object-position: {pos}"><div class="fade"></div></div>'


def card_html(file):
    row = seo.PAGES[file]
    panel = photo_panel(row['photo']) if row.get('photo') else default_art()
    framed = ' framed-card' if row.get('photo') and row['photo'][2] == 'contain' else ''
    heading = html.escape(row['heading'], quote=False)
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{lib.FONT_HREF}" rel="stylesheet">
<style>
html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
* {{ box-sizing: border-box; }}
.card {{ position: relative; width: 1200px; height: 630px; overflow: hidden; background: linear-gradient(180deg, #FCF5EB 0%, #FBF2E7 100%);
  font-family: {lib.SANS}; color: {lib.INK}; }}
.txt {{ position: absolute; left: 0; top: 0; bottom: 0; width: 680px; padding: 54px 48px 50px 72px; display: flex; flex-direction: column; }}
.lock {{ display: flex; align-items: center; gap: 16px; }}
.lock img {{ width: 96px; height: auto; display: block; }}
.word {{ font-family: {lib.SERIF}; font-weight: 700; font-size: 44px; line-height: 0.95; letter-spacing: -0.012em; color: {lib.H1C}; }}
.tag {{ font-size: 13.5px; font-weight: 700; letter-spacing: 0.035em; line-height: 1.25; text-transform: uppercase; color: {lib.INK}; }}
.mid {{ flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 16px; min-height: 0; }}
h1 {{ margin: 0; font-family: {lib.SERIF}; font-weight: 680; font-size: 64px; line-height: 1.04; letter-spacing: -0.014em; color: {lib.H1C}; text-wrap: balance; }}
.foot {{ display: flex; align-items: center; gap: 18px; font-size: 19px; font-weight: 600; letter-spacing: 0.01em; color: {lib.MUTED}; }}
.bar {{ width: 150px; height: 8px; border-radius: 2px; overflow: hidden; display: flex; box-shadow: 0 0 0 1px {lib.LINE}; }}
.pic {{ position: absolute; top: 0; right: 0; bottom: 0; width: 520px; overflow: hidden; }}
.pic > img {{ display: block; width: 100%; height: 100%; }}
.fade {{ position: absolute; top: 0; bottom: 0; left: 0; width: 84px; background: linear-gradient(90deg, #FBF3E8 0%, rgba(251, 243, 232, 0) 100%); }}
.framed-card .txt {{ width: 600px; }}   /* the framed photo starts at 600 px: keep the heading clear of it */
.framed {{ width: 600px; display: flex; align-items: center; justify-content: center; padding: 40px 44px 40px 4px; }}
.framed > img {{ width: auto; height: auto; max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 16px;
  border: 1px solid {lib.LINE}; box-shadow: {lib.SHADOW}; }}
</style>
</head>
<body>
<div class="card{framed}">
{lib.branch(150, '#A5B195', 0.42, 'left: -88px; top: -40px; transform: rotate(8deg)')}
<div class="txt">
<div class="lock"><img src="file://{EMBLEM}" alt="">
<div style="display: flex; flex-direction: column; gap: 6px"><span class="word">IIPCT</span><span class="tag">Indigenous Interprofessional<br>Primary Care Team</span></div></div>
<div class="mid"><h1 id="h">{heading}</h1>{lib.SQUIGGLE}</div>
<div class="foot"><span class="bar">{BAR}</span><span>iipct.org</span></div>
</div>
{panel}
</div>
<script>
// shrink the heading until it fits its space (at most four lines), once the fonts are in
document.fonts.ready.then(function () {{
  var h = document.getElementById('h'), mid = h.parentNode, size = 64;
  while (size > 34 && (h.scrollWidth > h.clientWidth + 1 || h.offsetHeight > 4.3 * size * 1.04 || mid.scrollHeight > mid.clientHeight + 1)) {{
    size -= 2; h.style.fontSize = size + 'px';
  }}
  document.title = 'ready ' + size;
}});
</script>
</body>
</html>
'''


def shoot(html_path, png_path, profile):
    cmd = [CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
           '--allow-file-access-from-files', f'--user-data-dir={profile}', '--window-size=1200,630',
           '--virtual-time-budget=15000', '--run-all-compositor-stages-before-draw', f'--screenshot={png_path}', 'file://' + html_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not os.path.isfile(png_path):
        raise SystemExit(f'Chrome failed for {html_path}:\n{r.stderr[-1500:]}')


def save_jpeg(png_path, out_path):
    im = Image.open(png_path).convert('RGB')
    assert im.size == (seo.OG_W, seo.OG_H), f'{png_path}: screenshot is {im.size}, want {seo.OG_W}x{seo.OG_H}'
    for q in (86, 82, 78, 74, 70):
        buf = io.BytesIO(); im.save(buf, format='JPEG', quality=q, optimize=True, progressive=True)
        if buf.tell() <= MAX_BYTES:
            break
    data = buf.getvalue()
    assert len(data) <= MAX_BYTES, f'{out_path}: {len(data)} bytes even at quality {q}'
    if os.path.exists(out_path):
        old = Image.open(out_path)
        if old.size == im.size and open(out_path, 'rb').read() == data:
            return len(data), q, False
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, 'wb').write(data)
    return len(data), q, True


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    out = os.path.abspath(args.pop(0)) + '/'
    html_only = None
    if args[:1] == ['--html']:
        html_only = os.path.abspath(args[1]); args = args[2:]
    files = args or list(seo.PAGES)
    unknown = [f for f in files if f not in seo.PAGES]
    assert not unknown, f'not in seo.PAGES: {unknown}'
    if html_only:
        os.makedirs(html_only, exist_ok=True)
        for f in files:
            open(os.path.join(html_only, f), 'w').write(card_html(f))
        print(len(files), 'card pages written to', html_only)
        return
    assert CHROME, 'no Chrome found: install Google Chrome or set CHROME=/path/to/chrome'
    with tempfile.TemporaryDirectory(prefix='og-cards-') as tmp:
        for f in files:
            hp, pp = os.path.join(tmp, f), os.path.join(tmp, f[:-5] + '.png')
            open(hp, 'w').write(card_html(f))
            shoot(hp, pp, os.path.join(tmp, 'profile'))
            size, q, changed = save_jpeg(pp, out + seo.og_image(f))
            print(f'{seo.og_image(f):50} {size // 1024:4d} KB  q{q}  {"written" if changed else "unchanged"}')


if __name__ == '__main__':
    main()
