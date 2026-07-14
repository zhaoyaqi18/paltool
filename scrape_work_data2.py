"""Rebatch scrape work suitabilities from paldb.cc - fixed parser"""
import json, re, time, urllib.request, urllib.error

WORK_ICONS = {
    'Ticonpalwork00': 'Kindling', 'Ticonpalwork01': 'Watering',
    'Ticonpalwork02': 'Planting', 'Ticonpalwork03': 'GeneratingElectricity',
    'Ticonpalwork04': 'Handiwork', 'Ticonpalwork05': 'Gathering',
    'Ticonpalwork06': 'Lumbering', 'Ticonpalwork07': 'Mining',
    'Ticonpalwork08': 'MedicineProduction', 'Ticonpalwork10': 'Cooling',
    'Ticonpalwork11': 'Transporting', 'Ticonpalwork12': 'Farming',
}

EGG_MAP = {
    'neutral': 'Common Egg', 'fire': 'Scorching Egg', 'water': 'Wetland Egg',
    'grass': 'Verdant Egg', 'electric': 'Electric Egg', 'ice': 'Frozen Egg',
    'ground': 'Rocky Egg', 'dark': 'Dark Egg', 'dragon': 'Dragon Egg',
}

def scrape_works(html):
    """Find work suitabilities from paldb HTML.
    Structure: a[href^=/en/WorkName] followed by sibling/child with LvN"""
    works = {}
    for icon_id, work_name in WORK_ICONS.items():
        # Find the icon, then look for LvN nearby (within next 500 chars)
        idx = html.find(icon_id)
        if idx > 0:
            chunk = html[idx:idx+500]
            m = re.search(r'Lv(\d+)', chunk)
            if m:
                works[work_name] = int(m.group(1))
    return works

def scrape_food(html):
    fm = re.search(r'FoodAmount[^>]*>(\d+)', html)
    return int(fm.group(1)) if fm else 7

# Load and check which pals need data
with open(r'D:\幻兽帕鲁\paltool\pals.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)

# Find pals without work data
todo = [(i, p) for i, p in enumerate(pals) if 'work' not in p or not p.get('work') or p['work'] == {}]
print(f"Need to scrape: {len(todo)} pals\n")

errors = 0
for i, (idx, pal) in enumerate(todo):
    name = pal['name']
    url_name = name.replace(' ', '_').replace("'", '').replace('.', '')
    if pal['id'] == 'kingpaca_cryst':
        url_name = 'Kingpaca_Cryst'
    if pal['id'] == 'ribunny':
        url_name = 'Ribunny'
    
    url = f'https://paldb.cc/en/{url_name}'
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8')
        
        works = scrape_works(html)
        food = scrape_food(html)
        egg = EGG_MAP.get(pal.get('element', 'neutral'), 'Unknown Egg')
        
        pal['work'] = works
        pal['food'] = food
        pal['egg'] = egg
        
        works_str = ', '.join(f'{k} Lv{v}' for k, v in sorted(works.items())) or 'none'
        print(f"  ✅ [{i+1}/{len(todo)}] {name:20s} | {works_str}")
        
        time.sleep(0.8)
        
    except Exception as e:
        print(f"  ⚠️  [{i+1}/{len(todo)}] {name:20s} ERROR: {str(e)[:60]}")
        errors += 1
        time.sleep(1)

# Save
with open(r'D:\幻兽帕鲁\paltool\pals.json', 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f"\nDone! {len(todo)-errors}/{len(todo)} scraped ({errors} errors)")
