"""Search engines and sharing: the ONE table every page's title, description and share image come from, plus the
structured data (JSON-LD), the sitemap, robots.txt and the redirects from the old site's addresses.

To change how a page appears in Google or in a pasted link, edit its row in PAGES and regenerate:
    python3 tools/generator/export_site.py .
If a row's `heading` or `photo` changed, also re-make the share images (needs headless Chrome; see og_cards.py):
    python3 tools/generator/og_cards.py .

Everything a search engine reads is written for the real address, SITE_URL. The test copy on GitHub Pages is kept out
of search results by tools/publish-preview.sh, which also points its share tags at the test address.

Facts (names, phone, hours, addresses) come from facts.py only. Titles and descriptions say what each page says (for
Home, Services and its seven service pages, Events & Programs, News and the two news posts they were first written from
IIPCT's current site, iipct.org, and then re-read against those pages as built: each still holds).
A row's photo is the page's own lead photograph (the file its lib.photo() call names under site-img/); the share image
shows it, and its fourth field says what it shows (used in the share image's alt text).
"""
import html, json, re
from datetime import date, datetime
import facts

SITE_URL = 'https://iipct.org/'          # the real site (after the domain move). Never the test address.
SITE_NAME = 'IIPCT'
LOCALE = 'en_CA'
THEME_COLOR = '#17402A'                  # the site's forest green (skip link, hover fills, footer family)
ORG_ID = SITE_URL + '#organization'
OG_DIR = 'assets/img/og/'                # one 1200 x 630 JPEG per page, made by og_cards.py
OG_W, OG_H = 1200, 630
NOT_PUBLIC = ('404.html',)               # shown for missing addresses: no canonical, not in the sitemap

# ---------------------------------------------------------------- the table
# file -> title (15-60 characters, subject first, " | IIPCT" last), desc (70-160 characters), heading (the words on the
# share image), photo (the page's own real lead photograph under site-img/, or None for the default landscape card):
# (path, object-position, fit, what it shows), and for news posts the published/modified dates.
PAGES = {
    'index.html': dict(
        title='IIPCT | Indigenous primary care in southeastern Ontario',
        # old home page: hero line + "A Place for Good Medicine" text; five locations: facts.LOCATIONS
        desc='Tsi Kanonhkhwatsheríyo (IIPCT): wholistic care blending medicine, culture and wellness, '
             'with five locations across southeastern Ontario.',
        heading='Wholistic Care Blending Medicine, Culture, and Wellness',
        photo=('home/hero-team-thunder-bay.jpg', 'center center', 'contain',
               'five IIPCT team members standing together beside a pond, two of them in ribbon skirts')),
    'who-we-are.html': dict(
        title='Who We Are: our vision, mission and values | IIPCT',
        desc='Tsi Kanonhkhwatsheríyo offers inclusive healthcare with a focus on Indigenous communities. '
             'Read our vision, mission and values, and meet our team.',
        heading='Who We Are',
        photo=('about/team-group.jpg', 'center center', 'contain', 'IIPCT staff together in a group photo')),
    'our-team.html': dict(
        title='Our Team: meet the staff at each location | IIPCT',
        desc='Meet the IIPCT team: our leadership and the staff at the Tyendinaga, Kingston, Bancroft and '
             'Deseronto clinics and the Shannonville office.',
        heading='Our Team'),
    'careers.html': dict(
        title='Career Opportunities: join our team | IIPCT',
        desc='Current job openings at IIPCT, each with a link to the full job description and how to apply. '
             'Check back often for new opportunities.',
        heading='Career Opportunities',
        photo=('about/sage-leaves.jpg', 'center center', 'cover', 'a close-up of sage leaves')),
    'board-of-directors.html': dict(
        title='Board of Directors | IIPCT',
        desc='Meet the Board of Directors of Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care '
             'Team (IIPCT): its officers and members.',
        heading='Board of Directors',
        photo=('about/field-sunset.jpg', 'center 60%', 'cover', 'a sunset over a green field with a barn and a lone tree')),
    'bpso.html': dict(
        title='Best Practice Spotlight Organization (BPSO) | IIPCT',
        desc='IIPCT is one of 17 Indigenous-focused Best Practice Spotlight Organization (BPSO) sites in Ontario. '
             'Learn what that means and about our work.',
        heading='Best Practice Spotlight Organization',
        photo=('bpso/gathering-thunder-bay.jpg', '22% center', 'cover',
               'five women, two in ribbon skirts, by a pond at the BPSO gathering in Thunder Bay')),
    'services.html': dict(
        title='Services: cultural, medical and mental health care | IIPCT',
        # old services page: "four key programs": Cultural Services, Primary Medical Care, Mental Health Services
        # (short-term, adults 18 and older), Health Support Services
        desc='Four IIPCT programs: cultural services and traditional healing, primary medical care, short-term '
             'mental health services for adults, and health support.',
        heading='Services',
        photo=('services/clinic-sign.jpg', 'center center', 'contain',
               'an IIPCT clinic building with the Tsi Kanonhkhwatsheríyo sign and turtle logo')),
    'primary-medical-care.html': dict(
        title='Primary Medical Care: chronic and same-day care | IIPCT',
        # old primary care page: chronic disease care, same-day acute care, minor procedures, referrals, blood draws
        desc='Primary medical care at IIPCT: chronic disease care, same-day appointments for urgent concerns, '
             'minor procedures, referrals, blood draws and more.',
        heading='Primary Medical Care'),
    'immunization.html': dict(
        title='Publicly Funded Immunization Program | IIPCT',
        desc='IIPCT’s immunization program offers culturally safe vaccines for all ages. See which vaccines '
             'are publicly funded in Ontario, and when.',
        heading='Publicly Funded Immunization Program'),
    'well-baby-well-child.html': dict(
        title='Well Baby and Well Child Appointments | IIPCT',
        desc='Well baby and well child visits at IIPCT check your child’s growth, development and health, '
             'from 2 months to 6 years of age.',
        heading='Well Baby and Well Child Appointments'),
    'tb-testing.html': dict(
        title='TB Testing (Mantoux skin test) | IIPCT',
        # old TB information sheet: skin test (Mantoux Test), return to the clinic after 48-72 hours
        desc='Tuberculosis (TB) skin testing at IIPCT. Learn what TB is, how the Mantoux skin test works, and '
             'why you come back 48 to 72 hours later.',
        heading='TB Testing'),
    'advanced-foot-care.html': dict(
        title='Advanced Foot Care Services | IIPCT',
        desc='Advanced foot care from IIPCT nurses with specialized certification, for clients with diabetes '
             'or other conditions that affect foot health.',
        heading='Advanced Foot Care Services',
        photo=('services/foot-care.jpg', '70% center', 'cover', 'a nurse in a gown, mask and gloves caring for a client’s foot')),
    'diabetic-retinopathy-screening.html': dict(
        title='Diabetic Retinopathy Screening | IIPCT',
        desc='Monthly diabetic eye screening clinics at IIPCT. If you have diabetes and have not had an eye '
             'screening in the past year, call to book.',
        heading='Diabetic Retinopathy Screening',
        photo=('services/retinal-screening.jpg', 'center center', 'contain',
               'a nurse in teal scrubs using a retinal screening camera while a seated client looks into it')),
    'outreach-community-support.html': dict(
        title='Outreach and Community Support | IIPCT',
        desc='IIPCT brings care into the community: kidney, cancer, diabetes and eye screening, support for '
             'displaced communities, and a presence at powwows.',
        heading='Outreach and Community Support',
        photo=('services/mobile-clinic-van.jpg', 'center center', 'contain',
               'IIPCT’s green-and-white Mobile Health Clinic van, parked with its side door and awning open')),
    'events-programs.html': dict(
        title='Events & Programs: workshops and community events | IIPCT',
        # old events page: "Community Programs. Join workshops and events that promote learning, wellness, and connection."
        desc='Join IIPCT workshops and community events that promote learning, wellness and connection. '
             'See what is coming up and how to take part.',
        heading='Events & Programs',
        photo=('events/hero-fall-into-harvest.jpg', 'center center', 'contain',
               'seven IIPCT team members sitting together among corn stalks, hay bales and pumpkins at Fall Into Harvest')),
    'news.html': dict(
        title='News & Updates: stories and notices | IIPCT',
        desc='Stories, announcements and notices from Tsi Kanonhkhwatsheríyo Indigenous Interprofessional '
             'Primary Care Team (IIPCT).',
        heading='News & Updates'),
    'news-iphcc-awards.html': dict(
        title='Our Team Honoured at the IPHCC Awards | IIPCT',
        desc='Five IIPCT staff members were honoured at the 2025 Indigenous Primary Health Care Council (IPHCC) '
             'Member Awards, out of 18 awards province-wide.',
        heading='Our Team Honoured at the IPHCC Awards',
        photo=('news/iphcc-awards-2025.jpg', 'center center', 'contain',
               'three women at the IPHCC Member Awards, the one in the middle holding a framed award'),
        # old site post record (pages/our-team-honoured-at-the-iphcc-awards.md): published 2025-10-09, modified 2025-10-22
        article=dict(published='2025-10-09', modified='2025-10-22')),
    'news-breast-cancer-screening.html': dict(
        title='Together We’re Stronger: breast cancer screening | IIPCT',
        desc='19 mammograms were completed at IIPCT’s Together We’re Stronger breast cancer screening event, '
             'held together with three partners.',
        heading='Together We’re Stronger: Breast Cancer Screening Event',
        photo=('news/breast-screening-event-table.jpg', 'center center', 'contain',
               'the event table, with a pink cloth, three pots of flowers, framed artwork and gift bags'),
        # old site post record (pages/together-were-stronger-breast-cancer-screening-event.md)
        article=dict(published='2025-10-09', modified='2025-10-22')),
    'contact.html': dict(
        title='Contact Us: phone, email, hours and locations | IIPCT',
        desc=f'Call IIPCT at {facts.MAIN_PHONE}, one number for all five locations, or email us. '
             'Find each location’s address, hours and staff extensions.',
        heading='Contact Us',
        photo=('contact/deseronto-clinic.jpg', 'center center', 'cover', 'the Deseronto Clinic building')),
    'schedule-your-visit.html': dict(
        title='Schedule Your Visit: book online or call | IIPCT',
        desc=f'Registered IIPCT patients can book online through Ocean. New to IIPCT? Call {facts.MAIN_PHONE} '
             'and press the number for your location.',
        heading='Schedule Your Visit'),
    'privacy-policy.html': dict(
        title='Privacy Policy | IIPCT',
        desc='How IIPCT collects, uses and protects personal information, on this website and in our care.',
        heading='Privacy Policy'),
    'accessibility.html': dict(
        title='Accessibility | IIPCT',
        desc='IIPCT’s commitment to care, services and information that everyone can use, on this website and '
             'at our clinics.',
        heading='Accessibility'),
    'site-map.html': dict(
        title='Site Map | IIPCT',
        desc='Every page on the IIPCT website in one place: services, our team, events, news, contact details '
             'and more.',
        heading='Site Map'),
    '404.html': dict(
        title='Page Not Found | IIPCT',
        desc='We could not find that page on the IIPCT website. Use the menu or these links to find services, '
             'booking and contact details.',
        heading='Page Not Found'),
}

# ---------------------------------------------------------------- the old site's addresses
# Old folder-style address (iipct.org) -> the new page. The generator writes a small redirect page at each old path
# (instant refresh + canonical + a plain link, noindex) and tools/redirects/nginx-old-urls.conf (301s for nginx).
OLD_URLS = [
    ('services/', 'services.html'),
    ('events-programs/', 'events-programs.html'),
    ('contact-us/', 'contact.html'),
    ('who-we-are/', 'who-we-are.html'),
    ('who-we-are/career-page/', 'careers.html'),
    ('who-we-are/board-of-directors/', 'board-of-directors.html'),
    ('no-title/', 'bpso.html'),
    ('primary-medical-care-information/', 'primary-medical-care.html'),
    ('publicly-funded-immunization-program/', 'immunization.html'),
    ('well-baby-and-well-child-appointments/', 'well-baby-well-child.html'),
    ('tb-testing/', 'tb-testing.html'),
    ('advanced-foot-care-services/', 'advanced-foot-care.html'),
    ('diabetic-retinopathy-screening/', 'diabetic-retinopathy-screening.html'),
    ('outreach-and-community-support/', 'outreach-community-support.html'),
    ('our-team-honoured-at-the-iphcc-awards/', 'news-iphcc-awards.html'),
    ('together-were-stronger-breast-cancer-screening-event/', 'news-breast-cancer-screening.html'),
    ('events/', 'events-programs.html'),
]
# Whole old folders whose pages all go to one new page. A static host cannot match a prefix, so these exist only in
# the nginx file (the old calendar's single events lived at /event/<name>/).
OLD_PREFIXES = [('event/', 'events-programs.html')]


# ---------------------------------------------------------------- helpers
def url(file):
    """The real address of a page: index.html is the site root."""
    return SITE_URL if file == 'index.html' else SITE_URL + file

def og_image(file):
    return OG_DIR + file[:-5] + '.jpg'

def plain(s):
    """Text of an HTML snippet: tags removed, entities decoded, spaces collapsed."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def esc(s):
    return html.escape(s, quote=True)

def og_alt(file):
    row = PAGES[file]
    pic = row.get('photo')
    beside = f'beside a photograph of {pic[3]}' if pic else 'beside a drawing of pine trees, hills and the sun'
    return f'The IIPCT turtle emblem and the words “{row["heading"]}”, {beside}.'

def ld(obj):
    """One JSON-LD block on one line. '</' is escaped so the text can never close the script element."""
    return ('<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
            + '</script>')

def _tel(number):
    d = re.sub(r'\D', '', number)
    return f'+1-{d[-10:-7]}-{d[-7:-4]}-{d[-4:]}'


# ---------------------------------------------------------------- structured data
def organization():
    return {
        '@context': 'https://schema.org', '@type': 'MedicalOrganization', '@id': ORG_ID,
        'name': f'{facts.ORG_NAME} {facts.ORG_EN}', 'alternateName': facts.ORG_SHORT,
        'url': SITE_URL, 'logo': SITE_URL + 'assets/img/logo-emblem.png',
        'telephone': _tel(facts.MAIN_PHONE), 'email': facts.GENERAL_EMAIL,
        'sameAs': [facts.FACEBOOK_URL, facts.TIKTOK_URL],
    }

def website():
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE_URL + '#website', 'name': SITE_NAME,
            'alternateName': f'{facts.ORG_NAME} {facts.ORG_EN}', 'url': SITE_URL, 'publisher': {'@id': ORG_ID}}

DAY = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
WEEK = list(DAY)

def days(label):
    """'Tue – Thu' -> [Tuesday, Wednesday, Thursday]; 'Sat & Sun' -> [Saturday, Sunday]; 'Mon' -> [Monday]."""
    m = re.fullmatch(r'(\w{3})\s*[–-]\s*(\w{3})', label)
    if m:
        a, b = WEEK.index(m.group(1)), WEEK.index(m.group(2))
        return [DAY[d] for d in WEEK[a:b + 1]]
    return [DAY[d.strip()] for d in label.split('&')]

def location(loc):
    """One location from facts.LOCATIONS, with the same hours the Contact page prints (facts.hours_rows)."""
    addr = {'@type': 'PostalAddress', 'streetAddress': loc['street'], 'addressLocality': loc['town'],
            'addressRegion': loc['province'], 'addressCountry': 'CA'}
    if loc.get('postal'):
        addr['postalCode'] = loc['postal']
    hours = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': days(d), 'opens': o, 'closes': c}
             for d, o, c in loc['hours'] if o is not None]
    out = {'@context': 'https://schema.org', '@type': 'MedicalClinic' if loc['kind'] == 'Clinic' else 'LocalBusiness',
           '@id': url('contact.html') + '#' + loc['key'], 'name': plain(loc['name']),
           'url': url('contact.html') + '#' + loc['key'], 'telephone': _tel(facts.MAIN_PHONE)}
    if loc.get('fax'):
        out['faxNumber'] = _tel(loc['fax'])
    out.update({'email': loc['email'], 'address': addr, 'openingHoursSpecification': hours,
                'hasMap': loc['map_url'], 'parentOrganization': {'@id': ORG_ID}})
    return out

def breadcrumbs(file, body):
    """BreadcrumbList made from the breadcrumb trail the page shows (lib.crumbs), so the two always match."""
    m = re.search(r'<nav aria-label="Breadcrumb"[^>]*>(.*?)</nav>', body, re.S)
    if not m:
        return None
    items = []
    for a in re.finditer(r'<a [^>]*href="([^"#]*)[^"]*"[^>]*>(.*?)</a>|<span aria-current="page"[^>]*>(.*?)</span>', m.group(1), re.S):
        href, label, here = a.groups()
        if here is not None:
            items.append((plain(here), url(file)))
        else:
            items.append((plain(label), url(href)))
    if len(items) < 2:
        return None
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}

def photo_url(file):
    """The real address of the row's lead photograph (lib.photo copies site-img/<path> to assets/img/<path>), or None."""
    pic = PAGES[file].get('photo')
    return SITE_URL + 'assets/img/' + pic[0] if pic else None

def article(file, body=''):
    """The news post as a NewsArticle; its images are the share image and, when the page shows it, the lead photograph."""
    row = PAGES[file]
    a = row['article']
    pic = photo_url(file)
    images = [SITE_URL + og_image(file)] + ([pic] if pic and f'src="{pic[len(SITE_URL):]}"' in body else [])
    return {'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': row['heading'],
            'datePublished': a['published'], 'dateModified': a['modified'],
            'image': images, 'mainEntityOfPage': url(file),
            'author': {'@type': 'Organization', 'name': SITE_NAME, 'url': SITE_URL},
            'publisher': {'@id': ORG_ID}}

def _offset(day, hhmm):
    """UTC offset of Ontario local time on that day ('-05:00' in winter, '-04:00' in summer)."""
    try:
        from zoneinfo import ZoneInfo
        t = datetime.fromisoformat(f'{day}T{hhmm}').replace(tzinfo=ZoneInfo('America/Toronto'))
        s = t.strftime('%z')
        return s[:3] + ':' + s[3:]
    except Exception:
        return ''

def events(file, today=None):
    """Event blocks for the dated, upcoming events the Events page lists. They are read from the page module's EVENTS
    list (p_events.EVENTS: dicts with title, dates ['YYYY-MM-DD', ...], start/end 'HH:MM', place, place_short, text,
    anchor, tag). A page with no such list gets no Event markup. One block per date; past dates are left out.
    IIPCT is named as organizer only for its own events: an event the page tags as a partner's ('Partner event') is
    run by another organisation (IIPCT co-brands it), so its block names no organizer."""
    if file != 'events-programs.html':
        return []
    try:
        import p_events
    except Exception:
        return []
    today = today or date.today().isoformat()
    out = []
    for ev in getattr(p_events, 'EVENTS', None) or []:
        if not isinstance(ev, dict) or not (ev.get('title') and ev.get('dates') and ev.get('place')):
            continue
        for d in ev['dates']:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(d)) or d < today:
                continue
            e = {'@context': 'https://schema.org', '@type': 'Event', 'name': plain(ev['title'])}
            e['startDate'] = f'{d}T{ev["start"]}:00{_offset(d, ev["start"])}' if ev.get('start') else d
            if ev.get('start') and ev.get('end'):
                e['endDate'] = f'{d}T{ev["end"]}:00{_offset(d, ev["end"])}'
            e['eventAttendanceMode'] = 'https://schema.org/OfflineEventAttendanceMode'
            e['location'] = {'@type': 'Place', 'name': plain(ev.get('place_short') or ev['place']), 'address': plain(ev['place'])}
            if ev.get('text'):
                first = ev['text'][0] if isinstance(ev['text'], (list, tuple)) else ev['text']
                e['description'] = plain(first)
            if 'partner' not in str(ev.get('tag', '')).lower():
                e['organizer'] = {'@id': ORG_ID}
            e['url'] = url(file) + ('#' + ev['anchor'] if ev.get('anchor') else '')
            out.append(e)
    return out

def structured(file, body):
    """All JSON-LD blocks for a page, in order."""
    blocks = [organization()]
    if file == 'index.html':
        blocks.append(website())
    if file in NOT_PUBLIC:
        return blocks
    if file == 'contact.html':
        blocks += [location(l) for l in facts.LOCATIONS]
    b = breadcrumbs(file, body)
    if b:
        blocks.append(b)
    if PAGES[file].get('article'):
        blocks.append(article(file, body))
    blocks += events(file)
    return blocks


# ---------------------------------------------------------------- the <head>
def head_tags(file):
    """The search and sharing tags for a page, one per line (tools/publish-preview.sh rewrites four of them line by line)."""
    row = PAGES[file]
    title, desc, img = row['title'], row['desc'], SITE_URL + og_image(file)
    lines = [f'<title>{esc(title)}</title>', f'<meta name="description" content="{esc(desc)}">']
    if file not in NOT_PUBLIC:
        lines.append(f'<link rel="canonical" href="{url(file)}">')
    kind = 'article' if row.get('article') else 'website'
    lines += [f'<meta property="og:type" content="{kind}">',
              f'<meta property="og:site_name" content="{SITE_NAME}">',
              f'<meta property="og:locale" content="{LOCALE}">',
              f'<meta property="og:title" content="{esc(title)}">',
              f'<meta property="og:description" content="{esc(desc)}">']
    if file not in NOT_PUBLIC:
        lines.append(f'<meta property="og:url" content="{url(file)}">')
    lines += [f'<meta property="og:image" content="{img}">',
              f'<meta property="og:image:width" content="{OG_W}">',
              f'<meta property="og:image:height" content="{OG_H}">',
              f'<meta property="og:image:alt" content="{esc(og_alt(file))}">']
    if row.get('article'):
        lines += [f'<meta property="article:published_time" content="{row["article"]["published"]}">',
                  f'<meta property="article:modified_time" content="{row["article"]["modified"]}">']
    lines += ['<meta name="twitter:card" content="summary_large_image">',
              f'<meta name="twitter:title" content="{esc(title)}">',
              f'<meta name="twitter:description" content="{esc(desc)}">',
              f'<meta name="twitter:image" content="{img}">',
              f'<meta name="twitter:image:alt" content="{esc(og_alt(file))}">',
              f'<meta name="theme-color" content="{THEME_COLOR}">']
    return '\n'.join(lines)


# ---------------------------------------------------------------- root files
def sitemap(entries):
    """entries: [(file, 'YYYY-MM-DD', [image paths])] for the public pages."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for file, day, imgs in entries:
        out.append('<url>')
        out.append(f'<loc>{url(file)}</loc>')
        out.append(f'<lastmod>{day}</lastmod>')
        for i in imgs:
            out.append(f'<image:image><image:loc>{esc(SITE_URL + i)}</image:loc></image:image>')
        out.append('</url>')
    out.append('</urlset>')
    return '\n'.join(out) + '\n'

def robots():
    return f'# {SITE_URL}robots.txt\nUser-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n'

def redirect_page(old, new):
    depth = old.rstrip('/').count('/') + 1
    rel = '../' * depth + new
    name = esc(PAGES[new]['heading'])
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>This page has moved | IIPCT</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{url(new)}">
<meta http-equiv="refresh" content="0; url={rel}">
</head>
<body style="margin: 0; padding: 32px 20px; background: #FBF4EA; color: #17231D; font: 17px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif">
<p>This page has moved. Go to <a href="{rel}" style="color: #8C2B18; font-weight: 600">{name}</a>.</p>
</body>
</html>
'''

def nginx_conf():
    lines = ['# Old iipct.org addresses -> the new pages, as permanent (301) redirects.',
             '# Generated by tools/generator/export_site.py from OLD_URLS / OLD_PREFIXES in tools/generator/seo.py.',
             '# Include inside the iipct.org server block. The static redirect pages at the same paths do the same',
             '# job on hosts without server rules (GitHub Pages); these rules answer first when nginx serves the site.', '']
    for old, new in OLD_URLS:
        bare = '/' + old.rstrip('/')
        lines.append(f'location = {bare} {{ return 301 /{"" if new == "index.html" else new}; }}')
        lines.append(f'location = {bare}/ {{ return 301 /{"" if new == "index.html" else new}; }}')
    for old, new in OLD_PREFIXES:
        lines.append(f'location ^~ /{old} {{ return 301 /{new}; }}')
    return '\n'.join(lines) + '\n'
