"""Board of Directors: the seven members the old iipct.org Board page lists, in its order (content/old-site/board.json).
The old page prints a title only for the Chair, Treasurer and Secretary, so the other four sit under "Members" with no
title. Stacia Loft is the only member with a published biography and photograph; the others get an initials tile."""
from lib import *
from p_team import real_hero

BOARD = [('Susan Barberstock', 'Chair'), ('Josh Cowan', 'Treasurer'), ('Dora Yates', 'Secretary')]
MEMBERS = ['Dionne Nolan', 'Kathy Brant', 'Deb Brant']          # no title printed on the old page
STACIA_BIO = ('Stacia Loft (Ie’khahatakhe) is Kanyen’keha:ka from Tyendinaga Mohawk Territory. She received her Juris Doctor from Queen’s University in January 2020, '
              'and a Bachelor of Arts, Hons. from the University of Western Ontario in 2004. Stacia completed her Articles with Amnesty International and was called '
              'to the Ontario Bar in May 2021. Stacia was appointed the Director of Indigenous Initiatives and EDII Programs at Queen’s Law in 2021 and also serves as '
              'Deputy Grand Chief of the Association of Iroquois and Allied Indians (AIAI). Stacia previously served three terms as an elected Band Councillor on '
              'the Tyendinaga Mohawk Council.')
TONES = [('#8E9C7A', '#6F8263'), ('#BD7862', '#9E5540'), ('#C9A26E', '#A88250'), ('#4E6B4B', '#36503A')]

def tile(name, n, size=96):
    hi, lo = TONES[n % len(TONES)]
    ini = ''.join(w[0] for w in name.split()[:2]).upper()
    return (f'<span aria-hidden="true" style="flex: none; width: {size}px; height: {size}px; border-radius: 12px; display: flex; align-items: center; justify-content: center; '
            f'background: radial-gradient(circle at 38% 30%, {hi} 0%, {lo} 80%); border: 1px solid {LINE}; font-family: {SERIF}; font-weight: 600; '
            f'font-size: {round(size * 0.34)}px; letter-spacing: 0.02em; color: #FCF2DF">{ini}</span>')

def member_card(name, role, n):
    rl = (f'<span style="font-size: 15px; font-style: italic; line-height: 1.2; color: {INK}; padding-bottom: 1px; border-bottom: 1.5px solid #C79A3D">{role}</span>'
          if role else '')
    return (f'<article style="display: flex; align-items: center; gap: 18px; padding: 14px; border-radius: 14px; {CARD}">{tile(name, n)}'
            f'<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 6px">'
            f'<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 21px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}">{name}</h3>{rl}</div></article>')

def page():
    buttons = (btn('Meet the Board', '#members', 'primary', 'people', True, 'md', 'padding: 0 22px; gap: 10px; font-size: 14.4px')
               + btn('About IIPCT', 'WhoWeAre.dc.html', 'outline', 'doc', False, 'md', 'padding: 0 26px; gap: 11px; font-size: 14.4px'))
    s = header('board')
    h = hero('hero-board', 58.7, 322, 'Board of Directors',
             'Meet the members of the Board of Directors of Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (IIPCT).', buttons,
             h1_size=50.6, lead_size=19, lead_lh=1.4, lead_w=520, pad='40px 0 38px 86px', gap=11, btn_mt=10, sq_mt=2, obj='center 60%')
    s += real_hero(h, 'hero-board', 'about/field-sunset.jpg')
    grid = lambda cards: f'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr)); gap: 18px">{cards}</div>'
    s += f'''
<section id="members" style="scroll-margin-top: 16px; {WRAP}; padding: 30px 62px 0 60px; display: flex; flex-direction: column; gap: 18px">
<div style="padding-left: 4px">{sec_head('Our Board', 'Officers', '', 32)}</div>
{grid(''.join(member_card(n, r, i) for i, (n, r) in enumerate(BOARD)))}
<div style="padding-left: 4px; margin-top: 14px">{h2('Members', 32)}</div>
{grid(''.join(member_card(n, None, i + 3) for i, n in enumerate(MEMBERS)))}
<article id="stacia-loft" style="display: flex; flex-wrap: wrap; overflow: hidden; border-radius: 14px; background: #153526; border: 1px solid #0C2218; box-shadow: {SHADOW}">
<div class="fbs" style="flex: 0 0 300px; max-width: 100%; position: relative; min-height: 300px">{photo('board/stacia-loft.jpg', 'Photo of Stacia Loft', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 25%', w=600, h=600)}</div>
<div class="pads" style="position: relative; flex: 1 1 360px; min-width: 0; padding: 24px 30px 26px; display: flex; flex-direction: column; align-items: flex-start; gap: 6px; color: #FFFFFF">
{branch(96, '#2C5A40', 0.9, 'right: -10px; bottom: -70px; transform: rotate(24deg)')}
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 600; font-size: 30px; line-height: 1.08; letter-spacing: -0.016em; color: #FFFFFF">Stacia Loft</h3>
<span style="font-size: 15.2px; color: #F4F1E8">Ie’khahatakhe</span>
<span aria-hidden="true" style="width: 60px; height: 2px; background: #C8A15A; margin: 10px 0 8px"></span>
<p style="position: relative; margin: 0; max-width: 720px; font-size: 14.6px; line-height: 1.55; color: #F4F1E8">{STACIA_BIO}</p>
</div>
</article>
</section>
<div style="margin-top: 30px">'''
    right = btn('Get the Newsletter', NEWSLETTER_URL, 'light', 'mail', False, 'md', 'padding: 0 24px; gap: 10px')
    s += rust_band('mail', 'Stay Connected with IIPCT', 'Get the latest news, events, programs, and wellness updates from our team.', right) + '</div>'
    s += footer()
    return 'IIPCT — Board of Directors', s
