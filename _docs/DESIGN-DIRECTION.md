# GLS website: art direction (v2)

## Concept
Daylight and equipment. A dark header and footer bookend a light page. Photography carries the weight; type stays small and precise. Structure comes from spacing and hairlines, not boxes. Existing brand colours are unchanged: blue marks system/links, red is reserved for the urgent call action.

## Type scale (Instrument Sans, one family, weights 400 to 700)
| Use | Size |
|---|---|
| Hero heading | 28px (phone) to 41.6px (desktop) |
| Section heading | 23px to 32px |
| Sub-heading | 17px |
| Body | 15px, line-height 1.65 |
| Navigation, buttons, links | 13px |
| Captions, notes | 12px |
| Labels | 11px, tracked, uppercase, used once per section |
Measured largest text on the whole site: 41.6px (1440px viewport), 28.2px (390px viewport). Previous version: about 74px.

## Layout principles
- Hero: full-bleed photograph, copy set low-left, triage sheet overlapping the hero base (the only shadow on the site).
- Services on the home page: image-led editorial rows, alternating sides. Inner pages: hairline rows.
- Work: grouped mosaic (four subject groups, sticky labels, varied spans) with a lightbox; dark mosaic teaser on the home page.
- No bordered boxes, no caption bars, no card grids. Images are borderless with a 2px radius.
- Mobile is composed separately: single column, overlap pair, promoted full-width tiles so no gallery row is left half empty.

## Motion rules
- GSAP 3 + ScrollTrigger: text reveals and image clip reveals, once, as sections enter. No parallax, no scroll-jacking, no looping effects.
- Hero copy entrance is CSS-only and transform-only so text is visible on the first frame.
- Hero photograph is deliberately not animated: tweening the largest element cost ~2s of LCP in lab testing.
- Hidden start states exist only under `html.anim`. That class is never set for reduced-motion users, is removed if GSAP fails to load, and is removed by a 4-second timer if scripts are blocked entirely. All three cases are tested.

## Distinct from the reference sites
The reference sites publish dark theme colours (MUBS `#1b1b1b`, MB FILMZ `#080808`). GLS is deliberately a light, daylight page with dark bookends, a different typeface, and a photography-and-hairline composition.

## What was and was not inspected
- MUBS: page text and structure read through a text fetch. No rendering.
- NMG Zembeta and MB FILMZ: only page metadata was retrievable (both build their pages in the browser). Their layouts, typography and animation were NOT inspected. The sandbox has no route to external sites, so none of the three could be rendered or scrolled.
