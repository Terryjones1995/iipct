"""The facts the pages print: locations, the phone line, booking, newsletter, social links, the organisation's names and the
staff extension lists. Every page reads them from here; no clinic fact is typed anywhere else.

Every record comes from IIPCT's current site (iipct.org) as collected and checked in
/home/terry/tasks/iipct/content/old-site/ (clinics.json, contacts.json, staff.json, VERIFICATION.md). The source of each
record is noted beside it. To change a fact, change it here and regenerate (tools/generator/export_site.py).
"""

# ---------------------------------------------------------------- names
# Old site header wordmark and page text: "Tsi Kanonhkhwatsheríyo" (pages/home.md, pages/no-title.md).
ORG_NAME = 'Tsi Kanonhkhwatsheríyo'
ORG_EN = 'Indigenous Interprofessional Primary Care Team'
ORG_SHORT = 'IIPCT'
# pages/no-title.md: "Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (IIPCT)"
ORG_FULL = f'{ORG_NAME} {ORG_EN} ({ORG_SHORT})'

# ---------------------------------------------------------------- phone, email, outside links
# contacts.json phones[0]: one main line for every location; header and footer of every old page.
MAIN_PHONE = '(343) 478-0196'
MAIN_TEL = '+13434780196'
# contacts.json emails[0]: general inquiries, footer of every old page.
GENERAL_EMAIL = 'info@iipct.com'
# contacts.json booking[0]: Ocean online booking, header "Schedule Your Visit" and footer "Book an Appointment" on every old page.
BOOKING_URL = 'https://ocean.cognisantmd.com/intake/patients.html?linkRef=23964341-fa0d-46a7-b261-29ad22a145a6#/online-booking'
# contacts.json newsletter[0]: main menu "Newsletter" item on every old page.
NEWSLETTER_URL = 'https://mailchi.mp/iipct/iipct-newsletter'
# The newsletter form (lib.newsletter) posts to the Mailchimp audience behind that page: its public form settings
# (https://mc.us22.list-manage.com/signup-form/settings?u=356268c1304222407acf3de5d&id=00d0dfe1f0, read 2026-11-22: one field,
# EMAIL; no human check) give the account u, audience id and form f_id. Host: the account's own list-manage host, where
# Mailchimp's own sign-up page for this audience posts its form; a GET of the form address answers 200 with that page
# (mc.us22.list-manage.com answers a GET with a redirect to this host). Never submit it in a test: it is a live list.
NEWSLETTER_FORM = dict(host='iipct-tmt.us22.list-manage.com', u='356268c1304222407acf3de5d', id='aeb4a67e2f', f_id='00d0dfe1f0')
# contacts.json social: footer icon links on every old page.
FACEBOOK_URL = 'https://www.facebook.com/IIPCT.TMT/'
TIKTOK_URL = 'https://www.tiktok.com/@theiipctcrew'

# ---------------------------------------------------------------- locations
# Source for every field unless noted: https://iipct.org/contact-us/ (clinics.json, re-checked in VERIFICATION.md).
# Ordered by the main line's menu option (press 1 to 5).
# hours: (days as the contact page groups them, opens, closes) in 24-hour time as the contact page writes it; None = closed.
LOCATIONS = [
    dict(key='tyendinaga', option=1,
         name='Tyendinaga Clinic', short='Tyendinaga', kind='Clinic',
         street='45 Meadow Drive', town='Tyendinaga', province='ON',
         # postal code: TB information sheet image images/2026-01_TB-2.webp ("45 Meadow Dr. Tyendinaga Territory Ontario K0K 1X0")
         postal='K0K 1X0',
         fax='(888) 999-6016',                    # contact page + footer, fax icon
         email='iipct.reception@iipct.com',
         hours=[('Mon', '08:30', '19:00'), ('Tue – Thu', '08:30', '16:30'), ('Fri', '07:30', '16:30'), ('Sat & Sun', None, None)],
         map_url='https://maps.app.goo.gl/iccMFePtJqWcBG347'),
    dict(key='kingston', option=2,
         name='Kingston Clinic', short='Kingston', kind='Clinic',
         street='730 Front Road', town='Kingston', province='ON',
         postal=None,                             # not given on the old site
         fax='(833) 999-1382',                    # contact page + footer, fax icon
         email='info@iipct.com',                  # the contact page gives info@ for Kingston
         hours=[('Mon', '08:30', '16:30'), ('Tue', '08:30', '16:30'), ('Wed', '08:30', '19:00'), ('Thu', '08:30', '16:30'),
                ('Fri', '08:30', '14:00'), ('Sat & Sun', None, None)],
         map_url='https://maps.app.goo.gl/MgTXA1Z384kMeK8s5'),
    dict(key='bancroft', option=3,
         name='Bancroft Clinic', short='Bancroft', kind='Clinic',
         street='69 Cleak Avenue', town='Bancroft', province='ON',
         postal=None,                             # not given on the old site
         fax='(613) 706-2001',                    # contact page + footer, fax icon (printed "(613)706-2001")
         # displayed address on the contact page; its link has a typo (bancroft.reeption@), the correct spelling is used here
         email='bancroft.reception@iipct.com',
         hours=[('Mon – Fri', '08:30', '16:30'), ('Sat & Sun', None, None)],
         map_url='https://maps.app.goo.gl/sRgYgAbrPq5KRZku7'),
    dict(key='deseronto', option=4,
         name='Deseronto Clinic', short='Deseronto', kind='Clinic',
         street='331 Dundas Street', town='Deseronto', province='ON',
         # The old site prints no postal code for this address (it appears only inside the footer's map link): left out.
         postal=None,
         fax='(613) 354-6992',                    # footer only, fax icon (the contact page shows no fax for Deseronto)
         email='iipct.reception@iipct.com',
         hours=[('Mon', '08:30', '19:00'), ('Tue – Thu', '08:30', '16:30'), ('Fri', '08:30', '13:00'), ('Sat & Sun', None, None)],
         # footer map link (the contact page shows this address without a link); tracking parameters removed
         map_url='https://www.google.ca/maps/place/331+Dundas+St,+Deseronto,+ON+K0K+1X0/@44.1977324,-77.0502582,20.5z'),
    dict(key='shannonville', option=5,
         # "Shannonville Office - Allied Health Team" on the contact page: an office, not a clinic.
         name='Shannonville Office (Allied Health Team)', short='Shannonville', kind='Office',
         street='14 York Road, Units 3 and 4', town='Shannonville', province='ON',
         # postal code: the old events calendar's venue record for 14 York Road, Unit 4 (venues.json)
         postal='K8N 4Z4',
         fax=None,                                # no fax listed anywhere
         email='iipct.reception@iipct.com',
         hours=[('Mon', '08:30', '18:30'), ('Tue – Thu', '08:30', '16:30'), ('Fri', '08:30', '14:30'), ('Sat & Sun', None, None)],
         # what is in each unit, as the contact page lists it
         units=['Unit 3: Physiotherapist, Traditional Healing, &amp; Management',
                'Unit 4: Mental Health Workers, Community Development Workers, &amp; Indigenous Life-Long Care Coordinator'],
         map_url='https://maps.app.goo.gl/qv38LoK6ZGpSbb1J9'),
]
BY_KEY = {l['key']: l for l in LOCATIONS}

# Who to ask for at each location, with their extension on the main line: the contact page's "Staff Extensions" lists
# (staff.json -> contact_page_extensions, all 32 rows checked verbatim in VERIFICATION.md). Names as the contact page
# writes them (two typographic clean-ups: "Rickard- Schaly" -> "Rickard-Schaly", "(on-leave)" -> "(on leave)").
# None = the contact page lists the person with no extension.
EXTENSIONS = {
    'tyendinaga': [('Nursing', [('Madison Weese', '125'), ('Sierra Bedford', '109'), ('Cassandra Weese', '123'), ('Chrystine Rickard-Schaly', '126')]),
                   ('Medical Office Administrator', [('Angela Spencer', '122')]),
                   ('Receptionists', [('Donna Brant / Katie Weese', '105')]),
                   ('Clinical Manager', [('Kiowa Sager', '102')])],
    'kingston': [('Nursing', [('Shaelee Jacklin', '215'), ('Jenessa McGuire', '205'), ('Tracey Keith', '208')]),
                 ('Mental Health', [('Caitlyn Vidal', '207')]),
                 ('Medical Office Administrator', [('Kim Burns', '202')]),
                 ('Receptionist', [('Kimberley E', '201')])],
    'bancroft': [('Nursing', [('Jessi Baker', '304')]),
                 ('Mental Health', [('Liz Passmore', '308')]),
                 ('Community Development Worker', [('Monica Sears', None)]),
                 ('Traditional Healing Coordinator', [('Sonya McCormick', None)]),
                 ('Medical Office Administrator', [('Marcy Francoeur', '301')]),
                 ('Clinical Manager', [('Melissa Daly', None)])],
    'deseronto': [('Medical Office Administrator', [('Kim Morris', '401')]),
                  ('Nursing', [('Courtney Loft / Jennifer Vancleaf', '405')]),
                  ('Management', [('Kiowa Sager', '404')])],
    'shannonville': [('Allied Health Administrator', [('Julie Emmons', '127')]),
                     ('Mental Health', [('Andrew Alkenbrack', '103'), ('Darcy Whalen (on leave)', '214')]),
                     ('Community Development Workers', [('Allison Loft', '213'), ('Kendra Garvin', '106'), ('Samantha Brant', None)]),
                     ('Traditional Healing Coordinator', [('Curtis Maracle', '116')]),
                     ('Indigenous Palliative Care Coordinator', [('Shelley Loft', '115')]),
                     ('Executive Assistant', [('Suzie Green', '108')]),
                     ('Allied Health Manager', [('Sarah Kring', '120')])],
}

# New patients: the Deseronto waitlist flyer on the old Events page (images/2026-06_Deseronto-Clinic-2026-5.jpg), in its
# own words. The flyer says "Press 3"; the contact page and the flu flyer say Deseronto is option 4, so option 4 is used.
WAITLIST = dict(
    location='deseronto',
    heading='Deseronto Clinic: accepting patients for waitlist',
    question='Are you Indigenous and in need of a family doctor or primary care provider, or hoping to find care closer to home?',
    how='Join our waitlist for Deseronto clinic by calling and speaking to our Reception',
    when='Monday to Friday, 8:30 am – 4:30 pm',
    must='Be Indigenous (Status &amp; Non-Status) to register with our clinic.',
)


# ---------------------------------------------------------------- formatting
def time12(hhmm):
    """'19:00' -> '7:00 pm' (the contact page writes 24-hour times; most readers expect am/pm)."""
    h, m = (int(x) for x in hhmm.split(':'))
    return f'{(h - 1) % 12 + 1}:{m:02d} {"am" if h < 12 else "pm"}'

def hours_rows(loc):
    """[(days, 'Closed' or '8:30 am – 4:30 pm'), ...] in the contact page's own grouping."""
    return [(d, 'Closed' if o is None else f'{time12(o)} – {time12(c)}') for d, o, c in loc['hours']]

def address(loc, postal=True):
    """'45 Meadow Drive, Tyendinaga, ON K0K 1X0'"""
    pc = f' {loc["postal"]}' if postal and loc.get('postal') else ''
    return f'{loc["street"]}, {loc["town"]}, {loc["province"]}{pc}'

def option_text(loc):
    return f'press {loc["option"]}'
