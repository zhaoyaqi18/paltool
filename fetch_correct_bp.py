import subprocess, re, json, time, sys

pals_json_path = r'D:\幻兽帕鲁\paltool\pals.json'

with open(pals_json_path, 'r', encoding='utf-8') as f:
    pals = json.load(f)

def fetch_combi_rank(name, pal_id):
    """Fetch CombiRank from paldb.cc"""
    # Handle special name mappings
    name_overrides = {
        'kingpaca_cryst': 'Kingpaca_Cryst',
    }
    if pal_id in name_overrides:
        url_name = name_overrides[pal_id]
    else:
        url_name = name.replace(' ', '_').replace("'", '').replace('.', '')
    url = f'https://paldb.cc/en/{url_name}'
    
    for attempt in range(2):
        try:
            result = subprocess.run(
                ['curl', '-s', url,
                 '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                 '--max-time', '8'],
                capture_output=True, text=True, timeout=10
            )
            html = result.stdout
            if len(html) < 1000:
                return None
            idx = html.find('CombiRank')
            if idx > 0:
                section = html[idx:idx+400]
                m = re.search(r'<div>(\d+)</div>', section)
                if m:
                    return int(m.group(1))
            
            # Try alternate: look for "CombiRank" in the aria-valuenow attribute context
            # Some pages might have different format
            matches = re.findall(r'CombiRank[^<]*<[^>]*>[^<]*<[^>]*>[^<]*<[^>]*>(\d+)', html)
            if matches:
                return int(matches[0])
            return None
        except:
            time.sleep(3)
    return None

total = len(pals)
updated = 0
failed = 0

for i, p in enumerate(pals):
    pal_id = p['id']
    name = p['name']
    
    old_bp = p['bp']
    new_bp = fetch_combi_rank(name, pal_id)
    
    if new_bp and new_bp != old_bp:
        p['bp'] = new_bp
        updated += 1
        print(f"[{i+1}/{total}] {name:20s} BP: {old_bp:5d} → {new_bp:5d}")
    elif new_bp and new_bp == old_bp:
        print(f"[{i+1}/{total}] {name:20s} BP: {old_bp:5d} ✓ (unchanged)")
    else:
        failed += 1
        print(f"[{i+1}/{total}] {name:20s} ✗ FAILED to fetch")
    
    # Rate limit
    if (i + 1) % 5 == 0:
        time.sleep(2)
    else:
        time.sleep(1.5)

# Save
with open(pals_json_path, 'w', encoding='utf-8') as f:
    json.dump(pals, f, indent=2, ensure_ascii=False)

print(f"\nDone! Updated: {updated}, Failed: {failed}, Total: {total}")
