"""Primary Medical Care and its six child pages, rebuilt from the live site's content in the new theme.
Every fact on these pages comes from the old site (iipct.org); the claim-by-claim sources are in the builder's notes."""
from lib import *

HOME = ('Home', 'Main.dc.html')
SVC = ('Services', 'Services.dc.html')
PC = ('Primary Medical Care', 'PrimaryCare.dc.html')
SUBS = [('Immunization Program', 'Immunization.dc.html'), ('Well Baby &amp; Well Child', 'WellBaby.dc.html'), ('TB Testing', 'TBTesting.dc.html'),
        ('Advanced Foot Care', 'FootCare.dc.html'), ('Diabetic Retinopathy Screening', 'Retinopathy.dc.html'), ('Outreach &amp; Community Support', 'Outreach.dc.html')]
SCHEDULE_URL = 'https://www.ontario.ca/page/ontarios-routine-immunization-schedule'
TB_SHEET_URL = 'https://hpepublichealth.ca/wp-content/uploads/2020/02/TB-6-Tuberculosis-Fact-Sheet.pdf'

def nl_band(sub=NL_SUB):
    """The newsletter band: lib.newsletter(), the sign-up form that posts to IIPCT's Mailchimp audience."""
    return newsletter(sub)

def hero_photo(path, wh, alt, pos='center center'):
    """A real photograph (site-img/) in the same box as sub_hero()'s photo slot: 440 px wide, 440 / 232, rounded, bordered."""
    return ('<div class="sh-photo" style="flex: 0 0 440px; max-width: 100%">'
            + photo(path, alt, f'width: 100%; height: auto; aspect-ratio: 440 / 232; object-fit: cover; object-position: {pos}; border-radius: 16px; border: 1px solid {LINE}',
                    w=wh[0], h=wh[1], lazy=False) + '</div>')

def page_hero(trail, title, lead, pic='', **kw):
    """lib.sub_hero(); pic (from hero_photo) fills its photo slot with a real photograph, which sub_hero() itself cannot take."""
    s = sub_hero(trail, title, lead, **kw)
    if kw.get('medal'):      # the icon medallion only balances the wide layout; once the hero stacks it is a lone circle
        medal_box = '<div aria-hidden="true" style="flex: 0 0 200px'
        assert s.count(medal_box) == 1, 'lib.sub_hero() markup changed: update p_sub.page_hero()'
        s = s.replace(medal_box, '<div class="hide-t" aria-hidden="true" style="flex: 0 0 200px')
    if not pic:
        return s
    tail = '\n\n</div>\n<div class="hero-hz"'
    assert s.count(tail) == 1, 'lib.sub_hero() markup changed: update p_sub.page_hero()'
    return s.replace(tail, '\n' + pic + '\n</div>\n<div class="hero-hz"', 1)

def related(current):
    tiles = [(f'<a class="card t-s" href="{h}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 54px; padding: 12px 16px; border-radius: 12px; {CARD}; '
              f'font-size: 14px; font-weight: 600; line-height: 1.25; color: {HEAD}; text-decoration: none"><span class="ct">{t}</span>{ico("arrow", 15, RUST, 1.9)}</a>')
             for t, h in [PC] + [(t, h) for t, h in SUBS if h != current]]
    return section('More in primary care', grid(tiles, 230, 12, '', 'g-tiles gt3'), size=23)

def shell(file, crumb, title, lead, main, aside_title='Book this service', pic='', **hero_kw):
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Contact a Clinic', 'Contact.dc.html', 'outline', 'phone', False)
    s = header('services')
    s += page_hero([HOME, SVC, PC, (crumb, None)], title, lead, pic, eyebrow_txt='Primary Medical Care', buttons=buttons, **hero_kw)
    s += two_col(main + related(file), book_aside('', aside_title))
    s += f'<div style="margin-top: 40px">{nl_band()}</div>'
    s += footer()
    return s

def sub_title(text):
    return f'<h3 style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; line-height: 1.2; color: {RUST}">{text}</h3>'

# ------------------------------------------------------------------ hub
def primary():
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Contact a Clinic', 'Contact.dc.html', 'outline', 'phone', False)
    s = header('services')
    s += page_hero([HOME, SVC, ('Primary Medical Care', None)], 'Primary Medical Care',
                   'Our team includes physicians, nurse practitioners, registered nurses and registered practical nurses, with connections to partner supports such as midwifery and other medical services.',
                   eyebrow_txt='Services', buttons=buttons, medal=('stethoscope', 'rust'))
    care = grid([
        icon_item('heart-pulse', 'rust', 'Chronic disease care', 'Prevention, diagnosis and ongoing management of long-term conditions. Our team includes a Certified Diabetes Nurse Educator.'),
        icon_item('bolt', 'gold', 'Acute care', 'Same-day appointments for urgent health concerns.'),
        icon_item('kit', 'sage', 'Minor surgical procedures', 'Safe minor procedures done here at the clinic by qualified providers.'),
        icon_item('route', 'sage', 'Referrals', 'We connect you with specialists and community services, and guide you through the referral process.'),
        icon_item('handshake', 'gold', 'Health partnerships', 'A Respiratory Therapist at the Tyendinaga clinic, a Registered Dietitian, and dermatology through the Kingston clinic.'),
        icon_item('shield', 'rust', 'Sexual health services', 'STI testing and treatment, contraception, pregnancy testing and sexual health counselling for rostered clients.'),
    ], 330)
    programs = grid([
        link_card('syringe', 'rust', 'Immunization Program', 'Publicly funded vaccines for infants, children and adults.', 'Immunization.dc.html'),
        link_card('baby', 'gold', 'Well Baby &amp; Well Child', 'Check-ups from two months to six years.', 'WellBaby.dc.html'),
        link_card('check-circle', 'sage', 'TB Testing', 'Tuberculosis skin testing (Mantoux).', 'TBTesting.dc.html'),
        link_card('foot', 'sage', 'Advanced Foot Care', 'Assessment and care from nurses with specialized certification.', 'FootCare.dc.html'),
        link_card('eye', 'rust', 'Diabetic Retinopathy Screening', 'Monthly eye screening clinics for people with diabetes.', 'Retinopathy.dc.html'),
        link_card('map', 'gold', 'Outreach &amp; Community Support', 'Screening and support out in the community.', 'Outreach.dc.html'),
    ], 330, 16, '', 'g-tiles gt2')
    col = lambda t, items: (f'<div style="flex: 1 1 220px; min-width: 0; display: flex; flex-direction: column; gap: 10px">{sub_title(t)}{bullets(items, "check", "#1F4A2B", 14.2, 8)}</div>')
    blood = panel(f'<div style="display: flex; align-items: center; gap: 16px">{circ("droplet", "rust", 52, 27, 1.5)}{h3("Blood draws (phlebotomy)", 21)}</div>'
                  + prose('A nurse or doctor uses a needle to take blood from a vein, usually in your arm. The blood is sent to a lab to help diagnose conditions.', size=14.4, style='margin-top: 14px')
                  + f'<div style="margin-top: 16px; display: flex; flex-wrap: wrap; gap: 20px 36px">'
                  + col('Before you come', ['Drink water and have a snack first.', 'Only fast if you were told to.', 'Tell us if needles make you anxious.'])
                  + col('What to expect', ['You sit or lie down.', 'A band may be tied around your arm.', 'The needle may sting going in.', 'Blood flows into containers, then the needle comes out.', 'Pressure is applied and a bandage goes on.'])
                  + col('Your results', ['Results go to the provider who ordered the test.', 'If we ordered it, expect results within a week.', 'You can also track your results through LifeLabs.'])
                  + '</div>', pad='22px 26px 24px')
    cancer = note('check-circle', 'Cancer screening and awareness',
                  'We support screening for breast, lung, cervical and colorectal cancer. For more information, visit '
                  + ext('Ontario Cancer Prevention and Care', 'https://www.ontario.ca/page/cancer-prevention-and-care', 14) + '.')
    main = (section('What we look after', care, 'At the clinic')
            + section('Programs and clinics', programs, 'With their own page')
            + section('Lab work and screening', blood + cancer, 'Good to know'))
    s += two_col(main, book_aside(link_list('In this section', SUBS), 'Book a primary care visit'))
    s += f'<div style="margin-top: 40px">{nl_band()}</div>'
    s += footer()
    return 'IIPCT — Primary Medical Care', s

# ------------------------------------------------------------------ child pages
def immunization():
    who = panel(prose('Our immunization program offers culturally safe vaccines for all ages, helping protect the health of our community.', size=14.6)
                + f'<div style="margin-top: 12px">{chips(["Infants", "Preschool children", "School-aged children", "Adults"])}</div>')
    shingrix = note('info', 'Shingles vaccine (Shingrix)',
                    'Adults aged 60 and over with status covered through Non-Insured Health Benefits (NIHB) can get the Shingrix vaccine earlier than the standard schedule, '
                    'with a prescription from a health care provider.')
    sched = panel(f'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px 24px">'
                  f'<div style="flex: 1 1 320px; min-width: 0; display: flex; align-items: center; gap: 16px">{ico("doc", 30, RUSTI, 1.4)}'
                  f'<div style="display: flex; flex-direction: column; gap: 3px">{h3("Ontario’s routine immunization schedule", 18.4)}'
                  f'<p style="margin: 0; font-size: 13.6px; line-height: 1.4; color: {INK}">Which routine vaccines are due at each age, on the Government of Ontario website. Opens in a new tab.</p></div></div>'
                  f'{btn("View the Schedule", SCHEDULE_URL, "outline", None, True, "sm", "min-height: 40px")}</div>')
    baby = note('baby', 'Booking for a baby or young child?',
                f'Your child may also get vaccines at a <a href="WellBaby.dc.html" style="color: {RUST}; font-weight: 600">well baby or well child visit</a>.', 'cream')
    main = section('Who it’s for', who + shingrix) + section('The schedule', sched + baby)
    return 'IIPCT — Immunization Program', shell('Immunization.dc.html', 'Immunization Program', 'Publicly Funded Immunization Program',
                                                  'Culturally safe vaccines for all ages, covered by Ontario’s publicly funded program.', main, 'Book a vaccine visit',
                                                  medal=('syringe', 'rust'), title_size=42)

def wellbaby():
    row = lambda label, items, last=False: (
        f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 22px; padding: 14px 0; {"" if last else "border-bottom: 1px solid #E6D9BF"}">'
        f'<span style="flex: 0 0 196px; font-family: {SERIF}; font-weight: 700; font-size: 17.6px; line-height: 1.15; letter-spacing: -0.014em; color: {HEAD}">{label}</span>{chips(items)}</div>')
    schedule = (prose('Well baby and well child visits usually take place at these ages. More visits may be booked if needed.', size=14.6)
                + panel(row('Infants', ['2 months', '4 months', '6 months', '9 months', '12 months', '15 months', '18 months'])
                        + row('Toddlers', ['2 years', '3 years'])
                        + row('Preschool and school age', ['4 years', '5 years', '6 years'], True), pad='6px 24px'))
    visit = grid([
        icon_item('stethoscope', 'rust', 'Physical assessment', 'This may include your child’s weight, length or height, and head circumference. The nurse or doctor may listen to the heart, lungs or abdomen, gently check the head and eyes, and check the hips.'),
        icon_item('sprout', 'sage', 'Development and milestones', 'We check how your child is developing. Please share any questions or concerns. The LookSee Checklist is a free resource for families in Ontario.',
                  ext('LookSee Checklist for parents', 'https://www.lookseechecklist.com/en/parents', 13.4, RUST, 'display: inline-flex; align-items: center; min-height: 40px; margin-top: 2px')),
        icon_item('chat-heart', 'gold', 'Time to talk', 'Questions about nutrition, sleep and behaviour, and guidance on injury prevention, healthy sleep, environmental health, oral health, fevers and more.'),
        icon_item('syringe', 'sage', 'Vaccinations', 'Your child may also get vaccines during the visit.',
                  textlink('Immunization Program', 'Immunization.dc.html', 13.4, 'gap: 8px; min-height: 40px; margin-top: 2px')),
    ], 330)
    main = section('When to book', schedule, 'Visit schedule') + section('What happens at a visit', visit, 'What to expect')
    return 'IIPCT — Well Baby and Well Child', shell('WellBaby.dc.html', 'Well Baby &amp; Well Child', 'Well Baby and Well Child Appointments',
                                                      'Our little ones are our future. We monitor their health and provide care in a gentle, supportive way.', main,
                                                      'Book a well child visit', medal=('baby', 'gold'), title_size=42)

def tb():
    about = panel(prose('We provide information about TB and access to screening using the Mantoux skin test. Call your clinic to book.', size=14.8))
    kind = lambda title, intro, items: panel(h3(title, 19) + prose(intro, size=14.2, style='margin: 8px 0 12px') + bullets(items, 'check', '#1F4A2B', 14.2, 7), pad='20px 22px 22px')
    facts = (prose('Tuberculosis (TB) is an infectious disease. It usually attacks the lungs, but can affect many parts of the body, including the brain, spine and kidneys. TB has been around for centuries.', size=14.8)
             + grid([
                 kind('TB infection (latent TB)', 'After breathing in TB, some people are able to trap the germs and keep them inactive. This is called latent TB. People with latent TB:',
                      ['Do not feel sick', 'Cannot spread TB', 'Will have a positive skin test', 'Could develop active TB later in life']),
                 kind('TB disease (active TB)', 'Latent TB germs become active when the body’s immunity cannot stop them from growing. The germs then damage the body, causing symptoms of:',
                      ['Cough (lasting longer than 3 weeks)', 'Bloody sputum', 'Chest pain with coughing', 'Fever, chills, night sweats and fatigue', 'Unexplained weight loss and/or decreased appetite']),
             ], 280, 14)
             + note('people', 'How TB is spread', 'Infected people with TB may spread the infection through the air (coughing or sneezing) with prolonged exposure.'))
    steps = grid([
        icon_item('syringe', 'rust', 'The skin test', 'Testing is done with a skin test (the Mantoux test). A small amount of solution is injected under a few layers of skin, creating a bleb (a small raised bump).'),
        icon_item('clock', 'gold', 'Come back in 48 to 72 hours', 'You will have to return to the clinic after 48 to 72 hours, so we can check for induration: an area of skin that has become hard.'),
        icon_item('review', 'sage', 'Reading the result', 'For the test to be positive, the induration must be 10 mm or greater.'),
    ], 250, 16, '', 'g-steps')
    positive = panel(h3('What a positive test means', 19)
                     + prose('A positive test shows that a person has the TB germs. A physical exam, chest x-ray and sputum samples are then collected and checked for TB disease. '
                             'A positive test does not mean the person has active TB: it could be latent TB.', size=14.4, style='margin-top: 8px'), pad='20px 22px 22px')
    remember = note('check-circle', 'Remember', 'TB is preventable, treatable and curable.', 'gold')
    source = p('This information comes from IIPCT’s TB fact sheet. The sheet’s reference: ' + ext('Tuberculosis Fact Sheet, hpePublicHealth.ca (PDF)', TB_SHEET_URL, 13.4) + '.',
               13.4, MUTED, 1.5)
    main = (section('About the test', about) + section('Tuberculosis: get the facts', facts, 'What is TB')
            + section('How testing is done', steps + positive + remember + source, 'The Mantoux test'))
    return 'IIPCT — TB Testing', shell('TBTesting.dc.html', 'TB Testing', 'TB Testing', 'Tuberculosis (TB) skin testing at your IIPCT clinic.', main, 'Book a TB test',
                                       medal=('check-circle', 'sage'))

def foot():
    who = panel(prose('We offer Advanced Foot Care from nurses with specialized certification. The program is for clients with diabetes or other conditions that affect foot health. '
                      'Our nurses provide care that is safe, compassionate and culturally respectful.', size=14.8))
    yearly = note('calendar-check', 'Living with diabetes?', 'We encourage clients with diabetes to have a foot assessment at least once a year. It helps prevent problems and keep feet healthy.')
    inc = panel(bullets(['Comprehensive lower limb assessments', 'Nail and skin care tailored to your needs', 'Ankle-brachial index (ABI) testing when needed',
                         'Offloading strategies to prevent pressure injuries', 'A focus on prevention and early intervention'], 'check', '#1F4A2B', 14.8, 11))
    main = section('Who it’s for', who + yearly) + section('What’s included', inc)
    return 'IIPCT — Advanced Foot Care', shell('FootCare.dc.html', 'Advanced Foot Care', 'Advanced Foot Care Services',
                                               'Foot care from nurses with specialized certification, for clients with diabetes or other conditions that affect foot health.', main,
                                               'Book a foot care visit', title_size=42,
                                               pic=hero_photo('services/foot-care.jpg', (1200, 633), 'A nurse in a gown, mask and gloves caring for a client’s foot during a foot care visit'))

def retino():
    who = panel(prose('We offer monthly diabetic retinopathy screening clinics. If you have diabetes and have not had an eye screening in the past year, we encourage you to call and book an appointment.', size=14.8))
    monthly = note('calendar-check', 'Clinics run monthly', 'Call your clinic to book an appointment.')
    expect = grid([
        icon_item('user', 'sage', 'Done by a trained nurse', 'A trained nurse examines the retina (the back of the eye) using non-invasive techniques.'),
        icon_item('clock', 'gold', 'Quick and safe', 'Screening is quick, safe and usually does not need any special preparation.'),
        icon_item('review', 'rust', 'Results and follow-up', 'Your results are reviewed with you. Follow-up care or referrals are provided if needed.'),
    ], 250, 16, '', 'g-steps')
    prog = panel(prose('This service is part of the Eye Health Screening Initiative (EHSI), delivered in partnership with Vision Loss Rehabilitation Canada (VLRC) and the Indigenous Diabetes Health Circle (IDHC).',
                       'The program was developed with guidance from local Indigenous partners, so that care is accessible, culturally safe and responsive to community needs. '
                       'IIPCT is honoured to be one of the participating communities offering this service.', size=14.6, style='margin-bottom: 10px'))
    main = section('Who should come', who + monthly) + section('What to expect', expect) + section('About the program', prog)
    return 'IIPCT — Diabetic Retinopathy Screening', shell('Retinopathy.dc.html', 'Diabetic Retinopathy Screening', 'Diabetic Retinopathy Screening',
                                                           'Monthly eye screening clinics for people living with diabetes, to find early changes in the retina and help prevent vision problems.', main,
                                                           'Book an eye screening', title_size=42,
                                                           pic=hero_photo('services/retinal-screening.jpg', (1200, 632), 'A nurse in teal scrubs uses a retinal screening camera while a seated client looks into it'))

def outreach():
    what = grid([
        icon_item('droplet', 'rust', 'Kidney health', 'Chronic kidney disease (CKD) screening, supporting early detection and management, especially for people at higher risk.'),
        icon_item('check-circle', 'sage', 'Cancer screening', 'HPV screening clinics to reduce barriers and improve cervical cancer prevention, breast cancer screening events, and colorectal screening pathways.'),
        icon_item('heart-pulse', 'gold', 'Diabetes screening', 'Promoting early identification and intervention.'),
        icon_item('eye', 'rust', 'Eye screening', 'Diabetic retinopathy screening, bringing essential eye care to the community.',
                  textlink('About eye screening', 'Retinopathy.dc.html', 13.4, 'gap: 8px; min-height: 40px; margin-top: 2px')),
        icon_item('house', 'sage', 'Support for displaced communities', 'Care, supplies and connections to services for people affected by emergencies, such as wildfire displacement.'),
        icon_item('tipi', 'gold', 'Powwows and community events', 'Sharing health and wellness information, providing culturally safe care, and building trust-based relationships.'),
    ], 330)
    goal = panel(prose('We support Indigenous individuals and families who may not have regular access to a primary care provider. Through outreach, we bring care directly to the community: meeting people where they are, in ways that honour their experiences and respect their needs.',
                       'Our goal is that all Indigenous people in our region have access to timely, preventive and compassionate care. Our outreach is community-driven and culturally grounded.',
                       size=14.8, style='margin-bottom: 10px'))
    reach = note('handshake', 'Connect with us about outreach', f'If you or someone you know needs support, or would like to connect about outreach, please <a href="Contact.dc.html" style="color: {RUST}; font-weight: 600">contact us</a>. We’re here to help.', 'cream')
    story = (f'<a class="card" href="NewsBreastScreening.dc.html" style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 26px; padding: 20px 24px; border-radius: 14px; {CARD}; color: {INK}; text-decoration: none">'
             f'<span style="flex: none; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 112px; height: 112px; border-radius: 50%; background: #153526; color: #FFFFFF">'
             f'<span style="font-family: {SERIF}; font-weight: 600; font-size: 38px; line-height: 1">19</span><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; margin-top: 4px; color: #E3BE74">mammograms</span></span>'
             f'<span style="flex: 1 1 320px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 6px">'
             f'<span class="ct" style="font-family: {SERIF}; font-weight: 700; font-size: 21px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}">Together We’re Stronger: Breast Cancer Screening Event</span>'
             f'<span style="font-size: 13.8px; line-height: 1.45">19 mammograms were completed, with our partners the Mohawks of the Bay of Quinte, the South East Indigenous Cancer Program and Kingston Health Sciences Centre.</span>'
             f'<span style="display: inline-flex; align-items: center; gap: 8px; font-size: 13.6px; font-weight: 600; color: {RUST}">Read the story{ico("arrow", 15, RUST, 1.9)}</span></span></a>')
    main = section('Why we do it', goal + reach, 'Our goal') + section('What outreach looks like', what) + section('From the community', story)
    return 'IIPCT — Outreach and Community Support', shell('Outreach.dc.html', 'Outreach &amp; Community Support', 'Outreach and Community Support',
                                                           'We bring care directly to the community, for Indigenous people and families who may not have regular access to a primary care provider.', main,
                                                           'Talk to the team', title_size=42,
                                                           pic=hero_photo('services/mobile-clinic-van.jpg', (884, 466), 'IIPCT’s green-and-white Mobile Health Clinic van, parked with its side door and awning open'))
