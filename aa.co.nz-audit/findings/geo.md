# GEO / AI Search Readiness Audit — aa.co.nz/membership/
**Score: 38/100**
**Date: 24 June 2026**

## Score Breakdown
| Dimension | Weight | Raw | Weighted |
|---|---|---|---|
| Citability | 25% | 42/100 | 10.5 |
| Structural Readability | 20% | 35/100 | 7.0 |
| Multi-Modal Content | 15% | 30/100 | 4.5 |
| Authority & Brand Signals | 20% | 55/100 | 11.0 |
| Technical Accessibility | 20% | 25/100 | 5.0 |
| **Total** | | | **38/100** |

## What Works
- AA is a well-established Wikipedia entity (1.7M members, founded 1903, FIA affiliation)
- All AI crawlers permitted (GPTBot, ClaudeBot, PerplexityBot, anthropic-ai all allowed by wildcard)
- Server-side rendering confirmed — core content visible pre-JS
- Strong brand authority signals (120+ years, 1M+ members, "we rescue a Kiwi every minute")
- Pricing data present on options-and-fees pages (partially citable)
- Specific benefit discounts with percentages present on benefits page

## AI Crawler Access
| Crawler | Status |
|---|---|
| Googlebot | Allowed |
| GPTBot | Allowed |
| ClaudeBot | Allowed |
| PerplexityBot | Allowed |
| anthropic-ai | Allowed |
| SemrushBot | Blocked |

## llms.txt Status
**MISSING — HTTP 404**. No machine-readable content manifest for AI systems.

## Citability by Query
| Query | Score | Issue |
|---|---|---|
| "How much does AA NZ membership cost?" | 55/100 | Prices in promo copy, no table headers, no FAQPage schema |
| "What does AA roadside assistance cover NZ?" | 48/100 | /what-we-cover/ returns 404; coverage fragmented across pages |
| "Is AA membership worth it NZ?" | 35/100 | No value-summary page; no testimonials/reviews |
| "How do I join AA NZ?" | 30/100 | Join page is CTA wrapper only; no step-by-step instructions |
| "AA Plus vs standard — what's the difference?" | 58/100 | Specific $ limits present but no side-by-side comparison table |

## Platform Visibility Estimates
| Platform | Score | Reason |
|---|---|---|
| Google AI Overviews | 32/100 | No schema, no meta descs, 404s on key sub-pages |
| ChatGPT | 40/100 | Wikipedia entity strong; live search citations limited |
| Perplexity | 35/100 | SSR accessible; fragmented passages dilute answer quality |
| Bing Copilot | 30/100 | Weights structured data heavily; near-zero schema |

## Critical Issues
**C1. 404 errors on linked sub-pages**
- Affected: /roadservice-breakdown-assistance/what-we-cover/, /options-and-fees/standard/, /options-and-fees/youth/, /roadservice-breakdown-assistance/callouts/
- Impact: AI crawlers cannot index these pages; "what we cover" is the primary answer source for highest-volume query
- Fix: Audit all /membership/ sub-pages for 404s, fix redirects or restore content

**C2. No schema markup on any page**
- Zero JSON-LD/microdata across entire /membership/ section
- Priority: FAQPage, Service+PriceSpecification, Organization, BreadcrumbList
- Effort: Medium (1-2 dev days)

**C3. No meta descriptions on any crawled page**
- Reduces probability of Google correctly associating pages with query intent
- Effort: Low (content team only)

**C4. No general membership FAQ page**
- Only FAQ page is about discontinued Smartfuel card
- Need: /membership/faq/ with 15-20 Q&A pairs
- Effort: Low

## High Issues
**H1.** Pricing not in structured extractable format (no table with column headers)
**H2.** "Covers you, not vehicle" + stand-down period facts fragmented across pages
**H3.** llms.txt missing
**H4.** No "worth it" / value summary page targeting evaluative queries
**H5.** Three 0800 numbers without clear primary contact designation

## Medium Issues
**M1.** Accordion FAQ content may not be crawler-accessible (JS-dependent)
**M2.** Passage length not optimised — needs inverted pyramid structure
**M3.** 1.7M member figure lives on Wikipedia, not on aa.co.nz
**M4.** Associate/Youth membership 404 pages
**M5.** No Standard vs AA Plus comparison table

## Low Issues
**L1.** No YouTube-linked content from membership pages
**L2.** No structured review/rating content (AggregateRating schema)
**L3.** Wikipedia article has citation gaps (flagged July 2023)
**L4.** No RSL 1.0 licensing declaration in llms.txt

## Top 5 GEO Actions (by ROI)
1. Fix 404 errors on key sub-pages
2. Implement FAQPage + Service + PriceSpecification + Organization schema
3. Create /membership/faq/ (15-20 Q&A pairs)
4. Add meta descriptions to all /membership/ pages
5. Create /llms.txt
