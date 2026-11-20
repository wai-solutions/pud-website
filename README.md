# PUD Consultants — Website

**60 Years of Shaping Sustainable Cities · 1966 – 2026**

Live site: **https://wai-solutions.github.io/pud-website/**

A fast, static, multi-page website for PUD Consultants (Planning & Urban Development Consultants). Plain HTML, CSS and JavaScript — no framework, no build step needed to deploy.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Projects (filterable) | `projects.html` |
| Project detail (hash-routed, e.g. `project.html#cairo-media-city`) | `project.html` |
| 60 Years story | `60-years.html` |
| People | `people.html` |
| Sustainability | `sustainability.html` |
| News | `news.html` |
| News article (hash-routed, e.g. `article.html#share-cairo-2026`) | `article.html` |
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

**GitHub Pages (current):** Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.

**Netlify / Vercel / Cloudflare Pages:** import this repo, leave the build command empty and set the publish/output directory to `/` (root).

**Any web server (Apache, Nginx, IIS, cPanel):** copy every file to the web root. No server-side code is required.

**Custom domain (e.g. pudconsultants.com):** add a `CNAME` file containing the domain, then point the domain's DNS to the host.

## Editing content

- **Text in pages:** edit `tools/build.py`, then run `python3 tools/build.py` to regenerate the HTML files (Python 3, no dependencies). You can also edit the HTML files directly, but they will be overwritten the next time the generator runs.
- **News:** edit the `NEWS` array in `assets/pud.js`.
- **Projects:** edit `assets/projects.js`; images go in `img/<slug>.jpg` with a thumbnail `img/<slug>-t.jpg`.
- **Timeline milestones:** the `M` array in `assets/pud.js`.

## Local preview

```
python3 -m http.server 8000
```
Then open http://localhost:8000

## Notes

- Fonts: Antonio and Roboto from Google Fonts.
- Respects `prefers-reduced-motion`, and includes a low-data mode toggle.
- © PUD Consultants. All rights reserved. Project images and logos belong to their respective owners.
