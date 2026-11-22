from lib import *

def service_card(photo, alt, icon, tone, title, text, items, cta):
    rows = ''.join(f'<li style="display: flex; align-items: center; gap: 14px; min-height: 27px">{ico(ic, 24, RUSTI, 1.35)}<span style="white-space: nowrap">{t}</span></li>' for ic, t in items)
    return f'''<article class="card" style="position: relative; display: flex; flex-direction: column; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div style="position: relative">
{img(photo, alt, 'width: 100%; aspect-ratio: 232 / 111; object-fit: cover; object-position: left bottom; border-radius: 13px 13px 0 0')}
{circ(icon, tone, 78, 38, 1.4, 'position: absolute; left: 14px; bottom: -33px; box-shadow: 0 0 0 5px #F7F0E3, 0 0 0 6px rgba(120, 92, 44, 0.30)')}
</div>
<div style="flex: 1; padding: 42px 9px 14px 9px; display: flex; flex-direction: column; gap: 9px">
<h3 style="margin: 0; padding-left: 14px; font-family: {SERIF}; font-weight: 700; font-size: 25.4px; line-height: 1.08; letter-spacing: -0.018em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; padding-left: 15px; font-size: 14.8px; line-height: 1.3; letter-spacing: -0.012em; color: {INK}">{text}</p>
<ul style="margin: 8px 0 0; padding: 10px 4px 10px 12px; list-style: none; border-radius: 10px; background: #FFFBF3; border: 1px solid #E6D8BD; display: flex; flex-direction: column; gap: 6px; font-size: 12.7px; letter-spacing: -0.012em; line-height: 1.2; color: {INK}">{rows}</ul>
<div style="margin-top: auto; padding: 10px 8px 0">{btn(cta, 'PrimaryCare.dc.html' if 'Primary Care' in cta else '#', 'primary', None, True, 'sm', 'width: 100%; gap: 14px; font-size: 12.4px; padding: 0 8px')}</div>
</div>
</article>'''

def step(icon, title, text, last=False):
    arrow = '' if last else f'<span class="hide-s" aria-hidden="true" style="flex: none; margin: 0 10px 0 auto">{ico("arrow", 24, "#93402B", 1.5)}</span>'
    return f'''<div style="flex: 1 1 250px; display: flex; align-items: center; gap: 18px; padding: 4px 0">
<span style="flex: none; width: 62px; height: 62px; border-radius: 50%; background: #E2E3CB; display: flex; align-items: center; justify-content: center">{ico(icon, 32, "#1F4A2B", 1.5)}</span>
<div style="display: flex; flex-direction: column; gap: 3px">
<h3 style="margin: 0; font-size: 16px; font-weight: 700; line-height: 1.2; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 12.3px; line-height: 1.34; color: {INK}">{text}</p>
</div>
{arrow}
</div>'''

def check_row(text):
    return f'<li style="display: flex; align-items: flex-start; gap: 13px">{ico("check", 20, "#1F4A2B", 2.1, "margin-top: 0")}<span>{text}</span></li>'

def path_row(icon, text):
    return f'<li style="display: flex; align-items: center; gap: 30px; min-height: 36px">{ico(icon, 34, RUSTI, 1.3)}<span>{text}</span></li>'

def benefit(text):
    return f'<li style="display: flex; align-items: center; gap: 15px; min-height: 30px">{ico("check-circle", 26, "#DCE6CF", 1.5)}<span>{text}</span></li>'

def page():
    buttons = btn('Schedule Your Visit', 'Contact.dc.html', 'primary', 'calendar-check') + btn('Book an Appointment', 'Contact.dc.html', 'outline', 'calendar-dot', False)
    s = header('services')
    extra = p('IIPCT brings together primary health care, mental wellness,<br>cultural services, and health supports to provide inclusive, holistic<br>care rooted in Indigenous ways of knowing, being, and healing.', 15.4, INK, 1.36, 'margin-top: 8px')
    s += hero('hero-services', 60.2, 344, 'Services',
              'Integrated, culturally grounded care for the<br>whole person, the family, and our communities.', buttons,
              h1_size=57, lead_size=20.6, lead_lh=1.3, lead_weight=500, extra=extra, pad='24px 0 34px 90px', gap=9, btn_mt=12, sq_mt=0)
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 40px; margin-top: 16px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 14px">
{service_card('svc-cultural', 'Smudge bowl with rising smoke', 'bowl', 'sage', 'Cultural Services', 'Land-based, traditional, and cultural<br>wellness supports that honour<br>Indigenous knowledge, language,<br>and ceremony.',
              [('sprout', 'Traditional healing supports'), ('tipi', 'Land-based and on-the-land care'), ('infinity', 'Cultural teachings and language'), ('people', 'Elder and Knowledge Keeper support')], 'Learn More About Cultural Services')}
{service_card('svc-primary', 'Stethoscope resting on a woven blanket', 'stethoscope', 'rust', 'Primary Medical Care', 'Comprehensive, inclusive primary<br>care for all ages, focused on prevention,<br>ongoing wellness, and the unique<br>health needs of Indigenous peoples.',
              [('heart', 'Primary and preventive care'), ('syringe', 'Chronic condition management'), ('people', 'Health screenings and immunizations'), ('kit', 'Care for all ages, from children to Elders')], 'Learn More About Primary Care')}
{service_card('svc-mental', 'Sage bundles and green leaves on bark', 'lotus', 'sage', 'Mental Health Services', 'Culturally safe, trauma-informed<br>mental health and addiction supports<br>that honour lived experience, resilience,<br>and community strengths.',
              [('chat-heart', 'Counselling and therapy'), ('sprout', 'Addiction and substance use supports'), ('people', 'Crisis and short-term supports'), ('lotus', 'Culturally grounded wellness approaches')], 'Learn More About Mental Health')}
{service_card('svc-support', 'Canoes on a lakeshore at sunset', 'people', 'gold', 'Health Support Services', 'Integrated supports to help you<br>and your family stay well, navigate care,<br>and access the right resources<br>at the right time.',
              [('hand-heart', 'Care navigation and system support'), ('apple', 'Health education and wellness programs'), ('house', 'Social and community resource supports'), ('heart', 'Practical supports for you and your family')], 'Learn More About Health Supports')}
</div>
</section>
<section style="position: relative; {WRAP}; padding: 24px 58px 0 61px">
{branch(96, '#B5BFA6', 0.5, 'left: -34px; bottom: -70px; transform: rotate(12deg)')}
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 36px; padding-left: 11px">
<div style="display: flex; flex-direction: column; gap: 0">{h2('How Care Works', 32.4)}<span style="display: block; margin-top: -1px">{SQUIGGLE.replace('width="160" height="17"', 'width="120" height="13"')}</span></div>
{vdiv('54px')}
{p('A team-based, whole-person approach that brings together medical, mental health, cultural,<br>and support services — so you can receive connected, respectful, and community-focused care.', 14.3, INK, 1.32, 'flex: 1 1 500px')}
</div>
<div style="position: relative; margin-top: 15px; padding: 12px 36px 12px 62px; border-radius: 14px; background: #F1ECD9; border: 1px solid #D8D2B4; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 8px">
{step('calendar', '1. Connect', 'Book a visit, self-refer,<br>or be referred by a partner.')}
{step('people', '2. Plan Together', 'Meet with our team to talk<br>about your needs and goals.')}
{step('leaf', '3. Receive Care', 'Access the right services<br>and supports, in a culturally<br>safe space.')}
{step('cycle', '4. Ongoing Support', 'Stay connected for follow-up,<br>wellness, and long-term care<br>as needed.', True)}
</div>
</section>
<section style="position: relative; {WRAP}; padding: 22px 60px 0 68px">
{branch(118, '#B5BFA6', 0.5, 'right: -30px; top: -30px; transform: rotate(-10deg)')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: stretch; gap: 18px 36px">
<div class="fbs mh-s" style="flex: 0 0 284px; position: relative; min-height: 176px">{img('svc-drum', 'Hand drum and drumstick', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 14px')}</div>
<div style="flex: 1 1 340px; min-width: 0; padding-top: 4px; display: flex; flex-direction: column; gap: 12px">
{h2('What to Expect', 28.4, HEAD, '', 'h2')}
<ul style="margin: 0; padding: 0 0 0 12px; list-style: none; display: flex; flex-direction: column; gap: 9px; font-size: 13.5px; line-height: 1.3; color: {INK}">
{check_row('A welcoming, respectful, and culturally safe space')}
{check_row('A team that listens and works with you')}
{check_row('Care that addresses your whole health —<br>physical, mental, emotional, and spiritual')}
{check_row('Support for you, your family, and your community')}
</ul>
</div>
{vdiv('120px', GOLDL, 'margin: 26px 0 10px')}
<div style="flex: 1.25 1 380px; min-width: 0; padding: 4px 0 0 34px; display: flex; flex-direction: column; gap: 6px">
{h2('Referral &amp; Support Pathway', 28.4, HEAD, 'letter-spacing: 0', 'h2')}
{p('Access care in a way that works for you. You can:', 14, INK, 1.3, 'padding-left: 4px')}
<ul style="margin: 4px 0 0; padding: 0 0 0 12px; list-style: none; display: flex; flex-direction: column; gap: 5px; font-size: 13.4px; line-height: 1.3; color: {INK}">
{path_row('calendar', 'Self-refer by booking a visit with our team')}
{path_row('people', 'Be referred by a health care provider, community partner,<br>or support service')}
{path_row('phone', 'Contact us if you’re not sure where to start — we can help<br>guide you to the right care and supports')}
</ul>
</div>
</div>
</section>'''
    cols = (f'<ul style="margin: 0; padding: 0; list-style: none; flex: 1.25 1 300px; display: flex; flex-direction: column; gap: 3px">{benefit("Whole-person, holistic care")}{benefit("Culturally grounded and trauma-informed supports")}{benefit("Easier access to the right services")}</ul>'
            f'<ul style="margin: 0; padding: 0; list-style: none; flex: 1 1 230px; display: flex; flex-direction: column; gap: 3px">{benefit("A care team that communicates and<br>plans with you")}{benefit("Better continuity and follow-up")}{benefit("Care that strengthens individual, family,<br>and community wellness")}</ul>')
    text = (p('Our integrated approach means you don’t have to navigate care<br>alone. We work together across services to provide:', 15.4, '#F4F1E8', 1.3)
            + f'<div style="margin-top: 7px; padding-left: 14px; display: flex; flex-wrap: wrap; gap: 4px 22px; font-size: 13.6px; letter-spacing: -0.01em; line-height: 1.25; color: #F4F1E8">{cols}</div>')
    s += green_band('svc-lake', None, 'Coordinated Care Benefits', text, '<span style="flex: 0 0 26px"></span>', 'margin-top: 20px; padding: 0 37px 0 41px', '40%', 190, 32)
    s += f'''
<section style="{WRAP}; padding: 19px 92px 0 93px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 40px">
{h2('Need Help or Have Questions?', 30.4)}
{vdiv('40px')}
{p('We’re here to support you. Reach out to learn more about our services,<br>get connected to care, or find the right supports for you or your family.', 13.8, INK, 1.3, 'flex: 1 1 380px')}
{btn('Contact Us', 'Contact.dc.html', 'primary', 'phone', True, 'md', 'min-width: 200px; font-size: 13.6px; gap: 14px')}
</section>
<div style="margin-top: 20px">{newsletter()}</div>'''
    s += footer()
    return 'IIPCT — Services', s
