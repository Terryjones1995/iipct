from lib import *

def info_card(icon, tone, title, text):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 22px; min-height: 140px; padding: 22px 16px 18px 24px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{circ(icon, tone, 90, 44, 1.3)}
<div style="display: flex; flex-direction: column; gap: 7px; padding-top: 1px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 21px; line-height: 1.1; letter-spacing: -0.014em; color: {HEAD}">{title}</h3>
<p style="margin: 0; padding-right: 30px; font-size: 14.4px; line-height: 1.3; color: {INK}">{text}</p>
</div>
{round_arrow(26, 'arrow', title, '#', 'position: absolute; right: 14px; bottom: 12px')}
</div>'''

def pillar(icon, color, title, text, first=False):
    bl = '' if first else 'border-left: 1px solid #E6D6BC; '
    return f'''<div style="{bl}padding: 4px 8px 4px 22px; display: flex; flex-direction: column; align-items: flex-start; gap: 8px">
{ico(icon, 42, color, 1.25)}
<h3 style="margin: 2px 0 0; font-family: {SERIF}; font-weight: 700; font-size: 16.6px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 13.6px; line-height: 1.32; color: {INK}">{text}</p>
</div>'''

def team_card(photo, role):
    return f'''<div class="card" style="position: relative; display: flex; align-items: stretch; min-height: 104px; border-radius: 14px; background: #FCF6EC; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05); overflow: hidden">
<div style="flex: 0 0 41%; position: relative">{img(photo, 'Placeholder portrait', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 20%')}</div>
<div style="flex: 1; min-width: 0; padding: 22px 12px 12px 22px; display: flex; flex-direction: column; gap: 5px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 18.4px; line-height: 1.1; letter-spacing: -0.014em; color: {HEAD}">[Staff name]</h3>
<p style="margin: 0; font-size: 14.2px; line-height: 1.25; color: {INK}">{role}</p>
</div>
{round_arrow(24, 'arrow', role, '#', 'position: absolute; right: 13px; bottom: 12px')}
</div>'''

def clinic_card(photo, title, text):
    return f'''<article class="card" style="display: flex; flex-wrap: wrap; align-items: stretch; gap: 0 22px; padding: 7px; border-radius: 14px; background: #FCF6EC; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div class="fbs mh-s" style="flex: 0 0 46.5%; min-width: min(240px, 100%); position: relative; min-height: 137px">{img(photo, 'Placeholder clinic exterior', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 8px')}</div>
<div class="pads2" style="flex: 1 1 220px; min-width: 0; padding: 12px 14px 11px 0; display: flex; flex-direction: column; align-items: flex-start; gap: 8px">
<h3 style="margin: 0; display: flex; align-items: center; gap: 10px; font-family: {SERIF}; font-weight: 700; font-size: 18px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}; white-space: nowrap">{pin_fill(18)}<span>{title}</span></h3>
<p style="margin: 0; font-size: 12.6px; line-height: 1.3; color: {INK}">{text}</p>
{btn('Learn More', 'Contact.dc.html', 'sage', None, True, 'xs', 'margin-top: 3px; padding: 0 22px; gap: 12px; font-size: 12.6px')}
</div>
</article>'''

COMMUNITIES = ['Tyendinaga Mohawk Territory', 'Napanee', 'Deseronto', 'Belleville', 'Trenton', 'Picton', 'Kingston', 'Perth', 'Gananoque', 'Smiths Falls', 'Madoc', 'North Hastings']

def page():
    buttons = btn('Schedule Your Visit', 'Contact.dc.html', 'primary', 'calendar-check') + btn('Book an Appointment', 'Contact.dc.html', 'outline', 'calendar-dot', False)
    s = header('who')
    s += hero('hero-who', 59.7, 345, 'Who We Are',
              'IIPCT is an Indigenous-led, community-grounded primary care<br>team providing comprehensive, culturally safe, and wholistic<br>care for Indigenous people and families across southeastern Ontario.',
              buttons, sub='Indigenous-centred,<br>wholistic care for healthy<br>people, families, and communities', h1_size=53, lead_size=15.3, lead_lh=1.4, sub_size=28.2,
              pad='20px 0 30px 83px', gap=8, btn_mt=4, obj='center center')
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 48px; margin-top: 16px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(360px, 100%), 1fr)); gap: 16px">
{info_card('sprout', 'sage', 'Our Vision', 'Thriving Indigenous individuals, families, and communities in southeastern Ontario, supported by culturally safe, wholistic primary care.')}
{info_card('heart', 'rust', 'Our Mission', 'To provide Indigenous-centred, wholistic, team-based primary care that honours culture, community, and self-determination.')}
{info_card('people', 'gold', 'Our Core Values', 'Culture &nbsp;•&nbsp; Respect &nbsp;•&nbsp; Relationships<br>Wholistic Wellness &nbsp;•&nbsp; Equity<br>Community &nbsp;•&nbsp; Self-Determination')}
</div>
</section>'''
    body = p('We provide primary care and wellness supports for Indigenous people of all ages — from children and youth to adults and Elders — including individuals, families, and community members living in the urban, rural, and remote communities we serve.', 15.8, INK, 1.25, 'max-width: 500px')
    feats = feature_list([('feather', 'Culturally Safe Care', 'Rooted in Indigenous knowledge,<br>traditions, and ways of being.'),
                          ('infinity', 'Wholistic Supports', 'Care that honours the whole person —<br>mind, body, spirit, and emotions.'),
                          ('people', 'For All Life Stages', 'Primary care and wellness supports for<br>children, youth, adults, and Elders.')], 44, 17.4, 16, 13.4)
    s += split_section(arc_photo('who-smudge', 'Smudge bowl with smoke rising, resting on a rock beside sweetgrass', 'flex: 1; min-height: 259px'),
                       'Who We Serve', 'Indigenous People and Families<br>Across Southeastern Ontario', body,
                       btn('Learn More About Our Services', 'Services.dc.html', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 14px'), feats, 'margin-top: 14px', 32, '29.9%')
    dots = ''.join(f'<li style="display: flex; align-items: center; gap: 13px"><span aria-hidden="true" style="flex: none; width: 9px; height: 9px; border-radius: 50%; background: #C89B4E; border: 2px solid #E8D1A4"></span><span>{c}</span></li>' for c in COMMUNITIES)
    s += f'''
<section style="{WRAP}; padding: 0 37px 0 46px; margin-top: 7px">
<div class="mapc" style="position: relative; overflow: hidden; border-radius: 16px; min-height: 287px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; box-shadow: 0 1px 2px rgba(20, 40, 25, 0.20)">
<div class="map-bg" aria-hidden="true" style="position: absolute; top: 0; bottom: 0; right: 0; width: 24%; background: #E4E0C7"></div>
{img('who-map', 'Illustrated map of southeastern Ontario with pins on the communities IIPCT serves', 'position: absolute; top: 0; left: 21.7%; width: 61.6%; height: 100%; object-fit: cover; object-position: left center; mask-image: linear-gradient(90deg, #000 95%, transparent 100%)').replace('<img ', '<img class="map-img" ')}
<div class="map-curve" aria-hidden="true" style="position: absolute; top: -12%; bottom: -12%; left: -6%; width: 44%; border-radius: 0 50% 50% 0 / 0 50% 50% 0; background: #153526"></div>
<div class="map-txt" style="position: relative; width: 33%; min-width: min(320px, 100%); padding: 26px 0 26px 39px; display: flex; flex-direction: column; align-items: flex-start; gap: 9px">
{eyebrow('Our Service Area', '#E3BE74')}
{h2('Caring Across<br>Southeastern Ontario', 33, '#FFFFFF', 'font-weight: 500')}
{p('IIPCT provides primary care and wellness services to Indigenous people and communities across southeastern Ontario, including the communities and areas shown on the map.', 15.8, '#F4F1E8', 1.33, 'max-width: 372px; margin-top: 3px')}
{btn('Explore Our Service Area', '#', 'gold', None, True, 'sm', 'margin-top: 10px; padding: 0 22px; gap: 12px; min-height: 41px; font-size: 14px')}
</div>
<div class="map-list" style="position: absolute; top: 10px; bottom: 12px; right: 9px; width: 16.6%; min-width: 222px; padding: 12px 8px 10px 14px; border-radius: 12px; background: #FBF4E8; border: 1px solid #CDBF9C; box-shadow: 0 1px 3px rgba(20, 35, 20, 0.28); color: {INK}; display: flex; flex-direction: column; gap: 9px">
<h3 style="margin: 0; display: flex; align-items: center; gap: 7px; font-size: 11.4px; font-weight: 700; color: {HEAD}; white-space: nowrap">{pin_fill(15)}<span>Communities &amp; Areas We Serve</span></h3>
<ul style="margin: 0; padding: 0 0 0 4px; list-style: none; display: flex; flex-direction: column; gap: 2.6px; font-size: 12.7px; line-height: 1.2">{dots}</ul>
</div>
</div>
</section>
<section style="{WRAP}; padding: 15px 55px 0 72px; display: flex; flex-wrap: wrap; align-items: center; gap: 18px 30px">
<div style="flex: 0 0 372px; max-width: 100%; display: flex; flex-direction: column; align-items: flex-start; gap: 8px">
{eyebrow('Our People')}
{h2('Our Leadership &amp; Team', 31)}
{p('IIPCT is guided by Indigenous leadership and a skilled, multidisciplinary team of health and wellness professionals who work together to provide comprehensive, culturally safe care.', 14.6, INK, 1.3, 'max-width: 372px')}
{btn('Meet Our Team', '#team', 'primary', None, True, 'sm', 'margin-top: 4px; padding: 0 24px; gap: 14px')}
</div>
{vdiv('120px')}
<div style="flex: 1 1 560px; min-width: 0; padding: 14px 10px 16px 6px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05); display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px 0">
{pillar('people', RUSTI, 'Indigenous<br>Leadership', 'Community-grounded<br>direction and oversight.', True)}
{pillar('leaf', '#4F6B48', 'Interprofessional Team', 'A collaborative team<br>of primary care, allied<br>health, and wellness<br>providers.')}
{pillar('heart', RUSTI, 'Culturally Informed', 'Care that integrates<br>Indigenous knowledge,<br>values, and healing practices.')}
{pillar('sunrise', '#B5632F', 'Community Focused', 'Working in partnership<br>with individuals, families,<br>and communities.')}
</div>
</section>
<section id="team" style="{WRAP}; padding: 20px 55px 0 66px">
<div style="display: flex; align-items: center; gap: 26px">
{h2('Meet Our Team', 25.4)}
<span aria-hidden="true" style="flex: 1; height: 1px; background: {GOLDL}"></span>
{textlink('View the Full Team', '#', 14.4)}
</div>
<div style="margin-top: 13px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 22px">
{team_card('who-team-1', 'Family Physician')}{team_card('who-team-2', 'Nurse Practitioner')}{team_card('who-team-3', 'Registered Nurse')}{team_card('who-team-4', 'Social Worker')}
</div>
</section>
<section style="{WRAP}; padding: 18px 55px 0 57px">
{eyebrow('Our Clinics &amp; Teams', RUST, 'padding-left: 15px')}
<div style="margin-top: 10px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(480px, 100%), 1fr)); gap: 22px">
{clinic_card('who-clinic-tyendinaga', 'Tyendinaga Clinic', 'Our primary care clinic in the Tyendinaga Mohawk Territory provides comprehensive, Indigenous-centred care for individuals and families in the community and surrounding areas.')}
{clinic_card('who-clinic-shannonville', 'Shannonville Allied Health Team', 'A team-based clinic offering a range of allied health and wellness services, including mental health, chronic disease supports, health promotion, and more.')}
</div>
</section>
<div style="margin-top: 16px">'''
    right = (btn('Schedule Your Visit', 'Contact.dc.html', 'primary', 'calendar-check', True, 'md', 'border-color: #C8A15A; min-width: 226px')
             + btn('Book an Appointment', 'Contact.dc.html', 'light', 'calendar-dot', False, 'md', 'min-width: 236px; font-size: 15px'))
    s += rust_band('mail', 'Connect with IIPCT', 'Have questions about who we are, our team, or how to access care? We’re here to help.', right, 'padding-right: 100px', 14.3) + '</div>'
    s += footer()
    return 'IIPCT — Who We Are', s
