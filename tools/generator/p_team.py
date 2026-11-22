"""Our Team: the people of IIPCT, by clinic. (Registered here as a starting page; the people and their photographs
come from the current iipct.org Who We Are page.)"""
from lib import *


def page():
    s = header('who')
    s += sub_hero([('Home', 'Main.dc.html'), ('Who We Are', 'WhoWeAre.dc.html'), ('Our Team', None)],
                  'Our Team',
                  'Our team is made up of highly trained and culturally safe professionals eager to provide care to the communities we serve.',
                  eyebrow_txt='Who We Are')
    s += f'''
<section style="{WRAP}; padding: 34px 48px 8px 83px">
{note('info', 'The team list is being moved over', 'Until it is here, the full team is on our current website.', 'sage')}
</section>'''
    s += footer()
    return 'IIPCT — Our Team', s
