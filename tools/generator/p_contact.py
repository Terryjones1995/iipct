from lib import *

LABEL = f'font-size: 12.6px; font-weight: 700; color: {HEAD}; line-height: 1.2'
FIELD = (f'width: 100%; height: 34px; padding: 0 13px; border-radius: 8px; border: 1px solid #CFC7B6; background: #FFFCF7; '
         f'font-family: inherit; font-size: 12.6px; color: {INK}; box-shadow: inset 0 1px 2px rgba(60, 40, 10, 0.05)')
REQ = '<span aria-hidden="true" style="color: #A3301C"> *</span>'

def field(fid, label, placeholder, kind='text', req=True):
    return (f'<div style="display: flex; flex-direction: column; gap: 6px"><label for="{fid}" style="{LABEL}">{label}{REQ if req else ""}</label>'
            f'<input id="{fid}" type="{kind}" placeholder="{placeholder}" style="{FIELD}"></div>')

def info_row(icon, label, lines, note=''):
    body = ''.join(f'<span>{l}</span>' for l in lines)
    nt = f'<span style="font-style: italic; font-size: 12.2px; margin-top: 3px">{note}</span>' if note else ''
    return f'''<div style="display: flex; align-items: flex-start; gap: 24px">
<span style="flex: none; width: 46px; height: 46px; border-radius: 50%; background: #FFFCF6; border: 1px solid #DCCBAB; display: flex; align-items: center; justify-content: center">{ico(icon, 24, '#A04A32', 1.7)}</span>
<div style="display: flex; flex-direction: column; gap: 1px; padding-top: 3px; font-size: 13.2px; line-height: 1.3; color: {INK}">
<span style="font-size: 14.8px; font-weight: 700; color: {HEAD}; line-height: 1.2">{label}</span>{body}{nt}
</div>
</div>'''

def clinic_card(photo, alt, name, addr1, addr2, phone, tel):
    row = lambda ic, html: f'<li style="display: flex; align-items: flex-start; gap: 17px">{ico(ic, 19, "#A04A32", 1.6, "margin-top: 1px")}<span>{html}</span></li>'
    return f'''<article class="card" style="display: flex; flex-direction: column; padding: 0 0 15px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{img(photo, alt, 'width: 100%; aspect-ratio: 188 / 72; object-fit: cover; border-radius: 13px 13px 0 0')}
<div style="flex: 1; padding: 9px 6px 0 24px; display: flex; flex-direction: column; gap: 8px">
<h3 style="margin: 0; display: flex; align-items: center; gap: 11px; font-family: {SERIF}; font-weight: 700; font-size: 19.4px; line-height: 1.1; letter-spacing: -0.022em; color: {HEAD}; white-space: nowrap">{pin_fill(22)}<span>{name}</span></h3>
<ul style="margin: 0; padding: 0 0 0 4px; list-style: none; display: flex; flex-direction: column; gap: 7px; font-size: 13.2px; line-height: 1.3; letter-spacing: -0.01em; color: {INK}">
{row('pin', addr1 + '<br class="k">' + addr2)}
{row('phone', f'<a href="tel:{tel}" style="color: {INK}; text-decoration: none">{phone}</a>')}
{row('mail', f'<a href="mailto:info@iipct.com" style="color: {INK}; text-decoration: none">info@iipct.com</a>')}
{row('clock', f'<span style="display: block; font-weight: 700; color: {HEAD}">Hours</span><span style="font-size: 12px">Mon – Fri, 8:30 AM – 4:30 PM</span>')}
</ul>
</div>
<div style="display: flex; justify-content: center; margin-top: 10px">{btn('View Location', '#locations', 'sage', None, True, 'xs', 'min-width: 174px; gap: 12px; font-size: 13px')}</div>
</article>'''

def faq_row(q):
    return (f'<li><button class="faq" type="button" aria-expanded="false" style="width: 100%; min-height: 34px; padding: 0 18px 0 20px; border-radius: 10px; border: 1px solid #DCCBAB; background: #FFFCF6; '
            f'display: flex; align-items: center; justify-content: space-between; gap: 12px; font-family: inherit; font-size: 13.4px; font-weight: 600; color: {HEAD}; text-align: left; cursor: pointer">'
            f'<span>{q}</span>{ico("chev-down", 17, "#A3301C", 2.2)}</button></li>')

def page():
    buttons = btn('Schedule Your Visit', '#', 'primary', 'calendar-check') + btn('Book an Appointment', '#', 'outline', 'calendar-dot', False)
    s = header('contact')
    s += hero('hero-contact', 58.4, 356, 'We’re Here to Support<br>Your Care Journey',
              'Have a question, need to book a service, or want to learn more<br>about our programs? Get in touch — we’re here to help. You can<br>schedule a visit, book an appointment, or connect with our team<br>for general inquiries and support.',
              buttons, eyebrow_txt='Contact Us', h1_size=45, lead_size=16.4, lead_lh=1.26, pad='24px 0 40px 84px', gap=10, btn_mt=6, sq_mt=-1, obj='center center')
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 40px; margin-top: 16px">
{branch(110, '#B5BFA6', 0.5, 'right: -30px; bottom: -44px; transform: rotate(-12deg)')}
<div style="position: relative; overflow: hidden; border-radius: 16px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05); display: flex; flex-wrap: wrap; align-items: stretch">
<form class="pads" style="flex: 1.14 1 520px; min-width: 0; padding: 18px 36px 16px 32px; display: flex; flex-direction: column; gap: 13px">
<div style="display: flex; align-items: center; gap: 20px">
{circ('mail', 'sage', 66, 32, 1.5)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('Send Us a Message', 28)}
{p('Use the form below for general inquiries, program information,<br>or non-urgent support. Our team will get back to you as soon as possible.', 13.8, INK, 1.3)}
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 12px 22px; padding-left: 6px">
{field('c-name', 'Full Name', 'Enter your full name')}
{field('c-phone', 'Phone Number', '(xxx) xxx-xxxx', 'tel', False)}
{field('c-email', 'Email Address', 'Enter your email address', 'email')}
<div style="display: flex; flex-direction: column; gap: 6px"><label for="c-type" style="{LABEL}">Inquiry Type{REQ}</label>
<select id="c-type" style="{FIELD}; appearance: auto"><option>Select an option</option><option>Book or change an appointment</option><option>Programs and events</option><option>General question</option></select></div>
</div>
<div style="display: flex; flex-direction: column; gap: 6px; padding-left: 6px"><label for="c-msg" style="{LABEL}">Your Message{REQ}</label>
<textarea id="c-msg" placeholder="Tell us how we can help..." style="{FIELD}; height: 66px; padding: 10px 13px; resize: vertical; line-height: 1.4"></textarea></div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 26px; padding-left: 6px">
<button type="button" style="display: inline-flex; align-items: center; justify-content: center; gap: 12px; height: 41px; min-width: 194px; padding: 0 24px; border-radius: 9px; border: 1px solid #2E5E38; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; font-family: inherit; font-size: 14.6px; font-weight: 600; cursor: pointer; box-shadow: 0 3px 7px rgba(16, 44, 24, 0.28)">{ico('send', 18, '#FFFFFF', 1.8)}<span>Send Message</span></button>
<span style="font-size: 12px; font-style: italic; color: {INK}"><span aria-hidden="true" style="color: #A3301C">* </span>Required field</span>
</div>
</form>
{vdiv('200px', GOLDL, 'margin: 26px 0 22px')}
<div class="pads" style="position: relative; flex: 1 1 440px; min-width: 0; padding: 18px 30px 16px 40px; display: flex; flex-direction: column; gap: 13px">
{img('feather-gold', '', 'position: absolute; right: 16px; top: 96px; width: 118px; height: auto; opacity: 0.5; transform: rotate(8deg)').replace('<img ', '<img class="hide-s" ')}
<div style="position: relative; display: flex; align-items: center; gap: 22px">
{circ('phone', 'rust', 66, 32, 1.5)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('General Contact Information', 26.6)}
{p('Reach out to our team for appointments, services, programs,<br>or community support.', 13.8, INK, 1.3)}
</div>
</div>
<div style="position: relative; display: flex; flex-direction: column; gap: 9px; padding-left: 18px">
{info_row('phone', 'Phone', ['<a href="tel:+13434780196" style="color: inherit; text-decoration: none">(343) 478-0196</a> &nbsp;·&nbsp; Toll-free <a href="tel:+18889996016" style="color: inherit; text-decoration: none">(888) 999-6016</a>'])}
{info_row('mail', 'Email', ['<a href="mailto:info@iipct.com" style="color: inherit; text-decoration: none">info@iipct.com</a>'])}
{info_row('pin', 'Mailing Address', ['Indigenous Interprofessional Primary Care Team (IIPCT)', '45 Meadow Drive', 'Tyendinaga Mohawk Territory, ON &nbsp;[POSTAL CODE]'])}
{info_row('clock', 'Office Hours (Administration)', ['Mon – Fri, 8:30 AM – 4:30 PM'], 'Clinic hours may vary by location. See below for details.')}
</div>
<div style="position: relative; padding-left: 18px; margin-top: 3px">{social_row(label='Follow IIPCT')}</div>
</div>
</div>
</section>
<section style="position: relative; {WRAP}; padding: 22px 44px 0 50px">
{pines(PINES_R, 200, 78, '#B4BF9F', 0.7, 'right: 46px; top: 26px')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 42px; padding-left: 22px">
<div style="display: flex; flex-direction: column; gap: 4px">{eyebrow('Our Clinics')}{h2('Multi-Clinic Directory', 39)}</div>
{vdiv('54px')}
{p('Access primary care, wellness services, and community programs<br>at a location near you.', 15.4, INK, 1.4, 'flex: 1 1 360px')}
</div>
<div style="position: relative; margin-top: 17px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 12px">
{clinic_card('con-bancroft', 'Forested lakeshore', 'Bancroft Clinic', '69 Cleak Avenue', 'Bancroft, ON', '(613) 706-2001', '+16137062001')}
{clinic_card('con-kingston', 'Kingston waterfront', 'Kingston Clinic', '730 Front Road', 'Kingston, ON', '(833) 999-1382', '+18339991382')}
{clinic_card('con-tyendinaga', 'Sunset over a lake', 'Tyendinaga Clinic', '45 Meadow Drive', 'Tyendinaga, ON', '(343) 478-0196', '+13434780196')}
{clinic_card('con-deseronto', 'Calm bay at sunset', 'Deseronto Clinic', '331 Dundas Street', 'Deseronto, ON', '(613) 354-6992', '+16133546992')}
{clinic_card('con-shannonville', 'River with rocky shore', 'Shannonville Clinic', '14 York Road', 'Shannonville, ON', '(343) 478-0196', '+13434780196')}
</div>
</section>
<section id="locations" style="{WRAP}; padding: 26px 55px 0 53px; display: flex; flex-wrap: wrap; align-items: stretch; gap: 20px 26px">
<div class="locm" style="position: relative; overflow: hidden; flex: 1.62 1 560px; min-width: 0; min-height: 268px; border-radius: 16px; background: #EFEAD6; border: 1px solid #D3CEAE">
{img('con-map', 'Illustrated map showing the Bancroft, Shannonville, Tyendinaga and Deseronto clinics', 'position: absolute; top: 0; right: 0; width: 54%; height: 100%; object-fit: cover; object-position: right center; mask-image: linear-gradient(90deg, transparent 0%, #000 12%)').replace('<img ', '<img class="locm-img" ')}
{pines(PINES_L, 200, 128, '#B4BF9F', 0.6, 'left: -4px; bottom: 0')}
{pines(PINES_R, 200, 88, '#B4BF9F', 0.5, 'left: 176px; bottom: 0')}
<div class="locm-txt" style="position: relative; width: 46%; min-width: min(300px, 100%); padding: 20px 0 20px 24px; display: flex; align-items: flex-start; gap: 20px">
{circ('pin', 'rust', 62, 30, 1.6)}
<div style="display: flex; flex-direction: column; align-items: flex-start; gap: 13px; padding-top: 8px">
{h2('Our Locations', 26.4)}
{p('Find IIPCT clinics across the region, providing culturally safe, whole-person care to our communities.', 14.4, INK, 1.42, 'max-width: 270px')}
{btn('View All Clinic Locations', '#', 'outline', None, True, 'sm', 'margin-top: 4px; padding: 0 16px; gap: 11px; font-size: 12.8px')}
</div>
</div>
</div>
{vdiv('200px', '#E6D6BC')}
<div style="flex: 1 1 400px; min-width: 0; display: flex; flex-direction: column; gap: 10px; padding-left: 10px">
<div style="display: flex; align-items: center; gap: 22px">
{circ('question', 'rust', 54, 28, 1.6)}
<div style="display: flex; flex-direction: column; gap: 4px">
{h2('Frequently Asked Questions', 24.6)}
{p('Quick answers to common questions about appointments, services, and staying connected with IIPCT.', 12.9, INK, 1.3)}
</div>
</div>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px">
{faq_row('How do I book an appointment?')}{faq_row('What services are available at IIPCT?')}{faq_row('Do I need a referral?')}{faq_row('Can I access care at any of the IIPCT clinics?')}{faq_row('How do I update my contact information?')}
</ul>
{textlink('View All FAQ &amp; Support Information', '#', 14.2, 'margin-top: 2px')}
</div>
</section>
<div style="margin-top: 30px">{newsletter()}</div>'''
    s += footer()
    return 'IIPCT — Contact Us', s
