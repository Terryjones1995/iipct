from lib import *

def cat_card(icon, tone, title, text):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 13px; min-height: 92px; padding: 12px 4px 10px 12px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{circ(icon, tone, 58, 31, 1.45)}
<div style="display: flex; flex-direction: column; gap: 5px; padding-top: 4px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 14.9px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; padding-right: 14px; font-size: 11.2px; line-height: 1.36; letter-spacing: -0.02em; color: {INK}">{text}</p>
</div>
{round_arrow(20, 'arrow', title, '#', 'position: absolute; right: 7px; bottom: 5px')}
</div>'''

def event_card(photo, month, day, tag, title, text):
    return f'''<article class="card" style="display: flex; flex-direction: column; padding: 6px 6px 13px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div style="position: relative">
{img(photo, '', 'width: 100%; aspect-ratio: 188 / 92; object-fit: cover; border-radius: 8px')}
<span style="position: absolute; left: 18px; top: 0; width: 50px; padding: 11px 0 8px; border-radius: 0 0 8px 8px; background: #FDF8EE; border: 1px solid #DCCBAB; border-top: none; display: flex; flex-direction: column; align-items: center; gap: 3px">
<span style="font-size: 11.4px; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase; color: {HEAD}; line-height: 1">{month}</span>
<span style="font-size: 18px; font-weight: 700; color: {HEAD}; line-height: 1">{day}</span>
</span>
<span style="position: absolute; left: 18px; bottom: -6px; padding: 6px 12px 5px; border-radius: 6px; background: #F0DDB5; border: 1px solid #D6BC86; font-size: 10.4px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; color: #2A2A1C; line-height: 1.1">{tag}</span>
</div>
<div style="flex: 1; padding: 20px 8px 0 15px; display: flex; flex-direction: column; align-items: flex-start; gap: 5px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 14.6px; line-height: 1.12; letter-spacing: -0.024em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0 0 9px; font-size: 12px; line-height: 1.34; letter-spacing: -0.014em; color: {INK}">{text}</p>
{btn('Register Now', 'Contact.dc.html', 'primary', None, True, 'xs', 'margin-top: auto; min-height: 31px; padding: 0 20px; gap: 12px; font-size: 12.4px')}
</div>
</article>'''

def program_card(icon, tone, title, text):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 14px; min-height: 118px; padding: 10px 6px 12px 14px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{circ(icon, tone, 60, 31, 1.45, 'margin-top: 12px')}
<div style="display: flex; flex-direction: column; gap: 8px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 16.8px; line-height: 1.08; letter-spacing: -0.02em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; padding-right: 22px; font-size: 11.4px; line-height: 1.38; letter-spacing: -0.014em; color: {INK}">{text}</p>
</div>
{round_arrow(20, 'arrow', 'About this program', '#', 'position: absolute; right: 7px; bottom: 7px')}
</div>'''

def calendar():
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    head = ''.join(f'<span style="font-size: 8.8px; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase; color: {INK}">{d}</span>' for d in days)
    cells = [''] * 4 + [str(i) for i in range(1, 32)]
    marked = {'10', '17', '24'}
    body = ''
    for c in cells:
        if c in marked:
            body += f'<span style="justify-self: center; min-width: 37px; padding: 2px 0; border-radius: 999px; background: #5F7F58; color: #FFFFFF; font-weight: 600">{c}</span>'
        else:
            body += f'<span>{c}</span>'
    return f'''<div style="flex: 0 0 398px; max-width: 100%; padding: 8px 20px 6px; border-radius: 14px; background: #FCF6EC; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
<div style="display: flex; align-items: center; justify-content: space-between; padding: 0 8px">
<button type="button" aria-label="Previous month" style="width: 26px; height: 26px; padding: 0; border: none; background: none; color: {HEAD}; cursor: pointer; display: flex; align-items: center; justify-content: center">{ico('chev-left', 18, HEAD, 2.2)}</button>
<span style="font-size: 13.6px; font-weight: 600; letter-spacing: 0.02em; color: {HEAD}">MAY 2025</span>
<button type="button" aria-label="Next month" style="width: 26px; height: 26px; padding: 0; border: none; background: none; color: {HEAD}; cursor: pointer; display: flex; align-items: center; justify-content: center">{ico('chev-right', 18, HEAD, 2.2)}</button>
</div>
<div style="margin-top: 3px; display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); text-align: center; row-gap: 5px">{head}</div>
<div style="margin-top: 7px; display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); text-align: center; row-gap: 2px; font-size: 12.6px; font-weight: 500; line-height: 19px; color: {INK}">{body}</div>
</div>'''

def month_row(date, title, last=False):
    bb = '' if last else 'border-bottom: 1px solid #E3D3B7; '
    return (f'<li style="{bb}display: flex; align-items: center; gap: 16px; padding: 3px 0 4px">'
            f'<span style="flex: none; width: 76px; padding: 5px 0 4px; border-radius: 999px; background: #F0DDB5; text-align: center; font-size: 12.6px; font-weight: 700; color: {HEAD}; line-height: 1.1">{date}</span>'
            f'<span style="font-size: 13.2px; font-weight: 500; color: {INK}">{title}</span></li>')

def page():
    buttons = (btn('View Upcoming Events', '#upcoming', 'primary', 'calendar-check', True, 'md', 'padding: 0 16px; gap: 9px; min-height: 39px; font-size: 12.8px')
               + btn('RSVP or Register', 'Contact.dc.html', 'outline', 'user', False, 'md', 'padding: 0 26px; gap: 10px; min-height: 39px'))
    s = header('events')
    s += hero('hero-events', 61.5, 290, 'Events &amp; Programs',
              'Wellness, learning, and community<br>connection rooted in culture, care, and<br>Indigenous ways of being.', buttons,
              h1_size=52, lead_size=21.3, lead_lh=1.33, lead_weight=450, pad='24px 0 34px 80px', gap=10, btn_mt=10, sq_mt=2, obj='center center')
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 40px; margin-top: 16px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr)); gap: 10px">
{cat_card('bowl', 'sage', 'Wellness Events', 'Activities, gatherings, and<br>holistic well-being programs.')}
{cat_card('stethoscope', 'rust', 'Learning Opportunities', 'Workshops, education, and<br>skill-building for all ages.')}
{cat_card('people', 'gold', 'Community Connection', 'Gather, share, and<br>strengthen our communities.')}
{cat_card('feather', 'rust', 'Cultural Programs', 'Language, land-based, and<br>cultural knowledge sharing.')}
{cat_card('heart', 'rust', 'Health Education', 'Practical topics to support your health and family well-being.')}
</div>
</section>'''
    meta = (f'<div style="display: flex; flex-direction: column; gap: 6px; font-size: 13.8px; font-weight: 500; color: #FFFFFF; margin-top: 2px">'
            f'<span style="display: flex; align-items: center; gap: 12px">{ico("calendar-check", 19, "#E3BE74", 1.7)}<span>Sat, May 24, 2025</span><span aria-hidden="true" style="width: 1px; height: 14px; background: #D8D2C0; margin: 0 8px"></span><span>9:00 AM – 4:00 PM</span></span>'
            f'<span style="display: flex; align-items: center; gap: 12px">{ico("pin", 19, "#E3BE74", 1.7)}<span>Tyendinaga Territory</span></span></div>'
            + p('A day of wellness on the land, including guided nature walks, traditional teachings, mindfulness practices, and a shared community meal.', 13.6, '#F4F1E8', 1.4, 'max-width: 486px; margin-top: 3px'))
    right = (f'<div class="gb-cta" style="position: relative; flex: none; display: flex; align-items: center; gap: 32px; padding: 18px 36px 18px 0">'
             f'{vdiv("100px", "#B8935A", "align-self: center; height: 100px")}{btn("Register Now", "Contact.dc.html", "gold", None, True, "sm", "padding: 0 30px; gap: 14px; font-size: 13px; min-height: 36px")}</div>')
    s += green_band('evt-featured', 'Featured Upcoming Event', 'Land-Based Wellness Retreat', meta, right, 'margin-top: 17px; padding: 0 39px 0 39px', '43.4%', 176, 30)
    s += f'''
<section id="upcoming" style="{WRAP}; padding: 21px 44px 0 56px">
{sec_head('Upcoming Events &amp; Programs', 'Join Us at an Upcoming Event', textlink('View All Events &amp; Programs', '#', 14.4, 'margin-bottom: 8px'), 28.6)}
</section>
<section style="{WRAP}; padding: 12px 38px 0 40px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 15px">
{event_card('evt-1', 'Apr', '17', 'Wellness', 'Drum Circle &amp; Wellness', 'A community space for connection,<br>healing, and cultural wellness.')}
{event_card('evt-2', 'May', '10', 'Cultural', 'Traditional Medicines Workshop', 'Learn about local medicinal plants,<br>preparation, and safe, respectful use.')}
{event_card('evt-3', 'May', '24', 'Land-Based', 'Land-Based Wellness Retreat', 'A full-day wellness retreat on the land with teachings, activities, and a shared meal.')}
{event_card('evt-4', 'Jun', '7', 'Skill-Building', 'Basket Weaving Workshop', 'A hands-on workshop to learn<br>traditional weaving techniques.')}
{event_card('evt-5', 'Jun', '21', 'Youth', 'Youth Wellness Day', 'A day of culture, wellness, and<br>connection for youth ages 12–24.')}
</div>
</section>
<section style="{WRAP}; padding: 22px 38px 0 40px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 38px; padding-left: 23px">
<div style="display: flex; flex-direction: column; gap: 5px">{eyebrow('Our Programs', RUST, 'font-size: 11.6px')}{h2('Explore Our Programs', 27.6)}</div>
{vdiv('40px')}
<p style="margin: 0; flex: 1 1 320px; font-size: 14.6px; font-style: italic; line-height: 1.4; color: {INK}">Ongoing and seasonal opportunities that support<br>wellness, learning, and community belonging.</p>
</div>
<div style="margin-top: 13px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); gap: 15px">
{program_card('people', 'sage', 'Community<br>Wellness Groups', 'Regular, supportive gatherings for mental, emotional, and spiritual well-being.')}
{program_card('feather', 'rust', 'Cultural<br>Workshops', 'Hands-on learning (e.g., language, traditional medicines, crafting, and more).')}
{program_card('people', 'gold', 'Youth<br>Programs', 'Culturally grounded activities, skill-building, and wellness support for youth (12–24).')}
{program_card('heart-pulse', 'rust', 'Health<br>Education', 'Practical workshops on topics like chronic disease prevention, nutrition, and family health.')}
{program_card('pine', 'sage', 'Seasonal<br>Gatherings', 'Community events that honour the seasons, land, and our shared traditions.')}
</div>
</section>
<section style="position: relative; margin-top: 12px; overflow: hidden">
<svg aria-hidden="true" viewBox="0 0 1440 60" preserveAspectRatio="none" style="position: absolute; left: 0; bottom: 0; width: 100%; height: 46px"><path d="M0 34 C 200 2 380 8 520 40 L 520 60 L 0 60 Z" fill="#E9EAD7" fill-opacity="0.75"></path><path d="M1060 60 C 1160 20 1300 12 1440 26 L 1440 60 Z" fill="#E9EAD7" fill-opacity="0.75"></path></svg>
{pines(PINES_L, 200, 150, '#C5CEB4', 0.6, 'left: -24px; bottom: 6px')}
{branch(132, '#B5BFA6', 0.5, 'right: -8px; top: -8px; transform: rotate(14deg)')}
<div style="position: relative; {WRAP}; padding: 12px 148px 12px 113px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px 46px">
<div style="flex: 0 0 262px; display: flex; flex-direction: column; gap: 7px; padding-bottom: 34px">
{eyebrow('At a Glance', RUST, 'font-size: 10.6px')}
{h2('This Month’s Events', 26.4)}
{p('Key events and programs happening this month at IIPCT.', 14.3, INK, 1.32, 'max-width: 250px')}
</div>
{calendar()}
{vdiv('140px')}
<div style="flex: 1 1 300px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 7px; padding-bottom: 4px">
{eyebrow('Coming Up This Month', RUST, 'font-size: 10.8px')}
<ul style="margin: 0; padding: 0; list-style: none; width: 100%; max-width: 372px; display: flex; flex-direction: column">
{month_row('MAY 10', 'Traditional Medicines Workshop')}{month_row('MAY 17', 'Drum Circle &amp; Wellness')}{month_row('MAY 24', 'Land-Based Wellness Retreat', True)}
</ul>
{textlink('View Full Calendar', '#', 13.6, 'margin-top: 1px')}
</div>
</div>
</section>
<section style="position: relative; {WRAP}; padding: 18px 120px 0 62px">
{branch(108, '#B5BFA6', 0.5, 'right: 34px; top: 40px; transform: rotate(-8deg)')}
<div style="position: relative; display: flex; flex-wrap: wrap; align-items: center; gap: 18px 44px">
<div style="flex: 0 0 386px; max-width: 100%; position: relative; min-height: 158px">{img('evt-smudge', 'Smudge bowl with smoke rising beside sweetgrass and a woven blanket', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 14px')}</div>
<div style="flex: 1 1 380px; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 7px">
{eyebrow('Community Story', RUST, 'font-size: 11.6px')}
{h2('Building Wellness Together', 28.2)}
{p('Our events and programs create space for people of all ages to learn, heal, and connect — strengthening wellness in our families and communities.', 15.2, INK, 1.24, 'max-width: 446px; margin-top: 2px')}
{btn('Read Our News', 'News.dc.html', 'primary', None, True, 'sm', 'margin-top: 8px; padding: 0 22px; gap: 14px; font-size: 13px; min-height: 34px')}
</div>
{vdiv('130px')}
<figure style="flex: 0 1 330px; min-width: 0; margin: 0; display: flex; align-items: flex-start; gap: 11px">
<span aria-hidden="true" style="font-family: {SERIF}; font-weight: 800; font-size: 50px; line-height: 0.8; color: #94391F">“</span>
<div style="display: flex; flex-direction: column; gap: 10px">
<blockquote style="margin: 0; font-family: {SERIF}; font-size: 16.6px; font-style: italic; font-weight: 500; line-height: 1.36; color: {INK}">“[Community member quote about what these gatherings mean — to come from IIPCT, shared with consent.]”</blockquote>
<figcaption style="font-size: 13.4px; color: {INK}">– [Community Member]</figcaption>
</div>
</figure>
</div>
</section>
<div style="margin-top: 21px">{newsletter('Get the latest events, programs, and wellness updates from our team.')}</div>
<section style="position: relative; z-index: 1; {WRAP}; padding: 20px 68px 0 387px; margin-bottom: -44px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 46px">
{h2('RSVP, Register, or<br>Ask a Question', 29, HEAD, 'line-height: 1.12')}
{vdiv('78px')}
<div style="flex: 1 1 400px; min-width: 0; display: flex; flex-direction: column; gap: 12px">
{p('We’re here to help you get involved. Contact us to RSVP for an event, register for a program, or learn more about what’s coming up.', 13.4, INK, 1.34, 'max-width: 520px')}
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 80px; font-size: 15px; font-weight: 700; color: {HEAD}">
<a href="tel:+13434780196" style="display: flex; align-items: center; gap: 16px; color: {HEAD}; text-decoration: none">{ico('phone', 22, HEAD, 1.6)}<span>(343) 478-0196</span></a>
<a href="mailto:info@iipct.com" style="display: flex; align-items: center; gap: 16px; color: {HEAD}; text-decoration: none">{ico('mail', 24, HEAD, 1.6)}<span>info@iipct.com</span></a>
</div>
</div>
{btn('Contact Us', 'Contact.dc.html', 'primary', None, True, 'md', 'align-self: flex-end; min-width: 154px; gap: 14px; margin-bottom: 4px')}
</section>'''
    s += footer(150, '', True)
    return 'IIPCT — Events &amp; Programs', s
