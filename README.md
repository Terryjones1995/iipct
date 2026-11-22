# IIPCT website rebuild

Static build of the new website for Tsi Kanonhkhwatsheríyo Indigenous Interprofessional Primary Care Team (iipct.org).

Built by [Pixel Elite Media](https://pixelelite.ca).

## Run it

Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

There is no build step and no JavaScript.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `who-we-are.html` | Who We Are |
| `careers.html` | Career Opportunities |
| `board-of-directors.html` | Board of Directors |
| `bpso.html` | Best Practice Spotlight Organization |
| `services.html` | Services |
| `primary-medical-care.html` | Primary Medical Care |
| `immunization.html` | Publicly Funded Immunization Program |
| `well-baby-well-child.html` | Well Baby and Well Child Appointments |
| `tb-testing.html` | TB Testing |
| `advanced-foot-care.html` | Advanced Foot Care Services |
| `diabetic-retinopathy-screening.html` | Diabetic Retinopathy Screening |
| `outreach-community-support.html` | Outreach and Community Support |
| `events-programs.html` | Events & Programs |
| `news.html` | News & Updates |
| `news-iphcc-awards.html` | News post: IPHCC Awards |
| `news-breast-cancer-screening.html` | News post: Breast Cancer Screening Event |
| `contact.html` | Contact Us |
| `schedule-your-visit.html` | Schedule Your Visit |
| `privacy-policy.html` | Privacy Policy (draft) |
| `accessibility.html` | Accessibility (draft) |
| `site-map.html` | Site Map |

## How it's put together

- One HTML file per page. Shared styles are in `assets/css/site.css`, images in `assets/img/`.
- Layout and colour are inline on the elements, because the pages were exported from the design canvas. `site.css` holds the base rules, hover states, the dropdown menus and the narrow-screen rules. Those rules use `!important` to override the inline styles.
- Breakpoints (max-width): 1399 small laptops (header keeps one booking button), 1199 the nav becomes a menu button, 1099 tablets (hero stacks, sections tighten), 900, 760 phones, 480 small phones.
- Desktop dropdowns are CSS only. The phone and tablet menu is a `<details>` element.
- Fonts come from Google Fonts: Newsreader (headings), DM Sans (text), Kaushan Script (footer words).

## Before this goes live

**Booking.** `schedule-your-visit.html` is a front-end mock of IIPCT's Ocean booking form. It does not submit anywhere. Health numbers must not be collected by this site. Send patients to the Ocean portal the current site uses:
`https://ocean.cognisantmd.com/intake/patients.html?linkRef=23964341-fa0d-46a7-b261-29ad22a145a6#/online-booking`

**Forms.** The contact form and the newsletter sign-up have no back end yet. The newsletter currently lives at `https://mailchi.mp/iipct/iipct-newsletter`.

**Legal pages.** Privacy Policy and Accessibility are drafts. Highlighted `[bracketed]` items need IIPCT's details, and the wording needs their sign-off.

**Events.** The three events on Home use real IIPCT program names. Two show "Date TBA" because no dated listing was available. `events-programs.html` still carries the sample events from the mockups.

**News.** The two stories are from posts on the current site. The notices list comes from the flyers on the current Events page, so "View flyer" links go nowhere yet. The "From Facebook" block is a placeholder.

**TB Testing.** The current page is two images with no text. The new page has placeholders until IIPCT supplies the text.

**People.** Staff, board and testimonial names are placeholders. The photos of people are stand-in images from the design mockups, not IIPCT staff or clients. Replace them before launch.

**Hours.** `contact.html` shows the same hours for every clinic. The current site lists different hours per clinic.

**Logo.** `assets/img/logo-emblem.png` is a cleaned-up copy of a 216 px file. Get the original vector from IIPCT.

**Placeholder links.** Links that have no destination yet use `href="#"`. Search for `href="#"` to find them.

## tools/generator

The Python scripts that generated these pages, kept so the pages can be regenerated. They are not needed to run the site. Paths inside them point at the folders they were built in (`/home/claude/iipct_work`, `/home/claude/iipct`), so recreate those or edit the constants at the top of `lib.py`, `build.py` and `export_site.py` before running them.
