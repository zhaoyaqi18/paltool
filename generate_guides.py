#!/usr/bin/env python3
"""Generate static guide pages for paltool.cc"""
import os, json

OUT = r'D:\幻兽帕鲁\paltool\guides'
os.makedirs(OUT, exist_ok=True)

GUIDES = [
    {
        'slug': 'fastest-way-to-breed-anubis',
        'title': 'Fastest Way to Breed Anubis in Palworld',
        'desc': 'Step-by-step guide to breeding Anubis with the shortest path. Wild-catchable parents, minimum generations, and pro tips.',
        'h1': 'Fastest Way to Breed Anubis',
        'body': '''<p>Anubis is one of the most sought-after Pals in Palworld, known for its incredible Handiwork Lv4 and combat prowess. Here's the fastest breeding path using only wild-catchable parents.</p>

<h2>Shortest Route: 1 Generation</h2>
<p>The fastest direct route uses two wild-catchable parents:</p>
<div class="guide-combo"><strong>Astegon</strong> + <strong>Blazamut</strong> → <strong>Anubis</strong></div>
<p>Both parents can be caught in the wild, making this a single-generation breed.</p>

<h2>Where to Catch the Parents</h2>
<ul>
<li><strong>Astegon</strong> — Found in No.3 Wildlife Sanctuary (northeast island). Level 40+ field boss.</li>
<li><strong>Blazamut</strong> — Found in No.3 Wildlife Sanctuary. Also appears as a field boss in the volcano region.</li>
</ul>

<h2>Alternative Routes</h2>
<p>Other 1-generation combos include <strong>Jetragon + Wumpo</strong> and <strong>Blazamut + Faleris</strong>. All require high-level wild catches but produce Anubis in a single breeding step.</p>

<h2>Recommended Passives</h2>
<p>For a combat Anubis: <strong>Legend + Musclehead + Ferocious + Earth Emperor</strong><br>
For a worker Anubis: <strong>Artisan + Serious + Work Slave + Lucky</strong></p>

<h2>Pro Tips</h2>
<ul>
<li>Each breeding attempt needs 1 Cake and produces 1 Rocky Egg</li>
<li>Plan for ~10 eggs to get your desired passive combination</li>
<li>Use the <a href="/">PalTool calculator</a> to explore all breeding paths</li>
</ul>'''
    },
    {
        'slug': 'top-10-early-game-pals',
        'title': 'Top 10 Early Game Pals to Catch First in Palworld',
        'desc': 'The best early-game Pals to catch for breeding, combat, and base building. Build your foundation right.',
        'h1': 'Top 10 Early Game Pals',
        'body': '''<p>Starting out in Palworld? These 10 Pals give you the best foundation for breeding, base work, and early combat.</p>

<h2>1. Lamball</h2>
<p>Your first Pal. Handiwork Lv1 and Transport Lv1. Easy to catch, breeds into many useful combos. Keep at least one male and female.</p>

<h2>2. Cattiva</h2>
<p>Handiwork Lv1, Mining Lv1, Transport Lv1. The Swiss Army knife of early Pals. Breeds with Lamball to produce a wide range of offspring.</p>

<h2>3. Chikipi</h2>
<p>Produces eggs passively at your base. Essential for cake production (breeding fuel).</p>

<h2>4. Foxparks</h2>
<p>Kindling Lv1. Your first fire source for smelting ore. Also a solid early combat pal with its flamethrower skill.</p>

<h2>5. Pengullet</h2>
<p>Watering Lv1 and Handiwork Lv1. Essential for watering crops and crafting. Breeds into many useful mid-game Pals.</p>

<h2>6. Lifmunk</h2>
<p>Planting Lv1, Lumbering Lv1, Medicine Lv1. A versatile base worker that covers three work types.</p>

<h2>7. Tanzee</h2>
<p>Planting Lv1, Lumbering Lv1, Transport Lv1. Another multi-role base Pal that pairs well with Lifmunk for breeding.</p>

<h2>8. Daedream</h2>
<p>Your first combat-focused Pal. Its passive ability lets it fight alongside you without being summoned.</p>

<h2>9. Eikthyrdeer</h2>
<p>Fastest early-game mount. Makes exploring and catching other Pals much faster.</p>

<h2>10. Nitewing</h2>
<p>Your first flying mount. Game-changing for exploration and reaching elevated areas.</p>

<h2>Breeding Tip</h2>
<p>These 10 Pals form the foundation of Palworld's breeding tree. Combined strategically, they can produce over 100+ different Pals. Use <a href="/">PalTool</a> to find the best combinations.</p>'''
    },
    {
        'slug': 'palworld-legendary-breeding-guide',
        'title': 'Palworld Legendary Breeding Guide — How to Get Every Legendary',
        'desc': 'Complete guide to breeding all Legendary Pals in Palworld. Jetragon, Frostallion, Paladius, Necromus, and more.',
        'h1': 'Legendary Breeding Guide',
        'body': '''<p>Legendary Pals are the pinnacle of Palworld breeding. Here's everything you need to know about obtaining each one.</p>

<h2>Jetragon</h2>
<p><strong>BP: 70</strong> — The fastest flying mount in the game. Cannot be bred — must be caught at <strong>Mount Obsidian</strong> (far west volcano). Level 50 field boss. Bring plenty of Legendary Spheres.</p>

<h2>Frostallion</h2>
<p><strong>BP: 150</strong> — Ice-type legendary. Wild-catchable at <strong>Land of Absolute Zero</strong> (north). Breeding Frostallion + Helzephyr produces <strong>Frostallion Noct</strong>.</p>

<h2>Frostallion Noct</h2>
<p><strong>BP: 110</strong> — Dark-type variant. <strong>Frostallion + Helzephyr</strong> is the only breeding combo. Helzephyr can be caught at night near the desert region.</p>

<h2>Paladius & Necromus</h2>
<p><strong>BP: 180 & 190</strong> — The twin knights. Both found together at the <strong>Desert</strong> (northeast). Cannot be bred through normal means — must be caught directly.</p>

<h2>Blazamut Ryu</h2>
<p><strong>BP: 100</strong> — Dragon/fire powerhouse. Special raid boss — cannot be caught in the wild or bred normally. Requires Blazamut raid summon.</p>

<h2>Quick Reference</h2>
<table class="guide-table">
<tr><th>Legendary</th><th>BP</th><th>How to Get</th><th>Breedable?</th></tr>
<tr><td>Jetragon</td><td>70</td><td>Mount Obsidian catch</td><td>❌</td></tr>
<tr><td>Frostallion</td><td>150</td><td>Ice region catch</td><td>✅ (as parent)</td></tr>
<tr><td>Frostallion Noct</td><td>110</td><td>Frostallion + Helzephyr</td><td>❌</td></tr>
<tr><td>Paladius</td><td>180</td><td>Desert catch</td><td>❌</td></tr>
<tr><td>Necromus</td><td>190</td><td>Desert catch</td><td>❌</td></tr>
<tr><td>Blazamut Ryu</td><td>100</td><td>Raid boss</td><td>❌</td></tr>
</table>
<p>For detailed breeding paths for any Pal, use the <a href="/">PalTool calculator</a>.</p>'''
    }
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | PalTool</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://paltool.cc/guides/{slug}/">
  <link rel="stylesheet" href="../css/mobile.css?v=204">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "isPartOf": {{
      "@type": "WebSite",
      "name": "PalTool - Palworld Breeding Calculator",
      "url": "https://paltool.cc/"
    }}
  }}
  </script>
</head>
<body>
  <header class="topbar" id="topbar" style="display:flex">
    <div class="topbar-left">
      <a href="/" style="text-decoration:none"><span class="logo">Pal<span>Tool</span></span></a>
      <span class="version">v0.5.0-beta</span>
    </div>
  </header>

  <main style="max-width:800px;margin:80px auto 0;padding:24px;color:var(--text);line-height:1.7">
    <a href="/" style="color:var(--accent);font-size:13px;text-decoration:none">← Back to PalTool</a>
    <h1 style="font-size:28px;margin:16px 0 8px;color:#fff">{h1}</h1>
    <p style="color:var(--text-dim);font-size:13px;margin-bottom:24px">{desc}</p>
    {body}
  </main>

  <footer class="footer" style="padding:20px 24px;text-align:center;color:#64748b;font-size:12px;border-top:1px solid rgba(255,255,255,0.06);margin-top:40px">
    <p>PalTool.cc &copy; 2026. Not affiliated with Pocketpair. Fan project.</p>
  </footer>
</body>
</html>'''

# Also add guide table styles
extra_css = '''
.guide-combo { background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); padding:12px 16px; border-radius:8px; text-align:center; font-size:16px; margin:16px 0; }
.guide-table { width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; }
.guide-table th { background:rgba(255,255,255,0.06); padding:8px 12px; text-align:left; color:var(--text); }
.guide-table td { padding:8px 12px; border-bottom:1px solid rgba(255,255,255,0.06); }
h2 { color:#fff; margin-top:28px; font-size:20px; }
ul { padding-left:20px; margin:8px 0; }
li { margin:4px 0; }
a { color:var(--accent); }
'''

for g in GUIDES:
    d = os.path.join(OUT, g['slug'])
    os.makedirs(d, exist_ok=True)
    html = TEMPLATE.format(title=g['title'], desc=g['desc'], slug=g['slug'], h1=g['h1'], body=g['body'])
    # Inject extra CSS into head
    html = html.replace('</head>', f'<style>{extra_css}</style>\n</head>')
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print(f'Generated {len(GUIDES)} guide pages in {OUT}/')
