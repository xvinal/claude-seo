# Technical SEO Audit — aa.co.nz/membership/
**Score: 61/100**
**Platform: Adobe Experience Manager (AEM) on Cloudflare CDN**
**Date: 24 June 2026**

## Score Breakdown
| Category | Score |
|----------|-------|
| Crawlability | 90/100 |
| Indexability | 72/100 |
| Security / Headers | 58/100 |
| URL Structure | 85/100 |
| Mobile | 80/100 |
| Core Web Vitals (signal) | 55/100 |
| Structured Data | 70/100 |
| Open Graph / Social | 35/100 |
| Title Tags | 65/100 |
| Meta Descriptions | 68/100 |
| **Composite** | **61/100** |

## What Works
- HTTPS enforced with 301 redirect; HSTS `max-age=63072000; includeSubdomains`
- No noindex signals on any of 29 in-scope pages
- No redirect chains — all 200 OK responses direct
- Viewport meta tag present on all pages
- Microdata BreadcrumbList implemented throughout
- Responsive images with srcset (320w–1600w AEM-generated)
- All 29 in-scope pages in sitemap with ISO 8601 lastmod
- robots.txt minimal/appropriate for AEM (only /content/experience-fragments/ blocked)
- CSP, X-Frame-Options, X-Content-Type-Options present
- Clean URL structure: lowercase, hyphens, trailing slashes, 3-4 levels max
- Global megamenu links to most key /membership/ pages

## Critical Issues

**C1. Canonical tags are relative, not absolute (all 29 pages)**
- Evidence: `<link rel="canonical" href="/membership/"/>` — path-only, not absolute
- Fix: AEM Externalizer OSGi config — set publish runmode domain to `https://www.aa.co.nz`
- Effort: Low (single config change)

**C2. og:image uses relative paths (social sharing broken)**
- Evidence: og:image = "/content/dam/nzaa/02-services/membership/..." (relative)
- Several pages (join-aa, options-and-fees) fall back to logo SVG instead of page-relevant image
- Fix: Same Externalizer config as C1 + audit fallback og:image assignments

**C3. og:url absent across all pages**
- Without og:url, UTM-tracked shares fragment social link equity
- Fix: Add `<meta property="og:url">` wired to Externalizer-resolved canonical

## High Issues

**H1. Meta description issues**
- /membership/options-and-fees/youth-membership/ — meta description and og:title both empty
- /membership/join-aa/ — description is seasonal: "This summer, drive with confidence..." (stale year-round)
- Fix: Write evergreen descriptions; fix empty og:title on youth-membership

**H2. Title tag quality issues (5 pages)**
| Page | Title | Chars | Issue |
|------|-------|-------|-------|
| /membership/join-aa/ | Join AA | 7 | Critically short |
| /membership/renew/ | Renew your AA Membership | 24 | Short, no differentiator |
| /membership/cardreplacement/ | Card Replacement | 16 | Generic, no brand |
| /membership/new-card-faqs/ | AA Membership New Card - FAQs | 29 | Low keyword value |
| /membership/options-and-fees/priceincrease/ | Membership Price Increase | 25 | Stale 2023 event |
- Suggested: join-aa → "Join AA New Zealand | Roadside Assistance Membership" (51 chars)
- Suggested: renew → "Renew AA Membership | NZ Automobile Association" (47 chars)
- Suggested: cardreplacement → "Replace Your AA Membership Card | AA New Zealand" (48 chars)

**H3. /membership/options-and-fees/priceincrease/ — stale indexed page**
- Meta description: "Find out about the AA Membership price increase effective from August 1, 2023"
- Sitemap lastmod: 2026-01-21 (template touch, not content update)
- Fix: 301 redirect to /options-and-fees/ OR update content + meta; or noindex + remove from sitemap

**H4. /roadservice-breakdown-assistance/business/ topical duplication with /business/**
- Both pages target business fleet roadside assistance; neither canonicals to the other
- Fix: Consolidate or tighten topic scoping; redirect /roadservice/business/ to /membership/business/aa-business-care/

## Medium Issues

**M1. Meta description lengths too short (3 pages)**
| Page | Desc Length | Target |
|------|-------------|--------|
| /membership/benefits-and-discounts/ | 55 chars | 120-155 |
| /membership/roadservice-breakdown-assistance/ | 69 chars | 120-155 |
| /membership/cardreplacement/ | 64 chars | 120-155 |

**M2. All hero images use loading="lazy" including LCP candidates**
- No `fetchpriority="high"` or `<link rel="preload">` on any above-fold image
- First hero on /membership/ is 1563x1458px JPEG loaded lazily — confirmed LCP risk
- Fix: Add `loading="eager"` + `fetchpriority="high"` to above-fold hero per page (AEM Image core component supports this)

**M3. og:type and og:locale absent sitewide**
- No og:type declared (should be `website`)
- No og:locale (defaulting to en_US; should be `en_NZ`)
- Fix: Add to AEM base page template

**M4. No Twitter Card / X meta tags**
- Fix: Add `twitter:card`, `twitter:site` to AEM template

**M5. CSP weak: `unsafe-inline` + `unsafe-eval` in script-src; no style-src**
- Adobe Launch/DTM dependency requires unsafe-inline; mitigate with nonce-based CSP where possible
- Add `Referrer-Policy: strict-origin-when-cross-origin` and `Permissions-Policy` header via Cloudflare

**M6. Sitemap architecture: single-entry sitemapindex**
- /sitemap.xml → /.sitemap.xml only (adds resolution step, no segmentation benefit)
- Fix: Flatten to single sitemap or segment into logical sub-sitemaps by section

## Low Issues
- L1. Hreflang absent — correct for single NZ English market; no action needed
- L2. /join-aa/ H1 is campaign slogan "We've got you." — change to keyword-bearing heading
- L3. /cardreplacement/ URL is camelCase run-on — redirect to /card-replacement/ if feasible
- L4. IndexNow not detected — enable Cloudflare native integration or use indexnow_submit.py
- L5. priceincrease/ lastmod reflects template touch not content update — audit AEM JCR modification triggers

## Top 5 Fixes (Effort vs. Impact)
1. Fix canonical + og:image + og:url to absolute URLs (single AEM Externalizer config change)
2. Rewrite join-aa title + H1 (highest-intent page, 7-char title)
3. Add `fetchpriority="high"` to hero images (LCP risk on all hub pages)
4. Address priceincrease/ page (redirect or update)
5. Write missing meta descriptions for 5 pages
