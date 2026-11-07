# GLS website: QA report (design upgrade v2)

Date: 2026-11-03. Tools: Chromium (Playwright 1.56) over local HTTP, Lighthouse (mobile profile, simulated throttling), html-validate, `_build/check_site.py`.

## Lighthouse (mobile) against the previous baseline
| Page | Performance (baseline) | Performance (now) | Accessibility | Best practices | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|---|
| index.html | 96 | 99 | 100 | 100 | 100 | 2.0 s | 0 | 0 ms |
| services.html | 98 | 98 | 100 | 100 | 100 | 2.2 s | 0 | 70 ms |
| air-conditioning.html | 98 | 98 | 100 | 100 | 100 | 2.4 s | 0 | 30 ms |
| commercial-refrigeration.html | 98 | 99 | 100 | 100 | 100 | 2.0 s | 0 | 10 ms |
| maintenance.html | 98 | 100 | 100 | 100 | 100 | 1.9 s | 0 | 0 ms |
| our-work.html | 89 | 98 | 100 | 100 | 100 | 1.1 s | 0 | 180 ms |
| about.html | 98 | 98 | 100 | 100 | 100 | 2.3 s | 0 | 40 ms |
| contact.html | 100 | 100 | 100 | 100 | 100 | 1.1 s | 0 | 0 ms |

Notes
- Accessibility, best practices and SEO are 100 on every page.
- The first redesign build dropped the homepage to 87. Investigation found two causes: a 2-second scale tween on the full-bleed hero photograph (the LCP element) and GSAP executing before first paint. Fixes: hero photograph no longer animated; hero copy entrance is CSS-only; GSAP loads after the `load` event. Final scores are above baseline.
- Lighthouse runs against a local server without gzip; real transfer sizes will be smaller.

## Regression results (final build)
| Area | Result |
|---|---|
| Hamburger menu | 190 of 190 assertions (7 phone/tablet widths with touch, 5 desktop widths, no-JS fallback) |
| Layout / console / network | 0 problems across 90 page-width combinations (9 pages x 10 widths, 320 to 1920px); no horizontal overflow, no console errors, no failed requests |
| Forms, map chooser, triage, video attributes | 36 of 37 (see limitation) |
| Motion, lightbox, typography | 46 of 46: all reveals complete visible; reduced-motion shows everything immediately and never starts GSAP; GSAP blocked and all-scripts-blocked cases reveal content; lightbox opens, navigates, closes and returns focus; largest text 41.6px desktop, 28.2px phone |
| HTML validity | html-validate: 0 errors on 9 pages |
| Static checks | 0 broken links, anchors or assets; unique titles and descriptions; canonical, sitemap and JSON-LD consistent; COR3 attribution present |
| Visual review | Every page reviewed at desktop and phone widths after rendering; four defects found and fixed (hidden images from a `clearProps` bug, lone gallery tile on phones, stray inline-fact divider, footer divider overshoot), plus a dark photo replaced on Contact |

## Not verified
- Video playback: the sandbox browser has no H.264 decoder (the one failing assertion). Files decode cleanly in ffmpeg. Play one on a real phone.
- WhatsApp app itself, map pins, real iOS/Android devices, Google's Rich Results Test.
- Reference sites: see `_docs/DESIGN-DIRECTION.md`. NMG Zembeta and MB FILMZ could not be inspected beyond metadata.

## Preserved unchanged
Navigation and hamburger code, form validation and WhatsApp hand-off, tel/mailto links, map chooser, video behaviour, internal links, SEO metadata, structured data, canonicals, sitemap, robots, llms.txt, humans.txt (credits updated), manifest and favicons, responsive images, COR3 attribution.

## Still needs client confirmation
Street spelling "Churchill", postal code, map pins, ownership/licence of the two studio-quality hero photographs, service area beyond Johannesburg and Germiston, DNS `www` CNAME. Details in the previous report and README.
