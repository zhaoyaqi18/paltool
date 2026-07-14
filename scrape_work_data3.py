"""Parallel scraper for pal work data - much faster"""
import json, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def scrape_one(name, pal_id, element):
    url_name = name.replace(' ', '_').replace("'", '').replace('.', '')
    if pal_id == 'kingpaca_cryst': url_name = 'Kingpaca_Cryst'
    if pal_id == 'ribunny': url_name = 'Ribunny'
    
    url = f'https://paldb.cc/en/{url_name}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        
        works = {}
        for icon, wname in WORK_ICONS.items():
            idx = html.find(icon)
            if idx > 0:
                m = re.search(r'Lv(\d+)', html[idx:idx+400])
                if m: works[wname] = int(m.group(1))
        
        food = 7
        fm = re.search(r'FoodAmount[^>]*>(\d+)', html)
        if fm: food = int(fm.group(1))
        
        egg = EGG_MAP.get(element, 'Common Egg')
        return (name, works, food, egg, None)
    except Exception as e:
        return (name, {}, 7, 'Common Egg', str(e)[:60])

# Load
with open(r'D:\幻兽帕鲁\paltool\pals.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)

print(f"Scraping {len(pals)} pals in parallel...")

# Parallel scrape with 8 workers
results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = {ex.submit(scrape_one, p['name'], p['id'], p.get('element', 'neutral')): p['name'] for p in pals}
    done = 0
    for f in as_completed(futures):
        name, works, food, egg, err = f.result()
        done += 1
        if err:
            print(f"  ⚠️ [{done}/{len(pals)}] {name:20s} {err}")
        else:
            ws = ', '.join(f'{k} Lv{v}' for k,v in sorted(works.items())) or 'none'
            print(f"  ✅ [{done}/{len(pals)}] {name:20s} | {egg:20s} | {ws}")
        results[name] = (works, food, egg)
        time.sleep(0.2)  # light rate limit
    
# Update pals
for p in pals:
    n = p['name']
    if n in results:
        p['work'] = results[n][0]
        p['food'] = results[n][1]
        p['egg'] = results[n][2]

with open(r'D:\幻兽帕鲁\paltool\pals.json', 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

# Verify
has_work = sum(1 for p in pals if p.get('work') and p['work'] != {})
has_egg = sum(1 for p in pals if 'egg' in p)
errs = sum(1 for p in pals if not p.get('work') or p['work'] == {})

print(f"\n{'='*50}")
print(f"Work data: {has_work}/{len(pals)}")
print(f"Egg types: {has_egg}/{len(pals)}")
print(f"Errors: {errs}/{len(pals)}")
