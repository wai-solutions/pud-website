import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # site root, one level up from tools/
import json, subprocess, html as _h
BASE = 'https://wai-solutions.github.io/pud-website/'
ORG = {
  "@type": ["Organization", "ProfessionalService"], "@id": BASE + "#org",
  "name": "PUD Consultants", "alternateName": ["Planning & Urban Development Consultants", "Planning Urban Development (PUD)"],
  "url": BASE, "logo": BASE + "img/pud-logo-v.png", "image": BASE + "img/cairo-media-city.jpg",
  "foundingDate": "1966", "founder": {"@type": "Person", "name": "Prof. Abdallah Abdel Aziz Attia"},
  "description": "Multidisciplinary planning and design consultancy founded in Cairo in 1966, shaping sustainable cities, tourism destinations, heritage areas and sacred landscapes across Egypt, Saudi Arabia, the UAE and beyond.",
  "slogan": "60 Years of Shaping Sustainable Cities",
  "knowsAbout": ["Urban and regional planning", "Master planning", "Urban design", "Sustainable tourism development", "Cultural heritage planning", "Landscape planning", "Architectural design", "Green economy", "Development consultancy", "Financial planning and feasibility", "Sustainable development goals"],
  "areaServed": ["Egypt", "Saudi Arabia", "United Arab Emirates", "Middle East and North Africa"],
  "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 150},
  "address": [
    {"@type": "PostalAddress", "streetAddress": "115 El Thawra Street, 5th Floor, Heliopolis", "postalCode": "11757", "addressLocality": "Cairo", "addressCountry": "EG"},
    {"@type": "PostalAddress", "streetAddress": "8620 Ibn Mousa Street, Diplomatic Quarter", "addressLocality": "Riyadh", "addressCountry": "SA"},
    {"@type": "PostalAddress", "streetAddress": "Shoreline 12, Al Anbara, Palm Jumeirah", "addressLocality": "Dubai", "addressCountry": "AE"}],
  "contactPoint": [{"@type": "ContactPoint", "telephone": "+20-2-2414-7537", "contactType": "customer service", "areaServed": "EG"},
                   {"@type": "ContactPoint", "telephone": "+966-540-39-8178", "contactType": "customer service", "areaServed": "SA"},
                   {"@type": "ContactPoint", "telephone": "+971-509-29-8178", "contactType": "customer service", "areaServed": "AE"}],
  "sameAs": ["https://www.pudconsultants.com/", "https://www.linkedin.com/in/amr-attia-9181898/"]
}
SEO = {
 'index.html': ("PUD Consultants: planning, urban design and sustainable development since 1966. 150+ projects across 11 countries, from Cairo Media City and the Pyramids Plateau to AlUla and the Holy Sites.", 'cairo-media-city.jpg'),
 'projects.html': ("Explore 150+ PUD Consultants projects: master plans, tourism destinations, heritage areas, smart and green cities and infrastructure across Egypt, Saudi Arabia and beyond.", 'al-rabita-competition.jpg'),
 '60-years.html': ("Sixty years of PUD Consultants, 1966 to 2026: the founder’s vision, the new chapter under Prof. Dr. Amr Attia, global collaborations and the projects that define six decades.", 'pyramids-plateau.jpg'),
 'people.html': ("Meet the people of PUD Consultants: founder Prof. Abdallah Abdel Aziz Attia, CEO Prof. Dr. Amr A. Attia, key staff, strategic partners and an international expert network.", 'people-gem.jpg'),
 'sustainability.html': ("PUD Consultants’ sustainability commitments: people, society, culture, environment and planet, aligned with UN SDGs 7, 8, 9, 11, 12, 13 and 17.", 'heliopark.jpg'),
 'news.html': ("Latest news from PUD Consultants: SHARE Architects forums, the Pyramids Destination master plan, Sumou Boulevard and more.", 'jorhum.jpg'),
 'about.html': ("About PUD Consultants: purpose, expertise, approach, awards and frequently asked questions about Egypt’s planning and urban development consultancy founded in 1966.", 'khaybar-heritage.jpg'),
 'contact.html': ("Contact PUD Consultants offices in Cairo, Riyadh and Dubai for master planning, urban design, strategic advisory and sustainable development projects.", 'prince-talal-hurghada.jpg'),
}
CRUMB_NAMES = {'projects.html':'Projects','60-years.html':'60 Years','people.html':'People','sustainability.html':'Sustainability','news.html':'News','about.html':'About','contact.html':'Contact'}
SITEMAP = []
import time as _t
VER = str(int(_t.time()))
try:
    subprocess.run(['node', os.path.join(OUT, 'tools', 'export_data.js')], check=True, capture_output=True)
except Exception as ex:
    print('note: node export skipped:', ex)
DATA = json.load(open(os.path.join(OUT, 'tools', 'data.json')))
PROJ_INDEX = '<section class="sec gut" id="index"><div class="row2"><div class="lbl">Project index A–Z</div><div><ul class="pidx">' + ''.join(f'<li><a href="project-{p["s"]}.html">{_h.escape(p["n"])}</a><span>{_h.escape(p.get("l",""))}</span></li>' for p in sorted(DATA['projects'], key=lambda p: p['n'].lower())) + '</ul></div></div></section>'

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>'

def head_meta(fn, title, desc, img, extra_ld=None, noindex=False, crumbs=None, ogtype='website'):
    url = BASE + ('' if fn == 'index.html' else fn)
    imgurl = BASE + 'img/' + img
    g = [ORG, {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "PUD Consultants", "publisher": {"@id": BASE + "#org"}, "inLanguage": "en"},
         {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "isPartOf": {"@id": BASE + "#site"}, "about": {"@id": BASE + "#org"}, "primaryImageOfPage": imgurl, "inLanguage": "en"}]
    if crumbs:
        g.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + ('' if u == 'index.html' else u)} for i, (n, u) in enumerate(crumbs)]})
    if extra_ld: g += extra_ld
    e = _h.escape
    m = [f'<meta name="description" content="{e(desc)}">',
         f'<meta name="robots" content="{"noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"}">',
         f'<link rel="canonical" href="{url}">',
         '<meta name="theme-color" content="#EE4223">', '<meta name="author" content="PUD Consultants">',
         f'<meta property="og:type" content="{ogtype}">', '<meta property="og:site_name" content="PUD Consultants">',
         f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
         f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{imgurl}">', '<meta property="og:locale" content="en_US">',
         '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{e(title)}">',
         f'<meta name="twitter:description" content="{e(desc)}">', f'<meta name="twitter:image" content="{imgurl}">',
         '<link rel="alternate" type="text/plain" title="LLM summary" href="llms.txt">',
         jsonld({"@context": "https://schema.org", "@graph": g})]
    if not noindex: SITEMAP.append(url)
    return '\n'.join(m)
AR = '<svg viewBox="0 0 16 10"><path d="M0 5h14M10 1l4 4-4 4"/></svg>'
CAR = lambda id, extra='': f'''<div class="car" id="{id}"{extra}><div class="car-track"></div><div class="car-ctl"><span class="car-n">01/01</span><div class="arrows"><button aria-label="Previous"><svg viewBox="0 0 16 16"><path d="M14 8H2M7 3L2 8l5 5"/></svg></button><button aria-label="Next"><svg viewBox="0 0 16 16"><path d="M2 8h12M9 3l5 5-5 5"/></svg></button></div></div></div>'''

def mi(label, href, cur, subs=None):
    c = ' class="cur" aria-current="page"' if href == cur else ''
    if not subs:
        return f'<div class="mi gut"><div class="mi-row"><a href="{href}"{c}>{label}</a></div></div>'
    s = ''.join(f'<a href="{h}">{t}</a>' for t, h in subs)
    return f'<div class="mi gut"><div class="mi-row"><a href="{href}"{c}>{label}</a><button class="mi-x" aria-expanded="false" aria-label="Show {label} links">+</button></div><div class="mi-sub"><div>{s}</div></div></div>'

def chrome(cur, solid):
    menu = ''.join([
        mi('Projects', 'projects.html', cur, [('All projects', 'projects.html'), ('Egypt', 'projects.html#egypt'), ('Saudi Arabia', 'projects.html#ksa'), ('International', 'projects.html#intl')]),
        mi('60 Years', '60-years.html', cur, [('The founder', '60-years.html#ch1'), ('The new chapter', '60-years.html#ch2'), ('Global minds', '60-years.html#ch3'), ('The journey', '60-years.html#journey'), ('Timeline', '60-years.html#timeline')]),
        mi('People', 'people.html', cur),
        mi('Sustainability', 'sustainability.html', cur, [('Our commitment', 'sustainability.html#commitment'), ('Goals we support', 'sustainability.html#sdgs'), ('Projects', 'sustainability.html#projects')]),
        mi('News', 'news.html', cur),
        mi('About', 'about.html', cur, [('Purpose', 'about.html'), ('Expertise', 'about.html#expertise'), ('Approach', 'about.html#approach'), ('Sustainability', 'sustainability.html'), ('Awards', 'about.html#awards'), ('FAQ', 'about.html#faq')]),
    ])
    return f'''<div class="fade" aria-hidden="true"></div>
<a class="sr" href="#main">Skip to content</a>
<header class="hdr gut always">
  <a class="logo" href="index.html" aria-label="PUD Consultants home"><img src="img/pud-logo-v.png" alt="PUD"><b>PUD<i></i></b><span>Planning &amp; Urban<br>Development Consultants</span></a>
  <div class="hdr-r">
    <a class="hdr-60" href="60-years.html"><strong>60</strong> Years</a>
    <button class="ibtn burger" id="menuBtn" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
    
  </div>
</header>
<div class="menu" role="dialog" aria-label="Site menu">
  <nav>{menu}</nav>
  <div>
    <div class="menu-60 gut"><b>60</b><p>1966 – 2026. Sixty years of shaping sustainable cities across Egypt, Saudi Arabia and beyond.</p></div>
    <div class="menu-foot gut"><span style="display:flex;gap:28px;align-items:center"><a href="contact.html" class="ul">Contact</a><button class="m-search" id="searchBtn"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>Search</button></span><span class="addr">Cairo · Riyadh · Dubai</span></div>
  </div>
</div>
<div class="lite">
  <button class="lite-btn" id="liteBtn" aria-expanded="false" aria-label="Viewing settings"><svg viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg></button>
  <div class="lite-panel" id="litePanel" hidden><p>Reduce motion and data use while you browse.</p><label class="sw"><input type="checkbox" id="liteSw"><span></span> Low-data mode</label></div>
</div>
<div class="search" role="dialog" aria-label="Search">
  <div class="gut"><label for="q" class="sr">Search PUD</label><input id="q" type="search" placeholder="Search projects, people, news" autocomplete="off"><div class="sres" id="sres"></div></div>
</div>
'''

FOOT = f'''<footer class="foot gut">
  <div class="foot-g">
    <div><a class="logo" href="index.html"><img src="img/pud-logo-v.png" alt="PUD"><b>PUD<i></i></b><span>Planning &amp; Urban<br>Development Consultants</span></a>
      <p style="margin-top:18px;font-size:14px;color:var(--mid);max-width:340px">Leadership · Harmony · Clarity. Shaping sustainable cities since 1966.</p></div>
    <div><h5>Work</h5><a class="l" href="projects.html">Projects</a><a class="l" href="about.html#expertise">Expertise</a><a class="l" href="about.html#approach">Approach</a></div>
    <div><h5>Company</h5><a class="l" href="about.html">About</a><a class="l" href="people.html">People</a><a class="l" href="60-years.html">60 Years</a><a class="l" href="about.html#awards">Awards</a></div>
    <div><h5>Connect</h5><a class="l" href="news.html">News</a><a class="l" href="contact.html">Contact</a><a class="l" href="sustainability.html">Sustainability</a></div>
    <div><h5>Follow</h5><div class="soc"><a href="https://www.linkedin.com/company/pud-consultants" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.2 21 14.5V21h-4v-5.8c0-1.4-.03-3.2-1.95-3.2-1.95 0-2.25 1.52-2.25 3.1V21H9z"/></svg></a><a href="https://www.pudconsultants.com" target="_blank" rel="noopener" aria-label="pudconsultants.com"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-3a15 15 0 00-1.3-4A8 8 0 0118.9 8zM12 4c.9 1.2 1.6 2.6 2 4h-4c.4-1.4 1.1-2.8 2-4zM4.3 14a8 8 0 010-4h3.4a16 16 0 000 4zm.8 2h3a15 15 0 001.3 4A8 8 0 015.1 16zm3-8h-3a8 8 0 014.3-4 15 15 0 00-1.3 4zM12 20c-.9-1.2-1.6-2.6-2-4h4c-.4 1.4-1.1 2.8-2 4zm2.3-6H9.7a14 14 0 010-4h4.6a14 14 0 010 4zm.3 6a15 15 0 001.3-4h3a8 8 0 01-4.3 4zm1.7-6a16 16 0 000-4h3.4a8 8 0 010 4z"/></svg></a></div></div>
  </div>
  <div class="foot-b"><span>© 2026 PUD Consultants. All rights reserved.</span><span>60 Years of Shaping Sustainable Cities · 1966 – 2026</span></div>
</footer>
'''

def page(fn, title, body, solid=True, desc=None, img=None, ld=None, noindex=False, crumbs=None, ogtype='website'):
    d0, i0 = SEO.get(fn, (None, None))
    desc = desc or d0 or 'PUD Consultants: 60 years of shaping sustainable cities.'
    img = img or i0 or 'cairo-media-city.jpg'
    if crumbs is None and fn in CRUMB_NAMES: crumbs = [('Home', 'index.html'), (CRUMB_NAMES[fn], fn)]
    meta = head_meta(fn, title, desc, img, ld, noindex, crumbs, ogtype)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="img/pud-logo-v.png">
<title>{title}</title>
{meta}
<meta name="pud-build" content="{VER}">
<script>/* show the newest version after an update, even if the browser cached this page */
(function(){{try{{var v="{VER}",k="pud-build";if(sessionStorage.getItem(k+location.pathname)==="1")return;fetch(location.pathname+"?_="+Date.now(),{{cache:"no-store"}}).then(function(r){{return r.text()}}).then(function(t){{var m=t.match(/name="pud-build" content="([0-9]+)"/);if(m&&m[1]!==v){{sessionStorage.setItem(k+location.pathname,"1");location.reload()}}}}).catch(function(){{}})}}catch(e){{}}}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Antonio:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/pud.css?v={VER}">
</head>
<body>
{chrome(fn, solid)}
<main id="main">
{body}
</main>
{FOOT}
<script src="assets/projects.js?v={VER}"></script>
<script src="assets/pud.js?v={VER}"></script>
</body>
</html>'''
    open(os.path.join(OUT, fn), 'w').write(html)

def landing(h1, p, crumb='', hero=None, wide=False):
    h = ''
    if hero:
        img, cap, slug = hero[:3]
        pos = hero[3] if len(hero) > 3 else '50% 50%'
        if slug:
            h = f'''<a class="land-hero" href="project.html#{slug}"><div class="lh-img" data-px="0.1"><img src="img/{img}" alt="{cap}" style="object-position:{pos}"></div><span class="lh-cap gut">{cap} <span>→</span></span></a>'''
        else:
            h = f'''<div class="land-hero"><div class="lh-img" data-px="0.1"><img src="img/{img}" alt="{cap}" style="object-position:{pos}"></div><span class="lh-cap gut">{cap}</span></div>'''
    if wide:
        return f'''<section class="landing landing-w gut">{crumb}<h1 class="rv">{h1}</h1><div class="row2"><div></div><p class="rv d1">{p}</p></div></section>{h}'''
    return f'''<section class="landing gut"><div class="row2"><div>{crumb}<h1 class="rv">{h1}</h1></div><p class="rv d1">{p}</p></div></section>{h}'''

# ---------------- HOME ----------------
page('index.html', 'PUD Consultants — 60 Years of Shaping Sustainable Cities', f"""
<section class="intro gut">
  <div class="lbl o rv">1966 – 2026 · 60 Years</div>
  <h1 class="intro-h rv d1">PUD is a multidisciplinary planning and design practice, shaping sustainable cities, destinations and sacred landscapes across the region since 1966.</h1>
</section>
<section class="strip" id="strip" aria-label="Featured project">
  <div class="strip-stage">
    <a class="s-side s-l" href="project-pyramids-plateau.html" tabindex="-1"><img src="img/pyramids-plateau.jpg" alt="Pyramids Plateau Destination"></a>
    <a class="s-main" href="project-cairo-media-city.html"><img src="img/cairo-media-city.jpg?v=2" alt="Cairo Media City, Giza">
      <span class="s-cap"><span class="lbl">60 Years · Cairo Media City, Giza</span><span class="s-h">Sixty years of building sustainable cities — the legacy continues, the future begins.</span></span></a>
    <a class="s-side s-r" href="project-alamein-riviera.html" tabindex="-1"><img src="img/alamein-riviera.jpg" alt="Alamein Riviera"></a>
  </div>
</section>

<section class="sec gut disc-sec">
  <div class="lbl mut">Disciplines</div>
  <div class="disc" id="disc"></div>
  <div class="disc-float" id="discFloat" aria-hidden="true"><img alt=""></div>
</section>

<section class="gut news-head"><span class="lbl mut">Latest News</span><span class="news-links"><a href="https://www.linkedin.com/in/amr-attia-9181898/" target="_blank" rel="noopener" class="more">Follow on LinkedIn <span>↗</span></a><a href="news.html" class="more">All news <span>→</span></a></span></section>
<div class="wide" id="wideNews"><div class="wide-track"></div><button class="wide-btn prev" aria-label="Previous">←</button><button class="wide-btn next" aria-label="Next">→</button></div>

<section class="sec gut culture story">
  <div class="row2"><div class="lbl">Our Story</div><div>
    <p class="pull rv" style="margin-top:0">Every legacy begins with a vision.</p>
    <p class="body rv d1" style="max-width:62ch;margin-top:18px">In 1966, Prof. Abdallah Abdel Aziz Attia founded PUD with a belief that planning should serve people, land and history. Sixty years on, the vision continues through Prof. Dr. Amr A. Attia — from Alex to Aswan, and across the region.</p>
    <div class="story-stats rv d2"><div><b data-count="1966" data-from="1900">1966</b><span>Founded in Cairo</span></div><div><b data-count="150" data-suf="+">150+</b><span>Projects</span></div><div><b data-count="11">11</b><span>Countries</span></div><div><b data-count="60" data-suf="+">60+</b><span>Cities</span></div></div>
    <a class="btn rv" href="60-years.html" style="margin-top:28px">Read the 60-year story {AR}</a> <a class="btn ghost rv" href="60-years.html#timeline" style="margin-top:28px">Explore the timeline {AR}</a>
  </div></div>
</section>

<section class="journey" id="journey" aria-label="Project map">
  <div class="j-stage">
    <div class="j-text">
      <span class="lbl">Where we work</span>
      <div class="j-tabs"><button class="chip on" data-go="0">Egypt</button><button class="chip" data-go="1">Saudi Arabia</button><button class="chip" data-go="2">Beyond borders</button></div>
      <div class="steps">
        <div class="step on" data-step="0"><div class="lbl o">Mediterranean · Red Sea · Nile</div><h3>From Alex to Aswan.</h3><p>From Alexandria to the Libyan border along the Mediterranean, from Marsa Alam to the Gulf of Suez and the Gulf of Aqaba, and from Aswan to the Delta along both banks of the Nile Valley.</p><div class="tags" data-tags="egypt"></div></div>
        <div class="step" data-step="1"><div class="lbl o">Red Sea · Arabian Gulf</div><h3>Then across the Red Sea.</h3><p>From Jazan to NEOM along the Red Sea and to Al Khafji on the Arabian Gulf, including the holy sites development at Al Mashaaer, welcoming 50,000+ pilgrims daily.</p><div class="tags" data-tags="ksa"></div></div>
        <div class="step" data-step="2"><div class="lbl o">11 countries</div><h3>Every place has its own rhythm.</h3><p>Kuwait, Syria, Iraq, the UAE, Iran, Palestine, Cameroon, Gambia and Germany: the journey keeps expanding.</p><div class="tags" data-tags="intl"></div></div>
      </div>
    </div>
    <div class="j-map"><svg id="map" viewBox="0 140 364 280" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Map of PUD project locations"></svg><div class="far" id="far"><span class="far-l">Beyond this map</span><span class="far-i"><b>↖</b>Germany</span><span class="far-i"><b>←</b>Gambia</span><a class="far-i" href="project-massoumbou-diwom.html"><b>↙</b>Cameroon · Massoumbou–Diwom</a></div></div>
  </div>
</section>




<section class="gut" style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;padding-bottom:22px">
  <h2 class="h-l rv">Selected projects</h2><a class="btn rv" href="projects.html">All projects {AR}</a>
</section>
{CAR('featCar')}

<section class="sec gut logos" aria-label="Clients and partners">
  <div class="row2"><div class="lbl">Clients &amp; partners</div><div>
    <h2 class="h-m rv" style="max-width:22ch">Trusted by clients. Built with partners.</h2>
    <p class="body rv d1" style="margin-top:14px;max-width:60ch">100+ clients and 90+ collaborations across six decades — from ministries and sovereign funds to the world’s leading design firms.</p>
  </div></div>
</section>
<div class="lg-bars">
  <div class="lg-cap gut"><span class="lbl mut">Our trusted clients</span></div>
  <div class="lg-row"><ul class="lg-track"><li><img src="img/logos/c01.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c02.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c03.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c04.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c05.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c06.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c07.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c08.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c09.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c10.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c11.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c12.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c13.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c14.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c15.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c16.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c17.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c18.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c19.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c20.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c21.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c22.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c23.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c24.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c25.jpg" alt="" loading="lazy"></li></ul><ul class="lg-track" aria-hidden="true"><li><img src="img/logos/c01.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c02.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c03.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c04.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c05.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c06.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c07.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c08.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c09.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c10.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c11.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c12.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c13.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c14.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c15.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c16.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c17.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c18.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c19.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c20.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c21.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c22.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c23.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c24.jpg" alt="" loading="lazy"></li><li><img src="img/logos/c25.jpg" alt="" loading="lazy"></li></ul></div>
  <div class="lg-cap gut"><span class="lbl mut">Partners &amp; collaborations</span></div>
  <div class="lg-row rev"><ul class="lg-track"><li><img src="img/logos/p01.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p02.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p03.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p04.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p05.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p06.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p07.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p08.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p09.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p10.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p11.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p12.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p13.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p14.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p15.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p16.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p17.jpg" alt="" loading="lazy"></li></ul><ul class="lg-track" aria-hidden="true"><li><img src="img/logos/p01.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p02.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p03.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p04.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p05.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p06.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p07.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p08.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p09.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p10.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p11.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p12.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p13.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p14.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p15.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p16.jpg" alt="" loading="lazy"></li><li><img src="img/logos/p17.jpg" alt="" loading="lazy"></li></ul></div>
</div>

<section class="sec gut ed">
  <div class="ed-txt rv"><div class="lbl">Our approach</div><p>We don’t believe in one-size-fits-all. Every project starts by listening, then curates the best-fit minds — planners, architects, economists and global experts — around a shared mission. <a href="about.html#approach" class="ul">Learn more about our approach</a></p></div>
  <a class="ed-img rv ed-link" data-px="0.06" href="project-kidana-al-khaif.html"><img src="img/kidana-al-khaif.jpg" alt="Kidana Al Khaif, Mina" loading="lazy"><span class="ed-cap">Kidana Al Khaif · Mina, Makkah</span></a>
</section>
<section class="gut ed ed-2">
  <a class="ed-img rv ed-link" data-px="0.06" href="project-heliopark.html"><img src="img/heliopark.jpg" alt="Heliopark, New Cairo" loading="lazy"><span class="ed-cap">Heliopark · New Cairo</span></a>
  <div class="ed-txt rv"><div class="lbl">Sustainability and responsibility</div><p>From mega cities to sacred landscapes, sustainability is a lens of transformation — responsible land use, social inclusion, cultural continuity and green building standards. <a href="sustainability.html" class="ul">Our commitment</a></p></div>
</section>

<section class="sec gut culture">
  <div class="row2"><div class="lbl">Our Culture</div><div>
    <p class="pull rv" style="margin-top:0">We don’t just gather experts. We orchestrate brilliance.</p>
    <div class="meta" style="font-size:14px">Prof. Dr. Amr A. Attia, CEO</div>
    <a class="btn rv" href="people.html" style="margin-top:28px">Meet our people {AR}</a>
  </div></div>
</section>

<section class="y60" id="next" aria-label="60 years of vision, experience and building for a better future">
  <div class="y60-stage">
    <div class="y60-bg" aria-hidden="true">60</div>
    <div class="y60-k gut"><span class="chap-n">1966 – 2026</span> <span class="lbl">The legacy continues</span></div>
    <h2 class="y60-h gut"><span class="y60-fix">60 years of</span>
      <span class="y60-w"><span class="on">vision.</span><span>experience.</span><span>building for a better future.</span></span></h2>
    <div class="y60-foot gut"><div class="y60-dots"><i class="on"></i><i></i><i></i></div><p class="meta">PUD · 60 Years of Shaping Sustainable Cities · <a href="60-years.html" class="ul">Read the story →</a></p></div>
  </div>
</section>

""", solid=False)

page('projects.html', 'Projects: Master Plans, Destinations & Urban Design | PUD Consultants', landing('Projects', 'Breadth, with depth: from regional visions to city-making, from urban places to coastal destinations and the Holy Sites.', hero=('al-rabita-competition.jpg','Al Rabita Pre-Concept Design Competition · Mina, Makkah','al-rabita-competition')) + f'''
<section class="sec tight gut">
  <div class="row2"><div class="lbl">Expertise</div><div>
    <h2 class="h-m rv" style="max-width:24ch">Every place has its own rhythm. Every challenge its own context.</h2>
    <p class="body rv d1" style="margin-top:16px">Our work crosses planning, design and heritage — and each project brings together the best-fit minds from PUD’s network of planners, architects, economists and specialists.</p>
    <div class="ptypes" id="ptypes"></div>
  </div></div>
</section>
<div class="fbar gut" id="fbar"><button class="fbtn" id="fbtn" aria-expanded="false" aria-controls="fpanel"><svg viewBox="0 0 24 24"><path d="M3 6h18M6 12h12M10 18h4"/></svg>Filter by</button><div class="fsum" id="fsum"></div></div>
<div class="fpanel gut" id="fpanel"><div><div class="fgrid">
  <div><h5>Region</h5><div class="chips" id="fRegion"></div></div>
  <div><h5>Project type</h5><div class="chips" id="fType"></div></div>
  <div><h5>Era</h5><div class="chips" id="fEra"></div></div>
</div></div></div>
<div class="pgrid" id="pIndex"></div>
<div class="empty" id="pEmpty" hidden>No results were found matching your selection.</div>
{PROJ_INDEX}
''')

# ---------------- PROJECT DETAIL ----------------
page('project.html', 'Project | PUD Consultants', noindex=True, body=f'''<article id="pDetail"></article>
<section class="gut" style="padding:60px 0 22px"><h2 class="h-m">Related projects</h2></section>
{CAR('relCar')}
<div style="height:80px"></div>''')

page('article.html', 'News | PUD Consultants', noindex=True, body='''<article id="aDetail"></article>
<section class="gut" style="padding:60px 0 22px"><h2 class="h-m">More news</h2></section>
<div class="gut more-news" id="moreNews"></div>
<div style="height:80px"></div>''')

# ---------------- 60 YEARS ----------------
page('60-years.html', '60 Years of Shaping Sustainable Cities, 1966–2026 | PUD Consultants', f'''
<header class="st-head gut">
  <div class="lbl o rv">Story · 1966 – 2026</div>
  <h1 class="rv d1" style="margin-top:14px">Sixty years of building sustainable cities.</h1>
  <p class="dek rv d2">Since 1966, PUD has helped shape places where people live, work and connect. Every project begins with questioning: how can we make places work better for people while respecting the land, culture and history?</p>
  <div class="st-kick rv d3"><span class="chap-n">60</span> <span class="lbl">The next chapter belongs to the generations who will shape the future</span></div>
</header>
<section class="z60" aria-label="Sixty years, seen through our projects">
  <div class="z60-stage">
    <div class="z60-ph"><img src="img/pyramids-plateau.jpg" alt="" class=on><img src="img/alamein-riviera.jpg" alt=""><img src="img/al-mashaaer.jpg" alt=""><img src="img/cairo-media-city.jpg?v=2" alt=""><img src="img/khaybar-heritage.jpg" alt=""></div>
    <div class="z60-mask" aria-hidden="true"><span>60</span></div>
    <div class="z60-cap gut"><span class="lbl">Scroll</span><span class="meta" id="z60Name">Pyramids Plateau Destination · Giza</span></div>
    <div class="z60-end gut"><b>1966 — 2026</b><p>150+ projects · 11 countries · 60+ cities</p></div>
  </div>
</section>
<section class="sec gut">
  <div class="stats">
    <div class="rv"><b data-count="150" data-suf="+">0</b><span>Projects</span></div>
    <div class="rv d1"><b data-count="11">0</b><span>Countries</span></div>
    <div class="rv d2"><b data-count="60" data-suf="+">0</b><span>Cities &amp; destinations</span></div>
    <div class="rv d3"><b>~<span data-count="6" style="font:inherit;color:inherit">0</span>M</b><span>Lives touched</span></div>
  </div>
  <div class="tnn">
    <a class="tnn-c rv" href="project-hilton-dahab.html"><div class="tnn-i" data-px="0.05"><img src="img/hilton-dahab.jpg" alt="Hilton Dahab Village" loading="lazy"></div><div class="tnn-t"><span class="lbl">Then</span><b>1991</b><h3>Hilton Dahab Village</h3><p>Gulf of Aqaba, Egypt</p></div></a>
    <a class="tnn-c rv d1" href="project-pyramids-plateau.html"><div class="tnn-i" data-px="0.05"><img src="img/pyramids-plateau.jpg" alt="Pyramids Plateau Destination" loading="lazy"></div><div class="tnn-t"><span class="lbl">Now</span><b>2025</b><h3>Pyramids Plateau Destination</h3><p>Giza, Egypt</p></div></a>
    <a class="tnn-c rv d2" href="project-cairo-media-city.html"><div class="tnn-i" data-px="0.05"><img src="img/cairo-media-city.jpg?v=2" alt="Cairo Media City" loading="lazy"></div><div class="tnn-t"><span class="lbl">Next</span><b>2026</b><h3>Cairo Media City</h3><p>Giza, Egypt</p></div></a>
  </div>
</section>

<section class="chap gut" id="ch1">
  <div class="prose">
    <span class="chap-n">01</span><span class="lbl">The founder · 1966</span>
    <h2 class="rv">Every legacy begins with a vision.</h2>
    <p class="rv">That vision did not begin today. Everything we build today has a root. In 1966, Prof. Abdallah Abdel Aziz Attia founded PUD with a strong belief in the synergy between people and their natural and cultural environments.</p>
    <figure class="fig rv" style="margin:30px 0;aspect-ratio:4/3;max-width:420px"><img src="img/founder.jpg" alt="Prof. Abdallah Abdel Aziz Attia" loading="lazy" style="object-position:50% 25%;filter:grayscale(1)"></figure>
    <p class="rv">He pioneered an architectural style rooted in local traditions and social responsibility, introducing the “cubed house” model that remains influential today, and reshaped architectural education in the region. His vision took shape in three pioneering projects.</p>
  </div>
  <div class="trio">
    <a href="project-hilton-dahab.html" class="rv"><div class="th" data-px="0.06"><img src="img/hilton-dahab.jpg" alt="" loading="lazy" style="height:112%"></div><h3>Hilton Dahab Village</h3><p>Gulf of Aqaba · One of Dahab’s early international beach resorts.</p></a>
    <a href="project-marina-el-alamein.html" class="rv d1"><div class="th" data-px="0.06"><img src="img/marina-el-alamein.jpg" alt="" loading="lazy" style="height:112%"></div><h3>Marina El-Alamein</h3><p>North Coast · The first large-scale tourism project on Egypt’s North West Coast.</p></a>
    <a href="project-tut-amoun-village.html" class="rv d2"><div class="th" data-px="0.06"><img src="img/tut-amoun-village.jpg" alt="" loading="lazy" style="height:112%"></div><h3>Tut Amoun Village</h3><p>Lake Nasser, Aswan · Egypt’s first tourist village. Best Tourist Project in Egypt, Rome Biennale 1992.</p></a>
  </div>
</section>

<section class="chap gut" id="ch2">
  <div class="lead-grid">
    <div class="portrait ph rv"><img src="img/amr-attia-2.jpg" alt="Prof. Dr. Amr A. Attia" loading="lazy" style="object-position:40% 30%"></div>
    <div class="prose" style="margin:0">
      <span class="chap-n">02</span><span class="lbl">The new chapter</span>
      <h2 class="rv">A great leader builds beyond today.</h2>
      <p class="rv">A vision becomes a legacy when it inspires others to carry it forward. That vision continues through Prof. Dr. Amr A. Attia.</p>
      <p class="rv">Building on the foundations established by his father, he has carried PUD into a new chapter — expanding its reach, strengthening its multidisciplinary expertise and connecting regional knowledge with international collaboration. In 2018 he founded PUD Saudi to expand the firm’s regional impact.</p>
      <div class="tags2 rv"><span>BSc Arch, ASU</span><span>MSc Econ, UCL</span><span>PhD Planning, London</span><span>Eisenhower Fellow</span><span>Aspen Institute</span><span>Former Principal Director, AECOM</span><span>Former VP Strategic Development, WATG</span><span>Board Member, SEA</span><span>Grand Egyptian Museum Technical Committee</span></div>
    </div>
  </div>
  <div class="lr-head rv"><span class="lbl">A new scale of ambition</span><span class="meta">From city frameworks to the Holy Sites</span></div>
  <div class="lead-row"><a class="lr-c rv" href="project-saudi-railway.html"><div class="th"><img src="img/saudi-railway.jpg" alt="Saudi Railway Land Optimisation" loading="lazy"></div><div class="meta"><b>2018</b> · Kingdom of Saudi Arabia</div><h3>Saudi Railway Land Optimisation</h3></a><a class="lr-c rv d1" href="project-alula-framework.html"><div class="th"><img src="img/alula-framework.jpg" alt="AlUla County Framework Plan" loading="lazy"></div><div class="meta"><b>2019</b> · AlUla, KSA</div><h3>AlUla County Framework Plan</h3></a><a class="lr-c rv d2" href="project-alamein-riviera.html"><div class="th"><img src="img/alamein-riviera.jpg" alt="Alamein Riviera" loading="lazy"></div><div class="meta"><b>2022</b> · North Coast, Egypt</div><h3>Alamein Riviera</h3></a><a class="lr-c rv d3" href="project-al-mashaaer.html"><div class="th"><img src="img/al-mashaaer.jpg" alt="Al Mashaaer Al Mugaddassah" loading="lazy"></div><div class="meta"><b>2024</b> · Makkah, KSA</div><h3>Al Mashaaer Al Mugaddassah</h3></a></div>
</section>

<section class="interlude" aria-label="Jabal Thabeer Park, Mina">
  <div class="il-img" data-px="0.18"><img src="img/jabal-thabeer-park.jpg" alt="Jabal Thabeer Park, Mina" loading="lazy"></div>
  <div class="il-txt gut"><p class="rv">Every place has its own rhythm.<br>Every challenge, its own context.</p><a class="meta rv d1" href="project-jabal-thabeer-park.html">Jabal Thabeer Park · Mina, Makkah →</a></div>
</section>

<section class="chap" id="ch3">
  <div class="prose gut">
    <span class="chap-n">03</span><span class="lbl">Collaboration</span>
    <h2 class="rv">Global minds. One mission.</h2>
    <p class="rv">Across six decades, PUD has worked with more than 100 clients and built over 90 collaborations, including 25+ individual experts from the SMEs &amp; CMPs Advisory Group — bringing together governments, public institutions, developers, strategic consultants, planners, architects, engineers, researchers and delivery partners. Each collaboration adds a different perspective to a shared vision.</p>
  </div>
  <div class="gut" style="margin:50px 0"><div class="stats" style="grid-template-columns:repeat(3,minmax(0,1fr))">
    <div><b data-count="100" data-suf="+">0</b><span>Clients</span></div><div><b data-count="90" data-suf="+">0</b><span>Collaborations</span></div><div><b data-count="25" data-suf="+">0</b><span>Individual experts</span></div></div></div>
  <div class="gut cp"><div class="lr-head rv" style="margin-top:0"><span class="lbl">Collaboration in practice</span><span class="meta">Global partners, local knowledge</span></div><div class="cp-grid"><a class="cp-c rv" href="project-kidana-al-khaif.html"><div class="th"><img src="img/kidana-al-khaif.jpg" alt="Kidana Al Khaif" loading="lazy"></div><div class="lbl o">With SOM &amp; BuroHappold</div><h3>Kidana Al Khaif</h3><p class="meta">Mina, Makkah</p></a><a class="cp-c rv d1" href="project-pyramids-plateau.html"><div class="th"><img src="img/li-pyramids.jpg" alt="Pyramids Plateau Destination" loading="lazy"></div><div class="lbl o">With WATG &amp; Shaker Group</div><h3>Pyramids Plateau Destination</h3><p class="meta">Giza, Egypt</p></a><a class="cp-c rv d2" href="project-alula-infrastructure.html"><div class="th"><img src="img/alula-infrastructure.jpg" alt="AlUla Infrastructure Master Plan" loading="lazy"></div><div class="lbl o">With AECOM</div><h3>AlUla Infrastructure Master Plan</h3><p class="meta">AlUla, KSA</p></a></div></div>
  <div class="marq"><div class="mtrack" id="mq1" data-mx="-0.5"></div></div>
  <div class="marq"><div class="mtrack" id="mq2" data-mx="0.5"></div></div>
  <div class="marq"><div class="mtrack" id="mq3" data-mx="-0.4"></div></div>
  <div class="gut"><p class="pull rv" style="margin-left:auto;margin-right:auto;text-align:center">We don’t just gather experts. We orchestrate brilliance.</p><p class="meta" style="text-align:center;font-size:14px">Prof. Dr. Amr A. Attia</p></div>
</section>

<section class="journey" id="journey" aria-label="Project map">
  <div class="j-stage">
    <div class="j-text">
      <span class="chap-n">04</span><span class="lbl">The journey</span>
      <div class="j-tabs"><button class="chip on" data-go="0">Egypt</button><button class="chip" data-go="1">Saudi Arabia</button><button class="chip" data-go="2">Beyond borders</button></div>
      <div class="steps">
        <div class="step on" data-step="0"><div class="lbl o">Mediterranean · Red Sea · Nile</div><h3>From Alex to Aswan.</h3><p>From Alexandria to the Libyan border along the Mediterranean, from Marsa Alam to the Gulf of Suez and the Gulf of Aqaba, and from Aswan to the Delta along both banks of the Nile Valley.</p><div class="tags" data-tags="egypt"></div></div>
        <div class="step" data-step="1"><div class="lbl o">Red Sea · Arabian Gulf</div><h3>Then across the Red Sea.</h3><p>From Jazan to NEOM along the Red Sea and to Al Khafji on the Arabian Gulf, including the holy sites development at Al Mashaaer, welcoming 50,000+ pilgrims daily.</p><div class="tags" data-tags="ksa"></div></div>
        <div class="step" data-step="2"><div class="lbl o">11 countries</div><h3>Every place has its own rhythm.</h3><p>Kuwait, Syria, Iraq, the UAE, Iran, Palestine, Cameroon, Gambia and Germany: the journey keeps expanding.</p><div class="tags" data-tags="intl"></div></div>
      </div>
    </div>
    <div class="j-map"><svg id="map" viewBox="0 140 364 280" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Map of PUD project locations"></svg><div class="far" id="far"><span class="far-l">Beyond this map</span><span class="far-i"><b>↖</b>Germany</span><span class="far-i"><b>←</b>Gambia</span><a class="far-i" href="project-massoumbou-diwom.html"><b>↙</b>Cameroon · Massoumbou–Diwom</a></div></div>
  </div>
</section>

<section class="film" aria-label="Places along the journey">
  <div class="gut lr-head" style="margin-top:0"><span class="lbl">Places along the journey</span><span class="fm-nav"><button class="jt-btn fm-prev" aria-label="Previous">←</button><button class="jt-btn fm-next" aria-label="Next">→</button></span></div>
  <div class="fm-track"><a class="fm-c" href="project-alamein-riviera.html"><div class="th"><img src="img/alamein-riviera.jpg" alt="Alamein Riviera" loading="lazy"></div><div class="meta">Mediterranean, Egypt</div><h3>Alamein Riviera</h3></a><a class="fm-c" href="project-port-ghalib-phase-2.html"><div class="th"><img src="img/port-ghalib-phase-2.jpg" alt="Port Ghalib" loading="lazy"></div><div class="meta">Red Sea, Egypt</div><h3>Port Ghalib</h3></a><a class="fm-c" href="project-prince-talal-hurghada.html"><div class="th"><img src="img/prince-talal-hurghada.jpg" alt="HRH Prince Talal Development" loading="lazy"></div><div class="meta">Hurghada, Egypt</div><h3>HRH Prince Talal Development</h3></a><a class="fm-c" href="project-pyramids-plateau.html"><div class="th"><img src="img/pyramids-plateau.jpg" alt="Pyramids Plateau" loading="lazy"></div><div class="meta">Giza, Egypt</div><h3>Pyramids Plateau</h3></a><a class="fm-c" href="project-sumou-boulevard.html"><div class="th"><img src="img/sumou-boulevard.jpg" alt="Sumou Boulevard" loading="lazy"></div><div class="meta">New Cairo, Egypt</div><h3>Sumou Boulevard</h3></a><a class="fm-c" href="project-al-rabita-competition.html"><div class="th"><img src="img/al-rabita-competition.jpg" alt="Al Rabita" loading="lazy"></div><div class="meta">Mina, KSA</div><h3>Al Rabita</h3></a><a class="fm-c" href="project-khaybar-heritage.html"><div class="th"><img src="img/khaybar-heritage.jpg" alt="Khaybar Heritage Area" loading="lazy"></div><div class="meta">AlUla, KSA</div><h3>Khaybar Heritage Area</h3></a><a class="fm-c" href="project-sharaan.html"><div class="th"><img src="img/sharaan.jpg" alt="Sharaan Nature Reserve" loading="lazy"></div><div class="meta">AlUla, KSA</div><h3>Sharaan Nature Reserve</h3></a><a class="fm-c" href="project-jazan-economic-city.html"><div class="th"><img src="img/jazan-economic-city.jpg" alt="Jazan Economic City" loading="lazy"></div><div class="meta">Jazan, KSA</div><h3>Jazan Economic City</h3></a><a class="fm-c" href="project-fawaz-alhokair-estate.html"><div class="th"><img src="img/fawaz-alhokair-estate.jpg" alt="Fawaz Alhokair Estate" loading="lazy"></div><div class="meta">Riyadh, KSA</div><h3>Fawaz Alhokair Estate</h3></a><a class="fm-c" href="project-bvlgari-mansion.html"><div class="th"><img src="img/bvlgari-mansion.jpg" alt="Bvlgari Mansion" loading="lazy"></div><div class="meta">Dubai, UAE</div><h3>Bvlgari Mansion</h3></a><a class="fm-c" href="project-maria-heights.html"><div class="th"><img src="img/maria-heights.jpg" alt="Maria Heights" loading="lazy"></div><div class="meta">Homs, Syria</div><h3>Maria Heights</h3></a><a class="fm-c" href="project-massoumbou-diwom.html"><div class="th"><img src="img/massoumbou-diwom.jpg" alt="Massoumbou–Diwom" loading="lazy"></div><div class="meta">Cameroon</div><h3>Massoumbou–Diwom</h3></a><div class="fm-end"></div></div>
</section>

<section class="sec gut jt" id="timeline" aria-label="Six decades timeline">
  <div style="margin-bottom:40px"><span class="chap-n">05</span> <span class="lbl">Six decades</span><h2 class="h-l" style="margin-top:10px">A legacy is not simply inherited. It is developed, tested and carried forward.</h2></div>
  <div class="jt-stage">
    <div class="jt-year" aria-hidden="true"><span id="jtYear">1966</span></div>
    <a class="jt-media" id="jtMedia" href="60-years.html"></a>
    <div class="jt-text" aria-live="polite">
      <div class="lbl o" id="jtKicker"></div>
      <h3 id="jtTitle"></h3>
      <p id="jtDesc"></p>
      <div class="jt-nav"><button class="jt-btn" id="jtPrev" aria-label="Previous milestone">←</button><span class="jt-count" id="jtCount"></span><button class="jt-btn" id="jtNext" aria-label="Next milestone">→</button></div>
    </div>
  </div>
  <div class="jt-rail" id="jtRail" role="slider" tabindex="0" aria-label="Timeline 1966 to 2026" aria-valuemin="1966" aria-valuemax="2026" aria-valuenow="1966">
    <div class="jt-line"><i id="jtFill"></i></div>
    <div class="jt-ticks" id="jtTicks"></div>
    <div class="jt-handle" id="jtHandle"><span></span></div>
  </div>
</section>

<section class="chap gut recog">
  <figure class="rc-img rv"><img src="img/founder-2.jpg" alt="International Star for Leadership in Quality, Paris 2010" loading="lazy"><figcaption class="meta">International Star for Leadership in Quality · Paris, 2010</figcaption></figure>
  <div class="prose" style="margin:0">
    <span class="lbl">Recognition</span>
    <h2 class="rv">20+ awards, with first- and second-place prizes.</h2>
    <p class="rv">Across this journey, PUD’s record includes the International Star for Leadership in Quality, Paris 2010, featured on the cover of BeattON World Report, May 2010.</p>
    <a class="btn rv" href="about.html#awards">All awards {AR}</a>
  </div>
</section>

<section class="nextb gut" aria-label="Building next">
  <div class="lr-head rv" style="margin-top:0"><span class="lbl">Already building the next chapter</span><a class="meta" href="projects.html">All projects →</a></div>
  <div class="nx-grid"><a class="nx-c rv" href="project-cairo-media-city.html"><div class="th" data-px="0.05"><img src="img/cairo-media-city.jpg?v=2" alt="Cairo Media City" loading="lazy"></div><div class="nx-t"><span class="lbl">Giza, Egypt</span><h3>Cairo Media City</h3></div></a><a class="nx-c rv d1" href="project-sumou-boulevard.html"><div class="th" data-px="0.05"><img src="img/sumou-boulevard.jpg" alt="Sumou Boulevard" loading="lazy"></div><div class="nx-t"><span class="lbl">New Cairo, Egypt</span><h3>Sumou Boulevard</h3></div></a><a class="nx-c rv d2" href="project-new-administrative-capital.html"><div class="th" data-px="0.05"><img src="img/new-administrative-capital.jpg" alt="New Administrative Capital" loading="lazy"></div><div class="nx-t"><span class="lbl">Greater Cairo, Egypt</span><h3>New Administrative Capital</h3></div></a><a class="nx-c rv d3" href="project-massoumbou-diwom.html"><div class="th" data-px="0.05"><img src="img/massoumbou-diwom.jpg" alt="Massoumbou–Diwom" loading="lazy"></div><div class="nx-t"><span class="lbl">Cameroon</span><h3>Massoumbou–Diwom</h3></div></a></div>
</section>

<section class="y60" id="next" aria-label="60 years of vision, experience and building for a better future">
  <div class="y60-stage">
    <div class="y60-bg" aria-hidden="true">60</div>
    <div class="y60-k gut"><span class="chap-n">06</span> <span class="lbl">The legacy continues</span></div>
    <h2 class="y60-h gut"><span class="y60-fix">60 years of</span>
      <span class="y60-w"><span class="on">vision.</span><span>experience.</span><span>building for a better future.</span></span></h2>
    <div class="y60-foot gut"><div class="y60-dots"><i class="on"></i><i></i><i></i></div><p class="meta">PUD · 60 Years of Shaping Sustainable Cities · The future begins.</p></div>
  </div>
</section>
''', solid=False)

PEOPLE_LD=[{'@type':'Person','name':'Prof. Dr. Amr Abdalla Abdelaziz Attia','alternateName':'Amr Attia','jobTitle':'CEO & Principal','worksFor':{'@id':BASE+'#org'},'image':BASE+'img/amr-attia.jpg','alumniOf':['Ain Shams University','University College London'],'award':'Eisenhower Fellowship (2007)','sameAs':['https://www.linkedin.com/in/amr-attia-9181898/'],'description':'Professor of Architecture & Urban Planning at Ain Shams University; Principal and Managing Partner of PUD Consultants; former VP Strategic Development MEA at WATG and Principal Director at AECOM.'},{'@type':'Person','name':'Prof. Abdallah Abdel Aziz Attia','jobTitle':'Founder','foundingDate':'1966','image':BASE+'img/founder.jpg','description':'Founder of PUD Consultants in 1966; pioneer of an urban style rooted in local tradition and affordable housing.'}]
# ---------------- PEOPLE ----------------
page('people.html', 'People & Leadership | PUD Consultants', landing('People', 'Our strength lies in our people: leaders who guide our mission, uphold our values and drive our vision in every region we work.', hero=('people-gem.jpg','The team at the Grand Egyptian Museum · Giza',None,'50% 36%')) + f'''
<section class="sec gut">
  <div class="row2"><div class="lbl">Global leadership</div><div>
    <p class="purpose rv">We value the relationship between people and their environment, and work in partnership with clients who value quality, safety and technical expertise.</p>
  </div></div>
</section>
<section class="sec tight gut vmv">
  <div class="vmv-grid">
    <div class="vmv-c rv"><span class="chap-n">01</span><h3>Vision</h3><p>To build lasting cooperation in a spirit of partnership with our clients, adding value to their objectives through the quality of our work.</p></div>
    <div class="vmv-c rv d1"><span class="chap-n">02</span><h3>Mission</h3><p>To meet every challenge with safe, reliable and innovative solutions, and to trust our skilled, multi-local teams to deliver sustainable development for our company and the communities where we work.</p></div>
    <div class="vmv-c rv d2"><span class="chap-n">03</span><h3>Values</h3><p>Core values built on integrity, giving us an ethical and responsible framework for every project and every partnership.</p></div>
  </div>
</section>
<section class="sec gut">
  <div class="lead-grid">
    <div class="portrait ph rv"><img src="img/founder.jpg" alt="Prof. Abdallah Abdel Aziz Attia"></div>
    <div><div class="lbl o">Founder · 1966</div><h2 class="h-l rv" style="margin:10px 0 20px">Prof. Abdallah Abdel Aziz Attia</h2>
      <p class="body rv">A visionary in shaping the urban fabric of the MENA region. He founded PUD on the synergy between people and their natural and cultural environments, pioneered an architectural style rooted in local tradition and social responsibility — introducing the “cubed house” model — and left an enduring impact on both the built environment and academia.</p>
      <p class="body rv">He developed a new urban style tailored to local places and affordable housing — including his pioneering concept of cubed houses, still popular today — and shaped how planning and architecture are taught in Egyptian universities.</p></div>
  </div>
</section>
<section class="sec gut" style="padding-top:0">
  <div class="lead-grid">
    <div class="portrait ph rv"><img src="img/amr-attia.jpg" alt="Prof. Dr. Amr A. Attia"></div>
    <div><div class="lbl o">CEO &amp; Principal</div><h2 class="h-l rv" style="margin:10px 0 20px">Prof. Dr. Amr Abdalla Abdelaziz Attia</h2>
      <p class="body rv">Visionary urban planner and sustainable tourism development ambassador, blending over 30 years of academic and industry experience. As CEO of PUD Consultants and a Professor of Urban Planning at Ain Shams University, he drives innovative, sustainable urban development across the Middle East.</p>
      <p class="body rv">Formerly a Principal Director at AECOM, he has led award-winning projects and co-chaired global forums on livability and urban design. He is known for advancing smart cities, affordable housing and inclusive growth, and founded PUD Saudi in 2018.</p>
      <div class="roles rv"><div><h5>Current roles</h5><ul><li>Professor of Architecture &amp; Urban Planning, Ain Shams University, Cairo</li><li>Principal and Managing Partner, PUD Consultants (Cairo – Riyadh – Dubai)</li><li>Board Member, Society of Egyptian Architects (SEA)</li><li>Vice President, NAGA Architects</li><li>Eisenhower Fellow, 2007</li></ul></div>
      <div><h5>Previously</h5><ul><li>Vice President, Strategic Development, MEA, WATG</li><li>Principal Director, Design, Planning + Economics, AECOM</li><li>Managing Director, Consultancy Unit for Planning &amp; Urban Design, Ain Shams University</li><li>Technical Committee Member, Grand Egyptian Museum</li></ul></div></div>
      <div class="tags2"><span>BSc Arch, ASU</span><span>MSc Econ, UCL</span><span>PhD Planning, London</span><span>Eisenhower Fellow</span><span>Aspen Institute Alumni</span></div></div>
  </div>
</section>
<section class="gut" style="padding-bottom:22px"><h2 class="h-l rv">Key staff</h2><p class="body rv" style="margin-top:12px">The permanent core driving PUD’s long-term vision, ensuring continuity, strategic leadership and quality from advisory orchestration to delivery.</p></section>
<div class="ppl" id="staff"></div>
<section class="sec gut eco">
  <div class="row2"><div class="lbl">Stronger together</div><div>
    <h2 class="h-l rv" style="max-width:18ch">Our strategic partners</h2>
    <p class="body rv" style="margin-top:14px;max-width:60ch">A collaborative consultants’ network that brings finance, engineering, law and sustainability expertise to every engagement.</p>
  </div></div>
  <div class="xp-grid"><div class="xp rv d0"><div class="xp-i">AT</div><h4>Dr. Amro Taibah</h4><div class="lbl o">Strategic partner</div><ul><li>PhD, Urban and Regional Science</li><li>MSc, Construction Management</li></ul></div><div class="xp rv d1"><div class="xp-i">WS</div><h4>Waleed Shaalan</h4><div class="lbl o">Strategic partner</div><ul><li>B.Arch</li><li>LEED Green Associate</li></ul></div><div class="xp rv d2"><div class="xp-i">JM</div><h4>Joanna M. Esty</h4><div class="lbl o">Strategic partner</div><ul><li>JD, University of Maryland School of Law</li><li>MBA, Pepperdine University</li><li>BSc Chemical Engineering, Georgia Tech</li></ul></div><div class="xp rv d3"><div class="xp-i">AN</div><h4>Abdel Nasser Taha</h4><div class="lbl o">Strategic partner</div><ul><li>BSc Architecture</li><li>MBA (IPE France): strategic planning, risk and change management</li></ul></div><div class="xp rv d0"><div class="xp-i">SS</div><h4>Sherif Saleh</h4><div class="lbl o">Strategic partner</div><ul><li>MBA, Financial Risk Management</li><li>MSc Project Management</li><li>BSc Civil Engineering</li></ul></div></div>
</section>
<section class="sec gut eco" style="padding-top:0">
  <div class="row2"><div class="lbl">Our experts</div><div>
    <h2 class="h-l rv" style="max-width:18ch">Specialists we call on</h2>
  </div></div>
  <div class="xp-grid"><div class="xp rv d0"><div class="xp-i">TE</div><h4>Dr. Tamer Elshayal</h4><div class="lbl o">Urbanism &amp; landscape</div><ul><li>PhD Urban Planning and MDes Urbanism, Landscape, Ecology, Harvard University</li><li>MLA with highest honours, Anhalt University</li></ul></div><div class="xp rv d1"><div class="xp-i">AG</div><h4>Dr. Abdullah Ghazal</h4><div class="lbl o">Horticulture &amp; landscape</div><ul><li>Hohenheim University, Stuttgart</li><li>MSc Horticulture, University of Aleppo</li></ul></div><div class="xp rv d2"><div class="xp-i">ME</div><h4>Maha El Nahas</h4><div class="lbl o">Environmental design</div><ul><li>BSc Environmental Design, University of Oklahoma</li><li>BIA competition winner: passive-solar hotel design</li></ul></div><div class="xp rv d3"><div class="xp-i">AY</div><h4>Ahmed Youssef</h4><div class="lbl o">Energy &amp; management</div><ul><li>BEng, MBA</li><li>EUREM-certified energy manager</li></ul></div><div class="xp rv d0"><div class="xp-i">SF</div><h4>Shady Fayed</h4><div class="lbl o">Real estate &amp; design</div><ul><li>MSc Real Estate, NYU Schack Institute</li><li>MSt Interdisciplinary Design for the Built Environment, University of Cambridge</li><li>BSc Mechanical Engineering, AUC</li></ul></div></div>
</section>
<section class="sec gut">
  <div class="row2"><div class="lbl">The curated expert ensemble</div><div>
    <h2 class="h-l rv" style="max-width:20ch">“We don’t just gather experts. We orchestrate brilliance… matching minds to missions, and context to calibre.”</h2>
    <div class="list3" style="margin-top:50px">
      <div><h4>Strategic project steering</h4><p>Lead guides in major urban initiatives, setting direction and transformation paths.</p></div>
      <div><h4>High-profile advisory boards</h4><p>Decoding complex challenges and offering contextualised counsel to decision-makers.</p></div>
      <div><h4>Competition juries</h4><p>Cross-disciplinary evaluation, as in the Al Rabita Design Competition, Makkah.</p></div>
    </div></div></div>
</section>
<section class="sec gut" id="network" style="padding-top:0">
  <div class="row2"><div class="lbl">Advisory network</div><div><h2 class="h-m rv" style="margin-bottom:30px">Experts who have served on PUD-led panels</h2><div class="list3" id="networkWrap"></div></div></div>
</section>
<section class="strat">
  <div class="st-img" data-px="0.12"><img src="img/al-mashaaer.jpg" alt="Al Mashaaer Al Mugaddassah, Makkah" loading="lazy"></div>
  <div class="st-box gut"><div class="st-in rv">
    <div class="lbl o">Our strategy for a sustainable future</div>
    <h2 class="h-l">People-driven. Extraordinary results.</h2>
    <p class="body">Our strategy is built on evolution, flexibility and focus. Clients and partners count on us to anticipate their needs and deliver creative solutions, to manage resources wisely and to contribute to a better quality of life. Our people are critical to our success, and we reward success by creating opportunities to achieve the extraordinary.</p>
    <div class="tags2"><span>Evolution</span><span>Flexibility</span><span>Focus</span><span>Diversity</span><span>Capability</span><span>Strength</span><span>Integrity</span></div>
    <a class="btn" href="contact.html" style="margin-top:26px">Join our community {AR}</a>
  </div></div>
</section>
''', ld=PEOPLE_LD)


# ---------------- SUSTAINABILITY ----------------
page('sustainability.html', 'Sustainability Commitments & SDGs | PUD Consultants', landing('Sustainable commitments for a vibrant urban future.', 'Our responsibilities and actions across the whole ecosystem — people, society, culture, the environment and the planet — measured by performance, to build a better future for our planet.', crumb='<div class="lbl o rv" style="margin-bottom:18px">Sustainability</div>', wide=True, hero=('heliopark.jpg','Heliopark · New Cairo','heliopark')) + f'''
<section class="sec gut">
  <div class="row2"><div class="lbl">Our commitment</div><div>
    <p class="pull rv" style="margin-top:0">Sustainability is at the core of everything we do.</p>
    <div class="sc2 rv d1">
      <p>We envision urban environments that are not only dynamic and livable, but deeply respectful of their environmental, social and cultural contexts.</p>
      <p>Our goal is simple: to leave a positive legacy. Through every project, we aim to contribute to a more sustainable, equitable and meaningful urban future.</p>
    </div>
  </div></div>
</section>
<section class="sec tight gut" style="padding-top:0">
  <div class="lr-head rv" style="margin-top:0"><span class="lbl">We are committed to</span><span class="meta">Designing with purpose. Building for tomorrow.</span></div>
  <div class="sc4">
    <div class="rv"><span class="chap-n">01</span><h4>Environmental responsibility</h4><p>Minimising our ecological impact through responsible land use, energy-efficient design and environmentally sound planning strategies.</p></div>
    <div class="rv d1"><span class="chap-n">02</span><h4>Social inclusion</h4><p>Creating accessible, inclusive spaces that serve diverse communities and foster a sense of belonging for all.</p></div>
    <div class="rv d2"><span class="chap-n">03</span><h4>Cultural heritage preservation</h4><p>Honouring the historical and cultural identity of each place in every project, ensuring continuity and authenticity.</p></div>
    <div class="rv d3"><span class="chap-n">04</span><h4>Green building standards</h4><p>International best practice and sustainable construction methods that enhance performance, reduce emissions and support long-term resilience.</p></div>
  </div>
</section>


<section class="cm gut" id="commitment" aria-label="Our commitment">
  <div class="cm-media" aria-hidden="false"><a class="cm-img on" data-i="0" href="project-kidana-al-khaif.html"><img src="img/kidana-al-khaif.jpg" alt="Kidana Al Khaif · Mina, Makkah" loading="lazy"><span class="ed-cap">Kidana Al Khaif · Mina, Makkah</span></a><a class="cm-img" data-i="1" href="project-sumou-boulevard.html"><img src="img/sumou-boulevard.jpg" alt="Sumou Boulevard · New Cairo" loading="lazy"><span class="ed-cap">Sumou Boulevard · New Cairo</span></a><a class="cm-img" data-i="2" href="project-khaybar-heritage.html"><img src="img/khaybar-heritage.jpg" alt="Khaybar Heritage Area · AlUla" loading="lazy"><span class="ed-cap">Khaybar Heritage Area · AlUla</span></a><a class="cm-img" data-i="3" href="project-sharaan.html"><img src="img/sharaan.jpg" alt="Sharaan Nature Reserve · AlUla" loading="lazy"><span class="ed-cap">Sharaan Nature Reserve · AlUla</span></a><a class="cm-img" data-i="4" href="project-nw-coast-regional-vision.html"><img src="img/nw-coast-regional-vision.jpg" alt="North-West Coast Regional Vision · Egypt" loading="lazy"><span class="ed-cap">North-West Coast Regional Vision · Egypt</span></a></div>
  <div class="cm-text"><div class="lr-head" style="margin-top:0"><span class="lbl">Our commitment</span><span class="meta">Five responsibilities, one approach</span></div><div class="cm-b" data-i="0" id="people"><span class="chap-n">01</span><div class="lbl">People</div><h3>Places designed around people.</h3><p>Every plan starts with the people who will live, work, pray and visit there — human-scale streets, shade, walkability and public spaces where communities can gather.</p><figure class="cm-mimg"><img src="img/kidana-al-khaif.jpg" alt="Kidana Al Khaif · Mina, Makkah" loading="lazy"></figure></div><div class="cm-b" data-i="1" id="society"><span class="chap-n">02</span><div class="lbl">Society</div><h3>Inclusive, affordable, connected.</h3><p>We plan for social inclusion: affordable housing, access to services and mixed-use neighbourhoods that give every generation a place to belong — and a stake in the city’s future.</p><figure class="cm-mimg"><img src="img/sumou-boulevard.jpg" alt="Sumou Boulevard · New Cairo" loading="lazy"></figure></div><div class="cm-b" data-i="2" id="culture"><span class="chap-n">03</span><div class="lbl">Culture</div><h3>Heritage as a living foundation.</h3><p>We read each place’s history before we draw a line, protecting cultural landscapes and carrying local identity forward, so that new development deepens a place’s character rather than erasing it.</p><figure class="cm-mimg"><img src="img/khaybar-heritage.jpg" alt="Khaybar Heritage Area · AlUla" loading="lazy"></figure></div><div class="cm-b" data-i="3" id="environment"><span class="chap-n">04</span><div class="lbl">Environment</div><h3>Working with nature, not against it.</h3><p>Responsible land use, protected ecosystems, water-wise landscapes and green building standards — from nature reserves in AlUla to green communities in New Cairo.</p><figure class="cm-mimg"><img src="img/sharaan.jpg" alt="Sharaan Nature Reserve · AlUla" loading="lazy"></figure></div><div class="cm-b" data-i="4" id="planet"><span class="chap-n">05</span><div class="lbl">Planet</div><h3>Resilient regions for a changing climate.</h3><p>At regional scale we plan for resilience: compact growth, low-carbon mobility and coastlines and deserts managed for the long term, so that our work leaves the planet better prepared.</p><figure class="cm-mimg"><img src="img/nw-coast-regional-vision.jpg" alt="North-West Coast Regional Vision · Egypt" loading="lazy"></figure></div></div>
</section>
<section class="interlude rf2" aria-label="Designing resilient futures">
  <div class="il-img" data-px="0.18"><img src="img/alamein-riviera.jpg" alt="Alamein Riviera, North Coast" loading="lazy"></div>
  <div class="il-txt gut"><p class="rv">Where sustainability shapes place, purpose and people.</p><a class="meta rv d1" href="project-alamein-riviera.html">Alamein Riviera · North Coast, Egypt →</a></div>
</section>
<section class="sec gut">
  <div class="row2"><div class="lbl">Designing resilient futures</div><div>
    <h2 class="h-l rv" style="max-width:22ch">Not just a guideline — a lens of transformation.</h2>
    <p class="body rv d1" style="margin-top:16px;max-width:60ch">From mega cities to sacred landscapes, we weave resilience into every layer of planning.</p>
    <div class="rf2-list">
      <div class="rv"><b>Adaptive land use</b></div><div class="rv d1"><b>Ecological corridors</b></div><div class="rv d2"><b>Human-centred access</b></div>
      <div class="rv"><b>Cultural continuity</b></div><div class="rv d1"><b>Context-sensitive design</b><span>Respecting natural topography, climate and ecosystems</span></div><div class="rv d2"><b>Green infrastructure systems</b></div>
    </div>
    <p class="body rv" style="margin-top:36px">Every decision we make is designed to serve the future. That’s how we build legacy, rooted in sustainability.</p>
  </div></div>
</section>

<section class="sec gut" id="sdgs" style="background:var(--tint)">
  <div class="row2"><div class="lbl">Goals we support</div><div>
    <h2 class="h-l rv" style="max-width:20ch">Leave no place behind.</h2>
    <p class="body rv" style="margin-top:14px;max-width:60ch">Our work is aligned with the UN Sustainable Development Goals, contributing most directly to seven of the seventeen.</p>
  </div></div>
  <div class="sdg-grid"><div class="sdg rv d0" style="--c:#FCC30B"><b>7</b><h4>Affordable and clean energy</h4><p class="sdg-o">Ensure access to affordable, reliable, sustainable and modern energy for all.</p><p class="sdg-p"><span>PUD</span> Energy-efficient master plans and renewable-ready districts.</p></div><div class="sdg rv d1" style="--c:#A21942"><b>8</b><h4>Decent work and economic growth</h4><p class="sdg-o">Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all.</p><p class="sdg-p"><span>PUD</span> Destinations and economic cities that create jobs and local value.</p></div><div class="sdg rv d2" style="--c:#FD6925"><b>9</b><h4>Industry, innovation and infrastructure</h4><p class="sdg-o">Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation.</p><p class="sdg-p"><span>PUD</span> Resilient infrastructure plans, from AlUla to the Saudi railway network.</p></div><div class="sdg rv d3" style="--c:#FD9D24"><b>11</b><h4>Sustainable cities and communities</h4><p class="sdg-o">Make cities and human settlements inclusive, safe, resilient and sustainable.</p><p class="sdg-p"><span>PUD</span> Our core purpose for sixty years.</p></div><div class="sdg rv d0" style="--c:#BF8B2E"><b>12</b><h4>Responsible consumption and production</h4><p class="sdg-o">Ensure sustainable consumption and production patterns.</p><p class="sdg-p"><span>PUD</span> Land, water and materials planned for efficiency over the life of a place.</p></div><div class="sdg rv d1" style="--c:#3F7E44"><b>13</b><h4>Climate action</h4><p class="sdg-o">Take urgent action to combat climate change and its impacts.</p><p class="sdg-p"><span>PUD</span> Climate-resilient regional plans and low-carbon frameworks.</p></div><div class="sdg rv d2" style="--c:#19486A"><b>17</b><h4>Partnerships for the goals</h4><p class="sdg-o">Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development.</p><p class="sdg-p"><span>PUD</span> A curated network of global partners and local experts.</p></div></div>
</section>
<section class="sec gut" id="projects">
  <div class="lr-head rv" style="margin-top:0"><span class="lbl">Sustainability in practice</span><a class="meta" href="projects.html">All projects →</a></div>
  <div class="lead-row"><a class="lr-c rv d0" href="project-alula-framework.html"><div class="th"><img src="img/alula-framework.jpg" alt="AlUla County Framework Plan" loading="lazy"></div><div class="meta">AlUla, KSA</div><h3>AlUla County Framework Plan</h3></a><a class="lr-c rv d1" href="project-khaybar-heritage.html"><div class="th"><img src="img/khaybar-heritage.jpg" alt="Khaybar Heritage Area" loading="lazy"></div><div class="meta">AlUla, KSA</div><h3>Khaybar Heritage Area</h3></a><a class="lr-c rv d2" href="project-nw-coast-regional-vision.html"><div class="th"><img src="img/nw-coast-regional-vision.jpg" alt="North-West Coast Regional Plan" loading="lazy"></div><div class="meta">Egypt</div><h3>North-West Coast Regional Plan</h3></a><a class="lr-c rv d3" href="project-sharaan.html"><div class="th"><img src="img/sharaan.jpg" alt="Sharaan Nature Reserve" loading="lazy"></div><div class="meta">AlUla, KSA</div><h3>Sharaan Nature Reserve</h3></a></div>
</section>
<section class="cta2 gut">
  <a class="cta2-c rv" href="contact.html"><span class="lbl o">For clients</span><h3>Need help developing your SDGs strategy?</h3><span class="more">Contact one of our experts →</span></a>
  <a class="cta2-c rv d1" href="contact.html"><span class="lbl o">For partners</span><h3>Making progress together.</h3><span class="more">Become one of our partners →</span></a>
</section>
''')

# ---------------- NEWS ----------------
page('news.html', 'News & Events | PUD Consultants', landing('News', 'Events, talks and project milestones — shared by Dr. Amr Attia, who represents PUD at forums and partners worldwide.', hero=('jorhum.jpg','Jorhum Mixed-Use Development · Makkah Region','jorhum')) + '''
<section class="sec tight gut"><div class="chips" id="newsF" style="margin-bottom:30px"></div><div class="nlist" id="newsList"></div></section>''')

FAQ = [('What is PUD Consultants?', 'PUD (Planning Urban Development) Consultants is a multidisciplinary planning and design consultancy founded in Cairo in 1966 by Prof. Abdallah Abdel Aziz Attia. It shapes sustainable cities, tourism destinations, heritage areas and sacred landscapes across Egypt, Saudi Arabia, the UAE and beyond.'), ('Who leads PUD Consultants today?', 'PUD is led by Prof. Dr. Amr A. Attia, CEO and Principal, Professor of Architecture and Urban Planning at Ain Shams University, an Eisenhower Fellow (2007) and former Vice President of Strategic Development at WATG and Principal Director at AECOM.'), ('What services does PUD offer?', 'Urban and regional planning, master planning and urban design, architectural design, sustainable tourism development, cultural heritage, landscape planning and design, environment and sustainability, green economy, development consultancy, and financial planning and assessment.'), ('Where does PUD work?', 'PUD has delivered 150+ projects in 11 countries and 60+ cities, with offices in Cairo (Egypt), Riyadh (Saudi Arabia) and Dubai (UAE). Work spans Egypt from Alexandria to Aswan, Saudi Arabia from NEOM to Jazan, and countries including Kuwait, Iraq, Syria, Palestine, Iran, Cameroon, Gambia and Germany.'), ('What are some of PUD’s notable projects?', 'Highlights include the Pyramids Plateau Destination and AKHET tourism master plan (with WATG), Al Mashaaer Al Mugaddassah in Makkah, Alamein Riviera, Sumou Boulevard, Cairo Media City, strategic advisory for the New Administrative Capital, the Khaybar Heritage Area and AlUla County framework plans, and Jazan Economic City.'), ('How does PUD approach sustainability?', 'Sustainability is at the core of every PUD project, through environmental responsibility, social inclusion, cultural heritage preservation and green building standards. PUD’s work aligns with UN Sustainable Development Goals 7, 8, 9, 11, 12, 13 and 17.'), ('Does PUD work with international firms?', 'Yes. PUD regularly collaborates with leading global firms including WATG, AECOM, SOM, BuroHappold, HOK, HILL International and Giugiaro, combining international expertise with deep local knowledge, alongside 100+ clients and 90+ collaborations over six decades.'), ('How can I contact PUD Consultants?', 'Call Cairo on +20 2 2414 7537, Riyadh on +966 540 39 8178 or Dubai on +971 509 29 8178, or use the enquiry form on the Contact page.')]
FAQPAGE = {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}
# ---------------- ABOUT ----------------
page('about.html', 'About PUD: Planning & Urban Development Consultants since 1966', landing('About', 'Planning Urban Development (PUD) is a pioneering consulting and design firm, established in 1966 by Prof. Abdallah Abdel Aziz Attia.', hero=('khaybar-heritage.jpg','Khaybar Heritage Area Master Plan · AlUla','khaybar-heritage')) + f'''
<section class="sec gut">
  <div class="row2"><div class="lbl">Our Purpose</div>
  <p class="purpose rv">We lead urban and tourism transformation, <a href="#expertise">decoding land and cultural narratives</a> and <a href="people.html">curating expert-driven collaborations</a> to preserve legacy, express identity and <a href="#sustainability">foster future-ready environments</a>.</p></div>
</section>
<section class="sec tight gut">
  <div class="row2"><div class="lbl">Who we are</div><div style="columns:2;column-gap:var(--gut)" class="body">
    <p>With six decades of impact, PUD stands as a multinational leader in urban planning, architecture and sustainable tourism — offering strategic consultancy, design excellence and delivery management, from visionary master planning to precise execution.</p>
    <p>Operating across Cairo, Dubai and Riyadh, PUD blends deep regional insight with global expertise to deliver innovative, culturally grounded, tailored and sustainable projects.</p>
    <p>Our strength lies in a holistic, end-to-end approach, powered by a network of multidisciplinary experts spanning consultancy, design, architecture, planning and project management.</p>
    <p>Guided by the values of leadership, harmony and clarity, we go beyond traditional consultancy by transferring knowledge, building capabilities and empowering our partners to achieve enduring, future-ready outcomes.</p>
  </div></div>
</section>
<section class="sec tight gut"><div class="mv">
  <div class="rv"><div class="lbl o">Mission</div><p class="lead" style="margin-top:14px">To lead urban and tourism transformation through contextual architecture, integrated design, strategic master planning and capacity building — shaping the leaders of tomorrow.</p></div>
  <div class="rv d1"><div class="lbl o">Vision</div><p class="lead" style="margin-top:14px">To become the trusted partner of visionary clients — shaping resilient communities, iconic destinations and transformative environments through design that tells a story and honours culture.</p></div>
</div></section>
<section class="sec tight gut"><h2 class="h-m rv" style="margin-bottom:24px">Core values</h2><div class="vals">
  <div class="rv"><b>01</b><h4>Integrity</h4><p>Our ethical approach underpins all our relationships and decisions.</p></div>
  <div class="rv d1"><b>02</b><h4>Sustainability</h4><p>Environmental, social and cultural harmony in all projects.</p></div>
  <div class="rv d2"><b>03</b><h4>Innovation</h4><p>Creativity and new technologies to shape future-ready spaces.</p></div>
  <div class="rv d3"><b>04</b><h4>Excellence</h4><p>The highest standards of quality and safety.</p></div>
</div></section>
<section class="gut"><figure class="fig rv" style="margin:0;aspect-ratio:21/8" data-px="0.06"><img src="img/nw-coast-regional-vision.jpg" alt="North-West Coast regional vision" loading="lazy" style="height:116%"></figure></section>
<section class="sec gut" id="expertise"><div class="row2"><div class="lbl">Expertise</div><div class="xlist">
  <div class="xrow"><b>01</b><h3>Urban &amp; Regional Planning &amp; City Making</h3><p>Resilient regions and vibrant cities through frameworks aligning land use, mobility, infrastructure and growth with national visions.</p></div>
  <div class="xrow"><b>02</b><h3>Urban Design &amp; Master Planning</h3><p>Mixed-use destinations and smart districts with strategic zoning, land optimisation and future-ready systems.</p></div>
  <div class="xrow"><b>03</b><h3>Architectural &amp; Experiential Design</h3><p>Context-driven architecture fusing aesthetics, function and user experience into signature landmarks.</p></div>
  <div class="xrow"><b>04</b><h3>Environmentally Sustainable Development</h3><p>Low-carbon strategies, green infrastructure and ecological systems that meet global standards.</p></div>
  <div class="xrow"><b>05</b><h3>Cultural Heritage &amp; Identity Preservation</h3><p>Integrating heritage into urban and architectural design for continuity and authenticity.</p></div>
  <div class="xrow"><b>06</b><h3>Strategic Advisory &amp; Green Economy</h3><p>Development economics aligning vision with market feasibility, investment strategy and regenerative models.</p></div>
  <div class="xrow"><b>07</b><h3>Global Expert Orchestration</h3><p>Bespoke advisory groups of internationally trusted specialists for each project.</p></div>
</div></div></section>
<section class="sec gut" id="approach" style="padding-top:0"><div class="row2"><div class="lbl">Approach</div><div>
  <h2 class="h-l rv" style="max-width:20ch">Tailored thinking. Integrated delivery. Lasting impact.</h2>
  <p class="body rv" style="margin:18px 0 40px">We don’t believe in one-size-fits-all solutions. We start by listening — then craft bespoke strategies balancing creative vision, technical precision and cultural understanding.</p>
  <div class="list3">
    <div><h4>Insight-driven planning</h4><p>Stakeholder engagement and contextual analysis.</p></div>
    <div><h4>Scenario-based thinking</h4><p>Future-forward options tested against change.</p></div>
    <div><h4>Collaborative co-creation</h4><p>Clients, communities and experts shape the vision together.</p></div>
    <div><h4>Legacy-oriented design</h4><p>Design that tells a story and honours culture.</p></div>
    <div><h4>Agile project structuring</h4><p>Project-specific teams and phasing.</p></div>
    <div><h4>Integrated sustainability</h4><p>Environmental, social and cultural harmony in every layer.</p></div>
  </div></div></div></section>
<section class="sec gut" id="sustainability" style="background:var(--tint)"><div class="row2"><div class="lbl">Sustainability</div><div>
  <h2 class="h-l rv" style="max-width:20ch">Designing with purpose. Building for tomorrow.</h2>
  <figure class="fig rv" style="margin:30px 0;aspect-ratio:21/9"><img src="img/sharaan.jpg" alt="Sharaan Nature Reserve, AlUla" loading="lazy"></figure>
  <p class="body rv" style="margin:18px 0 40px">Sustainability is not just a guideline, it is a lens of transformation. From mega cities to sacred landscapes, our goal is simple: to leave a positive legacy.</p>
  <div class="vals" style="border-color:var(--rule2)">
    <div><b>01</b><h4 style="font-size:22px">Environmental responsibility</h4><p>Responsible land use and energy-efficient design.</p></div>
    <div><b>02</b><h4 style="font-size:22px">Social inclusion</h4><p>Accessible spaces that foster belonging for all.</p></div>
    <div><b>03</b><h4 style="font-size:22px">Cultural heritage</h4><p>Continuity and authenticity of each place.</p></div>
    <div><b>04</b><h4 style="font-size:22px">Green building standards</h4><p>Best practice that reduces emissions and builds resilience.</p></div>
  </div></div></div></section>
<section class="sec gut" id="awards"><div class="row2"><div class="lbl">Awards</div><div>
  <h2 class="h-l rv">20+ awards, with first- and second-place prizes.</h2>
  <p class="body rv" style="margin:18px 0 40px">Including the International Star for Leadership in Quality, Paris 2010.</p>
  <div class="awl" id="awardList"></div></div></div></section>
<section class="sec gut" id="faq"><div class="row2"><div class="lbl">FAQ</div><div>
  <h2 class="h-l rv" style="margin-bottom:30px">Frequently asked questions</h2>
  <div class="faq"><details class="rv" open><summary><h3>What is PUD Consultants?</h3></summary><p>PUD (Planning Urban Development) Consultants is a multidisciplinary planning and design consultancy founded in Cairo in 1966 by Prof. Abdallah Abdel Aziz Attia. It shapes sustainable cities, tourism destinations, heritage areas and sacred landscapes across Egypt, Saudi Arabia, the UAE and beyond.</p></details><details class="rv"><summary><h3>Who leads PUD Consultants today?</h3></summary><p>PUD is led by Prof. Dr. Amr A. Attia, CEO and Principal, Professor of Architecture and Urban Planning at Ain Shams University, an Eisenhower Fellow (2007) and former Vice President of Strategic Development at WATG and Principal Director at AECOM.</p></details><details class="rv"><summary><h3>What services does PUD offer?</h3></summary><p>Urban and regional planning, master planning and urban design, architectural design, sustainable tourism development, cultural heritage, landscape planning and design, environment and sustainability, green economy, development consultancy, and financial planning and assessment.</p></details><details class="rv"><summary><h3>Where does PUD work?</h3></summary><p>PUD has delivered 150+ projects in 11 countries and 60+ cities, with offices in Cairo (Egypt), Riyadh (Saudi Arabia) and Dubai (UAE). Work spans Egypt from Alexandria to Aswan, Saudi Arabia from NEOM to Jazan, and countries including Kuwait, Iraq, Syria, Palestine, Iran, Cameroon, Gambia and Germany.</p></details><details class="rv"><summary><h3>What are some of PUD’s notable projects?</h3></summary><p>Highlights include the Pyramids Plateau Destination and AKHET tourism master plan (with WATG), Al Mashaaer Al Mugaddassah in Makkah, Alamein Riviera, Sumou Boulevard, Cairo Media City, strategic advisory for the New Administrative Capital, the Khaybar Heritage Area and AlUla County framework plans, and Jazan Economic City.</p></details><details class="rv"><summary><h3>How does PUD approach sustainability?</h3></summary><p>Sustainability is at the core of every PUD project, through environmental responsibility, social inclusion, cultural heritage preservation and green building standards. PUD’s work aligns with UN Sustainable Development Goals 7, 8, 9, 11, 12, 13 and 17.</p></details><details class="rv"><summary><h3>Does PUD work with international firms?</h3></summary><p>Yes. PUD regularly collaborates with leading global firms including WATG, AECOM, SOM, BuroHappold, HOK, HILL International and Giugiaro, combining international expertise with deep local knowledge, alongside 100+ clients and 90+ collaborations over six decades.</p></details><details class="rv"><summary><h3>How can I contact PUD Consultants?</h3></summary><p>Call Cairo on +20 2 2414 7537, Riyadh on +966 540 39 8178 or Dubai on +971 509 29 8178, or use the enquiry form on the Contact page.</p></details></div></div></div></section>
''', ld=[FAQPAGE])

# ---------------- CONTACT ----------------
page('contact.html', 'Contact PUD Consultants: Cairo, Riyadh, Dubai', landing('Contact', 'Five offices across Egypt, Saudi Arabia and the United Arab Emirates.', hero=('prince-talal-hurghada.jpg','HRH Prince Talal Development · Hurghada','prince-talal-hurghada')) + f'''
<section class="sec tight gut"><div class="offices">
  <div class="office rv"><h3>Cairo</h3><div class="lbl o">Egypt</div>
    <address><b>Heliopolis</b>115 El Thawra Street, 5th Floor, Heliopolis 11757, Cairo<br>Tel +20 2 2414 7537</address>
    <address><b>Sheikh Zayed</b>Polygon Building 8, Office 208, SODIC, 12588 Beverly Hills, Sheikh Zayed City<br>Tel +20 100 198 1111</address></div>
  <div class="office rv d1"><h3>Riyadh</h3><div class="lbl o">Saudi Arabia</div>
    <address><b>Diplomatic Quarter</b>8620 Ibn Mousa Street, 3372 Diplomatic Quarter, Riyadh 2513<br>Tel +966 540 39 8178</address>
    <address><b>Al Nakheel</b>7064 Salem bin Maaqil Street, Al Nakheel District 4092, Riyadh 12393<br>Tel 800 111 0893</address></div>
  <div class="office rv d2"><h3>Dubai</h3><div class="lbl o">United Arab Emirates</div>
    <address><b>Palm Jumeirah</b>Shoreline 12, Al Anbara, PH 06, Palm Jumeirah, Dubai<br>Tel +971 509 29 8178</address></div>
</div></section>
<section class="sec gut"><div class="row2"><div class="lbl">Enquiries</div><div>
  <h2 class="h-l rv" style="margin-bottom:40px">Let’s shape meaningful places together.</h2>
  <form class="form" id="cform" novalidate>
    <div class="two"><div class="fld"><label for="fn">First name</label><input id="fn" name="fn" autocomplete="given-name"></div><div class="fld"><label for="ln">Last name</label><input id="ln" name="ln" autocomplete="family-name"></div></div>
    <div class="two"><div class="fld"><label for="em">Email</label><input id="em" name="em" type="email" autocomplete="email"></div>
    <div class="fld"><label for="ty">Enquiry</label><select id="ty" name="ty"><option>New project</option><option>Strategic advisory</option><option>Partnership</option><option>Careers</option><option>Media</option></select></div></div>
    <div class="fld"><label for="msg">Message</label><textarea id="msg" name="msg" rows="4"></textarea></div>
    <button class="btn f" type="submit">Send message {AR}</button>
    <div class="note" id="fnote" aria-live="polite"></div>
  </form></div></div></section>
''')

# ---------------- STATIC PROJECT + ARTICLE PAGES (indexable) ----------------
REG = {'egypt': 'Egypt', 'ksa': 'Saudi Arabia', 'intl': 'International'}
E = _h.escape
def pimgname(p):
    return f"{p['s']}.jpg" if p.get('i') == '1' and os.path.exists(os.path.join(OUT, 'img', p['s'] + '.jpg')) else 'cairo-media-city.jpg'
for p in DATA['projects']:
    nm, img = p['n'], pimgname(p)
    desc = (p.get('d') or f"{nm}, {p.get('l','')}: a PUD Consultants project.").strip()
    mdesc = (desc[:155].rsplit(' ', 1)[0] + '…') if len(desc) > 160 else desc
    facts = [('Location', p.get('l')), ('Year', p.get('y')), ('Type', p.get('t')), ('Region', REG.get(p.get('r'))), ('Client', p.get('c')), ('Collaborators', p.get('co')), ('PUD scope', p.get('sc'))]
    facts = [f for f in facts if f[1]]
    fallback = f"""<div class="gut" style="padding-top:140px"><div class="crumb"><a href="projects.html">Projects</a> / {E(p.get('t',''))}</div>
<h1>{E(nm)}</h1><p class="meta">{E(p.get('l',''))}{(' · ' + E(p['y'])) if p.get('y') else ''}</p>
<img src="img/{img}" alt="{E(nm)}" style="width:100%;margin:30px 0">
<p class="body">{E(desc)}</p><dl class="facts">{''.join(f'<dt>{E(a)}</dt><dd>{E(b)}</dd>' for a, b in facts)}</dl></div>"""
    ld = [{"@type": "CreativeWork", "name": nm, "description": desc, "image": BASE + 'img/' + img, "url": BASE + f"project-{p['s']}.html",
           "creator": {"@id": BASE + "#org"}, "genre": p.get('t'), "dateCreated": p.get('y') or None,
           "contentLocation": {"@type": "Place", "name": p.get('l')} if p.get('l') else None,
           "sourceOrganization": {"@type": "Organization", "name": p['c']} if p.get('c') else None}]
    ld = [{k: v for k, v in ld[0].items() if v}]
    page(f"project-{p['s']}.html", f"{nm} | {p.get('t') or 'Project'} by PUD Consultants", f"""<article id="pDetail" data-slug="{p['s']}">{fallback}</article>
<section class="gut" style="padding:60px 0 22px"><h2 class="h-m">Related projects</h2></section>
{CAR('relCar')}
<div style="height:80px"></div>""", desc=mdesc, img=img, ld=ld, crumbs=[('Home', 'index.html'), ('Projects', 'projects.html'), (nm, f"project-{p['s']}.html")], ogtype='article')

MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
def iso(d):
    parts = d.split()
    return f"{parts[1]}-{MONTHS.get(parts[0],'01')}-01" if len(parts) == 2 else f"{d}-01-01"
PBY = {p['s']: p for p in DATA['projects']}
for n in DATA['news']:
    img = n.get('img') or (pimgname(PBY[n['p']]) if n.get('p') in PBY else 'cairo-media-city.jpg')
    body = ''.join(f'<p>{E(t)}</p>' for t in n.get('b', []))
    fallback = f"""<div class="gut" style="padding-top:140px"><div class="crumb"><a href="news.html">News</a> / {E(n['c'])}</div>
<h1>{E(n['h'])}</h1><p class="meta">{E(n['d'])} · {E(n['c'])}</p><img src="img/{img}" alt="" style="width:100%;margin:30px 0">
<div class="art-txt">{body}</div></div>"""
    ld = [{"@type": "NewsArticle", "headline": n['h'][:110], "description": n.get('x', ''), "image": [BASE + 'img/' + img], "datePublished": iso(n['d']),
           "author": {"@id": BASE + "#org"}, "publisher": {"@id": BASE + "#org"}, "mainEntityOfPage": BASE + f"article-{n['s']}.html",
           "articleBody": ' '.join(n.get('b', []))}]
    page(f"article-{n['s']}.html", f"{n['h']} | PUD Consultants News", f"""<article id="aDetail" data-slug="{n['s']}">{fallback}</article>
<section class="gut" style="padding:60px 0 22px"><h2 class="h-m">More news</h2></section>
<div class="gut more-news" id="moreNews"></div>
<div style="height:80px"></div>""", desc=n.get('x') or n['h'], img=img, ld=ld, crumbs=[('Home', 'index.html'), ('News', 'news.html'), (n['h'][:60], f"article-{n['s']}.html")], ogtype='article')

# ---------------- SITEMAP, ROBOTS, LLMS ----------------
import datetime
today = datetime.date.today().isoformat()
def prio(u):
    return '1.0' if u == BASE else ('0.6' if ('project-' in u or 'article-' in u) else '0.8')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{prio(u)}</priority></url>\n' for u in SITEMAP) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f"""# PUD Consultants — search engines and AI assistants are welcome.
User-agent: *
Allow: /

# AI / answer engines (explicitly allowed)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {BASE}sitemap.xml
""")
proj_lines = '\n'.join(f"- [{p['n']}]({BASE}project-{p['s']}.html): {p.get('l','')}{(', ' + p['y']) if p.get('y') else ''}. {p.get('t','')}." for p in DATA['projects'])
news_lines = '\n'.join(f"- [{n['h']}]({BASE}article-{n['s']}.html) ({n['d']}): {n.get('x','')}" for n in DATA['news'])
faq_lines = '\n\n'.join(f"### {q}\n{a}" for q, a in FAQ)
llms = f"""# PUD Consultants

> PUD (Planning Urban Development) Consultants is a multidisciplinary planning and design consultancy founded in Cairo in 1966 by Prof. Abdallah Abdel Aziz Attia and led today by Prof. Dr. Amr A. Attia. Over 60 years it has delivered 150+ projects in 11 countries and 60+ cities, shaping sustainable cities, tourism destinations, heritage areas and sacred landscapes across Egypt, Saudi Arabia, the UAE and beyond.

## Key facts
- Founded: 1966, Cairo, Egypt — by Prof. Abdallah Abdel Aziz Attia
- CEO & Principal: Prof. Dr. Amr Abdalla Abdelaziz Attia (Professor of Architecture & Urban Planning, Ain Shams University; Eisenhower Fellow 2007; former VP Strategic Development MEA, WATG; former Principal Director, AECOM)
- Scale: 150+ projects, 11 countries, 60+ cities, 100+ clients, 90+ collaborations, 20+ awards
- Offices: Cairo (Heliopolis, Sheikh Zayed), Riyadh (Diplomatic Quarter, Al Nakheel), Dubai (Palm Jumeirah)
- Services: urban & regional planning; master planning & urban design; architectural design; sustainable tourism; cultural heritage; landscape planning; environment & sustainability; green economy; development consultancy; financial planning & assessment
- Sustainability: environmental responsibility, social inclusion, cultural heritage preservation, green building standards; aligned with UN SDGs 7, 8, 9, 11, 12, 13, 17
- Partners include: WATG, AECOM, SOM, BuroHappold, HOK, HILL International, Giugiaro
- 60th anniversary: 2026 — "60 Years of Shaping Sustainable Cities"

## Main pages
- [Home]({BASE})
- [Projects]({BASE}projects.html)
- [60 Years story]({BASE}60-years.html)
- [People & leadership]({BASE}people.html)
- [Sustainability & SDGs]({BASE}sustainability.html)
- [News]({BASE}news.html)
- [About & FAQ]({BASE}about.html)
- [Contact]({BASE}contact.html)

## FAQ
{faq_lines}

## News
{news_lines}

## Projects
{proj_lines}
"""
open(os.path.join(OUT, 'llms.txt'), 'w').write(llms)

print('ok')
