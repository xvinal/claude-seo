# SXO (Search Experience Optimization) Audit — aa.co.nz/membership/
**Score: 54/100**
**Date: 24 June 2026**

## Score Breakdown
| Dimension | Score |
|-----------|-------|
| Page Type Match | 8/15 |
| Content Depth | 9/15 |
| UX Signals | 7/15 |
| Schema | 5/15 |
| Media | 9/15 |
| Authority | 10/15 |
| Freshness | 6/10 |
| **Total** | **54/100** |

## PRIMARY FINDING: Critical Page-Type Mismatch on /join-aa/

`/membership/join-aa/` ranks for decision-stage "join AA NZ" intent but delivers brand awareness content ("We've got you.") with no pricing, no tier selector, no inline purchase flow.

## SERP Analysis

| # | Result | Page Type | Signal |
|---|--------|-----------|--------|
| 1-3 | AA membership pages | Hybrid Service/Content | AA owns top 3 |
| 4 | MoneyHub review | Blog Post | "Is it worth it" evaluative |
| 5 | Frugal Kiwi | Blog Post | Cost analysis |
| 6 | Canstar NZ | Comparison Page | Provider matrix |
| 7 | AutoTrader NZ | Comparison Page | Side-by-side |
| 9 | cheapies.nz forum | UGC | Skeptical community |
| 10 | Consumer NZ | Comparison Page | Independent review |

**SERP consensus:** 60% evaluative/comparison, 30% transactional, 10% navigational. Third parties own positions 4-10 for consideration-stage queries.

## Search Intent Alignment

| Page | Query Intent | Page Type | Mismatch |
|------|-------------|-----------|----------|
| /membership/ | Mixed info + transactional | Hybrid | ALIGNED |
| /membership/options-and-fees/ | Transactional: pricing | Product (partial) | MEDIUM |
| /membership/aa-plus/ | "Is AA Plus worth it?" | Brochure | MEDIUM |
| /membership/benefits-and-discounts/ | Benefit research | Service | MEDIUM |
| /membership/roadservice/ | Awareness + transactional | Hybrid | ALIGNED |
| /membership/join-aa/ | Transactional: decision stage | Brand story | CRITICAL |
| /membership/renew/ | Transactional: retention | Informational | HIGH |

## User Stories (SERP-derived)

1. **New Driver (Awareness→Consideration):** Wants to know if $89 is worth it vs insurer add-on. Blocked: no value-comparison page on AA's site; third parties answer this.
2. **Stranded Driver (Decision):** Needs emergency join at 9pm. Blocked: /join-aa/ shows brand copy, not pricing or emergency join path.
3. **Comparison Researcher (Consideration):** Has insurer's $40 roadside add-on, wants to compare. Blocked: no AA page compares AA to alternatives.
4. **Long-term Member (Retention):** Wants to renew in 2 minutes. Blocked: renewal page shows no pricing, requires login or phone.
5. **Business Owner (B2B):** Wants fleet cover. Blocked: no B2B path from consumer /membership/ hub.

## Persona Scores

### /membership/ Hub Page
| Persona | Relevance | Clarity | Trust | Action | Total |
|---------|-----------|---------|-------|--------|-------|
| New Driver | 18/25 | 15/25 | 12/25 | 14/25 | 59/100 |
| Existing Member Upgrading | 14/25 | 12/25 | 13/25 | 12/25 | 51/100 |
| Fleet/Business Owner | 8/25 | 6/25 | 10/25 | 5/25 | 29/100 |
| Lapsed Member | 10/25 | 8/25 | 14/25 | 10/25 | 42/100 |

### /membership/join-aa/ Conversion Page
| Persona | Relevance | Clarity | Trust | Action | Total |
|---------|-----------|---------|-------|--------|-------|
| New Driver | 12/25 | 8/25 | 10/25 | 10/25 | 40/100 |
| Existing Member | 6/25 | 5/25 | 8/25 | 7/25 | 26/100 |
| Fleet/Business Owner | 5/25 | 4/25 | 6/25 | 4/25 | 19/100 |
| Lapsed Member | 8/25 | 5/25 | 9/25 | 8/25 | 30/100 |

## Above-Fold Analysis
| Page | CTA above fold | Price above fold | Trust signal | Assessment |
|------|---------------|-----------------|--------------|------------|
| /membership/ | Yes | Yes ($89) | Award claim | PASS |
| /options-and-fees/ | Yes | Yes (full table) | Loyalty discount | PASS |
| /roadservice/ | Yes | Yes | Kiwi/min stat | PASS (best page) |
| /join-aa/ | Yes (wrong goal) | NO | Brand character | FAIL |
| /renew/ | Yes | NO | Loyalty message | FAIL |
| /benefits-and-discounts/ | Login CTA only | No | "45 ways" | FAIL |

## Funnel Coherence
| Stage | Page | Match | Conversion Clarity | Score |
|-------|------|-------|-------------------|-------|
| Awareness | /roadservice/ | Aligned | Good | 75/100 |
| Consideration | None (GAP) | Missing | Ceded to 3rd parties | 0/100 |
| Decision | /join-aa/ | CRITICAL mismatch | Very poor | 28/100 |
| Retention | /renew/ | HIGH mismatch | Poor | 35/100 |

## Critical Issues

**C1. /join-aa/ page-type mismatch (decision page delivers brand story)**
Fix: Rebuild as conversion LP: H1 "Join AA – From $89/Year", inline tier selector, pricing on page, 1-click to payment. Emergency join path ($209) above fold.

**C2. No consideration-stage page (SERP positions 4-10 owned by third parties)**
Fix: Create /membership/is-aa-membership-worth-it/ — honest cost breakdown, value calculator, AA vs insurer comparison, testimonials, FAQPage schema.

**C3. No schema on pricing/options pages**
Fix: Product schema on tier pages, FAQPage schema on hub, Service schema on roadservice.

## High Issues

**H1.** /renew/ has no inline pricing or 1-click renewal — login wall blocks lapsed members
**H2.** /benefits-and-discounts/ has no conversion CTA — strongest consideration page converts zero
**H3.** H1 on /join-aa/ = "We've got you." → change to "Join AA – NZ's Largest Motoring Association"
**H4.** No meta description on /membership/ hub — Google auto-generates potentially weak snippet
**H5.** Business path invisible from consumer funnel — no B2B module on /membership/ hub

## Medium Issues
**M1.** No "AA vs alternatives" comparison content — third parties own this query space
**M2.** AA Plus page lacks "when it pays for itself" value justification  
**M3.** AA app promoted before value pitch complete (above fold on hub)
**M4.** No urgency/scarcity signals on any page
**M5.** Tier pages don't cross-link horizontally

## Top 10 SXO Recommendations
1. Rebuild /join-aa/ as conversion landing page (inline pricing + tier selector)
2. Create /membership/is-aa-membership-worth-it/ consideration-stage hub
3. Implement schema: Product, FAQPage, Service, BreadcrumbList
4. Fix /renew/ — show pricing, 1-click renewal, reframe loyalty message positively
5. Add conversion CTAs throughout /benefits-and-discounts/
6. Rewrite H1 on join-aa, renew, and aa-plus pages
7. Surface B2B path from /membership/ hub
8. Add "AA Plus worth it" value section with cost math
9. Add meta descriptions with pricing hooks to all pages
10. Cross-link tier pages horizontally
