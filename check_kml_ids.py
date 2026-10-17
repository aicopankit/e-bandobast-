import json

with open('nirankari_samalkha_ebandobast.geojson', 'r', encoding='utf-8') as f:
    geo = json.load(f)
with open('samalkha_bandobast_3d.kml', 'r', encoding='utf-8') as f:
    kml = f.read()

missing = []
for feat in geo['features']:
    fid = feat['id']
    if f'id="{fid}"' not in kml:
        missing.append((fid, feat['properties'].get('category')))

print(f"Total missing: {len(missing)}")
for m in missing[:15]:
    print("Missing:", m)
