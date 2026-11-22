"""Services: the four service areas as the old site (iipct.org/services/) describes them, and how to get care.
The claim-by-claim sources are in the builder's notes."""
from lib import *
import lib
from p_sub import nl_band

PHONE = getattr(lib, 'MAIN_PHONE', None) or CLINICS[0][2]          # main line, from lib (never typed here)
TEL = 'tel:' + (getattr(lib, 'MAIN_TEL', None) or CLINICS[0][3])

def service_card(pic, icon, tone, title, text, items, cta, href):
    rows = ''.join(f'<li style="display: flex; align-items: center; gap: 14px; min-height: 27px">{ico(ic, 24, RUSTI, 1.35)}<span style="white-space: nowrap">{t}</span></li>' for ic, t in items)
    return f'''<article class="card" style="position: relative; display: flex; flex-direction: column; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div style="position: relative">
{pic}
{circ(icon, tone, 78, 38, 1.4, 'position: absolute; left: 14px; bottom: -33px; box-shadow: 0 0 0 5px #F7F0E3, 0 0 0 6px rgba(120, 92, 44, 0.30)')}
</div>
<div style="flex: 1; padding: 42px 9px 14px 9px; display: flex; flex-direction: column; gap: 9px">
<h3 style="margin: 0; padding-left: 14px; font-family: {SERIF}; font-weight: 700; font-size: 25.4px; line-height: 1.08; letter-spacing: -0.018em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; padding-left: 15px; font-size: 14.8px; line-height: 1.3; letter-spacing: -0.012em; color: {INK}">{text}</p>
<ul style="margin: 8px 0 0; padding: 10px 4px 10px 12px; list-style: none; border-radius: 10px; background: #FFFBF3; border: 1px solid #E6D8BD; display: flex; flex-direction: column; gap: 6px; font-size: 12.7px; letter-spacing: -0.012em; line-height: 1.2; color: {INK}">{rows}</ul>
<div style="margin-top: auto; padding: 10px 8px 0">{btn(cta, href, 'primary', None, True, 'sm', 'width: 100%; min-height: 40px; gap: 14px; font-size: 12.4px; padding: 0 8px')}</div>
</div>
</article>'''

CARD_IMG = 'width: 100%; height: auto; aspect-ratio: 232 / 111; object-fit: cover; object-position: left bottom; border-radius: 13px 13px 0 0'

def area(aid, icon, tone, title, lead, body, branch_style):
    """One service area in full, with the id the cards above link to."""
    return f'''
<section id="{aid}" style="position: relative; {WRAP}; padding: 40px 58px 0 61px">
{branch(96, '#B5BFA6', 0.5, branch_style)}
<div style="position: relative; display: flex; align-items: center; gap: 16px">{circ(icon, tone, 58, 30, 1.4)}
<div style="min-width: 0; display: flex; flex-direction: column; gap: 5px">{h2(title, 30.4)}{p(lead, 14.8, MUTED, 1.4)}</div></div>
<div style="position: relative; margin-top: 16px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(440px, 100%), 1fr)); gap: 16px; align-items: start">{body}</div>
</section>'''

def contact_row(name, role, ext_, email):
    link = (f'display: inline-flex; align-items: center; gap: 8px; min-height: 40px; font-size: 14px; font-weight: 600; color: {RUST}; text-decoration: none')
    return (f'<li style="display: flex; flex-wrap: wrap; align-items: center; gap: 2px 22px; padding: 8px 0; border-top: 1px solid #E6D9BF">'
            f'<span style="flex: 1 1 200px; min-width: 0; display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14.6px; font-weight: 700; color: {HEAD}">{name}</span>'
            f'<span style="font-size: 13.4px; color: {MUTED}">{role}</span></span>'
            f'<a class="tl" href="{TEL}" style="{link}; white-space: nowrap">{ico("phone", 16, RUST, 1.8)}<span>{PHONE} ext. {ext_}</span></a>'
            f'<a class="tl" href="mailto:{email}" style="{link}">{ico("mail", 16, RUST, 1.8)}<span>{email}</span></a></li>')

def start_card(icon, tone, title, text, cta):
    """Text on the left, its button on the right (the immunization schedule panel's pattern); the button drops below on narrow screens."""
    return panel(f'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px 40px">'
                 f'<div style="flex: 1 1 min(420px, 100%); min-width: 0"><div style="display: flex; align-items: center; gap: 14px">{circ(icon, tone, 52, 27, 1.5)}{h3(title, 21)}</div>'
                 + prose(text, size=14.4, style='margin-top: 12px; max-width: 760px') + f'</div><div style="flex: none; max-width: 100%">{cta}</div></div>', '', '22px 24px 24px')

def page():
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Contact a Clinic', 'Contact.dc.html', 'outline', 'phone', False)
    s = header('services')
    extra = p('Our services draw equally from both Indigenous and mainstream ways of knowing and being.', 15.4, INK, 1.36, 'margin-top: 8px; max-width: 470px')
    top = hero('hero-services', 60.2, 344, 'Services', 'Explore four key programs supporting health, wellness, and community care.', buttons,
               h1_size=57, lead_size=20.6, lead_w=470, lead_lh=1.3, lead_weight=500, extra=extra, pad='24px 0 34px 90px', gap=9, btn_mt=12, sq_mt=0, obj='center 30%')
    # lib.hero() takes only mock-up crops: put IIPCT's own photograph in place of the stand-in (people who are not IIPCT's)
    stand_in = f'<img class="hero-photo" src="{BLOB["hero-services"]}" alt=""'
    assert stand_in in top, 'lib.hero() markup changed: update p_services.page()'
    s += top.replace(stand_in, '<img class="hero-photo" src="/_site/services/clinic-sign.jpg" alt="An IIPCT clinic building with the Tsi Kanonhkhwatsheríyo sign and turtle logo"')

    cards = [
        service_card(photo('services/traditional-medicines.jpg', 'A feather, an abalone shell holding sage, cedar and braided sweetgrass on a hide', CARD_IMG, w=582, h=278),
                     'bowl', 'sage', 'Cultural Services', 'Traditional healing, spiritual support and cultural learning, on a path of holistic wellness.',
                     [('sprout', 'Traditional healing'), ('people', 'Seers and knowledge holders'), ('infinity', 'Language, culture and identity'), ('leaf', 'Cultural learning')],
                     'Learn More About Cultural Services', '#cultural'),
        service_card(img('svc-primary', 'Stethoscope resting on a woven blanket', CARD_IMG), 'stethoscope', 'rust', 'Primary Medical Care',
                     'Physicians, nurse practitioners and nurses, with connections to partner supports such as midwifery.',
                     [('heart', 'Chronic disease care'), ('bolt', 'Same-day acute care'), ('syringe', 'Immunization and screening'), ('baby', 'Well baby and well child visits')],
                     'Learn More About Primary Care', 'PrimaryCare.dc.html'),
        service_card(img('svc-mental', 'Sage bundles and green leaves on bark', CARD_IMG), 'lotus', 'sage', 'Mental Health Services',
                     'Short-term support for adults 18 and older who receive care at IIPCT.',
                     [('chat-heart', 'Assessment and plan of care'), ('route', 'Resource connections and referrals'), ('people', 'Group workshops and programs'), ('heart', 'Pre- and post-natal linkage')],
                     'Learn More About Mental Health', '#mental-health'),
        service_card(img('svc-support', 'Canoes on a lakeshore at sunset', CARD_IMG), 'people', 'gold', 'Health Support Services',
                     'Care coordination across health and community systems, with ongoing programs that promote wellness.',
                     [('doc', 'Help with forms'), ('hand-heart', 'Help with funding programs'), ('house', 'Housing and food security'), ('leaf', 'Quit smoking (STOP program)')],
                     'Learn More About Health Supports', '#health-support'),
    ]
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 40px; margin-top: 16px">
<div class="g-cards gt2" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 14px">
{''.join(cards)}
</div>
</section>'''

    # ---- Cultural Services
    cultural = (panel(prose('Our Cultural Services blend traditional healing, spiritual support and cultural learning to guide clients on a path of holistic wellness.',
                            'Our Traditional Healing Coordinator connects clients with seers and knowledge holders from Rotinonhsyonni (Haudenosaunee) and other First Nations. '
                            'This makes sure medicines and guidance are used safely, whether alone or alongside pharmaceuticals.',
                            size=14.8, style='margin-bottom: 10px'))
                + panel(prose('Language, culture and identity are central to this care. Through discussions with seers and mental health professionals, clients regain direction and connection. '
                              'Traditional knowledge is used as a preventative and supportive approach for overall wellness.', size=14.8, style='margin-bottom: 10px')
                        + p(f'To connect with our Traditional Healing Coordinator, please <a href="Contact.dc.html" style="color: {RUST}; font-weight: 600">contact us</a>.',
                            14.8, INK, 1.55, 'margin-top: 2px')))
    s += area('cultural', 'bowl', 'sage', 'Cultural Services', 'Traditional healing, spiritual support and cultural learning.', cultural,
              'left: -40px; bottom: -60px; transform: rotate(12deg)')

    # ---- Mental Health Services
    mh = (panel(prose('The Mental Health Program offers short-term services for individuals aged 18 and older who receive care through Tsi Kanonhkhwatsheríyo.',
                      'Using a wholistic approach that blends Western and Traditional healing practices, the Mental Health Worker provides strengths-based and trauma-informed support to promote balance and well-being.',
                      size=14.8, style='margin-bottom: 10px')
                + note('info', None, 'In an emergency, call 911 or go to the nearest emergency department.', 'cream', 'margin-top: 6px'))
          + panel(h3('Short-term services include', 19)
                  + f'<div style="margin-top: 12px">{bullets(["Psychosocial assessment", "Goal setting and Plan of Care development", "Resource connections and referrals", "Education and guidance", "Case management", "Group workshops and programs", "A final wrap-up appointment to review goals and next steps"], "check", "#1F4A2B", 14.4, 7)}</div>'))
    s += area('mental-health', 'lotus', 'sage', 'Mental Health Services', 'Supporting adults, with linkage for pre- and post-natal mental health care.', mh,
              'right: -36px; top: -10px; transform: rotate(-10deg)')

    # ---- Health Support Services
    nrt = ('26 weeks of free Nicotine Replacement Therapy (NRT): patches (21 mg, 14 mg, 7 mg), Nicorette gum (2 mg), Thrive lozenges (2 mg) and the Nicorette inhaler (4 mg)')
    contacts = (f'<ul style="margin: 12px 0 0; padding: 0; list-style: none">'
                + contact_row('Sarah Kring', 'Allied Health Manager', '120', 'sarah.kring@iipct.com')
                + contact_row('Allison Loft', 'Community Development Worker', '213', 'allison.loft@iipct.com') + '</ul>')
    link = f'color: {RUST}; font-weight: 600'
    support = (panel(h3('Community health programs', 19)
                     + prose('Culturally safe programs help increase education and promote wellness for Indigenous people living in the South East LHIN region. '
                             'Support includes help with forms, funding, and access to essential community resources.', size=14.4, style='margin: 8px 0 12px')
                     + bullets(['Help with forms for IIPCT clients: Ontario Works, Ontario Disability Support Program, Indian Day Schools and Water Claims',
                                'Funding help through the Assistive Devices Program, NIHB and other available programs',
                                'Guidance with community services for housing and food security'], 'check', '#1F4A2B', 14.4, 7))
               + panel(h3('Smoking cessation support', 19)
                       + prose('We provide access to the STOP (Smoking Treatment for Ontario Patients) Program, a province-wide program that delivers smoking cessation treatment and counselling. '
                               'It is offered through a partnership with the Canadian Mental Health Association.', size=14.4, style='margin: 8px 0 12px')
                       + bullets([nrt, 'Smoking cessation counselling with goal setting, journaling, and one-on-one or phone-based support (weekly, biweekly or monthly)',
                                  'An Indigenous Quit Kit, available on request'], 'check', '#1F4A2B', 14.4, 7))
               + panel(h3('Questions about these programs?', 19) + contacts
                       + f'<div style="margin-top: 4px">{textlink("Contact a clinic", "Contact.dc.html", 14, "gap: 10px; min-height: 40px")}</div>'
                       + p(f'Stay connected to our community programs and events through our <a href="Events.dc.html" style="{link}">Events page</a>, '
                           f'our <a href="{FACEBOOK_URL}" style="{link}">Facebook page</a> and our <a href="{NEWSLETTER_URL}" style="{link}">monthly newsletter</a>.',
                           14.2, INK, 1.5, 'margin-top: 12px'), 'grid-column: 1 / -1'))
    s += area('health-support', 'people', 'gold', 'Health Support Services', 'Care coordination across all systems, with ongoing programs to promote wellness.', support,
              'left: -40px; bottom: -40px; transform: rotate(14deg)')

    # ---- Getting care (what the old site says: online booking for registered patients; new patients join a waitlist by phone)
    start = (start_card('calendar-check', 'sage', 'Already an IIPCT patient?', 'Registered patients can book a visit online. You can also call your clinic.',
                        btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check'))
             + start_card('people', 'gold', 'New to IIPCT?',
                          'Are you Indigenous and in need of a family doctor or primary care provider, or hoping to find care closer to home? '
                          'Our Deseronto clinic is accepting patients for its waitlist. To join, call and speak to our Reception. '
                          'You must be Indigenous (Status or Non-Status) to register with our clinic.',
                          btn('Contact Us', 'Contact.dc.html', 'outline', 'phone', False)))
    s += f'''
<section style="position: relative; {WRAP}; padding: 44px 58px 0 61px">
<div style="display: flex; flex-direction: column; gap: 6px">{eyebrow('Getting care')}{h2('How to get care', 30.4)}
{p('Our priority population is all people who identify as Indigenous, and their families, in our regions. All our services are status blind.', 14.8, INK, 1.45, 'max-width: 760px')}</div>
<div style="margin-top: 16px; display: flex; flex-direction: column; gap: 16px">{start}</div>
</section>
<div style="margin-top: 36px">{nl_band()}</div>'''
    s += footer()
    return 'IIPCT — Services', s
