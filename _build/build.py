#!/usr/bin/env python3
"""
GLS Refrigeration & Air Conditioning - site generator.
Designed and developed by COR3 Haus Production.

Writes every HTML page, sitemap.xml, robots.txt, llms.txt, humans.txt and
site.webmanifest into the project root. Contact details, domain and copy live
here once, so pages cannot drift out of sync.

Run:  python3 _build/build.py
"""
import os, re, json, glob, datetime
from urllib.parse import quote
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMGDIR = os.path.join(ROOT, 'assets', 'img')
TODAY = datetime.date.today()

# ------------------------------------------------------------------ business facts
DOMAIN = 'https://glsrefrigeration.co.za'          # canonical host; www also resolves
NAME = 'GLS Refrigeration and Air Conditioning'
LEGAL = 'GLS Refrigeration And Air Conditioning (PTY) LTD'
FOUNDED = '2011'
CALL = '+27736541480'
CALL_DISPLAY = '073\u00a0654\u00a01480'
WA = '27619342182'
WA_DISPLAY = '061\u00a0934\u00a02182'
EMAIL = 'glsrefcon@gmail.com'
STREET = '2 Churchill Avenue, Primrose'
LOCALITY = 'Germiston'
ADDRESS_LINE = '2 Churchill Avenue, Primrose, Germiston'
MAP_QUERY = quote('2 Churchill Avenue, Primrose, Germiston, South Africa')
MAP_GOOGLE = 'https://www.google.com/maps/search/?api=1&query=' + MAP_QUERY
MAP_APPLE = 'https://maps.apple.com/?q=' + MAP_QUERY
MAP_WAZE = 'https://waze.com/ul?q=' + MAP_QUERY + '&navigate=yes'
OG_IMAGE = DOMAIN + '/assets/img/og-gls-refrigeration-air-conditioning.jpg'

COR3 = {
    'name': 'COR3 Haus Production', 'url': 'https://cor3hausproduction.com/',
    'instagram': 'https://www.instagram.com/cor3hausproduction/',
    'linkedin': 'https://www.linkedin.com/company/cor3hausproduction/',
    'founder': 'Jeremie Kazadi', 'founder_linkedin': 'https://www.linkedin.com/in/jeremie-k-013a55372/',
}

NAV = [('./', 'Home', 'home'), ('services.html', 'Services', 'services'),
       ('our-work.html', 'Our work', 'work'), ('about.html', 'About', 'about'),
       ('contact.html', 'Contact', 'contact')]

# ------------------------------------------------------------------ images
ALT = {
 'condensing-unit-copper-receiver': 'Insulated copper pipework and a liquid receiver on a refrigeration condensing unit, with condenser fans behind',
 'brazing-compressor-connection': 'A hand holding a brazing rod to a compressor connection on a refrigeration unit',
 'compressor-rack-control-boxes': 'Compressors and electrical control boxes mounted on a metal rack',
 'evaporator-coils-in-frame': 'Finned evaporator coils held in a timber and steel frame',
 'rooftop-split-units-corrugated-roof': 'Several split-system outdoor units mounted along a corrugated roof, with a house roof beyond',
 'ceiling-mounted-indoor-unit-pipework': 'An indoor air-conditioning unit with blue-insulated pipework fitted at ceiling level',
 'condenser-fan-assembly-guard': 'Axial condenser fan with a protective guard on a steel base plate',
 'round-cassette-unit-fan-grille': 'Underside of a round-flow cassette air-conditioning unit with its perforated grille',
 'condensing-unit-on-stand-r410a': 'A condensing unit on a stand in a workshop, with an R410A refrigerant cylinder on the floor',
 'hermetic-compressor-wall-mounted': 'Hermetic compressor with copper pipework and a thermostat on a wall-mounted refrigeration unit',
 'condensing-unit-rooftop-platform': 'A white condensing unit on a rooftop platform with blue-insulated pipes',
 'refrigeration-control-enclosure': 'Electrical enclosure with breakers and a digital controller beside a compressor',
 'contactor-bank-digital-controller': 'Rows of contactors and wiring beside a digital temperature controller with a red display',
 'outdoor-unit-panel-removed-control-boards': 'A large outdoor air-conditioning unit with its panel removed, exposing control boards and wiring',
 'technician-rooftop-compressor': 'A technician on a rooftop holding a compressor, with condensing units behind him',
 'manifold-gauges-refrigerant-cylinder-ladder': 'Manifold gauges and a refrigerant cylinder at the foot of a ladder beside an outdoor split unit',
 'wall-mounted-split-outdoor-units': 'Two split-system outdoor units bracketed to an exterior wall',
 'outdoor-electrical-enclosure': 'Outdoor electrical enclosure on a wall, with razor wire along the top of the wall behind',
 'timer-and-contactor-box': 'An open electrical box with a time switch and contactors',
 'outdoor-units-bracketed-brick-wall': 'Two outdoor air-conditioning units on wall brackets against a face-brick wall',
 'split-unit-components-staged-copper-coil': 'Split-unit indoor and outdoor components with a refrigerant cylinder and a coil of copper pipe',
 'outdoor-unit-ground-mounted': 'An outdoor air-conditioning unit standing on brick paving',
 'rooftop-condensing-units-weathered': 'Several older, weathered condensing units on a flat roof',
}

def _widths(base):
    ws = []
    for p in glob.glob(os.path.join(IMGDIR, base + '-*.webp')):
        m = re.search(r'-(\d+)\.webp$', p)
        if m and os.path.basename(p)[:-len(m.group(0))] == base:
            ws.append(int(m.group(1)))
    return sorted(ws)

def img(base, sizes, alt=None, loading='lazy', cls='', fetch=None, pos=None):
    """Responsive <img>. IMAGE PLACEMENT is decided by the caller; alt text comes from ALT."""
    ws = _widths(base)
    if not ws:
        raise SystemExit('missing image: ' + base)
    big = ws[-1]
    with Image.open(os.path.join(IMGDIR, f'{base}-{big}.webp')) as im:
        w, h = im.size
    mid = [x for x in ws if x >= 800] or ws
    src = f'assets/img/{base}-{mid[0]}.webp'
    srcset = ', '.join(f'assets/img/{base}-{x}.webp {x}w' for x in ws)
    a = ALT.get(base, '') if alt is None else alt
    attrs = f'src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(a)}" decoding="async" loading="{loading}"'
    if fetch: attrs += f' fetchpriority="{fetch}"'
    if cls: attrs += f' class="{cls}"'
    if pos: attrs += f' style="object-position:{pos}"'
    return f'<img {attrs}>'

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def pic(base, sizes, ratio='r-32', caption=None, loading='lazy', fetch=None, pos=None, cls='', reveal=True):
    """Borderless figure: image in a clipped frame, optional small caption below."""
    classes = ' '.join(c for c in ('ph', ratio, cls) if c)
    rv = ' data-reveal-img' if reveal and loading == 'lazy' else ''
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'<figure class="{classes}"{rv}><div class="ph__frame">{img(base, sizes, loading=loading, fetch=fetch, pos=pos)}</div>{cap}</figure>'

def tile(base, caption, span, wide=False, sizes='(min-width: 52em) 30vw, 50vw', pos=None):
    """Gallery tile: a button that opens the lightbox. span = desktop column span (of 12)."""
    ws = _widths(base)
    full = f'assets/img/{base}-{max(x for x in ws if x <= 1200)}.webp'
    cls = f'tile s{span}' + (' is-wide' if (wide or span >= 7) else '')
    a = esc(ALT.get(base, ''))
    return (f'<button type="button" class="{cls}" data-lightbox data-full="{full}" data-alt="{a}" data-caption="{esc(caption)}" '
            f'aria-label="View larger: {esc(caption)}" data-reveal-img>{img(base, sizes, pos=pos)}<span class="tile__cap">{caption}</span></button>')

def icon(name):
    return f'<svg class="ico" aria-hidden="true" focusable="false"><use href="assets/img/sprite.svg#i-{name}"></use></svg>'

# ------------------------------------------------------------------ FAQ content (rendered AND emitted as FAQPage JSON-LD)
FAQ = {
 'services': [
  ('Does GLS work on homes and businesses?', 'Yes. GLS installs, repairs and maintains refrigeration and air-conditioning systems for homes, offices, restaurants, supermarkets and other commercial properties.'),
  ('Does GLS give a quote before starting work?', 'Yes. Quotes are upfront and clear, with no hidden fees, so you know what you are paying for before work begins.'),
  ('Is emergency repair available after hours?', f'Yes. Emergency repair is available 24 hours a day, 7 days a week. Call\u00a0{CALL_DISPLAY} or message {WA_DISPLAY} on WhatsApp.'),
 ],
 'ac': [
  ('Which air-conditioning systems does GLS install?', 'GLS installs split-unit and ducted air-conditioning systems for homes and commercial properties, including offices and server rooms.'),
  ('Does GLS repair air conditioners outside normal hours?', f'Yes. Emergency repair is available 24 hours a day, 7 days a week. Call\u00a0{CALL_DISPLAY} or message {WA_DISPLAY} on WhatsApp.'),
  ('Can GLS replace an old system with a more efficient one?', 'Yes. System upgrades cover energy-efficient and inverter units, eco-friendly refrigerants and smart climate control. A free site assessment is the starting point.'),
  ('Which areas does GLS serve?', 'Johannesburg and surrounding areas, from our base in Primrose, Germiston.'),
 ],
 'refrig': [
  ('Can GLS install a cold room or walk-in freezer?', 'Yes. GLS installs walk-in freezers and cold rooms as well as commercial refrigeration units, and services them afterwards.'),
  ('Who does GLS install commercial refrigeration for?', 'Restaurants, supermarkets and other retail businesses, along with offices that need climate control.'),
  ('What should I do if a fridge or freezer stops keeping cold?', 'Note the make and model, when it stopped and any code on the controller, then call or WhatsApp GLS. If you smell burning or see sparks, switch the unit off at the isolator and keep clear.'),
  ('Does GLS offer a free assessment for a new installation?', 'Yes. Free site assessments are available, covering system design, energy efficiency and options that suit your budget.'),
 ],
 'maint': [
  ('What does a maintenance service cover?', 'Inspection of filters, refrigerant levels and electrical wiring, cleaning of critical components, and performance optimisation.'),
  ('Does maintenance prevent breakdowns?', 'Regular servicing finds worn or dirty components before they fail, which reduces breakdowns and extends the life of the system. It cannot rule out every fault.'),
  ('How often should a system be serviced?', 'That depends on the system, how hard it runs and where it is installed. GLS can recommend a schedule once the equipment has been assessed.'),
  ('Does GLS maintain both refrigeration and air conditioning?', 'Yes, for homes and businesses.'),
 ],
}

def faq_html(key):
    items = ''.join(f'<div class="faq__item"><h3>{q}</h3><p>{a}</p></div>' for q, a in FAQ[key])
    return f'<div class="faq">{items}</div>'

# ------------------------------------------------------------------ structured data
def business_node():
    return {
        '@type': 'HVACBusiness', '@id': DOMAIN + '/#business',
        'name': NAME, 'legalName': LEGAL, 'url': DOMAIN + '/',
        'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/assets/img/gls-logo-480.png', 'width': 480, 'height': 364},
        'image': OG_IMAGE,
        'description': 'GLS installs, repairs and maintains refrigeration and air-conditioning systems for homes and businesses in Johannesburg and surrounding areas. Registered company, operating since 2011, with 24/7 emergency repair.',
        'foundingDate': FOUNDED, 'telephone': CALL, 'email': EMAIL,
        'contactPoint': [
            {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': CALL, 'email': EMAIL, 'areaServed': 'ZA', 'availableLanguage': 'English'},
            {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+' + WA, 'description': 'WhatsApp', 'areaServed': 'ZA', 'availableLanguage': 'English'},
        ],
        'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': LOCALITY, 'addressRegion': 'Gauteng', 'addressCountry': 'ZA'},
        'areaServed': [{'@type': 'City', 'name': 'Johannesburg'}, {'@type': 'City', 'name': 'Germiston'}],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Refrigeration and air-conditioning services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in (
                'Air-conditioning installation', 'Air-conditioning repair and maintenance',
                'Commercial refrigeration and cold rooms', 'Planned maintenance',
                '24/7 emergency repair', 'System upgrades', 'Free site assessment')]},
    }

def website_node():
    return {
        '@type': 'WebSite', '@id': DOMAIN + '/#website', 'url': DOMAIN + '/', 'name': NAME,
        'inLanguage': 'en-ZA', 'publisher': {'@id': DOMAIN + '/#business'},
        'creator': {
            '@type': 'Organization', '@id': COR3['url'] + '#organization', 'name': COR3['name'], 'url': COR3['url'],
            'sameAs': [COR3['instagram'], COR3['linkedin']],
            'founder': {'@type': 'Person', '@id': COR3['url'] + '#founder', 'name': COR3['founder'],
                        'jobTitle': 'Founder', 'worksFor': {'@id': COR3['url'] + '#organization'},
                        'sameAs': [COR3['founder_linkedin']]},
        },
    }

def page_url(p):
    return DOMAIN + '/' if p['file'] == 'index.html' else f"{DOMAIN}/{p['file']}"

def graph(p):
    url = page_url(p)
    g = [business_node(), website_node()]
    wp = {'@type': p.get('schema_type', 'WebPage'), '@id': url + '#webpage', 'url': url, 'name': p['title'],
          'description': p['desc'], 'inLanguage': 'en-ZA', 'isPartOf': {'@id': DOMAIN + '/#website'},
          'about': {'@id': DOMAIN + '/#business'}, 'primaryImageOfPage': {'@type': 'ImageObject', 'url': OG_IMAGE}}
    if p.get('crumbs'): wp['breadcrumb'] = {'@id': url + '#breadcrumb'}
    g.append(wp)
    if p.get('crumbs'):
        g.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': (DOMAIN + '/' + h if h else url)}
            for i, (n, h) in enumerate(p['crumbs'])]})
    if p.get('service'):
        s = p['service']
        g.append({'@type': 'Service', '@id': url + '#service', 'name': s['name'], 'serviceType': s['type'],
                  'description': s['desc'], 'url': url, 'provider': {'@id': DOMAIN + '/#business'},
                  'areaServed': [{'@type': 'City', 'name': 'Johannesburg'}, {'@type': 'City', 'name': 'Germiston'}]})
    if p.get('faq'):
        g.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ[p['faq']]]})
    return {'@context': 'https://schema.org', '@graph': g}

# ------------------------------------------------------------------ shared components
def head(p):
    url = page_url(p)
    robots = 'noindex, follow' if p.get('noindex') else 'index, follow, max-image-preview:large'
    ld = json.dumps(graph(p), ensure_ascii=False, indent=2)
    canonical = '' if p.get('noindex') else f'<link rel="canonical" href="{url}">\n'
    return f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
{canonical}<meta name="robots" content="{robots}">
<meta name="theme-color" content="#15252f">
<meta name="author" content="COR3 Haus Production">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_ZA">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="GLS logo beside copper pipework and a receiver on a refrigeration condensing unit">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p['title'])}">
<meta name="twitter:description" content="{esc(p['desc'])}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="assets/fonts/instrument-sans-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/main.css">
<script>(function(){{var d=document.documentElement;d.classList.add('js');if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){{d.classList.add('anim');setTimeout(function(){{if(!window.__glsMotion)d.classList.remove('anim')}},4000)}}}})();</script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body data-wa="{WA}" data-tel="{CALL}" data-tel-display="{CALL_DISPLAY}" data-email="{EMAIL}">
'''

def header(active):
    links = ''
    for href, label, key in NAV:
        cur = ''
        if key == active: cur = ' aria-current="page"'
        elif key == 'services' and active in ('ac', 'refrig', 'maint'): cur = ' aria-current="true"'
        links += f'<li><a class="nav__link" href="{href}"{cur}>{label}</a></li>'
    return f'''<a class="skip" href="#main" data-inert-when-nav-open>Skip to content</a>
<header class="site-header">
  <div class="site-header__bar">
    <!-- LOGO PLACEMENT: sits directly on the dark bar (the logo is designed for black). Source: assets/img/gls-logo-120.webp / -240.webp -->
    <a class="brand" href="./" aria-label="{NAME}, home page" data-inert-when-nav-open>
      <img src="assets/img/gls-logo-120.webp" srcset="assets/img/gls-logo-120.webp 120w, assets/img/gls-logo-240.webp 240w" sizes="42px" width="42" height="32" alt="" fetchpriority="high" decoding="async">
    </a>
    <nav class="nav" id="site-nav" aria-label="Main" data-open="false">
      <ul class="nav__list">{links}</ul>
      <div class="nav__contact">
        <a class="btn btn--call" href="tel:{CALL}">{icon('phone')}Call\u00a0{CALL_DISPLAY}</a>
        <a class="btn" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}WhatsApp\u00a0{WA_DISPLAY}</a>
        <p><a class="nav__mail" href="mailto:{EMAIL}">{EMAIL}</a><br>Emergency repair 24/7</p>
      </div>
    </nav>
    <div class="header-actions" data-inert-when-nav-open>
      <a class="btn btn--ghost btn--wa" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}WhatsApp</a>
      <a class="btn btn--call" href="tel:{CALL}">{icon('phone')}Call<span class="hide-mobile">&nbsp;{CALL_DISPLAY}</span></a>
    </div>
    <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span class="nav-toggle__bars" aria-hidden="true"></span></button>
  </div>
  <div class="nav-scrim" id="nav-scrim" data-open="false"></div>
</header>
'''

def band(title='Need someone on site?', text=None):
    text = text or 'Call for urgent faults. Emergency repair is available 24 hours a day, 7 days a week.'
    return f'''<section class="section section--frost closing" aria-labelledby="band-title">
  <div class="wrap closing__grid">
    <div data-reveal>
      <p class="label">Contact</p>
      <h2 class="h2" id="band-title">{title}</h2>
      <p class="lead">{text}</p>
    </div>
    <div class="contact-index" data-reveal>
      <div><small>Call, emergency repair 24/7</small><a href="tel:{CALL}"><strong>{CALL_DISPLAY}</strong></a></div>
      <div><small>WhatsApp</small><a href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer"><strong>{WA_DISPLAY}</strong></a></div>
      <div><small>Send an enquiry</small><a href="contact.html"><strong>Online form</strong></a></div>
      <div><small>Based in</small><strong>Primrose, Germiston</strong></div>
    </div>
  </div>
</section>
'''

def footer():
    y = TODAY.year
    return f'''<footer class="site-footer" data-inert-when-nav-open>
  <div class="wrap footer__grid">
    <div class="footer__brand">
      <!-- LOGO PLACEMENT: footer -->
      <img src="assets/img/gls-logo-240.webp" srcset="assets/img/gls-logo-240.webp 240w, assets/img/gls-logo-480.webp 480w" sizes="73px" width="73" height="55" alt="{NAME}" loading="lazy">
      <p>Refrigeration and air-conditioning installation, repair and maintenance. Operating since {FOUNDED}.</p>
    </div>
    <div class="footer__col">
      <h2>Contact</h2>
      <ul>
        <li><a href="tel:{CALL}">Call\u00a0{CALL_DISPLAY}</a></li>
        <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">WhatsApp\u00a0{WA_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><address>{ADDRESS_LINE}<br><a href="{MAP_GOOGLE}" data-map-open target="_blank" rel="noopener noreferrer">Get directions</a></address></li>
      </ul>
    </div>
    <div class="footer__col">
      <h2>Services</h2>
      <ul>
        <li><a href="air-conditioning.html">Air conditioning</a></li>
        <li><a href="commercial-refrigeration.html">Commercial refrigeration</a></li>
        <li><a href="maintenance.html">Planned maintenance</a></li>
        <li><a href="services.html">All services</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <h2>Company</h2>
      <ul>
        <li><a href="about.html">About GLS</a></li>
        <li><a href="our-work.html">Our work</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap">
    <div class="footer__legal">
      <p>&copy; {FOUNDED}&ndash;{y} {LEGAL}. All rights reserved.</p>
      <!-- ATTRIBUTION (required wording): Website designed and developed by COR3 Haus Production -->
      <p>Website designed and developed by <a href="{COR3['url']}" target="_blank" rel="noopener noreferrer">COR3 Haus Production</a></p>
    </div>
  </div>
</footer>
'''

def map_dialog():
    return f'''<!-- MAP CHOOSER: opens from any [data-map-open] link. Without JavaScript those links open Google Maps directly. -->
<dialog class="mapdlg" id="map-dialog" aria-labelledby="map-dialog-title">
  <div class="mapdlg__head">
    <h2 id="map-dialog-title">Open in maps</h2>
    <button class="mapdlg__close" type="button" data-map-close aria-label="Close">&times;</button>
  </div>
  <div class="mapdlg__body">
    <p>{ADDRESS_LINE}. Pick the app you use.</p>
    <a class="btn mapdlg__opt" href="{MAP_GOOGLE}" target="_blank" rel="noopener noreferrer">{icon('pin')}Google Maps</a>
    <a class="btn mapdlg__opt" href="{MAP_APPLE}" target="_blank" rel="noopener noreferrer">{icon('pin')}Apple Maps</a>
    <a class="btn mapdlg__opt" href="{MAP_WAZE}" target="_blank" rel="noopener noreferrer">{icon('pin')}Waze</a>
  </div>
</dialog>
'''

def crumbs(p):
    items = []
    for i, (n, h) in enumerate(p['crumbs']):
        if i == len(p['crumbs']) - 1: items.append(f'<li><span aria-current="page">{n}</span></li>')
        else: items.append(f'<li><a href="{h or "./"}">{n}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'

def row(title, text, items=None, links=None, rid=None):
    """Hairline service row (inner pages)."""
    idattr = f' id="{rid}"' if rid else ''
    tags = ''.join(f'<li>{i}</li>' for i in items) if items else ''
    tags_html = f'<ul class="tags">{tags}</ul>' if tags else ''
    lk = ''
    if links:
        lk = '<div>' + '<br>'.join(f'<a class="link" href="{h_}">{t}</a>' for t, h_ in links) + '</div>'
    return f'<div class="rows__item"{idattr} data-reveal><h3>{title}</h3><div><p>{text}</p>{tags_html}</div>{lk}</div>'

LIGHTBOX = '''<dialog class="lightbox" id="lightbox" aria-label="Photograph viewer">
  <img class="lightbox__img" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="1200" height="800" alt="">
  <div class="lightbox__bar">
    <p class="lightbox__cap" aria-live="polite"></p>
    <div class="lightbox__btns">
      <button type="button" data-lb-prev aria-label="Previous photograph">Prev</button>
      <button type="button" data-lb-next aria-label="Next photograph">Next</button>
      <button type="button" data-lb-close aria-label="Close viewer">Close</button>
    </div>
  </div>
</dialog>
'''

def page(p, body):
    lb = LIGHTBOX if p.get('lightbox') else ''
    # SCRIPTS: main.js (behaviour) is deferred. GSAP + ScrollTrigger + motion.js load sequentially AFTER the window
    # 'load' event, so the animation library can never delay first paint or LCP. If they fail, head()'s 4s timer
    # removes the .anim class and all content is shown.
    loader = ("<script>window.addEventListener('load',function(){var q=['assets/js/vendor/gsap.min.js','assets/js/vendor/ScrollTrigger.min.js','assets/js/motion.js'];"
              "(function n(){var s=q.shift();if(!s)return;var e=document.createElement('script');e.src=s;e.onload=n;e.onerror=n;document.head.appendChild(e)})()})</script>\n")
    scripts = '<script src="assets/js/main.js" defer></script>\n' + loader
    return (head(p) + header(p['active']) + f'<main id="main" data-inert-when-nav-open>\n{body}\n</main>\n'
            + footer() + map_dialog() + lb + scripts + '</body>\n</html>\n')

BANNER_SIZES = '(min-width: 76rem) 1160px, 100vw'

def phead(p, title, lead, actions='', media=None, split=False):
    cr = crumbs(p) if p.get('crumbs') else ''
    if split:
        return f'''<header class="phead phead--split section--tight"><div class="wrap phead__grid">
  <div>{cr}<h1 class="phead__title">{title}</h1><p class="phead__lead">{lead}</p>{actions}</div>
  <div class="phead__media">{media}</div></div></header>'''
    m = f'<div class="phead__media">{media}</div>' if media else ''
    return f'''<header class="phead"><div class="wrap">{cr}<h1 class="phead__title">{title}</h1><p class="phead__lead">{lead}</p>{actions}{m}</div></header>'''

def call_actions(extra=''):
    return f'<div class="actions"><a class="btn btn--call" href="tel:{CALL}">{icon("phone")}Call\u00a0{CALL_DISPLAY}</a>{extra}</div>'

PAGES = []

# ---------------------------------------------------------------- Home
def home():
    p = dict(file='index.html', active='home', schema_type='WebPage',
             title='GLS Refrigeration & Air Conditioning | Johannesburg',
             desc='GLS installs, repairs and maintains refrigeration and air-conditioning systems for homes and businesses in Johannesburg and Germiston. Operating since 2011.')
    opts = [('fridge', 'Fridge or freezer isn’t keeping cold'), ('coldroom', 'Cold room or walk-in freezer problem'),
            ('aircon', 'Air conditioner isn’t cooling'), ('other', 'Something else, or not sure')]
    buttons = ''.join(f'<button type="button" class="triage__opt" data-issue="{k}" aria-pressed="false">{t}</button>' for k, t in opts)
    nos = ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in [('Fridge or freezer', 'contact.html?issue=fridge'), ('Cold room or walk-in freezer', 'contact.html?issue=coldroom'), ('Air conditioner', 'contact.html?issue=aircon'), ('Something else', 'contact.html?issue=other')])
    body = f'''<section class="hero" aria-labelledby="hero-title">
  <!-- IMAGE PLACEMENT: hero photograph, assets/img/condensing-unit-copper-receiver-*.webp (from 16.png). Confirm it is GLS's own or licensed. -->
  <div class="hero__media">{img('condensing-unit-copper-receiver', '100vw', loading='eager', fetch='high', cls='hero__img')}</div>
  <div class="hero__shade"></div>
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <p class="label">Refrigeration and air conditioning</p>
      <h1 class="hero__title" id="hero-title">What’s not keeping cold?</h1>
      <p class="hero__lead">GLS installs, repairs and maintains refrigeration and air-conditioning systems for homes and businesses in Johannesburg and surrounding areas. A registered company, operating since {FOUNDED}.</p>
      <div class="actions"><a class="btn btn--call" href="tel:{CALL}">{icon('phone')}Call\u00a0{CALL_DISPLAY}</a><a class="btn" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}WhatsApp</a><a class="link" href="services.html">Our services</a></div>
    </div>
    <p class="hero__caption">Copper pipework and receiver on a refrigeration condensing unit</p>
  </div>
</section>

<!-- TRIAGE: buttons are enhanced by assets/js/main.js (initTriage); the noscript list keeps it usable without JavaScript. -->
<section class="triage-wrap" aria-labelledby="triage-title">
  <div class="wrap">
    <div class="triage">
      <div class="triage__head">
        <h2 class="triage__title" id="triage-title">Something not working?</h2>
        <p class="triage__sub">Pick the closest match and we’ll tell you what to send us.</p>
      </div>
      <div class="triage__opts" id="triage-options" role="group" aria-labelledby="triage-title">{buttons}</div>
      <div id="triage-result" class="triage__result" aria-live="polite"></div>
      <noscript><div class="triage__fallback"><p>Choose what is wrong:</p><ul>{nos}</ul></div></noscript>
    </div>
  </div>
</section>

<section class="section intro" aria-labelledby="what-title">
  <div class="wrap intro__grid">
    <div class="intro__text" data-reveal>
      <p class="label">About GLS</p>
      <h2 class="h2" id="what-title">One company for installation, repair and maintenance.</h2>
      <p>GLS started in {FOUNDED}. We work on refrigeration and air-conditioning systems in homes, offices, restaurants and supermarkets: new installations, servicing for existing equipment, and call-outs when something fails.</p>
      <p>On every job the aim is the same: a system that runs efficiently, and a clear quote before any work begins.</p>
      <ul class="inline-facts"><li>Operating since {FOUNDED}</li><li>Registered company</li><li>Emergency repair 24/7</li></ul>
      <a class="link" href="about.html">About GLS</a>
    </div>
    <div class="intro__media">
      <!-- IMAGE PLACEMENT: layered pair -->
      {pic('technician-rooftop-compressor', '(min-width: 52em) 28vw, 70vw', ratio='r-45', cls='m1', pos='50% 40%')}
      {pic('outdoor-units-bracketed-brick-wall', '(min-width: 52em) 18vw, 40vw', ratio='r-34', cls='m2')}
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="services-title" style="padding-top:0">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Services</p><h2 class="h2" id="services-title">What GLS does</h2></header>
    <article class="svc" data-reveal>
      <div class="svc__media">{pic('rooftop-split-units-corrugated-roof', '(min-width: 52em) 50vw, 100vw', pos='70% 50%')}</div>
      <div class="svc__body">
        <h3 class="h3">Air conditioning</h3>
        <p>Split-unit and ducted systems installed in homes, offices and server rooms, then serviced, repaired and upgraded to energy-efficient inverter units.</p>
        <ul class="tags"><li>Installation</li><li>Servicing</li><li>Repair</li><li>Upgrades</li></ul>
        <a class="link" href="air-conditioning.html">Air-conditioning services</a>
      </div>
    </article>
    <article class="svc svc--flip" data-reveal>
      <div class="svc__media">{pic('hermetic-compressor-wall-mounted', '(min-width: 52em) 50vw, 100vw', pos='45% 50%')}</div>
      <div class="svc__body">
        <h3 class="h3">Commercial refrigeration and cold rooms</h3>
        <p>Walk-in freezers, cold rooms and commercial refrigeration units for restaurants, supermarkets and retail, installed and kept running.</p>
        <ul class="tags"><li>Cold rooms</li><li>Walk-in freezers</li><li>Retail units</li><li>Emergency repair</li></ul>
        <a class="link" href="commercial-refrigeration.html">Refrigeration services</a>
      </div>
    </article>
    <article class="svc" data-reveal>
      <div class="svc__media">{pic('contactor-bank-digital-controller', '(min-width: 52em) 50vw, 100vw', pos='50% 40%')}</div>
      <div class="svc__body">
        <h3 class="h3">Planned maintenance</h3>
        <p>Inspections of filters, refrigerant levels and electrical wiring, with critical components cleaned, to prevent breakdowns and extend system life.</p>
        <ul class="tags"><li>Inspections</li><li>Filter cleaning</li><li>Refrigerant checks</li><li>Wiring checks</li></ul>
        <a class="link" href="maintenance.html">Maintenance plans</a>
      </div>
    </article>
    <div class="pair" data-reveal>
      <div><h3 class="h3">Emergency repair</h3><p>When a system fails, call. Repair is available 24 hours a day, 7 days a week, with fast response and expert diagnostics.</p><a class="link" href="contact.html">Call or WhatsApp</a></div>
      <div><h3 class="h3">Free site assessment</h3><p>Not sure what suits your space? A technician assesses the site, recommends a system and goes through options that fit your budget.</p><a class="link" href="contact.html?service=consultation">Request an assessment</a></div>
    </div>
  </div>
</section>

<section class="section section--ink" aria-labelledby="work-title">
  <div class="wrap">
    <header class="sec-head sec-head--row" data-reveal>
      <div><p class="label">Our work</p><h2 class="h2" id="work-title">From the field</h2></div>
      <a class="link" href="our-work.html">See all photos and video</a>
    </header>
    <!-- IMAGE PLACEMENT: work mosaic (five real job photographs) -->
    <div class="teaser">
      {pic('outdoor-unit-panel-removed-control-boards', '(min-width: 52em) 28vw, 100vw', ratio='', cls='t1', pos='50% 35%')}
      {pic('brazing-compressor-connection', '(min-width: 52em) 40vw, 100vw', ratio='', cls='t2', pos='60% 50%')}
      {pic('compressor-rack-control-boxes', '(min-width: 52em) 24vw, 50vw', ratio='', cls='t3', pos='50% 40%')}
      {pic('condensing-unit-rooftop-platform', '(min-width: 52em) 24vw, 50vw', ratio='', cls='t4', pos='60% 55%')}
      {pic('ceiling-mounted-indoor-unit-pipework', '(min-width: 52em) 16vw, 50vw', ratio='', cls='t5', pos='50% 55%')}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Why GLS</p><h2 class="h2" id="why-title">How GLS works with you</h2></header>
    <div class="cols4">
      <div data-reveal><h3>Experienced technicians</h3><p>Licensed and insured technicians with field experience since {FOUNDED} handle every installation and repair.</p></div>
      <div data-reveal><h3>Fast response</h3><p>We respond quickly, work efficiently on site and respect your time.</p></div>
      <div data-reveal><h3>Clear pricing</h3><p>Upfront quotes with no hidden fees. You know what you are paying for before work starts.</p></div>
      <div data-reveal><h3>Aftercare</h3><p>Ongoing maintenance and client support, so systems keep performing after the job is done.</p></div>
    </div>
  </div>
</section>

{band()}'''
    return p, body
PAGES.append(home)

# ---------------------------------------------------------------- Services hub
def services():
    p = dict(file='services.html', active='services', schema_type='CollectionPage',
             title='Refrigeration & Air-Conditioning Services | GLS',
             desc='Air-conditioning, commercial refrigeration, cold rooms, maintenance and 24/7 emergency repair from GLS, serving Johannesburg and Germiston since 2011.',
             crumbs=[('Home', ''), ('Services', None)], faq='services',
             service=dict(name='Refrigeration and air-conditioning services', type='Refrigeration and air-conditioning installation, maintenance and repair',
                          desc='Installation, preventative maintenance, 24/7 emergency repair, system upgrades and consultation for residential and commercial refrigeration and air-conditioning systems.'))
    rows = ''.join([
        row('Installation', 'Modern cooling systems installed to the standard each job needs, for residential and commercial properties.', ['Split-unit air conditioners', 'Ducted HVAC systems', 'Walk-in freezers and cold rooms', 'Commercial refrigeration units'], [('Air conditioning', 'air-conditioning.html'), ('Cold rooms and refrigeration', 'commercial-refrigeration.html')]),
        row('Preventative maintenance', 'Regular servicing keeps systems efficient. We inspect filters, refrigerant levels and electrical wiring, and clean critical components, to prevent breakdowns and extend system life.', ['Comprehensive system inspections', 'Filter cleaning and replacement', 'Refrigerant level checks', 'Performance optimisation'], [('Maintenance plans', 'maintenance.html')]),
        row('24/7 emergency repair', 'When a cooling system fails, call. Our team repairs refrigeration and air-conditioning systems around the clock to protect your comfort and your business.', ['Available 24 hours, 7 days a week', 'Fast response', 'Expert diagnostics', 'Reliable, lasting solutions'], [('Call or WhatsApp', 'contact.html')]),
        row('Commercial and residential', 'Supermarkets, office buildings, restaurants and homes, from a single home unit to large commercial systems.', ['Residential air conditioning', 'Office climate control', 'Retail refrigeration', 'Server room cooling']),
        row('System upgrades', 'Move to modern, eco-friendly systems that use less energy and perform more reliably.', ['Energy-efficient systems', 'Modern inverter technology', 'Eco-friendly refrigerants', 'Smart climate control'], [('Air conditioning', 'air-conditioning.html#upgrades')]),
        row('Expert consultation', 'Not sure what suits your space? Experienced technicians assess your needs and recommend a system.', ['Free site assessments', 'Custom system design', 'Energy efficiency analysis', 'Budget-friendly options'], [('Request an assessment', 'contact.html?service=consultation')]),
    ])
    media = pic('condensing-unit-rooftop-platform', BANNER_SIZES, ratio='', loading='eager', fetch='high', pos='50% 62%')
    body = f'''{phead(p, 'Refrigeration and air-conditioning services', 'Installation, maintenance, emergency repair and upgrades for homes and businesses in Johannesburg and surrounding areas, from our base in Primrose, Germiston.', call_actions('<a class="btn btn--ghost" href="contact.html">Request a quote</a>'), media)}
<section class="section" aria-labelledby="all-title">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Everything GLS offers</p><h2 class="h2" id="all-title">Six areas of work</h2></header>
    <div class="rows">{rows}</div>
  </div>
</section>
<section class="section section--frost" aria-labelledby="faq-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Questions</p><h2 class="h2" id="faq-title">Common questions</h2></div>
    <div data-reveal>{faq_html('services')}</div>
  </div>
</section>
{band()}'''
    return p, body
PAGES.append(services)

# ---------------------------------------------------------------- Air conditioning
def aircon():
    p = dict(file='air-conditioning.html', active='ac', schema_type='WebPage',
             title='Air-Conditioning Installation & Repair | GLS Germiston',
             desc='Split-unit and ducted air-conditioning installation, servicing, repair and upgrades for homes and businesses in Johannesburg and Germiston.',
             crumbs=[('Home', ''), ('Services', 'services.html'), ('Air conditioning', None)], faq='ac',
             service=dict(name='Air-conditioning installation, repair and maintenance', type='Air-conditioning installation and repair',
                          desc='Installation of split-unit and ducted air-conditioning for homes, offices and server rooms, plus servicing, 24/7 emergency repair and upgrades to energy-efficient inverter systems.'))
    media = pic('rooftop-split-units-corrugated-roof', BANNER_SIZES, ratio='', loading='eager', fetch='high', pos='65% 50%')
    body = f'''{phead(p, 'Air-conditioning installation, servicing and repair', 'GLS installs split-unit and ducted systems for homes, offices and server rooms in Johannesburg and Germiston, and keeps them running with servicing, 24/7 emergency repair and upgrades.', call_actions('<a class="btn btn--ghost" href="contact.html?issue=aircon">Describe the problem</a>'), media)}
<section class="section" aria-labelledby="ac-services">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Air conditioning</p><h2 class="h2" id="ac-services">What we do</h2></header>
    <div class="rows">
      {row('Installation', 'Split units and ducted systems installed with precision for long-lasting performance, for residential and commercial properties.', ['Split-unit air conditioners', 'Ducted HVAC systems', 'Office climate control', 'Server room cooling'])}
      {row('Servicing and maintenance', 'Thorough inspections of filters, refrigerant levels and electrical wiring, with critical components cleaned to prevent breakdowns.', ['System inspections', 'Filter cleaning and replacement', 'Refrigerant level checks', 'Performance optimisation'], [('Maintenance plans', 'maintenance.html')])}
      {row('Emergency repair', 'A failed system at the wrong time is a problem we attend to around the clock, with expert diagnostics and a lasting fix.', ['24 hours a day, 7 days a week', 'Fast response', 'Expert diagnostics'], [('Call or WhatsApp', 'contact.html?issue=aircon')])}
      {row('Upgrades', 'Replace ageing equipment with systems that use less energy and perform better.', ['Energy-efficient systems', 'Modern inverter technology', 'Eco-friendly refrigerants', 'Smart climate control'], rid='upgrades')}
      {row('Free site assessment', 'We assess the space, recommend a system and discuss options that fit your budget.', ['Custom system design', 'Energy efficiency analysis', 'Budget-friendly options'], [('Request an assessment', 'contact.html?service=consultation')])}
    </div>
  </div>
</section>
<section class="section section--frost" aria-label="Air-conditioning photographs">
  <div class="wrap">
    <div class="duo">
      <div class="wide">{pic('outdoor-unit-ground-mounted', '(min-width: 52em) 55vw, 100vw', caption='A ground-mounted outdoor unit.')}</div>
      {pic('wall-mounted-split-outdoor-units', '(min-width: 52em) 36vw, 50vw', ratio='r-45', caption='Outdoor units bracketed to a wall.', pos='50% 40%')}
    </div>
  </div>
</section>
<section class="section" aria-labelledby="faq-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Questions</p><h2 class="h2" id="faq-title">Air-conditioning questions</h2></div>
    <div data-reveal>{faq_html('ac')}</div>
  </div>
</section>
{band('Air conditioner not cooling?')}'''
    return p, body
PAGES.append(aircon)

# ---------------------------------------------------------------- Commercial refrigeration
def refrig():
    p = dict(file='commercial-refrigeration.html', active='refrig', schema_type='WebPage',
             title='Commercial Refrigeration & Cold Rooms | GLS Germiston',
             desc='Commercial refrigeration, walk-in freezers and cold rooms installed, serviced and repaired for restaurants, supermarkets and retail. Germiston and Johannesburg.',
             crumbs=[('Home', ''), ('Services', 'services.html'), ('Commercial refrigeration', None)], faq='refrig',
             service=dict(name='Commercial refrigeration, cold room and walk-in freezer services', type='Commercial refrigeration installation and repair',
                          desc='Installation, maintenance and 24/7 emergency repair of commercial refrigeration units, walk-in freezers and cold rooms for restaurants, supermarkets and retail.'))
    media = pic('brazing-compressor-connection', BANNER_SIZES, ratio='', loading='eager', fetch='high', pos='60% 50%')
    body = f'''{phead(p, 'Commercial refrigeration, cold rooms and walk-in freezers', 'GLS installs, services and repairs refrigeration for restaurants, supermarkets and retail across Johannesburg and Germiston. When a unit stops keeping cold, we respond around the clock.', call_actions('<a class="btn btn--ghost" href="contact.html?issue=fridge">Describe the problem</a>'), media)}
<section class="section" aria-labelledby="rf-services">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Refrigeration</p><h2 class="h2" id="rf-services">What we do</h2></header>
    <div class="rows">
      {row('Commercial refrigeration units', 'Installation and servicing of refrigeration units for retail and food businesses.', ['Retail refrigeration', 'Supermarket and restaurant equipment', 'Installation and commissioning'])}
      {row('Cold rooms and walk-in freezers', 'Walk-in freezers and cold rooms installed with precision, then maintained so they hold temperature.', ['Walk-in freezers', 'Cold rooms', 'Condensing units and controls'], rid='cold-rooms')}
      {row('Maintenance', 'Regular inspections of refrigerant levels and electrical wiring, with critical components cleaned, to prevent breakdowns.', ['System inspections', 'Refrigerant level checks', 'Performance optimisation'], [('Maintenance plans', 'maintenance.html')])}
      {row('Emergency repair', 'A failed refrigeration unit puts stock and trading at risk. Repair is available 24 hours a day, 7 days a week.', ['24 hours a day, 7 days a week', 'Fast response', 'Expert diagnostics'], [('Call or WhatsApp', 'contact.html?issue=fridge')])}
      {row('Free site assessment', 'We assess the site, design the system and talk through options that suit your budget.', ['Custom system design', 'Energy efficiency analysis', 'Budget-friendly options'], [('Request an assessment', 'contact.html?service=consultation')])}
    </div>
  </div>
</section>
<section class="section section--frost" aria-label="Refrigeration photographs">
  <div class="wrap">
    <div class="duo duo--rev">
      {pic('evaporator-coils-in-frame', '(min-width: 52em) 36vw, 50vw', ratio='r-45', caption='Evaporator coils in a frame.', pos='50% 45%')}
      <div class="wide">{pic('hermetic-compressor-wall-mounted', '(min-width: 52em) 55vw, 100vw', caption='A hermetic compressor on a wall-mounted unit.')}</div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="faq-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Questions</p><h2 class="h2" id="faq-title">Refrigeration questions</h2></div>
    <div data-reveal>{faq_html('refrig')}</div>
  </div>
</section>
{band('Fridge, freezer or cold room down?')}'''
    return p, body
PAGES.append(refrig)

# ---------------------------------------------------------------- Maintenance
def maint():
    p = dict(file='maintenance.html', active='maint', schema_type='WebPage',
             title='Refrigeration & Aircon Maintenance Plans | GLS',
             desc='Planned maintenance for refrigeration and air conditioning: inspections, filter cleaning, refrigerant and wiring checks. Johannesburg and Germiston.',
             crumbs=[('Home', ''), ('Services', 'services.html'), ('Planned maintenance', None)], faq='maint',
             service=dict(name='Refrigeration and air-conditioning maintenance', type='Preventative maintenance',
                          desc='Preventative maintenance including system inspections, filter cleaning and replacement, refrigerant level checks, electrical wiring checks and performance optimisation.'))
    media = pic('manifold-gauges-refrigerant-cylinder-ladder', '(min-width: 52em) 30vw, 80vw', ratio='r-45', loading='eager', fetch='high', pos='50% 50%')
    body = f'''{phead(p, 'Planned maintenance for refrigeration and air conditioning', 'Regular servicing finds worn and dirty components before they fail. GLS builds maintenance plans around your equipment, for homes and businesses in Johannesburg and Germiston.', call_actions('<a class="btn btn--ghost" href="contact.html?service=consultation">Request an assessment</a>'), media, split=True)}
<section class="section" aria-labelledby="m-covers">
  <div class="wrap split">
    <div class="split__text" data-reveal>
      <p class="label">What is covered</p>
      <h2 class="h2" id="m-covers">What a maintenance service covers</h2>
      <ul class="checklist">
        <li>Comprehensive system inspections</li>
        <li>Filter cleaning and replacement</li>
        <li>Refrigerant level checks</li>
        <li>Electrical wiring checks</li>
        <li>Cleaning of critical components</li>
        <li>Performance optimisation</li>
      </ul>
      <p>The aim is fewer breakdowns and a longer working life for the system. Maintenance plans are personalised to your home or business, and GLS supports you after each visit.</p>
      <a class="link" href="contact.html?service=consultation">Talk to GLS about a plan</a>
    </div>
    {pic('condenser-fan-assembly-guard', '(min-width: 52em) 36vw, 100vw', ratio='r-45', caption='A condenser fan with its guard.', pos='50% 40%')}
  </div>
</section>
<section class="section section--frost" aria-labelledby="faq-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Questions</p><h2 class="h2" id="faq-title">Maintenance questions</h2></div>
    <div data-reveal>{faq_html('maint')}</div>
  </div>
</section>
{band('Book a maintenance assessment')}'''
    return p, body
PAGES.append(maint)

# ---------------------------------------------------------------- Our work
CAP = {
 'brazing-compressor-connection': 'Brazing a compressor connection.', 'condensing-unit-copper-receiver': 'Copper pipework and receiver on a condensing unit.',
 'rooftop-split-units-corrugated-roof': 'Split-system outdoor units on a roof.', 'contactor-bank-digital-controller': 'Contactors and a digital temperature controller.',
 'hermetic-compressor-wall-mounted': 'A hermetic compressor on a wall-mounted unit.', 'technician-rooftop-compressor': 'A technician with a compressor on a rooftop.',
 'compressor-rack-control-boxes': 'Compressors and control boxes on a rack.', 'wall-mounted-split-outdoor-units': 'Outdoor units bracketed to a wall.',
 'evaporator-coils-in-frame': 'Evaporator coils in a frame.', 'condensing-unit-rooftop-platform': 'A condensing unit on a rooftop platform.',
 'ceiling-mounted-indoor-unit-pipework': 'An indoor unit fitted with pipework.', 'timer-and-contactor-box': 'A time switch and contactors.',
 'round-cassette-unit-fan-grille': 'Underside of a round-flow cassette unit.', 'outdoor-units-bracketed-brick-wall': 'Outdoor units on a face-brick wall.',
 'refrigeration-control-enclosure': 'A control enclosure beside a compressor.', 'condensing-unit-on-stand-r410a': 'A condensing unit with an R410A cylinder.',
 'outdoor-unit-panel-removed-control-boards': 'An outdoor unit with its panel removed.', 'outdoor-unit-ground-mounted': 'A ground-mounted outdoor unit.',
 'condenser-fan-assembly-guard': 'A condenser fan with its guard.', 'split-unit-components-staged-copper-coil': 'Split-unit components ready for installation.',
 'manifold-gauges-refrigerant-cylinder-ladder': 'Manifold gauges and a refrigerant cylinder.', 'outdoor-electrical-enclosure': 'An outdoor electrical enclosure.',
 'rooftop-condensing-units-weathered': 'Older condensing units on a flat roof.',
}
# Each group: (title, description, [(image, desktop column span of 12)]). Spans per row sum to 12.
GROUPS = [
 ('Compressors and refrigeration units', 'Compressors, condensing units, coils and pipework.',
  [('brazing-compressor-connection', 7), ('evaporator-coils-in-frame', 5), ('condensing-unit-on-stand-r410a', 4), ('compressor-rack-control-boxes', 4),
   ('condenser-fan-assembly-guard', 4), ('condensing-unit-copper-receiver', 7), ('hermetic-compressor-wall-mounted', 5)]),
 ('Controls and electrical', 'Contactors, controllers and enclosures.',
  [('contactor-bank-digital-controller', 7), ('refrigeration-control-enclosure', 5), ('outdoor-electrical-enclosure', 5), ('timer-and-contactor-box', 7)]),
 ('Air-conditioning installations', 'Split units, cassette units and ducted equipment.',
  [('rooftop-split-units-corrugated-roof', 7), ('ceiling-mounted-indoor-unit-pipework', 5), ('wall-mounted-split-outdoor-units', 4), ('outdoor-units-bracketed-brick-wall', 4),
   ('split-unit-components-staged-copper-coil', 4), ('outdoor-unit-ground-mounted', 8), ('round-cassette-unit-fan-grille', 4)]),
 ('On site', 'Rooftops, gauges and open units.',
  [('condensing-unit-rooftop-platform', 7), ('technician-rooftop-compressor', 5), ('manifold-gauges-refrigerant-cylinder-ladder', 4),
   ('outdoor-unit-panel-removed-control-boards', 4), ('rooftop-condensing-units-weathered', 4)]),
]
VIDEOS = [
 ('outdoor-unit-control-boards', 'Control boards inside a large outdoor air-conditioning unit with the panel removed.'),
 ('compressor-copper-rooftop', 'A technician working on a compressor and copper pipework beside outdoor units.'),
 ('rooftop-refrigerant-service', 'Service work on rooftop outdoor units, with a refrigerant cylinder and toolbox.'),
 ('rooftop-outdoor-units-team', 'Two technicians working on a bank of rooftop outdoor units.'),
]
def mosaic(items):
    """Build tiles; on mobile (2 columns) an unpaired narrow tile is promoted to full width so no row is left half empty."""
    flags, run = [], []
    for i, (_, span) in enumerate(items):
        if span >= 7:
            if len(run) % 2: flags[run[-1]] = True
            run = []; flags.append(False)
        else:
            flags.append(False); run.append(i)
    if len(run) % 2: flags[run[-1]] = True
    return ''.join(tile(b, CAP[b], s, wide=flags[i], sizes=('(min-width: 52em) %dvw, 100vw' % (s * 6) if s >= 7 else '(min-width: 52em) %dvw, 50vw' % (s * 6)))
                   for i, (b, s) in enumerate(items))

def work():
    p = dict(file='our-work.html', active='work', schema_type='CollectionPage', lightbox=True,
             title='Our Work: Refrigeration & Air-Con Projects | GLS',
             desc='Photos and video from GLS jobs: condensing units, compressors, control panels and air-conditioning installations in Johannesburg and Germiston.',
             crumbs=[('Home', ''), ('Our work', None)])
    total = sum(len(g[2]) for g in GROUPS)
    groups = ''.join(f'''<section class="group" aria-labelledby="g{i}" data-reveal>
  <div class="group__head"><span class="count">{len(items):02d} photographs</span><h2 id="g{i}">{t}</h2><p>{d}</p></div>
  <div class="mosaic">{mosaic(items)}</div>
</section>''' for i, (t, d, items) in enumerate(GROUPS))
    vids = ''
    for b, c in VIDEOS:
        # VIDEO PLACEMENT: assets/video/{b}.mp4 (compressed from the supplied videos), poster assets/img/poster-{b}.webp
        with Image.open(os.path.join(IMGDIR, f'poster-{b}.webp')) as im: pw, ph = im.size
        vids += f'<figure class="video" data-reveal><video controls preload="none" playsinline poster="assets/img/poster-{b}.webp" width="{pw}" height="{ph}" aria-label="{esc(c)}"><source src="assets/video/{b}.mp4" type="video/mp4">Your browser can’t play this video. <a href="assets/video/{b}.mp4">Download it</a>.</video><figcaption>{c}</figcaption></figure>'
    body = f'''{phead(p, 'Our work', f'{total} photographs and four short videos from GLS jobs: condensing units, compressors, control panels and air-conditioning installations. Select a photograph to view it larger.')}
<section class="section section--tight" aria-label="Photographs">
  <div class="wrap">{groups}</div>
</section>
<section class="section section--ink" aria-labelledby="video-title">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Video</p><h2 class="h2" id="video-title">Video from site</h2><p class="muted" style="margin-top:.6rem;color:rgba(246,248,249,.7)">Short clips from site. Video loads only when you press play.</p></header>
    <div class="videos">{vids}</div>
  </div>
</section>
{band('Have a similar job?')}'''
    return p, body
PAGES.append(work)

# ---------------------------------------------------------------- About
def about():
    p = dict(file='about.html', active='about', schema_type='AboutPage',
             title='About GLS | Refrigeration & Air Conditioning Since 2011',
             desc='GLS is a registered refrigeration and air-conditioning company operating since 2011 from Primrose, Germiston. Our approach, mission and vision.',
             crumbs=[('Home', ''), ('About', None)])
    media = pic('technician-rooftop-compressor', '(min-width: 52em) 30vw, 80vw', ratio='r-45', loading='eager', fetch='high', pos='50% 40%', caption='A technician on a rooftop with a compressor.')
    body = f'''{phead(p, f'A local refrigeration and air-conditioning company, operating since {FOUNDED}', 'GLS keeps homes, businesses and industrial sites running with reliable cooling across Johannesburg and surrounding areas.', '', media, split=True)}
<section class="section" aria-labelledby="approach-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Approach</p><h2 class="h2" id="approach-title">Our approach</h2></div>
    <div data-reveal>
      <p class="lead">We start by understanding what your space needs, then design the installation or maintenance plan around it.</p>
      <p>Our focus is on energy-efficient, durable systems that meet your requirements. Our licensed technicians install and maintain systems to industry standards, and quality and customer satisfaction come first on every job.</p>
    </div>
  </div>
</section>
<section class="section section--ink" aria-labelledby="mv-title">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Direction</p><h2 class="h2" id="mv-title">Mission and vision</h2></header>
    <div class="cols4" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))">
      <div data-reveal style="border-top-color:rgba(246,248,249,.16)"><h3>Mission</h3><p style="color:rgba(246,248,249,.82)">To provide reliable, efficient and affordable refrigeration and air-conditioning solutions that improve comfort and productivity for our clients across Johannesburg and surrounding areas.</p></div>
      <div data-reveal style="border-top-color:rgba(246,248,249,.16)"><h3>Vision</h3><p style="color:rgba(246,248,249,.82)">A future where climate control is smarter, more reliable and accessible to everyone, with environments that support wellbeing and efficiency in every space we serve.</p></div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <header class="sec-head" data-reveal><p class="label">Why GLS</p><h2 class="h2" id="why-title">Why clients choose GLS</h2></header>
    <div class="cols4">
      <div data-reveal><h3>Fast response</h3><p>We respect your time and respond promptly when a cooling system fails.</p></div>
      <div data-reveal><h3>Tailored solutions</h3><p>Installations and maintenance plans designed around your home or business.</p></div>
      <div data-reveal><h3>Aftercare and support</h3><p>Ongoing maintenance and dedicated client support so systems keep performing.</p></div>
      <div data-reveal><h3>Licensed and trusted</h3><p>Certified technicians with experience and a track record since {FOUNDED}.</p></div>
    </div>
  </div>
</section>
<section class="section section--frost" aria-labelledby="co-title">
  <div class="wrap split split--even">
    <div data-reveal><p class="label">Company</p><h2 class="h2" id="co-title">Company details</h2><p class="muted" style="margin-top:.8rem">Residential, commercial and industrial refrigeration and air conditioning. <a class="link" href="our-work.html">See our work</a></p></div>
    <dl class="facts" data-reveal>
      <div class="facts__item"><dt>Registered name</dt><dd>{LEGAL}</dd></div>
      <div class="facts__item"><dt>Operating since</dt><dd>{FOUNDED}</dd></div>
      <div class="facts__item"><dt>Based in</dt><dd>{ADDRESS_LINE}</dd></div>
      <div class="facts__item"><dt>Area served</dt><dd>Johannesburg and surrounding areas</dd></div>
    </dl>
  </div>
</section>
{band()}'''
    return p, body
PAGES.append(about)

# ---------------------------------------------------------------- Contact
def contact():
    p = dict(file='contact.html', active='contact', schema_type='ContactPage',
             title='Contact GLS | Call, WhatsApp or Visit in Primrose',
             desc=f'Call {CALL_DISPLAY}, WhatsApp {WA_DISPLAY} or visit {ADDRESS_LINE}. Emergency refrigeration and air-conditioning repair 24/7.',
             crumbs=[('Home', ''), ('Contact', None)])
    svc = ['Air-conditioning installation', 'Air-conditioning repair', 'Refrigeration repair', 'Cold room or walk-in freezer', 'Planned maintenance', 'System upgrade', 'Free site assessment', 'Other']
    opts = '<option value="">Choose a service (optional)</option>' + ''.join(f'<option value="{s}">{s}</option>' for s in svc)
    body = f'''{phead(p, 'Contact GLS', 'Call for urgent faults. Use WhatsApp for quotes and for anything you want to send us a photo of.')}
<section class="section section--tight" aria-labelledby="enquire-title" style="padding-top:clamp(1.5rem,3vw,2.5rem)">
  <div class="wrap contact-grid">
    <div data-reveal>
      <h2 class="h3" id="enquire-title" style="margin-bottom:1rem">Reach GLS directly</h2>
      <div class="methods">
        <div class="method"><span class="method__label">Call</span><a class="method__value" href="tel:{CALL}">{CALL_DISPLAY}</a><p class="method__note">Fastest for urgent faults. Emergency repair is available 24 hours a day, 7 days a week.</p></div>
        <div class="method"><span class="method__label">WhatsApp</span><a class="method__value" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">{WA_DISPLAY}</a><p class="method__note">Send a message or photos of the fault.</p></div>
        <div class="method"><span class="method__label">Email</span><a class="method__value" href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="method"><span class="method__label">Visit</span><span class="method__value">{ADDRESS_LINE}</span><p class="method__note"><a href="{MAP_GOOGLE}" data-map-open target="_blank" rel="noopener noreferrer">Get directions</a></p></div>
      </div>
    </div>

    <!-- ENQUIRY FORM: delivers by WhatsApp hand-off (assets/js/main.js, initForm). FUTURE INTEGRATION: add a server-side email/CRM endpoint here if GLS wants enquiries logged. -->
    <form class="form" id="enquiry-form" novalidate data-reveal>
      <div class="form__head"><h2>Send an enquiry by WhatsApp</h2></div>
      <div class="form__body">
        <div class="form__row">
          <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-error"><p class="field__error" id="f-name-error" hidden></p></div>
          <div class="field"><label for="f-phone">Phone number</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required aria-describedby="f-phone-error"><p class="field__error" id="f-phone-error" hidden></p></div>
        </div>
        <div class="field"><label for="f-email">Email <span class="hint">(optional)</span></label><input id="f-email" name="email" type="email" autocomplete="email" aria-describedby="f-email-error"><p class="field__error" id="f-email-error" hidden></p></div>
        <div class="field"><label for="f-service">Service</label><select id="f-service" name="service">{opts}</select></div>
        <div class="field"><label for="f-message">What do you need?</label><textarea id="f-message" name="message" rows="5" required aria-describedby="f-message-error"></textarea><p class="field__error" id="f-message-error" hidden></p></div>
        <button class="btn" type="submit">{icon('whatsapp')}Continue in WhatsApp</button>
        <p class="form__note">This opens WhatsApp with your message ready to send. It reaches GLS when you press Send in WhatsApp.</p>
        <div class="form__status" id="form-status" role="status" tabindex="-1" hidden>
          <p><strong data-status-title>WhatsApp is opening with your message ready.</strong>Press Send in WhatsApp to deliver it to GLS. Until you do, GLS has not received it.</p>
          <p>WhatsApp didn’t open? <a id="status-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">Open WhatsApp</a>. Prefer email? <a id="status-mail" href="mailto:{EMAIL}">Send it by email</a>.</p>
        </div>
      </div>
    </form>
  </div>
</section>

<section class="section" aria-labelledby="find-title">
  <div class="wrap">
    <!-- MAP: no embedded map. The button opens a chooser for Google Maps, Apple Maps or Waze. -->
    <div class="locate">
      <div class="locate__body" data-reveal>
        <p class="label">Visit</p>
        <h2 class="h2" id="find-title">Find GLS</h2>
        <p class="locate__addr">{ADDRESS_LINE}</p>
        <p class="muted">GLS is based in Primrose, Germiston and serves Johannesburg and surrounding areas. Choose Google Maps, Apple Maps or Waze to get directions.</p>
        <div class="actions"><a class="btn" href="{MAP_GOOGLE}" data-map-open target="_blank" rel="noopener noreferrer">{icon('pin')}Open in maps</a></div>
      </div>
      <div class="locate__photo">{pic('wall-mounted-split-outdoor-units', '(min-width: 52em) 40vw, 100vw', ratio='', pos='50% 38%')}</div>
    </div>
  </div>
</section>'''
    return p, body
PAGES.append(contact)

# ---------------------------------------------------------------- 404
def notfound():
    p = dict(file='404.html', active='', title='Page not found | GLS Refrigeration & Air Conditioning',
             desc='The page you were looking for could not be found. Return to GLS Refrigeration and Air Conditioning.', noindex=True)
    body = f'''<section class="notfound">
  <div class="wrap">
    <h1 class="phead__title">That page isn’t here</h1>
    <p class="phead__lead">The link may be old or mistyped. Use the menu, or go straight to a service.</p>
    <div class="actions"><a class="btn" href="./">Go to the homepage</a><a class="btn btn--ghost" href="services.html">View services</a><a class="btn btn--call" href="tel:{CALL}">{icon('phone')}Call\u00a0{CALL_DISPLAY}</a></div>
  </div>
</section>'''
    return p, body
PAGES.append(notfound)

# ------------------------------------------------------------------ write everything
def w(path, text):
    with open(os.path.join(ROOT, path), 'w', encoding='utf-8', newline='\n') as f: f.write(text)

built = []
for fn in PAGES:
    p, body = fn()
    w(p['file'], page(p, body))
    built.append(p)

# sitemap (indexable pages only; every entry is a file that exists)
urls = ''.join(f"  <url><loc>{page_url(p)}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for p in built if not p.get('noindex'))
w('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
w('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
w('site.webmanifest', json.dumps({
    'name': NAME, 'short_name': 'GLS', 'description': 'Refrigeration and air-conditioning installation, repair and maintenance.',
    'start_url': '/', 'scope': '/', 'display': 'browser', 'lang': 'en-ZA',
    'background_color': '#e3e8ea', 'theme_color': '#15252f',
    'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=2) + '\n')

w('llms.txt', f'''# {NAME}

> GLS installs, repairs and maintains refrigeration and air-conditioning systems for homes and businesses in Johannesburg and surrounding areas. It is a registered company ({LEGAL}), operating since {FOUNDED}, based in Primrose, Germiston, South Africa. Emergency repair is available 24 hours a day, 7 days a week.

## Key facts
- Business: refrigeration and air-conditioning contractor (installation, maintenance, repair, upgrades, consultation)
- Founded: {FOUNDED}
- Address: {ADDRESS_LINE}, South Africa
- Area served: Johannesburg and surrounding areas
- Phone (calls): {CALL_DISPLAY} ({CALL})
- WhatsApp: {WA_DISPLAY} (+{WA})
- Email: {EMAIL}
- Customers: homes, offices, restaurants, supermarkets and other commercial and industrial properties
- Quotes: upfront, no hidden fees. Free site assessments available.

## Services
- [Air-conditioning installation, servicing and repair]({DOMAIN}/air-conditioning.html): split-unit and ducted systems, server room cooling, inverter and energy-efficient upgrades
- [Commercial refrigeration, cold rooms and walk-in freezers]({DOMAIN}/commercial-refrigeration.html): installation, servicing and repair for restaurants, supermarkets and retail
- [Planned maintenance]({DOMAIN}/maintenance.html): inspections, filter cleaning, refrigerant level and wiring checks, performance optimisation
- [All services]({DOMAIN}/services.html)

## Company
- [About GLS]({DOMAIN}/about.html)
- [Our work]({DOMAIN}/our-work.html): photographs and video from jobs
- [Contact]({DOMAIN}/contact.html): call, WhatsApp, email, directions

## Website
Designed and developed by {COR3['name']} ({COR3['url']}), founded by {COR3['founder']}. {COR3['name']} is the website developer, not part of GLS's business.
''')

w('humans.txt', f'''/* TEAM */
Business: {LEGAL}
Site: {DOMAIN}/
Location: Primrose, Germiston, South Africa

/* SITE CREDITS */
Design and development: {COR3['name']}
Agency site: {COR3['url']}
Founder of {COR3['name']}: {COR3['founder']}
Contact: {COR3['url']}

/* TECHNOLOGY */
Static HTML, CSS and vanilla JavaScript plus GSAP for entrance animation. No frameworks, no tracking scripts.
Typeface: Instrument Sans (SIL Open Font License), self-hosted.
Animation: GSAP 3 and ScrollTrigger (GSAP Standard 'no charge' license), self-hosted, loaded after page load.
Last update: {TODAY.isoformat()}
''')
print('built', [p['file'] for p in built])
for p in built:
    print(f"{p['file']:32s} title {len(p['title']):2d}  desc {len(p['desc']):3d}")
