"""Who We Are. Vision, Mission, Core Values, Who We Serve and the service area in the old iipct.org page's own words
(content/old-site/pages/who-we-are.md); the people come from p_team.TEAM. Real photographs only: the staff group photo
that headed the old page, the old service-area map and the staff's own portraits."""
from lib import *
from p_team import TEAM, LOCATIONS, TEAM_PAGE

def value_card(icon, tone, title, intro, items, ordered=False):
    tag_ = 'ol' if ordered else 'ul'
    pad = 'padding-left: 22px' if ordered else 'padding-left: 18px'
    rows = ''.join(f'<li style="padding-left: 2px">{t}</li>' for t in items)
    return (f'<div style="display: flex; flex-direction: column; gap: 12px; padding: 20px 22px 22px; border-radius: 14px; {CARD}">'
            f'<div style="display: flex; align-items: center; gap: 16px">{circ(icon, tone, 58, 29, 1.4)}'
            f'<h2 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 23px; line-height: 1.1; letter-spacing: -0.014em; color: {HEAD}">{title}</h2></div>'
            f'<p style="margin: 0; font-size: 14.6px; line-height: 1.5; color: {INK}">{intro}</p>'
            f'<{tag_} style="margin: 0; {pad}; display: flex; flex-direction: column; gap: 7px; font-size: 14.6px; line-height: 1.5; color: {INK}">{rows}</{tag_}></div>')

WHERE = ('<ul style="margin: 8px 0 0; padding-left: 18px; display: flex; flex-direction: column; gap: 5px; list-style: disc">'
         '<li><strong>Geographically</strong> – care that sees no boundaries and is status blind;</li>'
         '<li><strong>Emotionally</strong> – care that is provided in a safe place defined by the client;</li>'
         '<li><strong>Culturally</strong> – care that respects wherever clients are in their spiritual journey and cultural identity;</li>'
         '<li><strong>Physically</strong> – care that treats all medical needs and addresses complexity of care.</li></ul>')
VISION = ['All Indigenous people receive friendly, warm care “where they are”:' + WHERE,
          'Generosity of time and skills is shared freely.',
          'Traditional ways of knowing and being are valued and celebrated.']
MISSION = ['Provides excellence in wholistic primary healthcare;', 'Equally values traditional healing and clinical supports;',
           'Connects Indigenous people to regional services and professionals whom they can trust;',
           'Engages with all Indigenous communities across the region; and',
           'Shapes care and services based on the needs determined by the people/communities in our regions.']
VALUES = ['Everyone who walks in the door is treated as family;', 'Community builds community.']
SERVE = ('Our priority population are all the people who identify as Indigenous as well as their families, in our regions, with a special focus on '
         'people at risk for and living with chronic diseases as well as people living with mental health conditions and/or addictions. '
         'All our services are status blind.')
# sub-regions and communities exactly as the old page lists them ('Smiths Falls' corrected from the old 'Smith Falls')
REGIONS = [('Rural Frontenac, Lennox and Addington', ['Tyendinaga Mohawk Territory (MBQ)', 'Napanee', 'Deseronto', 'Ardoch Algonquin First Nation']),
           ('Rural Hastings', ['Kijicho Manito Madaouskarini Algonquin First Nation', 'Madoc', 'North Hastings']),
           ('Quinte', ['Belleville', 'Trenton', 'Picton']),
           ('Kingston', ['City of Kingston']),
           ('Leeds, Lanark, and Grenville', ['Perth', 'Gananoque', 'Smiths Falls'])]
STRIP = [1, 43, 29, 39, 15]      # Tera Osborne, Dr. Ryan McConnell, Kristine Canty, Jessi Baker, Andrew Alkenbrack
LOC_NAME = {k: label for k, aid, label in LOCATIONS}
LOC_ID = {k: aid for k, aid, label in LOCATIONS}

def strip_card(m):
    num, sec, a, name, short, role, leave, photo_file, bio = m
    where = '' if sec == 'leadership' else f'<span style="font-size: 13px; line-height: 1.3; color: {MUTED}">{LOC_NAME[sec]}</span>'
    return (f'<a class="card" href="{TEAM_PAGE}#{a}" style="display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; {CARD}; color: {INK}; text-decoration: none">'
            + photo(f'people/{photo_file}.jpg', f'Photo of {short}', f'width: 100%; height: auto; aspect-ratio: 1 / 1; object-fit: cover; border-bottom: 1px solid {LINE}', w=600, h=600)
            + f'<span style="display: flex; flex-direction: column; gap: 4px; padding: 13px 14px 15px">'
            f'<span style="font-family: {SERIF}; font-weight: 700; font-size: 18px; line-height: 1.12; letter-spacing: -0.014em; color: {HEAD}">{name}</span>'
            f'<span style="font-size: 14px; line-height: 1.3; color: {INK}">{role}</span>{where}</span></a>')

def location_tile(key, aid, label, tone):
    hi, lo = CIRC[tone]
    count = sum(1 for m in TEAM if m[1] == key)
    link = lambda t, h: (f'<a class="tl" href="{h}" style="display: inline-flex; align-items: center; gap: 8px; min-height: 40px; font-size: 13.8px; font-weight: 600; '
                         f'color: {RUST}; text-decoration: none"><span style="text-decoration: underline; text-underline-offset: 3px">{t}</span>{ico("arrow", 15, RUST, 1.9)}</a>')
    return (f'<article style="display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; {CARD}">'
            f'<div aria-hidden="true" style="height: 58px; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at 30% 20%, {hi} 0%, {lo} 85%)">'
            f'{pin_fill(28, "#FCF2DF", lo)}</div>'
            f'<div style="flex: 1; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; padding: 12px 16px 10px">'
            f'<h3 style="margin: 0 0 4px; font-family: {SERIF}; font-weight: 700; font-size: 18.4px; line-height: 1.15; letter-spacing: -0.014em; color: {HEAD}">{label}</h3>'
            f'{link(f"Meet the team ({count})", f"{TEAM_PAGE}#{aid}")}{link("Address, phone and hours", "Contact.dc.html")}</div></article>')

def page():
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Meet Our Team', 'Team.dc.html', 'outline', 'people', False)
    s = header('who')
    h = hero('hero-who', 59.7, 345, 'Who We Are',
             'Tsi Kanonhkhwatsheríyo offers inclusive healthcare with a focus on Indigenous communities. Our team provides accessible support across multiple disciplines, ensuring respectful and coordinated care for all who visit our clinic.',
             buttons, sub='Meet the experts combining traditional knowledge and modern healthcare.', h1_size=53, lead_size=15.8, lead_lh=1.45, sub_size=26,
             lead_w=560, pad='24px 0 30px 83px', gap=10, btn_mt=6, obj='center 35%')
    h = h.replace('position: relative; z-index: 1; max-width: 1440px; margin: 0 auto"', 'position: relative; z-index: 1; max-width: 1440px; margin: 0 auto; width: 100%"', 1)   # stacked hero: keep the text column full width
    s += h.replace(f'src="{BLOB["hero-who"]}" alt=""', 'src="/_site/about/team-group.jpg" alt="IIPCT staff together in a group photo, standing and seated on a sofa"', 1)
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 48px; margin-top: 18px">
<div style="display: flex; flex-wrap: wrap; align-items: stretch; gap: 16px">
<div style="flex: 1.15 1 520px; min-width: 0; display: flex">{value_card('sprout', 'sage', 'Our Vision', 'We envision vibrant communities where:', VISION, True).replace('display: flex; flex-direction: column; gap: 12px; padding', 'flex: 1; display: flex; flex-direction: column; gap: 12px; padding', 1)}</div>
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 16px">
{value_card('heart', 'rust', 'Our Mission', 'To accomplish this vision, the regional team:', MISSION)}
{value_card('people', 'gold', 'Our Core Values', 'To accomplish our vision and mission, the regional team upholds these values:', VALUES)}
</div>
</div>
</section>
<section style="position: relative; {WRAP}; margin-top: 22px">
{branch(104, '#B5BFA6', 0.5, 'right: -58px; bottom: -22px; transform: rotate(-14deg)')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: stretch">
<div class="sp-photo" style="flex: 0 0 29.9%; min-width: min(300px, 100%); display: flex">{arc_photo('who-smudge', 'Smudge bowl with smoke rising, resting on a rock beside sweetgrass', 'flex: 1; min-height: 259px')}</div>
<div class="sp-txt" style="flex: 1 1 380px; min-width: 0; padding: 14px 48px 20px 30px; display: flex; flex-direction: column; align-items: flex-start; gap: 11px; justify-content: center">
{eyebrow('Who We Serve')}
{h2('Indigenous People and Families<br>Across Southeastern Ontario', 32)}
{p(SERVE, 15.8, INK, 1.5, 'max-width: 720px')}
<div style="margin-top: 6px">{btn('Learn More About Our Services', 'Services.dc.html', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 14px; min-height: 40px')}</div>
</div>
</div>
</section>'''
    regions = ''.join(f'<li style="display: flex; flex-direction: column; gap: 4px"><h4 style="margin: 0; font-size: 13.6px; font-weight: 700; line-height: 1.25; color: {HEAD}">{r}</h4>'
                      f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 2px">'
                      + ''.join(f'<li style="display: flex; align-items: baseline; gap: 9px; font-size: 13.4px; line-height: 1.3"><span aria-hidden="true" style="flex: none; width: 7px; height: 7px; border-radius: 50%; background: #C89B4E; transform: translateY(-1px)"></span><span>{c}</span></li>' for c in cs)
                      + '</ul></li>' for r, cs in REGIONS)
    s += f'''
<section style="{WRAP}; padding: 0 37px 0 46px; margin-top: 18px">
<div style="position: relative; overflow: hidden; border-radius: 16px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; box-shadow: 0 1px 2px rgba(20, 40, 25, 0.20); padding: 22px; display: flex; flex-wrap: wrap; align-items: center; gap: 22px 26px">
{branch(118, '#2C5A40', 0.9, 'left: 6px; bottom: -92px; transform: rotate(-24deg)')}
<div class="pads2" style="position: relative; flex: 1 1 280px; min-width: 0; padding: 4px 0 4px 17px; display: flex; flex-direction: column; align-items: flex-start; gap: 9px">
{eyebrow('Our Service Area', '#E3BE74')}
{h2('Caring Across<br>Southeastern Ontario', 33, '#FFFFFF', 'font-weight: 500')}
{p('We serve five sub-regions. The map shows where they are, and the list names the communities in each.', 15.4, '#F4F1E8', 1.45, 'max-width: 340px; margin-top: 3px')}
</div>
<figure style="position: relative; flex: 1.3 1 340px; min-width: 0; margin: 0; padding: 10px; border-radius: 12px; background: #FBF4E8; border: 1px solid #CDBF9C">
{photo('about/service-area-map.png', 'Map of the five sub-regions IIPCT serves: Rural Hastings, Rural Frontenac, Lennox and Addington, Lanark, Leeds and Grenville, Quinte, and Kingston', 'width: 100%; height: auto; margin: 0 auto; max-width: 640px', w=640, h=471)}
</figure>
<div style="position: relative; flex: 1 1 300px; min-width: 0; padding: 16px 16px 16px 18px; border-radius: 12px; background: #FBF4E8; border: 1px solid #CDBF9C; color: {INK}">
<h3 style="margin: 0 0 10px; display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: {HEAD}">{pin_fill(16)}<span>Communities &amp; Areas We Serve</span></h3>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: 12px 18px">{regions}</ul>
</div>
</div>
</section>'''
    strip = ''.join(strip_card(next(m for m in TEAM if m[0] == n)) for n in STRIP)
    tiles = ''.join(location_tile(k, aid, label, tone) for (k, aid, label), tone in zip(LOCATIONS[1:], ['sage', 'rust', 'forest', 'gold', 'sage']))
    s += f'''
<section id="team" style="{WRAP}; padding: 30px 55px 0 66px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 26px">
{h2('Meet Our Team', 30)}
<span class="hide-s" aria-hidden="true" style="flex: 1; height: 1px; background: {GOLDL}"></span>
{textlink('Meet the full team', 'Team.dc.html', 14.4, 'min-height: 40px')}
</div>
{p('Our team is made up of highly trained and culturally safe professionals eager to provide care to the communities we serve.', 15.4, INK, 1.45, 'max-width: 720px; margin-top: 6px')}
<div style="margin-top: 16px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(136px, 100%), 1fr)); gap: 16px">{strip}</div>
</section>
<section style="{WRAP}; padding: 30px 55px 0 66px">
{eyebrow('Our Clinics &amp; Teams')}
{h2('Five Locations', 30, HEAD, 'margin-top: 6px')}
<div style="margin-top: 14px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); gap: 16px">{tiles}</div>
</section>
<div style="margin-top: 26px">'''
    right = (btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check', True, 'md', 'border-color: #C8A15A; min-width: 226px')
             + btn('Contact Us', 'Contact.dc.html', 'light', 'phone', False, 'md', 'min-width: 200px; font-size: 15px'))
    s += rust_band('mail', 'Connect with IIPCT', 'Have questions about who we are, our team, or how to access care? We’re here to help.', right, 'padding-right: 100px', 14.3) + '</div>'
    s += footer()
    return 'IIPCT — Who We Are', s
