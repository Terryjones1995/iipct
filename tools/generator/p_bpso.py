"""BPSO: what the old iipct.org BPSO page says (content/old-site/pages/no-title.md): one of 17 Indigenous-focused BPSO sites
(Cohort 4 on RNAO's map), working toward integrating selected RNAO Best Practice Guidelines, the one guideline named,
the steering committee, and the two BPSO events with their photographs."""
from lib import *
from p_team import TEAM, TEAM_PAGE

RNAO_BPSO = 'https://rnao.ca/bpg/bpso'
GUIDELINE = 'Promoting Smoking Reduction and Cessation with Indigenous Peoples of Reproductive Age and Their Communities'
ABOUT = ('The Best Practice Spotlight Organization® (BPSO®) designation is a longstanding knowledge translation strategy that helps optimize health outcomes at the '
         'individual, organizational and health system levels. This program gives health service and academic organizations the opportunity to formally partner with '
         'RNAO – or an approved “Host” organization – to achieve “designation” as a BPSO. This internationally-renowned program’s strategic approach has been proven to '
         'trigger evidence-based cultures, improve patient experience and health outcomes, lower cost of care by preventing complications, and enrich staff satisfaction.')
BPG = ('The Registered Nurses’ Association of Ontario (RNAO) develops Best Practice Guidelines (BPGs) to support high-quality, evidence-informed care. These guidelines '
       'bring together the best available research and expert knowledge to provide recommendations for nurses, interprofessional healthcare teams, organizations and '
       'decision-makers. They cover a wide range of topics, from clinical care and mental health to health equity, person-centred care and population health.')
OURS = ('At Tsi Kanonhkhwatsheríyo (IIPCT), we recognize that providing quality care means bringing evidence and Indigenous ways of knowing together, while respecting '
        'the voices, experiences and priorities of the Indigenous individuals, families and communities we serve. As an Indigenous-focused Best Practice Spotlight '
        'Organization® (BPSO®), we are working toward integrating selected RNAO Best Practice Guidelines into our policies, processes and everyday practices.')
# steering committee as the old page lists it: (team-page card number, label)
COMMITTEE = [(2, 'Kiowa', 'BPSO Lead'), (8, 'Madison', 'BPSO Co-Lead'), (14, 'Sarah', 'BPSO Co-Lead'), (27, 'Shaelee', None), (39, 'Jessi', None)]
STORIES = [
 ('IIPCT Begins Its BPSO Journey: Official Orientation and Launch', 'bpso/orientation-toronto.jpg', 1400, 1050,
  'Five women in ribbon skirts in front of an RNAO and BPSO banner at the BPSO orientation in Toronto',
  ['Staff from Tsi Kanonhkhwatsheríyo (IIPCT) attended the RNAO Best Practice Spotlight Organization® (BPSO®) Program Orientation and Launch in Toronto, marking an important first gathering in our BPSO journey.',
   'The event brought together representatives from newly designated BPSOs to build connections, learn about the expectations of the designation, explore key milestones and prepare for the implementation and evaluation of Best Practice Guidelines (BPGs). Staff also participated in the Best Practice Champions Workshop, which focused on developing change agents to support the adoption and integration of evidence-informed practices within organizations.',
   'This was an important first step in building our collective knowledge, strengthening relationships and preparing our team to advance culturally safe, Indigenous-led and evidence-informed care. We look forward to continuing this work together as we begin our BPSO journey and build on the strengths, knowledge and priorities of the Indigenous communities and families we serve.']),
 ('Building Bridges Together: Representing IIPCT at the Indigenous-Focused BPSO Gathering', 'bpso/gathering-thunder-bay-group.jpg', 1400, 887,
  'A large group of people, many in ribbon skirts and ribbon shirts, in front of a tall white tipi at the Indigenous-focused BPSO gathering in Thunder Bay',
  ['Staff from Tsi Kanonhkhwatsheríyo (IIPCT) were proud to participate in the Indigenous-Focused Best Practice Spotlight Organization® (BPSO®) Gathering, Building Bridges Together to Shape a Balanced Path Forward in Thunder Bay, Ontario, in June 2026.',
   'The gathering brought together Indigenous-focused BPSOs, communities and partners to honour Indigenous ways of knowing, strengthen relationships, share experiences and explore how Best Practice Guidelines can be implemented in ways that reflect and respect Indigenous priorities, voices and experiences.',
   'Participating in this gathering was an opportunity to learn alongside others, celebrate collective progress and strengthen our commitment to culturally safe, Indigenous-led and evidence-informed care. We look forward to bringing these learnings back to IIPCT as we continue to build relationships, grow our BPSO journey and support the health and well-being of the Indigenous communities and families we serve.']),
]

def committee_card(num, label, role):
    m = next(x for x in TEAM if x[0] == num)
    rl = f'<span style="font-size: 13.6px; line-height: 1.3; color: {INK}">{role}</span>' if role else ''
    return (f'<a class="card" href="{TEAM_PAGE}#{m[2]}" style="display: flex; align-items: center; gap: 14px; padding: 12px; border-radius: 14px; {CARD}; color: {INK}; text-decoration: none">'
            + photo(f'people/{m[7]}.jpg', f'Photo of {label}', f'flex: none; width: 76px; height: 76px; border-radius: 50%; object-fit: cover; border: 2px solid #FFFDF8; box-shadow: 0 0 0 1px {LINE}', w=600, h=600)
            + f'<span style="min-width: 0; display: flex; flex-direction: column; gap: 3px"><span style="font-family: {SERIF}; font-weight: 700; font-size: 19px; line-height: 1.1; color: {HEAD}">{label}</span>{rl}</span></a>')

def story(title, img_rel, w, h, alt, paras, flip):
    order = 'order: 2; ' if flip else ''
    return (f'<article style="display: flex; flex-wrap: wrap; align-items: stretch; overflow: hidden; border-radius: 16px; {CARD}">'
            f'<div class="fbs" style="{order}flex: 0 0 44%; min-width: min(320px, 100%); position: relative; min-height: 260px">'
            + photo(img_rel, alt, 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover', w=w, h=h)
            + f'</div><div class="pads" style="flex: 1 1 380px; min-width: 0; padding: 24px 28px 26px; display: flex; flex-direction: column; gap: 12px">'
            f'{h3(title, 22)}' + ''.join(p(t, 14.6, INK, 1.55) for t in paras) + '</div></article>')

def page():
    buttons = (btn('What is a BPSO?', RNAO_BPSO, 'primary', 'external', False, 'md', 'padding: 0 22px; gap: 10px')
               + btn('Our BPSO Work', '#guideline', 'outline', None, True, 'md', 'padding: 0 22px; gap: 10px'))
    s = header('bpso')
    h = hero('hero-bpso', 55.4, 358, 'Best Practice Spotlight<br>Organization (BPSO)',
             'Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (IIPCT) is proud to be one of 17 Indigenous-focused BPSO sites across Ontario.', buttons,
             h1_size=47.6, lead_size=18, lead_lh=1.42, lead_w=540, pad='40px 0 40px 84px', gap=12, btn_mt=10, sq_mt=2, obj='center 40%')
    h = h.replace('position: relative; z-index: 1; max-width: 1440px; margin: 0 auto"', 'position: relative; z-index: 1; max-width: 1440px; margin: 0 auto; width: 100%"', 1)   # stacked hero: keep the text column full width
    s += h.replace(f'src="{BLOB["hero-bpso"]}" alt=""', 'src="/_site/bpso/gathering-thunder-bay.jpg" alt="Five women, several in ribbon skirts, outdoors by a pond at the BPSO gathering in Thunder Bay"', 1)
    s += f'''
<section id="overview" style="scroll-margin-top: 16px; position: relative; {WRAP}; padding: 30px 52px 0 70px; display: flex; flex-wrap: wrap; align-items: center; gap: 24px 44px">
{branch(104, '#B5BFA6', 0.5, 'right: -58px; bottom: -22px; transform: rotate(-14deg)')}
<div style="position: relative; flex: 1 1 460px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 12px">
{eyebrow('Overview')}
{h2('What is a BPSO?', 32.4)}
{p(ABOUT, 15.2, INK, 1.55, 'max-width: 640px')}
{photo('bpso/logo-indigenous-focused-bpso.png', 'RNAO Best Practice Spotlight Organization, Indigenous Focused, logo', 'width: 300px; max-width: 100%; height: auto; margin-top: 6px', w=600, h=220)}
{ext('Read more about BPSOs on the RNAO website', RNAO_BPSO, 14.4, RUST, 'display: inline-flex; align-items: center; min-height: 40px')}
</div>
<figure style="position: relative; flex: 1 1 420px; min-width: 0; margin: 0; padding: 12px 12px 10px; border-radius: 14px; {CARD}">
<a href="/_site/bpso/map-indigenous-bpso.jpg" style="display: block">{photo('bpso/map-indigenous-bpso.jpg', 'Map of Ontario showing the Indigenous-focused BPSO organizations by cohort; IIPCT is listed in Cohort 4', 'width: 100%; height: auto; border-radius: 8px', w=1195, h=897)}</a>
<figcaption style="margin-top: 9px; font-size: 13.4px; line-height: 1.4; color: {MUTED}">Indigenous-focused BPSO organizations across Ontario. IIPCT is in Cohort 4. Select the map to see it larger.</figcaption>
</figure>
</section>'''
    text = p(BPG, 14.2, '#F4F1E8', 1.5, 'max-width: 640px')
    s += green_band('bpso-lake', 'Best Practice Guidelines', 'What Are RNAO Best Practice Guidelines?', text, '', 'margin-top: 30px; padding: 0 58px 0 62px', '34%', 176, 28.2, '20px 34px 22px 40px')
    s += f'''
<section id="guideline" style="scroll-margin-top: 16px; {WRAP}; padding: 30px 52px 0 70px; display: flex; flex-direction: column; gap: 12px">
{eyebrow('Our Focus')}
{h2('The Guideline We Are Working to Implement', 32)}
{p(OURS, 15.2, INK, 1.55, 'max-width: 900px')}
<div style="margin-top: 6px; display: flex; align-items: center; gap: 20px; padding: 18px 22px; border-radius: 14px; {CARD}; max-width: 900px">
{circ('book', 'sage', 62, 32, 1.4)}
<div style="min-width: 0; display: flex; flex-direction: column; gap: 4px">
<span style="font-size: 12.4px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: {RUST}">RNAO Best Practice Guideline</span>
{h3(GUIDELINE, 20)}
</div>
</div>
</section>
<section style="{WRAP}; padding: 34px 52px 0 70px; display: flex; flex-direction: column; gap: 16px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 26px">
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 6px">
{eyebrow('Our People')}
{h2('Meet the Tsi Kanonhkhwatsheríyo BPSO Steering Committee', 30)}
</div>
{photo('bpso/logo-bpso-champion.png', 'BPSO Champion logo', 'flex: none; width: 150px; height: auto; border-radius: 10px', w=480, h=320)}
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); gap: 14px">{''.join(committee_card(*c) for c in COMMITTEE)}</div>
</section>
<section style="{WRAP}; padding: 34px 52px 0 70px; display: flex; flex-direction: column; gap: 18px">
<div style="display: flex; flex-direction: column; gap: 6px">{eyebrow('BPSO Events')}{h2('Our BPSO Journey', 32)}</div>
{''.join(story(*st, flip=(i % 2 == 1)) for i, st in enumerate(STORIES))}
</section>
<div style="margin-top: 30px">'''
    right = (btn('What is a BPSO?', RNAO_BPSO, 'light', 'external', False, 'md', 'padding: 0 22px; gap: 10px; font-size: 13.6px; min-height: 40px')
             + btn('Connect with Our Team', 'Contact.dc.html', 'primary', None, True, 'md', 'padding: 0 24px; gap: 14px; font-size: 13.6px; min-height: 40px; border-color: #C8A15A'))
    band = rust_band('mail', 'Learn More or Connect with Us', 'Want to know more about IIPCT’s BPSO work? We’re happy to share and connect.', right, 'padding: 18px 120px 18px 126px', 14.2)
    band = band.replace(ico('mail', 36, '#FFFFFF', 1.3, 'position: relative'), '')
    band = band.replace('font-weight: 500; font-size: 24.8px;', 'font-weight: 500; font-size: 29.6px;')
    s += band + '</div>'
    s += footer()
    return 'IIPCT — BPSO', s
