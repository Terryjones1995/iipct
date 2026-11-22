"""Primary Medical Care and its six child pages, rebuilt from the live site's content in the new theme."""
from lib import *

HOME = ('Home', 'Main.dc.html')
SVC = ('Services', 'Services.dc.html')
PC = ('Primary Medical Care', 'PrimaryCare.dc.html')
SUBS = [('Immunization Program', 'Immunization.dc.html'), ('Well Baby &amp; Well Child', 'WellBaby.dc.html'), ('TB Testing', 'TBTesting.dc.html'),
        ('Advanced Foot Care', 'FootCare.dc.html'), ('Diabetic Retinopathy Screening', 'Retinopathy.dc.html'), ('Outreach &amp; Community Support', 'Outreach.dc.html')]

def related(current):
    tiles = [(f'<a class="card" href="{h}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 54px; padding: 12px 16px; border-radius: 12px; {CARD}; '
              f'font-size: 14px; font-weight: 600; line-height: 1.25; color: {HEAD}; text-decoration: none"><span>{t}</span>{ico("arrow", 15, RUST, 1.9)}</a>')
             for t, h in [PC] + [(t, h) for t, h in SUBS if h != current]]
    return section('More in primary care', grid(tiles, 230, 12), size=23)

def shell(file, crumb, title, lead, main, aside_title='Book this service', **hero_kw):
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Contact a Clinic', 'Contact.dc.html', 'outline', 'phone', False)
    s = header('services')
    s += sub_hero([HOME, SVC, PC, (crumb, None)], title, lead, eyebrow_txt='Primary Medical Care', buttons=buttons, **hero_kw)
    s += two_col(main + related(file), book_aside('', aside_title))
    s += f'<div style="margin-top: 40px">{newsletter()}</div>'
    s += footer()
    return s

def sub_title(text):
    return f'<h3 style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; line-height: 1.2; color: {RUST}">{text}</h3>'

# ------------------------------------------------------------------ hub
def primary():
    buttons = btn('Schedule Your Visit', BOOKING, 'primary', 'calendar-check') + btn('Contact a Clinic', 'Contact.dc.html', 'outline', 'phone', False)
    s = header('services')
    s += sub_hero([HOME, SVC, ('Primary Medical Care', None)], 'Primary Medical Care',
                  'Everyday and ongoing care for you and your family: check-ups, same-day visits for urgent concerns, screening, and support for long-term conditions.',
                  'car-staff', 'A member of the IIPCT care team outdoors, smiling', 'Services', buttons, pos='left center')
    care = grid([
        icon_item('heart-pulse', 'rust', 'Chronic disease care', 'Prevention, diagnosis and ongoing management of long-term conditions. Our team includes a Certified Diabetes Nurse Educator.'),
        icon_item('bolt', 'gold', 'Acute care', 'Same-day appointments for urgent health concerns.'),
        icon_item('kit', 'sage', 'Minor surgical procedures', 'Minor procedures done here at the clinic.'),
        icon_item('route', 'sage', 'Referrals', 'When you need a specialist or another service, your provider arranges the referral.'),
        icon_item('handshake', 'gold', 'Health partnerships', 'A Respiratory Therapist at the Tyendinaga clinic, a Registered Dietitian, and dermatology through the Kingston clinic.'),
        icon_item('shield', 'rust', 'Sexual health services', 'STI testing and treatment, contraception, pregnancy testing and counselling for rostered clients.'),
    ], 330)
    programs = grid([
        link_card('syringe', 'rust', 'Immunization Program', 'Publicly funded vaccines for infants, children and adults.', 'Immunization.dc.html'),
        link_card('baby', 'gold', 'Well Baby &amp; Well Child', 'Check-ups from two months to six years.', 'WellBaby.dc.html'),
        link_card('check-circle', 'sage', 'TB Testing', 'Tuberculosis skin testing (Mantoux).', 'TBTesting.dc.html'),
        link_card('foot', 'sage', 'Advanced Foot Care', 'Assessment and care from nurses with specialized certification.', 'FootCare.dc.html'),
        link_card('eye', 'rust', 'Diabetic Retinopathy Screening', 'Monthly eye screening clinics for people with diabetes.', 'Retinopathy.dc.html'),
        link_card('map', 'gold', 'Outreach &amp; Community Support', 'Screening and support out in the community.', 'Outreach.dc.html'),
    ], 330)
    col = lambda t, items: (f'<div style="flex: 1 1 260px; min-width: 0; display: flex; flex-direction: column; gap: 10px">{sub_title(t)}{bullets(items, "check", "#1F4A2B", 14.2, 8)}</div>')
    blood = panel(f'<div style="display: flex; align-items: center; gap: 16px">{circ("droplet", "rust", 52, 27, 1.5)}{h3("Blood draws (phlebotomy)", 21)}</div>'
                  f'<div style="margin-top: 16px; display: flex; flex-wrap: wrap; gap: 20px 40px">'
                  + col('Before you come', ['Drink water and have a snack first.', 'Only fast if your provider told you to.', 'If blood draws make you anxious, tell staff when you arrive.'])
                  + col('Your results', ['Results go to the provider who ordered the test.', 'For tests ordered by IIPCT, allow about a week.', 'You can also follow your results through LifeLabs.'])
                  + '</div>', pad='22px 26px 24px')
    cancer = note('check-circle', 'Cancer screening and awareness',
                  'We support screening for breast, lung, cervical and colorectal cancer. Ask your provider what you’re due for, or read '
                  + ext('Ontario’s guide to cancer prevention and care', 'https://www.ontario.ca/page/cancer-prevention-and-care', 14) + '.')
    main = (section('What we look after', care, 'At the clinic')
            + section('Programs and clinics', programs, 'With their own page')
            + section('Lab work and screening', blood + cancer, 'Good to know'))
    s += two_col(main, book_aside(link_list('In this section', SUBS), 'Book a primary care visit'))
    s += f'<div style="margin-top: 40px">{newsletter()}</div>'
    s += footer()
    return 'IIPCT — Primary Medical Care', s

# ------------------------------------------------------------------ child pages
def immunization():
    who = panel(prose('We give the vaccines on Ontario’s publicly funded schedule to:', size=14.6)
                + f'<div style="margin-top: 12px">{chips(["Infants", "Preschool and school-aged children", "Adults"])}</div>')
    shingrix = note('info', 'Shingles vaccine (Shingrix)',
                    'Adults 60 and over who are covered through Non-Insured Health Benefits (NIHB) can get Shingrix earlier, with a prescription from their provider.')
    sched = panel(f'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px 24px">'
                  f'<div style="flex: 1 1 320px; min-width: 0; display: flex; align-items: center; gap: 16px">{ico("doc", 30, RUSTI, 1.4)}'
                  f'<div style="display: flex; flex-direction: column; gap: 3px">{h3("Ontario’s immunization schedule", 18.4)}'
                  f'<p style="margin: 0; font-size: 13.6px; line-height: 1.4; color: {INK}">Which vaccines are due at each age. PDF, opens in a new tab.</p></div></div>'
                  f'{btn("View the Schedule", "#", "outline", None, True, "sm")}</div>')
    baby = note('baby', 'Booking for a baby or young child?',
                'Routine vaccines are given at well baby and well child visits. ' + textlink('See the visit schedule', 'WellBaby.dc.html', 14, 'gap: 8px'), 'cream')
    main = section('Who it’s for', who + shingrix) + section('The schedule', sched + baby)
    return 'IIPCT — Immunization Program', shell('Immunization.dc.html', 'Immunization Program', 'Publicly Funded Immunization Program',
                                                  'Routine vaccines for every age, covered by Ontario’s publicly funded program.', main, 'Book a vaccine visit',
                                                  photo='hero-careers', alt='Three members of the care team in scrubs, laughing together outdoors', pos='8% center', title_size=42)

def wellbaby():
    row = lambda label, items, last=False: (
        f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 22px; padding: 14px 0; {"" if last else "border-bottom: 1px solid #E6D9BF"}">'
        f'<span style="flex: 0 0 196px; font-family: {SERIF}; font-weight: 700; font-size: 17.6px; line-height: 1.15; letter-spacing: -0.014em; color: {HEAD}">{label}</span>{chips(items)}</div>')
    schedule = panel(row('Infants', ['2 months', '4 months', '6 months', '9 months', '12 months', '15 months', '18 months'])
                     + row('Toddlers', ['2 years', '3 years'])
                     + row('Preschool and school age', ['4 years', '5 years', '6 years'], True), pad='6px 24px')
    visit = grid([
        icon_item('stethoscope', 'rust', 'Physical assessment', 'Weight, length or height, and head circumference. A check of the heart, lungs and abdomen, and of the head, eyes and hips.'),
        icon_item('sprout', 'sage', 'Development and milestones', 'A look at how your child is growing and learning. The LookSee Checklist helps you follow milestones between visits.',
                  ext('LookSee Checklist for parents', 'https://www.lookseechecklist.com/en/parents', 13.4, RUST, 'margin-top: 4px')),
        icon_item('chat-heart', 'gold', 'Time to talk', 'Nutrition, sleep, behaviour, injury prevention, environmental health, oral health and managing fevers.'),
        icon_item('syringe', 'sage', 'Vaccinations', 'Routine vaccines are given at these visits.',
                  textlink('Immunization Program', 'Immunization.dc.html', 13.4, 'gap: 8px; margin-top: 4px')),
    ], 330)
    main = section('When to book', schedule, 'Visit schedule') + section('What happens at a visit', visit, 'What to expect')
    return 'IIPCT — Well Baby and Well Child', shell('WellBaby.dc.html', 'Well Baby &amp; Well Child', 'Well Baby and Well Child Appointments',
                                                      'Regular check-ups that follow your child’s growth, development and vaccines, from two months to six years.', main,
                                                      'Book a well child visit', photo='hero-home', alt='A young girl with a nurse and her grandmother by the water', pos='38% center', title_size=42)

def tb():
    about = panel(prose('IIPCT offers the tuberculosis (TB) skin test, also called the Mantoux test. Call your clinic to book.', size=14.8))
    todo = note('info', 'Details to come from IIPCT',
                '[On the current site this page is two images with no text. Their content gets typed out here, so it can be read on a phone, by a screen reader, and found in search.]', 'gold')
    sheets = grid([photo_ph('TB testing information, sheet 1<br>(image on the current site)', '4 / 3'), photo_ph('TB testing information, sheet 2<br>(image on the current site)', '4 / 3')], 260)
    main = section('About the test', about) + section('What to know before your test', todo + sheets)
    return 'IIPCT — TB Testing', shell('TBTesting.dc.html', 'TB Testing', 'TB Testing', 'Tuberculosis skin testing at your IIPCT clinic.', main, 'Book a TB test',
                                       photo='hero-careers', alt='Members of the care team in scrubs, outdoors', pos='right center')

def foot():
    who = panel(prose('Our foot care nurses hold specialized certification. They see clients living with diabetes and other conditions that affect foot health.', size=14.8))
    yearly = note('calendar-check', 'Living with diabetes?', 'A foot assessment once a year is recommended.')
    inc = panel(bullets(['Comprehensive lower limb assessments', 'Nail and skin care', 'Ankle-brachial index (ABI) testing when indicated', 'Offloading strategies',
                         'Prevention and early intervention'], 'check', '#1F4A2B', 14.8, 11))
    main = section('Who it’s for', who + yearly) + section('What’s included', inc)
    return 'IIPCT — Advanced Foot Care', shell('FootCare.dc.html', 'Advanced Foot Care', 'Advanced Foot Care Services',
                                               'Foot care from nurses with specialized certification, for clients with diabetes or other conditions that affect foot health.', main,
                                               'Book a foot care visit', photo='hero-bpso', alt='An Elder wrapped in a woven blanket, smiling with a nurse', pos='right center', title_size=42)

def retino():
    who = panel(prose('These clinics are for people living with diabetes who haven’t had an eye screening in the past year.', size=14.8))
    monthly = note('calendar-check', 'Clinics run monthly', 'Call your clinic for the next date.')
    expect = grid([
        icon_item('user', 'sage', 'Done by a trained nurse', 'The screening is carried out at the clinic by a nurse trained to do it.'),
        icon_item('clock', 'gold', 'Quick and non-invasive', 'Most people don’t need to do anything to prepare.'),
        icon_item('review', 'rust', 'Results and follow-up', 'Your results are reviewed, and follow-up or a referral is arranged if you need one.'),
    ], 250)
    prog = panel(prose('The screening is part of the Eye Health Screening Initiative (EHSI), delivered with Vision Loss Rehabilitation Canada (VLRC) and the Indigenous Diabetes Health Circle (IDHC).', size=14.6))
    main = section('Who should come', who + monthly) + section('What to expect', expect) + section('About the program', prog)
    return 'IIPCT — Diabetic Retinopathy Screening', shell('Retinopathy.dc.html', 'Diabetic Retinopathy Screening', 'Diabetic Retinopathy Screening',
                                                           'Monthly eye screening clinics for people living with diabetes.', main, 'Book an eye screening',
                                                           photo='hero-who', alt='An Elder smiling with her family by the lake', pos='left center', title_size=42)

def outreach():
    what = grid([
        icon_item('droplet', 'rust', 'Kidney health', 'Screening for chronic kidney disease (CKD).'),
        icon_item('check-circle', 'sage', 'Cancer screening', 'HPV clinics, breast screening events and colorectal screening pathways.'),
        icon_item('heart-pulse', 'gold', 'Diabetes screening', 'Screening for diabetes, with a link back to the clinic for follow-up.'),
        icon_item('eye', 'rust', 'Eye screening', 'Diabetic retinopathy screening for people living with diabetes.',
                  textlink('About eye screening', 'Retinopathy.dc.html', 13.4, 'gap: 8px; margin-top: 4px')),
        icon_item('house', 'sage', 'Support for displaced communities', 'Care for people who have had to leave home, such as during wildfire evacuations.'),
        icon_item('tipi', 'gold', 'At community events', 'Look for the IIPCT team at powwows and community events.'),
    ], 330)
    goal = panel(prose('Outreach is for community members who may not see a primary care provider regularly. Our goal is to bring screening closer to where people are, and to connect them with care afterwards.', size=14.8))
    story = (f'<a class="card" href="NewsBreastScreening.dc.html" style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 26px; padding: 20px 24px; border-radius: 14px; {CARD}; color: {INK}; text-decoration: none">'
             f'<span style="flex: none; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 112px; height: 112px; border-radius: 50%; background: #153526; color: #FFFFFF">'
             f'<span style="font-family: {SERIF}; font-weight: 600; font-size: 38px; line-height: 1">19</span><span style="font-size: 9.6px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 4px; color: #E3BE74">mammograms</span></span>'
             f'<span style="flex: 1 1 320px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 6px">{tag("Outreach story", "sage")}'
             f'<span style="font-family: {SERIF}; font-weight: 700; font-size: 21px; line-height: 1.12; letter-spacing: -0.016em; color: {HEAD}">Together We’re Stronger: Breast Cancer Screening Event</span>'
             f'<span style="font-size: 13.8px; line-height: 1.45">Run with the Mohawks of the Bay of Quinte, the South East Indigenous Cancer Program and Kingston Health Sciences Centre.</span>'
             f'<span style="display: inline-flex; align-items: center; gap: 8px; font-size: 13.6px; font-weight: 600; color: {RUST}">Read the story{ico("arrow", 15, RUST, 1.9)}</span></span></a>')
    main = section('Why we do it', goal, 'Our goal') + section('What outreach looks like', what) + section('From the community', story)
    return 'IIPCT — Outreach and Community Support', shell('Outreach.dc.html', 'Outreach &amp; Community Support', 'Outreach and Community Support',
                                                           'Care that comes to you: screening and support out in the community, for people who don’t see a primary care provider regularly.', main,
                                                           'Talk to the team', photo='con-map', alt='Map of southeastern Ontario showing IIPCT clinic locations', pos='right center', title_size=42)
