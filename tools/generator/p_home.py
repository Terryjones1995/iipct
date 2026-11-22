from lib import *

def svc_card(icon, tone, title, text, href='Services.dc.html'):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 13px; min-height: 124px; padding: 18px 8px 16px 16px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{circ(icon, tone, 66)}
<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 2px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 17.4px; line-height: 1.1; letter-spacing: -0.014em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; font-size: 12.3px; line-height: 1.5; letter-spacing: -0.016em; color: {INK}">{text}</p>
</div>
{round_arrow(23, 'arrow', 'Learn about ' + title, href, 'position: absolute; right: 16px; bottom: 11px')}
</div>'''

def event_card(photo, month, day, title, text, tag, tone, pos='center'):
    tagbg = {'sage': '#D2D6BC', 'tan': '#EAD3AE'}[tone]
    return f'''<article class="card" style="display: flex; min-height: 133px; border-radius: 14px; overflow: hidden; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div style="flex: 0 0 130px; position: relative">{img(photo, '', f'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {pos}')}</div>
<div style="flex: 0 0 58px; padding-top: 18px; display: flex; flex-direction: column; align-items: center; gap: 4px">
<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: {RUST}; line-height: 1">{month}</span>
<span style="font-size: 18.5px; font-weight: 700; color: {HEAD}; line-height: 1">{day}</span>
</div>
<div style="flex: 1; min-width: 0; padding: 17px 6px 13px 4px; display: flex; flex-direction: column; align-items: flex-start; gap: 6px">
<h3 style="margin: 0; font-size: 13px; font-weight: 700; line-height: 1.2; letter-spacing: -0.005em; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 11.4px; line-height: 1.5; letter-spacing: -0.008em; color: {INK}">{text}</p>
<span style="margin-top: 5px; margin-left: 8px; padding: 5px 11px 4px; border-radius: 5px; background: {tagbg}; font-size: 10.4px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #1B3122; line-height: 1.1">{tag}</span>
</div>
</article>'''

def loc_card(name):
    return f'''<div class="card" style="padding: 10px 8px 11px 16px; border-radius: 10px; background: #FCF7EC; border: 1px solid #CFC9A8; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05); display: flex; flex-direction: column; gap: 2px">
<span style="display: flex; align-items: center; gap: 9px">{pin_fill(17)}<span style="font-size: 14.8px; font-weight: 700; color: {HEAD}; line-height: 1.15">{name}</span></span>
<span style="padding-left: 26px; font-size: 11.1px; color: {INK}; line-height: 1.3">IIPCT Clinic</span>
<span style="padding-left: 26px; margin-top: 4px">{textlink('View Location', 'Contact.dc.html', 10.8, 'gap: 8px')}</span>
</div>'''

def page():
    buttons = btn('Schedule Your Visit', 'Contact.dc.html', 'primary', 'calendar-check') + btn('Book an Appointment', 'Contact.dc.html', 'outline', 'calendar-dot', False)
    s = header('home')
    s += hero('hero-home', 59.8, 366, 'Wholistic Care<br>Blending Medicine,<br>Culture, and Wellness',
              'Indigenous-centred primary care for individuals,<br>families, and communities across southeastern Ontario.', buttons)
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 48px; margin-top: 16px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 16px">
{svc_card('bowl', 'sage', 'Cultural Services', 'Land-based, traditional, and<br>cultural wellness supports.')}
{svc_card('stethoscope', 'rust', 'Primary Medical Care', 'Comprehensive, inclusive<br>primary care for all ages.')}
{svc_card('lotus', 'sage', 'Mental Health Services', 'Culturally safe, trauma-informed<br>mental health and addiction supports.')}
{svc_card('people', 'gold', 'Health Support Services', 'Integrated supports to help you<br>and your family stay well.')}
</div>
</section>'''
    body = p('IIPCT provides culturally grounded, wholistic primary care that honours Indigenous knowledge, values, and ways of being. We care for the whole person — mind, body, spirit, and emotional well-being — while working alongside individuals, families, and communities to support long-term health, wellness, and self-determination.', 14.8, INK, 1.26, 'max-width: 484px')
    feats = feature_list([('feather', 'Culturally Grounded Care', 'Healthcare that respects and uplifts<br>Indigenous knowledge, traditions, and identity.'),
                          ('people', 'Community Wellness', 'Programs, services, and partnerships that<br>strengthen individuals, families, and communities.'),
                          ('heart', 'A Wholistic Approach', 'Integrated physical, mental, emotional, and<br>spiritual care for all stages of life.')])
    s += split_section(arc_photo('home-smudge', 'Smudge bowl with sage, sweetgrass braid and a woven blanket on a rock', 'flex: 1; min-height: 281px'),
                       'Our Purpose', 'Whole-Person Care for<br>Healthy, Thriving Communities', body,
                       btn('Learn More About Us', 'WhoWeAre.dc.html', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 14px'), feats, 'margin-top: 18px')
    right = (f'<div class="gb-cta" style="position: relative; flex: none; display: flex; align-items: center; gap: 34px; padding: 18px 28px 18px 0">'
             f'{vdiv("78px", "#B8935A", "align-self: center; height: 78px")}{btn("Read the Full Story", "NewsIPHCCAwards.dc.html", "gold", None, True, "sm", "padding: 0 20px; gap: 12px")}</div>')
    s += green_band('home-lake', 'Community Highlight', 'Our Team Honoured at the<br>IPHCC Awards',
                    p('Five of the 18 awards at the 2025 Indigenous Primary Health Care Council Member Awards went to IIPCT staff, for work in community innovation, traditional healing, nursing and medicine.', 13.5, '#F4F1E8', 1.47, 'max-width: 456px'),
                    right, 'margin-top: 10px')
    s += f'''
<section style="{WRAP}; padding: 21px 72px 0 76px">
{sec_head('Events &amp; Programs', 'Upcoming Events', textlink('View All Events &amp; Programs', 'Events.dc.html', 14.4, 'margin-bottom: 8px'), 30.2)}
<div style="margin-top: 15px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(340px, 100%), 1fr)); gap: 22px">
{event_card('svc-primary', 'Fall', '2026', 'Cancer Screening Clinics', 'Screening clinics are running this fall. See the poster or call your clinic for dates.', 'Health Clinic', 'tan', '62% center')}
{event_card('home-ev-drum', 'Date', 'TBA', 'Social Songs &amp; Dances', 'Learn Haudenosaunee social songs, drumming and the teachings behind them.', 'Cultural Program', 'sage')}
{event_card('home-ev-herbs', 'Date', 'TBA', 'Full Moon Ceremony', 'For those who identify as women. Bring water, tobacco if you have it, and a dish for the potluck.', 'Ceremony', 'sage')}
</div>
<div style="margin-top: 14px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px 24px">
<p style="margin: 0; font-size: 13.2px; line-height: 1.4; color: {MUTED}">New dates are posted as they’re confirmed.</p>
{social_row(label='Also on')}
</div>
</section>
<section style="position: relative; overflow: hidden; margin-top: 30px; padding: 24px 0; background: #EBE7D2; border-top: 1px solid #D3CEAE; border-bottom: 1px solid #D3CEAE">
{pines(PINES_L, 200, 104, '#BCC6A9', 0.7, 'left: -4px; bottom: 0')}
{pines(PINES_R, 200, 92, '#BCC6A9', 0.7, 'right: -6px; bottom: 0')}
<div style="position: relative; {WRAP}; padding: 0 86px 0 145px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px 30px">
<div style="flex: 0 0 244px; display: flex; flex-direction: column; gap: 8px">
{h2('Our Clinic Locations', 25.6)}
{p('Caring for communities across southeastern Ontario.', 15.6, INK, 1.3, 'max-width: 240px')}
</div>
{vdiv('70px')}
<div style="flex: 1 1 560px; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px">
{loc_card('Tyendinaga')}{loc_card('Deseronto')}{loc_card('Kingston')}{loc_card('Bancroft')}{loc_card('Shannonville')}
</div>
</div>
</section>
<section style="position: relative">
<div style="{WRAP}; padding: 26px 152px 22px 129px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px 42px">
<div style="flex: 0 0 374px; max-width: 100%; display: flex; flex-direction: column; gap: 5px">
{eyebrow('Our Impact')}
{h2('In Our Community’s Words', 27.8)}
</div>
{vdiv('78px')}
<figure style="flex: 1 1 400px; min-width: 0; margin: 0; display: flex; align-items: flex-start; gap: 13px">
<span aria-hidden="true" style="font-family: {SERIF}; font-weight: 800; font-size: 58px; line-height: 0.8; color: #94391F">“</span>
<div style="display: flex; flex-direction: column; gap: 12px">
<blockquote style="margin: 0; max-width: 430px; font-size: 12.8px; font-style: italic; line-height: 1.6; color: {INK}">“[Community testimonial to come from IIPCT — two or three sentences in a client’s own words, shared with their consent.]”</blockquote>
<figcaption style="font-size: 12px; font-weight: 600; color: {INK}">— [Community Member]</figcaption>
</div>
</figure>
<div style="flex: none; display: flex; align-items: center; gap: 30px">
<span aria-hidden="true" style="display: flex; gap: 7px"><span style="width: 9px; height: 9px; border-radius: 50%; background: #A04A32"></span><span style="width: 9px; height: 9px; border-radius: 50%; border: 1px solid #A8998A"></span><span style="width: 9px; height: 9px; border-radius: 50%; border: 1px solid #A8998A"></span></span>
<span style="display: flex; gap: 14px">{round_arrow(36, 'arrow-left', 'Previous testimonial')}{round_arrow(36, 'arrow', 'Next testimonial')}</span>
</div>
</div>
</section>
<div style="margin-top: 4px">{newsletter()}</div>'''
    s += footer()
    return 'IIPCT — Home', s
