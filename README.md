# GLS Refrigeration & Air Conditioning: website

Designed and developed by [COR3 Haus Production](https://cor3hausproduction.com/).
Live domain: https://glsrefrigeration.co.za (apex is canonical; `www` must also resolve).

## What the website has and does

**Pages (9)**
| File | Purpose |
|---|---|
| `index.html` | Introduces GLS; fault triage ("What's not keeping cold?"); services overview; work strip; why GLS |
| `services.html` | Hub for all six service areas, FAQ |
| `air-conditioning.html` | Installation, servicing, emergency repair, upgrades, free site assessment; FAQ |
| `commercial-refrigeration.html` | Commercial units, cold rooms and walk-in freezers, maintenance, repair; FAQ |
| `maintenance.html` | Planned maintenance scope; FAQ |
| `our-work.html` | 23 real job photographs in four subject groups with a lightbox, and 4 short videos (video loads only on play) |
| `about.html` | Approach, mission, vision, why GLS, company details |
| `contact.html` | Call / WhatsApp / email / address, enquiry form, directions chooser |
| `404.html` | Not-found page (noindex) |

**Interactive features** (all in `assets/js/main.js`, no dependencies)
1. Mobile navigation drawer: accessible toggle, Escape, outside tap, link click, resize and back-button reset, scroll lock, focus trap. Without JavaScript the nav stays a visible list.
2. Map chooser: any "Get directions" link opens a dialog offering Google Maps, Apple Maps or Waze. Without JavaScript the link opens Google Maps.
3. Fault triage on the homepage: tells the visitor what to send GLS, then offers WhatsApp (pre-filled), call, and the relevant service page.
4. Enquiry form: validates, then opens WhatsApp (+27 71 934 2182) with the message ready. It never claims the message was sent. Email fallback link included. Supports `?issue=` and `?service=consultation` pre-fill.
5. Videos: only one plays at a time; nothing downloads until play.
6. Gallery lightbox (Our work): click a photograph to enlarge; arrow keys, Escape, focus return.
7. Motion (`assets/js/motion.js`, GSAP 3 + ScrollTrigger, self-hosted): quiet scroll reveals and image reveals. Loaded after the page `load` event so it never delays first paint. Not started for `prefers-reduced-motion` users; content is never left hidden if the scripts fail (see `_docs/DESIGN-DIRECTION.md`).

**SEO / discoverability**: unique title, description and canonical per page; Open Graph and Twitter cards; JSON-LD (HVACBusiness, WebSite, WebPage, BreadcrumbList, Service, FAQPage); `sitemap.xml`, `robots.txt`, `llms.txt`, `humans.txt`, `site.webmanifest`, favicons.

## Structure
```
*.html                 generated pages (do not hand-edit; edit _build/build.py)
assets/css/main.css    the only stylesheet
assets/js/main.js      all behaviour (nav, forms, maps, triage, lightbox)
assets/js/motion.js    GSAP entrance animation only
assets/js/vendor/      gsap.min.js, ScrollTrigger.min.js + licence note
assets/img/            optimised WebP, logo, sprite.svg, OG card, video posters
assets/video/          compressed MP4
assets/fonts/          Instrument Sans variable (SIL OFL) + licence
_build/build.py        generates all pages, sitemap, robots, llms, humans, manifest
_build/make_media.py   regenerates images, favicons, OG card from the original files
_build/check_site.py   static QA (links, anchors, assets, metadata, JSON-LD)
_docs/QA-REPORT.md     test results and open items
_docs/DESIGN-DIRECTION.md  art direction, type scale, motion rules
```
`_build` and `_docs` start with an underscore, so GitHub Pages (Jekyll) does not publish them.

## Change contact details or copy
Edit the constants at the top of `_build/build.py` (numbers, address, email) or the page functions, then run:
```
python3 _build/build.py && python3 _build/check_site.py
```
Requires Python 3 and Pillow. `make_media.py` also needs the original photos and ffmpeg; it is only needed when images change.

## Placement comments
Search the generated HTML for `IMAGE PLACEMENT`, `LOGO PLACEMENT`, `VIDEO PLACEMENT`, `MAP`, `ATTRIBUTION` and `FUTURE INTEGRATION`.

## Deployment (GitHub Pages)
- Keep the `CNAME` file (`glsrefrigeration.co.za`).
- DNS: apex A/ALIAS records to GitHub Pages, and a `www` CNAME to the Pages host, so both addresses work. GitHub redirects `www` to the apex; canonical tags point to the apex.
- GitHub Pages cannot set server redirects or headers. Existing page filenames are unchanged, so old URLs keep working.
- The old mirror `j24y-k.github.io/GLS` was indexed by search engines. With the custom domain set, GitHub redirects it to the domain.

## Future integrations
- Server-side email or CRM logging for enquiries (the form currently delivers by WhatsApp only, as decided).
- Google Business Profile and any real social profiles: add to `sameAs` in `business_node()` once they exist.
- Verified reviews or testimonials: none are included because none were supplied.
