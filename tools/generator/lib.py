"""Shared building blocks for the IIPCT rebrand artboards (inline-styled markup)."""
import json, os, re, math, random
import facts
from facts import (LOCATIONS, EXTENSIONS, MAIN_PHONE, MAIN_TEL, GENERAL_EMAIL, BOOKING_URL, ORG_NAME, ORG_EN, ORG_SHORT,
                   hours_rows, address, option_text)

# ---------------------------------------------------------------- the server copy of the site
# Until iipct.org moves, the server version of the site (the events staff publish, sign-ups, staff sign-in) runs at
# this address and this static copy stays the public front end: the events lists on Home and Events & Programs follow
# the server's public events feed (tools/generator/live-events.js, copied to assets/js/), and the footer links to the
# server's sign-in. Empty = the feature is off and every page is exactly what it is without it.
# tools/publish-preview.sh --launch refuses while this is a test address (README: "Live events from the server").
LIVE_SITE = "https://taylordunning.ca"
assert LIVE_SITE == '' or re.fullmatch(r'https://[a-z0-9.-]+', LIVE_SITE), 'LIVE_SITE: an https:// origin with no path or trailing slash, or ""'

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets') + '/'
BLOB = json.load(open(A + 'blobs.json'))
META = json.load(open(A + 'meta.json'))

SERIF = "Newsreader, Georgia, 'Times New Roman', serif; font-variation-settings: 'opsz' 72"
SANS = "'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"
SCRIPT = "'Kaushan Script', 'Brush Script MT', cursive"
CREAM = '#FBF4EA'
INK = '#17231D'
HEAD = '#10291F'
H1C = '#0F3325'
RUST = '#8C2B18'
RUSTI = '#9C4530'
GOLD = '#C8A15A'
GOLDL = '#D9BC88'
MUTED = '#3A4640'
WRAP = 'max-width: 1440px; margin: 0 auto'
LINE = '#DCCBAB'
SHADOW = '0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)'
CARD = f'background: #F7F0E3; border: 1px solid {LINE}; box-shadow: {SHADOW}'

# ---------------------------------------------------------------- icons
def P(d): return f'<path d="{d}"></path>'
def Ci(cx, cy, r): return f'<circle cx="{cx}" cy="{cy}" r="{r}"></circle>'
def Rc(x, y, w, h, rx): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"></rect>'

_heart = 'M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z'
_cal = Rc(3.5, 5, 17, 15.5, 2.5) + P('M3.5 10h17') + P('M8 3v4') + P('M16 3v4')
_case = Rc(3, 7, 18, 13, 2) + P('M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2')
IC = {
 'arrow': P('M5 12h14') + P('M13 6l6 6-6 6'),
 'arrow-left': P('M19 12H5') + P('M11 6l-6 6 6 6'),
 'chev-down': P('M6 9l6 6 6-6'),
 'menu': P('M4 7h16') + P('M4 12h16') + P('M4 17h16'),
 'close': P('M6 6l12 12') + P('M18 6L6 18'),
 'chev-left': P('M15 6l-6 6 6 6'),
 'chev-right': P('M9 6l6 6-6 6'),
 'calendar': _cal,
 'calendar-check': _cal + P('M9 15l2 2 4-4'),
 'calendar-dot': _cal + P('M10.3 13.6h3.4v3.4h-3.4z'),
 'mail': Rc(3, 5, 18, 14, 2.5) + P('M3.5 7.5l8.5 6 8.5-6'),
 'phone': P('M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z'),
 'pin': P('M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z') + Ci(12, 10, 3),
 'clock': Ci(12, 12, 9) + P('M12 7v5l3 2'),
 'heart': P(_heart),
 'people': Ci(12, 8, 3) + P('M6.5 20v-1.5a5.5 5.5 0 0 1 11 0V20') + Ci(4.8, 10.5, 2.2) + P('M1.5 19v-.8a3.6 3.6 0 0 1 4.3-3.5') + Ci(19.2, 10.5, 2.2) + P('M22.5 19v-.8a3.6 3.6 0 0 0-4.3-3.5'),
 'feather': P('M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z') + P('M16 8 2 22') + P('M17.5 15H9'),
 'leaf': P('M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z') + P('M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12'),
 'sprout': P('M7 20h10') + P('M10 20c5.5-2.5.8-6.4 3-10') + P('M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z') + P('M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z'),
 'infinity': P('M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1.33-6 4Z'),
 'stethoscope': P('M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3') + P('M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4') + Ci(20, 10, 2),
 'bowl': P('M3.5 12.5h17c0 4.2-3.6 6.5-8.5 6.5s-8.5-2.3-8.5-6.5Z') + P('M9 21.5h6') + P('M10 9.5c-1.2-1.3 1.2-2.4 0-4') + P('M14 9.5c-1.2-1.3 1.2-2.4 0-4'),
 'lotus': P('M12 4.5c2.1 2.3 3.1 4.7 3.1 7.2 0 2.4-1 4.4-3.1 6.3-2.1-1.9-3.1-3.9-3.1-6.3 0-2.5 1-4.9 3.1-7.2Z') + P('M9.3 16.9c-2.9-.4-5-2.4-6.1-5.9 2.2-.4 4.1.1 5.7 1.5') + P('M14.7 16.9c2.9-.4 5-2.4 6.1-5.9-2.2-.4-4.1.1-5.7 1.5') + P('M5 20c2.2.6 4.6.9 7 .9s4.8-.3 7-.9'),
 'sunrise': P('M12 3v3') + P('M5.2 7.2l2 2') + P('M18.8 7.2l-2 2') + P('M2 16h3') + P('M19 16h3') + P('M7 16a5 5 0 0 1 10 0') + P('M3 20h18'),
 'scales': P('m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z') + P('m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z') + P('M7 21h10') + P('M12 3v18') + P('M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2'),
 'book': P('M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z') + P('M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z'),
 'chart': P('M4 20h16') + P('M7 20v-4') + P('M12 20v-7') + P('M17 20V10') + P('M5 11l5-4 3 2 6-5') + P('M16 4h3v3'),
 'award': Ci(12, 8, 6) + P('M15.477 12.89 17 22l-5-3-5 3 1.523-9.11') + Ci(12, 8, 2.2),
 'cycle': P('M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8') + P('M21 3v5h-5') + P('M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16') + P('M8 16H3v5'),
 'check': P('M5 12.5l4.5 4.5L19 7.5'),
 'check-circle': Ci(12, 12, 9) + P('M8 12.5l2.8 2.8L16 9.5'),
 'briefcase': _case + P('M3 13h18'),
 'bell': P('M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9') + P('M10.3 21a1.94 1.94 0 0 0 3.4 0'),
 'doc': P('M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z') + P('M14 3v5h5') + P('M9 13h6') + P('M9 17h6'),
 'review': Ci(11, 11, 7) + P('M21 21l-4.3-4.3') + Ci(11, 9.5, 1.8) + P('M7.8 14.2a3.4 3.4 0 0 1 6.4 0'),
 'handshake': P('m11 17 2 2a1 1 0 1 0 3-3') + P('m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4') + P('m21 3 1 11h-2') + P('M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3') + P('M3 4h8'),
 'send': P('M22 2 11 13') + P('M22 2l-7 20-4-9-9-4z'),
 'user': Ci(12, 8, 4) + P('M4 21v-1a7 7 0 0 1 16 0v1'),
 'question': P('M21 12a8.5 8.5 0 0 1-12.3 7.6L3.5 21l1.4-5.2A8.5 8.5 0 1 1 21 12Z') + P('M9.9 9.6a2.3 2.3 0 0 1 4.4.8c0 1.5-2.2 2-2.2 3.3') + P('M12.1 16.7h.01'),
 'tipi': P('M12 5 4.5 20h15L12 5Z') + P('M12 5l-2.2-2.5') + P('M12 5l2.2-2.5') + P('M10 20l2-5 2 5'),
 'syringe': P('m18 2 4 4') + P('m17 7 3-3') + P('M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5') + P('m9 11 4 4') + P('m5 19-3 3') + P('m14 4 6 6'),
 'kit': _case + P('M12 11v5') + P('M9.5 13.5h5'),
 'chat-heart': P('M21 11.5a8.4 8.4 0 0 1-12 7.6L3 21l1.9-5.7A8.4 8.4 0 1 1 21 11.5Z') + P('M12 15.2s-3-1.9-3-4.2a1.7 1.7 0 0 1 3-1 1.7 1.7 0 0 1 3 1c0 2.3-3 4.2-3 4.2Z'),
 'hand-heart': P('M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16') + P('m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9') + P('m2 15 6 6') + P('M19.5 8.5c.7-.7 1.5-1.6 1.5-2.7A2.73 2.73 0 0 0 16 4a2.78 2.78 0 0 0-5 1.8c0 1.2.8 2 1.5 2.8L16 12Z'),
 'apple': P('M12 20.94c1.5 0 2.75 1.06 4 1.06 3 0 6-8 6-12.22A4.91 4.91 0 0 0 17 5c-2.22 0-4 1.44-5 2-1-.56-2.78-2-5-2a4.9 4.9 0 0 0-5 4.78C2 14 5 22 8 22c1.25 0 2.5-1.06 4-1.06Z') + P('M10 2c1 .5 2 2 2 5'),
 'house': P('M3 10.5 12 3l9 7.5') + P('M5 9.5V20h14V9.5') + P('M10 20v-6h4v6'),
 'heart-plus': P(_heart) + P('M12 8.8v4.6') + P('M9.7 11.1h4.6'),
 'heart-pulse': P(_heart) + P('M3.3 12.2H9l1.4-2.6 2.6 5 1.6-2.4h6'),
 'pine': P('M12 2.5 7.5 8.5h2.6L6 14h3L5.2 19.5h13.6L15 14h3l-4.1-5.5h2.6L12 2.5Z') + P('M12 19.5V22'),
 'hand-sprout': P('M3 15.5h3.2l3.6 1.6h4a1.5 1.5 0 0 0 0-3H12') + P('M14.6 16.4l4.4-2a1.6 1.6 0 0 1 1.5 2.8L15 20.6H9L3 19.2') + P('M12 11.5V6.5') + P('M12 8.2c0-2.4-1.5-3.9-4-3.9 0 2.5 1.5 3.9 4 3.9Z') + P('M12 6.6c0-2 1.2-3.2 3.6-3.2 0 2-1.2 3.2-3.6 3.2Z'),
 'eye': P('M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z') + Ci(12, 12, 3),
 'droplet': P('M12 2.7c-3 3.6-6 6.9-6 10.3a6 6 0 0 0 12 0c0-3.4-3-6.7-6-10.3Z'),
 'shield': P('M12 3l7 3v5c0 4.6-3 8.3-7 10-4-1.7-7-5.4-7-10V6l7-3Z') + P('M9 12l2.2 2.2L15.2 10'),
 'lock': Rc(5, 11, 14, 10, 2) + P('M8 11V7.5a4 4 0 0 1 8 0V11'),
 'camera': P('M4 8h3l1.6-2.4h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z') + Ci(12, 13.2, 3.4),
 'map': P('M9 4 3 6.5v13L9 17l6 2.5 6-2.5v-13L15 6.5 9 4Z') + P('M9 4v13') + P('M15 6.5v13'),
 'access': Ci(12, 12, 9.5) + Ci(12, 7.4, 1.3) + P('M7.6 10.2c2.9.9 5.9.9 8.8 0') + P('M12 10.9v3.5') + P('M12 14.4l-2.3 4') + P('M12 14.4l2.3 4'),
 'external': P('M14 4h6v6') + P('M20 4l-9 9') + P('M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5'),
 'globe': Ci(12, 12, 9) + P('M3 12h18') + P('M12 3c2.6 2.9 3.9 5.9 3.9 9s-1.3 6.1-3.9 9c-2.6-2.9-3.9-5.9-3.9-9s1.3-6.1 3.9-9Z'),
 'help': Ci(12, 12, 9) + P('M9.6 9.3a2.5 2.5 0 0 1 4.8.9c0 1.7-2.4 2.2-2.4 3.7') + P('M12 17h.01'),
 'info': Ci(12, 12, 9) + P('M12 11v5.5') + P('M12 7.6h.01'),
 'bolt': P('M13 2 4 14h7l-1 8 9-12h-7l1-8Z'),
 'route': Ci(6, 18.5, 2.5) + Ci(18, 5.5, 2.5) + P('M8.5 18.5H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5'),
 'foot': P('M9 3.5c2.6 0 4 2 4 5 0 2.2-.8 3.6-.8 5.6 0 1.7 1.4 2.6 1.4 4.4a3 3 0 0 1-3 3c-2.3 0-3.6-1.7-3.6-4.2 0-2.4.9-3.9.9-6.1 0-1.8-1-2.7-1-4.5 0-1.9.7-3.2 2.1-3.2Z') + P('M16 5.2v.01') + P('M17.6 8v.01') + P('M18 11v.01'),
 'baby': Ci(12, 12, 9) + P('M9 9.6v.01') + P('M15 9.6v.01') + P('M9 14c.8 1.1 1.8 1.6 3 1.6s2.2-.5 3-1.6') + P('M11 3.2c0 1.6 2 1.6 2 0'),
 'news': Rc(3, 4.5, 15, 15.5, 2) + P('M18 9h2a1 1 0 0 1 1 1v8a2 2 0 0 1-2 2H6') + P('M7 9h7') + P('M7 13h7') + P('M7 16.5h4'),
}

def ico(name, size=20, color='currentColor', sw=1.7, style=''):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="flex: none; {style}">{IC[name]}</svg>')

def pin_fill(size=18, color='#A0432C', dot='#FBF4EA', style=''):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" style="flex: none; {style}">'
            f'<path d="M20 10c0 6-8 12.5-8 12.5S4 16 4 10a8 8 0 0 1 16 0Z" fill="{color}"></path><circle cx="12" cy="10" r="3" fill="{dot}"></circle></svg>')

CIRC = {'sage': ('#8E9C7A', '#75866A'), 'rust': ('#BD7862', '#A55A43'), 'gold': ('#DDBB8C', '#C59D69'), 'forest': ('#4E6B4B', '#3A5639')}
def circ(name, tone='sage', size=66, isize=None, sw=1.5, style=''):
    hi, lo = CIRC[tone]
    isize = isize or round(size * 0.52)
    return (f'<span class="ci" style="flex: none; width: {size}px; height: {size}px; border-radius: 50%; display: flex; align-items: center; justify-content: center; '
            f'background: radial-gradient(circle at 38% 30%, {hi} 0%, {lo} 78%); box-shadow: 0 0 0 2px #FFFDF8, 0 0 0 3px rgba(120, 92, 44, 0.32); {style}">'
            f'{ico(name, isize, "#FCF2DF", sw)}</span>')

def img(name, alt, style):
    return f'<img src="{BLOB[name]}" alt="{alt}" style="display: block; {style}">'

def photo(path, alt, style='', cls='', w=None, h=None, lazy=True):
    """A real photograph kept as an ordinary file: tools/generator/site-img/<path>, published as assets/img/<path>.
    (img() above is for the crops taken from the design mock-ups.) Give the file's real width and height so the page
    does not jump while it loads."""
    c = f' class="{cls}"' if cls else ''
    wh = (f' width="{w}" height="{h}"' if w and h else '') + (' loading="lazy" decoding="async"' if lazy else '')
    return f'<img{c} src="/_site/{path}" alt="{alt}"{wh} style="display: block; {style}">'

# ---------------------------------------------------------------- type helpers
def eyebrow(text, color=RUST, style=''):
    return f'<span style="display: block; font-size: 12.8px; font-weight: 700; letter-spacing: 0.16em; line-height: 1.1; text-transform: uppercase; color: {color}; {style}">{text}</span>'

def h2(text, size=32, color=HEAD, style='', tag='h2', weight=600):
    cls = ' class="h2"' if size >= 22 else ''
    return f'<{tag}{cls} style="margin: 0; font-family: {SERIF}; font-weight: {weight}; font-size: {size}px; line-height: 1.06; letter-spacing: -0.018em; color: {color}; {style}">{text}</{tag}>'

def p(text, size=14, color=INK, lh=1.36, style='', cls='t-b'):
    c = f' class="{cls}"' if cls else ''
    return f'<p{c} style="margin: 0; font-size: {size}px; line-height: {lh}; color: {color}; {style}">{text}</p>'

def vdiv(h='100%', color=GOLDL, style=''):
    return f'<span class="vd" aria-hidden="true" style="flex: none; align-self: stretch; width: 1px; min-height: {h}; background: {color}; {style}"></span>'

SQUIGGLE = ('<svg class="sqg" aria-hidden="true" width="160" height="17" viewBox="0 0 160 17" style="display: block">'
            '<path d="M1 15 C 24 5 58 1 95 4 C 118 6 140 5.6 159 1 C 145 10.6 120 13.6 94 11 C 62 7.8 30 9.8 1 15 Z" fill="#C79A3D"></path></svg>')

# ---------------------------------------------------------------- buttons
# Booking has one name: "Schedule Your Visit" (the one word "Schedule" where there is no room), always to that page.
BOOK_LABELS = ('Schedule Your Visit',)
def btn(label, href='#', kind='primary', icon=None, arrow=True, size='md', style='', cls=''):
    if label in BOOK_LABELS:
        href = 'Booking.dc.html'
    h, fs, px = {'xs': (30, 12, 13), 'sm': (37, 13.2, 14), 'md': (42, 13.7, 22), 'lg': (44, 14.2, 26)}[size]
    base = (f'display: inline-flex; align-items: center; justify-content: center; gap: 9px; min-height: {h}px; padding: 0 {px}px; border-radius: 9px; '
            f'font-size: {fs}px; font-weight: 600; line-height: 1; text-decoration: none; white-space: nowrap; ')
    look = {
        'primary': 'background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; border: 1px solid #2E5E38; box-shadow: 0 3px 7px rgba(16, 44, 24, 0.28)',
        'outline': 'background: #FFFDF8; color: #13261B; border: 1.5px solid #1E3D28; box-shadow: 0 2px 5px rgba(40, 30, 10, 0.08)',
        'gold': 'background: rgba(10, 35, 24, 0.25); color: #FFFFFF; border: 1px solid #C8A15A',
        'light': 'background: #FFFDF8; color: #13261B; border: 1px solid #F1E3CF; box-shadow: 0 2px 5px rgba(60, 25, 10, 0.18)',
        'soft': 'background: linear-gradient(180deg, #F3EDD9 0%, #E7E0C8 100%); color: #13261B; border: 1px solid #CFC9AA; box-shadow: 0 2px 4px rgba(40, 30, 10, 0.10)',
        'sage': 'background: #FAF6EA; color: #133019; border: 1.5px solid #7E9471; box-shadow: 0 2px 4px rgba(40, 30, 10, 0.07)',
    }[kind]
    # hover classes (HOVER_CSS): bp primary, bo outline, bl light button on a dark band, bg gold-edged on a dark band, bs soft
    cls = {'primary': 'btn bp', 'outline': 'btn bo', 'gold': 'btn bg', 'light': 'btn bl', 'soft': 'btn bs', 'sage': 'btn bo'}[kind] + (' ' + cls if cls else '')
    ic = ico(icon, round(fs + 3.5), 'currentColor', 1.8) if icon else ''
    ar = ico('arrow', round(fs + 1.5), 'currentColor', 2) if arrow else ''
    return f'<a class="{cls}" href="{href}" style="{base}{look}; {style}">{ic}<span>{label}</span>{ar}</a>'

def textlink(label, href='#', size=14.4, style='', icon='arrow', cls=''):
    return (f'<a class="tl{" " + cls if cls else ""}" href="{href}" style="display: inline-flex; align-items: center; gap: 12px; font-size: {size}px; font-weight: 600; color: {RUST}; text-decoration: none; white-space: nowrap; {style}">'
            f'<span style="text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1.5px">{label}</span>{ico(icon, size + 2, RUST, 1.9)}</a>')

def round_arrow(size=24, name='arrow', label='Open', href='#', style=''):
    return (f'<a class="ra" href="{href}" aria-label="{label}" style="flex: none; width: {size}px; height: {size}px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; '
            f'background: #FFFDF8; border: 1px solid #C9B691; color: #13261B; {style}">{ico(name, round(size * 0.52), "#13261B", 2)}</a>')

# ---------------------------------------------------------------- decoration
BRANCH_PATHS = (P('M132 370C125 277 119 212 144 32') +
                ''.join(f'<path fill="currentColor" fill-opacity="0.5" d="{d}"></path>' for d in [
                    'M137 315q92 -63 87 -9q-57 27 -87 9Z', 'M130 281q-100 -75 -93 -10q51 29 93 10Z', 'M137 247q92 -63 87 -9q-57 27 -87 9Z',
                    'M130 213q-100 -75 -93 -10q51 29 93 10Z', 'M137 179q92 -63 87 -9q-57 27 -87 9Z', 'M130 145q-100 -75 -93 -10q51 29 93 10Z',
                    'M137 111q92 -63 87 -9q-57 27 -87 9Z', 'M130 77q-100 -75 -93 -10q51 29 93 10Z']))

def branch(w=120, color='#A9B59A', opacity=0.55, style='', sw=4, outline=False):
    paths = BRANCH_PATHS.replace('fill="currentColor" fill-opacity="0.5"', 'fill="none"') if outline else BRANCH_PATHS
    return (f'<svg class="dcb" aria-hidden="true" width="{w}" height="{round(w * 380 / 260)}" viewBox="0 0 260 380" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="position: absolute; pointer-events: none; color: {color}; opacity: {opacity}; {style}">{paths}</svg>')

def pine_d(x, base, h, w, tiers=4):
    pts_r = []
    for i in range(1, tiers + 1):
        y = base - h + h * 0.9 * i / tiers
        tw = w * 0.5 * (0.3 + 0.7 * i / tiers)
        pts_r.append((x + tw, y))
        if i < tiers:
            pts_r.append((x + tw * 0.42, y))
    tr = max(w * 0.07, 0.9)
    yl = pts_r[-1][1]
    d = f'M{x:.1f} {base - h:.1f}' + ''.join(f'L{px:.1f} {py:.1f}' for px, py in pts_r)
    d += f'L{x + tr:.1f} {yl:.1f}L{x + tr:.1f} {base:.1f}L{x - tr:.1f} {base:.1f}L{x - tr:.1f} {yl:.1f}'
    d += ''.join(f'L{2 * x - px:.1f} {py:.1f}' for px, py in reversed(pts_r)) + 'Z'
    return d

def pines(spec, w, h, fill='#B7C2A4', opacity=0.8, style=''):
    """spec: list of (x, height, width, alpha) with base at the bottom of the box."""
    body = ''.join(f'<path d="{pine_d(x, h, ph, pw)}" fill-opacity="{a}"></path>' for x, ph, pw, a in spec)
    return (f'<svg class="dcp" aria-hidden="true" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="{fill}" '
            f'style="position: absolute; pointer-events: none; opacity: {opacity}; {style}">{body}</svg>')

PINES_L = [(26, 66, 36, 0.55), (62, 118, 62, 0.9), (104, 58, 34, 0.5), (140, 88, 50, 0.85), (178, 40, 26, 0.45), (12, 34, 22, 0.4)]
PINES_R = [(22, 44, 28, 0.5), (56, 82, 46, 0.85), (92, 52, 32, 0.55), (122, 104, 56, 0.9), (160, 62, 36, 0.6), (188, 36, 24, 0.4)]

def landscape(h=98, sun_x=720, style='', tall=False, cls=''):
    """Rolling hills, sun and tree lines along the bottom edge. tall=True adds the big left stand of pines and a second sun."""
    rnd = random.Random(7)
    trees = ''
    for side in (0, 1):
        x = 6.0
        while x < 372:
            frac = 1 - x / 372
            ph = (16 + 40 * frac ** 1.25) * rnd.uniform(0.72, 1.12)
            if tall and side == 0:
                ph *= 1.0 + 1.25 * frac ** 1.6
            pw = ph * rnd.uniform(0.44, 0.56)
            base = h - 28 + 7 * (1 - frac) + rnd.uniform(-1.5, 1.5)
            xx = x if side == 0 else 1440 - x
            trees += f'<path d="{pine_d(xx, base, ph, pw)}"></path>'
            x += pw * rnd.uniform(0.62, 0.95)
    extra = ''
    if tall:
        extra = (f'<circle cx="232" cy="{h - 84}" r="40" fill="#E6B768"></circle>'
                 f'<path d="M0 {h - 58} C 120 {h - 96} 300 {h - 104} 470 {h - 62} S 640 {h - 30} 760 {h - 34} V{h} H0Z" fill="#9FAF8C"></path>')
    c = f' class="{cls}"' if cls else ''
    return f'''<svg{c} aria-hidden="true" viewBox="0 0 1440 {h}" preserveAspectRatio="xMidYMax slice" style="display: block; width: 100%; height: {h}px; {style}">
{extra}<path d="M0 {h - 44} C 150 {h - 62} 300 {h - 60} 470 {h - 44} S 700 {h - 30} 860 {h - 36} S 1180 {h - 64} 1440 {h - 48} V{h} H0Z" fill="#B4C0A1"></path>
<path d="M0 {h - 36} C 190 {h - 52} 380 {h - 44} 560 {h - 32} S 900 {h - 24} 1090 {h - 40} S 1330 {h - 50} 1440 {h - 42} V{h} H0Z" fill="#7C9070"></path>
<circle cx="{sun_x}" cy="{h - 26}" r="36" fill="#DDAB5B"></circle>
<circle cx="{sun_x - 4}" cy="{h - 31}" r="27" fill="#EBC581" fill-opacity="0.55"></circle>
<path d="M0 {h - 24} C 220 {h - 36} 430 {h - 26} 620 {h - 24} S 900 {h - 22} 1060 {h - 30} S 1320 {h - 36} 1440 {h - 28} V{h} H0Z" fill="#35553B"></path>
<g fill="#173A28">{trees}</g>
<path d="M0 {h - 15} C 300 {h - 22} 520 {h - 18} 720 {h - 18} S 1180 {h - 22} 1440 {h - 16} V{h} H0Z" fill="#17392A"></path>
<path d="M0 {h - 7} C 300 {h - 12} 520 {h - 9} 720 {h - 9} S 1180 {h - 12} 1440 {h - 8} V{h} H0Z" fill="#0C271D"></path>
<g stroke="#E0B463" stroke-linecap="round" stroke-width="1.3" opacity="0.55"><path d="M{sun_x - 34} {h - 15}h68"></path><path d="M{sun_x - 24} {h - 11}h48"></path><path d="M{sun_x - 14} {h - 7}h28"></path></g>
</svg>'''

def horizon(w=480, h=64, cls='', seed=11):
    """landscape() drawn for a narrow box (phones: w=480, tablets: w=960): the same hills stretched to the box, the sun
    off centre and a stand of pines at each end, so the brand's horizon reads at phone width (the 1440-wide drawing
    shows only hills and the sun there). Scales with the width of its box (height follows); hidden at 1100 px and up."""
    rnd = random.Random(seed)
    k = w / 1440
    span = w * 0.3
    trees = ''
    for side in (0, 1):
        x = 3.0
        while x < span:
            frac = 1 - x / span
            ph = (11 + (h * 0.62) * frac ** 1.3) * rnd.uniform(0.74, 1.1)
            pw = ph * rnd.uniform(0.44, 0.56)
            base = h - 11 + 4 * (1 - frac) + rnd.uniform(-1, 1)
            xx = x if side == 0 else w - x
            trees += f'<path d="{pine_d(xx, base, ph, pw)}"></path>'
            x += pw * rnd.uniform(0.6, 0.9)
    sx, r = round(w * 0.64), round(h * 0.4)
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} aria-hidden="true" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMax meet" style="width: 100%; height: auto">'
            f'<g transform="scale({k:.4f} 1)">'
            f'<path d="M0 {h - 34} C 150 {h - 48} 300 {h - 47} 470 {h - 34} S 700 {h - 24} 860 {h - 29} S 1180 {h - 50} 1440 {h - 38} V{h} H0Z" fill="#B4C0A1"></path>'
            f'<path d="M0 {h - 28} C 190 {h - 41} 380 {h - 35} 560 {h - 25} S 900 {h - 19} 1090 {h - 31} S 1330 {h - 39} 1440 {h - 33} V{h} H0Z" fill="#7C9070"></path></g>'
            f'<g class="hz-sun"><circle cx="{sx}" cy="{h - 20}" r="{r}" fill="#DDAB5B"></circle>'
            f'<circle cx="{sx - 3}" cy="{h - 24}" r="{round(r * 0.75)}" fill="#EBC581" fill-opacity="0.55"></circle></g>'
            f'<g transform="scale({k:.4f} 1)">'
            f'<path d="M0 {h - 18} C 220 {h - 27} 430 {h - 20} 620 {h - 18} S 900 {h - 17} 1060 {h - 23} S 1320 {h - 27} 1440 {h - 21} V{h} H0Z" fill="#35553B"></path></g>'
            f'<g fill="#173A28">{trees}</g>'
            f'<g transform="scale({k:.4f} 1)">'
            f'<path d="M0 {h - 10} C 300 {h - 15} 520 {h - 12} 720 {h - 12} S 1180 {h - 15} 1440 {h - 11} V{h} H0Z" fill="#17392A"></path>'
            f'<path d="M0 {h - 5} C 300 {h - 8} 520 {h - 6} 720 {h - 6} S 1180 {h - 8} 1440 {h - 5} V{h} H0Z" fill="#0C271D"></path></g>'
            f'<g stroke="#E0B463" stroke-linecap="round" stroke-width="1.2" opacity="0.55"><path d="M{sx - 22} {h - 9}h44"></path><path d="M{sx - 14} {h - 6}h28"></path></g>'
            f'</svg>')

def hero_horizon():
    """Closes a hero on phones and tablets with the drawn horizon (one drawing per size; hidden at 1100 px and up)."""
    return f'<div class="hero-hz" aria-hidden="true">{horizon(480, 64, "hz-p")}{horizon(960, 80, "hz-t", 5)}</div>'

def arc_photo(name, alt, style='', rad='62% 56%', br=''):
    """Photo with the big curved top-right corner and the gold arc line behind it."""
    extra = f'border-bottom-right-radius: {br}; ' if br else ''
    return (f'<div style="position: relative; {style}">'
            f'<div aria-hidden="true" style="position: absolute; inset: 0; border-top-right-radius: {rad}; '
            f'background-image: linear-gradient(180deg, rgba(251, 244, 234, 0) 42%, #FBF4EA 74%), linear-gradient(90deg, #FBF4EA 30%, #CBA35A 62%)"></div>'
            + img(name, alt, f'position: absolute; left: 0; top: 4px; width: calc(100% - 5px); height: calc(100% - 4px); object-fit: cover; border-top-right-radius: {rad}; {extra}')
            + '</div>')

# ---------------------------------------------------------------- header / footer
NAV = [('Home', 'Main.dc.html', False, 'home'), ('Who We Are', 'WhoWeAre.dc.html', True, 'who'), ('Services', 'Services.dc.html', True, 'services'),
       ('Events &amp; Programs', 'Events.dc.html', True, 'events'), ('Careers', 'Careers.dc.html', False, 'careers'), ('Board', 'Board.dc.html', False, 'board'),
       ('BPSO', 'BPSO.dc.html', False, 'bpso'), ('Contact', 'Contact.dc.html', False, 'contact')]

NEWSLETTER_URL = facts.NEWSLETTER_URL
MENUS = {
 'who': [('About IIPCT', 'WhoWeAre.dc.html', 0), ('Our Team', 'Team.dc.html', 0), ('Career Opportunities', 'Careers.dc.html', 0), ('Board of Directors', 'Board.dc.html', 0), ('Best Practice Spotlight (BPSO)', 'BPSO.dc.html', 0)],
 'services': [('All Services', 'Services.dc.html', 0), ('Primary Medical Care', 'PrimaryCare.dc.html', 0), ('Immunization Program', 'Immunization.dc.html', 1),
              ('Well Baby &amp; Well Child', 'WellBaby.dc.html', 1), ('TB Testing', 'TBTesting.dc.html', 1), ('Advanced Foot Care', 'FootCare.dc.html', 1),
              ('Diabetic Retinopathy Screening', 'Retinopathy.dc.html', 1), ('Outreach &amp; Community Support', 'Outreach.dc.html', 1)],
 'events': [('Events &amp; Programs', 'Events.dc.html', 0), ('News &amp; Updates', 'News.dc.html', 0), ('Newsletter', NEWSLETTER_URL, 0)],
}

def book_btn(href='Booking.dc.html'):
    """Header CTA: one primary button. Booking has one name and one place (Schedule Your Visit)."""
    return (f'<a class="btn bp hd-cta" href="{href}" style="flex: none; display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 44px; padding: 0 16px; '
            f'border-radius: 10px; font-size: 12.6px; font-weight: 600; line-height: 1; text-decoration: none; white-space: nowrap; '
            f'background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; border: 1px solid #2E5E38; box-shadow: 0 1px 2px rgba(16, 44, 24, 0.20)">'
            f'{ico("calendar-check", 16, "currentColor", 1.8)}<span>Schedule Your Visit</span></a>')

def _menu(key):
    rows = ''
    for label, href, lvl in MENUS[key]:
        ext = ico('external', 13, '#8C2B18', 1.9) if href.startswith('http') else ''
        if lvl:
            st = 'padding: 7px 12px 7px 26px; font-size: 12.8px; font-weight: 500; color: #3A4640'
        else:
            st = 'padding: 9px 12px; font-size: 13.4px; font-weight: 600; color: #10291F'
        rows += (f'<a class="mi" href="{href}" style="display: flex; align-items: center; justify-content: space-between; gap: 14px; border-radius: 8px; '
                 f'line-height: 1.2; text-decoration: none; white-space: nowrap; {st}"><span>{label}</span>{ext}</a>')
    return (f'<span class="nvm"><span style="display: flex; flex-direction: column; gap: 1px; min-width: 236px; padding: 8px; border-radius: 12px; '
            f'background: #FFFDF8; border: 1px solid {LINE}; box-shadow: 0 2px 4px rgba(40, 30, 10, 0.06), 0 14px 28px rgba(40, 30, 10, 0.16); letter-spacing: 0">{rows}</span></span>')

def _mobile(active):
    """Book button + menu for tablet and phone widths. The menu is a native <details>, so it opens without script.
    The menu opens as a full-width sheet: one group per section (section row, then its pages in a grid of large rows).
    export_site.py marks the link to the page being shown (class cur, aria-current="page").
    The header's Schedule button (hd-book) is hidden wherever the bottom action bar (action_bar) carries Schedule."""
    rows = ''
    for label, href, dd, key in NAV:
        col = '#9A3B26' if key == active else '#10291F'
        subs = ''
        for l2, h2, lvl in (MENUS[key][1:] if dd else []):
            x = ico('external', 13, '#8C2B18', 1.9) if h2.startswith('http') else ''
            subs += (f'<a class="ml ml2" href="{h2}" style="display: flex; align-items: center; gap: 8px; min-height: 44px; padding: 6px 10px 6px 12px; border-radius: 9px; font-size: 15px; '
                     f'font-weight: 500; line-height: 1.25; color: #3A4640; text-decoration: none"><span>{l2}</span>{x}</a>')
        rows += (f'<div class="ml-g"><a class="ml ml1{" ml-on" if key == active else ""}" href="{href}" style="display: flex; align-items: center; min-height: 52px; padding: 0 12px; border-radius: 9px; '
                 f'font-size: 17px; font-weight: 700; color: {col}; text-decoration: none">{label}</a>'
                 + (f'<div class="ml-sub">{subs}</div>' if subs else '') + '</div>')
    book = ('display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 44px; padding: 0 15px; border-radius: 10px; font-size: 13.6px; font-weight: 600; line-height: 1; '
            'text-decoration: none; white-space: nowrap; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; border: 1px solid #2E5E38')
    return (f'<div class="hd-m">'
            f'<a class="btn bp hd-book" href="Booking.dc.html" style="{book}">{ico("calendar-check", 17, "currentColor", 1.8)}<span>Schedule<span class="xs-hide"> Your Visit</span></span></a>'
            f'<details class="mnav"><summary class="bo" aria-label="Menu" style="width: 46px; height: 44px; border-radius: 10px; border: 1.5px solid #1E3D28; background: #FFFDF8; color: #13261B; '
            f'display: flex; align-items: center; justify-content: center; cursor: pointer">'
            f'<span class="mi-o" style="display: flex">{ico("menu", 22, "currentColor", 2)}</span><span class="mi-x" style="display: flex">{ico("close", 22, "currentColor", 2)}</span></summary>'
            f'<div class="msheet" style="position: absolute; left: 0; right: 0; top: 100%; z-index: 40; padding: 10px 20px 22px; background: #FFFDF8; border-top: 1px solid {LINE}; border-bottom: 1px solid {LINE}; '
            f'box-shadow: 0 18px 30px rgba(40, 30, 10, 0.18)"><nav class="mlist" aria-label="Menu" style="display: flex; flex-direction: column; gap: 1px">{rows}</nav>'
            f'<div class="mfoot" style="margin-top: 14px; padding-top: 16px; border-top: 1px solid {LINE}; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px">'
            f'<a class="btn bp" href="Booking.dc.html" style="{book}; flex: 1 1 220px; min-height: 48px; font-size: 15px">{ico("calendar-check", 18, "currentColor", 1.8)}<span>Schedule Your Visit</span></a>'
            f'<a href="tel:{MAIN_TEL}" style="display: inline-flex; align-items: center; gap: 10px; min-height: 44px; font-size: 16px; font-weight: 700; color: #10291F; text-decoration: none">'
            f'{ico("phone", 19, "#9C4530", 1.8)}<span>{MAIN_PHONE}</span></a></div></div></details></div>')

NAV_SIZE = 14
def header(active):
    items = ''
    for label, href, dd, key in NAV:
        on = key == active
        col = '#9A3B26' if on else '#10291F'
        bb = '#9A3B26' if on else 'transparent'
        chev = ico('chev-down', 12, col, 2.4) if dd else ''
        link = (f'<a class="nv{" nv-on" if on else ""}" href="{href}" style="display: inline-flex; align-items: center; gap: 5px; padding: 10px 0 8px; border-bottom: 2px solid {bb}; '
                f'color: {col}; text-decoration: none; white-space: nowrap">{label}{chev}</a>')
        items += f'<span class="nvi">{link}{_menu(key)}</span>' if dd else link
    return f'''
<header style="position: relative; z-index: 20; border-bottom: 1px solid {LINE}">
<div class="hd" style="{WRAP}; padding: 11px 40px 10px 48px; min-height: 102px; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px">
<a class="lg" href="Main.dc.html" style="display: flex; align-items: center; gap: 12px; text-decoration: none; color: {H1C}">
{img('logo-emblem', 'IIPCT logo: a turtle carrying a medicine wheel, with a stethoscope shaped like a heart', 'width: 80px; height: auto').replace('<img ', '<img class="hd-logo" ')}
<span style="display: flex; flex-direction: column; gap: 5px">
<span class="lgw" style="font-family: {SERIF}; font-weight: 700; font-size: 30px; line-height: 0.95; letter-spacing: -0.012em; color: {H1C}">IIPCT</span>
<span class="hd-tag lk" style="font-size: 9.6px; font-weight: 700; letter-spacing: 0.035em; line-height: 1.22; text-transform: uppercase; color: {INK}">Indigenous Interprofessional<br class="k">Primary Care Team</span>
</span>
</a>
<span class="hd-div" aria-hidden="true" style="flex: none; width: 1px; height: 60px; background: {GOLDL}; margin: 0 8px 0 2px"></span>
<nav class="hd-nav" aria-label="Main" style="flex: 1 1 420px; min-width: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 17px; font-size: {NAV_SIZE}px; font-weight: 600; letter-spacing: -0.005em">{items}</nav>
{book_btn()}
{_mobile(active)}
</div>
</header>'''

def _fcol(title, links, w, pl, cls=''):
    rows = ''.join(f'<a class="fl" href="{h}" style="color: #F4EFE4; text-decoration: none; font-size: 12.4px; line-height: 1.2">{t}</a>' for t, h in links)
    return (f'<div class="ft-col{" " + cls if cls else ""}" style="flex: none; width: {w}px; min-height: 110px; padding: 2px 10px 2px {pl}px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; flex-direction: column; gap: 10px">'
            f'<span style="font-size: 13.2px; font-weight: 700; color: #FFFFFF; margin-bottom: 3px">{title}</span>{rows}</div>')

def footer(top_h=90, pre='', tall=False):
    crow = lambda ic, t, h: (f'<a class="fl" href="{h}" style="display: flex; align-items: center; gap: 13px; color: #F4EFE4; text-decoration: none; font-size: 12.4px; line-height: 1.2">{ico(ic, 17, "#D9B36A", 1.7)}<span>{t}</span></a>')
    bar = ''.join(f'<span style="flex: 1; background: {c}"></span>' for c in ['#FEFDFC', '#F7D80C', '#BA2B2C', '#0A8242'])
    pipe = '<span class="ft-pipe" aria-hidden="true" style="width: 1px; height: 15px; background: #C8A15A"></span>'
    # the way to the server's sign-in (staff, members): only while LIVE_SITE is set
    signin = (f'\n{pipe}<a class="fl" href="{LIVE_SITE}/login" style="min-width: 44px; justify-content: center; text-align: center; color: #F4EFE4; text-decoration: none">Sign in</a>') if LIVE_SITE else ''   # min-width: a short word still makes a 44 px wide tap target
    return f'''
<footer style="position: relative; margin-top: 4px">
{pre}{landscape(top_h, 720, '', tall, 'hz-d')}{horizon(480, 64, 'hz-p ft-hz', 3)}
<div class="ft-dark" style="background: #0C271D; color: #F4EFE4; margin-top: -1px">
<div style="{WRAP}; padding: 14px 40px 0 55px">
<div class="ft-row" style="display: flex; flex-wrap: wrap; gap: 26px 0; align-items: flex-start; padding-bottom: 22px">
<div class="ft-logo" style="flex: none; width: 308px; display: flex; flex-direction: column; align-items: flex-start; gap: 14px; padding-top: 2px">
<a class="lg lgd" href="Main.dc.html" style="display: flex; align-items: center; gap: 13px; text-decoration: none">
<span style="flex: none; width: 94px; height: 94px; border-radius: 50%; background: #FBF4EA; display: flex; align-items: center; justify-content: center">{img('logo-emblem', 'IIPCT logo', 'width: 76px; height: auto')}</span>
<span style="display: flex; flex-direction: column; gap: 6px">
<span class="lgw" style="font-family: {SERIF}; font-weight: 600; font-size: 33px; line-height: 0.95; letter-spacing: -0.01em; color: #FFFFFF">IIPCT</span>
<span class="lk" style="font-size: 9.6px; font-weight: 600; letter-spacing: 0.06em; line-height: 1.25; text-transform: uppercase; color: #FFFFFF">Indigenous Interprofessional<br class="k">Primary Care Team</span>
</span>
</a>
{social_row(dark=True)}
</div>
<div class="ft-col ft-contact" style="flex: none; width: 278px; min-height: 110px; padding: 2px 10px 2px 40px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; flex-direction: column; gap: 10px">
<span style="font-size: 13.2px; font-weight: 700; color: #FFFFFF; margin-bottom: 3px">Contact Us</span>
{crow('phone', MAIN_PHONE, 'tel:' + MAIN_TEL)}
{crow('mail', GENERAL_EMAIL, 'mailto:' + GENERAL_EMAIL)}
{crow('pin', f'{len(LOCATIONS)} locations in southeastern Ontario', 'Contact.dc.html#locations')}
{crow('clock', 'Hours differ by location', 'Contact.dc.html#locations')}
</div>
{_fcol('Quick Links', [('Home', 'Main.dc.html'), ('Who We Are', 'WhoWeAre.dc.html'), ('Services', 'Services.dc.html'), ('Events &amp; Programs', 'Events.dc.html'), ('News &amp; Updates', 'News.dc.html'), ('Newsletter', NEWSLETTER_URL)], 196, 42, 'ft-ql')}
{_fcol('Our Locations', [(l['name'], 'Contact.dc.html#' + l['key']) for l in LOCATIONS], 198, 41, 'ft-loc')}
{_fcol('More', [('Careers', 'Careers.dc.html'), ('Board', 'Board.dc.html'), ('BPSO', 'BPSO.dc.html'), ('Contact', 'Contact.dc.html')], 127, 41, 'ft-more')}
<div class="ft-col ft-art" style="flex: none; min-height: 110px; padding-left: 34px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; align-items: center; gap: 20px">
{img('feather-gold', '', 'width: 70px; height: auto; margin-top: -4px')}
<span style="display: flex; flex-direction: column; gap: 3px; font-family: {SCRIPT}; font-size: 21px; line-height: 1.38; color: #DDB86C">
<span>Culture</span><span>Community</span><span>Care</span><span>Wellness</span>
</span>
</div>
</div>
<div class="ft-legal" style="border-top: 1px solid rgba(255, 255, 255, 0.42); padding: 15px 0 19px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; font-size: 12.4px; color: #F4EFE4">
<span>© 2026 {ORG_NAME} ({ORG_SHORT}). All rights reserved.</span>
{pipe}<a class="fl" href="Privacy.dc.html" style="color: #F4EFE4; text-decoration: none">Privacy Policy</a>
{pipe}<a class="fl" href="Accessibility.dc.html" style="color: #F4EFE4; text-decoration: none">Accessibility</a>
{pipe}<a class="fl" href="SiteMap.dc.html" style="color: #F4EFE4; text-decoration: none">Site Map</a>{signin}
{pipe}<span>Built by <a class="fl dg" href="https://pixelelite.ca" style="color: #E3BE74; font-weight: 600; text-decoration: none">Pixel Elite Media</a> · <a class="fl" href="https://pixelelite.ca" style="color: #F4EFE4; text-decoration: none">pixelelite.ca</a></span>
<span class="ft-bar" aria-hidden="true" style="margin-left: auto; width: 150px; height: 7px; border-radius: 2px; overflow: hidden; display: flex">{bar}</span>
</div>
</div>
</div>
</footer>
{action_bar()}'''

def action_bar():
    """The two things people come for, always under the thumb on phones and tablets: Call, Schedule, Locations.
    Plain links in a bar fixed to the bottom of the screen (styles: .mbar in RESP_CSS). Hidden from 1100 px, on
    screens under 500 px tall (phones held sideways) and in print; the footer gets matching bottom padding."""
    cell = lambda ic, label, href, extra='': (f'<a class="mb-a" href="{href}"{extra}>{ico(ic, 21, "#E3BE74", 1.8)}<span>{label}</span></a>')
    return ('<nav class="mbar" aria-label="Quick actions">'
            + cell('phone', 'Call', 'tel:' + MAIN_TEL, f' aria-label="Call {MAIN_PHONE}"')
            + cell('calendar-check', 'Schedule', 'Booking.dc.html', ' aria-label="Schedule your visit"')
            + cell('pin', 'Locations', 'Contact.dc.html#locations', ' aria-label="Our locations"') + '</nav>')

# ---------------------------------------------------------------- shared sections
def hero(photo, photo_w, min_h, h1, lead, buttons, eyebrow_txt=None, sub=None, h1_size=46, lead_size=18.6, lead_w=600, text_w=680, pad='36px 0 30px 83px', gap=14, sub_size=27.5, lead_lh=1.32, btn_mt=8, obj='right center', lead_weight=450, extra='', sq_mt=0,
         site_photo=None, photo_alt='', photo_wh=None, narrow_pos=None, narrow_ratio=None):
    """photo = a mock-up crop name; or site_photo = a real photograph under site-img/ (with photo_alt and photo_wh=(w, h))."""
    eb = eyebrow(eyebrow_txt, RUST, 'font-size: 12.5px; letter-spacing: 0.14em; margin-bottom: 2px') if eyebrow_txt else ''
    sb = (f'<p class="hsub" style="margin: 0; font-family: {SERIF}; font-weight: 620; font-size: {sub_size}px; line-height: 1.2; letter-spacing: -0.014em; color: {H1C}">{sub}</p>') if sub else ''
    sq = f'<span class="sq" style="display: block; margin-top: {sq_mt}px">{SQUIGGLE}</span>'
    sq_first = sq if not sub else ''
    sq_last = sq if sub else ''
    fade_l = 100 - photo_w
    return f'''
<section class="hero-sec" style="position: relative; min-height: {min_h}px">
{_hero_img(photo, photo_w, obj, site_photo, photo_alt, photo_wh, narrow_pos, narrow_ratio)}
<div class="hero-fade" aria-hidden="true" style="position: absolute; top: 0; bottom: 0; left: {fade_l}%; width: 7%; background: linear-gradient(90deg, #FBF3E8 0%, rgba(251, 243, 232, 0) 100%)"></div>
{branch(168, '#A5B195', 0.58, 'left: -84px; top: -12px; transform: rotate(8deg)')}
{branch(100, '#ADB89E', 0.5, 'left: -40px; bottom: -30px; transform: rotate(-12deg) scaleX(-1)')}
<div style="position: relative; z-index: 1; {WRAP}">
<div class="hero-txt" style="max-width: {text_w}px; padding: {pad}; display: flex; flex-direction: column; align-items: flex-start; gap: {gap}px">
{eb}<h1 class="h1" style="margin: 0; font-family: {SERIF}; font-weight: 680; font-size: {h1_size}px; line-height: 1.02; letter-spacing: -0.014em; color: {H1C}">{h1}</h1>
{sq_first}{sb}{sq_last}
<p class="lead" style="margin: 0; max-width: {lead_w}px; font-size: {lead_size}px; font-weight: {lead_weight}; line-height: {lead_lh}; color: {INK}">{lead}</p>{extra}
<div class="btn-row" style="display: flex; flex-wrap: wrap; gap: 14px 23px; margin-top: {btn_mt}px">{buttons}</div>
</div>
</div>
{hero_horizon()}
</section>'''

def hero_pic(img_html, ratio=None):
    """The hero photograph's box. Takes no part in the desktop layout (display: contents, the image is placed by its
    own inline style); on phones and tablets it becomes the box with the arched corner and the gold arc line."""
    st = f' style="--nr: {ratio}"' if ratio else ''       # tablets: the box's shape when it sits beside the text (default 5 / 4)
    return f'<div class="hero-pic"{st}>{img_html}</div>'

def hero_call(phones_only=True):
    """The hero's quiet second action: the main line as a text link (phones_only: shown under 600 px only; else on every screen)."""
    return (f'<a class="tl{" show-p" if phones_only else ""} hero-call" href="tel:{MAIN_TEL}" style="display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 44px; '
            f'font-size: 15px; font-weight: 700; color: {RUST}; text-decoration: none">{ico("phone", 18, RUST, 1.8)}'
            f'<span style="text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1.5px">Call {MAIN_PHONE}</span></a>')

def _hero_img(crop, photo_w, obj, site_photo, alt, wh, narrow_pos=None, narrow_ratio=None):
    """narrow_pos: object-position once the photo stacks above the text (tablets and phones), when the default 60% 30% crops it badly."""
    st = f'position: absolute; top: 0; right: 0; width: {photo_w}%; height: 100%; object-fit: cover; object-position: {obj}'
    cls = 'hero-photo'
    if narrow_pos:
        st += f'; --np: {narrow_pos}'; cls += ' hp-np'
    if site_photo:
        w, h = wh or (None, None)
        return hero_pic(photo(site_photo, alt, st, cls, w, h, lazy=False), narrow_ratio)
    return hero_pic(f'<img class="{cls}" src="{BLOB[crop]}" alt="" style="display: block; {st}">', narrow_ratio)

def rust_band(icon, title, sub, right, style='', sub_size=13.1, right_style='', right_cls=''):
    return f'''
<section style="{WRAP}; padding: 0 52px">
<div class="band" style="position: relative; overflow: hidden; border-radius: 16px; background: #A85C43; border: 1px solid #8A4530; color: #FFFFFF; padding: 16px 132px 17px 90px; min-height: 84px; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 22px; box-shadow: 0 1px 2px rgba(90, 40, 20, 0.18); {style}">
{branch(86, '#E4B58E', 0.5, 'left: -6px; bottom: -58px; transform: rotate(-18deg)', 4, True)}
{branch(96, '#E4B58E', 0.5, 'right: 6px; bottom: -66px; transform: rotate(14deg)', 4, True)}
{ico(icon, 36, '#FFFFFF', 1.3, 'position: relative')}
<div style="position: relative; flex: 1 1 380px; display: flex; flex-direction: column; gap: 4px">
<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 24.8px; line-height: 1.05; letter-spacing: -0.012em; color: #FFFFFF">{title}</h2>
<p style="margin: 0; font-size: {sub_size}px; line-height: 1.3; color: #FFF6EC">{sub}</p>
</div>
<div class="band-r{" " + right_cls if right_cls else ""}" style="position: relative; min-width: 0; max-width: 100%; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px{"; " + right_style if right_style else ""}">{right}</div>
</div>
</section>'''

NL_SUB = 'Get our news, events and programs by email.'
NEWSLETTER_FORM = facts.NEWSLETTER_FORM
def newsletter(sub=NL_SUB):
    """Newsletter band, as designed: an email box and a Subscribe button. It is a plain HTML form that posts straight to
    IIPCT's Mailchimp audience (facts.NEWSLETTER_FORM, Mailchimp's own embedded-form address) and opens Mailchimp's
    answer in a new tab: no script, and this site stores nothing. The hidden b_... field is Mailchimp's anti-robot field,
    written as their embed code writes it. Styles for narrow screens: .nl-* in RESP_CSS."""
    f = NEWSLETTER_FORM
    action = f'https://{f["host"]}/subscribe/post?u={f["u"]}&amp;id={f["id"]}&amp;f_id={f["f_id"]}'
    right = (f'<form class="nl-form" action="{action}" method="post" target="_blank" rel="noopener" '
             f'style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 12px; width: 100%">'
             f'<label for="nl-email" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap">Email address</label>'
             f'<input class="nl-in" id="nl-email" type="email" name="EMAIL" required autocomplete="email" placeholder="Enter your email address" aria-describedby="nl-note" '
             f'style="flex: 1 1 240px; min-width: 0; width: 346px; max-width: 100%; height: 40px; padding: 0 16px; border-radius: 9px; border: 1px solid #F3E4D2; background: #FFFDF8; '
             f'font-family: inherit; font-size: 13.4px; color: {INK}">'
             f'<div aria-hidden="true" style="position: absolute; left: -5000px"><input type="text" name="b_{f["u"]}_{f["id"]}" tabindex="-1" value=""></div>'
             f'<button class="btn bp nl-btn" type="submit" style="flex: none; display: inline-flex; align-items: center; justify-content: center; gap: 12px; min-height: 40px; min-width: 156px; '
             f'padding: 0 22px; border-radius: 9px; border: 1px solid #C8A15A; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; font-family: inherit; '
             f'font-size: 13.6px; font-weight: 600; line-height: 1.2; cursor: pointer; box-shadow: 0 2px 6px rgba(40, 20, 10, 0.3)"><span>Subscribe</span>{ico("arrow", 15, "currentColor", 2)}</button>'
             f'<p id="nl-note" style="flex: 1 1 100%; margin: 0; font-size: 12.6px; line-height: 1.4; color: #FFF6EC">Your email address goes to Mailchimp, the service IIPCT uses for its newsletter. '
             f'You can unsubscribe at any time. <a class="dl dg" href="Privacy.dc.html" style="color: #FFFFFF; font-weight: 600; text-decoration: underline; text-underline-offset: 3px">Privacy Policy</a>. '
             f'Subscribe opens Mailchimp in a new tab.</p>'
             f'</form>')
    return rust_band('mail', 'Stay Connected with IIPCT', sub, right, right_style='flex: 0 1 520px', right_cls='nl-r')

def feature_list(items, icon_size=46, title_size=15.6, gap=22, text_size=12.5, icon_gap=33):
    """items: (icon, title, text)"""
    out = ''
    for ic, t, d in items:
        out += (f'<div class="fl-i" style="display: flex; align-items: flex-start; gap: {icon_gap}px">{ico(ic, icon_size, RUSTI, 1.2, "margin-top: 1px")}'
                f'<div style="display: flex; flex-direction: column; gap: 4px"><h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: {title_size}px; line-height: 1.12; letter-spacing: -0.01em; color: {HEAD}">{t}</h3>'
                f'<p style="margin: 0; font-size: {text_size}px; line-height: 1.32; color: {INK}">{d}</p></div></div>')
    return f'<div class="fl-list" style="display: flex; flex-direction: column; gap: {gap}px">{out}</div>'

def split_section(photo_html, eyebrow_txt, title, body_html, cta, features, style='', title_size=30.5, photo_w='29.4%', feat_w='32.2%'):
    return f'''
<section style="position: relative; {WRAP}; {style}">
{branch(104, '#B5BFA6', 0.5, 'right: -58px; bottom: -22px; transform: rotate(-14deg)')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: stretch">
<div class="sp-photo" style="flex: 0 0 {photo_w}; min-width: min(300px, 100%); display: flex">{photo_html}</div>
<div class="sp-txt" style="flex: 1 1 380px; min-width: 0; padding: 14px 24px 20px 30px; display: flex; flex-direction: column; align-items: flex-start; gap: 11px">
{eyebrow(eyebrow_txt)}
{h2(title, title_size)}
{body_html}
<div style="margin-top: 6px">{cta}</div>
</div>
{vdiv('120px', GOLDL, 'margin: 20px 0 28px')}
<div class="sp-feat" style="flex: 0 0 {feat_w}; min-width: min(300px, 100%); padding: 12px 12px 20px 42px">{features}</div>
</div>
</section>'''

def green_band(photo, eyebrow_txt, title, text_html, right_html, style='', photo_w='40.6%', min_h=186, title_size=27.5, text_pad='16px 26px 17px 54px'):
    return f'''
<section style="{WRAP}; padding: 0 61px 0 63px; {style}">
<div style="position: relative; overflow: hidden; border-radius: 16px; min-height: {min_h}px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-wrap: wrap; align-items: stretch; box-shadow: 0 1px 2px rgba(20, 40, 25, 0.20)">
{branch(118, '#2C5A40', 0.9, 'right: 4px; bottom: -92px; transform: rotate(24deg)')}
<div class="gb-photo" style="flex: 0 0 {photo_w}; min-width: min(280px, 100%); position: relative; min-height: 150px">{img(photo, '', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover')}</div>
<div class="gb-txt" style="position: relative; flex: 1 1 360px; min-width: 0; padding: {text_pad}; display: flex; flex-direction: column; justify-content: center; gap: 8px">
{eyebrow(eyebrow_txt, '#E3BE74') if eyebrow_txt else ''}
{h2(title, title_size, '#FFFFFF', 'font-weight: 500')}
{text_html}
</div>
{right_html}
</div>
</section>'''

def sec_head(eyebrow_txt, title, right='', size=30.4, style=''):
    return (f'<div style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 12px 30px; {style}">'
            f'<div style="display: flex; flex-direction: column; gap: 5px">{eyebrow(eyebrow_txt)}{h2(title, size)}</div>{right}</div>')

# ---------------------------------------------------------------- sub-page helpers
FACEBOOK_URL = facts.FACEBOOK_URL
TIKTOK_URL = facts.TIKTOK_URL
BOOKING = 'Booking.dc.html'
# (name, street + town, phone as people should dial it, tel) for each location, in menu-option order. Kept for callers of
# the old 4-tuple list; new code reads facts.LOCATIONS. The numbers that used to sit here were fax numbers.
CLINICS = [(l['name'], address(l, False), f'{MAIN_PHONE}, press {l["option"]}', MAIN_TEL) for l in LOCATIONS]

def call_list(dark=False, size=13.4):
    """The main line's menu: one row per location ("Tyendinaga Clinic ... press 1"). Each row dials the main line."""
    name_c, opt_c, line = ('#FFFFFF', '#E3BE74', 'rgba(255, 255, 255, 0.22)') if dark else (HEAD, RUST, '#E6D9BF')
    rows = ''.join(f'<li style="border-top: 1px solid {line}"><a class="cl{" cld" if dark else ""}" href="tel:{MAIN_TEL}" aria-label="Call {MAIN_PHONE} and press {l["option"]} for the {l["name"]}" '
                   f'style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 36px; padding: 6px 0; text-decoration: none">'
                   f'<span style="font-weight: 600; color: {name_c}">{l["name"]}</span>'
                   f'<span style="flex: none; font-weight: 700; color: {opt_c}; white-space: nowrap">Press {l["option"]}</span></a></li>' for l in LOCATIONS)
    return f'<ul class="t-b" style="margin: 0; padding: 0; list-style: none; font-size: {size}px; line-height: 1.3">{rows}</ul>'

def social_row(dark=False, label='Follow us'):
    if dark:
        st = 'color: #F4EFE4; border: 1px solid rgba(200, 161, 90, 0.75); background: rgba(255, 255, 255, 0.04)'
        lc, cls, ic = '#C9D2C6', 'btn bg', '#E3BE74'
    else:
        st = f'color: {HEAD}; border: 1px solid #C9B691; background: #FFFDF8'
        lc, cls, ic = MUTED, 'btn bo', RUST
    pill = lambda t, h: (f'<a class="{cls}" href="{h}" style="display: inline-flex; align-items: center; gap: 7px; min-height: 30px; padding: 0 12px; border-radius: 999px; '
                         f'font-size: 12.4px; font-weight: 600; line-height: 1; text-decoration: none; {st}"><span>{t}</span>{ico("external", 12, ic, 2)}</a>')
    return (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px"><span style="font-size: 11.6px; font-weight: 600; letter-spacing: 0.04em; color: {lc}">{label}</span>'
            f'{pill("Facebook", FACEBOOK_URL)}{pill("TikTok", TIKTOK_URL)}</div>')

def crumbs(trail):
    parts = []
    for label, href in trail:
        if href:
            parts.append(f'<a class="tl" href="{href}" style="color: {RUST}; font-weight: 600; text-decoration: none">{label}</a>')
        else:
            parts.append(f'<span aria-current="page" style="color: {MUTED}">{label}</span>')
    sep = '<span aria-hidden="true" style="color: #A8998A">/</span>'
    return f'<nav aria-label="Breadcrumb" class="crumb" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: 12.6px; font-weight: 500">{sep.join(parts)}</nav>'

def sub_hero(trail, title, lead, photo=None, alt='', eyebrow_txt=None, buttons='', title_size=46, extra='', pos='center center', medal=None, lead_w=640):
    pic = ''
    if photo:
        pic = (f'<div class="sh-photo" style="flex: 0 0 440px; max-width: 100%">'
               + img(photo, alt, f'width: 100%; aspect-ratio: 440 / 232; object-fit: cover; object-position: {pos}; border-radius: 16px; border: 1px solid {LINE}') + '</div>')
    elif medal:
        pic = f'<div aria-hidden="true" style="flex: 0 0 200px; display: flex; justify-content: center">{circ(medal[0], medal[1], 124, 60, 1.25)}</div>'
    eb = eyebrow(eyebrow_txt, RUST, 'margin-top: 6px') if eyebrow_txt else ''
    bt = f'<div class="btn-row" style="display: flex; flex-wrap: wrap; gap: 12px 16px; margin-top: 8px">{buttons}</div>' if buttons else ''
    return f"""
<section class="sh" style="position: relative; overflow: hidden; border-bottom: 1px solid #E6D9BF">
{branch(150, '#A5B195', 0.5, 'left: -86px; top: -34px; transform: rotate(8deg)')}
<div class="sh-row" style="position: relative; {WRAP}; padding: 26px 48px 32px 83px; display: flex; flex-wrap: wrap; align-items: center; gap: 26px 64px">
<div class="sh-txt" style="flex: 1 1 520px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 11px">
{crumbs(trail)}
{eb}<h1 class="h1" style="margin: 4px 0 0; font-family: {SERIF}; font-weight: 680; font-size: {title_size}px; line-height: 1.04; letter-spacing: -0.014em; color: {H1C}">{title}</h1>
{SQUIGGLE}
<p class="lead" style="margin: 0; max-width: {lead_w}px; font-size: 17px; line-height: 1.42; color: {INK}">{lead}</p>
{extra}{bt}
</div>
{pic}
</div>
{hero_horizon()}
</section>"""

def h3(text, size=21, style='', cls='t-h3'):
    return f'<h3 class="{cls}" style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: {size}px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}; {style}">{text}</h3>'

def panel(inner, style='', pad='22px 24px'):
    return f'<div style="padding: {pad}; border-radius: 14px; {CARD}; {style}">{inner}</div>'

def bullets(items, icon='check', color='#1F4A2B', size=14.4, gap=9):
    rows = ''.join(f'<li style="display: flex; align-items: flex-start; gap: 12px">{ico(icon, 19, color, 2.1, "margin-top: 1px")}<span>{t}</span></li>' for t in items)
    return f'<ul class="t-b" style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: {gap}px; font-size: {size}px; line-height: 1.42; color: {INK}">{rows}</ul>'

def section(title, body, eyebrow_txt=None, size=27):
    eb = eyebrow(eyebrow_txt) if eyebrow_txt else ''
    return f'<section style="display: flex; flex-direction: column; gap: 12px">{eb}{h2(title, size)}{body}</section>'

def photo_ph(label, ratio='16 / 9', style=''):
    return (f'<div role="img" aria-label="{label}" style="aspect-ratio: {ratio}; border-radius: 14px; border: 1px dashed #B9AA86; background: #EFE9D6; display: flex; flex-direction: column; '
            f'align-items: center; justify-content: center; gap: 10px; padding: 18px; text-align: center; color: {MUTED}; font-size: 12.6px; line-height: 1.35; {style}">'
            f'{ico("camera", 30, "#7E8F6C", 1.5)}<span>{label}</span></div>')

def book_aside(related='', title='Book this service'):
    return f"""<aside class="aside" style="flex: 0 0 372px; max-width: 100%; display: flex; flex-direction: column; gap: 18px">
<div style="padding: 22px 22px 22px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-direction: column; align-items: flex-start; gap: 10px; box-shadow: {SHADOW}">
{eyebrow('Book a visit', '#E3BE74')}
<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 25px; line-height: 1.1; letter-spacing: -0.012em; color: #FFFFFF">{title}</h2>
<p class="t-b" style="margin: 0; font-size: 13.6px; line-height: 1.45; color: #F4F1E8">Registered patients can book online. New to IIPCT, or not sure what you need? Call us and reception will help.</p>
{btn('Schedule Your Visit', BOOKING, 'light', 'calendar-check', True, 'md', 'margin-top: 6px; width: 100%')}
<a class="fl" href="tel:{MAIN_TEL}" style="display: flex; align-items: center; gap: 10px; margin-top: 4px; font-size: 15px; font-weight: 700; color: #FFFFFF; text-decoration: none">{ico('phone', 18, '#E3BE74', 1.8)}<span>{MAIN_PHONE}</span></a>
</div>
<div style="padding: 18px 22px 12px; border-radius: 14px; {CARD}">
{h3('Call your clinic', 19)}
<p class="t-b" style="margin: 6px 0 10px; font-size: 13.4px; line-height: 1.4; color: {INK}">Call {MAIN_PHONE}, then press the number for your location.</p>
{call_list()}
</div>
{related}
</aside>"""

def link_list(title, links):
    rows = ''.join(f'<li><a class="tl il" href="{h}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 9px 0; border-top: 1px solid #E6D9BF; '
                   f'font-size: 13.6px; font-weight: 600; color: {HEAD}; text-decoration: none"><span>{t}</span>{ico("arrow", 15, RUST, 1.9)}</a></li>' for t, h in links)
    return f'<div style="padding: 18px 22px 10px; border-radius: 14px; {CARD}">{h3(title, 19)}<ul class="t-b" style="margin: 10px 0 0; padding: 0; list-style: none">{rows}</ul></div>'

def two_col(main, aside, style=''):
    return (f'<div style="{WRAP}; padding: 34px 48px 8px 83px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 34px 56px; {style}">'
            f'<div style="flex: 1 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 30px">{main}</div>{aside}</div>')

def cta_band(title, sub, icon='calendar-check'):
    right = (btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check', True, 'md', 'border-color: #C8A15A')
             + btn('Contact a Clinic', 'Contact.dc.html', 'light', 'phone', False, 'md'))
    return rust_band(icon, title, sub, right, 'padding-right: 100px', 13.6)

def note(icon, title, text, tone='sage', style=''):
    bg, bd = {'sage': ('#EBE7D2', '#D3CEAE'), 'cream': ('#FFFDF8', LINE), 'gold': ('#F6EACD', '#DCC28C')}[tone]
    ttl = f'<h3 style="margin: 0; font-size: 15px; font-weight: 700; line-height: 1.25; color: {HEAD}">{title}</h3>' if title else ''
    return (f'<div style="display: flex; align-items: flex-start; gap: 16px; padding: 16px 20px 17px; border-radius: 14px; background: {bg}; border: 1px solid {bd}; {style}">'
            f'{ico(icon, 25, "#1F4A2B", 1.6, "margin-top: 1px")}<div style="min-width: 0; display: flex; flex-direction: column; gap: 4px">{ttl}'
            f'<p class="t-b" style="margin: 0; font-size: 14px; line-height: 1.46; color: {INK}">{text}</p></div></div>')

def ext(label, href, size=14, color=RUST, style=''):
    """Inline link to another website, marked with the external-link icon."""
    return (f'<a class="tl" href="{href}" style="font-size: {size}px; font-weight: 600; color: {color}; text-decoration: none; {style}">'
            f'<span style="text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1.5px">{label}</span>'
            f'{ico("external", round(size), color, 1.9, "display: inline; vertical-align: -2px; margin-left: 6px")}</a>')

def icon_item(icon, tone, title, text, more=''):
    """Icon medallion + title + text, as a bordered card."""
    return (f'<div style="display: flex; align-items: flex-start; gap: 16px; padding: 18px 20px 18px 18px; border-radius: 14px; {CARD}">'
            f'{circ(icon, tone, 52, 27, 1.5)}<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 5px; padding-top: 2px">'
            f'{h3(title, 18.4)}<p class="t-b" style="margin: 0; font-size: 13.8px; line-height: 1.46; color: {INK}">{text}</p>{more}</div></div>')

def link_card(icon, tone, title, text, href):
    """Whole card is the link to a child page."""
    return (f'<a class="card tile tila" href="{href}" style="position: relative; display: flex; align-items: flex-start; gap: 15px; min-height: 112px; padding: 18px 46px 18px 18px; border-radius: 14px; '
            f'{CARD}; color: {INK}; text-decoration: none">{circ(icon, tone, 56, 29, 1.5)}'
            f'<span class="tile-b" style="min-width: 0; display: flex; flex-direction: column; gap: 5px; padding-top: 2px">'
            f'<span class="t-h3 ct" style="font-family: {SERIF}; font-weight: 700; font-size: 18.4px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}">{title}</span>'
            f'<span class="t-s" style="font-size: 13.4px; line-height: 1.44; color: {INK}">{text}</span></span>'
            f'<span class="tile-ar" aria-hidden="true" style="position: absolute; right: 14px; bottom: 13px; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; '
            f'background: #FFFDF8; border: 1px solid #C9B691">{ico("arrow", 13, "#13261B", 2)}</span></a>')

def grid(items, minw=300, gap=16, style='', cls=''):
    """cls: the card kind for phones and tablets: 'g-tiles gt3' (small tiles: two-up on phones, three-up on tablets),
    'g-cards gt2' (content cards: one-up on phones, two-up on tablets). See the grid rules in RESP_CSS."""
    c = f' class="{cls}"' if cls else ''
    return f'<div{c} style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min({minw}px, 100%), 1fr)); gap: {gap}px; {style}">{"".join(items)}</div>'

def chips(items, style=''):
    out = ''.join(f'<li style="padding: 6px 13px 5px; border-radius: 999px; background: #FFFDF8; border: 1px solid #C9B691; font-size: 13px; font-weight: 600; line-height: 1.2; color: {HEAD}; white-space: nowrap">{t}</li>' for t in items)
    return f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: 8px; {style}">{out}</ul>'

def tag(text, tone='tan'):
    bg, bd = {'tan': ('#F0DDB5', '#D6BC86'), 'sage': ('#D9DCC4', '#B9BF9C'), 'rust': ('#F1D5C8', '#D9A892'), 'cream': ('#FFFDF8', '#C9B691')}[tone]
    return (f'<span style="display: inline-block; padding: 5px 10px 4px; border-radius: 6px; background: {bg}; border: 1px solid {bd}; font-size: 10.6px; font-weight: 700; '
            f'letter-spacing: 0.06em; text-transform: uppercase; line-height: 1.1; color: #2A2A1C; white-space: nowrap">{text}</span>')

def prose(*paras, size=14.8, style=''):
    return ''.join(f'<p class="t-b" style="margin: 0; max-width: 700px; font-size: {size}px; line-height: 1.55; color: {INK}; {style}">{t}</p>' for t in paras)

def draft_bar(text):
    """Thin strip under the header marking a page whose wording still needs the client's sign-off."""
    return (f'<div style="background: #F6EACD; border-bottom: 1px solid #DCC28C"><div style="{WRAP}; padding: 9px 48px 9px 83px; display: flex; align-items: center; gap: 11px; '
            f'font-size: 13px; line-height: 1.35; color: #3B2E12">{ico("info", 17, "#7A5A14", 1.9)}<span class="t-s">{text}</span></div></div>')

# ---------------------------------------------------------------- document shell
# Narrow-width rules. They key off the page's own width (a container query), so a page behaves the same in a
# phone-width frame on the canvas as it does in a real phone-width window.
RESP_CSS = """.pg{container-type:inline-size;container-name:pg;min-width:320px}
.pg{padding-left:env(safe-area-inset-left,0px);padding-right:env(safe-area-inset-right,0px)}
.hero-pic{display:contents}
.hero-hz,.hz-p,.hz-t,.mbar{display:none}
.show-p{display:none !important}
@keyframes hz-rise{from{transform:translateY(9px)}to{transform:none}}
.hd-m{display:none;margin-left:auto;align-items:center;gap:10px}
.mnav>summary{list-style:none}.mnav>summary::-webkit-details-marker{display:none}
.mnav[open] .mi-o,.mnav:not([open]) .mi-x{display:none !important}
.xt>summary,.faq>summary{list-style:none}.xt>summary::-webkit-details-marker,.faq>summary::-webkit-details-marker{display:none}
.xt[open]>summary>svg,.faq[open]>summary>svg{transform:rotate(180deg)}
@container pg (max-width:1399px){
.hd{padding-left:32px !important;padding-right:28px !important}
.hd-nav{gap:4px 14px !important}
.pg h3,.pg li,.pg li>span{white-space:normal !important}
.hero-txt{padding-left:56px !important}
.hero-txt .h1{font-size:42px !important}
.hero-txt .lead{font-size:16.6px !important}
.g3l{grid-template-columns:repeat(3,minmax(0,1fr)) !important}
}
@container pg (max-width:1199px){
.hd-nav,.hd-cta,.hd-div{display:none !important}
.hd-m{display:flex}
.hd{min-height:0 !important;padding-top:9px !important;padding-bottom:9px !important;flex-wrap:nowrap !important}
.hd-logo{width:68px !important}
.msheet{padding:6px 16px 18px !important;max-height:calc(100vh - 150px);max-height:calc(100dvh - 140px);overflow-y:auto;overscroll-behavior:contain}
.ml-g+.ml-g{border-top:1px solid #EFE3CC}
.ml-g{padding:2px 0}
.ml-sub{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(160px,100%),1fr));gap:0 6px;padding:0 0 8px}
.mnav .cur{background:#F6EEDD;color:#8C2B18 !important;box-shadow:inset 3px 0 0 #A0432C}
.mfoot{margin-top:8px !important}
}
@container pg (max-width:1199px){
.fl{display:inline-flex !important;align-items:center;min-height:40px !important}
.ft-col{gap:2px !important}
.tl,.cl,a[href^="tel:"],a[href^="mailto:"]{min-height:40px !important}
nav[aria-label="Breadcrumb"] a{min-width:40px}
.tl:not([style*="display"]):not(p .tl):not(li .tl),a[href^="tel:"]:not([style*="display"]):not(p a):not(li a),a[href^="mailto:"]:not([style*="display"]):not(p a):not(li a){display:inline-flex;align-items:center}
.btn{min-height:40px !important}
.nl-in,.nl-btn{min-height:44px !important}
.nl-in{font-size:16px !important}
.ra{width:40px !important;height:40px !important}
.toc a{display:flex !important;align-items:center;min-height:40px}
}
@container pg (max-width:940px){
.fsu{font-size:12px !important}
}
@container pg (max-width:1099px){
.w{padding-left:32px !important;padding-right:32px !important}
.hero-sec{min-height:0 !important}
.hero-fade{display:none}
.hero-pic{display:block;position:relative}
.hero-pic::before,.sh-photo::before{content:"";position:absolute;inset:0;border-top-right-radius:58% 46%;background-image:linear-gradient(180deg,rgba(251,244,234,0) 42%,#FBF4EA 74%),linear-gradient(90deg,#FBF4EA 30%,#CBA35A 62%)}
.hero-photo{position:absolute !important;left:0 !important;top:5px !important;width:calc(100% - 6px) !important;height:calc(100% - 5px) !important;border-top-right-radius:58% 46%;object-position:60% 30% !important}
.hero-photo.hp-np{object-position:var(--np) !important}
.hero-txt{max-width:none !important}
.hero-hz{display:block;line-height:0}

.hz-sun{animation:hz-rise 1.6s cubic-bezier(.2,.7,.2,1) .25s both}
.sh-photo{position:relative}
.sh-photo img{position:relative;z-index:1;margin-top:5px;width:calc(100% - 6px) !important;border:none !important;border-radius:0 !important;border-top-right-radius:58% 46% !important}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #10291F;outline-offset:2px;box-shadow:0 0 0 5px #F2D49A}
.pg h1,.pg h2,.pg h3,.pg h4,.hsub{text-wrap:balance}
.t-b{font-size:16px !important;line-height:1.55 !important}
.t-s{font-size:14.5px !important;line-height:1.45 !important}
.crumb{font-size:14px !important}
.nb{white-space:nowrap}
a[href^="mailto:"]{overflow-wrap:anywhere}
.mbar{display:flex !important;position:fixed;left:0;right:0;bottom:0;z-index:60;background:#153526;border-top:1px solid #C8A15A;padding:0 env(safe-area-inset-right,0px) env(safe-area-inset-bottom,0px) env(safe-area-inset-left,0px);box-shadow:0 -4px 16px rgba(12,39,29,.22)}
.mb-a{flex:1 1 0;min-width:0;display:flex !important;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-height:56px !important;color:#FFFFFF;text-decoration:none;font-size:13px;font-weight:700;line-height:1.1;letter-spacing:.01em}
.mb-a+.mb-a{border-left:1px solid rgba(200,161,90,.32)}
.ft-dark{padding-bottom:calc(56px + env(safe-area-inset-bottom,0px))}
.hd-book{display:none !important}
.sp-photo,.sp-feat{flex:1 1 100% !important}
.sp-txt{padding:22px 0 20px !important}
.sp-feat{padding:4px 0 16px !important}
.gb-cta{flex:1 1 100% !important;justify-content:flex-end !important;padding:0 28px 22px !important}
.dcb,.dcp{display:none !important}
.ft-pipe{display:none !important}
.ft-bar{margin-left:0 !important}
.pg br{display:none}.pg br.k{display:inline}
.vd{display:none !important}
.band{padding:20px 28px !important}
.nl-r{flex:1 1 100% !important}
.aside{flex:1 1 100% !important;max-width:none !important;display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start}
.aside>*{max-width:none !important}
.ft-row{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 24px !important}
.ft-col{width:auto !important;min-height:0 !important;border-left:none !important;padding-left:0 !important;padding-right:0 !important}
.ft-logo{width:auto !important}
.ft-logo,.ft-art{grid-column:1 / -1}
.ft-art{justify-content:flex-start !important}
.fb{flex:1 1 100% !important;max-width:100% !important;width:auto !important}
.st{flex-direction:column !important;align-items:stretch !important}
.nw{white-space:normal !important}
.p0{padding-left:0 !important;padding-right:0 !important}
.m0{margin-left:0 !important;margin-right:0 !important}
.cx{justify-content:flex-start !important}
.hide-t{display:none !important}
.g2t{grid-template-columns:repeat(2,minmax(0,1fr)) !important}
}
@container pg (max-width:900px){
.mapc,.locm{display:flex !important;flex-direction:column;min-height:0 !important}
.map-bg,.map-curve{display:none !important}
.map-txt{order:1;width:auto !important;min-width:0 !important;padding:26px 28px 20px !important}
.map-img{order:2;position:static !important;width:100% !important;height:230px !important;-webkit-mask-image:none !important;mask-image:none !important}
.map-list{order:3;position:static !important;width:auto !important;min-width:0 !important;margin:14px !important}
.map-list ul{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 14px !important}
.locm-txt{order:1;width:auto !important;min-width:0 !important}
.locm-img{order:2;position:static !important;width:100% !important;height:210px !important;-webkit-mask-image:none !important;mask-image:none !important}
}
@container pg (max-width:760px){
.w{padding-left:20px !important;padding-right:20px !important}
.h1{font-size:36px !important;line-height:1.06 !important}
.h2{font-size:26px !important}
.lead{font-size:16.5px !important;line-height:1.4 !important}
.sh-photo{flex:1 1 100% !important}
.band{padding:20px 20px 22px !important}
.band-r{flex:1 1 100%}
.gb-photo{flex:1 1 100% !important;min-height:190px !important}
.gb-txt{padding:20px 20px 16px !important}
.gb-cta{justify-content:flex-start !important;padding:0 20px 22px !important}
.aside{grid-template-columns:minmax(0,1fr)}
.ft-row{grid-template-columns:repeat(2,minmax(0,1fr))}
.ft-contact{grid-column:1 / -1}
.dcp{display:none !important}
.pads{padding:18px 18px 20px !important}
.pads2{padding:14px 8px 8px !important}
.mh-s{min-height:190px !important}
.gap-s{gap:14px !important}
.fbs{flex:1 1 100% !important;max-width:100% !important;width:auto !important}
.sts{flex-direction:column !important;align-items:stretch !important}
.hide-s{display:none !important}
.g1{grid-template-columns:minmax(0,1fr) !important}
}
@container pg (max-width:480px){
.w{padding-left:16px !important;padding-right:16px !important}
.h1{font-size:32px !important}
.h2{font-size:24px !important}
.hd-tag,.xs-hide{display:none !important}
.hd-logo{width:56px !important}
.hd{gap:8px !important}
.btn-row>.btn{flex:1 1 100%}
.g2x{grid-template-columns:repeat(2,minmax(0,1fr)) !important}
.g3x{grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:10px !important}
}
@container pg (1099px < width <= 1399px){
.lcg{grid-template-columns:repeat(6,minmax(0,1fr)) !important}
.lcg>*{grid-column:span 2}
.lcg>:nth-child(3n+1):nth-last-child(2){grid-column:2 / span 2}
.lcg>:nth-child(3n+1):last-child{grid-column:3 / span 2}
}
@container pg (760px < width <= 1099px){
.lcg{grid-template-columns:repeat(4,minmax(0,1fr)) !important}
.lcg>*{grid-column:span 2}
.lcg>:nth-child(odd):last-child{grid-column:2 / span 2}
}
@container pg (width <= 760px){
.lcg{grid-template-columns:minmax(0,1fr) !important}
}
@container pg (min-width:600px) and (max-width:1099px){
.hero-txt .h1{font-size:clamp(34px,4.4vw,44px) !important;line-height:1.05 !important}
.hero-txt .lead{font-size:17px !important;line-height:1.45 !important}
.hz-t{display:block}
.h2{font-size:30px !important}
#main :is(p,dd,figcaption,li.t-b,li.t-s,ul.t-b>li,ol.t-b>li,ul.t-s>li){max-width:32em !important}
#main>*{margin-top:48px !important}
#main>:first-child,#main>.hero-sec,#main>.sh{margin-top:0 !important}
#main>.hero-sec+*,#main>.sh+*{margin-top:28px !important}
#main>.w{padding-top:0 !important}
.fl-list{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px !important}
.fl-i{flex-direction:column;gap:10px !important}
.ft-col .fl{font-size:14.5px !important}
.ev-tm{flex-basis:152px !important}
.gt2{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:16px !important}
.gt2>:last-child:nth-child(odd){grid-column:1 / -1}
.gt3{display:grid !important;grid-template-columns:repeat(6,minmax(0,1fr)) !important;gap:16px !important}
.gt3>*{grid-column:span 2}
.gt3>:nth-child(3n+1):nth-last-child(2){grid-column:2 / span 2}
.gt3>:nth-child(3n+1):last-child{grid-column:3 / span 2}
}
@container pg (min-width:760px) and (max-width:1099px){
.hero-sec{display:grid !important;grid-template-columns:minmax(0,1.08fr) minmax(0,1fr)}
.hero-sec>.w{grid-column:1;grid-row:1;align-self:center;padding-right:28px !important}
.hero-pic{grid-column:2;grid-row:1;align-self:center;margin:24px 32px 8px 0;aspect-ratio:var(--nr,5 / 4)}
.hero-hz{grid-column:1 / -1;grid-row:2;margin-top:8px}
.hero-txt{padding:24px 0 20px !important}
.sh-row{flex-wrap:nowrap !important;align-items:center !important;gap:32px !important}
.sh-txt{flex:1 1 0 !important}
.sh-photo{flex:0 0 42% !important}
.sh-photo img{aspect-ratio:4 / 3 !important}
.sh .h1{font-size:40px !important}
.tila .tile-b{padding-right:50px !important}
.bt{flex-direction:column !important;align-items:flex-start !important;gap:10px !important}
.g-steps{grid-template-columns:repeat(3,minmax(0,1fr)) !important}
.g-steps>*{flex-direction:column;gap:12px !important}
.aside>:last-child:nth-child(odd){grid-column:1 / -1}
.aside>:last-child:nth-child(odd) ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:28px}
.sp-photo{flex:0 0 40% !important}
.sp-txt{flex:1 1 0 !important;padding:6px 0 10px 28px !important}
.sp-feat{flex:1 1 100% !important;padding:12px 0 0 !important}
.cu-col{flex:1 1 0 !important}
.cu-col+.cu-col{border-left:1px solid #E6D6BC}
.gt2w{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:16px !important}
}
@container pg (min-width:600px) and (max-width:759px){
.hero-sec{display:flex !important;flex-direction:column;padding-top:12px}
.hero-pic{margin-right:20px;aspect-ratio:16 / 9}
.hero-txt{padding:20px 0 8px !important;gap:11px !important}
.sh-row{padding-top:14px !important;padding-bottom:20px !important;gap:0 !important}
.sh-photo{order:-1;flex:1 1 100% !important;max-width:none !important;margin:0 0 18px -20px;width:calc(100% + 20px)}
.sh-photo img{aspect-ratio:21 / 9 !important}
.sh .h1{font-size:36px !important}
}
@container pg (max-width:759px){
.g-steps{grid-template-columns:minmax(0,1fr) !important}
}
@container pg (min-width:600px) and (max-width:899px){
.ft-row{grid-template-columns:repeat(2,minmax(0,1fr)) !important}
.ft-contact{grid-column:auto !important}
}
@container pg (min-width:900px) and (max-width:1099px){
.ft-row{grid-template-columns:repeat(4,minmax(0,1fr)) !important}
}
@container pg (max-width:759px){
.tile{flex-direction:column !important;align-items:flex-start !important;gap:10px !important;min-height:0 !important;padding:14px !important}
.tila{padding-bottom:50px !important}
.g-tiles>.tile:last-child:nth-child(odd){flex-direction:row !important;align-items:center !important;gap:14px !important}
.tile>.ci{width:46px !important;height:46px !important}
.tile>.ci svg{width:25px;height:25px}
.tile-b{padding:0 !important;gap:6px !important}
.tile .t-h3{font-size:17.5px !important;white-space:normal !important}
.tile>.ra,.tile>.tile-ar{right:12px !important;bottom:12px !important}
.tile>img{width:64px !important;height:64px !important}
.bt>span[aria-hidden]{width:64px !important;height:64px !important;font-size:22px !important}
}
@container pg (max-width:599px){
.w{padding-left:16px !important;padding-right:16px !important}
.hd{padding-top:7px !important;padding-bottom:7px !important}
.hd-logo{width:50px !important}
.hide-p{display:none !important}
.show-p{display:inline-flex !important}
.hero-sec{display:flex !important;flex-direction:column;padding-top:10px}
.hero-pic{margin-right:16px;aspect-ratio:16 / 10}
.hero-txt{padding:16px 0 4px !important;gap:9px !important}
.hero-txt .h1,.sh .h1{font-size:31px !important;line-height:1.08 !important}
.hero-txt .lead,.sh .lead{font-size:16.5px !important;line-height:1.45 !important}
.sqg{width:112px;height:12px}
.hz-p{display:block}
.hz-d{display:none !important}
.hero-sec .btn-row,.sh .btn-row{flex-direction:column !important;align-items:stretch !important;gap:2px !important;width:100%;margin-top:6px !important}
.hero-sec .btn-row>.btn:first-child,.sh .btn-row>.btn:first-child{min-height:48px !important;font-size:15.5px !important;border-radius:11px !important}
.hero-sec .btn-row>.btn~.btn,.sh .btn-row>.btn~.btn{background:none !important;border-color:transparent !important;box-shadow:none !important;color:#8C2B18 !important;min-height:44px !important;font-size:15px !important;transform:none !important}
.hero-sec .btn-row>.btn~.btn>span,.sh .btn-row>.btn~.btn>span{text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1.5px}
.sh-row{padding-top:12px !important;padding-bottom:18px !important;gap:0 !important}
.sh-photo{order:-1;flex:1 1 100% !important;max-width:none !important;margin:0 0 16px -16px;width:calc(100% + 16px)}
.sh-photo img{aspect-ratio:16 / 9 !important}
.sh-txt{gap:10px !important}
.t-h3{font-size:20px !important;line-height:1.2 !important}
.t-h3l{font-size:22px !important;line-height:1.15 !important}
.t-h3t{font-size:17.5px !important;line-height:1.2 !important}
.t-hs{font-size:15.5px !important;line-height:1.3 !important}
.h2{font-size:26px !important;line-height:1.1 !important}
.tl{font-size:15px !important}
.crumb .tl{font-size:14px !important}
.g-tiles{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:12px !important}
.g-tiles>:last-child:nth-child(odd){grid-column:1 / -1}
.g-cards{grid-template-columns:minmax(0,1fr) !important;gap:14px !important}
.mj{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr))}
.mj a{width:100%;justify-content:center}
.ev{display:grid !important;grid-template-columns:auto minmax(0,1fr);gap:12px 14px !important;padding:16px !important}
.ev-b{display:contents !important}
.ev-d{grid-column:1;grid-row:1 / span 2;align-self:start}
.ev-b>*{grid-column:1 / -1}
.ev-b>.ev-t{grid-column:2;grid-row:1;align-self:end}
.ev-b>.ev-h{grid-column:2;grid-row:2;align-self:start}
.ev-f{grid-column:1 / -1;flex:none !important;flex-direction:row !important;align-items:center !important;max-width:none !important;width:100%;gap:14px !important}
.ev-f>img{width:84px !important;flex:none}
.ft-row{grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:22px 16px !important;padding-bottom:16px !important}
.ft-contact{order:-1;grid-column:1 / -1}
.ft-ql{order:1}.ft-loc{order:2}
.ft-more{order:3;grid-column:1 / -1;display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:16px}
.ft-more>span:first-child{grid-column:1 / -1}
.ft-logo{order:4;grid-column:1 / -1;flex-direction:row !important;flex-wrap:wrap;align-items:center !important;justify-content:space-between;gap:14px 20px !important}
.ft-art{display:none !important}
.ft-legal{gap:2px 18px !important;padding-top:10px !important;font-size:14px !important}
.ft-col .fl{font-size:15px !important}
.ft-logo>a>span:first-child{width:64px !important;height:64px !important}
.ft-logo>a>span:first-child>img{width:52px !important}
#main>*{margin-top:40px !important}
#main>:first-child,#main>.hero-sec,#main>.sh{margin-top:0 !important}
#main>.hero-sec+*,#main>.sh+*{margin-top:24px !important}
#main>.w{padding-top:0 !important}
.sp-photo>div{min-height:210px !important}
.sp-txt{padding:20px 0 12px !important}
.hsub{font-size:21px !important;line-height:1.2 !important}
.ev-tm{flex:1 1 100% !important}
.loc-g .tl{white-space:nowrap;font-size:14px !important}
.loc-g>a>span{padding-left:0 !important}
.loc-g>a>span:first-child{gap:7px !important}
.cu-col .ci{width:52px !important;height:52px !important}
.cu-col .ci svg{width:26px;height:26px}
.jl{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px !important}
.jl>a{justify-content:center;text-align:center;padding:6px 10px !important;min-height:44px !important;font-size:14px !important;border-radius:14px !important}
.toc ul{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 8px !important}
.btn{font-size:15px !important;white-space:normal !important;line-height:1.25 !important;text-align:center;padding-top:9px !important;padding-bottom:9px !important}
.nl-in,.nl-btn{flex:1 1 100% !important;width:100% !important}
.g-tm{grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:12px !important}
.tm{padding:12px !important;gap:10px !important}
.tm-h{flex-direction:column;align-items:flex-start !important;gap:10px !important}
.tm-h>:first-child{width:76px !important;height:76px !important;border-radius:10px !important;font-size:25px !important}
.tm-n{font-size:17.5px !important;line-height:1.16 !important}
.tm-d{margin-top:auto}
.tm-d>summary{font-size:14.5px !important;line-height:1.3 !important;padding:10px 0 !important}
.g-tm>.tm:last-child:nth-child(odd),.g-tm>.tm:has(>details[open]){grid-column:1 / -1}
.g-tm>.tm:last-child:nth-child(odd)>.tm-h,.g-tm>.tm:has(>details[open])>.tm-h{flex-direction:row;align-items:center !important;gap:14px !important}
.lt{flex-direction:row !important}
.lt-band{flex:none;width:54px;height:auto !important}
.mfoot{position:sticky;bottom:-18px;margin:8px -16px 0 !important;padding:12px 16px 18px !important;background:#FFFDF8;box-shadow:0 -10px 14px -10px rgba(40,30,10,.25)}
}
@container pg (max-width:374px){
.hero-txt .h1,.sh .h1{font-size:29px !important}
.loc-g .tl svg{display:none}
.tl{white-space:normal !important}
.mb-a{font-size:12.5px}
}
@media (max-width:1119px){
html{scroll-padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))}
}
@media (max-height:499px){
html{scroll-padding-bottom:0}
.mbar{display:none !important}
.ft-dark{padding-bottom:0 !important}
.hd-book{display:inline-flex !important}
}
@media print{
.mbar{display:none !important}
}
@media (prefers-reduced-motion:reduce){
.hz-sun{animation:none !important}
}
"""

FONT_HREF = ('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700'
             '&amp;family=Kaushan+Script&amp;family=Newsreader:ital,opsz,wght@0,6..72,400..800;1,6..72,400..800&amp;display=swap')
# ---------------------------------------------------------------- hover and keyboard focus
# Every link, button and summary answers the pointer, and keyboard focus, with a colour change. Most colours sit
# inline on the elements, so these rules carry !important. One class per kind of control:
#   tl, tx  text link (rust): forest, gold underline (tu: the label sits in its own underlined span)
#   il      link in ink (event titles, card titles, rows): rust; ct marks the title inside a row or a card link
#   fl, dl  link on a dark band or the footer (cream, white): light gold; dg: gold at rest, or on the rust band where light
#           gold would be too faint: white with a gold underline
#   bp      primary button: a lighter forest with a gold edge
#   bo, bs  outline and soft buttons: forest fill, white words
#   bl, bg  light button and gold-edged button on a dark band: gold fill, dark words
#   card    a card that is a link: gold edge and a lift; its title (ct, t-h3) turns rust
#   nv nv-on mi ml mb-a ra cl cld lg lgd pl, .toc a: header menu (and its current item), dropdown items, the phone menu,
#   the bottom bar, round arrows, call-list rows, the logo, picture links, the legal pages' contents list
# lib.responsive() gives every hand-written link without a class its kind from its colour (_linkkind).
# Pointer rules sit behind @media (hover: hover), so touch screens never keep a stuck hover colour; keyboard focus
# (:focus-visible) gets the same colours on every screen, as well as its outline. Movement (the lift, the arrow
# nudge) only for visitors who have not asked for reduced motion. tools/hover-check.mjs checks every page.
_UL = 'text-decoration-line:underline !important;text-decoration-color:#C8A15A !important;text-underline-offset:4px;text-decoration-thickness:1.5px'
HOVER = [   # (selectors, with % where the state goes; declarations)
    ('.tl:not(.il)%,.tx%', 'color:#17402A !important'),
    ('.tl:not(.il):not(.tu)%,.tx:not(.tu)%', _UL),
    ('.tu%>span', 'text-decoration-color:#C8A15A !important'),
    ('.il%,.il% .ct', 'color:#8C2B18 !important'),
    ('.tl% svg,.tx% svg,.il% svg', 'stroke:currentColor'),
    ('.fl%,.dl%', 'color:#E3BE74 !important'),
    ('.dg%', 'color:#FFFFFF !important;' + _UL),
    ('.cl% span:first-child', 'color:#8C2B18 !important'),
    ('.cld% span:first-child', 'color:#E3BE74 !important'),
    ('.lg% .lgw', 'color:#8C2B18 !important'),
    ('.lgd% .lgw', 'color:#E3BE74 !important'),
    ('.pl% img', 'border-color:#C8A15A !important'),
    ('.bp%', 'background:linear-gradient(180deg,#31723F 0%,#1F4E2A 100%) !important;border-color:#C8A15A !important'),
    ('.bo%,.bs%', 'background:#17402A !important;color:#FFFFFF !important;border-color:#17402A !important'),
    ('.bl%', 'background:#E3BE74 !important;color:#10291F !important;border-color:#E3BE74 !important'),
    ('.bg%', 'background:#C8A15A !important;color:#10291F !important;border-color:#C8A15A !important'),
    ('.bo% svg,.bs% svg,.bl% svg,.bg% svg', 'stroke:currentColor'),
    ('.card%', 'border-color:#C8A15A !important;box-shadow:0 2px 4px rgba(64,44,14,.08),0 14px 26px rgba(64,44,14,.13) !important'),
    ('a.card% .ct,a.card% .t-h3', 'color:#8C2B18 !important'),
    ('.nv%', 'color:#9A3B26 !important;border-bottom-color:#9A3B26 !important'),
    ('.nv-on%', 'color:#17402A !important;border-bottom-color:#C8A15A !important'),
    ('.nv% svg', 'stroke:currentColor'),
    ('.mi%,.ml%,.toc a%', 'background:#F1E7D3;color:#8C2B18 !important'),
    ('.mnav .ml.cur%', 'background:#EFE0C2 !important;color:#17402A !important'),
    ('.mb-a%', 'background:#1C4632;color:#E3BE74'),
    ('.ra%', 'background:#17402A !important;border-color:#17402A !important'),
    ('.ra% svg', 'stroke:#FFFFFF'),
]
# phones: a hero's second button is drawn as a text link there (RESP_CSS), so it answers like one
HOVER_P = [('.hero-sec .btn-row>.btn~.btn%,.sh .btn-row>.btn~.btn%', 'color:#17402A !important'),
           ('.hero-sec .btn-row>.btn~.btn%>span,.sh .btn-row>.btn~.btn%>span', 'text-decoration-color:#C8A15A !important')]
def _rules(rules, state):
    return ''.join(','.join(sel.replace('%', state) for sel in sels.split(',')) + '{' + decl + '}' for sels, decl in rules)
HOVER_CSS = ('.tl,.tx,.il,.fl,.dl,.cl span,.lgw,.pl img,.btn,.bo,.bs,.bl,.bg,.nv,.mi,.ml,.mb-a,.toc a,.ra,.ct,summary,.card,.tl svg,.tx svg,.il svg,.btn svg,.nv svg,.ra svg'
             '{transition:color .15s,background-color .15s,border-color .15s,text-decoration-color .15s,box-shadow .15s,stroke .15s,transform .15s}\n'
             '@media (hover:hover){' + _rules(HOVER, ':hover') + '.faq:hover{border-color:#C8A15A !important;background:#FFF8EA !important}}\n'
             + _rules(HOVER, ':focus-visible') + '\n'
             '@media (hover:hover) and (prefers-reduced-motion:no-preference){.btn:hover{transform:translateY(-1px)}.card:hover{transform:translateY(-3px)}'
             '.tl:hover svg,.tx:hover svg{transform:translateX(3px)}}\n'
             '@container pg (max-width:599px){@media (hover:hover){' + _rules(HOVER_P, ':hover') + '}' + _rules(HOVER_P, ':focus-visible') + '}\n')

BASE_CSS = ('body{margin:0;background:#FBF4EA}\n*,*::before,*::after{box-sizing:border-box}\n'
            'a{color:#8C2B18}\ninput::placeholder,textarea::placeholder{color:#6B746E}\n'
            '.nvi{position:relative;display:inline-flex}.nvm{position:absolute;top:100%;left:-16px;padding-top:9px;display:none;z-index:40}'
            '.nvi:hover>.nvm,.nvi:focus-within>.nvm{display:block}\n'
            'input:focus,textarea:focus,select:focus{outline:2px solid #C8A15A;outline-offset:1px}'
            'a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #C8A15A;outline-offset:2px}\n' + RESP_CSS + HOVER_CSS)

_TAG = re.compile(r'<[a-zA-Z][^<>]*>')
def _hook(m):
    t = m.group(0)
    if 'max-width: 1440px; margin: 0 auto' not in t:
        return t
    if ' class="' in t:
        return t.replace(' class="', ' class="w ', 1)
    return re.sub(r'^<(\w+)', r'<\1 class="w"', t, count=1)

_FS = re.compile(r'font-size:\s*([0-9.]+)px')
def _fsu(m):
    t = m.group(0)
    if t.startswith(('<svg', '<path', '<circle', '<rect')) or ' style="' not in t:
        return t
    f = _FS.findall(t.split(' style="', 1)[1])
    if not f or float(f[-1]) >= 12:
        return t
    cm = re.search(r' class="([^"]*)"', t)
    if cm and ('lk' in cm.group(1).split() or 'fsu' in cm.group(1).split()):
        return t
    if cm:
        return t.replace(cm.group(0), f' class="{cm.group(1)} fsu"', 1)
    return re.sub(r'^<(\w+)', r'<\1 class="fsu"', t, count=1)

ROLE_CLASSES = {'t-b', 't-s', 't-h3', 't-h3l', 'lead', 'h1', 'h2', 'fsu', 'lk', 'tl', 'btn', 'nv', 'ml', 'fl', 'mb-a', 'bo', 'bl', 'cl', 'crumb'}
_ROLE_TAGS = {'p', 'li', 'dd', 'dt', 'figcaption', 'ul', 'ol', 'span', 'a', 'div', 'summary'}
def _role(m):
    """Type roles for phones and tablets (RESP_CSS sets their sizes there; desktop keeps the inline sizes). Helpers set
    t-b (body, 16 px) and t-s (secondary, 14.5 px) themselves; any other text element with an inline size from 12.5 to
    15.9 px gets one here: under 13.5 px secondary, else body. Labels (uppercase or tracked), headings (serif), text that
    must stay on one line (nowrap) and elements with their own size rule are left alone."""
    t = m.group(0)
    tag = t[1:].split(' ', 1)[0].rstrip('>')
    if tag not in _ROLE_TAGS or ' style="' not in t:
        return t
    st = t.split(' style="', 1)[1]
    f = _FS.findall(st)
    if not f or not 12.5 <= float(f[-1]) < 16:
        return t
    if 'uppercase' in st or 'nowrap' in st or 'Newsreader' in st or re.search(r'letter-spacing:\s*0\.(0[5-9]|1)', st):
        return t
    cm = re.search(r' class="([^"]*)"', t)
    if cm and ROLE_CLASSES & set(cm.group(1).split()):
        return t
    role = 't-s' if float(f[-1]) < 13.5 else 't-b'
    if cm:
        return t.replace(cm.group(0), f' class="{cm.group(1)} {role}"', 1)
    return re.sub(r'^<(\w+)', rf'<\1 class="{role}"', t, count=1)

HEAD_ROLES = {'h1', 'h2', 't-h3', 't-h3l', 't-h3t', 't-hs', 'tm-n', 'hsub'}
def _head(m):
    """One heading scale on phones (sizes in RESP_CSS, under 600 px; wider screens keep the inline sizes): display h1 31,
    section h2 26, panel and featured-card titles t-h3l 22, card titles t-h3 20, tile and feature titles t-h3t 17.5,
    small sans headings t-hs 15.5. Helpers set h1, h2 and t-h3 themselves; any other h2/h3/h4 gets its step here: a serif
    h2 without the section class sits in a band or a panel (t-h3l); a serif h3/h4 from 23 px is a featured title (t-h3l),
    from 17 px a card title (t-h3), smaller a feature title (t-h3t); a sans heading is a small heading (t-hs)."""
    t = m.group(0)
    tag = t[1:3]
    if tag not in ('h2', 'h3', 'h4') or t[3:4] not in (' ', '>') or ' style="' not in t:
        return t
    cm = re.search(r' class="([^"]*)"', t)
    if cm and HEAD_ROLES & set(cm.group(1).split()):
        return t
    st = t.split(' style="', 1)[1]
    f = _FS.findall(st)
    if not f:
        return t
    size = float(f[-1])
    if 'Newsreader' in st:
        role = 't-h3l' if (tag == 'h2' or size >= 23) else ('t-h3' if size >= 17 else 't-h3t')
    else:
        role = 't-hs'
    if cm:
        return t.replace(cm.group(0), f' class="{cm.group(1)} {role}"', 1)
    return re.sub(r'^<(\w+)', rf'<\1 class="{role}"', t, count=1)

_TXT = re.compile(r'(<[a-zA-Z/!][^<>]*>)')
_PHONE = re.compile(r'\(\d{3}\) \d{3}-\d{4}(?: ext\. \d+)?|\d{3}-\d{3}-\d{4}(?: ext\. \d+)?|\b[A-Z]\d[A-Z] \d[A-Z]\d\b')
_TELEXT = re.compile(r'(<a [^>]*href="tel:[^"]*"[^>]*>[^<]*</a>)( ext\. \d+)')
def _nobreak(body):
    """Phone numbers, "ext. 213" and postal codes (K0K 1X0) never split across lines (class nb, nowrap under 1100 px only, so wide layouts are
    unchanged). Only text between tags is touched, never attributes or scripts. Email addresses are left as they are:
    an element inside an address changes how the browser measures it, and wide layouts must not change; under 1100 px
    mailto links may break anywhere if one does not fit on its line (RESP_CSS)."""
    body = _TELEXT.sub(r'<span class="nb">\1\2</span>', body)
    parts = _TXT.split(body)
    inside_script = False
    for i, part in enumerate(parts):
        if i % 2:
            low = part[:8].lower()
            inside_script = low.startswith('<script') or (inside_script and not low.startswith('</script'))
            continue
        if inside_script or not part.strip():
            continue
        parts[i] = _PHONE.sub(lambda m: f'<span class="nb">{m.group(0)}</span>', part)
    return ''.join(parts)

# _linkkind: the hover kind (HOVER_CSS) of a link written by hand in page text, from its inline colour
LINK_INK = {'#10291F', '#17231D', '#0F3325', '#13261B', '#3A4640', '#133019'}
LINK_ON_DARK = {'#FFFFFF', '#F4EFE4', '#F4F1E8', '#FFF6EC', '#FBF4EA'}
LINK_GOLD_ON_DARK = {'#E3BE74', '#D9B36A', '#DDB86C'}
LINK_RUST = {'#8C2B18', '#9C4530', '#A0432C', '#9A3B26'}
_LINKTAG = re.compile(r'<(a|summary)(\s[^<>]*)?>(<img |<span style="text-decoration: underline)?')
def _linkkind(m):
    """Every link and summary gets a hover class. Helpers give theirs; a link without a class gets one here: a picture
    link (it holds only an image) pl; ink il; cream or white on a dark band dl; gold on a dark band dl dg; rust or the
    page's own link colour tx. A label in its own underlined span adds tu (its underline turns gold, none is added)."""
    tag, attrs, nxt = m.group(1), m.group(2) or '', m.group(3) or ''
    if tag == 'a' and ' href=' not in attrs:
        return m.group(0)
    cm = re.search(r' class="([^"]*)"', attrs)
    have = cm.group(1).split() if cm else []
    add = []
    if not have:
        st = re.search(r' style="([^"]*)"', attrs)
        col = re.search(r'(?:^|;)\s*color:\s*(#[0-9A-Fa-f]{6})', st.group(1)) if st else None
        c = col.group(1).upper() if col else None
        if nxt == '<img ':
            add.append('pl')
        elif c in LINK_INK:
            add.append('il')
        elif c in LINK_GOLD_ON_DARK:
            add += ['dl', 'dg']
        elif c in LINK_ON_DARK:
            add.append('dl')
        elif c is None or c in LINK_RUST:
            add.append('tx')
        else:
            raise AssertionError(f'_linkkind: a link coloured {c} has no hover kind; give it a class: {m.group(0)[:160]}')
    if nxt.startswith('<span') and 'tu' not in have:
        add.append('tu')
    if not add:
        return m.group(0)
    if cm:
        tagtxt = m.group(0).replace(cm.group(0), f' class="{" ".join(have + add)}"', 1)
    else:
        tagtxt = f'<{tag} class="{" ".join(add)}"{attrs}>{nxt}'
    return tagtxt

def responsive(body):
    """Hooks the narrow-width rules need: every link gets its hover kind (_linkkind), every page-width wrapper gets class w, text set below 12 px gets class fsu
    (lifted to 12 px on phones, except the logo lockup, class lk), headings get a step of the phone scale (_head), body
    copy gets a type role (_role), phone numbers get
    their no-break rule (_nobreak), and forced line breaks keep a space when they are switched off."""
    body = _LINKTAG.sub(_linkkind, body)
    body = _TAG.sub(_hook, body)
    body = _TAG.sub(_fsu, body)
    body = _TAG.sub(_head, body)
    body = _TAG.sub(_role, body)
    body = _nobreak(body)
    return body.replace('<br>', ' <br>')

def root(body, frame=None):
    page = (f'<div class="pg" style="position: relative; overflow: hidden; font-family: {SANS}; font-size: 15px; font-weight: 450; line-height: 1.45; color: {INK}; '
            f'background: linear-gradient(180deg, #FCF5EB 0%, #FBF2E7 100%)">{responsive(body)}</div>')
    if frame:      # tablet / phone artboards: the same page held to a device width
        return f'<div style="max-width: {frame}px; margin: 0 auto">{page}</div>'
    return page

def dc_document(title, body, height, frame=None):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="{FONT_HREF}" rel="stylesheet">
<style>
{BASE_CSS}
</style>
</helmet>
{root(body, frame)}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{frame or 1440},"height":{height}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''

FDIR = '/home/claude/iipct_work/fonts/node_modules'
def preview_document(title, body):
    faces = ''
    for fam, pkg in (('Newsreader', 'newsreader'), ('DM Sans', 'dm-sans')):
        for st in ('normal', 'italic'):
            faces += (f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:100 1000;"
                      f"src:url('file://{FDIR}/@fontsource-variable/{pkg}/files/{pkg}-latin-opsz-{st}.woff2') format('woff2');}}\n")
    faces += f"@font-face{{font-family:'Kaushan Script';src:url('file://{FDIR}/@fontsource/kaushan-script/files/kaushan-script-latin-400-normal.woff2') format('woff2');}}\n"
    html = root(body)
    for name, url in BLOB.items():
        html = html.replace(f'src="{url}"', f'src="file://{A}{META[name]["file"]}"')
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{faces}{BASE_CSS}</style></head><body>{html}</body></html>'
