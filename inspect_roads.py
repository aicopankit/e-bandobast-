import xml.etree.ElementTree as ET
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse('samalkha_osm_data.osm')
root = tree.getroot()

nodes = {elem.attrib['id']: (float(elem.attrib['lat']), float(elem.attrib['lon'])) for elem in root if elem.tag == 'node'}

road_segments = []

for elem in root:
    if elem.tag == 'way':
        tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
        hw = tags.get('highway')
        rw = tags.get('railway')
        name = tags.get('name', tags.get('name:en', ''))
        nds = [nodes[nd.attrib['ref']] for nd in elem.findall('nd') if nd.attrib['ref'] in nodes]
        if nds and (hw or rw):
            lats = [pt[0] for pt in nds]
            lons = [pt[1] for pt in nds]
            road_segments.append({
                'id': elem.attrib['id'],
                'type': hw if hw else rw,
                'category': 'railway' if rw else 'highway',
                'name': name,
                'tags': tags,
                'lat_range': [min(lats), max(lats)],
                'lon_range': [min(lons), max(lons)],
                'points_count': len(nds),
                'coordinates': nds
            })

print(f"Extracted {len(road_segments)} road and rail segments.")

# Group by category
hw_types = {}
for s in road_segments:
    t = s['type']
    hw_types[t] = hw_types.get(t, 0) + 1

print("Segment breakdown by type:", hw_types)

# Find roads connecting GT Road (lon ~77.026) to Railway Station (lon ~77.008)
connecting_roads = []
for s in road_segments:
    if s['lon_range'][0] < 77.015 and s['lon_range'][1] > 77.015:
        connecting_roads.append(s)

print(f"\nEast-West connecting corridors crossing longitude 77.015: {len(connecting_roads)}")
for r in connecting_roads:
    print(f"* Way {r['id']} ({r['type']}): name='{r['name']}', lat range: {r['lat_range']}, tags: {r['tags']}")

with open('osm_road_segments.json', 'w', encoding='utf-8') as f:
    json.dump(road_segments, f, indent=2, ensure_ascii=False)
