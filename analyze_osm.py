import xml.etree.ElementTree as ET
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse('samalkha_osm_data.osm')
root = tree.getroot()

nodes = {}
ways = []
relations = []

for elem in root:
    if elem.tag == 'node':
        nid = elem.attrib['id']
        lat = float(elem.attrib['lat'])
        lon = float(elem.attrib['lon'])
        tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
        nodes[nid] = {'lat': lat, 'lon': lon, 'tags': tags}
    elif elem.tag == 'way':
        wid = elem.attrib['id']
        nds = [nd.attrib['ref'] for nd in elem.findall('nd')]
        tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
        ways.append({'id': wid, 'nds': nds, 'tags': tags})
    elif elem.tag == 'relation':
        rid = elem.attrib['id']
        members = [{'type': m.attrib['type'], 'ref': m.attrib['ref'], 'role': m.attrib['role']} for m in elem.findall('member')]
        tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
        relations.append({'id': rid, 'members': members, 'tags': tags})

print(f"Total Nodes: {len(nodes)}, Ways: {len(ways)}, Relations: {len(relations)}")

# Filter features
highways = [w for w in ways if 'highway' in w['tags']]
railways = [w for w in ways if 'railway' in w['tags']]
named_ways = [w for w in ways if 'name' in w['tags'] or 'name:en' in w['tags']]
named_nodes = [n for n in nodes.values() if 'name' in n['tags']]

summary = {
    "total_nodes": len(nodes),
    "total_ways": len(ways),
    "highways_count": len(highways),
    "railways_count": len(railways),
    "named_ways": [{"id": w['id'], "tags": w['tags']} for w in named_ways],
    "named_nodes": [{"tags": n['tags'], "lat": n['lat'], "lon": n['lon']} for n in named_nodes],
    "railways": [{"id": w['id'], "tags": w['tags']} for w in railways]
}

with open('osm_features_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("Saved osm_features_summary.json successfully.")

print("\n--- NAMED NODES (LANDMARKS & STATIONS) ---")
for n in named_nodes:
    name = n['tags'].get('name', '')
    name_en = n['tags'].get('name:en', '')
    print(f"* [{n['lat']:.5f}, {n['lon']:.5f}] {name} ({name_en}) | tags: {n['tags']}")

print("\n--- KEY NAMED HIGHWAYS / RAILWAYS ---")
for w in named_ways[:15]:
    print(f"* Way {w['id']}: {w['tags'].get('name')} ({w['tags'].get('ref', '')}) type={w['tags'].get('highway', w['tags'].get('railway'))}")
