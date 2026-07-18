#!/usr/bin/env python3
"""Generate work-suitability ranking pages (Best X Pals) for PalTool.
Sample mode: python generate_rankings.py mining
Full mode:   python generate_rankings.py all
"""
import json, os, sys

OUT_DIR = 'D:/幻兽帕鲁/paltool'

with open(os.path.join(OUT_DIR, 'pals.json'), encoding='utf-8') as f:
    pals = json.load(f)

# work key -> (url slug, display name, emoji, task description)
WORK_TYPES = {
    'Mining':                ('mining',      'Mining',                '⛏️', 'mine ore, coal and stone at your base'),
    'Kindling':              ('kindling',    'Kindling',              '🔥', 'smelt ingots and cook food'),
    'Handiwork':             ('handiwork',   'Handiwork',             '🔨', 'craft items and build structures'),
    'Lumbering':             ('lumbering',   'Lumbering',             '🪓', 'chop trees and produce wood'),
    'Transporting':          ('transporting','Transporting',          '📦', 'move items into storage'),
    'Planting':              ('planting',    'Planting',              '🌱', 'plant crops at plantations'),
    'Watering':              ('watering',    'Watering',              '💧', 'water crops and run mills'),
    'Gathering':             ('gathering',   'Gathering',             '🧺', 'harvest crops and berries'),
    'GeneratingElectricity': ('electricity', 'Electricity Generation','⚡', 'power generators and machines'),
    'MedicineProduction':    ('medicine',    'Medicine Production',   '💊', 'brew medicine at the apothecary'),
    'Cooling':               ('cooling',     'Cooling',               '❄️', 'run coolers and preserve food'),
    'Farming':               ('farming',     'Farming',               '🐄', 'produce resources at the ranch'),
}

# element -> (slug, display, emoji)
ELEMENTS = {
    'fire':     ('fire',     'Fire',     '🔥'),
    'water':    ('water',    'Water',    '💧'),
    'grass':    ('grass',    'Grass',    '🌿'),
    'electric': ('electric', 'Electric', '⚡'),
    'ice':      ('ice',      'Ice',      '❄️'),
    'ground':   ('ground',   'Ground',   '🪨'),
    'dark':     ('dark',     'Dark',     '🌑'),
    'dragon':   ('dragon',   'Dragon',   '🐉'),
    'neutral':  ('neutral',  'Neutral',  '⚪'),
}

def nav_strip():
    work = ' · '.join(f'<a href="/best/{s}-pals/" style="color:#7dd3fc;text-decoration:none;">{e} {l}</a>'
                      for s, l, e, _ in WORK_TYPES.values())
    els = ' · '.join(f'<a href="/elements/{s}-pals/" style="color:#7dd3fc;text-decoration:none;">{e} {l}</a>'
                     for s, l, e in ELEMENTS.values())
    return (f'<div style="margin-top:28px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.08);font-size:12px;color:#64748b;">'
            f'<p><strong style="color:#94a3b8;">Work rankings:</strong> {work}</p>'
            f'<p><strong style="color:#94a3b8;">Pals by element:</strong> {els}</p></div>')

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def gen_ranking_page(work_key):
    slug, label, emoji, taskdesc = WORK_TYPES[work_key]
    ranked = sorted(
        (p for p in pals if (p.get('work') or {}).get(work_key)),
        key=lambda p: (-p['work'][work_key], p.get('dex', 999)))
    if not ranked:
        return None

    total = len(ranked)
    best = ranked[0]
    best_wild = next((p for p in ranked if p.get('isWild')), None)
    # early game = wild, low dex, decent level
    early = next((p for p in ranked if p.get('isWild') and p.get('dex', 999) <= 60), None)

    title = f'Best {label} Pals in Palworld 1.0 — All {total} Ranked | PalTool'
    desc = (f'Complete Palworld 1.0 {label.lower()} tier list: all {total} Pals ranked by {label.lower()} level. '
            f'Updated for the 1.0 work suitability rework — top pick: {best["name"]} (Lv{best["work"][work_key]}).')
    url = f'https://paltool.cc/best/{slug}-pals/'

    rows = ''
    for i, p in enumerate(ranked, 1):
        lv = p['work'][work_key]
        el = p.get('element', '?').title()
        if p.get('element2') and p['element2'] != p.get('element'):
            el += '/' + p['element2'].title()
        others = ', '.join(f'{WORK_TYPES[k][1]} {v}' for k, v in sorted(p['work'].items(), key=lambda x: -x[1])
                           if k != work_key and k in WORK_TYPES)[:60]
        obtain = '✅ Wild' if p.get('isWild') else '🥚 Breed only'
        rows += (f'<tr>'
                 f'<td style="text-align:center;color:#64748b;">{i}</td>'
                 f'<td><a href="../../pals/{p["id"]}/" style="color:#7dd3fc;text-decoration:none;">'
                 f'<img src="../../img/pals/{p["id"]}.png" alt="{esc(p["name"])}" width="28" height="28" '
                 f'style="vertical-align:middle;border-radius:50%;margin-right:8px;" onerror="this.style.display=\'none\'">'
                 f'{esc(p["name"])}</a> <span style="color:#475569;font-size:11px;">#{p.get("dex","?")}</span></td>'
                 f'<td style="text-align:center;"><strong style="color:#fbbf24;">Lv{lv}</strong></td>'
                 f'<td>{esc(el)}</td>'
                 f'<td style="font-size:12px;color:#64748b;">{esc(others) or "—"}</td>'
                 f'<td style="font-size:12px;">{obtain}</td></tr>')

    items_ld = ','.join(
        f'{{"@type":"ListItem","position":{i},"name":"{esc(p["name"])}","url":"https://paltool.cc/pals/{p["id"]}/"}}'
        for i, p in enumerate(ranked[:20], 1))

    picks = f'<li><strong>Best overall:</strong> <a href="../../pals/{best["id"]}/" style="color:#7dd3fc;">{esc(best["name"])}</a> — {label} Lv{best["work"][work_key]}'
    picks += ' (breed-only)</li>' if not best.get('isWild') else '</li>'
    if best_wild and best_wild is not best:
        picks += f'<li><strong>Best wild-catchable:</strong> <a href="../../pals/{best_wild["id"]}/" style="color:#7dd3fc;">{esc(best_wild["name"])}</a> — {label} Lv{best_wild["work"][work_key]}</li>'
    if early and early not in (best, best_wild):
        picks += f'<li><strong>Best early game:</strong> <a href="../../pals/{early["id"]}/" style="color:#7dd3fc;">{esc(early["name"])}</a> (#{early.get("dex","?")}) — {label} Lv{early["work"][work_key]}, low Paldeck number so you can catch it early</li>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="../../css/mobile.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"ItemList","name":"{esc(f'Best {label} Pals in Palworld')}","url":"{url}","itemListElement":[{items_ld}]}}
  </script>
</head>
<body>
  <header class="topbar" id="topbar">
    <div class="topbar-left">
      <span class="logo">Pal<span>Tool</span></span>
      <span class="version">v0.4.0-beta</span>
    </div>
    <div class="topbar-right">
      <a href="https://paypal.me/zhaoyaqi08" target="_blank" class="coffee-btn" rel="noopener">☕ Buy Me a Coffee</a>
    </div>
  </header>

  <div class="hero">
    <div class="hero-content">
      <h2 class="hero-subtitle">Palworld 1.0 Rankings</h2>
      <h1 class="hero-logo">Pal<span>Tool</span></h1>
      <p class="hero-tagline">{emoji} Best {label} Pals</p>
      <p class="hero-hint">✅ Updated for Palworld 1.0 · 299 Pals · 44,552 Recipes</p>
    </div>
  </div>

  <div class="seo-content" style="max-width:860px;margin:0 auto;padding:0 24px 40px;color:#94a3b8;font-size:14px;line-height:1.6;">
    <p style="font-size:12px;"><a href="../../" style="color:#64748b;">← PalTool Home</a></p>
    <h2 style="color:#e2e8f0;font-size:22px;margin-bottom:12px;">{emoji} Best {label} Pals in Palworld (1.0 Rankings)</h2>
    <p>Looking for the best Pals to {taskdesc}? Palworld 1.0 <strong>reworked the entire work suitability system</strong> — level caps went up and many Pals got new values, so most pre-1.0 tier lists are outdated. This ranking is generated from extracted 1.0 game data and covers all <strong>{total} Pals</strong> with {label.lower()} suitability.</p>
    <h3 style="color:#e2e8f0;font-size:16px;margin-top:20px;">Quick picks</h3>
    <ul>{picks}</ul>
    <h3 style="color:#e2e8f0;font-size:16px;margin-top:20px;">Full ranking — all {total} {label.lower()} Pals</h3>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead><tr style="color:#e2e8f0;border-bottom:1px solid rgba(255,255,255,0.15);text-align:left;">
        <th style="padding:8px 6px;">#</th><th>Pal</th><th style="text-align:center;">{label}</th><th>Element</th><th>Other work</th><th>How to get</th>
      </tr></thead>
      <tbody style="border-bottom:1px solid rgba(255,255,255,0.06);">{rows}</tbody>
    </table>
    </div>
    <p style="margin-top:16px;">🥚 <strong>Breed-only Pal?</strong> Use the <a href="../../" style="color:#7dd3fc;">PalTool reverse breeding calculator</a> to find the shortest breeding path from Pals you can catch in the wild.</p>
    {nav_strip()}
    <p style="margin-top:20px;font-size:12px;color:#64748b;">Data sourced from Palworld 1.0 game files. Last updated: July 2026.</p>
  </div>

  <footer class="footer" style="padding:20px 24px;text-align:center;color:#64748b;font-size:12px;border-top:1px solid rgba(255,255,255,0.06);">
    <p>Not affiliated with Pocketpair. Fan project. 44,552 game-accurate breeding recipes.</p>
  </footer>
</body>
</html>'''

    page_dir = os.path.join(OUT_DIR, 'best', f'{slug}-pals')
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    return slug, total

def gen_element_page(el):
    slug, label, emoji = ELEMENTS[el]
    members = sorted((p for p in pals
                      if p.get('element') == el or p.get('element2') == el),
                     key=lambda p: p.get('dex', 9999))
    if not members:
        return None
    total = len(members)
    wild_n = sum(1 for p in members if p.get('isWild'))

    title = f'All {label} Pals in Palworld 1.0 — Complete List of {total} | PalTool'
    desc = (f'Every {label.lower()}-element Pal in Palworld 1.0: {total} Pals with Paldeck numbers, work suitability '
            f'and how to obtain them ({wild_n} catchable in the wild, {total - wild_n} breed-only).')
    url = f'https://paltool.cc/elements/{slug}-pals/'

    rows = ''
    for p in members:
        el_disp = p.get('element', '?').title()
        if p.get('element2') and p['element2'] != p.get('element'):
            el_disp += '/' + p['element2'].title()
        works = ', '.join(f'{WORK_TYPES[k][1]} {v}' for k, v in sorted((p.get('work') or {}).items(), key=lambda x: -x[1])
                          if k in WORK_TYPES)[:70]
        obtain = '✅ Wild' if p.get('isWild') else '🥚 Breed only'
        rows += (f'<tr>'
                 f'<td style="text-align:center;color:#64748b;">#{p.get("dex","?")}</td>'
                 f'<td><a href="../../pals/{p["id"]}/" style="color:#7dd3fc;text-decoration:none;">'
                 f'<img src="../../img/pals/{p["id"]}.png" alt="{esc(p["name"])}" width="28" height="28" '
                 f'style="vertical-align:middle;border-radius:50%;margin-right:8px;" onerror="this.style.display=\'none\'">'
                 f'{esc(p["name"])}</a></td>'
                 f'<td>{esc(el_disp)}</td>'
                 f'<td style="font-size:12px;color:#64748b;">{esc(works) or "—"}</td>'
                 f'<td style="font-size:12px;">{obtain}</td></tr>')

    items_ld = ','.join(
        f'{{"@type":"ListItem","position":{i},"name":"{esc(p["name"])}","url":"https://paltool.cc/pals/{p["id"]}/"}}'
        for i, p in enumerate(members[:20], 1))

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="../../css/mobile.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"ItemList","name":"{esc(f'All {label} Pals in Palworld')}","url":"{url}","itemListElement":[{items_ld}]}}
  </script>
</head>
<body>
  <header class="topbar" id="topbar">
    <div class="topbar-left">
      <span class="logo">Pal<span>Tool</span></span>
      <span class="version">v0.4.0-beta</span>
    </div>
    <div class="topbar-right">
      <a href="https://paypal.me/zhaoyaqi08" target="_blank" class="coffee-btn" rel="noopener">☕ Buy Me a Coffee</a>
    </div>
  </header>

  <div class="hero">
    <div class="hero-content">
      <h2 class="hero-subtitle">Palworld 1.0 Paldeck</h2>
      <h1 class="hero-logo">Pal<span>Tool</span></h1>
      <p class="hero-tagline">{emoji} All {label} Pals</p>
      <p class="hero-hint">✅ Updated for Palworld 1.0 · 299 Pals · 44,552 Recipes</p>
    </div>
  </div>

  <div class="seo-content" style="max-width:860px;margin:0 auto;padding:0 24px 40px;color:#94a3b8;font-size:14px;line-height:1.6;">
    <p style="font-size:12px;"><a href="../../" style="color:#64748b;">← PalTool Home</a></p>
    <h2 style="color:#e2e8f0;font-size:22px;margin-bottom:12px;">{emoji} All {label} Pals in Palworld (1.0)</h2>
    <p>There are <strong>{total} {label.lower()}-element Pals</strong> in Palworld 1.0 — {wild_n} can be caught in the wild and {total - wild_n} are breed-only. Sorted by Paldeck number. Click any Pal for its full breeding guide.</p>
    <h3 style="color:#e2e8f0;font-size:16px;margin-top:20px;">Complete {label} Pal list</h3>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead><tr style="color:#e2e8f0;border-bottom:1px solid rgba(255,255,255,0.15);text-align:left;">
        <th style="padding:8px 6px;">#</th><th>Pal</th><th>Element</th><th>Work suitability</th><th>How to get</th>
      </tr></thead>
      <tbody style="border-bottom:1px solid rgba(255,255,255,0.06);">{rows}</tbody>
    </table>
    </div>
    <p style="margin-top:16px;">🥚 <strong>Want a breed-only Pal?</strong> The <a href="../../" style="color:#7dd3fc;">PalTool reverse breeding calculator</a> finds the shortest path from wild-catchable parents.</p>
    {nav_strip()}
    <p style="margin-top:20px;font-size:12px;color:#64748b;">Data sourced from Palworld 1.0 game files. Last updated: July 2026.</p>
  </div>

  <footer class="footer" style="padding:20px 24px;text-align:center;color:#64748b;font-size:12px;border-top:1px solid rgba(255,255,255,0.06);">
    <p>Not affiliated with Pocketpair. Fan project. 44,552 game-accurate breeding recipes.</p>
  </footer>
</body>
</html>'''

    page_dir = os.path.join(OUT_DIR, 'elements', f'{slug}-pals')
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    return slug, total

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'mining'
    if mode == 'all':
        for k in WORK_TYPES:
            r = gen_ranking_page(k)
            if r:
                print(f'Generated /best/{r[0]}-pals/ ({r[1]} pals)')
        for el in ELEMENTS:
            r = gen_element_page(el)
            if r:
                print(f'Generated /elements/{r[0]}-pals/ ({r[1]} pals)')
    else:
        keys = [k for k in WORK_TYPES if WORK_TYPES[k][0] == mode]
        for k in keys:
            r = gen_ranking_page(k)
            if r:
                print(f'Generated /best/{r[0]}-pals/ ({r[1]} pals)')
