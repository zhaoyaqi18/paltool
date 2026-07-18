#!/usr/bin/env python3
"""Generate static SEO pages for each Pal and sitemap.xml"""

import json, os, textwrap

OUT_DIR = 'D:/幻兽帕鲁/paltool'
PALS_DIR = os.path.join(OUT_DIR, 'pals')

with open(os.path.join(OUT_DIR, 'pals.json')) as f:
    pals = json.load(f)

with open(os.path.join(OUT_DIR, 'breed_data.json')) as f:
    bd = json.load(f)

# Build reverse lookup: what combos produce each child
child_from = {}
for key in '0123456789abcdef':
    if key in bd and isinstance(bd[key], dict):
        for combo, child in bd[key].items():
            child_from.setdefault(child, []).append(combo)

# Build forward lookup: what each pal produces with common partners
# (not used for static pages, just validation)

bp_map = {p['id']: p['bp'] for p in pals}

def page_title(pal):
    return f"How to Breed {pal['name']} in Palworld — Best Combinations | PalTool"

def meta_desc(pal):
    name = pal['name']
    bp = pal.get('bp', '?')
    egg = pal.get('egg', 'Unknown Egg')
    element = pal.get('element', '?').title()
    return f"Learn how to breed {name} in Palworld. Find the fastest breeding path, best parent combos, and step-by-step roadmap. {element} type, BP={bp}, {egg}. 44,552 verified game-accurate recipes."

def pal_to_url(pal):
    return f"https://paltool.cc/pals/{pal['id']}/"

def gen_page(pal):
    name = pal['name']
    pid = pal['id']
    bp = pal.get('bp', '?')
    element = pal.get('element', '?').title()
    egg = pal.get('egg', 'Unknown Egg')
    food = pal.get('food', '?')
    is_wild = pal.get('isWild', False)
    work = pal.get('work', '')
    dex = pal.get('dex', '?')
    
    # Work skills
    work_skills = ''
    if work:
        work_list = ', '.join([f"{k.title()} Lv{v}" for k, v in work.items()])
        work_skills = f'<p>Work Suitability: {work_list}</p>'
    
    # Breeding info
    breed_info = ''
    combos = child_from.get(pid, [])
    if combos and not (len(combos) == 1 and combos[0] == f'{pid}|{pid}'):
        # Multiple ways to breed this pal
        breed_info += '<p>This pal can be bred from:</p><ul>'
        for c in combos[:10]:
            p1, p2 = c.split('|')
            p1name = next((p['name'] for p in pals if p['id'] == p1), p1)
            p2name = next((p['name'] for p in pals if p['id'] == p2), p2)
            breed_info += f'<li>{p1name} + {p2name}</li>'
        if len(combos) > 10:
            breed_info += f'<li>...and {len(combos)-10} more combinations</li>'
        breed_info += '</ul>'
    elif is_wild:
        breed_info = '<p>This pal can be caught in the wild.</p>'
    
    # Wild habitat
    habitat_info = ''
    if is_wild:
        habitat_info = '<p>✅ Can be found in the wild.</p>'
    else:
        habitat_info = '<p>❌ Cannot be found in the wild — must be bred.</p>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title(pal)}</title>
  <meta name="description" content="{meta_desc(pal)}">
  <link rel="canonical" href="{pal_to_url(pal)}">
  <link rel="stylesheet" href="../../css/mobile.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{page_title(pal)}",
    "description": "{meta_desc(pal)}",
    "url": "{pal_to_url(pal)}",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "PalTool - Palworld Breeding Calculator",
      "url": "https://paltool.cc/"
    }}
  }}
  </script>
</head>
<body>
  <header class="topbar" id="topbar">
    <div class="topbar-left">
      <span class="logo">Pal<span>Tool</span></span>
      <span class="version">v0.4.0-beta</span>
    </div>
    <div id="route-tabs" class="route-tabs hidden dt-only"></div>
    <div class="topbar-right">
      <a href="https://paypal.me/zhaoyaqi08" target="_blank" class="coffee-btn" rel="noopener">☕ Buy Me a Coffee</a>
    </div>
  </header>

  <!-- ===== Hero Section ===== -->
  <div class="hero">
    <div class="hero-content">
      <h2 class="hero-subtitle">Reverse Breeding Planner</h2>
      <h1 class="hero-logo">Pal<span>Tool</span></h1>
      <p class="hero-tagline">Know Exactly What to Breed</p>
      <div class="search-wrapper">
        <input type="text" id="search-input" class="search-input" placeholder="Search by Pal name or number..." autocomplete="off" value="{name}">
        <button id="search-btn" class="search-btn">🔍 SEARCH</button>
      </div>
      <p class="hero-hint">301 Pals · 44,552 Recipes · 100% Game Data</p>
    </div>
  </div>

  <!-- ===== Static SEO Content ===== -->
  <div class="seo-content" style="max-width:800px;margin:0 auto;padding:0 24px 40px;color:#94a3b8;font-size:14px;line-height:1.6;">
    <h2 style="color:#e2e8f0;font-size:20px;margin-bottom:12px;">How to Breed {name} in Palworld</h2>
    <p><strong>{name}</strong> is a {element}-type Pal (#{dex} in the Paldeck) with a Breeding Power of <strong>{bp}</strong>. It hatches from a <strong>{egg}</strong> and requires {food} food per meal.</p>
    {habitat_info}
    {work_skills}
    {breed_info}
    <p style="margin-top:20px;font-size:12px;color:#64748b;">Data sourced directly from Palworld 1.0 game files. 44,552 verified breeding combinations. Last updated: July 2026.</p>
  </div>

  <!-- ===== Results ===== -->
  <div id="route-tabs-mb" class="route-tabs hidden mb-only"></div>
  <section id="result-section" class="result-section hidden">
    <div id="result-container"></div>
  </section>

  <!-- ===== Footer ===== -->
  <footer class="footer" style="padding:20px 24px;text-align:center;color:#64748b;font-size:12px;border-top:1px solid rgba(255,255,255,0.06);">
    <p>Not affiliated with Pocketpair. Fan project. 44,552 game-accurate breeding recipes.</p>
  </footer>

  <!-- ===== Scripts ===== -->
  <script>
    // Auto-search this pal on page load
    window.addEventListener('DOMContentLoaded', () => {{
      setTimeout(() => {{
        const input = document.getElementById('search-input');
        const btn = document.getElementById('search-btn');
        if (input && btn && !btn.disabled) {{
          input.value = '{name}';
          btn.click();
        }}
      }}, 300);
    }});
  </script>
  <script src="../../js/data.js?v=202"></script>
  <script src="../../js/algorithm.js?v=202"></script>
  <script src="../../js/renderer.js?v=202"></script>
  <script src="../../js/share.js?v=202"></script>
  <script src="../../js/app.js?v=202"></script>
</body>
</html>'''
    return html

# Generate all pages
os.makedirs(PALS_DIR, exist_ok=True)
count = 0
for pal in pals:
    pid = pal['id']
    pal_dir = os.path.join(PALS_DIR, pid)
    os.makedirs(pal_dir, exist_ok=True)
    with open(os.path.join(pal_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(gen_page(pal))
    count += 1

print(f"Generated {count} static SEO pages in {PALS_DIR}/")

# Generate sitemap.xml
import datetime
TODAY = datetime.date.today().isoformat()

def mtime_date(path):
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except OSError:
        return TODAY

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += f'  <url><loc>https://paltool.cc/</loc><lastmod>{mtime_date(os.path.join(OUT_DIR, "index.html"))}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
for pal in pals:
    sitemap += f'  <url><loc>https://paltool.cc/pals/{pal["id"]}/</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
# Include guide pages
guides_dir = os.path.join(OUT_DIR, 'guides')
if os.path.isdir(guides_dir):
    for g in sorted(os.listdir(guides_dir)):
        gpath = os.path.join(guides_dir, g)
        if os.path.isdir(gpath):
            gmod = mtime_date(os.path.join(gpath, 'index.html'))
            sitemap += f'  <url><loc>https://paltool.cc/guides/{g}/</loc><lastmod>{gmod}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
# Include ranking / element listing pages
for section in ('best', 'elements'):
    sec_dir = os.path.join(OUT_DIR, section)
    if os.path.isdir(sec_dir):
        for g in sorted(os.listdir(sec_dir)):
            gpath = os.path.join(sec_dir, g)
            if os.path.isdir(gpath):
                gmod = mtime_date(os.path.join(gpath, 'index.html'))
                sitemap += f'  <url><loc>https://paltool.cc/{section}/{g}/</loc><lastmod>{gmod}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
sitemap += '</urlset>\n'

with open(os.path.join(OUT_DIR, 'sitemap.xml'), 'w') as f:
    f.write(sitemap)
print(f"sitemap.xml generated with {len(pals)+1} URLs")

# Generate robots.txt
robots = '''User-agent: *
Allow: /
Sitemap: https://paltool.cc/sitemap.xml
'''
with open(os.path.join(OUT_DIR, 'robots.txt'), 'w') as f:
    f.write(robots)
print("robots.txt generated")
