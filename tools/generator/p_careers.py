"""Career Opportunities: the old iipct.org career page's own introduction (content/old-site/pages/career-page.md), its two
postings, and the two postings IIPCT shared on its Facebook page on November 17, 2026 (content/facebook/posts.json), each
with its real BambooHR link. Nothing else: no benefits list, hiring steps or staff quote (none of it has a source)."""
from lib import *
from p_team import swap, real_hero

# (title, place or None, note or None, link, source)
JOBS = [('Nurse Practitioner', 'Kingston', None, 'https://iipct.bamboohr.com/careers/27', 'old site career page'),
        ('Registered Practical Nurse', 'Deseronto Location', None, 'https://iipct.bamboohr.com/careers/30', 'old site career page'),
        ('Nurse Practitioner', None, 'Apply by November 30, 2026', 'https://iipct.bamboohr.com/careers/45', 'Facebook post, Nov 17 2026'),
        ('Addictions &amp; Mental Health Counsellor', 'Shannonville, Ontario', None, 'https://iipct.bamboohr.com/careers/44', 'Facebook post, Nov 17 2026')]
INTRO = ('Thank you for your interest in joining our team. We encourage you to check back regularly for future employment opportunities as they become available. '
         'We appreciate your interest in supporting the health and well-being of our community.')

def job_card(title, place, note, href, tone):
    meta = ''
    if place:
        meta += f'<span style="display: flex; align-items: center; gap: 8px">{pin_fill(17)}<span>{place}</span></span>'
    if note:
        meta += f'<span style="display: flex; align-items: center; gap: 8px">{ico("calendar", 17, "#A3301C", 1.8)}<span>{note}</span></span>'
    meta = (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 18px; font-size: 13.8px; font-weight: 600; color: {HEAD}">{meta}</div>' if meta else '')
    return (f'<article style="display: flex; align-items: flex-start; gap: 18px; padding: 18px 20px 20px; border-radius: 14px; {CARD}">'
            f'{circ("briefcase", tone, 54, 27, 1.5)}'
            f'<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 9px; padding-top: 2px">'
            f'<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 21.2px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}">{title}</h3>{meta}'
            f'{btn("View and Apply", href, "soft", "external", False, "sm", "margin-top: 4px; padding: 0 18px; gap: 10px; font-size: 13.4px; border-radius: 10px; min-height: 40px")}'
            f'</div></article>')

def page():
    buttons = btn('See Current Openings', '#jobs', 'primary', 'briefcase', True, 'md', 'padding: 0 24px; gap: 10px')
    s = header('careers')
    h = hero('hero-careers', 61.2, 334, 'Career<br>Opportunities', INTRO, buttons, sub='Join our Team!',
             h1_size=52, lead_size=17, lead_lh=1.45, lead_w=520, sub_size=26, pad='30px 0 38px 88px', gap=11, btn_mt=10, sq_mt=2, obj='center center')
    s += real_hero(h, 'hero-careers', 'about/sage-leaves.jpg')
    cards = ''.join(job_card(t, pl, nt, hr, tone) for (t, pl, nt, hr, src), tone in zip(JOBS, ['sage', 'rust', 'gold', 'forest']))
    s += f'''
<section id="jobs" style="scroll-margin-top: 16px; {WRAP}; padding: 30px 56px 0 68px">
<div class="p0" style="padding-left: 20px">{sec_head('Current Opportunities', 'Join Our Team', '', 31.6)}</div>
{p('Each posting opens on IIPCT’s hiring page, where you can read the full job description and apply.', 15, INK, 1.45, 'max-width: 640px; margin: 8px 0 0 20px', 't-b m0')}
<div class="g-cards gt2w" style="margin-top: 16px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 18px">{cards}</div>
</section>
<div style="margin-top: 30px">'''
    right = (btn('See Current Openings', '#jobs', 'light', None, True, 'md', 'padding: 0 24px; gap: 13px; font-size: 13px; min-height: 40px')
             + btn('Follow Us on Facebook', FACEBOOK_URL, 'light', 'external', False, 'md', 'padding: 0 24px; gap: 10px; font-size: 13px; min-height: 40px'))
    band = rust_band('briefcase', 'Ready to Make a Difference?', 'Check back regularly for new opportunities. We also share job postings on our Facebook page.', right, 'padding-right: 112px; padding-left: 122px', 14)
    s += swap(band, 'font-weight: 500; font-size: 24.8px;', 'font-weight: 500; font-size: 25.8px;') + '</div>'
    s += footer()
    return 'IIPCT — Career Opportunities', s
