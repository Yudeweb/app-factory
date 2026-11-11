# Platform: web

Read when `plan.md` says the platform is web or both. In stage 1, settle which kind it is: **web application** (accounts and data: SaaS, dashboard, marketplace), **installable web app (PWA)**, **content or marketing site**, or **API or backend only**. Record it on the `Platform:` line.

**Technology options to compare (stage 1):** server-rendered, single-page or static site, and why it matters (search visibility, first-load speed, complexity); the framework for the chosen approach; hosting (managed platform, containers, or a plain server); a managed backend service versus a custom backend; sign-in; database. Ask which browsers and devices matter and whether it must be found through search.

**Design (stage 2):** responsive layouts for phone, tablet and desktop widths; keyboard navigation and visible focus; hover and touch both work; loading behaviour on slow connections.

**Build plan (stage 3):** environments (preview, staging, production), domain and DNS, and environment secrets are tasks. Production deployment stays behind manual approval.

**QA (stage 5):** current Chrome, Safari and Firefox, on desktop and phone widths; page speed and accessibility audits (for example Lighthouse); forms, sign-in and error pages; behaviour with a slow or lost connection. Use the browser tools available in the session to exercise the running site.

**Security review:** cross-site scripting and request forgery, cookie and session settings, CORS, security headers, what the browser bundle exposes, rate limiting on public endpoints.

**Launch (stage 6):** domain, hosting plan and its cost, search visibility (titles, descriptions, sitemap), analytics, cookie and privacy notices, a landing page, and monitoring.

## By kind

- **PWA:** manifest, home-screen icon, service worker; QA checks that it installs and what works offline. Say what a PWA cannot do on iOS compared with a native app before the user chooses it over mobile.
- **Content or marketing site:** search visibility and page speed lead; consider a static site and how the owner will edit content. The build plan is short.
- **API or backend only:** there are no screens, so stage 2 uses no Figma. The design is the API contract (endpoints, inputs, outputs, errors, authentication, versioning), written to `docs/design.md` and approved at Gate 2. QA is contract tests and a load check; launch covers documentation, keys, rate limits and pricing.
