"""Batch scrape work suitabilities and egg types from paldb.cc"""
import json, re, time, urllib.request, urllib.error

# Element -> Egg Type mapping (Palworld standard)
EGG_MAP = {
    'neutral': ('Common Egg', 'TitemiconMaterialPalEggNormal01'),
    'fire': ('Scorching Egg', 'TitemiconMaterialPalEggFlame01'),
    'water': ('Wetland Egg', 'TitemiconMaterialPalEggAqua01'),
    'grass': ('Verdant Egg', 'TitemiconMaterialPalEggLeaf01'),
    'electric': ('Electric Egg', 'TitemiconMaterialPalEggThunder01'),
    'ice': ('Frozen Egg', 'TitemiconMaterialPalEggIce01'),
    'ground': ('Rocky Egg', 'TitemiconMaterialPalEggEarth01'),
    'dark': ('Dark Egg', 'TitemiconMaterialPalEggDark01'),
    'dragon': ('Dragon Egg', 'TitemiconMaterialPalEggDragon01'),
}

# Work suitability icon mapping
WORK_ICONS = {
    'Ticonpalwork00': 'Kindling', 'Ticonpalwork01': 'Watering',
    'Ticonpalwork02': 'Planting', 'Ticonpalwork03': 'GeneratingElectricity',
    'Ticonpalwork04': 'Handiwork', 'Ticonpalwork05': 'Gathering',
    'Ticonpalwork06': 'Lumbering', 'Ticonpalwork07': 'Mining',
    'Ticonpalwork08': 'MedicineProduction', 'Ticonpalwork10': 'Cooling',
    'Ticonpalwork11': 'Transporting', 'Ticonpalwork12': 'Farming',
}

def scrape_pal(page_html, pal_name):
    """Extract work suitabilities from paldb page HTML"""
    works = {}
    
    # Find Work Suitability section and extract levels
    # Pattern: TiconpalworkXX followed by LvN
    for icon_id, work_name in WORK_ICONS.items():
        idx = page_html.find(icon_id)
        if idx > 0:
            # Look for "Lv" after the icon
            after = page_html[idx:idx+300]
            m = re.search(r'Lv(\d+)', after)
            if m:
                works[work_name] = int(m.group(1))
    
    # Also check food
    food = 7  # default
    fm = re.search(r'FoodAmount[^>]*>(\d+)', page_html)
    if fm:
        food = int(fm.group(1))
    
    return works, food

# Load current pals data
with open(r'D:\幻兽帕鲁\paltool\pals.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)

print(f"Scraping {len(pals)} pals from paldb.cc...\n")

errors = 0
for i, pal in enumerate(pals):
    name = pal['name']
    url_name = name.replace(' ', '_').replace("'", '').replace('.', '')
    if pal['id'] == 'kingpaca_cryst':
        url_name = 'Kingpaca_Cryst'
    
    url = f'https://paldb.cc/en/{url_name}'
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8')
        
        works, food = scrape_pal(html, name)
        
        # Egg type from element
        elem = pal.get('element', 'neutral')
        egg_name, egg_icon = EGG_MAP.get(elem, ('Unknown Egg', ''))
        
        # Add to pal data
        pal['egg'] = f"{egg_name}"
        pal['eggIcon'] = egg_icon
        pal['work'] = works
        pal['food'] = food
        
        status = '✅' if works else '⚠️'
        works_str = ', '.join(f'{k} Lv{v}' for k, v in sorted(works.items()))
        if not works_str: works_str = 'none'
        print(f"  {status} [{i+1}/{len(pals)}] {name:20s} | {egg_name:20s} | {works_str}")
        
        time.sleep(1.0)  # rate limit
        
    except Exception as e:
        print(f"  ❌ [{i+1}/{len(pals)}] {name:20s} ERROR: {str(e)[:60]}")
        errors += 1
        time.sleep(2)

print(f"\n{'='*60}")
print(f"Done! {len(pals)-errors}/{len(pals)} scraped successfully ({errors} errors)")

# Save
with open(r'D:\幻兽帕鲁\paltool\pals.json', 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f"Data saved to pals.json")
