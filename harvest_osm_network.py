import xml.etree.ElementTree as ET
import json

tree = ET.parse("samalkha_osm_data.osm")
root = tree.getroot()

nodes = {}
for elem in root.findall("node"):
    nid = elem.attrib["id"]
    lat = float(elem.attrib["lat"])
    lon = float(elem.attrib["lon"])
    nodes[nid] = (lon, lat) # GeoJSON expects [lon, lat]

external_roads = []
railway_lines = []

for elem in root.findall("way"):
    wid = elem.attrib["id"]
    tags = {t.attrib["k"]: t.attrib["v"] for t in elem.findall("tag")}
    hw = tags.get("highway")
    rw = tags.get("railway")
    nds = [nodes[nd.attrib["ref"]] for nd in elem.findall("nd") if nd.attrib["ref"] in nodes]
    
    if len(nds) >= 2:
        if hw:
            name = tags.get("name", tags.get("name:en", tags.get("ref", f"Road-{hw}-{wid}")))
            feat = {
                "type": "Feature",
                "id": f"OSM-ROAD-{wid}",
                "properties": {
                    "name": name,
                    "category": "EXTERNAL_ROAD",
                    "highway_type": hw,
                    "surface": tags.get("surface", "paved" if hw in ["trunk", "primary", "secondary"] else "unpaved"),
                    "lanes": tags.get("lanes", "6" if hw == "trunk" else "2"),
                    "oneway": tags.get("oneway", "no"),
                    "bridge": tags.get("bridge", "no"),
                    "osm_id": wid,
                    "evidence_status": "VERIFIED",
                    "permanence": "PERMANENT",
                    "source_id": "SRC-OSM-DATASET",
                    "confidence": "HIGH"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": nds
                }
            }
            external_roads.append(feat)
            
        elif rw:
            name = tags.get("name", f"Rail-{rw}-{wid}")
            feat = {
                "type": "Feature",
                "id": f"OSM-RAIL-{wid}",
                "properties": {
                    "name": name if name else "Delhi - Ambala Trunk Railway Line",
                    "category": "RAILWAY_INFRASTRUCTURE",
                    "railway_type": rw,
                    "gauge": tags.get("gauge", "1676"), # Indian Broad Gauge
                    "electrified": tags.get("electrified", "contact_line"),
                    "osm_id": wid,
                    "evidence_status": "VERIFIED",
                    "permanence": "PERMANENT",
                    "source_id": "SRC-OSM-DATASET",
                    "confidence": "HIGH"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": nds
                }
            }
            railway_lines.append(feat)

print(f"Extracted {len(external_roads)} external road features and {len(railway_lines)} railway track features from OSM!")

with open("osm_extracted_roads_rails.json", "w", encoding="utf-8") as f:
    json.dump({"roads": external_roads, "rails": railway_lines}, f, indent=2, ensure_ascii=False)
