"""Schedule Your Visit (booking), Privacy Policy, Accessibility and Site Map."""
from lib import *

HOME = ('Home', 'Main.dc.html')
from facts import BY_KEY, WAITLIST

# ------------------------------------------------------------------ booking
def booking():
    """Schedule Your Visit. This site never collects personal or health information: booking happens on IIPCT's Ocean page."""
    go = (f'<a class="btn bp" href="{BOOKING_URL}" aria-label="Book online on Ocean, IIPCT’s booking site (opens in a new tab)" '
          f'style="display: inline-flex; align-items: center; justify-content: center; gap: 12px; min-height: 50px; padding: 0 28px; border-radius: 10px; '
          f'border: 1px solid #2E5E38; background: linear-gradient(180deg, #20502B 0%, #133419 100%); color: #FFFFFF; font-size: 16px; font-weight: 600; line-height: 1; '
          f'text-decoration: none; box-shadow: 0 3px 7px rgba(16, 44, 24, 0.28)">{ico("calendar-check", 20, "currentColor", 1.8)}<span>Book online</span>{ico("external", 17, "currentColor", 2)}</a>')
    book = f'''<section style="flex: 1.25 1 480px; min-width: 0; padding: 26px 30px 28px; border-radius: 16px; {CARD}; display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
<div style="display: flex; align-items: center; gap: 16px">{circ('calendar-check', 'forest', 54, 28, 1.5)}{h2('Book online', 28)}</div>
<p style="margin: 0; font-size: 15.4px; line-height: 1.5; color: {INK}">Online booking is for patients who are already registered with IIPCT.</p>
{go}
<p style="margin: 0; display: flex; align-items: flex-start; gap: 9px; font-size: 13.4px; line-height: 1.45; color: {MUTED}">{ico('lock', 16, '#1F4A2B', 1.9, 'margin-top: 2px')}<span>The button opens Ocean, the booking website IIPCT uses, in a new tab. This website does not ask for your health information.</span></p>
{note('info', 'Not registered with IIPCT?', 'You can’t book online yet. Call us instead, and reception will help.', 'sage', 'align-self: stretch')}
</section>'''
    call = f'''<section style="flex: 1 1 340px; min-width: 0; padding: 24px 24px 18px; border-radius: 16px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-direction: column; gap: 10px; box-shadow: {SHADOW}">
{eyebrow('Booking help', '#E3BE74')}
<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 27px; line-height: 1.1; letter-spacing: -0.012em; color: #FFFFFF">Prefer to call?</h2>
<a class="fl" href="tel:{MAIN_TEL}" style="display: inline-flex; align-items: center; gap: 10px; align-self: flex-start; min-height: 44px; font-size: 22px; font-weight: 700; color: #FFFFFF; text-decoration: none">{ico('phone', 21, '#E3BE74', 1.8)}<span>{MAIN_PHONE}</span></a>
<p style="margin: 0; font-size: 14px; line-height: 1.45; color: #F4F1E8">Then press the number for your location:</p>
{call_list(dark=True, size=14.4)}
<p style="margin: 6px 0 0; font-size: 13.4px; line-height: 1.45; color: #F4F1E8">Hours differ by location. <a href="Contact.dc.html#locations" style="color: #E3BE74; font-weight: 600">See each location’s hours</a>.</p>
</section>'''
    w = WAITLIST
    wl = BY_KEY[w['location']]
    new = f'''<section id="new-patients" style="padding: 24px 30px 26px; border-radius: 16px; background: #FFFDF8; border: 1px solid {LINE}; box-shadow: {SHADOW}; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 18px 30px">
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 12px">
{eyebrow('New patients')}
{h2(w['heading'], 27)}
<p style="margin: 0; max-width: 640px; font-size: 15.4px; font-weight: 600; line-height: 1.45; color: {HEAD}">{w['question']}</p>
<p style="margin: 0; max-width: 640px; font-size: 15px; line-height: 1.5; color: {INK}">{w['how']} at <a href="tel:{MAIN_TEL}" style="font-weight: 700; color: {HEAD}">{MAIN_PHONE}</a>, press {wl['option']}, {w['when']}.</p>
<p style="margin: 0; max-width: 640px; font-size: 15px; line-height: 1.5; color: {INK}"><strong style="color: {HEAD}">You must:</strong> {w['must']}</p>
</div>
<div style="flex: 0 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 6px; padding: 16px 18px; border-radius: 12px; background: #F7F0E3; border: 1px solid {LINE}; font-size: 13.6px; line-height: 1.4; color: {INK}">
<span style="font-weight: 700; color: {HEAD}">{wl['name']}</span><span>{address(wl)}</span>
<a href="Contact.dc.html#{wl['key']}" style="font-weight: 600">Hours and staff at this clinic</a>
</div>
</section>'''
    s = header('')
    s += sub_hero([HOME, ('Schedule Your Visit', None)], 'Schedule Your Visit',
                  'Already a patient? Book online. New to IIPCT, or prefer to talk to someone? Call us.', eyebrow_txt='Appointments', lead_w=600)
    s += (f'<div style="{WRAP}; padding: 34px 48px 8px 83px; display: flex; flex-direction: column; gap: 26px">'
          f'<div style="display: flex; flex-wrap: wrap; align-items: stretch; gap: 26px 30px">{book}{call}</div>{new}</div>')
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
         h3('On this website', 18) + B(['This website has no forms. It does not ask for your name, contact details or health information.', 'If you email us, we receive your email address and your message.', 'If you sign up for the newsletter, Mailchimp collects your email address on its sign-up page.', f'Basic visit statistics, such as pages viewed. {ph("confirm analytics tool, or remove")}'])
         + h3('When you book or receive care', 18, 'margin-top: 8px') + P('Personal health information, such as your name, date of birth, health card number and health history. Online booking collects only what is needed to find your chart and confirm your appointment.')),
        ('use', 'How we use it', B(['To provide and coordinate your care.', 'To book, confirm and follow up on appointments.', 'To answer your questions.', 'To send the newsletter, if you asked for it. You can unsubscribe at any time.', 'To meet our legal and reporting obligations.'])),
        ('phipa', 'Your health information', P('IIPCT follows Ontario’s Personal Health Information Protection Act, 2004 (PHIPA). We collect, use and share your health information only as the Act allows, and with your consent where consent is required.')),
        ('share', 'Who we share it with', P('With the health care providers involved in your care, and with companies that run our systems under agreements that protect your information. We don’t sell personal information.')),
        ('services', 'Services we use', P('These services handle information on our behalf. Each has its own privacy policy.')
         + f'<ul style="margin: 2px 0 0; padding: 0; list-style: none; font-size: 14.4px; line-height: 1.45; border-bottom: 1px solid #E6D9BF">'
         + svc('Ocean', 'Online appointment booking for registered patients') + svc('Mailchimp', 'Newsletter sign-up and delivery') + svc('BambooHR', 'Job postings and applications')
         + svc('Google Maps', 'Maps of our locations, when you open a map link') + svc('Google Fonts', 'The typefaces this website uses. Your browser downloads them from Google.')
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
        col('Who We Are', [('About IIPCT', 'WhoWeAre.dc.html', 0), ('Our Team', 'Team.dc.html', 0), ('Career Opportunities', 'Careers.dc.html', 0), ('Board of Directors', 'Board.dc.html', 0),
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

def notfound():
    """404 page (GitHub Pages serves 404.html for any address it does not have)."""
    buttons = btn('Go to the Home Page', 'Main.dc.html', 'primary', 'house', False) + btn('See Every Page', 'SiteMap.dc.html', 'outline', None, True)
    s = header('')
    s += sub_hero([HOME, ('Page not found', None)], 'We could not find that page',
                  'The page may have moved, or the link may have a typo. Use the menu above, or one of these links.', buttons=buttons, title_size=44)
    s += f'''<div style="{WRAP}; padding: 30px 48px 48px 83px">{grid([
        link_list('Popular pages', [('Services', 'Services.dc.html'), ('Schedule Your Visit', 'Booking.dc.html'), ('Contact Us', 'Contact.dc.html')]),
        link_list('About us', [('Who We Are', 'WhoWeAre.dc.html'), ('Events &amp; Programs', 'Events.dc.html'), ('News &amp; Updates', 'News.dc.html')])], 300, 20, 'max-width: 760px; align-items: start')}</div>'''
    s += footer()
    return 'IIPCT — Page Not Found', s
