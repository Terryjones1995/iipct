"""Shared building blocks for the IIPCT rebrand artboards (inline-styled markup)."""
import json, os, re, math, random

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
    return (f'<span style="flex: none; width: {size}px; height: {size}px; border-radius: 50%; display: flex; align-items: center; justify-content: center; '
            f'background: radial-gradient(circle at 38% 30%, {hi} 0%, {lo} 78%); box-shadow: 0 0 0 2px #FFFDF8, 0 0 0 3px rgba(120, 92, 44, 0.32); {style}">'
            f'{ico(name, isize, "#FCF2DF", sw)}</span>')

def img(name, alt, style):
    return f'<img src="{BLOB[name]}" alt="{alt}" style="display: block; {style}">'

# ---------------------------------------------------------------- type helpers
def eyebrow(text, color=RUST, style=''):
    return f'<span style="display: block; font-size: 12.8px; font-weight: 700; letter-spacing: 0.16em; line-height: 1.1; text-transform: uppercase; color: {color}; {style}">{text}</span>'

def h2(text, size=32, color=HEAD, style='', tag='h2', weight=600):
    cls = ' class="h2"' if size >= 26.4 else ''
    return f'<{tag}{cls} style="margin: 0; font-family: {SERIF}; font-weight: {weight}; font-size: {size}px; line-height: 1.06; letter-spacing: -0.018em; color: {color}; {style}">{text}</{tag}>'

def p(text, size=14, color=INK, lh=1.36, style=''):
    return f'<p style="margin: 0; font-size: {size}px; line-height: {lh}; color: {color}; {style}">{text}</p>'

def vdiv(h='100%', color=GOLDL, style=''):
    return f'<span class="vd" aria-hidden="true" style="flex: none; align-self: stretch; width: 1px; min-height: {h}; background: {color}; {style}"></span>'

SQUIGGLE = ('<svg aria-hidden="true" width="160" height="17" viewBox="0 0 160 17" style="display: block">'
            '<path d="M1 15 C 24 5 58 1 95 4 C 118 6 140 5.6 159 1 C 145 10.6 120 13.6 94 11 C 62 7.8 30 9.8 1 15 Z" fill="#C79A3D"></path></svg>')

# ---------------------------------------------------------------- buttons
BOOK_LABELS = ('Schedule Your Visit', 'Book an Appointment', 'Book Online')
def btn(label, href='#', kind='primary', icon=None, arrow=True, size='md', style=''):
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
    cls = {'primary': 'btn bp', 'outline': 'btn bo', 'gold': 'btn bg', 'light': 'btn bo', 'soft': 'btn bs', 'sage': 'btn bo'}[kind]
    ic = ico(icon, round(fs + 3.5), 'currentColor', 1.8) if icon else ''
    ar = ico('arrow', round(fs + 1.5), 'currentColor', 2) if arrow else ''
    return f'<a class="{cls}" href="{href}" style="{base}{look}; {style}">{ic}<span>{label}</span>{ar}</a>'

def textlink(label, href='#', size=14.4, style='', icon='arrow'):
    return (f'<a class="tl" href="{href}" style="display: inline-flex; align-items: center; gap: 12px; font-size: {size}px; font-weight: 600; color: {RUST}; text-decoration: none; white-space: nowrap; {style}">'
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

def landscape(h=98, sun_x=720, style='', tall=False):
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
    return f'''<svg aria-hidden="true" viewBox="0 0 1440 {h}" preserveAspectRatio="xMidYMax slice" style="display: block; width: 100%; height: {h}px; {style}">
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

NEWSLETTER_URL = 'https://mailchi.mp/iipct/iipct-newsletter'
MENUS = {
 'who': [('About IIPCT', 'WhoWeAre.dc.html', 0), ('Career Opportunities', 'Careers.dc.html', 0), ('Board of Directors', 'Board.dc.html', 0), ('Best Practice Spotlight (BPSO)', 'BPSO.dc.html', 0)],
 'services': [('All Services', 'Services.dc.html', 0), ('Primary Medical Care', 'PrimaryCare.dc.html', 0), ('Immunization Program', 'Immunization.dc.html', 1),
              ('Well Baby &amp; Well Child', 'WellBaby.dc.html', 1), ('TB Testing', 'TBTesting.dc.html', 1), ('Advanced Foot Care', 'FootCare.dc.html', 1),
              ('Diabetic Retinopathy Screening', 'Retinopathy.dc.html', 1), ('Outreach &amp; Community Support', 'Outreach.dc.html', 1)],
 'events': [('Events &amp; Programs', 'Events.dc.html', 0), ('News &amp; Updates', 'News.dc.html', 0), ('Newsletter', NEWSLETTER_URL, 0)],
}

def dual_btn(href='Booking.dc.html'):
    """Header CTA: the two actions joined into one segmented control."""
    seg = ('display: inline-flex; align-items: center; justify-content: center; gap: 7px; min-height: 44px; padding: 0 12px; '
           'font-size: 12.6px; font-weight: 600; line-height: 1; text-decoration: none; white-space: nowrap; ')
    return (f'<span class="hd-cta" style="flex: none; display: inline-flex; border-radius: 10px; overflow: hidden; border: 1.5px solid #1E3D28; box-shadow: 0 1px 2px rgba(16, 44, 24, 0.20)">'
            f'<a class="seg" href="{href}" style="{seg}background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF">{ico("calendar-check", 16, "currentColor", 1.8)}<span>Schedule Your Visit</span></a>'
            f'<a class="seg sego hd-seg2" href="{href}" style="{seg}background: #FFFDF8; color: #13261B; border-left: 1.5px solid #1E3D28">{ico("calendar-dot", 16, "currentColor", 1.8)}<span>Book an Appointment</span></a>'
            f'</span>')

def _menu(key):
    rows = ''
    for label, href, lvl in MENUS[key]:
        ext = ico('external', 13, '#8C2B18', 1.9) if href.startswith('http') else ''
        if lvl:
            st = 'padding: 7px 12px 7px 26px; font-size: 12.8px; font-weight: 500; color: #3A4640'
        else:
            st = 'padding: 9px 12px; font-size: 13.4px; font-weight: 600; color: #10291F'
        rows += (f'<a href="{href}" style="display: flex; align-items: center; justify-content: space-between; gap: 14px; border-radius: 8px; '
                 f'line-height: 1.2; text-decoration: none; white-space: nowrap; {st}"><span>{label}</span>{ext}</a>')
    return (f'<span class="nvm"><span style="display: flex; flex-direction: column; gap: 1px; min-width: 236px; padding: 8px; border-radius: 12px; '
            f'background: #FFFDF8; border: 1px solid {LINE}; box-shadow: 0 2px 4px rgba(40, 30, 10, 0.06), 0 14px 28px rgba(40, 30, 10, 0.16); letter-spacing: 0">{rows}</span></span>')

def _mobile(active):
    """Book button + menu for tablet and phone widths. The menu is a native <details>, so it opens without script."""
    rows = ''
    for label, href, dd, key in NAV:
        col = '#9A3B26' if key == active else '#10291F'
        rows += (f'<a class="ml" href="{href}" style="display: flex; align-items: center; min-height: 46px; padding: 0 12px; border-radius: 9px; font-size: 16px; font-weight: 700; '
                 f'color: {col}; text-decoration: none">{label}</a>')
        for l2, h2, lvl in (MENUS[key][1:] if dd else []):
            x = ico('external', 13, '#8C2B18', 1.9) if h2.startswith('http') else ''
            rows += (f'<a class="ml" href="{h2}" style="display: flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 12px 0 {28 + 16 * lvl}px; border-radius: 9px; font-size: 14.6px; '
                     f'font-weight: 500; color: #3A4640; text-decoration: none"><span>{l2}</span>{x}</a>')
    book = ('display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 44px; padding: 0 15px; border-radius: 10px; font-size: 13.6px; font-weight: 600; line-height: 1; '
            'text-decoration: none; white-space: nowrap; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; border: 1px solid #2E5E38')
    return (f'<div class="hd-m">'
            f'<a class="btn bp" href="Booking.dc.html" style="{book}">{ico("calendar-check", 17, "currentColor", 1.8)}<span>Book<span class="xs-hide"> a Visit</span></span></a>'
            f'<details class="mnav"><summary aria-label="Menu" style="width: 46px; height: 44px; border-radius: 10px; border: 1.5px solid #1E3D28; background: #FFFDF8; color: #13261B; '
            f'display: flex; align-items: center; justify-content: center; cursor: pointer">'
            f'<span class="mi-o" style="display: flex">{ico("menu", 22, "currentColor", 2)}</span><span class="mi-x" style="display: flex">{ico("close", 22, "currentColor", 2)}</span></summary>'
            f'<div style="position: absolute; left: 0; right: 0; top: 100%; z-index: 40; padding: 10px 20px 22px; background: #FFFDF8; border-top: 1px solid {LINE}; border-bottom: 1px solid {LINE}; '
            f'box-shadow: 0 18px 30px rgba(40, 30, 10, 0.18)"><nav aria-label="Menu" style="display: flex; flex-direction: column; gap: 1px">{rows}</nav>'
            f'<div style="margin-top: 14px; padding-top: 16px; border-top: 1px solid {LINE}; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px">'
            f'<a class="btn bp" href="Booking.dc.html" style="{book}; flex: 1 1 220px; min-height: 48px; font-size: 15px">{ico("calendar-check", 18, "currentColor", 1.8)}<span>Schedule Your Visit</span></a>'
            f'<a href="tel:+13434780196" style="display: inline-flex; align-items: center; gap: 10px; min-height: 44px; font-size: 16px; font-weight: 700; color: #10291F; text-decoration: none">'
            f'{ico("phone", 19, "#9C4530", 1.8)}<span>(343) 478-0196</span></a></div></div></details></div>')

NAV_SIZE = 14
def header(active):
    items = ''
    for label, href, dd, key in NAV:
        on = key == active
        col = '#9A3B26' if on else '#10291F'
        bb = '#9A3B26' if on else 'transparent'
        chev = ico('chev-down', 12, col, 2.4) if dd else ''
        link = (f'<a class="nv" href="{href}" style="display: inline-flex; align-items: center; gap: 5px; padding: 10px 0 8px; border-bottom: 2px solid {bb}; '
                f'color: {col}; text-decoration: none; white-space: nowrap">{label}{chev}</a>')
        items += f'<span class="nvi">{link}{_menu(key)}</span>' if dd else link
    return f'''
<header style="position: relative; z-index: 20; border-bottom: 1px solid {LINE}">
<div class="hd" style="{WRAP}; padding: 11px 40px 10px 48px; min-height: 102px; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px">
<a href="Main.dc.html" style="display: flex; align-items: center; gap: 12px; text-decoration: none; color: {H1C}">
{img('logo-emblem', 'IIPCT logo: a turtle carrying a medicine wheel, with a stethoscope shaped like a heart', 'width: 80px; height: auto').replace('<img ', '<img class="hd-logo" ')}
<span style="display: flex; flex-direction: column; gap: 5px">
<span style="font-family: {SERIF}; font-weight: 700; font-size: 30px; line-height: 0.95; letter-spacing: -0.012em; color: {H1C}">IIPCT</span>
<span class="hd-tag" style="font-size: 9.6px; font-weight: 700; letter-spacing: 0.035em; line-height: 1.22; text-transform: uppercase; color: {INK}">Indigenous Interprofessional<br class="k">Primary Care Team</span>
</span>
</a>
<span class="hd-div" aria-hidden="true" style="flex: none; width: 1px; height: 60px; background: {GOLDL}; margin: 0 8px 0 2px"></span>
<nav class="hd-nav" aria-label="Main" style="flex: 1 1 420px; min-width: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 17px; font-size: {NAV_SIZE}px; font-weight: 600; letter-spacing: -0.005em">{items}</nav>
{dual_btn()}
{_mobile(active)}
</div>
</header>'''

def _fcol(title, links, w, pl):
    rows = ''.join(f'<a class="fl" href="{h}" style="color: #F4EFE4; text-decoration: none; font-size: 12.4px; line-height: 1.2">{t}</a>' for t, h in links)
    return (f'<div class="ft-col" style="flex: none; width: {w}px; min-height: 110px; padding: 2px 10px 2px {pl}px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; flex-direction: column; gap: 10px">'
            f'<span style="font-size: 13.2px; font-weight: 700; color: #FFFFFF; margin-bottom: 3px">{title}</span>{rows}</div>')

def footer(top_h=90, pre='', tall=False):
    crow = lambda ic, t, h: (f'<a class="fl" href="{h}" style="display: flex; align-items: center; gap: 13px; color: #F4EFE4; text-decoration: none; font-size: 12.4px; line-height: 1.2">{ico(ic, 17, "#D9B36A", 1.7)}<span>{t}</span></a>')
    bar = ''.join(f'<span style="flex: 1; background: {c}"></span>' for c in ['#FEFDFC', '#F7D80C', '#BA2B2C', '#0A8242'])
    pipe = '<span class="ft-pipe" aria-hidden="true" style="width: 1px; height: 15px; background: #C8A15A"></span>'
    return f'''
<footer style="position: relative; margin-top: 4px">
{pre}{landscape(top_h, 720, '', tall)}
<div style="background: #0C271D; color: #F4EFE4; margin-top: -1px">
<div style="{WRAP}; padding: 14px 40px 0 55px">
<div class="ft-row" style="display: flex; flex-wrap: wrap; gap: 26px 0; align-items: flex-start; padding-bottom: 22px">
<div class="ft-logo" style="flex: none; width: 308px; display: flex; flex-direction: column; align-items: flex-start; gap: 14px; padding-top: 2px">
<a href="Main.dc.html" style="display: flex; align-items: center; gap: 13px; text-decoration: none">
<span style="flex: none; width: 94px; height: 94px; border-radius: 50%; background: #FBF4EA; display: flex; align-items: center; justify-content: center">{img('logo-emblem', 'IIPCT logo', 'width: 76px; height: auto')}</span>
<span style="display: flex; flex-direction: column; gap: 6px">
<span style="font-family: {SERIF}; font-weight: 600; font-size: 33px; line-height: 0.95; letter-spacing: -0.01em; color: #FFFFFF">IIPCT</span>
<span style="font-size: 9.6px; font-weight: 600; letter-spacing: 0.06em; line-height: 1.25; text-transform: uppercase; color: #FFFFFF">Indigenous Interprofessional<br class="k">Primary Care Team</span>
</span>
</a>
{social_row(dark=True)}
</div>
<div class="ft-col ft-contact" style="flex: none; width: 278px; min-height: 110px; padding: 2px 10px 2px 40px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; flex-direction: column; gap: 10px">
<span style="font-size: 13.2px; font-weight: 700; color: #FFFFFF; margin-bottom: 3px">Contact Us</span>
{crow('phone', '(343) 478-0196', 'tel:+13434780196')}
{crow('mail', 'info@iipct.com', 'mailto:info@iipct.com')}
{crow('pin', 'Southeastern Ontario', 'Contact.dc.html')}
{crow('clock', 'Mon – Fri, 8:30 AM – 4:30 PM', 'Contact.dc.html')}
</div>
{_fcol('Quick Links', [('Home', 'Main.dc.html'), ('Who We Are', 'WhoWeAre.dc.html'), ('Services', 'Services.dc.html'), ('Events &amp; Programs', 'Events.dc.html'), ('News &amp; Updates', 'News.dc.html'), ('Newsletter', NEWSLETTER_URL)], 196, 42)}
{_fcol('Clinic Links', [('Tyendinaga Clinic', 'Contact.dc.html'), ('Deseronto Clinic', 'Contact.dc.html'), ('Kingston Clinic', 'Contact.dc.html'), ('Bancroft Clinic', 'Contact.dc.html'), ('Shannonville Clinic', 'Contact.dc.html')], 198, 41)}
{_fcol('More', [('Careers', 'Careers.dc.html'), ('Board', 'Board.dc.html'), ('BPSO', 'BPSO.dc.html'), ('Contact', 'Contact.dc.html')], 127, 41)}
<div class="ft-col ft-art" style="flex: none; min-height: 110px; padding-left: 34px; border-left: 1px solid rgba(200, 161, 90, 0.75); display: flex; align-items: center; gap: 20px">
{img('feather-gold', '', 'width: 70px; height: auto; margin-top: -4px')}
<span style="display: flex; flex-direction: column; gap: 3px; font-family: {SCRIPT}; font-size: 21px; line-height: 1.38; color: #DDB86C">
<span>Culture</span><span>Community</span><span>Care</span><span>Wellness</span>
</span>
</div>
</div>
<div style="border-top: 1px solid rgba(255, 255, 255, 0.42); padding: 15px 0 19px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; font-size: 12.4px; color: #F4EFE4">
<span>© 2026 IIPCT – Indigenous Interprofessional Primary Care Team. All rights reserved.</span>
{pipe}<a class="fl" href="Privacy.dc.html" style="color: #F4EFE4; text-decoration: none">Privacy Policy</a>
{pipe}<a class="fl" href="Accessibility.dc.html" style="color: #F4EFE4; text-decoration: none">Accessibility</a>
{pipe}<a class="fl" href="SiteMap.dc.html" style="color: #F4EFE4; text-decoration: none">Site Map</a>
{pipe}<span>Built by <a class="fl" href="https://pixelelite.ca" style="color: #E3BE74; font-weight: 600; text-decoration: none">Pixel Elite Media</a> · <a class="fl" href="https://pixelelite.ca" style="color: #F4EFE4; text-decoration: none">pixelelite.ca</a></span>
<span class="ft-bar" aria-hidden="true" style="margin-left: auto; width: 150px; height: 7px; border-radius: 2px; overflow: hidden; display: flex">{bar}</span>
</div>
</div>
</div>
</footer>'''

# ---------------------------------------------------------------- shared sections
def hero(photo, photo_w, min_h, h1, lead, buttons, eyebrow_txt=None, sub=None, h1_size=46, lead_size=18.6, lead_w=600, text_w=680, pad='36px 0 30px 83px', gap=14, sub_size=27.5, lead_lh=1.32, btn_mt=8, obj='right center', lead_weight=450, extra='', sq_mt=0):
    eb = eyebrow(eyebrow_txt, RUST, 'font-size: 12.5px; letter-spacing: 0.14em; margin-bottom: 2px') if eyebrow_txt else ''
    sb = (f'<p style="margin: 0; font-family: {SERIF}; font-weight: 620; font-size: {sub_size}px; line-height: 1.2; letter-spacing: -0.014em; color: {H1C}">{sub}</p>') if sub else ''
    sq = f'<span style="display: block; margin-top: {sq_mt}px">{SQUIGGLE}</span>'
    sq_first = sq if not sub else ''
    sq_last = sq if sub else ''
    fade_l = 100 - photo_w
    return f'''
<section class="hero-sec" style="position: relative; min-height: {min_h}px">
<img class="hero-photo" src="{BLOB[photo]}" alt="" style="display: block; position: absolute; top: 0; right: 0; width: {photo_w}%; height: 100%; object-fit: cover; object-position: {obj}">
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
</section>'''

def rust_band(icon, title, sub, right, style='', sub_size=13.1):
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
<div class="band-r" style="position: relative; min-width: 0; max-width: 100%; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px">{right}</div>
</div>
</section>'''

def newsletter(sub='Get the latest news, events, programs, and wellness updates from our team.'):
    right = (f'<label for="nl-email" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%)">Email address</label>'
             f'<input id="nl-email" type="email" placeholder="Enter your email address" style="flex: 1 1 240px; min-width: 0; width: 346px; max-width: 100%; height: 36px; padding: 0 18px; border-radius: 9px; border: 1px solid #F3E4D2; background: #FFFDF8; font-family: inherit; font-size: 12.4px; color: {INK}">'
             f'<button type="button" style="display: inline-flex; align-items: center; justify-content: center; gap: 12px; height: 40px; min-width: 156px; padding: 0 22px; border-radius: 9px; border: 1px solid #C8A15A; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; font-family: inherit; font-size: 13px; font-weight: 600; cursor: pointer; box-shadow: 0 2px 6px rgba(40, 20, 10, 0.3)"><span>Subscribe</span>{ico("arrow", 15, "#FFFFFF", 2)}</button>')
    return rust_band('mail', 'Stay Connected with IIPCT', sub, right)

def feature_list(items, icon_size=46, title_size=15.6, gap=22, text_size=12.5, icon_gap=33):
    """items: (icon, title, text)"""
    out = ''
    for ic, t, d in items:
        out += (f'<div style="display: flex; align-items: flex-start; gap: {icon_gap}px">{ico(ic, icon_size, RUSTI, 1.2, "margin-top: 1px")}'
                f'<div style="display: flex; flex-direction: column; gap: 4px"><h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: {title_size}px; line-height: 1.12; letter-spacing: -0.01em; color: {HEAD}">{t}</h3>'
                f'<p style="margin: 0; font-size: {text_size}px; line-height: 1.32; color: {INK}">{d}</p></div></div>')
    return f'<div style="display: flex; flex-direction: column; gap: {gap}px">{out}</div>'

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
FACEBOOK_URL = 'https://www.facebook.com/IIPCT.TMT/'
TIKTOK_URL = 'https://www.tiktok.com/@theiipctcrew'
BOOKING = 'Booking.dc.html'
CLINICS = [('Tyendinaga Clinic', '45 Meadow Drive, Tyendinaga', '(343) 478-0196', '+13434780196'),
           ('Deseronto Clinic', '331 Dundas Street, Deseronto', '(613) 354-6992', '+16133546992'),
           ('Kingston Clinic', '730 Front Road, Kingston', '(833) 999-1382', '+18339991382'),
           ('Bancroft Clinic', '69 Cleak Avenue, Bancroft', '(613) 706-2001', '+16137062001'),
           ('Shannonville Office', '14 York Road, Shannonville', '(343) 478-0196', '+13434780196')]

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
    return f'<nav aria-label="Breadcrumb" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: 12.6px; font-weight: 500">{sep.join(parts)}</nav>'

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
<section style="position: relative; overflow: hidden; border-bottom: 1px solid #E6D9BF">
{branch(150, '#A5B195', 0.5, 'left: -86px; top: -34px; transform: rotate(8deg)')}
<div style="position: relative; {WRAP}; padding: 26px 48px 32px 83px; display: flex; flex-wrap: wrap; align-items: center; gap: 26px 64px">
<div style="flex: 1 1 520px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 11px">
{crumbs(trail)}
{eb}<h1 class="h1" style="margin: 4px 0 0; font-family: {SERIF}; font-weight: 680; font-size: {title_size}px; line-height: 1.04; letter-spacing: -0.014em; color: {H1C}">{title}</h1>
{SQUIGGLE}
<p style="margin: 0; max-width: {lead_w}px; font-size: 17px; line-height: 1.42; color: {INK}">{lead}</p>
{extra}{bt}
</div>
{pic}
</div>
</section>"""

def h3(text, size=21, style=''):
    return f'<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: {size}px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}; {style}">{text}</h3>'

def panel(inner, style='', pad='22px 24px'):
    return f'<div style="padding: {pad}; border-radius: 14px; {CARD}; {style}">{inner}</div>'

def bullets(items, icon='check', color='#1F4A2B', size=14.4, gap=9):
    rows = ''.join(f'<li style="display: flex; align-items: flex-start; gap: 12px">{ico(icon, 19, color, 2.1, "margin-top: 1px")}<span>{t}</span></li>' for t in items)
    return f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: {gap}px; font-size: {size}px; line-height: 1.42; color: {INK}">{rows}</ul>'

def section(title, body, eyebrow_txt=None, size=27):
    eb = eyebrow(eyebrow_txt) if eyebrow_txt else ''
    return f'<section style="display: flex; flex-direction: column; gap: 12px">{eb}{h2(title, size)}{body}</section>'

def photo_ph(label, ratio='16 / 9', style=''):
    return (f'<div role="img" aria-label="{label}" style="aspect-ratio: {ratio}; border-radius: 14px; border: 1px dashed #B9AA86; background: #EFE9D6; display: flex; flex-direction: column; '
            f'align-items: center; justify-content: center; gap: 10px; padding: 18px; text-align: center; color: {MUTED}; font-size: 12.6px; line-height: 1.35; {style}">'
            f'{ico("camera", 30, "#7E8F6C", 1.5)}<span>{label}</span></div>')

def book_aside(related='', title='Book this service'):
    rows = ''.join(f'<li style="display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 8px 0; border-top: 1px solid #E6D9BF">'
                   f'<span style="font-weight: 600; color: {HEAD}">{n}</span><a class="tl" href="tel:{tel}" style="color: {RUST}; font-weight: 600; text-decoration: none; white-space: nowrap">{ph}</a></li>'
                   for n, ad, ph, tel in CLINICS)
    return f"""<aside class="aside" style="flex: 0 0 372px; max-width: 100%; display: flex; flex-direction: column; gap: 18px">
<div style="padding: 22px 22px 22px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-direction: column; align-items: flex-start; gap: 10px; box-shadow: {SHADOW}">
{eyebrow('Book a visit', '#E3BE74')}
<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 25px; line-height: 1.1; letter-spacing: -0.012em; color: #FFFFFF">{title}</h2>
<p style="margin: 0; font-size: 13.6px; line-height: 1.45; color: #F4F1E8">Registered patients can book online. New to IIPCT, or not sure what you need? Call us and reception will help.</p>
{btn('Schedule Your Visit', BOOKING, 'light', 'calendar-check', True, 'md', 'margin-top: 6px; width: 100%')}
<a class="fl" href="tel:+13434780196" style="display: flex; align-items: center; gap: 10px; margin-top: 4px; font-size: 15px; font-weight: 700; color: #FFFFFF; text-decoration: none">{ico('phone', 18, '#E3BE74', 1.8)}<span>(343) 478-0196</span></a>
</div>
<div style="padding: 18px 22px 12px; border-radius: 14px; {CARD}">
{h3('Call your clinic', 19)}
<ul style="margin: 10px 0 0; padding: 0; list-style: none; font-size: 13.4px; line-height: 1.3">{rows}</ul>
</div>
{related}
</aside>"""

def link_list(title, links):
    rows = ''.join(f'<li><a class="tl" href="{h}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 9px 0; border-top: 1px solid #E6D9BF; '
                   f'font-size: 13.6px; font-weight: 600; color: {HEAD}; text-decoration: none"><span>{t}</span>{ico("arrow", 15, RUST, 1.9)}</a></li>' for t, h in links)
    return f'<div style="padding: 18px 22px 10px; border-radius: 14px; {CARD}">{h3(title, 19)}<ul style="margin: 10px 0 0; padding: 0; list-style: none">{rows}</ul></div>'

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
            f'<p style="margin: 0; font-size: 14px; line-height: 1.46; color: {INK}">{text}</p></div></div>')

def ext(label, href, size=14, color=RUST, style=''):
    """Inline link to another website, marked with the external-link icon."""
    return (f'<a class="tl" href="{href}" style="font-size: {size}px; font-weight: 600; color: {color}; text-decoration: none; {style}">'
            f'<span style="text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1.5px">{label}</span>'
            f'{ico("external", round(size), color, 1.9, "display: inline; vertical-align: -2px; margin-left: 6px")}</a>')

def icon_item(icon, tone, title, text, more=''):
    """Icon medallion + title + text, as a bordered card."""
    return (f'<div style="display: flex; align-items: flex-start; gap: 16px; padding: 18px 20px 18px 18px; border-radius: 14px; {CARD}">'
            f'{circ(icon, tone, 52, 27, 1.5)}<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 5px; padding-top: 2px">'
            f'{h3(title, 18.4)}<p style="margin: 0; font-size: 13.8px; line-height: 1.46; color: {INK}">{text}</p>{more}</div></div>')

def link_card(icon, tone, title, text, href):
    """Whole card is the link to a child page."""
    return (f'<a class="card" href="{href}" style="position: relative; display: flex; align-items: flex-start; gap: 15px; min-height: 112px; padding: 18px 46px 18px 18px; border-radius: 14px; '
            f'{CARD}; color: {INK}; text-decoration: none">{circ(icon, tone, 56, 29, 1.5)}'
            f'<span style="min-width: 0; display: flex; flex-direction: column; gap: 5px; padding-top: 2px">'
            f'<span style="font-family: {SERIF}; font-weight: 700; font-size: 18.4px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}">{title}</span>'
            f'<span style="font-size: 13.4px; line-height: 1.44; color: {INK}">{text}</span></span>'
            f'<span aria-hidden="true" style="position: absolute; right: 14px; bottom: 13px; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; '
            f'background: #FFFDF8; border: 1px solid #C9B691">{ico("arrow", 13, "#13261B", 2)}</span></a>')

def grid(items, minw=300, gap=16, style=''):
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min({minw}px, 100%), 1fr)); gap: {gap}px; {style}">{"".join(items)}</div>'

def chips(items, style=''):
    out = ''.join(f'<li style="padding: 6px 13px 5px; border-radius: 999px; background: #FFFDF8; border: 1px solid #C9B691; font-size: 13px; font-weight: 600; line-height: 1.2; color: {HEAD}; white-space: nowrap">{t}</li>' for t in items)
    return f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: 8px; {style}">{out}</ul>'

def tag(text, tone='tan'):
    bg, bd = {'tan': ('#F0DDB5', '#D6BC86'), 'sage': ('#D9DCC4', '#B9BF9C'), 'rust': ('#F1D5C8', '#D9A892'), 'cream': ('#FFFDF8', '#C9B691')}[tone]
    return (f'<span style="display: inline-block; padding: 5px 10px 4px; border-radius: 6px; background: {bg}; border: 1px solid {bd}; font-size: 10.6px; font-weight: 700; '
            f'letter-spacing: 0.06em; text-transform: uppercase; line-height: 1.1; color: #2A2A1C; white-space: nowrap">{text}</span>')

def prose(*paras, size=14.8, style=''):
    return ''.join(f'<p style="margin: 0; max-width: 700px; font-size: {size}px; line-height: 1.55; color: {INK}; {style}">{t}</p>' for t in paras)

def draft_bar(text):
    """Thin strip under the header marking a page whose wording still needs the client's sign-off."""
    return (f'<div style="background: #F6EACD; border-bottom: 1px solid #DCC28C"><div style="{WRAP}; padding: 9px 48px 9px 83px; display: flex; align-items: center; gap: 11px; '
            f'font-size: 13px; line-height: 1.35; color: #3B2E12">{ico("info", 17, "#7A5A14", 1.9)}<span>{text}</span></div></div>')

# ---------------------------------------------------------------- document shell
# Narrow-width rules. They key off the page's own width (a container query), so a page behaves the same in a
# phone-width frame on the canvas as it does in a real phone-width window.
RESP_CSS = """.pg{container-type:inline-size;container-name:pg;min-width:320px}
.hd-m{display:none;margin-left:auto;align-items:center;gap:10px}
.mnav>summary{list-style:none}.mnav>summary::-webkit-details-marker{display:none}
.mnav[open] .mi-o,.mnav:not([open]) .mi-x{display:none !important}
.ml{transition:background .15s}.ml:hover{background:#F1E7D3}
@container pg (max-width:1399px){
.hd{padding-left:32px !important;padding-right:28px !important}
.hd-nav{gap:4px 14px !important}
.hd-seg2{display:none !important}
.pg h3,.pg li,.pg li>span{white-space:normal !important}
.hero-txt{padding-left:56px !important}
.hero-txt .h1{font-size:42px !important}
.hero-txt .lead{font-size:16.6px !important}
}
@container pg (max-width:1199px){
.hd-nav,.hd-cta,.hd-div{display:none !important}
.hd-m{display:flex}
.hd{min-height:0 !important;padding-top:9px !important;padding-bottom:9px !important;flex-wrap:nowrap !important}
.hd-logo{width:68px !important}
}
@container pg (max-width:1099px){
.w{padding-left:32px !important;padding-right:32px !important}
.hero-sec{min-height:0 !important;display:flex;flex-direction:column-reverse}
.hero-photo{position:relative !important;width:100% !important;height:320px !important}
.hero-fade{display:none}
.hero-photo{object-position:60% 30% !important}
.hero-txt{max-width:none !important;padding:30px 0 28px !important}
.hero-txt .h1{font-size:44px !important}
.hero-txt .lead{font-size:17.6px !important}
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
.hero-photo{height:240px !important}
.hero-txt{padding:26px 0 24px !important}
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
"""

FONT_HREF = ('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700'
             '&amp;family=Kaushan+Script&amp;family=Newsreader:ital,opsz,wght@0,6..72,400..800;1,6..72,400..800&amp;display=swap')
BASE_CSS = ('body{margin:0;background:#FBF4EA}\n*,*::before,*::after{box-sizing:border-box}\n'
            'a{color:#8C2B18}a:hover{color:#5F1B0E}\ninput::placeholder,textarea::placeholder{color:#6B746E}\n'
            '.nvi{position:relative;display:inline-flex}.nvm{position:absolute;top:100%;left:-16px;padding-top:9px;display:none;z-index:40}'
            '.nvi:hover>.nvm,.nvi:focus-within>.nvm{display:block}\n'
            '.nv{transition:color .15s,border-color .15s}.nv:hover{color:#9A3B26 !important;border-bottom-color:#9A3B26 !important}.nv:hover svg{stroke:#9A3B26}\n'
            '.nvm a{transition:background .15s,color .15s}.nvm a:hover{background:#F1E7D3;color:#8C2B18 !important}\n'
            '.btn,.seg{transition:transform .15s,box-shadow .15s,filter .15s,background .15s}.btn:hover{transform:translateY(-1px)}'
            '.bp:hover,.seg:hover{filter:brightness(1.16)}.bo:hover,.sego:hover{background:#F1E7D3 !important;filter:none}'
            '.bs:hover{filter:brightness(.96)}.bg:hover{background:#C8A15A !important;color:#10291F !important}\n'
            '.tl svg{transition:transform .15s}.tl:hover{color:#5F1B0E !important}.tl:hover svg{stroke:#5F1B0E;transform:translateX(3px)}\n'
            '.ra{transition:background .15s,border-color .15s}.ra:hover{background:#17402A !important;border-color:#17402A !important}.ra:hover svg{stroke:#fff}\n'
            '.card{transition:transform .18s,box-shadow .18s,border-color .18s}'
            '.card:hover{transform:translateY(-3px);border-color:#C8A15A !important;box-shadow:0 2px 4px rgba(64,44,14,.08),0 14px 26px rgba(64,44,14,.13) !important}\n'
            '.fl{transition:color .15s}.fl:hover{color:#E3BE74 !important}.faq:hover{border-color:#C8A15A !important;background:#FFF8EA !important}\n'
            '.toc a:hover{background:#F1E7D3}\n'
            'input:focus,textarea:focus,select:focus{outline:2px solid #C8A15A;outline-offset:1px}'
            'a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid #C8A15A;outline-offset:2px}\n' + RESP_CSS)

_TAG = re.compile(r'<[a-zA-Z][^<>]*>')
def _hook(m):
    t = m.group(0)
    if 'max-width: 1440px; margin: 0 auto' not in t:
        return t
    if ' class="' in t:
        return t.replace(' class="', ' class="w ', 1)
    return re.sub(r'^<(\w+)', r'<\1 class="w"', t, count=1)

def responsive(body):
    """Hooks the narrow-width rules need: every page-width wrapper gets class w, and forced line breaks keep a space when they are switched off."""
    body = _TAG.sub(_hook, body)
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
