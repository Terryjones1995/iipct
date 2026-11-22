"""Schedule Your Visit (booking), Privacy Policy, Accessibility and Site Map."""
from lib import *

HOME = ('Home', 'Main.dc.html')
LABEL = f'font-size: 13px; font-weight: 700; color: {HEAD}; line-height: 1.2'
FIELD = (f'width: 100%; height: 44px; padding: 0 14px; border-radius: 9px; border: 1px solid #BFB59E; background: #FFFDF8; '
         f'font-family: inherit; font-size: 15px; color: {INK}; box-shadow: inset 0 1px 2px rgba(60, 40, 10, 0.05)')
HINT = f'font-size: 12.4px; line-height: 1.35; color: {MUTED}'

def field(fid, label, hint='', kind='text', extra='', ph=''):
    hn = f'<span id="{fid}-hint" style="{HINT}">{hint}</span>' if hint else ''
    ab = f' aria-describedby="{fid}-hint"' if hint else ''
    return (f'<div style="display: flex; flex-direction: column; gap: 6px"><label for="{fid}" style="{LABEL}">{label}</label>'
            f'<input id="{fid}" type="{kind}" placeholder="{ph}"{ab} {extra} style="{FIELD}">{hn}</div>')

# ------------------------------------------------------------------ booking
def booking():
    months = ''.join(f'<option>{m}</option>' for m in ['Month', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    seg = 'min-width: 44px; height: 36px; padding: 0 12px; border: none; font-family: inherit; font-size: 13px; font-weight: 700; cursor: pointer'
    lang = (f'<div role="group" aria-label="Language" style="display: inline-flex; border-radius: 9px; overflow: hidden; border: 1.5px solid #1E3D28">'
            f'<button type="button" aria-pressed="true" style="{seg}; background: #17402A; color: #FFFFFF">EN</button>'
            f'<button class="sego" type="button" aria-pressed="false" style="{seg}; background: #FFFDF8; color: #13261B; border-left: 1.5px solid #1E3D28">FR</button></div>')
    form = f'''<form style="flex: 999 1 560px; min-width: 0; padding: 26px 30px 28px; border-radius: 16px; {CARD}; display: flex; flex-direction: column; gap: 20px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 20px">
<div style="display: flex; align-items: center; gap: 16px">{circ('calendar-check', 'forest', 54, 28, 1.5)}{h2('Online booking', 28)}</div>
<div style="display: flex; align-items: center; gap: 18px">{lang}
<a class="tl" href="#booking-help" style="display: inline-flex; align-items: center; gap: 7px; min-height: 36px; font-size: 13.6px; font-weight: 600; color: {RUST}; text-decoration: none">{ico('help', 17, RUST, 1.9)}<span>Help</span></a></div>
</div>
<p style="margin: 0; font-size: 15.4px; line-height: 1.5; color: {INK}">Welcome! To start your online booking, enter the information below.</p>
{note('info', 'For registered patients', 'Online booking is only available to patients already registered at this clinic. New patients can’t book appointments online. Call us and we’ll get you set up.')}
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 18px 22px">
{field('b-first', 'First name', extra='autocomplete="given-name"')}
{field('b-last', 'Last name', extra='autocomplete="family-name"')}
</div>
<div class="g1" style="display: grid; grid-template-columns: minmax(0, 2.6fr) minmax(0, 1fr); gap: 18px 22px; align-items: start">
{field('b-hn', 'Health number', '10 digits, on the front of your Ontario health card.', 'text', 'inputmode="numeric" autocomplete="off" maxlength="16"', '1234 - 567 - 890')}
{field('b-vc', 'Version code', 'The letters after the number, if your card has them.', 'text', 'autocomplete="off" autocapitalize="characters" maxlength="2"', 'AB')}
</div>
<fieldset style="margin: 0; padding: 0; border: none; display: flex; flex-direction: column; gap: 6px">
<legend style="padding: 0; margin-bottom: 6px; {LABEL}">Birth date</legend>
<div class="g3x" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(130px, 100%), 1fr)); gap: 12px 14px">
<div style="display: flex; flex-direction: column; gap: 5px"><label for="b-yyyy" style="{HINT}; font-weight: 600">Year</label><input id="b-yyyy" type="text" inputmode="numeric" placeholder="yyyy" autocomplete="bday-year" style="{FIELD}"></div>
<div style="display: flex; flex-direction: column; gap: 5px"><label for="b-mm" style="{HINT}; font-weight: 600">Month</label><select id="b-mm" autocomplete="bday-month" style="{FIELD}; appearance: auto">{months}</select></div>
<div style="display: flex; flex-direction: column; gap: 5px"><label for="b-dd" style="{HINT}; font-weight: 600">Day</label><input id="b-dd" type="text" inputmode="numeric" placeholder="dd" autocomplete="bday-day" style="{FIELD}"></div>
</div>
</fieldset>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 24px; margin-top: 2px">
<button class="btn bp" type="button" style="display: inline-flex; align-items: center; justify-content: center; gap: 12px; height: 46px; min-width: 190px; padding: 0 26px; border-radius: 9px; border: 1px solid #2E5E38; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; font-family: inherit; font-size: 15px; font-weight: 600; cursor: pointer; box-shadow: 0 3px 7px rgba(16, 44, 24, 0.28)"><span>Submit</span>{ico('arrow', 17, '#FFFFFF', 2)}</button>
<span style="flex: 1 1 260px; display: flex; align-items: flex-start; gap: 9px; {HINT}">{ico('lock', 16, '#1F4A2B', 1.9, 'margin-top: 1px')}<span>Your details go through Ocean, the secure patient portal IIPCT uses for online booking.</span></span>
</div>
</form>'''
    rows = ''.join(f'<li style="display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 8px 0; border-top: 1px solid #E6D9BF">'
                   f'<span style="font-weight: 600; color: {HEAD}">{n}</span><a class="tl" href="tel:{tel}" style="color: {RUST}; font-weight: 600; text-decoration: none; white-space: nowrap">{ph}</a></li>'
                   for n, ad, ph, tel in CLINICS)
    aside = f'''<aside style="flex: 1 1 340px; max-width: 420px; min-width: 0; display: flex; flex-direction: column; gap: 18px">
<div id="booking-help" style="padding: 22px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-direction: column; align-items: flex-start; gap: 10px; box-shadow: {SHADOW}">
{eyebrow('Booking help', '#E3BE74')}
<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 25px; line-height: 1.1; letter-spacing: -0.012em; color: #FFFFFF">Questions, or trouble booking?</h2>
<a class="fl" href="tel:+13434780196" style="display: flex; align-items: center; gap: 10px; margin-top: 2px; font-size: 19px; font-weight: 700; color: #FFFFFF; text-decoration: none">{ico('phone', 20, '#E3BE74', 1.8)}<span>(343) 478-0196</span></a>
<p style="margin: 0; font-size: 13.8px; line-height: 1.5; color: #F4F1E8">Press <strong style="color: #FFFFFF">1</strong> for Tyendinaga or <strong style="color: #FFFFFF">2</strong> for Kingston.</p>
</div>
<div style="padding: 18px 22px 20px; border-radius: 14px; {CARD}; display: flex; flex-direction: column; gap: 12px">
{h3('Before you book', 19)}
{bullets(['Online booking is for registered patients only.', 'Book only the appointment types offered to you.', 'New patient? Call us instead of booking online.'], 'check', '#1F4A2B', 13.8, 8)}
</div>
<div style="padding: 18px 22px 12px; border-radius: 14px; {CARD}">
{h3('Prefer to call?', 19)}
<ul style="margin: 10px 0 0; padding: 0; list-style: none; font-size: 13.4px; line-height: 1.3">{rows}</ul>
</div>
</aside>'''
    s = header('')
    s += sub_hero([HOME, ('Schedule Your Visit', None)], 'Schedule Your Visit',
                  'Book online if you’re already a patient, or call your clinic and reception will set it up for you.', eyebrow_txt='Appointments', lead_w=600)
    s += f'<div style="{WRAP}; padding: 34px 48px 8px 83px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 30px 44px">{form}{aside}</div>'
    s += f'<div style="margin-top: 40px">{newsletter()}</div>'
    s += footer()
    return 'IIPCT — Schedule Your Visit', s

# ------------------------------------------------------------------ legal pages
def legal(crumb, title, lead, sections, draft):
    toc = ''.join(f'<li><a href="#{i}" style="display: block; padding: 8px 12px; border-radius: 8px; font-size: 13.6px; font-weight: 600; line-height: 1.25; color: {HEAD}; text-decoration: none">{t}</a></li>' for i, t, _ in sections)
    body = ''.join(f'<section id="{i}" style="display: flex; flex-direction: column; gap: 11px; padding-top: 4px">{h2(t, 25)}{b}</section>' for i, t, b in sections)
    updated = f'<p style="margin: 0; font-size: 13.4px; font-weight: 600; color: {MUTED}">Last updated: [date]</p>'
    s = header('')
    s += draft_bar(draft)
    s += sub_hero([HOME, (crumb, None)], title, lead, extra=updated, title_size=44, lead_w=620)
    s += f'''<div style="{WRAP}; padding: 34px 48px 48px 83px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 30px 56px">
<nav class="toc" aria-label="On this page" style="flex: 1 1 230px; max-width: 280px; padding: 16px 12px 12px; border-radius: 14px; {CARD}">
<span style="display: block; padding: 0 12px 8px; font-size: 11.6px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: {RUST}">On this page</span>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 1px">{toc}</ul>
</nav>
<div style="flex: 999 1 560px; min-width: 0; max-width: 780px; display: flex; flex-direction: column; gap: 30px">{body}</div>
</div>'''
    s += footer()
    return s

def ph(text):
    """Bracketed placeholder for facts only IIPCT can supply."""
    return f'<span style="background: #F6EACD; border-radius: 4px; padding: 1px 5px">[{text}]</span>'

def privacy():
    P = lambda *t: prose(*t, size=14.8, style='margin-bottom: 0')
    B = lambda items: bullets(items, 'check', '#1F4A2B', 14.6, 9)
    svc = lambda name, what: f'<li style="display: flex; flex-wrap: wrap; gap: 4px 14px; padding: 10px 0; border-top: 1px solid #E6D9BF"><span style="flex: 0 0 150px; font-weight: 700; color: {HEAD}">{name}</span><span style="flex: 1 1 280px">{what}</span></li>'
    sections = [
        ('who', 'Who we are', P('Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (IIPCT) provides primary care to Indigenous people and their families in southeastern Ontario. This policy explains what personal information we collect, why, and the choices you have.')),
        ('collect', 'What we collect',
         h3('On this website', 18) + B(['Your name, contact details and message when you write to us.', 'Your email address when you sign up for the newsletter.', f'Basic visit statistics, such as pages viewed. {ph("confirm analytics tool, or remove")}'])
         + h3('When you book or receive care', 18, 'margin-top: 8px') + P('Personal health information, such as your name, date of birth, health card number and health history. Online booking collects only what is needed to find your chart and confirm your appointment.')),
        ('use', 'How we use it', B(['To provide and coordinate your care.', 'To book, confirm and follow up on appointments.', 'To answer your questions.', 'To send the newsletter, if you asked for it. You can unsubscribe at any time.', 'To meet our legal and reporting obligations.'])),
        ('phipa', 'Your health information', P('IIPCT follows Ontario’s Personal Health Information Protection Act, 2004 (PHIPA). We collect, use and share your health information only as the Act allows, and with your consent where consent is required.')),
        ('share', 'Who we share it with', P('With the health care providers involved in your care, and with companies that run our systems under agreements that protect your information. We don’t sell personal information.')),
        ('services', 'Services we use', P('These services handle information on our behalf. Each has its own privacy policy.')
         + f'<ul style="margin: 2px 0 0; padding: 0; list-style: none; font-size: 14.4px; line-height: 1.45; border-bottom: 1px solid #E6D9BF">'
         + svc('Ocean', 'Online appointment booking') + svc('Mailchimp', 'Newsletter sign-up and delivery') + svc('BambooHR', 'Job applications')
         + svc('Facebook, TikTok', 'Our social pages. What you post or message there is covered by their policies.') + '</ul>'),
        ('safe', 'Keeping it safe', P(ph('Summary of IIPCT’s safeguards and how long records are kept, from the organization’s policy'))),
        ('rights', 'Your rights', P('You can ask to see your health record, ask us to correct it, and withdraw your consent, within the limits set by law.')
         + P(f'Contact our Privacy Officer: {ph("name")}, {ph("email")}, {ph("phone")}.')),
        ('complaints', 'Questions and complaints', P('Talk to us first and we’ll do our best to sort it out. If you’re not satisfied with our answer, you can contact the Information and Privacy Commissioner of Ontario.')
         + f'<div>{ext("ipc.on.ca", "https://www.ipc.on.ca/", 14.4)}</div>'),
        ('changes', 'Changes to this policy', P('If this policy changes, the new version is posted here with a new date at the top.')),
    ]
    return 'IIPCT — Privacy Policy', legal('Privacy Policy', 'Privacy Policy', 'How IIPCT collects, uses and protects personal information, on this website and in our care.', sections,
                                          'Draft for IIPCT to review. Items in [brackets] need their details, and the wording needs sign-off from IIPCT’s privacy lead before launch.')

def accessibility():
    P = lambda *t: prose(*t, size=14.8)
    B = lambda items: bullets(items, 'check', '#1F4A2B', 14.6, 9)
    sections = [
        ('commitment', 'Our commitment', P('IIPCT is committed to care, services and information that everyone can use, in keeping with the Accessibility for Ontarians with Disabilities Act, 2005 (AODA).')),
        ('website', 'This website', P('We are building this site to meet the Web Content Accessibility Guidelines (WCAG) 2.0, Level AA. That includes:')
         + B(['Text you can resize, with strong colour contrast.', 'Every page and menu usable with a keyboard.', 'Text alternatives for images.', 'Event and program details posted as text, not only as a flyer image.'])),
        ('clinics', 'At our clinics', B(['Service animals are welcome.', 'Support persons are welcome to come with you.', 'You can use your own assistive devices.'])
         + P(ph('Clinic details from IIPCT: accessible parking, entrances and washrooms at each location'))),
        ('formats', 'Accessible formats and communication supports', P('Need a document in another format, or support to communicate with us? Tell us what works for you and we’ll arrange it with you.')),
        ('disruptions', 'Service disruptions', P('If something you rely on is temporarily unavailable at a clinic, we’ll post a notice here and at the location, with the reason and how long we expect it to last.')),
        ('feedback', 'Feedback', P('Tell us where you ran into a barrier, or how we can do better.')
         + f'<div style="display: flex; flex-wrap: wrap; gap: 10px 28px; font-size: 15px; font-weight: 700">'
           f'<a class="tl" href="tel:+13434780196" style="display: inline-flex; align-items: center; gap: 10px; color: {HEAD}; text-decoration: none">{ico("phone", 19, RUSTI, 1.7)}<span>(343) 478-0196</span></a>'
           f'<a class="tl" href="mailto:info@iipct.com" style="display: inline-flex; align-items: center; gap: 10px; color: {HEAD}; text-decoration: none">{ico("mail", 20, RUSTI, 1.7)}<span>info@iipct.com</span></a></div>'
         + P(f'Accessibility contact: {ph("name and role")}.')),
        ('policies', 'Policies and training', P(ph('How to request IIPCT’s accessibility policies, and a line on staff training'))),
    ]
    return 'IIPCT — Accessibility', legal('Accessibility', 'Accessibility', 'Our commitment to care and information that everyone can use.', sections,
                                         'Draft for IIPCT to review. Items in [brackets] need their details before launch.')

def sitemap():
    def col(title, links, icon):
        rows = ''
        for t, h, lvl in links:
            x = ico('external', 13, RUST, 1.9) if h.startswith('http') else ''
            pad = '8px 0 8px 18px' if lvl else '9px 0'
            fw = '500' if lvl else '600'
            rows += (f'<li><a class="tl" href="{h}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: {pad}; border-top: 1px solid #E6D9BF; '
                     f'font-size: 14px; font-weight: {fw}; line-height: 1.25; color: {HEAD}; text-decoration: none"><span>{t}</span>{x}</a></li>')
        return (f'<div style="padding: 20px 22px 12px; border-radius: 14px; {CARD}"><div style="display: flex; align-items: center; gap: 13px; margin-bottom: 12px">{ico(icon, 24, RUSTI, 1.5)}{h3(title, 20)}</div>'
                f'<ul style="margin: 0; padding: 0; list-style: none">{rows}</ul></div>')
    cols = [
        col('Main pages', [('Home', 'Main.dc.html', 0), ('Who We Are', 'WhoWeAre.dc.html', 0), ('Services', 'Services.dc.html', 0), ('Events &amp; Programs', 'Events.dc.html', 0),
                           ('News &amp; Updates', 'News.dc.html', 0), ('Contact Us', 'Contact.dc.html', 0), ('Schedule Your Visit', 'Booking.dc.html', 0)], 'house'),
        col('Who We Are', [('About IIPCT', 'WhoWeAre.dc.html', 0), ('Career Opportunities', 'Careers.dc.html', 0), ('Board of Directors', 'Board.dc.html', 0),
                           ('Best Practice Spotlight Organization (BPSO)', 'BPSO.dc.html', 0)], 'people'),
        col('Services', [('All Services', 'Services.dc.html', 0), ('Primary Medical Care', 'PrimaryCare.dc.html', 0), ('Immunization Program', 'Immunization.dc.html', 1),
                         ('Well Baby &amp; Well Child', 'WellBaby.dc.html', 1), ('TB Testing', 'TBTesting.dc.html', 1), ('Advanced Foot Care', 'FootCare.dc.html', 1),
                         ('Diabetic Retinopathy Screening', 'Retinopathy.dc.html', 1), ('Outreach &amp; Community Support', 'Outreach.dc.html', 1)], 'stethoscope'),
        col('News', [('News &amp; Updates', 'News.dc.html', 0), ('Our Team Honoured at the IPHCC Awards', 'NewsIPHCCAwards.dc.html', 1),
                     ('Together We’re Stronger: Breast Cancer Screening Event', 'NewsBreastScreening.dc.html', 1)], 'news'),
        col('Legal', [('Privacy Policy', 'Privacy.dc.html', 0), ('Accessibility', 'Accessibility.dc.html', 0), ('Site Map', 'SiteMap.dc.html', 0)], 'scales'),
        col('Elsewhere', [('Newsletter sign-up', NEWSLETTER_URL, 0), ('Facebook', FACEBOOK_URL, 0), ('TikTok', TIKTOK_URL, 0)], 'globe'),
    ]
    s = header('')
    s += sub_hero([HOME, ('Site Map', None)], 'Site Map', 'Every page on the site, in one place.', title_size=44)
    s += f'<div style="{WRAP}; padding: 34px 48px 48px 83px">{grid(cols, 330, 20, "align-items: start")}</div>'
    s += footer()
    return 'IIPCT — Site Map', s
