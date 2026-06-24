# Performance / Core Web Vitals Audit — aa.co.nz/membership/
**Score: 42/100 (estimated — PSI API quota exhausted; scores based on source analysis + HTTP timing)**
**Date: 24 June 2026**

## What Works
- TTFB excellent: Cloudflare CDN with NZ edge (AKL), sub-100ms across all key pages
- Cache-Control: max-age=300, HIT responses confirmed
- GTM loaded asynchronously (acceptable)
- reCAPTCHA loaded with async defer (acceptable)

## Real TTFB Data (curl measurements)
| Page | TTFB | Total Transfer | HTML Size | Status |
|------|------|----------------|-----------|--------|
| /membership/ | 71ms | 113ms | 213 KB | 200 |
| /membership/options-and-fees/ | 108ms | 138ms | 203 KB | 200 |
| /membership/join-aa/ | 51ms | 79ms | 169 KB | 200 |
| /membership/roadservice-breakdown-assistance/ | 53ms | 75ms | 194 KB | 200 |

## Estimated CWV (Source-Pattern Based)
| Metric | Estimate | Target | Status |
|--------|----------|--------|--------|
| LCP | 4.0-6.0s | < 2.5s | POOR |
| INP | 150-250ms | < 200ms | Borderline |
| CLS | < 0.1 | < 0.1 | Likely PASS |
| FCP | 2.0-3.5s | < 1.8s | POOR |
| TTFB | < 100ms | < 800ms | PASS |
| Lighthouse Mobile (est.) | 35-50 | >90 | POOR |

## Critical Issues

**P1. 9 synchronous render-blocking scripts on all pages**
All 9 scripts load without `async` or `defer` — browser cannot render until all fully download and execute:
- `clientlib-dependencies` (zero-byte file — still incurs blocking round-trip)
- `map/clientlibs` — loaded on ALL pages including those with no map
- `granite/jquery` + `foundation/clientlibs/jquery` — jQuery loaded TWICE in blocking position
- `clientlib-site`, `clientlib-react`
- `https://staticcdn.co.nz/embed/embed.js` — Shielded Site badge, synchronous, cross-origin, no defer
- `granite/utils`, `granite/jquery/granite`

Estimated LCP impact: +800ms to +1500ms

**P2. Hero/LCP image rendered via JS, invisible to browser preload scanner**
Hero banner (`Membership-hero-banner_FINAL.jpg`) is injected by AEM's `data-cmp-hook-image="imageV3"` JavaScript component — not a native `<img>`. Browser cannot discover it during HTML parsing. LCP image only loads after the entire blocking script chain completes.

## High Issues

**P3. No fetchpriority or preload hints on any page**
Zero instances of `fetchpriority="high"` or `<link rel="preload">` across all 4 tested pages.

**P4. Images missing explicit width/height (CLS risk)**
| Page | Images missing WH | Total |
|------|-------------------|-------|
| /membership/ | 14/22 | High |
| /options-and-fees/ | 10/17 | High |
| /join-aa/ | 10/11 | High |
| /roadservice/ | 13/19 | High |
Header/footer SVG icons and app store badges load without reserved space — potential CLS contributors.

**P5. AEM content images use JS-driven lazy loading**
Main content images use `data-cmp-src="{.width}"` JavaScript pattern — not discoverable by browser preload scanner at all. Even above-fold images wait for JS execution.

## Medium Issues

**P6. clientlib-react loaded globally on all pages** — including static pages that don't use React. Unnecessary main-thread parse/execute.

**P7. map/clientlibs loaded on all pages** — including pages with no map component. Classic AEM clientlib scoping issue.

**P8. No next-gen image formats (WebP/AVIF)** — all images served as JPEG/PNG. AEM image servlet supports WebP via format negotiation but not enabled.

**P9. Third-party scripts adding TBT** — Hotjar, Intercom, Facebook Connect, Reddit, Optmonster fire via GTM.

## Prioritised Fixes
| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| 1 | Add `defer` to all 9 blocking scripts; move non-critical to body end | LCP -800ms to -1500ms | Medium |
| 2 | Preload hero with `<link rel="preload as="image">` + `fetchpriority="high"` | LCP -500ms to -1000ms | Low |
| 3 | Add `defer` to `staticcdn.co.nz/embed.js` | TBT reduction | Low |
| 4 | Descope map/clientlibs + clientlib-react to pages that need them | TBT -200ms to -500ms | Medium |
| 5 | Enable WebP from AEM image servlet; add `<picture>` with WebP source | LCP image size -30-50% | Medium |
| 6 | Add explicit `width`/`height` on all `<img>` tags | CLS stabilisation | Low |
| 7 | Replace JS-driven above-fold images with native `<img loading="eager">` | LCP discovery fix | Medium |
| 8 | Consolidate duplicate jQuery bundles | JS parse time -minor | Low |

**Expected outcome after items 1-4:** Lighthouse mobile score from 35-50 range → 65-80 range.
