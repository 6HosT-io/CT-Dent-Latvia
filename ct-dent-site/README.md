# CT-Dent · Revamped Website (production build)

Static, dependency-free rebuild of **ct-dent.lv** in the approved **V6 "Editorial × Diagnostic"**
design code. 21 pages × 3 languages (LV main, EN/RU additional) = **63 HTML pages**,
dual theme (light/dark), GDPR-ready consent, WCAG-oriented markup, SEO & security configs.

## Preview
Serve the `public/` folder with any static server, e.g.:
```
cd public && python3 -m http.server 8000
```
Language URLs: `/` (LV), `/en/…`, `/ru/…` — every page has hreflang alternates + canonical.

## Structure
```
ct-dent-site/
├── public/            ← deploy this folder (site root)
│   ├── index.html …   63 pages
│   ├── assets/        css, js, fonts (woff2 subsets LV/EN/RU), img, docs (referral PDF)
│   ├── robots.txt, sitemap.xml
│   ├── _headers       ← Netlify-style security headers
│   └── .htaccess      ← Apache/LiteSpeed security headers + HTTPS redirect
├── assets/            source assets (copied into public at build)
└── _src/
    ├── build.py       static site generator  →  python3 build.py
    ├── content.py     ALL trilingual copy (single source of truth)
    └── fontface.css   @font-face rules (Playfair Display + Manrope, latin/latin-ext/cyrillic)
```

## What was fixed vs the old site (audit → action)
- **GDPR**: privacy policy, cookie policy, terms of use created (LV/EN/RU); consent banner with
  equal-weight **Accept / Reject / Preferences** (persisted, reopenable from footer); no third-party
  scripts load before consent; referral form has explicit consent checkbox; Art. 9 health-data basis stated.
- **Security**: HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy
  shipped via `_headers` / `.htaccess`; no WordPress login surface; no version disclosure.
- **Content**: single phone (+371 262 67 763); booking contradiction resolved ("registration recommended,
  walk-ins may wait"); Lithuanian leftovers removed; © 2026; one current referral PDF (2025-03).
- **SEO**: unique titles + meta descriptions per page/language, Open Graph, hreflang + x-default,
  canonical, JSON-LD `MedicalClinic`, sitemap.xml, localized slugs (`/pakalpojumi/cbct/` etc.).
- **Accessibility**: skip link, landmarks, single H1 per page, labelled forms with inline errors,
  focus-visible styles, `prefers-reduced-motion` respected, contrast-safe palettes in both themes.
- **Performance**: no frameworks; 2 woff2 families subsetted; system monospace for data labels;
  lazy-loaded images; ~0 JS besides theme/consent/forms/motion.

## Data status (updated after owner confirmation)

Confirmed & baked in:
- Legal entity: SIA "CT-Dent", reg. Nr. 40203769230, Cēsu iela 31 k-2, Rīga, LV-1012 — Privacy Policy, Terms of Use, footer, Contacts, JSON-LD (`legalName`, `postalCode`).
- Data retention: 5 years (referral & contact data); cookie consent 12 months.
- Working hours: Mon–Fri (P.–Pk.) 9:30–18:00 — corner-capsule info card, Contacts page, JSON-LD.
- E-mail: `info@ct-dent.lv` displayed everywhere (address is being provisioned). Interim inbox: `ctdentriga@gmail.com` — to switch, change `EMAIL` in `_src/content.py` and `CONTACT_EMAIL` in `assets/js/site.js`, then rebuild.
- Utility bar: original dark topbar replaced by the floating corner capsule (concept E) — phone, LV/EN/RU, theme switch + (i) card with address, hours, e-mail and directions. It rises above the cookie banner while consent is open.

Still open:
1. Hosting provider name — remaining placeholder `[HOSTINGA SNIEDZĒJS]` / `[HOSTING PROVIDER]` / `[ХОСТИНГ-ПРОВАЙДЕР]` in `_src/content.py` (Privacy Policy).
2. Map embed — Contacts page keeps a styled placeholder; a cookie-free OpenStreetMap embed can be added on approval.
3. Real testimonials — the home-page quote card is brand voice (no invented attribution); a real, consented review can be swapped in later (`q_text`/`q_author` in `_src/content.py`).
4. iRYS section — mother page "iRYS programmatūra" (EN "iRYS Software" / RU "Платформа iRYS") under Ārstiem with guide, analysis and downloads as children: in progress.

## Forms
Referral & contact forms validate client-side and open the visitor's e-mail client (mailto fallback,
as approved). `site.js` exposes a single place to swap in a real API endpoint later.

## Portal pages
`/portals/…` are styled UI pages that link to the existing DentQ/WordPress backend
(login, my documents, file browser, create account, password reset) until migration.

## Rebuild
Edit copy in `_src/content.py`, then:
```
cd _src && python3 build.py
```
