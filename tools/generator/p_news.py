"""News & Updates, plus the two posts that exist on the live site."""
from lib import *

HOME = ('Home', 'Main.dc.html')
NEWS = ('News &amp; Updates', 'News.dc.html')
AWARDS = 'NewsIPHCCAwards.dc.html'
BREAST = 'NewsBreastScreening.dc.html'

def meta(date, by='IIPCT'):
    return (f'<span style="display: inline-flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; font-size: 13px; font-weight: 600; color: {MUTED}">'
            f'<span style="display: inline-flex; align-items: center; gap: 7px">{ico("calendar", 15, RUSTI, 1.8)}{date}</span>'
            f'<span aria-hidden="true" style="width: 1px; height: 13px; background: #C9B691"></span><span>{by}</span></span>')

def story(date, cat, tone, title, text, href):
    return (f'<article class="card" style="display: flex; flex-direction: column; align-items: flex-start; gap: 11px; padding: 22px 24px 22px; border-radius: 14px; {CARD}">'
            f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px">{tag(cat, tone)}{meta(date)}</div>'
            f'<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 23px; line-height: 1.12; letter-spacing: -0.018em; color: {HEAD}">'
            f'<a href="{href}" style="color: {HEAD}; text-decoration: none">{title}</a></h3>'
            f'<p style="margin: 0; font-size: 14.4px; line-height: 1.5; color: {INK}">{text}</p>'
            f'{textlink("Read the story", href, 14, "margin-top: auto; padding-top: 4px; gap: 9px")}</article>')

def notice(cat, tone, title, when, href='#', link='View flyer'):
    return (f'<li style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; padding: 13px 0; border-top: 1px solid #E6D9BF">'
            f'<span style="flex: 0 0 76px">{tag(cat, tone)}</span>'
            f'<span style="flex: 1 1 260px; min-width: 0; font-size: 15px; font-weight: 600; line-height: 1.3; color: {HEAD}">{title}</span>'
            f'<span style="flex: 0 0 150px; font-size: 13.4px; color: {MUTED}">{when}</span>'
            f'{textlink(link, href, 13.2, "gap: 7px")}</li>')

def press(source, date, title, text, href):
    return (f'<li style="display: flex; flex-direction: column; align-items: flex-start; gap: 5px; padding: 14px 0; border-top: 1px solid #E6D9BF">'
            f'<span style="font-size: 11.4px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {RUST}">{source} · {date}</span>'
            f'<span style="font-size: 15px; font-weight: 700; line-height: 1.28; color: {HEAD}">{title}</span>'
            f'<span style="font-size: 13.4px; line-height: 1.45; color: {INK}">{text}</span>'
            f'{ext("Read the article", href, 13.2)}</li>')

def follow_card():
    return (f'<div style="padding: 22px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-direction: column; align-items: flex-start; gap: 11px; box-shadow: {SHADOW}">'
            f'{eyebrow("Day to day", "#E3BE74")}'
            f'<h2 style="margin: 0; font-family: {SERIF}; font-weight: 500; font-size: 25px; line-height: 1.1; letter-spacing: -0.012em; color: #FFFFFF">Follow IIPCT</h2>'
            f'<p style="margin: 0; font-size: 13.8px; line-height: 1.48; color: #F4F1E8">Follow along for flyers, notices and updates between newsletters.</p>'
            f'<div style="margin-top: 2px">{social_row(dark=True, label="")}</div></div>')

def aside_news(extra=''):
    nl = (f'<div style="padding: 20px 22px 22px; border-radius: 14px; {CARD}; display: flex; flex-direction: column; align-items: flex-start; gap: 9px">{h3("Newsletter", 19)}'
          f'<p style="margin: 0; font-size: 13.6px; line-height: 1.45; color: {INK}">News, events and programs, sent by email.</p>'
          f'{btn("Sign Up", NEWSLETTER_URL, "outline", "mail", True, "sm", "margin-top: 4px")}</div>')
    return f'<aside style="flex: 1 1 320px; max-width: 400px; min-width: 0; display: flex; flex-direction: column; gap: 18px">{follow_card()}{extra}{nl}</aside>'

# ------------------------------------------------------------------ listing
def news():
    stories = grid([
        story('October 9, 2025', 'Recognition', 'tan', 'Our Team Honoured at the IPHCC Awards',
              'IIPCT staff received 5 of the 18 awards at the 2025 IPHCC Member Awards, for work in community innovation, traditional healing, nursing and medicine.', AWARDS),
        story('October 9, 2025', 'Community health', 'sage', 'Together We’re Stronger: Breast Cancer Screening Event',
              'Nineteen mammograms completed, with the Mohawks of the Bay of Quinte, the South East Indigenous Cancer Program and Kingston Health Sciences Centre.', BREAST),
    ], 330, 18)
    notices = (f'<ul style="margin: 0; padding: 0 22px; list-style: none; border-radius: 14px; {CARD}">'
               + notice('Health', 'rust', 'Cancer Screening Clinics', 'Fall 2026').replace('border-top: 1px solid #E6D9BF', 'border-top: none', 1)
               + notice('Event', 'tan', 'Scrapbooking Workshop', 'November 2026')
               + notice('Event', 'tan', 'Social Songs and Dances', 'October 14, 2026')
               + notice('Event', 'tan', 'Full Moon', 'October 2026')
               + notice('Event', 'tan', 'Harvest Social and Vendor Market', 'Fall 2026')
               + notice('Event', 'tan', 'Community Closet Clearout', '2026')
               + notice('Event', 'tan', 'Battle of the Bowls', 'See flyer')
               + notice('Notice', 'sage', 'Deseronto Clinic', '2026')
               + notice('Notice', 'sage', 'Mamawi Room Survey', 'See flyer')
               + notice('BPSO', 'cream', '“Building Bridges Together” gathering, Thunder Bay', 'June 2026', 'BPSO.dc.html', 'About BPSO')
               + notice('Hiring', 'cream', 'Nurse Practitioner, Kingston', 'Open now', 'Careers.dc.html', 'See posting')
               + notice('Hiring', 'cream', 'Registered Practical Nurse, Deseronto', 'Open now', 'Careers.dc.html', 'See posting')
               + '</ul>')
    fb = (f'<div style="padding: 22px 24px; border-radius: 14px; border: 1px dashed #B9AA86; background: #F3ECDB; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 24px">'
          f'<p style="margin: 0; flex: 1 1 320px; font-size: 14.4px; line-height: 1.5; color: {INK}">[Posts from the IIPCT Facebook page, last six months. Each one becomes a story here, with its own date, text and photos.]</p>'
          f'{social_row(label="See them on")}</div>')
    coverage = (f'<div style="padding: 20px 22px 8px; border-radius: 14px; {CARD}">{h3("In the news", 19)}'
                f'<ul style="margin: 12px 0 0; padding: 0; list-style: none">'
                + press('Kingstonist', 'Apr 24, 2026', 'More than $2.1 million for a Deseronto clinic and mobile care',
                        'Announced on Tyendinaga Mohawk Territory, and expected to connect about 2,100 people to primary care.',
                        'https://www.kingstonist.com/news/new-deseronto-clinic-mobile-care-expansion-aim-to-connect-2100-patients-in-tyendinaga/')
                + press('Napanee Today', 'Apr 27, 2026', 'Province expands primary care access in Tyendinaga',
                        'Funding to grow IIPCT’s primary care, allied health and traditional healing services.', 'https://www.napaneetoday.ca/2026/04/27/97117/')
                + press('Bancroft This Week', 'Dec 10, 2025', 'Bancroft clinic opens its doors',
                        'Taking new patients who identify as Indigenous, have an Ontario health card and have no primary care provider.',
                        'https://www.bancroftthisweek.com/indigenous-health-clinic-offers-culturally-grounded-care-in-bancroft/')
                + '</ul></div>')
    main = (section('Stories', stories, 'From IIPCT')
            + section('Notices and events', notices, 'Past six months')
            + section('From Facebook', fb))
    s = header('events')
    s += sub_hero([HOME, ('News &amp; Updates', None)], 'News &amp; Updates', 'Stories, announcements and notices from Tsi Kanonhkhwatsheríyo.',
                  'evt-featured', 'A canoe on a misty lake at sunrise', 'News', pos='center center')
    s += (f'<div style="{WRAP}; padding: 34px 48px 8px 83px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 34px 48px">'
          f'<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 32px">{main}</div>{aside_news(coverage)}</div>')
    s += f'<div style="margin-top: 40px">{newsletter()}</div>'
    s += footer()
    return 'IIPCT — News &amp; Updates', s

# ------------------------------------------------------------------ posts
def post(title, date, cat, tone, lead, body, other):
    more = link_list('More news', [other, ('All news and updates', 'News.dc.html')])
    s = header('events')
    s += sub_hero([HOME, NEWS, (cat, None)], title, lead, extra=f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px">{tag(cat, tone)}{meta(date)}</div>',
                  title_size=42, lead_w=700)
    s += (f'<div style="{WRAP}; padding: 34px 48px 8px 83px; display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 34px 56px">'
          f'<article style="flex: 999 1 560px; min-width: 0; max-width: 780px; display: flex; flex-direction: column; gap: 22px">{body}'
          f'<div style="padding-top: 6px">{textlink("Back to News &amp; Updates", "News.dc.html", 14.2, "gap: 9px", "arrow-left")}</div></article>'
          f'{aside_news(more)}</div>')
    s += f'<div style="margin-top: 40px">{newsletter()}</div>'
    s += footer()
    return s

def post_awards():
    winners = [('Integrated Care / Community Innovation', 'Jamie Kring'), ('Traditional Healing and Wellness', 'Allison Loft'), ('Staff / Co-worker Recognition', 'Kristine Canty'),
               ('Nursing Recognition, Merit (RPN)', 'Sierra Bedford'), ('Recognition of Excellence, Physicians Honoured', 'Kimberley Edwards')]
    rows = ''.join(f'<li style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 20px; padding: 13px 0; {"" if i == 0 else "border-top: 1px solid #E6D9BF"}">'
                   f'{ico("award", 22, RUSTI, 1.5)}<span style="flex: 1 1 260px; min-width: 0; font-size: 14.4px; color: {INK}">{a}</span>'
                   f'<span style="flex: 0 0 auto; font-family: {SERIF}; font-weight: 700; font-size: 18px; letter-spacing: -0.012em; color: {HEAD}">{n}</span></li>' for i, (a, n) in enumerate(winners))
    stat = (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 26px; padding: 20px 26px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF">'
            f'<span style="font-family: {SERIF}; font-weight: 600; font-size: 46px; line-height: 1; color: #E3BE74">5 of 18</span>'
            f'<span style="flex: 1 1 280px; font-size: 15px; line-height: 1.45; color: #F4F1E8">awards went to IIPCT staff at the 2025 Indigenous Primary Health Care Council (IPHCC) Member Awards.</span></div>')
    body = (prose('The Indigenous Primary Health Care Council represents 32 member locations. At its 2025 Member Awards, five people from our team were recognized for their work.', size=15.6)
            + stat + section('Our award recipients', f'<ul style="margin: 0; padding: 4px 24px; list-style: none; border-radius: 14px; {CARD}">{rows}</ul>', size=25)
            + photo_ph('Photo from the awards<br>(from the original post)', '16 / 6'))
    return 'IIPCT — Our Team Honoured at the IPHCC Awards', post('Our Team Honoured at the IPHCC Awards', 'October 9, 2025', 'Recognition', 'tan',
                                                                 'Five of the 18 awards at this year’s IPHCC Member Awards went to people on our team.', body,
                                                                 ('Together We’re Stronger: Breast Cancer Screening Event', BREAST))

def post_breast():
    prow = lambda n, first=False: (f'<li style="display: flex; align-items: center; gap: 16px; padding: 13px 0; {"" if first else "border-top: 1px solid #E6D9BF"}">'
                                   f'{ico("handshake", 24, RUSTI, 1.5)}<span style="font-family: {SERIF}; font-weight: 700; font-size: 18px; letter-spacing: -0.012em; color: {HEAD}">{n}</span></li>')
    partners = (f'<ul style="margin: 0; padding: 4px 24px; list-style: none; border-radius: 14px; {CARD}">' + prow('Mohawks of the Bay of Quinte', True)
                + prow('South East Indigenous Cancer Program') + prow('Kingston Health Sciences Centre') + '</ul>')
    stat = (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 26px; padding: 20px 26px; border-radius: 14px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF">'
            f'<span style="font-family: {SERIF}; font-weight: 600; font-size: 46px; line-height: 1; color: #E3BE74">19</span>'
            f'<span style="flex: 1 1 280px; font-size: 15px; line-height: 1.45; color: #F4F1E8">mammograms completed at the event.</span></div>')
    thanks = note('info', 'Thank-yous', '[The original post thanks the staff and partners who made the day happen, by name. That list goes here.]', 'gold')
    due = note('calendar-check', 'Due for a screening?', 'Call your clinic, or see what our outreach team offers. ' + textlink('Outreach &amp; Community Support', 'Outreach.dc.html', 14, 'gap: 8px'), 'sage')
    body = (prose('Nineteen mammograms were completed at our breast cancer screening event, run together with three partners.', size=15.6)
            + stat + section('Our partners', partners, size=25) + thanks
            + photo_ph('Photo from the event<br>(from the original post)', '16 / 6') + due)
    return 'IIPCT — Together We’re Stronger: Breast Cancer Screening Event', post('Together We’re Stronger: Breast Cancer Screening Event', 'October 9, 2025', 'Community health', 'sage',
                                                                                   'Nineteen mammograms completed, with three partners working alongside our team.', body,
                                                                                   ('Our Team Honoured at the IPHCC Awards', AWARDS))
