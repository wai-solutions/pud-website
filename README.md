# PUD Consultants — Website

**60 Years of Shaping Sustainable Cities · 1966 – 2026**

Live site: **https://wai-solutions.github.io/pud-website/**

A fast, static, multi-page website for PUD Consultants (Planning & Urban Development Consultants). Plain HTML, CSS and JavaScript — no framework, no build step needed to deploy.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Projects (filterable) | `projects.html` |
| Project detail (one page each) | `project-<slug>.html` |
| 60 Years story | `60-years.html` |
| People | `people.html` |
| Sustainability | `sustainability.html` |
| News | `news.html` |
| News articles (one page each) | `article-<slug>.html` |
| About | `about.html` |
| Contact | `contact.html` |

## Structure

```
/                 HTML pages (ready to serve)
assets/pud.css    all styles
assets/pud.js     interactions, news, timeline, map, search
assets/projects.js  project data (window.PUD_PROJECTS)
img/              photography, logos (img/logos/), thumbnails (*-t.jpg)
tools/build.py    optional generator for the HTML pages
```

## Deploy

The site is fully static — upload the folder as-is to any host.

> **Before going live on a new domain, complete the [Deployment checklist](#deployment-checklist-required) below.** Otherwise search engines will index the wrong URLs.

**GitHub Pages (current):** Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.

**Netlify / Vercel / Cloudflare Pages:** import this repo, leave the build command empty and set the publish/output directory to `/` (root).

**Any web server (Apache, Nginx, IIS, cPanel):** copy every file to the web root. No server-side code is required.

**Custom domain (e.g. pudconsultants.com):** add a `CNAME` file containing the domain, then point the domain's DNS to the host.

## SEO, GEO & AEO

- **Every page** has a unique title, meta description, canonical URL, Open Graph and Twitter card tags, and Schema.org JSON-LD (Organization/ProfessionalService, WebSite, WebPage, BreadcrumbList).
- **Indexable detail pages:** each project (`project-<slug>.html`, CreativeWork schema) and news story (`article-<slug>.html`, NewsArticle schema) is a real static page with its content in the HTML. Old `project.html#slug` links redirect automatically.
- **AEO:** the About page has a FAQ (`about.html#faq`) with FAQPage schema, written as direct, quotable answers.
- **GEO:** `llms.txt` gives AI assistants a concise, factual summary (key facts, FAQ, news, all projects with links). `robots.txt` explicitly allows search and AI crawlers.
- **Sitemap:** `sitemap.xml`. See the **Deployment checklist** below for the two required steps: set the domain, then submit the sitemap.

## Deployment checklist (required)

Complete these two steps whenever the site is deployed, and again whenever its address changes.

### Step 1 — Set the final domain and rebuild

Canonical URLs, the sitemap, `robots.txt`, `llms.txt`, social-share previews and all structured data are generated with the site's full address. If the site is served from a different address than the one in `BASE`, search engines will index the wrong URLs.

1. Open `tools/build.py` and change the `BASE` line near the top to the final address, **with a trailing slash**:
   ```python
   BASE = 'https://www.pudconsultants.com/'
   ```
2. Rebuild (requires Python 3 and Node.js, no packages):
   ```
   python3 tools/build.py
   ```
3. Check that the new address appears in the generated files:
   ```
   grep -m1 "<loc>" sitemap.xml
   grep "Sitemap:" robots.txt
   grep 'rel="canonical"' index.html
   ```
4. For a custom domain on GitHub Pages, add a `CNAME` file at the root containing only the domain (e.g. `www.pudconsultants.com`). Then, in **Settings → Pages**, enter the domain and tick **Enforce HTTPS**.
5. At the domain registrar, point DNS to the host:
   - **GitHub Pages:** for `www`, add a `CNAME` record pointing to `wai-solutions.github.io`. For the bare domain, add `A` records for `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`.
   - **Other hosts:** follow the host's custom-domain instructions.
6. Commit and push (or upload). Then open the live site and confirm the address bar, the page source's `<link rel="canonical">` and `/sitemap.xml` all show the final domain.

### Step 2 — Submit the sitemap to search engines

Without this step, Google and Bing can take weeks to discover the site.

**Google Search Console** — https://search.google.com/search-console
1. Click **Add property**. Choose **Domain** (verified with a DNS TXT record, covers http/https and www) or **URL prefix** (enter the exact `BASE` address).
2. Verify ownership. For a Domain property, add the TXT record Google provides at the registrar. For a URL prefix property, the simplest option is the **HTML tag**: add the `<meta name="google-site-verification" ...>` tag Google gives you to the `<head>` template in `tools/build.py` (next to `<meta name="author" ...>`), rebuild and redeploy.
3. Open **Sitemaps** in the left menu, enter `sitemap.xml` and click **Submit**. The status should change to **Success**, with about 78 discovered pages.
4. Optional: use **URL Inspection** on the home page and click **Request indexing** to speed things up.

**Bing Webmaster Tools** — https://www.bing.com/webmasters (Bing also feeds Copilot, DuckDuckGo and ChatGPT search)
1. Sign in. The fastest route is **Import from Google Search Console**, which brings over the verified site and sitemap in one step.
2. Or add the site manually, verify it (XML file, meta tag or DNS), then open **Sitemaps → Submit sitemap** and enter the full sitemap URL, e.g. `https://www.pudconsultants.com/sitemap.xml`.

**After launch (recommended)**
- Test a few pages in the Rich Results Test (https://search.google.com/test/rich-results): Home (Organization), About (FAQ), a project page and a news article.
- Test the share preview by pasting the URL into the LinkedIn Post Inspector (https://www.linkedin.com/post-inspector/).
- Whenever projects or news are added, run `python3 tools/build.py` before deploying. The sitemap and `llms.txt` update automatically, and search engines re-read the submitted sitemap on their own.

## Editing content

- **Text in pages:** edit `tools/build.py`, then run `python3 tools/build.py` to regenerate all HTML files, the sitemap, robots.txt and llms.txt (Python 3 + Node.js, no packages). You can also edit the HTML files directly, but they will be overwritten the next time the generator runs.
- **News:** edit the `NEWS` array in `assets/pud.js`.
- **Projects:** edit `assets/projects.js`; images go in `img/<slug>.jpg` with a thumbnail `img/<slug>-t.jpg`.
- **Timeline milestones:** the `M` array in `assets/pud.js`.

## Enquiries (floating chat + contact form)

- A floating chat button (bottom-right, every page) and the Contact page form send enquiries by email through **FormSubmit** (https://formsubmit.co), with no server needed.
- Recipients: `inas.bakeer@wai-s.com` (main) and `m.sawaf@risepersonal.com` (CC). To change them, edit `MAIL_TO` and `MAIL_CC` at the top of the "ENQUIRIES" block in `assets/pud.js`.
- **One-time activation:** the very first submission triggers a confirmation email from FormSubmit to `MAIL_TO`. Click **Activate** in that email. Messages are delivered only after activation. Repeat this whenever `MAIL_TO` changes or the site moves to a new domain.
- After sending, visitors see: *"Thank you for contacting us. Our team will respond and get back to you within 48 hours."*
- Spam protection: a hidden honeypot field. FormSubmit's reCAPTCHA can be enabled by removing the `_captcha=false` line.

## Local preview

```
python3 -m http.server 8000
```
Then open http://localhost:8000

## Notes

- Fonts: Antonio and Roboto from Google Fonts.
- Respects `prefers-reduced-motion`, and includes a low-data mode toggle.
- © PUD Consultants. All rights reserved. Project images and logos belong to their respective owners.
