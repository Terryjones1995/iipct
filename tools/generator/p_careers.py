from lib import *

def benefit_card(icon, tone, title, text):
    return f'''<div style="display: flex; flex-direction: column; align-items: center; text-align: center; gap: 7px; min-height: 186px; padding: 13px 6px 14px; border-radius: 14px; {CARD}">
{circ(icon, tone, 60, 31, 1.45)}
<h3 style="margin: 5px 0 0; font-family: {SERIF}; font-weight: 700; font-size: 17.4px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 13.4px; line-height: 1.36; letter-spacing: -0.012em; color: {INK}">{text}</p>
</div>'''

def job_card(photo, alt, title, place, text):
    return f'''<article class="card" style="display: flex; flex-wrap: wrap; align-items: stretch; gap: 0 34px; padding: 9px; border-radius: 14px; {CARD}">
<div class="fbs mh-s" style="flex: 0 0 186px; position: relative; min-height: 156px">{img(photo, alt, 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 8px')}</div>
<div class="pads2" style="flex: 1 1 300px; min-width: 0; padding: 4px 10px 6px 0; display: flex; flex-direction: column; align-items: flex-start; gap: 9px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 21.2px; line-height: 1.08; letter-spacing: -0.02em; color: {HEAD}">{title}</h3>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 16px; margin-top: 4px; font-size: 13.4px; font-weight: 600; color: {HEAD}">
<span style="display: flex; align-items: center; gap: 9px">{pin_fill(17)}<span>{place}</span></span>
<span aria-hidden="true" style="width: 1px; height: 14px; background: #8E8A7A"></span>
<span style="display: flex; align-items: center; gap: 10px">{ico('briefcase', 18, '#A3301C', 1.8)}<span>Full-Time</span></span>
</div>
<p style="margin: 0; font-size: 13.6px; line-height: 1.38; color: {INK}">{text}</p>
{btn('View Job Details', '#', 'soft', None, True, 'sm', 'margin-top: 1px; padding: 0 24px; gap: 13px; font-size: 13.4px; border-radius: 10px')}
</div>
</article>'''

def hire_step(icon, tone, title, text, last=False):
    arrow = '' if last else f'<span class="hide-s" aria-hidden="true" style="position: absolute; right: -14px; top: 14px">{ico("arrow", 24, "#93402B", 1.5)}</span>'
    return f'''<div style="position: relative; flex: 1 1 150px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 4px">
{circ(icon, tone, 54, 28, 1.5)}
<h3 style="margin: 6px 0 0; font-size: 15.8px; font-weight: 700; line-height: 1.2; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 13px; line-height: 1.36; color: {INK}">{text}</p>
{arrow}
</div>'''

def page():
    buttons = (btn('View Current Opportunities', '#jobs', 'primary', 'calendar-check', False, 'md', 'padding: 0 24px; gap: 10px')
               + btn('Get Hiring Updates', '#updates', 'outline', 'mail', False, 'md', 'padding: 0 24px; gap: 10px'))
    s = header('careers')
    s += hero('hero-careers', 61.2, 334, 'Career<br>Opportunities',
              'Join the IIPCT team and help advance<br>culturally grounded, whole-person care for<br>Indigenous communities across southeastern Ontario.', buttons,
              h1_size=52, lead_size=18.8, lead_lh=1.36, pad='30px 0 38px 88px', gap=11, btn_mt=10, sq_mt=2, obj='center 30%')
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 50px 0 56px; margin-top: 16px">
<div class="sts pads gap-s" style="display: flex; align-items: center; gap: 40px; padding: 13px 30px 14px 42px; border-radius: 14px; {CARD}">
{circ('hand-sprout', 'sage', 76, 40, 1.4)}
<div style="display: flex; flex-direction: column; gap: 6px">
{h2('Serve Community Through Culturally Grounded Care', 21.8, HEAD, '', 'h2', 700)}
{p('At IIPCT, we provide whole-person, culturally safe primary care that honours Indigenous ways of knowing, health and well-being.<br>Our team works in partnership with individuals, families, and communities to deliver compassionate, inclusive, and community-led care.', 15.4, INK, 1.4)}
</div>
</div>
</section>'''
    body = p('Be part of a collaborative, values-driven team that centres Indigenous health, community wellness, and whole-person care. At IIPCT, your work contributes to healthier people, stronger communities, and more culturally grounded health care close to home.', 15.6, INK, 1.32, 'max-width: 440px; padding-left: 12px; margin-top: 8px')
    feats = feature_list([('feather', 'Purpose-Driven Work', 'Make a real difference in the health and<br>well-being of Indigenous communities.'),
                          ('people', 'Collaborative &amp; Respectful Culture', 'Work in a supportive, interdisciplinary team that values each person’s expertise and lived experience.'),
                          ('heart', 'Culturally Safe &amp; Inclusive', 'Contribute to care that respects culture, identity,<br>language, and community priorities.')], 46, 15.8, 28, 13.3, 26)
    s += split_section(arc_photo('car-lake', 'Lakeshore at sunset framed by pines', 'flex: 1; min-height: 262px', '58% 62%', '40% 46%'),
                       'Why Work at IIPCT', 'A Meaningful Career<br>with Lasting Impact', body,
                       btn('Learn More About Our Team', 'WhoWeAre.dc.html', 'primary', None, True, 'sm', 'margin-left: 12px; padding: 0 26px; gap: 14px; font-size: 13.6px; min-height: 38px'), feats, 'margin-top: 24px', 33.8, '32.4%')
    s += f'''
<section style="position: relative; {WRAP}; padding: 26px 50px 0 68px">
{branch(118, '#B5BFA6', 0.5, 'right: -22px; top: -28px; transform: rotate(-150deg)')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 56px; padding-left: 15px">
<div style="display: flex; flex-direction: column; gap: 5px">{eyebrow('Benefits &amp; Perks')}{h2('A Supportive Place to Grow', 32.4)}</div>
{vdiv('40px')}
{p('We value our team and offer a comprehensive benefits package,<br>professional development opportunities, and a healthy work-life balance.', 14.4, INK, 1.4, 'flex: 1 1 380px')}
</div>
<div style="position: relative; margin-top: 16px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(190px, 100%), 1fr)); gap: 12px">
{benefit_card('heart-plus', 'sage', 'Health &amp; Wellness<br>Benefits', 'Comprehensive benefits<br>to support you and<br>your family.')}
{benefit_card('sprout', 'rust', 'Professional<br>Development', 'Ongoing learning, training,<br>and growth opportunities.')}
{benefit_card('people', 'gold', 'Supportive<br>Team Environment', 'A respectful, inclusive,<br>and collaborative workplace.')}
{benefit_card('scales', 'forest', 'Work-Life<br>Balance', 'Flexible options where<br>possible to support<br>your well-being.')}
{benefit_card('pin', 'rust', 'Community<br>Impact', 'Meaningful work that<br>strengthens the health<br>of local communities.')}
{benefit_card('pine', 'gold', 'Culturally Grounded<br>Practice', 'A workplace that values<br>Indigenous knowledge,<br>culture, and ways of being.')}
</div>
</section>
<section id="jobs" style="{WRAP}; padding: 24px 56px 0 68px">
<div style="padding-left: 20px">{sec_head('Current Opportunities', 'Join Our Team', textlink('View All Opportunities', '#', 15, 'margin-bottom: 6px'), 31.6)}</div>
<div style="margin-top: 14px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(520px, 100%), 1fr)); gap: 26px">
{job_card('car-job-drum', 'Hand drum and drumstick', 'Nurse Practitioner – Kingston', 'Kingston, ON', 'Provide comprehensive, whole-person primary care within a culturally safe, community-focused environment.')}
{job_card('car-job-cedar', 'Cedar boughs', 'Registered Practical Nurse –<br>Deseronto Location', 'Deseronto, ON', 'Deliver high-quality, client-centred care as part of our interdisciplinary primary care team.')}
</div>
</section>
<section style="{WRAP}; padding: 26px 70px 0 82px; display: flex; flex-wrap: wrap; align-items: center; gap: 18px 60px">
<div style="flex: 0 0 322px; max-width: 100%; display: flex; flex-direction: column; gap: 6px">
{eyebrow('Our Hiring Process')}
{h2('A Clear &amp; Supportive<br>Application Experience', 29)}
</div>
{vdiv('96px')}
<div style="flex: 1 1 620px; min-width: 0; display: flex; flex-wrap: wrap; align-items: flex-start; gap: 16px 30px">
{hire_step('doc', 'forest', '1. Apply', 'Submit your application<br>online.')}
{hire_step('review', 'gold', '2. Review', 'Our team reviews<br>applications and<br>selects candidates.')}
{hire_step('people', 'forest', '3. Connect', 'Be invited for an<br>interview with our<br>hiring team.')}
{hire_step('handshake', 'rust', '4. Welcome', 'Successful candidates receive<br>an offer and onboarding<br>support to join the IIPCT team.', True)}
</div>
</section>
<section style="{WRAP}; padding: 22px 50px 0 62px">
<div style="position: relative; overflow: hidden; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 50px; padding: 0; border-radius: 14px; {CARD}">
{branch(104, '#B5BFA6', 0.55, 'right: 10px; top: 8px; transform: rotate(14deg)')}
<div style="flex: 0 0 456px; max-width: 100%; position: relative; min-height: 144px; align-self: stretch">{img('car-staff', 'Placeholder staff portrait', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 30%')}</div>
{vdiv('96px', GOLDL, 'align-self: center; height: 96px')}
<figure class="pads" style="position: relative; flex: 1 1 480px; min-width: 0; margin: 0; padding: 14px 130px 14px 0; display: flex; flex-direction: column; gap: 6px">
{eyebrow('Staff Spotlight')}
<div style="display: flex; align-items: flex-start; gap: 12px">
<span aria-hidden="true" style="font-family: {SERIF}; font-weight: 800; font-size: 50px; line-height: 0.82; color: #94391F">“</span>
<div style="display: flex; flex-direction: column; gap: 9px">
<blockquote style="margin: 0; font-family: {SERIF}; font-size: 19.4px; font-style: italic; font-weight: 500; line-height: 1.24; color: {INK}">“[Staff quote to come from IIPCT — a sentence or two, in a team member’s own words, about what working here means to them.]”</blockquote>
<figcaption style="font-size: 14.4px; font-weight: 500; color: {INK}">– [Staff member name, role], IIPCT</figcaption>
</div>
</div>
</figure>
</div>
</section>
<div id="updates" style="margin-top: 16px">'''
    right = (btn('View Current Opportunities', '#jobs', 'light', None, True, 'md', 'padding: 0 24px; gap: 13px; font-size: 13px; min-height: 38px')
             + btn('Get Hiring Updates', '#', 'light', 'bell', False, 'md', 'padding: 0 26px; gap: 11px; font-size: 13px; min-height: 38px'))
    s += rust_band('briefcase', 'Ready to Make a Difference?', 'Apply today to join the IIPCT team — or check back regularly for new opportunities.', right, 'padding-right: 112px; padding-left: 122px', 14).replace('font-weight: 500; font-size: 24.8px;', 'font-weight: 500; font-size: 25.8px;') + '</div>'
    s += footer()
    return 'IIPCT — Career Opportunities', s
