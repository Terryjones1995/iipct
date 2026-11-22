"""Home. Wording from the old site's home and services pages (content/old-site/pages/home.md, services.md, who-we-are.md);
the events section comes from p_events (IIPCT's own Facebook posts and flyers)."""
from lib import *
from p_events import site_hero, home_events, nl_band
from p_news import AWARD_ALT

def svc_card(icon, tone, title, text, href='Services.dc.html'):
    return f'''<div class="card" style="position: relative; display: flex; align-items: flex-start; gap: 13px; min-height: 124px; padding: 18px 8px 16px 16px; border-radius: 14px; background: #F7F0E3; border: 1px solid #DCCBAB; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05)">
{circ(icon, tone, 66)}
<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 2px; padding-right: 28px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 17.4px; line-height: 1.1; letter-spacing: -0.014em; color: {HEAD}; white-space: nowrap">{title}</h3>
<p style="margin: 0; font-size: 12.3px; line-height: 1.5; letter-spacing: -0.016em; color: {INK}">{text}</p>
</div>
{round_arrow(23, 'arrow', 'Learn about ' + title, href, 'position: absolute; right: 16px; bottom: 11px')}
</div>'''

def loc_card(name, kind):
    return f'''<div class="card" style="padding: 10px 8px 11px 16px; border-radius: 10px; background: #FCF7EC; border: 1px solid #CFC9A8; box-shadow: 0 1px 2px rgba(64, 44, 14, 0.07), 0 5px 12px rgba(64, 44, 14, 0.05); display: flex; flex-direction: column; gap: 2px">
<span style="display: flex; align-items: center; gap: 9px">{pin_fill(17)}<span style="font-size: 14.8px; font-weight: 700; color: {HEAD}; line-height: 1.15">{name}</span></span>
<span style="padding-left: 26px; font-size: 11.1px; color: {INK}; line-height: 1.3">{kind}</span>
<span style="padding-left: 26px; margin-top: 4px">{textlink('View Location', 'Contact.dc.html', 10.8, 'gap: 8px')}</span>
</div>'''

def green_band_photo(pic, eyebrow_txt, title, text_html, right_html, style='', photo_w='40.6%', min_h=186, title_size=27.5, text_pad='16px 26px 17px 54px'):
    """lib.green_band() with a real photograph (pic = lib.photo(...) markup) instead of a mock-up crop."""
    return f'''
<section style="{WRAP}; padding: 0 61px 0 63px; {style}">
<div style="position: relative; overflow: hidden; border-radius: 16px; min-height: {min_h}px; background: #153526; border: 1px solid #0C2218; color: #FFFFFF; display: flex; flex-wrap: wrap; align-items: stretch; box-shadow: 0 1px 2px rgba(20, 40, 25, 0.20)">
{branch(118, '#2C5A40', 0.9, 'right: 4px; bottom: -92px; transform: rotate(24deg)')}
<div class="gb-photo" style="flex: 0 0 {photo_w}; min-width: min(280px, 100%); position: relative; min-height: 150px">{pic}</div>
<div class="gb-txt" style="position: relative; flex: 1 1 360px; min-width: 0; padding: {text_pad}; display: flex; flex-direction: column; justify-content: center; gap: 8px">
{eyebrow(eyebrow_txt, '#E3BE74') if eyebrow_txt else ''}
{h2(title, title_size, '#FFFFFF', 'font-weight: 500')}
{text_html}
</div>
{right_html}
</div>
</section>'''

def page():
    buttons = btn('Schedule Your Visit', 'Contact.dc.html', 'primary', 'calendar-check') + btn('Book an Appointment', 'Contact.dc.html', 'outline', 'calendar-dot', False)
    s = header('home')
    # Hero: IIPCT team members at the BPSO gathering in Thunder Bay (old site, BPSO page photo); see site-img/SOURCES.md.
    s += site_hero('home/hero-team-thunder-bay.jpg', (1600, 840),
                   'Five IIPCT team members standing together outdoors beside a pond, two of them in ribbon skirts',
                   59.8, 366, 'Wholistic Care<br>Blending Medicine,<br>Culture, and Wellness',
                   'Inclusive healthcare with a focus on Indigenous<br>communities across southeastern Ontario.', buttons, obj='center 40%')
    # Service cards: old site services page (four key programs).
    s += f'''
<section style="position: relative; z-index: 2; {WRAP}; padding: 0 48px; margin-top: 16px">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: 16px">
{svc_card('bowl', 'sage', 'Cultural Services', 'Traditional healing, spiritual support,<br>and cultural learning.')}
{svc_card('stethoscope', 'rust', 'Primary Medical Care', 'Physicians, nurse practitioners,<br>and nurses, with partner supports.')}
{svc_card('lotus', 'sage', 'Mental Health Services', 'Short-term services for adults<br>aged 18 and older.')}
{svc_card('people', 'gold', 'Health Support Services', 'Care coordination and wellness<br>programs, plus help with forms.')}
</div>
</section>'''
    # "A Place for Good Medicine" and "Wholistic Care for All": old site home page; "status blind": who-we-are page.
    body = (p('Tsi Kanonhkhwatsheríyo offers inclusive healthcare with a focus on Indigenous communities. Our team provides accessible support across multiple disciplines, ensuring respectful and coordinated care for all who visit our clinic.', 14.8, INK, 1.4, 'max-width: 484px')
            + p('By combining clinical expertise with culturally sensitive approaches, we strive to improve health outcomes, build trust, and guide our community toward wellness and balance.', 14.8, INK, 1.4, 'max-width: 484px'))
    feats = feature_list([('feather', 'Wholistic Care for All', 'Care that respects culture, tradition,<br>and medical needs.'),
                          ('heart', 'Body, Mind and Spirit', 'A supportive environment for physical,<br>mental, and spiritual well-being.'),
                          ('people', 'Who We Serve', 'People who identify as Indigenous, and their<br>families. All our services are status blind.')])
    s += split_section(arc_photo('home-smudge', 'Smudge bowl with sage, sweetgrass braid and a woven blanket on a rock', 'flex: 1; min-height: 281px'),
                       'About IIPCT', 'A Place for<br>Good Medicine', body,
                       btn('Learn More About Us', 'WhoWeAre.dc.html', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 14px'), feats, 'margin-top: 18px')
    # Community Highlight: the old site's IPHCC awards post (2025-10-09) and its photo.
    right = (f'<div class="gb-cta" style="position: relative; flex: none; display: flex; align-items: center; gap: 34px; padding: 18px 28px 18px 0">'
             f'{vdiv("78px", "#B8935A", "align-self: center; height: 78px")}{btn("Read the Full Story", "NewsIPHCCAwards.dc.html", "gold", None, True, "md", "padding: 0 20px; gap: 12px")}</div>')
    pic = photo('news/iphcc-awards-2025.jpg', AWARD_ALT, 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 30%', '', 1280, 960)
    s += green_band_photo(pic, 'Community Highlight', 'Our Team Honoured at the<br>IPHCC Awards',
                          p('Out of 18 awards presented province-wide at the Indigenous Primary Health Care Council (IPHCC) Member Awards, our team brought home five: for community innovation, traditional healing and wellness, co-worker recognition, nursing, and physicians.', 13.5, '#F4F1E8', 1.47, 'max-width: 456px'),
                          right, 'margin-top: 10px', min_h=210)
    s += home_events()
    s += f'''
<section style="position: relative; overflow: hidden; margin-top: 30px; padding: 24px 0; background: #EBE7D2; border-top: 1px solid #D3CEAE; border-bottom: 1px solid #D3CEAE">
{pines(PINES_L, 200, 104, '#BCC6A9', 0.7, 'left: -4px; bottom: 0')}
{pines(PINES_R, 200, 92, '#BCC6A9', 0.7, 'right: -6px; bottom: 0')}
<div style="position: relative; {WRAP}; padding: 0 86px 0 145px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px 30px">
<div style="flex: 0 0 244px; display: flex; flex-direction: column; gap: 8px">
{h2('Our Locations', 25.6)}
{p('Caring for communities across southeastern Ontario.', 15.6, INK, 1.3, 'max-width: 240px')}
</div>
{vdiv('70px')}
<div style="flex: 1 1 560px; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px">
{loc_card('Tyendinaga', 'Clinic')}{loc_card('Deseronto', 'Clinic')}{loc_card('Kingston', 'Clinic')}{loc_card('Bancroft', 'Clinic')}{loc_card('Shannonville', 'Office (Allied Health Team)')}
</div>
</div>
</section>
<div style="margin-top: 34px">{nl_band()}</div>'''
    s += footer()
    return 'IIPCT — Home', s
