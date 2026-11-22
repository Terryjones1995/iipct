"""Our Team: everyone on the old iipct.org Who We Are page, grouped the way that page groups them (leadership first, then
by location). Names, titles and biographies are copied from the old page (content/old-site/staff.json, as corrected in
VERIFICATION.md). Changes from the old wording, each listed in the work notes: three plain title typos fixed
('Executive Directive', 'Nurse Practicitioner', 'Administator'); the organisation's name written 'Tsi Kanonhkhwatsheríyo'
in the biographies; the biographies of Kendra, Shaelee and Kim Morris held back because they contradict the card's title
or clinic (IIPCT to confirm). Nine people have no photograph on the old site: they get an initials tile, never a stand-in."""
from lib import *

# section key -> (anchor id, heading as IIPCT names the location)
LOCATIONS = [('leadership', 'leadership', 'Leadership'),
             ('tyendinaga', 'tyendinaga-clinic', 'Tyendinaga Clinic'),
             ('shannonville', 'shannonville-office', 'Shannonville Office (Allied Health Team)'),
             ('kingston', 'kingston-clinic', 'Kingston Clinic'),
             ('bancroft', 'bancroft-clinic', 'Bancroft Clinic'),
             ('deseronto', 'deseronto-clinic', 'Deseronto Clinic')]
TEAM_PAGE = 'our-team.html'      # links with an #anchor use the published file name (export only rewrites bare .dc.html links)

# (old card number, section, anchor, name as printed, short name, title as printed, on leave, photo file in site-img/people/, biography paragraphs)
TEAM = [
  (1, 'leadership', 'tera-osborne', 'Tera Osborne', 'Tera Osborne', 'Executive Director', False, 'tera-osborne',
   ['Tera is a Registered Nurse and loves working with Indigenous communities to help improve overall health and wellness. Our goal as a team is to expand our services to cover our catchment area and provide services tailored to the needs of each community we care for.', "Tera was born and raised in Napanee and continues to live there now. She has a husband, Justin, and 3 children, Isaac, Jack, and Mia. Tera’s maternal grandmother was Indigenous. Her father was Algonquin and grew up in the Pembroke area; her mother was Metis and grew up near Barry’s Bay. Unfortunately, her grandmother was not exposed to her parents' culture growing up, so Tera continues to learn about the important history of Indigenous People and how important it is to incorporate culture into overall wellness."]),
  (2, 'tyendinaga', 'kiowa-sager', 'Kiowa Sager', 'Kiowa', 'Clinical Manager', False, 'kiowa-sager',
   ['Kiowa is a proud Haudenosaunee woman from Kenhtè:ke (Tyendinaga Mohawk Territory) and a graduate of Queen’s University’s Bachelor of Nursing Science program. She lives in the community with her family. She’s passionate about providing high-quality, culturally safe care in her home community and beyond.']),
  (3, 'tyendinaga', 'dr-kim-edwards', 'Dr. Kim Edwards', 'Dr. Edwards', 'Physician', False, 'kim-edwards',
   ['Kim Edwards is Cree from Attawapiskat and grew up in the Ottawa Valley. She completed medical school in Sudbury at the Northern Ontario School of Medicine and Family Medicine Residency in Belleville, where she now lives with her family. In Kim’s spare time, she enjoys travelling, reading, and spending time with my loved ones.']),
  (4, 'tyendinaga', 'dr-jamaica-cass', 'Dr. Jamaica Cass, MD, PhD, CCFP DABOM', 'Dr. Cass', 'Physician', False, 'jamaica-cass',
   ['Dr. Jamaica Cass, a member of the Mohawks of the Bay of Quinte, provides both primary care and metabolic health care at the IIPCT. She grew up nearby in Belleville, and received her BScH in biological science from the University of Guelph, her PhD in breast cancer molecular biology from Queen’s University, and her MD from Tulane University in New Orleans, Louisiana. Prior to family medicine training, Dr. Cass spent three years training as a general surgeon. Outside of clinical practice, her professional interests are all driven by her desire to advance reconciliation in medical education and healthcare. She is the first Director of the Queen’s Weeneebayko Health Education Program and the Director of Indigenous Health at Queen’s University.', 'Dr. Cass is the first Indigenous woman in Canada to earn both an MD and a PhD. A national leader in Indigenous health education, she has driven advocacy and change through leadership roles with Ontario Health, the Indigenous Physicians Association of Canada, the Medical Council of Canada, the National Circle on Indigenous Medical Education, and the Indigenous Health Committee of the Association of Faculties of Medicine of Canada. She holds faculty appointments at both Queen’s University and Toronto Metropolitan University. Her work in education, mentorship, and community impact has earned numerous honours, including the King Charles III Coronation Medal.', 'Outside of professional interests, Dr. Cass enjoys creating beadwork and garments blending Indigenous and contemporary elements.']),
  (5, 'tyendinaga', 'charmaine', 'Charmaine', 'Charmaine', 'Nurse Practitioner', False, 'charmaine',
   None),
  (6, 'tyendinaga', 'sierra-bedford', 'Sierra Bedford', 'Sierra', 'Registered Practical Nurse', False, 'sierra-bedford',
   ['Sierra is a Mohawk First Nation from Kenhtè:ke. She received her diploma as a Registered Practical Nurse in 2020 and has worked at Tsi Kanonhkhwatsheríyo since then. You can find Sierra at the Tyendinaga Clinic, and my roles at the clinic include advanced diabetic foot care, well baby/child visits, routine immunizations, blood work, chronic disease management/support, and many more. Her spare time is spent with family and loved ones, and enjoying all the time she can in nature.']),
  (7, 'tyendinaga', 'cassandra', 'Cassandra', 'Cassandra', 'Registered Practical Nurse', False, 'cassandra',
   ['Cassandra is a Registered Practical Nurse (RPN) with over 10 years of nursing experience and a passion for community-based healthcare. Living on the territory with her family, she is proud to provide care to the community through her role with the Indigenous Interprofessional Primary Care Team.', 'Her clinical interests include chronic disease management, preventative care, diabetic education, and advanced diabetic foot care. Cassandra also holds certifications in Gerontology and Palliative Care, Advanced Diabetic Foot Care as well as Clinical Skills in Gynecological Health. She believes in empowering patients through education, support, and compassionate care.', 'When she is not working, Cassandra enjoys spending time with her husband and four children and can often be found cheering from the sidelines or driving between hockey, school, and extracurricular activities. She values family, community, and making the most of time spent together.']),
  (8, 'tyendinaga', 'madison', 'Madison', 'Madison', 'Registered Nurse', False, 'madison',
   ['Madison is a member of the Mohawks of the Bay of Quinte and resides on Territory with her partner and daughter. Madison is a Registered Nurse and graduate of Flemming College, Centennial College, and Ryerson University. In her spare time, Madison enjoys spending time with family and friends, beading, and being active.']),
  (9, 'tyendinaga', 'angela-spencer', 'Angela Spencer', 'Angela', 'Medical Office Administrator', False, None,
   None),
  (10, 'tyendinaga', 'donna-brant', 'Donna Brant', 'Donna', 'Receptionist', False, 'donna-brant',
   ['Donna is a member of the Mohawk First Nation and has resided on the Tyendinaga Mohawk Territory for the past 36 years. Alongside her husband, she raised two sons in the heart of the community. Donna joined IIPCT in 2021, bringing 34 years of experience working in the medical field. Donna shares the receptionist role in the Tyendinaga Clinic. She takes pride in supporting culturally grounded healthcare services. Donna’s commitment to community wellness and the people she serves is at the core of her work.']),
  (11, 'tyendinaga', 'katie', 'Katie', 'Katie', 'Receptionist', False, None,
   None),
  (12, 'tyendinaga', 'chrystine-rickard-schaly', 'Chrystine Rickard-Schaly RN, BScN, RN CDE', 'Chrystine', 'Certified Diabetes Educator', False, 'chrystine-rickard-schaly',
   ['Chrystine is a graduate of Lakehead University School of Nursing. She is also a Certified Diabetes Educator. Chrystine lives in Belleville with her husband and 2 children. She is committed to holistic client centred care.']),
  (13, 'tyendinaga', 'bill-loft', 'Bill Loft', 'Bill', 'Custodian', False, None,
   ['Bill Loft is a status member of the Mohawks of the Bay of Quinte. Bill is married with 2 daughters and 7 grandchildren. He worked as Quality Control in the food industry for 32 years and has been working in sanitation (custodian) for about 12 years. Joined IIPCT in 2020.']),
  (14, 'shannonville', 'sarah-kring', 'Sarah Kring', 'Sarah', 'Allied Health Manager', False, 'sarah-kring',
   ["I currently live on-territory with my family. My husband and children are Mohawk First Nation. I am a Registered Social Service Worker with a Bachelor's degree in Psychology and Sociology. I am a Certified Tobacco Educator, and I enjoy reading, golfing, and soccer."]),
  (15, 'shannonville', 'andrew-alkenbrack', 'Andrew Alkenbrack', 'Andrew Alkenbrack', 'Registered Psychotherapist', False, 'andrew-alkenbrack',
   ['Originally from the Tyendinaga area, Andrew has worked in the mental health field for over 25 years, in both private practice and in a hospital setting. Clinical experience and training with children, adolescents, and adults over the years allow for treating a diverse population.', 'Andrew has an undergraduate degree in Psychology from York University and a Master of Arts in Counselling from Yorkville University. He is a Registered Psychotherapist with the College of Registered Psychotherapists of Ontario (# 001878).', 'Cognitive Behavioural Therapy (CBT) is his usual modality of therapy, which is often identified as one of the most effective forms of therapy for dealing with mood and anxiety problems. As a member of the Mohawks of the Bay of Quinte, Andrew also utilizes a First Nations perspective on mental and overall health, with a focus on balance in various aspects of one’s life. Andrew also received training in Solution-Focused Brief Therapy, EMDR, and Anger Solutions.', 'His approach is client-centred, with a focus on helping clients identify and achieve their goals. Andrew looks forward to helping you navigate life’s journey.']),
  (16, 'shannonville', 'darcy-whalen', 'Darcy Whalen', 'Darcy', 'Registered Social Worker', True, 'darcy-whalen',
   ['Shékon sewakwekon. I was born and raised in Belleville, Ontario, and I am a member of the Mohawks of the Bay of Quinte. For the past 8 years, I have lived in Prince Edward County, Ontario, with my husband and son.', 'I graduated from Loyalist College with my Social Service Worker diploma in 2016 and then from Trent University with my Bachelor of Social Work in the Honours Program in 2019. I have been privileged to support individuals at Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team for the past 5 years as a Registered Social Worker. Over the past 5 years, I have worked with both Indigenous and non-Indigenous individuals to foster holistic balance by providing mental health counselling, cultural programming, advocacy, psychoeducation, and more. I am passionate about walking alongside others as they find their path to healing and wellbeing.']),
  (17, 'shannonville', 'shelley-loft', 'Shelley Loft', 'Shelley', 'Indigenous Palliative Care Coordinator', False, 'shelley-loft',
   ['I have lived on-territory with my family for 18 years. My husband and children are members of the Mohawks of the Bay of Quinte. I have been a PSW working in Community Care and Long-Term Care for 30 years. Over the years, I have done training programs, workshops, and online courses to help educate myself in palliative care. I have certificates in Palliative Care in Indigenous Communities through Lakehead University. Furthering my studies in Continuing the Journey and Leap Training for Indigenous Communities, along with Death Doula training. I enjoy spending time with my family, making earrings, shopping, and reading.']),
  (18, 'shannonville', 'curtis-maracle', 'Curtis Maracle', 'Curtis', 'Traditional Healing Coordinator', False, 'curtis-maracle',
   ['Sekoh Sewakwekon,Tehanatoken yonkya’ts, Kanyenke’haka ki ni’i tanon Kenhteke (TMT) kenakere.', 'I am the Traditional Healing Coordinator, and my position is to facilitate between traditional healers and Tsi Kanonhkhwatsheríyo patients identifying with First Nations heritage in our catchment area who want an alternative to pharmaceutical medicines. I can also research and provide education for traditional medicines and find people for traditional teachings regarding medicines and culture for any of the First Nations patients of Tsi Kanonhkhwatsheríyo. I also work with the Tsi Kanonhkhwatsheríyo’s Community Development Workers, helping with cultural education and social events in our catchment area.']),
  (19, 'shannonville', 'kendra-garvin', 'Kendra Garvin', 'Kendra', 'Community Development Worker', False, 'kendra-garvin',
   None),
  (20, 'shannonville', 'allison-loft', 'Allison Loft', 'Allison', 'Community Development Worker', False, 'allison-loft',
   ['Allison Loft grew up in Belleville, Ontario, just outside of Kenhtèke (Tyendinaga Mohawk Territory). She currently lives on the Tyendinaga Mohawk Territory as a Mohawks of the Bay of Quinte member with her son.', 'Allison’s role is to connect self-identifying Indigenous people to services, events, and programs to help their whole being. She focuses on Indigenous specific events and programs, and looks into the tradition of why we do what we do. She continues to learn about the ways of our people and our Mohawk language.', 'She graduated from Loyalist College in 2019 for Public Relations and Event Management, as well as from Algonquin College in 2018 for Recreation and Leisure Services.', 'In her spare time, she enjoys hanging out with family and friends, beading, and watching a good true crime documentary.']),
  (21, 'shannonville', 'samantha', 'Samantha', 'Samantha', 'Community Development Worker', False, 'samantha',
   None),
  (22, 'shannonville', 'pawandeep', 'Pawandeep', 'Pawandeep', 'Physiotherapist', False, None,
   None),
  (23, 'shannonville', 'juliann-emmons', 'Juliann Emmons', 'Juliann', 'Medical Office Administrator', False, 'juliann-emmons',
   None),
  (24, 'shannonville', 'jamie-maracle', 'Jamie Maracle', 'Jamie', 'Community Development Worker', True, None,
   ["I am Mohawk, born and raised in Tyendinaga Mohawk Territory. I currently live on-territory with my family. I am a Registered Social Service Worker with a Bachelor's degree in Psychology and am a Certified Tobacco Educator. I enjoy beading, golfing, and spending time with my family."]),
  (25, 'shannonville', 'suzie-green', 'Suzie Green', 'Suzie', 'Executive Assistant', False, 'suzie-green',
   None),
  (26, 'shannonville', 'amanda', 'Amanda', 'Amanda', 'Human Resources Business Manager', False, None,
   None),
  (27, 'kingston', 'shaelee-jacklin', 'Shaelee Jacklin', 'Shaelee', 'Clinical Manager', False, 'shaelee-jacklin',
   None),
  (28, 'kingston', 'dr-matt-dumas', 'Dr. Matt Dumas', 'Dr. Dumas', 'Physician', False, 'matt-dumas',
   ["Aaniin! Dr Matt Dumas is an Ojibway family physician who grew up in North Bay. Matt enjoyed summers on the French River while visiting his family's cottage on the Dokis First Nation. Matt is a graduate of the Life Science program, School of Undergraduate Medicine and Family Medicine at Queen’s University. Matt decided to practice in eastern Ontario as the scenery reminded him of North Bay. Matt has been practicing for 9 years in a rural community setting, which he enjoys very much. During his free time, he enjoys walking in the woods, enjoying nature, geocaching, as well as solving escape room puzzles."]),
  (29, 'kingston', 'kristine-canty', 'Kristine Canty', 'Kristine', 'Nurse Practitioner', False, 'kristine-canty',
   ['Kristine Canty, RN(EC), is originally from the northwestern community of Red Lake, Ontario. She completed her Honours Bachelor of Science in Nursing in 1994 at Lakehead University and returned to her home town of Red Lake to work in Red Lake Margaret Cochenour Hospital for 2 years before moving to the Kingston area. She worked in home care for a few years and then became a Certified Diabetes Educator and worked at Hotel Dieu Hospital Diabetes Education Centre for 14 years. In 2006, she began the Primary Care Nurse Practitioner Program at Queens University and graduated in 2008. This then took her to Maple Family Health Team, working as a primary care NP. After 3 years, Kristine accepted a position at KHSC within the Kingston Bariatric Centre of Excellence, helping to develop the program and working as a Nurse Practitioner supporting people making positive lifestyle changes. In 2023, Kristine began working at the IIPCT in Kingston and remains in this role today. She loves her role working with and supporting Indigenous patients and their families. Kristine enjoys spending time with her family, her German shepherd Coco, camping, kayaking, reading, and enjoying nature.']),
  (30, 'kingston', 'jenessa', 'Jenessa', 'Jenessa', 'Registered Nurse', False, None,
   None),
  (31, 'kingston', 'jennifer-vancleaf', 'Jennifer Vancleaf', 'Jennifer', 'Registered Practical Nurse', False, None,
   None),
  (32, 'kingston', 'caitlyn-westerberg', 'Caitlyn Westerberg', 'Caitlyn', 'Registered Social Worker', False, None,
   None),
  (33, 'kingston', 'hannah-kirkland', 'Hannah Kirkland', 'Hannah', 'Registered Social Worker', True, 'hannah-kirkland',
   ['My name is Hannah Kirkland, and I am a Registered Social Worker that works as a Mental Health Worker at the Kingston office of IIPCT. I have a bachelor’s degree in social work from Laurentian University and have been working at IIPCT since May of 2024. Before working at IIPCT, I have had experience working at an Indigenous child welfare agency as well as experience in a school placement at the hospital in Sudbury, Ontario, on their mental health unit. I love reading and I use it as my self-care after my workdays, maybe too much as I’ve read over 300 books in a year before…self-care is important though, especially in the mental health field, so it’s okay.']),
  (34, 'kingston', 'kim-burns', 'Kim Burns', 'Kim', 'Medical Office Administrator', False, 'kim-burns',
   ['I am the Medical Office Administrator here at Tsi Kanonhkhwatsheríyo IIPCT. I live in Tamworth with my husband and two children.', 'I graduated from St. Lawrence College in June 1996 with a diploma in Early Childhood Education. I was a preschool nanny for a family of 5 for 4 years. I then worked for Kingston Daycare Inc. in Kingston for the next 8 years. I have since worked in a retirement residence and at CIBC as a CSR.', 'I have been with IIPCT since June 2023 and look forward to contributing to our vastly growing office in Kingston.', 'In my spare time, I love spending time with my family at our trailer.']),
  (35, 'kingston', 'mariah-miller', 'Mariah Miller', 'Mariah', 'Registered Nurse', True, 'mariah-miller',
   ['I am one of the Registered Nurses at IIPCT. I originally lived in Edmonton, Alberta, where I completed my BScN program at MacEwan University. I moved to Ontario shortly thereafter to be with my much-loved husband.', 'I pride myself on friendly, informative patient interactions and treating every person equally, regardless of race, age, sexual orientation, sex, gender, social status, health conditions, disability, or spiritual beliefs.', 'In my free time, I enjoy reading, writing, and spending time with my husband and our two cats']),
  (36, 'kingston', 'kimberley-esquimaux', 'Kimberley Esquimaux', 'Kimberley', 'Receptionist', False, 'kimberley-esquimaux',
   ['Kimberley is a dedicated professional with a recent Honours Diploma in Business Management. She brings a diverse background to her current role at IIPCT, with a strong foundation in long-term care nursing and academic studies in Social Service Work, Gerontology, Practical Nursing, and Police Foundations. Throughout her career, Kimberley has demonstrated a deep commitment to supporting individuals and communities, drawing on her multidisciplinary education and hands-on experience in healthcare and social services. Outside of her professional life, Kimberley is a proud wife and mother of three. She values quality time with her family and pets &amp; embraces her cultural heritage as a Women’s Traditional dancer, regularly participating in Pow Wows. She also enjoys road trips, home improvement projects, and exploring new ways to stay connected to her community and culture.']),
  (37, 'bancroft', 'melissa', 'Melissa', 'Melissa', 'Bancroft Clinic Manager', False, 'melissa',
   ['Melissa is the Clinical Manager for the Bancroft IIPCT clinic. She is a Registered Nurse with over 15 years of nursing experience, from critical care to dialysis to hospital and community care coordination.', 'Melissa has developed a growing passion for building community connections, while continuing to learn, respect, and strengthen her knowledge of Indigenous cultures and ways of being. Recently discovering her own Métis lineage has been a meaningful part of her personal journey, inspiring her to deepen her understanding of her heritage, cultures, and traditions.', 'Melissa enjoys spending time with her family, cherishing the simple moments with her young son and husband, being outdoors and on the water, and embracing off-grid living on her family’s ancestral land.']),
  (38, 'bancroft', 'erica-harder', 'Erica Harder', 'Erica', 'Nurse Practitioner', False, 'erica-harder',
   ['Erica Harder is a Nurse Practitioner with the Indigenous Interprofessional Primary Care Team in Bancroft. She completed her Master of Nursing and Primary Health Care Nurse Practitioner program at Queen’s University and brings over 15 years of critical care nursing experience, including international critical care flight nursing. She is also certified in critical care through the Canadian Nurses Association (CNCC-C).', 'Erica is passionate about evidence-based practice and research, pain and chronic illness management, and advocating for underserved populations. Her experience also includes maternal, emergency, and rural community health care in Tanzania, which strengthened her commitment to accessible and equitable care. Having grown up on a farm, Erica enjoys the outdoors and values the opportunity to support health and wellbeing in rural communities.']),
  (39, 'bancroft', 'jessi-baker', 'Jessi Baker', 'Jessi', 'Registered Nurse', False, 'jessi-baker',
   ['I am one of the Registered Nurses at the IIPCT, working at the Bancroft site. I have always lived in Centre Hastings and love living rurally. I have obtained a BA in Psychology from Trent University (2014), my Registered Practical Nursing diploma from Loyalist College (2018), and my Bachelor of Science in Nursing from Nipissing University (2025). My past nursing experience has primarily been in the areas of inpatient medicine and more recently, minor surgical procedures. I have also worked as a nurse in the community supporting patients to manage opioid use disorders. I have additional certifications in palliative care and dementia care. I am passionate about providing holistic, patient-centred care and ensuring that clients feel supported and empowered on their wellness journeys.']),
  (40, 'bancroft', 'marcy', 'Marcy', 'Marcy', 'Receptionist/Medical Office Administrator', False, 'marcy',
   ['Marcy is an experienced administrative assistant and operations professional with a strong background in Indigenous governance, community services, and trauma informed practice.', 'Her previous roles include serving as Administrative Support Specialist with the Algonquins of Pikwakanagan First Nation Chief and Council and the Manager of Political operations and as an Administrative Specialist with Dnaagdanwenmag Biinnoojiiyag Child &amp; Family services, where she provided comprehensive support to leadership teams, frontline staff, and multi-disciplinary service areas.', 'Marcy joined the Indigenous Interprofessional Primary Care Team and will serve as the administrative assistant/receptionist for the Bancroft office. Marcy brings cultural awareness, empathy, community centered values and commitment to culturally safe care.']),
  (41, 'bancroft', 'monica', 'Monica', 'Monica', 'Community Development Worker', False, 'monica',
   ["Monica is a French-speaking Mi'kmaq woman living on the unceded traditional territory of the Anishinaabeg Algonquin Peoples in Bancroft. She is dedicated to building meaningful relationships, creating inclusive spaces, and supporting individuals and communities through warmth, compassion, and collaboration.", 'With a background in therapeutic recreation, volunteering, community programming, and event coordination, Monica enjoys bringing people together by creating opportunities that foster belonging, and growth. She is committed to respecting and honouring a lifelong learning of Indigenous knowledge, traditions, and ways of being.', 'Outside of work, Monica enjoys spending time with her daughter and strengthening their connection to the land.']),
  (42, 'bancroft', 'sonya', 'Sonya', 'Sonya', 'Traditional Healing Coordinator', False, 'sonya',
   ['Sonya is the Traditional Healing Coordinator at Tsi Kanonhkhwatsheríyo IIPCT Bancroft office, where she facilitates connections between Traditional Healers and clients who wish to reconnect with their Indigenous roots and traditional ways of healing.', 'She grew up in Bancroft, where she built her home and raised her children. She has always appreciated and fostered close ties to the local Indigenous communities, being committed to remaining a strong ally. She is also a firefighter, reflecting her dedication to serving and protecting her community in multiple ways.', 'Sonya is a graduate of Loyalist College, where she completed the Educational Assistant program. Her education, combined with her passion for helping others, supports her commitment to meeting the unique needs and goals of each client with compassion and respect.', 'Outside of her work, Sonya enjoys spending time with her family, crafting, and embracing the outdoors whenever she can. Her strong passion for her community and her dedication to supporting others makes her a valued member of the Tsi Kanonhkhwatsheríyo team.']),
  (43, 'deseronto', 'dr-ryan-mcconnell', 'Dr. Ryan McConnell', 'Dr. McConnell', 'Family Physician', False, 'ryan-mcconnell',
   None),
  (44, 'deseronto', 'tracy-keith', 'Tracy Keith', 'Tracy', 'Registered Practical Nurse', False, 'tracy-keith',
   ['Tracy believes that prevention and education are the foundation of good health. She provides gentle, thorough footcare, well-women’s exams and community outreach and prevention services designed to help clients stay healthy and make preventative healthcare accessible for the community she serves. Her friendly compassionate approach helps people feel comfortable and cared for each step of the way.', 'When she is not at work, you can find Tracy on the sidelines of a football game or in the arena cheering on her 3 boys.']),
  (45, 'deseronto', 'taryn', 'Taryn', 'Taryn', 'Nurse Practitioner', False, 'taryn',
   None),
  (46, 'deseronto', 'kim-morris', 'Kim Morris', 'Kim', 'Receptionist/Medical Office Administrator', False, 'kim-morris',
   None),
  (47, 'deseronto', 'courtney-loft', 'Courtney Loft', 'Courtney', 'Registered Practical Nurse', False, 'courtney-loft',
   None),
]

TONES = [('#8E9C7A', '#6F8263'), ('#BD7862', '#9E5540'), ('#C9A26E', '#A88250'), ('#4E6B4B', '#36503A')]

def initials(name):
    words = [w for w in re.sub(r'^Dr\.\s*', '', name.split(',')[0]).split() if w[0].isalpha()]
    return ''.join(w[0] for w in words[:2]).upper()

def portrait(person, size=112, radius=12, style=''):
    """The person's photograph, or an initials tile when the old site has none."""
    num, sec, a, name, short, role, leave, photo_file, bio = person
    box = f'flex: none; width: {size}px; height: {size}px; border-radius: {radius}px; {style}'
    if photo_file:
        return photo(f'people/{photo_file}.jpg', f'Photo of {short}', f'{box}; object-fit: cover; border: 1px solid {LINE}', w=600, h=600)
    hi, lo = TONES[num % len(TONES)]
    return (f'<span aria-hidden="true" style="{box}; display: flex; align-items: center; justify-content: center; '
            f'background: radial-gradient(circle at 38% 30%, {hi} 0%, {lo} 80%); border: 1px solid {LINE}; '
            f'font-family: {SERIF}; font-weight: 600; font-size: {round(size * 0.34)}px; letter-spacing: 0.02em; color: #FCF2DF">{initials(name)}</span>')

def member_card(person):
    num, sec, a, name, short, role, leave, photo_file, bio = person
    lv = (f'<span style="margin-top: 4px; display: inline-block; padding: 4px 10px 3px; border-radius: 6px; background: #F1D5C8; border: 1px solid #D9A892; font-size: 12px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; line-height: 1.2; color: #2A2A1C">On leave</span>' if leave else '')
    more = ''
    if bio:
        paras = ''.join(f'<p style="margin: 0; font-size: 14px; line-height: 1.55; color: {INK}">{t}</p>' for t in bio)
        more = (f'<details style="border-top: 1px solid #E6D9BF">'
                f'<summary style="padding: 10px 2px; min-height: 40px; line-height: 20px; font-size: 14px; font-weight: 600; color: {RUST}; cursor: pointer">Read more about {short}</summary>'
                f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 2px 2px 6px">{paras}</div></details>')
    return (f'<article id="{a}" style="scroll-margin-top: 16px; display: flex; flex-direction: column; gap: 12px; padding: 14px; border-radius: 14px; {CARD}">'
            f'<div style="display: flex; align-items: center; gap: 16px">{portrait(person)}'
            f'<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 4px">'
            f'<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 19px; line-height: 1.15; letter-spacing: -0.014em; color: {HEAD}; overflow-wrap: anywhere">{name}</h3>'
            f'<p style="margin: 0; font-size: 14px; line-height: 1.35; color: {INK}; overflow-wrap: anywhere">{role}</p>{lv}</div></div>{more}</article>')

def jump_links():
    pill = (f'display: inline-flex; align-items: center; min-height: 40px; padding: 0 16px; border-radius: 999px; background: #FFFDF8; '
            f'border: 1px solid #C9B691; font-size: 13.6px; font-weight: 600; line-height: 1.2; color: {HEAD}; text-decoration: none')
    links = ''.join(f'<a class="btn bo" href="#{aid}" style="{pill}">{label}</a>' for key, aid, label in LOCATIONS)
    return f'<nav aria-label="Team by location" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px">{links}</nav>'

def page():
    s = header('who')
    s += sub_hero([('Home', 'Main.dc.html'), ('Who We Are', 'WhoWeAre.dc.html'), ('Our Team', None)],
                  'Our Team',
                  'Our team is made up of highly trained and culturally safe professionals eager to provide care to the communities we serve.',
                  eyebrow_txt='Who We Are', extra=jump_links())
    secs = ''
    for key, aid, label in LOCATIONS:
        people = [m for m in TEAM if m[1] == key]
        where = '' if key == 'leadership' else textlink('Address, phone and hours', 'Contact.dc.html', 13.6, 'min-height: 40px')
        secs += (f'<section id="{aid}" aria-labelledby="{aid}-h" style="scroll-margin-top: 16px; display: flex; flex-direction: column; gap: 14px">'
                 f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 22px; padding-bottom: 10px; border-bottom: 1px solid {GOLDL}">'
                 + h2(label, 27, HEAD, 'flex: 1 1 auto', 'h2').replace('<h2 ', f'<h2 id="{aid}-h" ', 1)
                 + f'<span style="font-size: 13.6px; font-weight: 600; color: {MUTED}">{len(people)} {"person" if len(people) == 1 else "people"}</span>{where}</div>'
                 f'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(330px, 100%), 1fr)); gap: 16px">'
                 + ''.join(member_card(m) for m in people) + '</div></section>')
    s += f'''
<div style="{WRAP}; padding: 30px 48px 8px 83px; display: flex; flex-direction: column; gap: 40px">
{secs}
</div>
<div style="margin-top: 36px">{cta_band('Book a visit or reach a clinic', 'Book online, or contact a clinic and reception will help.')}</div>'''
    s += footer()
    return 'IIPCT — Our Team', s
