"""Contact Us. Every phone number, email, address, hour and extension comes from facts.py (IIPCT's current contact page)."""
from lib import *
from facts import BY_KEY, WAITLIST

SMALL = f'font-size: 13.2px; line-height: 1.35; color: {INK}'

def out_btn(label, href, aria):
    """Button-style link to another website (opens in a new tab), in the 'sage' look of btn()."""
    return (f'<a class="btn bo" href="{href}" aria-label="{aria}" style="display: inline-flex; align-items: center; justify-content: center; gap: 9px; min-height: 36px; padding: 0 15px; '
            f'border-radius: 9px; font-size: 13px; font-weight: 600; line-height: 1.2; text-align: center; text-decoration: none; background: #FAF6EA; color: #133019; '
            f'border: 1.5px solid #7E9471; box-shadow: 0 2px 4px rgba(40, 30, 10, 0.07)">{ico("map", 16, "currentColor", 1.8)}<span>{label}</span>{ico("external", 14, "currentColor", 1.9)}</a>')

def hours_table(loc):
    rows = ''.join(f'<span style="font-weight: 600; color: {HEAD}">{d}</span><span style="white-space: nowrap">{t}</span>' for d, t in hours_rows(loc))
    return f'<div style="display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; padding: 0 0 0 33px; font-size: 12.8px; line-height: 1.35; color: {INK}">{rows}</div>'

def extensions(loc):
    groups = ''
    for heading, people in EXTENSIONS[loc['key']]:
        names = ''.join(f'<li style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 2px 10px"><span>{n}</span>'
                        + (f'<span style="font-weight: 600; color: {HEAD}; white-space: nowrap">ext. {x}</span>' if x else '') + '</li>' for n, x in people)
        groups += (f'<div style="display: flex; flex-direction: column; gap: 3px"><span style="font-size: 12.4px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: {RUST}">{heading}</span>'
                   f'<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 3px">{names}</ul></div>')
    return f'''<details class="xt" style="margin-top: 4px; border-top: 1px solid #E6D9BF">
<summary style="display: flex; align-items: center; justify-content: space-between; gap: 10px; min-height: 44px; cursor: pointer; font-size: 13.4px; font-weight: 700; color: {HEAD}">
<span>Staff and extensions</span>{ico('chev-down', 17, '#A3301C', 2.2)}</summary>
<div style="display: flex; flex-direction: column; gap: 10px; padding: 2px 0 8px; {SMALL}">
<p style="margin: 0">Call {MAIN_PHONE}, press {loc['option']}, then ask reception for the person you need. Their extension is beside their name.</p>
{groups}
</div>
</details>'''

def location_card(loc, crop):
    row = lambda ic, html: f'<li style="display: flex; align-items: flex-start; gap: 14px">{ico(ic, 19, "#A04A32", 1.6, "margin-top: 1px")}<span style="min-width: 0">{html}</span></li>'
    fax = row('doc', f'Fax {loc["fax"]}') if loc.get('fax') else ''
    units = ''
    if loc.get('units'):
        units = ('<ul style="margin: 2px 0 0; padding: 0 0 0 33px; list-style: none; display: flex; flex-direction: column; gap: 3px; font-size: 12.8px; line-height: 1.35">'
                 + ''.join(f'<li>{u}</li>' for u in loc['units']) + '</ul>')
    return f'''<article id="{loc['key']}" style="scroll-margin-top: 16px; display: flex; flex-direction: column; padding: 0 0 16px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: {SHADOW}">
{img(crop, '', 'width: 100%; aspect-ratio: 188 / 60; object-fit: cover; border-radius: 13px 13px 0 0')}
<div style="flex: 1; padding: 12px 18px 0 20px; display: flex; flex-direction: column; gap: 10px">
<h3 style="margin: 0; display: flex; align-items: flex-start; gap: 10px; font-family: {SERIF}; font-weight: 700; font-size: 19.4px; line-height: 1.12; letter-spacing: -0.02em; color: {HEAD}">{pin_fill(22, style='margin-top: 1px')}<span>{loc['name']}</span></h3>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; {SMALL}">
{row('pin', address(loc))}
{row('phone', f'<a href="tel:{MAIN_TEL}" style="color: {INK}; font-weight: 700; text-decoration: none">{MAIN_PHONE}</a>, press {loc["option"]}')}
{fax}
{row('mail', f'<a href="mailto:{loc["email"]}" style="color: {INK}; text-decoration: underline; text-underline-offset: 3px; overflow-wrap: anywhere">{loc["email"]}</a>')}
{row('clock', f'<span style="display: block; font-weight: 700; color: {HEAD}">Hours</span>')}
</ul>
{hours_table(loc)}
{units}
{extensions(loc)}
<div style="padding-top: 4px">{out_btn('Open in Google Maps', loc['map_url'], f'Open the {loc["name"]} in Google Maps (opens in a new tab)')}</div>
</div>
</article>'''

def faq(q, a):
    return (f'<li><details class="faq" style="border-radius: 10px; border: 1px solid #DCCBAB; background: #FFFCF6">'
            f'<summary style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 44px; padding: 6px 16px 6px 18px; cursor: pointer; '
            f'font-size: 13.6px; font-weight: 600; line-height: 1.3; color: {HEAD}"><span>{q}</span>{ico("chev-down", 17, "#A3301C", 2.2)}</summary>'
            f'<div style="padding: 0 18px 14px; font-size: 13.6px; line-height: 1.5; color: {INK}">{a}</div></details></li>')

def emails():
    """The location emails, grouped by address, as the contact page gives them."""
    by = {}
    for l in LOCATIONS:
        by.setdefault(l['email'], []).append(l['short'])
    rows = ''
    for addr, places in by.items():
        who = places[0] if len(places) == 1 else ', '.join(places[:-1]) + ' and ' + places[-1]
        rows += (f'<li style="display: flex; flex-direction: column; gap: 1px; padding: 8px 0; border-top: 1px solid #E6D9BF">'
                 f'<span style="font-size: 12.6px; font-weight: 700; color: {MUTED}">{who}</span>'
                 f'<a href="mailto:{addr}" style="font-size: 14.4px; font-weight: 700; color: {HEAD}; text-decoration: underline; text-underline-offset: 3px; overflow-wrap: anywhere">{addr}</a></li>')
    return f'<ul style="margin: 0; padding: 0; list-style: none">{rows}</ul>'

def page():
    buttons = (btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check')
               + btn(f'Call {MAIN_PHONE}', 'tel:' + MAIN_TEL, 'outline', 'phone', False))
    s = header('contact')
    s += hero(None, 58.4, 356, 'We’re Here to Support<br>Your Care Journey',
              f'One phone number reaches all {len(LOCATIONS)} of our locations. Call, then press the number for the location you need. You can also email the location directly.',
              buttons, eyebrow_txt='Contact Us', h1_size=45, lead_size=16.4, lead_lh=1.34, lead_w=520, pad='24px 0 40px 84px', gap=10, btn_mt=6, sq_mt=-1, obj='center 80%',
              site_photo='contact/deseronto-clinic.jpg', photo_wh=(872, 606), narrow_pos='50% 85%',
              photo_alt=f'The Deseronto Clinic at {BY_KEY["deseronto"]["street"]}: a one-storey building of stone and blue siding, with a ramp to the front door')
    w = WAITLIST
    wl = BY_KEY[w['location']]
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 40px; margin-top: 16px">
{branch(110, '#B5BFA6', 0.5, 'right: -30px; bottom: -44px; transform: rotate(-12deg)')}
<div style="position: relative; overflow: hidden; border-radius: 16px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: {SHADOW}; display: flex; flex-wrap: wrap; align-items: stretch">
<div class="pads cu-col" style="flex: 1 1 440px; min-width: 0; padding: 20px 32px 22px 32px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 20px">
{circ('phone', 'rust', 66, 32, 1.5)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('Call Us', 28)}
{p('One number for every location. After you call, press the number for the location you need.', 13.8, INK, 1.35)}
</div>
</div>
<a class="fl" href="tel:{MAIN_TEL}" style="display: inline-flex; align-items: center; gap: 12px; align-self: flex-start; min-height: 44px; font-family: {SERIF}; font-size: 30px; font-weight: 700; letter-spacing: -0.01em; color: {HEAD}; text-decoration: none">{ico('phone', 26, '#A04A32', 1.7)}<span>{MAIN_PHONE}</span></a>
{call_list(size=14)}
<p style="margin: 4px 0 0; font-size: 13.8px; line-height: 1.45; color: {INK}">Hours differ by location. <a href="#locations" style="font-weight: 600">See each location’s hours</a>.</p>
</div>
{vdiv('200px', GOLDL, 'margin: 26px 0 22px')}
<div class="pads cu-col" style="position: relative; flex: 1 1 440px; min-width: 0; padding: 20px 30px 22px 36px; display: flex; flex-direction: column; gap: 12px">
<div style="position: relative; display: flex; align-items: center; gap: 20px">
{circ('mail', 'sage', 66, 32, 1.5)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('Email Us', 28)}
{p(f'For general questions, write to <a href="mailto:{GENERAL_EMAIL}" style="font-weight: 700; color: {HEAD}">{GENERAL_EMAIL}</a>. Each location also has its own email.', 13.8, INK, 1.4)}
</div>
</div>
{emails()}
{note('info', 'Email is not for medical questions or emergencies', f'For a health question, call your clinic at {MAIN_PHONE}. In an emergency, call 911.', 'gold', 'margin-top: 2px')}
<p style="margin: 0; font-size: 13.8px; line-height: 1.45; color: {INK}">Registered patients can book appointments online. {ext('Book online', BOOKING_URL, 13.8)}</p>
<div style="position: relative; margin-top: 2px">{social_row(label='Follow IIPCT')}</div>
</div>
</div>
</section>
<section id="locations" style="position: relative; scroll-margin-top: 16px; {WRAP}; padding: 26px 44px 0 50px">
{pines(PINES_R, 200, 78, '#B4BF9F', 0.7, 'right: 46px; top: 26px')}
<div class="p0" style="position: relative; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 42px; padding-left: 22px">
<div style="display: flex; flex-direction: column; gap: 4px">{eyebrow('Our Locations')}{h2(f'Find Your Location', 39)}</div>
{vdiv('54px')}
{p('Each location has its own hours and email. Open “Staff and extensions” to see who works there.', 15.4, INK, 1.4, 'flex: 1 1 360px')}
</div>
<div class="lcg" style="position: relative; margin-top: 17px; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; align-items: start">
{''.join(location_card(l, c) for l, c in zip(LOCATIONS, ['con-tyendinaga', 'con-kingston', 'con-bancroft', 'con-deseronto', 'con-shannonville']))}
</div>
</section>
<section style="{WRAP}; padding: 26px 55px 0 53px; display: flex; flex-wrap: wrap; align-items: stretch; gap: 20px 26px">
<div class="locm" style="position: relative; overflow: hidden; flex: 1.5 1 560px; min-width: 0; min-height: 300px; border-radius: 16px; background: #EFEAD6; border: 1px solid #D3CEAE">
{photo('contact/service-area-map.png', 'Map of the regions IIPCT serves in southeastern Ontario: Rural Hastings; Rural Frontenac, Lennox and Addington; Lanark, Leeds and Grenville; Quinte; and Kingston', 'position: absolute; top: 0; right: 0; width: 52%; height: 100%; padding: 14px; object-fit: contain', 'locm-img', 640, 471)}
{pines(PINES_L, 200, 128, '#B4BF9F', 0.6, 'left: -4px; bottom: 0')}
<div class="locm-txt" style="position: relative; width: 48%; min-width: min(300px, 100%); padding: 22px 0 22px 24px; display: flex; align-items: flex-start; gap: 20px">
{circ('map', 'rust', 62, 30, 1.6)}
<div style="display: flex; flex-direction: column; align-items: flex-start; gap: 13px; padding-top: 8px">
{h2('Where We Serve', 26.4)}
{p('Our locations serve Indigenous people and their families across these regions of southeastern Ontario.', 14.4, INK, 1.42, 'max-width: 270px')}
{btn('See All Locations', '#locations', 'outline', None, True, 'sm', 'margin-top: 4px; padding: 0 16px; gap: 11px; font-size: 12.8px')}
</div>
</div>
</div>
{vdiv('200px', '#E6D6BC')}
<div style="flex: 1 1 400px; min-width: 0; display: flex; flex-direction: column; gap: 10px; padding-left: 10px">
<div style="display: flex; align-items: center; gap: 22px">
{circ('question', 'rust', 54, 28, 1.6)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('Questions and Answers', 24.6)}
{p('Tap a question to see the answer.', 13.4, INK, 1.3)}
</div>
</div>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px">
{faq('How do I book an appointment?', f'If you are a registered patient, you can book online on our <a href="{BOOKING}">Schedule Your Visit</a> page. You can also call {MAIN_PHONE} and press the number for your location.')}
{faq('Is IIPCT taking new patients?', f'The {wl["name"]} is accepting patients for its waitlist. To join, call {MAIN_PHONE}, press {wl["option"]}, and speak to Reception, {w["when"]}. You must {w["must"][0].lower() + w["must"][1:]}')}
{faq('Who can get care at IIPCT?', 'We focus on people who identify as Indigenous, and their families, in our regions. All our services are status blind: Status and Non-Status people are welcome.')}
{faq('What services does IIPCT offer?', f'Four programs: Cultural Services, Primary Medical Care, Mental Health Services and Health Support Services. <a href="Services.dc.html">See all our services</a>.')}
</ul>
</div>
</section>
<div style="margin-top: 30px">{newsletter()}</div>'''
    s += footer()
    return 'IIPCT — Contact Us', s
