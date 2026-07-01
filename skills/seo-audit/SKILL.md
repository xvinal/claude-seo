---
name: seo-audit
description: "Full website SEO audit with parallel subagent delegation. Crawls up to 500 pages, detects business type, delegates to up to 15 specialists (8 always + 7 conditional), generates health score. Use when user says audit, full SEO check, analyze my site, or website health check."
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.2.0"
  category: seo
---

# Full Website SEO Audit

## Process

0. **Preflight Check** — run ALL checks before doing anything else. If any **required** check fails, print the diagnostic table and ABORT immediately. Do not crawl, do not spawn subagents.

   **Required (abort if any fail):**
   | Tool | Check |
   |------|-------|
   | Google API | `python3 scripts/google_auth.py --check --json` → `tier.tier >= 0` |
   | Firecrawl MCP | `firecrawl_map` present in active tool list |
   | DataForSEO MCP | `dataforseo_serp_google_organic_live_advanced` present in active tool list |
   | Playwright | `python3 scripts/capture_screenshot.py --check` exits 0 |
   | Semrush MCP | `mcp__claude_ai_Semrush__execute_report` present in active tool list |

   **Optional (warn only, continue):**
   | Tool | Check |
   |------|-------|
   | Moz API | `python3 scripts/backlinks_auth.py --check --json` → `services.moz.available = true` |
   | Bing Webmaster | same → `services.bing.available = true` |

   **On any required failure**, output this table and stop:
   ```
   ⛔ Preflight failed — audit cannot proceed.

   | Tool           | Required | Status  | Fix                                                        |
   |----------------|----------|---------|------------------------------------------------------------|
   | Google API     | ✅ Yes   | ❌ FAIL | Add api_key to ~/.config/claude-seo/google-api.json        |
   | Firecrawl MCP  | ✅ Yes   | ❌ FAIL | Run .\extensions\firecrawl\install.ps1 then restart Claude |
   | DataForSEO MCP | ✅ Yes   | ❌ FAIL | Run .\extensions\dataforseo\install.ps1 then restart Claude|
   | Playwright     | ✅ Yes   | ❌ FAIL | pip install playwright && playwright install chromium       |
   | Semrush MCP    | ✅ Yes   | ❌ FAIL | Connect Semrush MCP in Claude settings                     |
   | Moz API        | Optional | ⚠ WARN  | Add moz_api_key to ~/.config/claude-seo/backlinks-api.json |
   | Bing Webmaster | Optional | ⚠ WARN  | Add bing_api_key + fix bing_verified_sites URL format      |

   Fix the ❌ items above and re-run /seo audit.
   ```

   **On all required passing**, output:
   ```
   ✅ Preflight passed (5/5 required ready[, ⚠ N/2 optional unavailable — backlink data limited])
   ```
   Then proceed.

1. **Load site context**: before any analysis, check for `contexts/{domain}/_site.md`. If it exists, load it as global brand/business context for the domain. Pass it to every subagent as pre-loaded background — agents must treat it as ground truth for business intent, personas, product details and competitive positioning and must not contradict it with generic assumptions. If no file exists, proceed without it.
2. **Render homepage**: use `python3 scripts/render_page.py <url> --mode auto --json` to capture raw HTML, rendered HTML, extracted text, SPA status, and accessibility data when needed
3. **Detect business type**: analyze homepage signals per seo orchestrator, informed by loaded context if available
3. **Crawl site**: check for `firecrawl_map` tool in the active tool list. If present, use Firecrawl as the primary crawler:
   - `firecrawl_map(url)` → discover all URLs (fast, credit-efficient)
   - Filter to top 50–100 most important pages (homepage, key sections, top linked)
   - `firecrawl_crawl(url, limit=100, scrapeOptions.formats=["markdown","html","links"])` → full content extraction with JS rendering
   - Fallback when `firecrawl_map` tool is not found: follow internal links manually up to 500 pages, respect robots.txt
4. **Delegate to subagents** (if available, otherwise run inline sequentially):
   - `seo-technical` -- robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` -- E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` -- detection, validation, generation recommendations
   - `seo-sitemap` -- structure analysis, quality gates, missing pages
   - `seo-performance` -- LCP, INP, CLS measurements
   - `seo-visual` -- screenshots, mobile testing, above-fold analysis
   - `seo-geo` -- AI crawler access, citability, brand mention signals
   - `seo-local` -- GBP signals, NAP consistency, reviews, local schema, industry-specific local factors (spawn when Local Service industry detected: brick-and-mortar, SAB, or hybrid business type)
   - `seo-maps` -- Geo-grid rank tracking, GBP audit, review intelligence, competitor radius mapping (spawn when Local Service detected AND DataForSEO MCP available)
   - `seo-google` -- CWV field data (CrUX), URL indexation (GSC), organic traffic (GA4) (spawn when Google API credentials detected via `python3 scripts/google_auth.py --check`)
   - `seo-backlinks` -- Backlink profile data: DA/PA, referring domains, anchor text, toxic links (spawn when Moz or Bing API credentials detected via `python3 scripts/backlinks_auth.py --check`, or always include Common Crawl domain-level metrics)
   - `seo-cluster` -- Semantic clustering analysis (spawn when content strategy signals detected: blog, pillar pages, topic clusters)
   - `seo-sxo` -- Search experience analysis: page-type mismatch, user stories, persona scoring (always include in full audits)
   - `seo-drift` -- Drift analysis: compare against stored baseline (spawn when drift baseline exists for the URL via `python3 scripts/drift_history.py <url>`)
   - `seo-ecommerce` -- Product schema, marketplace intelligence (spawn when E-commerce industry detected)
   - `seo-dataforseo` -- Live SERP positions, keyword metrics, backlink spam scores, business listings, AI visibility (spawn when `dataforseo_serp_google_organic_live_advanced` tool is present in the active tool list). Do NOT use DataForSEO Lighthouse tools — PageSpeed MCP already covers CWV and Lighthouse scores.
4b. **Semrush competitive enrichment** (run in parallel with subagents): if `execute_report` tool is present in the active tool list, call Semrush directly from the orchestrator:
   - `overview_research(domain)` → organic traffic estimate, keyword count, authority score, referring domains
   - `organic_research(domain)` → top 10 ranking keywords with position, volume, difficulty
   - `backlink_research(domain)` → referring domain count, top anchors, authority distribution
   - Inject these figures into the audit summary as a "Competitive Benchmarks" section. Label all data "Semrush (live)". Do not duplicate anything already covered by DataForSEO backlink data.
5. **Score** -- aggregate into SEO Health Score (0-100)
6. **Persist audit artifacts** -- write all outputs under `{domain}-audit/`
7. **Report** -- generate prioritized action plan and optional PDF/HTML report

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `{domain}-audit/FULL-AUDIT-REPORT.md`: Comprehensive findings
- `{domain}-audit/ACTION-PLAN.md`: Prioritized recommendations (Critical > High > Medium > Low)
- `{domain}-audit/audit-data.json`: Structured audit envelope for report generation
- `{domain}-audit/findings/*.md`: Per-category specialist findings (`technical.md`, `content.md`, `schema.md`, `performance.md`, `visual.md`, etc.)
- `{domain}-audit/screenshots/`: Desktop + mobile captures (if Playwright available)
- **HTML + DOCX Report** (default): After every audit, run `python3 scripts/google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/ --format html+docx`. This produces both a browser-viewable HTML report and a client-ready Word document (.docx) with embedded charts, severity-coloured action plan tables, and footer branding. Always generate both after completing an audit.

## Structured Audit Data Envelope

Write `{domain}-audit/audit-data.json` with this shape so `python3 scripts/google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/` can generate a report even when Google API data is unavailable:

```json
{
  "summary": {
    "health_score": 0,
    "business_type": "detected type",
    "top_findings": [],
    "quick_wins": []
  },
  "categories": [
    {
      "name": "Technical SEO",
      "score": 0,
      "what_works": [],
      "findings": [
        {
          "title": "Finding title",
          "severity": "Critical|High|Medium|Low|Info",
          "description": "Evidence-backed detail",
          "recommendation": "Specific fix"
        }
      ]
    }
  ],
  "action_plan": {
    "phases": [
      {"name": "Phase 1: Critical Fixes", "timeframe": "Week 1", "items": []},
      {"name": "Phase 2: High-Impact Improvements", "timeframe": "Weeks 2-3", "items": []},
      {"name": "Phase 3: Content & Authority", "timeframe": "Month 2", "items": []},
      {"name": "Phase 4: Monitoring & Iteration", "timeframe": "Ongoing", "items": []}
    ]
  },
  "artifacts": {
    "findings_dir": "findings/",
    "screenshots_dir": "screenshots/"
  }
}
```

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Technical SEO
- Crawlability issues
- Indexability problems
- Security concerns
- Core Web Vitals status

### Content Quality
- E-E-A-T assessment
- Thin content pages
- Duplicate content issues
- Readability scores

### On-Page SEO
- Title tag issues
- Meta description problems
- Heading structure
- Internal linking gaps

### Schema & Structured Data
- Current implementation
- Validation errors
- Missing opportunities

### Performance
- LCP, INP, CLS scores
- Resource optimization needs
- Third-party script impact

### Images
- Missing alt text
- Oversized images
- Format recommendations

### AI Search Readiness
- Citability score
- Structural improvements
- Authority signals

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Firecrawl Integration (Optional)

If Firecrawl MCP is available (`firecrawl_map` tool present), use it as the primary crawler:

1. `firecrawl_map(url, limit=5000)` → full URL discovery, compare against XML sitemap to surface orphan/missing pages
2. `firecrawl_crawl(url, limit=100)` → JS-rendered content extraction fed to all subagents
3. Feed crawled markdown to `seo-content`, `seo-schema`, `seo-technical`, `seo-geo` agents
4. Report total crawlable pages, URL pattern breakdown, and crawl depth in audit output

**Credit awareness:** Inform user of estimated Firecrawl credit usage before large crawls (free tier: 500 credits/month; 1 credit per page crawled, 0.5 per URL mapped).

**Fallback:** If Firecrawl unavailable or credits exhausted, use `fetch_page.py` + manual link following.

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, spawn the `seo-dataforseo` agent alongside existing subagents to enrich the audit with live data: real SERP positions, backlink profiles with spam scores, on-page analysis (Lighthouse), business listings, and AI visibility checks (ChatGPT scraper, LLM mentions).

## Google API Integration (Optional)

If Google API credentials are configured (`python3 scripts/google_auth.py --check`), spawn the `seo-google` agent to enrich the audit with real Google field data: CrUX Core Web Vitals (replaces lab-only estimates), GSC URL indexation status, search performance (clicks, impressions, CTR), and GA4 organic traffic trends. The Performance (CWV) category score benefits most from field data.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| robots.txt blocks crawling | Report which paths are blocked. Analyze only accessible pages and note the limitation in the report. |
| Rate limiting (429 responses) | Back off and reduce concurrent requests. Report partial results with a note on which sections could not be completed. |
| Timeout on large sites (500+ pages) | Cap the crawl at the timeout limit. Report findings for pages crawled and estimate total site scope. |
