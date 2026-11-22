from lib import *

def person_card(photo, name, role, text, ratio='212 / 114', name_size=19.6, text_size=13.1):
    return f'''<article class="card" style="position: relative; display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; {CARD}">
{img(photo, 'Placeholder portrait', f'width: 100%; aspect-ratio: {ratio}; object-fit: cover; object-position: center 24%; border-bottom: 1px solid {LINE}')}
<div style="flex: 1; padding: 13px 12px 44px 23px; display: flex; flex-direction: column; align-items: flex-start; gap: 4px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: {name_size}px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}">{name}</h3>
<span style="font-size: 15px; font-style: italic; line-height: 1.2; color: {INK}; padding-bottom: 1px; border-bottom: 1.5px solid #C79A3D">{role}</span>
<p style="margin: 9px 0 0; font-size: {text_size}px; line-height: 1.4; letter-spacing: -0.012em; color: {INK}">{text}</p>
</div>
{round_arrow(26, 'arrow', 'Read bio', '#', 'position: absolute; right: 12px; bottom: 12px')}
</article>'''

def pillar(icon, tone, title, text, first=False):
    bl = '' if first else f'border-left: 1px solid {GOLD}; '
    return f'''<div style="{bl}flex: 1 1 320px; display: flex; align-items: center; gap: 20px; padding: 2px 8px 2px 38px">
{circ(icon, tone, 74, 38, 1.4)}
<div style="display: flex; flex-direction: column; gap: 4px">
<h3 style="margin: 0; font-family: {SERIF}; font-weight: 700; font-size: 20.4px; line-height: 1.1; letter-spacing: -0.02em; color: {HEAD}">{title}</h3>
<p style="margin: 0; font-size: 13.6px; line-height: 1.4; color: {INK}">{text}</p>
</div>
</div>'''

def page():
    buttons = (btn('Our Governance', '#governance', 'primary', 'people', True, 'md', 'padding: 0 22px; gap: 10px; font-size: 14.4px')
               + btn('Organizational Overview', 'WhoWeAre.dc.html', 'outline', 'doc', False, 'md', 'padding: 0 26px; gap: 11px; font-size: 14.4px'))
    s = header('board')
    s += hero('hero-board', 58.7, 322, 'Board of Directors',
              'Guiding good governance, community<br>leadership, and a strong, sustainable future<br>for primary care in our communities.', buttons,
              h1_size=50.6, lead_size=21, lead_lh=1.36, pad='40px 0 38px 86px', gap=11, btn_mt=10, sq_mt=2, obj='center center')
    body = p('The IIPCT Board of Directors provides strategic leadership, governance, and oversight to ensure high-quality, culturally safe, and community-informed primary care. The Board works in partnership with our team, patients, and communities to uphold our mission, values, and long-term sustainability.', 14.2, INK, 1.36, 'max-width: 520px; margin-top: 4px')
    feats = feature_list([('feather', 'Strategic Direction', 'Sets the organization’s strategic priorities<br>and long-term vision.'),
                          ('people', 'Oversight &amp; Accountability', 'Ensures responsible stewardship of resources,<br>quality and safety, and organizational performance.'),
                          ('heart', 'Community-Centred Leadership', 'Brings community perspectives and lived experience<br>to guide inclusive, culturally grounded care.')], 46, 15.8, 21, 13.2, 28)
    s += f'<div id="governance">' + split_section(arc_photo('brd-feather', 'Eagle feather resting on a woven blanket with cedar', 'flex: 1; min-height: 240px', '56% 60%'),
                       'Governance &amp; Oversight', 'Service, Stewardship, and<br>Community Accountability', body,
                       btn('Our Governance Framework', '#', 'primary', None, True, 'sm', 'padding: 0 24px; gap: 14px; font-size: 13.6px; min-height: 38px'), feats, 'margin-top: 24px', 31.6, '27.3%') + '</div>'
    s += f'''
<section style="{WRAP}; padding: 26px 62px 0 60px">
<div style="padding-left: 22px">{sec_head('Our Leadership', 'Meet Our Board of Directors', textlink('Board Governance &amp; Policies', '#', 14.6, 'margin-bottom: 10px'), 38)}</div>
<div style="margin-top: 22px; display: flex; flex-wrap: wrap; align-items: stretch; gap: 22px">
<article style="flex: 2.36 1 600px; min-width: 0; display: flex; flex-wrap: wrap; overflow: hidden; border-radius: 14px; background: #153526; border: 1px solid #0C2218; box-shadow: {SHADOW}">
<div style="flex: 0.92 1 280px; position: relative; min-height: 318px">{img('brd-chair', 'Placeholder portrait', 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 20%')}</div>
<div style="position: relative; flex: 1 1 300px; min-width: 0; padding: 20px 22px 20px 30px; display: flex; flex-direction: column; align-items: flex-start; gap: 5px; color: #FFFFFF">
{branch(96, '#2C5A40', 0.9, 'right: -10px; bottom: -70px; transform: rotate(24deg)')}
{eyebrow('Board Chair Spotlight', '#E3BE74')}
<h3 style="margin: 10px 0 0; font-family: {SERIF}; font-weight: 600; font-size: 30px; line-height: 1.08; letter-spacing: -0.016em; color: #FFFFFF">[Board Chair name]</h3>
<span style="font-size: 15.2px; color: #FFFFFF">Chair, Board of Directors</span>
<span aria-hidden="true" style="width: 60px; height: 2px; background: #C8A15A; margin: 10px 0 8px"></span>
<p style="position: relative; margin: 0; max-width: 330px; font-size: 13.7px; line-height: 1.42; color: #F4F1E8">[Chair bio to come from IIPCT — two or three sentences on their background in community health and governance, and what guides their leadership of the Board.]</p>
{btn('Read the Chair’s Full Bio', '#', 'gold', None, True, 'sm', 'position: relative; margin-top: 12px; padding: 0 22px; gap: 14px; font-size: 13.6px; min-height: 38px')}
</div>
</article>
<div style="flex: 1 1 240px; min-width: 0; display: flex">{person_card('brd-officer-1', '[Treasurer name]', 'Treasurer', 'Brings financial stewardship, strategic planning, and a strong commitment to community well-being.', '212 / 115', 21, 13.5)}</div>
<div style="flex: 1 1 240px; min-width: 0; display: flex">{person_card('brd-officer-2', '[Secretary name]', 'Secretary', 'Supports effective governance, board operations, and clear communication across the organization.', '212 / 115', 21, 13.5)}</div>
</div>
<div style="margin-top: 22px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(230px, 100%), 1fr)); gap: 22px">
{person_card('brd-dir-1', '[Director name]', 'Director', 'Community health advocate with a focus on equitable access to primary care.', '180 / 90')}
{person_card('brd-dir-2', '[Director name]', 'Director', 'Brings experience in Indigenous wellness, program development, and community engagement.', '180 / 90')}
{person_card('brd-dir-3', '[Director name]', 'Director', 'Offers a depth of leadership in community services, health systems, and organizational growth.', '180 / 90')}
{person_card('brd-dir-4', '[Director name]', 'Director', 'Committed to culturally safe care, health equity, and the voices of patients and families.', '180 / 90')}
{person_card('brd-dir-5', '[Director name]', 'Director', 'Contributes expertise in strategy, partnerships, and sustainable community health initiatives.', '180 / 90')}
</div>
</section>
<section style="position: relative; overflow: hidden; margin-top: 28px; padding: 24px 0 26px; background: #EBE7D2; border-top: 1px solid #D3CEAE; border-bottom: 1px solid #D3CEAE">
{pines(PINES_L, 200, 104, '#BCC6A9', 0.7, 'left: -4px; bottom: 0')}
{pines(PINES_R, 200, 92, '#BCC6A9', 0.7, 'right: -6px; bottom: 0')}
<div style="position: relative; {WRAP}; padding: 0 150px 0 161px; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 56px">
<div style="display: flex; flex-direction: column; gap: 5px">
{eyebrow('Our Commitment')}
{h2('Accountability, Community Voice,<br>and Organizational Stewardship', 29)}
</div>
{vdiv('76px', GOLD)}
{p('The Board of Directors is committed to accountable leadership, meaningful community engagement, and the long-term stewardship of IIPCT’s people, programs, and resources — so that individuals, families, and communities continue to have access to high-quality, culturally grounded primary care.', 14.3, INK, 1.42, 'flex: 1 1 420px; max-width: 548px')}
</div>
</section>
<section style="{WRAP}; padding: 26px 56px 4px 50px; display: flex; flex-wrap: wrap; align-items: stretch; gap: 18px 0">
{pillar('scales', 'sage', 'Accountability', 'Responsible governance, transparency,<br>and a focus on quality and safety.', True)}
{pillar('people', 'rust', 'Community Voice', 'Lived experience and community perspectives<br>inform our decisions and priorities.')}
{pillar('lotus', 'gold', 'Organizational Stewardship', 'Sustainable, values-driven leadership<br>for today and future generations.')}
</section>
<div style="margin-top: 22px">{newsletter()}</div>'''
    s += footer()
    return 'IIPCT — Board of Directors', s
