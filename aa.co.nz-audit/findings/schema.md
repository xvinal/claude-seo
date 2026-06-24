# Schema / Structured Data Audit — aa.co.nz/membership/
**Score: 14/100**

## What Works
- Microdata BreadcrumbList present on all 10 audited pages (AEM CMS component)
- Microdata ImageObject wrapping all promotional images with `contentUrl`

## Critical Issues
**C1. No Organization schema** — zero entity markup; Google cannot confirm name, URL, logo, contacts, sameAs
**C2. No Product + Offer schema on tier pages** — 4 purchasable tiers with explicit prices, none exposed via schema; direct revenue opportunity lost
**C3. BreadcrumbList uses `http://` not `https://`** — all itemtype declarations use deprecated http:// prefix (CMS-wide defect)
**C4. BreadcrumbList `item` hrefs are relative not absolute** — spec requires absolute URLs; affects all pages
**C5. Current page absent from breadcrumb on all tier pages** — trail terminates at parent, not current page

## High Issues
- No WebSite schema with SearchAction (suppresses sitelinks search box)
- No Service schema on /roadservice-breakdown-assistance/
- No Service / Organization schema on /membership/business/
- No WebPage schema on /membership/join-aa/

## Medium Issues
- No ItemList on /membership/benefits-and-discounts/ (45+ benefits in 6 categories)
- No FAQPage on roadservice page (aids GEO/AI citation)
- ImageObject `contentUrl` uses relative paths (should be absolute)
- ImageObject instances lack `name` property

## Low Issues
- No `@id` anchors for entity disambiguation
- No `sameAs` to Wikidata or social profiles

## Top 3 JSON-LD Recommendations

### 1. Organization (sitewide, highest impact)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.aa.co.nz/#organization",
  "name": "New Zealand Automobile Association",
  "alternateName": "AA New Zealand",
  "url": "https://www.aa.co.nz/",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.aa.co.nz/content/dam/nzaa/logos/aa-logo.svg",
    "width": 200,
    "height": 60
  },
  "description": "New Zealand's largest motoring organisation, providing roadside assistance, insurance, travel, and member benefits to over 1.7 million members.",
  "foundingDate": "1903",
  "areaServed": { "@type": "Country", "name": "New Zealand" },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+64-800-500-444",
      "contactType": "roadside assistance",
      "availableLanguage": "English"
    },
    {
      "@type": "ContactPoint",
      "telephone": "+64-800-500-444",
      "contactType": "customer service",
      "availableLanguage": "English"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/AANewZealand",
    "https://www.instagram.com/aa_newzealand/",
    "https://en.wikipedia.org/wiki/New_Zealand_Automobile_Association"
  ],
  "memberOf": {
    "@type": "Organization",
    "name": "Fédération Internationale de l'Automobile",
    "url": "https://www.fia.com/"
  }
}
```

### 2. Product + Offer for Standard Membership (/membership/options-and-fees/standard-membership/)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://www.aa.co.nz/membership/options-and-fees/standard-membership/#product",
  "name": "AA Standard Membership",
  "description": "24/7 roadside breakdown assistance, battery service, key lockout, tyre change, tow to safety, emergency fuel delivery, and access to 45+ AA Member Benefits.",
  "brand": { "@type": "Brand", "name": "AA New Zealand" },
  "provider": { "@id": "https://www.aa.co.nz/#organization" },
  "url": "https://www.aa.co.nz/membership/options-and-fees/standard-membership/",
  "offers": [
    {
      "@type": "Offer",
      "name": "Standard Membership – Rest of New Zealand",
      "price": "89.00",
      "priceCurrency": "NZD",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "89.00",
        "priceCurrency": "NZD",
        "unitText": "year"
      },
      "eligibleRegion": { "@type": "AdministrativeArea", "name": "New Zealand" },
      "url": "https://www.aa.co.nz/membership/join-aa/",
      "availability": "https://schema.org/InStock",
      "seller": { "@id": "https://www.aa.co.nz/#organization" }
    }
  ],
  "additionalProperty": [
    { "@type": "PropertyValue", "name": "Roadside callouts included", "value": "Unlimited" },
    { "@type": "PropertyValue", "name": "24/7 availability", "value": "Yes" },
    { "@type": "PropertyValue", "name": "Reciprocal overseas cover", "value": "Yes" }
  ]
}
```

### 3. Service for Roadside Assistance (/membership/roadservice-breakdown-assistance/)
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://www.aa.co.nz/membership/roadservice-breakdown-assistance/#service",
  "name": "AA Roadservice – 24/7 Breakdown Assistance",
  "description": "24/7 breakdown assistance including battery service, key lockout, tyre change, tow to safety, emergency fuel delivery, and EV mobile charging. Available across New Zealand.",
  "serviceType": "Roadside Assistance",
  "provider": { "@id": "https://www.aa.co.nz/#organization" },
  "areaServed": { "@type": "Country", "name": "New Zealand" },
  "availableChannel": {
    "@type": "ServiceChannel",
    "servicePhone": {
      "@type": "ContactPoint",
      "telephone": "+64-800-500-222",
      "contactType": "roadside assistance"
    }
  },
  "hoursAvailable": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  },
  "url": "https://www.aa.co.nz/membership/roadservice-breakdown-assistance/"
}
```

## Page-by-Page Opportunity Matrix
| Page | Existing Schema | Key Gap | Priority |
|---|---|---|---|
| /membership/ | BreadcrumbList, ImageObject | Organization, WebSite+SearchAction | Critical |
| /membership/options-and-fees/ | BreadcrumbList, ImageObject | ItemList of tiers | High |
| /membership/options-and-fees/standard-membership/ | BreadcrumbList (missing current page) | Product + Offer ($89) | Critical |
| /membership/options-and-fees/associate-membership/ | BreadcrumbList (missing current page) | Product + Offer ($44.50) | Critical |
| /membership/options-and-fees/youth-membership/ | BreadcrumbList (missing current page) | Product + Offer ($50) | Critical |
| /membership/options-and-fees/aa-plus/ | BreadcrumbList (missing current page) | Product + Offer ($27 upgrade) | Critical |
| /membership/benefits-and-discounts/ | BreadcrumbList, ImageObject | ItemList (6 categories) | High |
| /membership/roadservice-breakdown-assistance/ | BreadcrumbList, ImageObject | Service schema | Critical |
| /membership/join-aa/ | BreadcrumbList, ImageObject | WebPage, JoinAction | High |
| /membership/business/ | BreadcrumbList, ImageObject | Service ×4 B2B products | High |

## Implementation Notes
- BreadcrumbList fix is a CMS template change (not page-by-page): change http:// to https://, make hrefs absolute, add current page as final item
- Inject all JSON-LD via AEM `<head>` component as `<script type="application/ld+json">`
- Organization block belongs in global page template (sitewide)
- Product/Service blocks belong in respective page templates
- Validate with Google's Rich Results Test after implementation
