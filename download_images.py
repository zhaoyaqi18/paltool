import json, os, time, urllib.request, urllib.error, sys

pals_json_path = r'D:\幻兽帕鲁\paltool\pals.json'
img_dir = r'D:\幻兽帕鲁\paltool\img\pals'
os.makedirs(img_dir, exist_ok=True)

with open(pals_json_path, 'r', encoding='utf-8') as f:
    pals = json.load(f)

# Build set of what's already downloaded
existing = set()
if os.path.exists(img_dir):
    for fname in os.listdir(img_dir):
        name_no_ext = os.path.splitext(fname)[0]
        existing.add(name_no_ext.lower())

print(f"Existing: {len(existing)} images")
print(f"Total: {len(pals)} pals")

# Track which pals got images
updated = []
total = len(pals)

for i, p in enumerate(pals):
    pal_id = p['id']
    safe_name = pal_id.lower()
    
    if safe_name in existing:
        # Already have it
        p['image'] = f'img/pals/{safe_name}.png'
        updated.append(p)
        continue
    
    # Try different URL sources  
    urls_to_try = [
        # wiki.gg with filename matching the name field (spaces → underscores)
        f"https://palworld.wiki.gg/wiki/Special:FilePath/{p['name'].replace(' ', '_')}.png",
        # Try with encoded spaces
        f"https://palworld.wiki.gg/wiki/Special:FilePath/{p['name'].replace(' ', '%20')}.png",
    ]
    
    downloaded = False
    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "image/webp,image/png,image/*,*/*;q=0.8",
                "Referer": "https://palworld.wiki.gg/"
            })
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read()
            
            if len(data) > 100:
                filepath = os.path.join(img_dir, f"{safe_name}.png")
                with open(filepath, 'wb') as f:
                    f.write(data)
                print(f"[{i+1}/{total}] ✓ {p['name']} ({len(data)} bytes)")
                p['image'] = f'img/pals/{safe_name}.png'
                downloaded = True
                break
            else:
                print(f"[{i+1}/{total}] ✗ {p['name']} too small ({len(data)} bytes)")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[{i+1}/{total}] ⏳ {p['name']} rate limited, waiting 5s...")
                time.sleep(5)
            else:
                pass  # try next URL
        except Exception as e:
            pass  # try next URL
    
    if not downloaded:
        print(f"[{i+1}/{total}] ✗ {p['name']} - no source worked, using fallback")
        p['image'] = ''  # No image, will show fallback letter
        # Clean the pals.json later
    
    updated.append(p)
    
    # Rate limit: wait 1.5s between requests
    if (i+1) % 3 == 0:
        print(f"  --- rate limit pause ---")
    time.sleep(1.5)

# Save updated pals.json
with open(pals_json_path, 'w', encoding='utf-8') as f:
    json.dump(updated, f, indent=2, ensure_ascii=False)

print(f"\nDone! Downloaded images. Updated pals.json with local paths.")
print(f"Total with images: {sum(1 for p in updated if p.get('image') and 'img/' in p['image'])}")
