from lib import *

def theme_card(icon, tone, title, text):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 20px; min-height: 148px; padding: 15px 8px 44px 18px; border-radius: 14px; {CARD}">
{circ(icon, tone, 74, 39, 1.35)}
<div style="display: flex; flex-direction: column; gap: 9px; padding-top: 3px">
<h3 class="nw" style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 18.6px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; font-size: 13.8px; line-height: 1.42; letter-spacing: -0.014em; color: {INK}">{text}</p>
</div>
{round_arrow(25, 'arrow', title, '#', 'position: absolute; right: 12px; bottom: 11px')}
</div>'''

def milestone(icon, color, title, text, first=False):
    bl = '' if first else f'border-left: 1px solid {GOLDL}; '
    return f'''<div style="{bl}flex: 1 1 280px; display: flex; align-items: flex-start; gap: 22px; padding: 4px 10px 4px 36px">
{ico(icon, 52, color, 1.15, 'margin-top: 2px')}
<div style="display: flex; flex-direction: column; gap: 5px">
<h3 class="nw" style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 16.6px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; font-size: 13.2px; line-height: 1.4; color: {INK}">{text}</p>
</div>
</div>'''

def check(text):
    return f'<li style="display: flex; align-items: center; gap: 14px">{ico("check-circle", 25, "#EAF0E0", 1.5)}<span>{text}</span></li>'

def page():
    buttons = (btn('Learn About Our BPSO Work', '#overview', 'primary', 'calendar-check', True, 'md', 'padding: 0 22px; gap: 10px')
               + btn('Connect with Our Team', 'Contact.dc.html', 'outline', 'calendar-dot', True, 'md', 'padding: 0 22px; gap: 10px'))
    s = header('bpso')
    s += hero('hero-bpso', 55.4, 358, 'Best Practice Spotlight<br>Organization (BPSO)',
              'IIPCT’s commitment to evidence-informed care and<br>continuous quality improvement to achieve better<br>health and wellness for the people and communities we serve.', buttons,
              h1_size=47.6, lead_size=19, lead_lh=1.4, pad='40px 0 40px 84px', gap=12, btn_mt=10, sq_mt=2, obj='center center')
    body = (p('A Best Practice Spotlight Organization (BPSO) is a health care organization that partners in a province-wide initiative to put evidence-based best practices into everyday care.', 15.5, INK, 1.4, 'max-width: 470px; padding-left: 4px; margin-top: 4px')
            + p('In simple terms, it means we use the best available knowledge, work with our teams and community, and keep improving care to support better health and wellness for our patients and families.', 15.5, INK, 1.4, 'max-width: 500px; padding-left: 4px; margin-top: 4px'))
    feats = feature_list([('heart', 'Evidence-Informed Care', 'Bringing proven, up-to-date practices<br>into everyday care.'),
                          ('people', 'Better Experiences', 'More supportive, culturally safe, and<br>person-centred care.'),
                          ('feather', 'Continuous Improvement', 'Learning, measuring, and making meaningful<br>changes together.')], 50, 15.8, 26, 13)
    s += '<div id="overview">' + split_section(arc_photo('bpso-smudge', 'Smudge bowl with smoke rising, resting on a rock beside sweetgrass', 'flex: 1; min-height: 288px', '58% 62%', '34% 40%'),
                       'Overview', 'What is a BPSO?', body,
                       btn('About the BPSO Initiative at IIPCT', '#', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 16px; font-size: 14.8px; min-height: 40px'), feats, 'margin-top: 20px', 32.4, '31.7%', '30.4%') + '</div>'
    text = p('IIPCT is proud to be a Best Practice Spotlight Organization in partnership with the Registered Nurses’ Association of Ontario (RNAO), a recognized leader in evidence-based practice and quality improvement in health care.', 14.2, '#F4F1E8', 1.42, 'max-width: 426px')
    right = (f'<div class="gb-cta" style="position: relative; flex: 0 1 auto; display: flex; align-items: center; gap: 24px; padding: 20px 18px 20px 0">'
             f'{vdiv("120px", "#B8935A", "align-self: center; height: 120px")}'
             f'<div style="display: flex; flex-direction: column; gap: 12px">{eyebrow("Partnership Highlights", "#E3BE74", "font-size: 12.2px")}'
             f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 12.6px; color: #F4F1E8">'
             f'{check("Access to evidence-based best practices")}{check("Guidance, tools, and implementation support")}{check("Connection to a province-wide learning network")}</ul></div></div>')
    s += green_band('bpso-lake', 'Our Partnership', 'A Valued Partnership with RNAO', text, right, 'margin-top: 22px; padding: 0 58px 0 62px', '36%', 176, 28.2, '16px 12px 17px 46px')
    s += f'''
<section style="{WRAP}; padding: 26px 52px 0 55px">
<div style="padding-left: 18px; display: flex; flex-direction: column; gap: 6px">
{eyebrow('Our Focus')}
{h2('Best-Practice Themes at IIPCT', 34.4)}
{p('We bring evidence-informed best practices to life in ways that reflect our Indigenous-centred approach to primary care. Our BPSO work focuses on key themes that support high-quality, culturally safe, and holistic care for our patients, families, and communities.', 15.2, INK, 1.42, 'max-width: 1180px; margin-top: 6px')}
</div>
<div style="margin-top: 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 14px">
{theme_card('people', 'sage', 'Person-Centred Care', 'Respecting each person’s<br>unique needs, strengths,<br>values, and cultural identity.')}
{theme_card('stethoscope', 'rust', 'Clinical Excellence', 'Using the best available<br>evidence and guidelines to<br>deliver safe, high-quality care.')}
{theme_card('book', 'sage', 'Team Learning', 'Building knowledge, skills,<br>and shared practice across<br>our interprofessional team.')}
{theme_card('chart', 'gold', 'Health Outcomes', 'Improving the health and<br>wellness of the people and<br>communities we serve.')}
</div>
</section>
<section style="position: relative; margin-top: 24px">
<svg aria-hidden="true" viewBox="0 0 1440 240" preserveAspectRatio="xMaxYMin slice" style="position: absolute; left: 0; top: 0; width: 100%; height: 150px">
<path d="M560 150 C 700 60 860 30 1010 70 C 1120 20 1300 10 1440 60 L 1440 150 Z" fill="#EEEFDD"></path>
<path d="M640 150 C 780 96 900 84 1040 108 C 1180 70 1320 66 1440 96 L 1440 150 Z" fill="#E2E6CF"></path>
</svg>
{pines([(26, 52, 30, 0.6), (64, 78, 42, 0.8), (100, 44, 26, 0.5)], 130, 78, '#AEBB9B', 0.75, 'left: 46%; top: 72px')}
{pines(PINES_R, 200, 112, '#AEBB9B', 0.8, 'right: 6px; top: 38px')}
<div style="position: relative; {WRAP}; padding: 8px 32px 0 36px">
<div style="padding-left: 37px; display: flex; flex-direction: column; gap: 6px">
{eyebrow('Our Impact')}
{h2('Our Impact &amp; Milestones', 37.6)}
{p('Our BPSO journey strengthens the care we provide today and builds a stronger, healthier tomorrow for the people and communities we serve.', 16, INK, 1.4, 'max-width: 580px; margin-top: 8px')}
</div>
<div style="margin-top: 18px; padding: 22px 16px 22px 30px; border-radius: 14px; background: #FCF6EB; border: 1px solid {LINE}; box-shadow: {SHADOW}; display: flex; flex-wrap: wrap; align-items: stretch; gap: 18px 0">
{milestone('award', '#B5792E', 'BPSO Designation', 'Proudly designated as a<br>Best Practice Spotlight<br>Organization (BPSO).', True)}
{milestone('people', '#B5792E', 'Best Practices in Action', 'Implementing<br>RNAO best practice<br>guidelines in our clinical work.')}
{milestone('sprout', '#2F6A3C', 'Improved Care &amp; Experience', 'Supporting positive changes<br>in care, team practice,<br>and patient experience.')}
{milestone('cycle', '#B5792E', 'Ongoing Growth', 'Monitoring, learning, and<br>continually improving<br>together.')}
</div>
</div>
</section>
<div style="margin-top: 26px">'''
    right = (btn('Learn More About BPSO', '#overview', 'light', None, True, 'md', 'padding: 0 22px; gap: 14px; font-size: 13.6px; min-height: 39px')
             + btn('Connect with Our Team', 'Contact.dc.html', 'primary', None, True, 'md', 'padding: 0 24px; gap: 14px; font-size: 13.6px; min-height: 39px; border-color: #C8A15A'))
    band = rust_band('mail', 'Learn More or Connect with Us', 'Want to know more about IIPCT’s BPSO work, our focus areas, or how it supports care in our community? We’re happy to share, connect, and explore together.', right, 'padding: 18px 120px 18px 126px', 14.2)
    band = band.replace(ico('mail', 36, '#FFFFFF', 1.3, 'position: relative'), '')
    band = band.replace('font-weight: 500; font-size: 24.8px;', 'font-weight: 500; font-size: 29.6px;')
    s += band + '</div>'
    s += footer()
    return 'IIPCT — BPSO', s
