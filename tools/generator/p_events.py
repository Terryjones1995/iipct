"""Events & Programs, built from IIPCT's own Facebook posts and flyers (collected 2026-11-22).
Every event below is traceable to a post and, where there is one, a flyer: see notes/static-news.md.
The Home page's "Upcoming Events" section is built from the same EVENTS list (home_events() below)."""
import re
from datetime import date
import lib
from lib import *
from p_news import update_href, tlink, nl_band, tg

PHONE = getattr(lib, 'MAIN_PHONE', '(343) 478-0196')
_tel = getattr(lib, 'MAIN_TEL', '+13434780196')        # frame's facts.MAIN_TEL is the bare number
TEL = _tel if _tel.startswith('tel:') else 'tel:' + _tel
SHANNONVILLE = 'Shannonville Office, 14 York Road, Unit 4, Shannonville'

# ------------------------------------------------------------------ the events (soonest first)
# Fields the source does not state are left out. Times are America/Toronto.
EVENTS = [
    dict(key='full-moon', anchor='full-moon-ceremony', tag='Ceremony', tone='sage',
         title='Full Moon Ceremony – Honouring Grandmother Moon', dates=['2026-11-24'], start='18:00', end=None,
         place=SHANNONVILLE, place_short='Shannonville Office',
         text=['Join us for an evening of ceremony, connection, and reflection as we come together to honour our relationship and connection to Grandmother Moon.',
               'What to bring: water, tobacco (if you have any), a dish to share for our potluck feast, and a skirt, if comfortable (not mandatory).'],
         who='Open to all who identify as women.',
         how=f'For more information, call <a href="{TEL}">{PHONE}</a> ext. 213 or email <a href="mailto:allison.loft@iipct.com">allison.loft@iipct.com</a>.',
         flyer=None,   # the flyer prints a community member's personal email address, so it is not shown here
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid0QwPa4n6sfmQ2SrjDh7Je8etV51B7svPfAM9pw1qgMMti5fs9gi5bo6vFW6SZhWDhl'),
    dict(key='massage', anchor='massage-appointments', tag='Appointments', tone='rust',
         title='Free Massage Appointments', dates=['2026-11-27'], start='09:00', end='12:00',
         place=SHANNONVILLE, place_short='Shannonville Office',
         when_note='The last of the November dates (Fridays, November 6, 13, 20 and 27).',
         text=['Students from the Loyalist College Massage Therapy Program are offering free 45–60 minute massage appointments at our Shannonville location throughout November.',
               'All appointments are completed by students under the supervision of a Registered Massage Therapist (RMT) Faculty Member.'],
         who='You must identify as Indigenous, live within an Indigenous household, or be a rostered patient of an IIPCT clinic.',
         how=f'Book online. Spaces are limited. For more information, call <a href="{TEL}">{PHONE}</a> ext. 106 or email <a href="mailto:kendra.garvin@iipct.com">kendra.garvin@iipct.com</a>.',
         register=('Book an appointment', 'https://bookings.cloud.microsoft/book/MassageTherapywithLoyalistCollege@iipct.com/'),
         partner='With the Loyalist College Massage Therapy Program.',
         flyer=('events/massage-appointments-november-2026.jpg', 640, 828, 'events/massage-appointments-november-2026-full.jpg'),
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid024x86h13wktRVYWMu1GtJzEfXwjRTjjUnumN4R8jHnoxadUqu58Z4UvKGVBgqr2Gel'),
    dict(key='candy-cane', anchor='candy-cane-lane-family-dance', tag='Partner event', tone='cream',
         title='Tobacco Awareness Candy Cane Lane Family Dance', dates=['2026-11-27'], start='18:00', end='20:00',
         place='Community Centre, 1807 York Road', place_short='Community Centre, 1807 York Road',
         when_note='Sensory-friendly hour from 5:00–6:00 pm, with the lights on and the music turned down.',
         text=['Put on your coziest Christmas pajamas and join us for an evening filled with music, laughter, holiday activities, and memories with your loved ones!',
               'Music with DJ Reese, winter crafts, pizza (while supplies last), a family photo keepsake, Christmas tree prizes, and smoking trivia and tobacco awareness activities. This is a drug- and alcohol-free event.'],
         who='Open to MBQ members and on-territory residents only. All youth must be accompanied by an adult.',
         how='For more information, contact Hannah Hill, CHR, at <a href="mailto:chrcwb@mbq-tmt.org">chrcwb@mbq-tmt.org</a>.',
         partner='Run with community partners.',
         flyer=('news/2026-11-02-candy-cane-lane-family-dance.jpg', 640, 853, 'news/2026-11-02-candy-cane-lane-family-dance-full.jpg'),
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid0cEYMWakrxb7BdDRuRRKNnJVcT8ck2uV9p4Fy5afRJQvjVGns2i39T4douAoXDuSEl'),
    dict(key='will-planning', anchor='will-planning-presentation', tag='Workshop', tone='tan',
         title='Will Planning Presentation', dates=['2026-11-30'], start='15:00', end='16:30',
         place=SHANNONVILLE, place_short='Shannonville Office',
         text=['Planning ahead is an important step in protecting yourself and your loved ones! Learn about the basics of wills and Powers of Attorney, why planning ahead matters, and what costs may be involved. There will also be an opportunity to ask questions.',
               'All attendees will be entered into a draw for a Life File Box filled with prizes. Light refreshments will be provided.'],
         who='IIPCT rostered clients and Indigenous community members, both on and off Territory.',
         how=f'Registration is required. For more information, contact Shelley Loft, Indigenous Lifelong Care Coordinator, at <a href="{TEL}">{PHONE}</a> ext. 115 or <a href="mailto:shelley.loft@iipct.com">shelley.loft@iipct.com</a>.',
         register=('Register online', 'https://forms.cloud.microsoft/r/7VMrU1rGAS'),
         partner='Facilitated by Queen’s Elder Law Clinic.',
         flyer=('news/2026-11-06-will-planning-presentation-shannonville.jpg', 640, 828, 'news/2026-11-06-will-planning-presentation-shannonville-full.jpg'),
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid02Usxxojs1KLimGCD6wkTrRoCrkBK1o1PmPQgxNTiA4wz4LLGPbrpiXNWefocFaJzAl'),
    dict(key='puzzle', anchor='santas-puzzle-palooza', tag='Community event', tone='tan',
         title='Santa’s Puzzle Palooza', dates=['2026-12-07'], start='18:00', end='20:00',
         place=SHANNONVILLE, place_short='Shannonville Office',
         when_note='Doors open at 5:00 pm. Turkey dinner will be available.',
         text=['Gather your team of 4 for a holiday-themed puzzle challenge. Teams race to finish the puzzle the fastest, and there are prizes to be won!'],
         who='Teams of 4. At least one team member must be an IIPCT rostered patient (have a doctor or nurse practitioner with one of our clinics).',
         status='Registration is closed (IIPCT’s post of November 16).', status_short='Registration is closed',
         how='For questions, contact Allison Loft at <a href="mailto:allison.loft@iipct.com">allison.loft@iipct.com</a> or 613-827-5178.',
         flyer=('news/2026-11-10-santa-s-puzzle-palooza-is-coming-get-your-team-r.jpg', 640, 828, 'news/2026-11-10-santa-s-puzzle-palooza-is-coming-get-your-team-r-full.jpg'),
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid025LjJNBvPmWdCbkW2RNDFaTJBp4R3YDjB3SK9MvcyAS5EszucokUvYvPmTDAQiir4l'),
    dict(key='social-songs', anchor='social-songs-dance', tag='Partner event', tone='cream',
         title='Social Songs &amp; Dance', dates=['2026-12-09', '2027-01-13', '2027-02-10', '2027-03-10', '2027-04-14'], start='18:00', end='20:00',
         place='Tsi Tyónnheht Onkwawén:na Language and Cultural Centre, 39 Salmon River Road, Shannonville (planned location)',
         place_short='Tsi Tyónnheht Onkwawén:na, Shannonville (planned location)',
         text=['Join us to learn social songs and dances! Whether you are joining for the first time or have been dancing for years, everyone is encouraged to take part.',
               'Bring rattles, plates, cups, or feast baskets if you have them. Ribbon skirts and/or ribbon shirts are encouraged. Bring a refillable water bottle. Indoor shoes must be worn. Light snacks and refreshments will be provided.'],
         who='Open to all MBQ members and community. Youth under 16 must be accompanied by an adult.',
         how='More details for each evening will be shared as they become available. For the October and November evenings, registration was encouraged and drop-ins were welcome. Questions: Tracey Gazley, <a href="mailto:traceyg@mbq-tmt.org">traceyg@mbq-tmt.org</a>, or Nancy Gourlay, <a href="mailto:events@kenhteke.org">events@kenhteke.org</a>.',
         partner='With Mohawk Family Services, the Family Wellbeing Program and the Tsi Tyónnheht Onkwawén:na Language and Cultural Centre.',
         flyer=('news/2026-10-10-social-songs-dance-save-the-dates.jpg', 640, 828, 'news/2026-10-10-social-songs-dance-save-the-dates-full.jpg'),
         fb='https://www.facebook.com/IIPCT.TMT/posts/pfbid02EZy84EEjsHTRaNvmEokSpHLLL3myNsWjpzfmi6TjrntRa9aAcuYThPVMSLxVnGrvl'),
]

# ------------------------------------------------------------------ formatting
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def t12(hm):
    h, m = map(int, hm.split(':'))
    return f'{h % 12 or 12}:{m:02d} {"am" if h < 12 else "pm"}'

def trange(s, e):
    if not e: return t12(s)
    a, b = t12(s), t12(e)
    if a[-2:] == b[-2:]: a = a[:-3]
    return f'{a}–{b}'

def dlong(iso, year=True):
    d = date.fromisoformat(iso)
    return f'{DAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}' + (f', {d.year}' if year else '')

def occurrences():
    """One row per date, soonest first: (date, event)."""
    rows = [(dt, e) for e in EVENTS for dt in e['dates']]
    return sorted(rows, key=lambda r: (r[0], r[1]['start'] or ''))

def when_text(e):
    if len(e['dates']) == 1:
        return f'{dlong(e["dates"][0])} · {trange(e["start"], e["end"])}'
    by_year = {}
    for d in e['dates']:
        by_year.setdefault(d[:4], []).append(d)
    parts = []
    for y, ds in by_year.items():
        names = [f'{MONTHS[int(d[5:7]) - 1]} {int(d[8:])}' for d in ds]
        parts.append((', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else names[0]) + f', {y}')
    return f'Wednesdays, {trange(e["start"], e["end"])}: ' + '; '.join(parts)

# ------------------------------------------------------------------ shared pieces (Home uses these too)
def site_hero(path, wh, alt, photo_w, min_h, h1, lead, buttons, obj='center center', h1_size=46, lead_size=18.6, lead_w=600, text_w=680,
              pad='36px 0 30px 83px', gap=14, lead_lh=1.32, btn_mt=8, lead_weight=450, sq_mt=0):
    """lib.hero() with a real photograph from site-img/ instead of a mock-up crop (same markup and classes)."""
    pic = photo(path, alt, f'position: absolute; top: 0; right: 0; width: {photo_w}%; height: 100%; object-fit: cover; object-position: {obj}',
                'hero-photo', wh[0], wh[1], lazy=False)
    return f'''
<section class="hero-sec" style="position: relative; min-height: {min_h}px">
{pic}
<div class="hero-fade" aria-hidden="true" style="position: absolute; top: 0; bottom: 0; left: {100 - photo_w}%; width: 7%; background: linear-gradient(90deg, #FBF3E8 0%, rgba(251, 243, 232, 0) 100%)"></div>
{branch(168, '#A5B195', 0.58, 'left: -84px; top: -12px; transform: rotate(8deg)')}
{branch(100, '#ADB89E', 0.5, 'left: -40px; bottom: -30px; transform: rotate(-12deg) scaleX(-1)')}
<div style="position: relative; z-index: 1; {WRAP}">
<div class="hero-txt" style="max-width: {text_w}px; padding: {pad}; display: flex; flex-direction: column; align-items: flex-start; gap: {gap}px">
<h1 class="h1" style="margin: 0; font-family: {SERIF}; font-weight: 680; font-size: {h1_size}px; line-height: 1.02; letter-spacing: -0.014em; color: {H1C}">{h1}</h1>
<span style="display: block; margin-top: {sq_mt}px">{SQUIGGLE}</span>
<p class="lead" style="margin: 0; max-width: {lead_w}px; font-size: {lead_size}px; font-weight: {lead_weight}; line-height: {lead_lh}; color: {INK}">{lead}</p>
<div class="btn-row" style="display: flex; flex-wrap: wrap; gap: 14px 23px; margin-top: {btn_mt}px">{buttons}</div>
</div>
</div>
</section>'''

def facebook_line(style=''):
    return (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 18px; {style}">'
            f'<p style="margin: 0; font-size: 14px; line-height: 1.45; color: {INK}">New dates are posted on IIPCT’s Facebook page first.</p>'
            f'{tlink("IIPCT on Facebook", FACEBOOK_URL)}</div>')

# ------------------------------------------------------------------ Events page
def date_tile(iso, big=False):
    d = date.fromisoformat(iso)
    w, ds = (84, 34) if big else (68, 27)
    return (f'<span aria-hidden="true" style="flex: none; width: {w}px; padding: 9px 0 10px; border-radius: 12px; background: #FDF8EE; border: 1px solid #D6BC86; '
            f'display: flex; flex-direction: column; align-items: center; gap: 4px; line-height: 1">'
            f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {RUST}">{MONTHS[d.month - 1][:3]}</span>'
            f'<span style="font-family: {SERIF}; font-size: {ds}px; font-weight: 700; color: {HEAD}">{d.day}</span>'
            f'<span style="font-size: 12px; font-weight: 600; color: {MUTED}">{DAYS[d.weekday()][:3]}</span></span>')

def meta_row(icon, html):
    return (f'<span style="display: flex; align-items: flex-start; gap: 10px; font-size: 14.2px; font-weight: 600; line-height: 1.4; color: {HEAD}">'
            f'{ico(icon, 18, RUSTI, 1.8, "margin-top: 1px")}<span style="min-width: 0">{html}</span></span>')

def fact(label, html):
    return (f'<div style="display: flex; flex-direction: column; gap: 3px"><dt style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {RUST}">{label}</dt>'
            f'<dd style="margin: 0; font-size: 14.2px; line-height: 1.5; color: {INK}">{html}</dd></div>')

def flyer_link(e):
    th, w, h, full = e['flyer']
    title = re.sub(r'<[^>]+>', '', e['title']).replace('&amp;', '&')
    return (f'<a class="card" href="/_site/{full}" style="flex: 0 0 150px; max-width: 100%; align-self: flex-start; display: flex; flex-direction: column; gap: 8px; padding: 8px 8px 6px; '
            f'border-radius: 12px; background: #FFFDF8; border: 1px solid {LINE}; color: {RUST}; text-decoration: none">'
            + photo(th, f'Flyer for {title}', 'width: 100%; height: auto; border-radius: 7px', '', w, h)
            + f'<span style="display: inline-flex; align-items: center; justify-content: center; gap: 7px; min-height: 32px; font-size: 13px; font-weight: 600">'
              f'<span style="text-decoration: underline; text-underline-offset: 3px">Full flyer</span>{ico("arrow", 14, RUST, 1.9)}</span></a>')

def event_card(e):
    paras = ''.join(f'<p style="margin: 0; font-size: 14.6px; line-height: 1.55; color: {INK}; max-width: 780px">{t}</p>' for t in e['text'])
    when = meta_row('calendar', when_text(e)) + (meta_row('clock', e['when_note']) if e.get('when_note') else '') + meta_row('pin', e['place'])
    facts = fact('Who can come', e['who']) + fact('How to take part', e['how'])
    status = (f'<p style="margin: 0; padding: 10px 14px; border-radius: 10px; background: #F1D5C8; border: 1px solid #D9A892; font-size: 14px; font-weight: 600; line-height: 1.4; color: #5A1E10">'
              f'{e["status"]}</p>') if e.get('status') else ''
    partner = f'<p style="margin: 0; font-size: 13.6px; font-style: italic; line-height: 1.45; color: {MUTED}">{e["partner"]}</p>' if e.get('partner') else ''
    actions = ''
    if e.get('register'):
        actions += btn(e['register'][0], e['register'][1], 'primary', 'calendar-check', False, 'md')
    actions += tlink('See the Facebook post', e['fb'])
    return f'''<article id="{e['anchor']}" style="scroll-margin-top: 16px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 18px 24px; padding: 22px 24px; border-radius: 16px; {CARD}">
{date_tile(e['dates'][0])}
<div style="flex: 1 1 260px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 11px">
<div style="display: flex; flex-wrap: wrap; gap: 8px">{tg(e['tag'], e['tone'])}</div>
{h3(e['title'], 23)}
<div style="display: flex; flex-direction: column; gap: 6px">{when}</div>
{paras}
<dl style="margin: 2px 0 0; display: grid; gap: 10px">{facts}</dl>
{status}{partner}
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 20px; margin-top: 2px">{actions}</div>
</div>
{flyer_link(e) if e.get('flyer') else ''}
</article>'''

# Programs that repeat: only what the dates prove (content/facebook/recurring-programs.md).
PROGRAMS = [
    ('feather', 'rust', 'Breakfast &amp; Beads', 'A monthly beading circle',
     'Saturday mornings, 9:00 am–12:00 pm, at 14 York Road, Unit 4, Shannonville, with a light breakfast and all supplies provided. In 2026 it ran on April 18, May 2, August 22, October 3 and November 14. You must register for each session, and spots fill quickly.'),
    ('sunrise', 'sage', 'Full Moon Ceremony', 'About once a month, near the full moon',
     'An evening ceremony at 14 York Road, Unit 4, Shannonville, for those who identify as women. In 2026: May 1, May 31, July 2, July 29, August 28, September 25, October 26 and November 24.'),
    ('hand-heart', 'gold', 'Free student massage', 'Friday mornings, in monthly blocks',
     'Students from the Loyalist College Massage Therapy Program, 9:00 am–12:00 pm at 14 York Road, Unit 4, in September, October and November 2026. Booking opens at 8:30 am on a set day and fills fast.'),
    ('leaf', 'forest', 'Visiting healers and seers', 'About every one to two months',
     'A traditional healer or seer visits for appointments in Shannonville, Bancroft and Kingston (in 2026: May, June, July, August and November). Priority goes to IIPCT rostered patients, and some sessions are only for them. Booking is by phone with our team.'),
    ('people', 'sage', 'Lifelong Care workshops', 'About one a month',
     'Often the same workshop at three locations a week apart: advance care planning, caregiver support, death doula training, scrapbooking with the Alzheimer Society, and will planning. Ask Shelley Loft, Indigenous Lifelong Care Coordinator, ext. 115.'),
    ('heart-pulse', 'rust', 'Community cancer screening days', 'Spring and fall',
     'In May and October 2026, from 4:30–7:00 pm at our clinics, for people without a family doctor or nurse practitioner. Booked by phone.'),
    ('sprout', 'gold', 'Strawberry Social', 'Every June',
     'Held each June since 2023. The 4th Annual Strawberry Social was on June 25, 2026, at the Deseronto Community Centre, with social songs and dances, an Indigenous makers market, and free strawberries and ice cream.'),
    ('scales', 'forest', 'Annual General Meeting', 'Once a year',
     'The 5th Annual General Meeting of Tsi Kanonhkhwatsheríyo was held online on September 18, 2026.'),
]

def program_card(icon, tone, title, pattern, text):
    return (f'<div style="display: flex; align-items: flex-start; gap: 14px; padding: 16px 18px 17px 16px; border-radius: 14px; {CARD}">'
            f'{circ(icon, tone, 48, 25, 1.5)}<div style="min-width: 0; display: flex; flex-direction: column; gap: 5px">'
            f'{h3(title, 18)}<span style="font-size: 13px; font-weight: 700; color: {RUST}">{pattern}</span>'
            f'<p style="margin: 0; font-size: 13.8px; line-height: 1.5; color: {INK}">{text}</p></div></div>')

# Recently: the last few past events, each linking to its post on the News page.
RECENT = [
    ('Creating Memories: A Scrapbooking Workshop', 'November 5 (Bancroft), November 12 (Kingston) and November 19 (Shannonville), 2026', 35),
    ('Social Songs &amp; Dance', 'Wednesday, November 18, 2026', 32),
    ('Community Connections Sharing Circle', 'Sunday, November 15, 2026', 22),
    ('Battle of the Bowls', 'Friday, November 13, 2026', 5),
    ('Menopause Wellness Workshop', 'Tuesday, November 10, 2026', 25),
    ('Fall Into Harvest', 'Thursday, October 15, 2026', 29),
]

def page():
    buttons = (btn('See Upcoming Events', '#upcoming', 'primary', 'calendar-check', True, 'md')
               + btn('News &amp; Updates', 'News.dc.html', 'outline', 'news', False, 'md'))
    s = header('events')
    s += site_hero('events/hero-fall-into-harvest.jpg', (1413, 916),
                   'Seven IIPCT team members sitting together among corn stalks, hay bales and pumpkins on the day of Fall Into Harvest, October 15, 2026',
                   61.5, 290, 'Events &amp; Programs', 'Join workshops and events that promote learning, wellness, and connection.', buttons,
                   obj='center 45%', h1_size=52, lead_size=21.3, lead_lh=1.33, pad='24px 0 34px 80px', gap=10, btn_mt=10, sq_mt=2, lead_w=520)
    cards = '\n'.join(event_card(e) for e in EVENTS)
    s += f'''
<section id="upcoming" style="scroll-margin-top: 16px; {WRAP}; padding: 30px 56px 0 56px">
{sec_head('Upcoming Events', 'Join Us at an Upcoming Event', '', 30)}
<p style="margin: 10px 0 0; max-width: 760px; font-size: 15px; line-height: 1.5; color: {INK}">Soonest first. Each event says who it is for and how to take part, in IIPCT’s own words.</p>
<div style="margin-top: 18px; display: flex; flex-direction: column; gap: 18px">
{cards}
</div>
{facebook_line('margin-top: 12px')}
</section>
<section id="programs" style="scroll-margin-top: 16px; {WRAP}; padding: 34px 56px 0 56px">
{sec_head('Programs That Repeat', 'Regular Programs', '', 28.6)}
<p style="margin: 10px 0 0; max-width: 760px; font-size: 15px; line-height: 1.5; color: {INK}">These programs come back regularly. The next dates are posted on Facebook when they are set.</p>
{grid([program_card(*pr) for pr in PROGRAMS], 330, 14, 'margin-top: 16px')}
</section>
<section id="recent" style="scroll-margin-top: 16px; {WRAP}; padding: 34px 56px 0 56px">
{sec_head('Recently', 'Recent Events', tlink('All news and updates', 'News.dc.html', 'arrow', 14.4), 28.6)}
<ul style="margin: 14px 0 0; padding: 4px 22px; list-style: none; border-radius: 14px; {CARD}">
{''.join(f'<li style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 2px 18px; padding: 8px 0; {"" if i == 0 else "border-top: 1px solid #E6D9BF"}">'
         f'<span style="flex: 1 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 2px"><span style="font-size: 15px; font-weight: 700; line-height: 1.3; color: {HEAD}">{t}</span>'
         f'<span style="font-size: 13.6px; line-height: 1.4; color: {MUTED}">{d}</span></span>{tlink("Read the post", update_href(n), "arrow", 13.6)}</li>' for i, (t, d, n) in enumerate(RECENT))}
</ul>
</section>
<div style="margin-top: 40px">{nl_band('Get our news, events and programs by email. Sign up on our newsletter page.')}</div>'''
    s += footer(150, '', True)
    return 'IIPCT — Events &amp; Programs', s

# ------------------------------------------------------------------ Home: "Up next" + "Coming up", kept right by a small script
HOME_SCRIPT = """<script>
(function () {
  var box = document.getElementById('ev-home');
  if (!box) return;
  var p = {};
  new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
  var today = p.year + '-' + p.month + '-' + p.day, now = today + 'T' + p.hour + ':' + p.minute;
  var utc = function (s) { var a = s.split('-'); return Date.UTC(+a[0], a[1] - 1, +a[2]); };
  var rows = box.querySelectorAll('[data-end]'), next = null, i;
  for (i = 0; i !== rows.length; i++) {
    var over = rows[i].getAttribute('data-end') < now;
    if (over) rows[i].style.display = 'none';
    else if (!next) next = rows[i];
  }
  if (next) {
    var card = document.getElementById('next-' + next.getAttribute('data-key'));
    var diff = (utc(next.getAttribute('data-day')) - utc(today)) / 864e5;
    var label = diff === 0 ? 'Today' : diff === 1 ? 'Tomorrow' : diff > 1 && diff < 7 ? card.getAttribute('data-wd') : '';
    var lab = card.querySelector('.ev-when');
    if (label) { lab.textContent = label; lab.parentNode.hidden = false; }
    card.hidden = false;
    document.getElementById('ev-next-col').hidden = false;
    next.style.display = 'none';
  } else {
    document.getElementById('ev-none').hidden = false;
  }
  var days = box.querySelectorAll('[data-group]'), shown = 0;
  for (i = 0; i !== days.length; i++) {
    var vis = 0, r = days[i].querySelectorAll('[data-end]');
    for (var j = 0; j !== r.length; j++) if (r[j].style.display !== 'none') vis++;
    if (!vis || shown === 5) days[i].style.display = 'none';
    else shown++;
  }
  if (!shown) document.getElementById('ev-list-head').style.display = 'none';
})();
</script>"""

def home_events():
    occ = occurrences()
    cards, groups, last = '', '', None
    for dt, e in occ:
        key = f'{e["key"]}-{dt}'
        end = f'{dt}T{e["end"] or "23:59"}'
        href = f'events-programs.html#{e["anchor"]}'   # final file name: the exporter renames only whole-page links
        d = date.fromisoformat(dt)
        when = f'{dlong(dt)} · {trange(e["start"], e["end"])}'
        closed = e.get('status_short')
        closed_card = (f'<p style="margin: 2px 0 0; padding: 7px 12px; border-radius: 10px; background: #F1D5C8; border: 1px solid #D9A892; '
                       f'font-size: 13.6px; font-weight: 600; line-height: 1.4; color: #5A1E10">{closed}.</p>') if closed else ''
        closed_row = f'<span style="font-size: 13px; font-weight: 700; line-height: 1.35; color: #8A2E17">{closed}</span>' if closed else ''
        cards += (f'<div id="next-{key}" data-wd="{DAYS[d.weekday()]}" hidden>'
                  f'<div style="display: flex; flex-wrap: wrap; align-items: flex-start; gap: 14px 18px; padding: 20px 22px; border-radius: 16px; {CARD}">{date_tile(dt, True)}'
                  f'<div style="flex: 1 1 280px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 7px">'
                  f'<span style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">{eyebrow("Up next")}'
                  f'<span hidden><span class="ev-when" style="display: inline-block; padding: 4px 10px 3px; border-radius: 999px; background: #17402A; color: #FFFFFF; font-size: 12px; font-weight: 700; line-height: 1.2"></span></span></span>'
                  f'{h3(e["title"], 22)}'
                  f'{meta_row("calendar", when)}{meta_row("pin", e["place_short"])}{closed_card}'
                  f'<p style="margin: 2px 0 0; font-size: 14px; line-height: 1.5; color: {INK}">{e["text"][0]}</p>'
                  f'<p style="margin: 0; font-size: 13.6px; line-height: 1.45; color: {MUTED}"><strong style="color: {HEAD}">Who can come:</strong> {e["who"]}</p>'
                  f'{tlink("Event details", href, "arrow", 14)}</div></div></div>')
        if dt != last:
            if last: groups += '</ul></li>'
            groups += (f'<li data-group="{dt}" style="display: flex; flex-direction: column; gap: 2px; padding: 10px 0 8px; border-top: 1px solid #E6D9BF">'
                       f'<span style="font-size: 12.4px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {RUST}">{dlong(dt)}</span>'
                       f'<ul style="margin: 0; padding: 0; list-style: none">')
            last = dt
        groups += (f'<li data-end="{end}" data-day="{dt}" data-key="{key}">'
                   f'<a class="tl" href="{href}" style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 14px; min-height: 40px; padding: 6px 0; text-decoration: none; color: {INK}">'
                   f'<span style="flex: 0 0 128px; font-size: 13.6px; font-weight: 600; color: {MUTED}">{trange(e["start"], e["end"])}</span>'
                   f'<span style="flex: 1 1 220px; min-width: 0; display: flex; flex-direction: column; gap: 1px">'
                   f'<span style="font-size: 15px; font-weight: 700; line-height: 1.3; color: {HEAD}; text-decoration: underline; text-decoration-color: #D6BC86; text-underline-offset: 4px">{e["title"]}</span>'
                   f'<span style="font-size: 13.4px; line-height: 1.35; color: {MUTED}">{e["place_short"]}</span>{closed_row}</span></a></li>')
    if last: groups += '</ul></li>'
    today = date.today().isoformat()
    none_hidden = '' if not any(dt >= today for dt, _ in occ) else ' hidden'
    return f'''
<section id="ev-home" style="{WRAP}; padding: 26px 72px 0 76px">
{sec_head('Events &amp; Programs', 'Upcoming Events', tlink('View all events', 'Events.dc.html', 'arrow', 14.4), 30.2)}
<div style="margin-top: 15px; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 22px 30px">
<div id="ev-next-col" hidden style="flex: 1 1 380px; min-width: 0">{cards}</div>
<div style="flex: 1.3 1 400px; min-width: 0">
<h3 id="ev-list-head" style="margin: 0 0 4px; font-family: {SERIF}; font-weight: 700; font-size: 19px; line-height: 1.2; color: {HEAD}">Coming up</h3>
<ul style="margin: 0; padding: 0; list-style: none; border-bottom: 1px solid #E6D9BF">{groups}</ul>
<div id="ev-none"{none_hidden}>{note('calendar', 'No upcoming events are posted right now', 'Our regular programs are on the <a href="events-programs.html#programs">Events &amp; Programs page</a>.', 'cream', 'margin-top: 12px')}</div>
</div>
</div>
{facebook_line('margin-top: 12px')}
{HOME_SCRIPT}
</section>'''
