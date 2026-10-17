import json
import csv
import os

print("=== AUDITING EXISTING PROJECT ASSETS ===")

files_to_check = [
    "index.html",
    "samalkha_bandobast_3d.kml",
    "map_2d.html",
    "nirankari_samalkha_ebandobast.geojson",
    "site_feature_inventory.csv",
    "site_feature_inventory.json",
    "source_register.json",
    "esri_satellite_detail_z16.jpg",
    "samalkha_osm_data.osm"
]

for f in files_to_check:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    print(f"File: {f:38} | Exists: {str(exists):5} | Size: {size:8} bytes")

# Inspect GeoJSON contents
with open("nirankari_samalkha_ebandobast.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

print(f"\nGeoJSON Feature Count: {len(geo['features'])}")
categories = {}
status_counts = {}
for feat in geo["features"]:
    cat = feat["properties"].get("category", "Unknown")
    stat = feat["properties"].get("evidence_status", "Unknown")
    categories[cat] = categories.get(cat, 0) + 1
    status_counts[stat] = status_counts.get(stat, 0) + 1

print("Categories in GeoJSON:", categories)
print("Evidence Status breakdown in GeoJSON:", status_counts)

# Inspect OSM raw vector data available in samalkha_osm_data.osm
import xml.etree.ElementTree as ET
osm_tree = ET.parse("samalkha_osm_data.osm")
osm_root = osm_tree.getroot()
osm_highways = [e for e in osm_root.findall("way") if any(t.attrib['k'] == 'highway' for t in e.findall('tag'))]
osm_railways = [e for e in osm_root.findall("way") if any(t.attrib['k'] == 'railway' for t in e.findall('tag'))]
osm_buildings = [e for e in osm_root.findall("way") if any(t.attrib['k'] == 'building' for t in e.findall('tag'))]
print(f"\nAvailable Unharvested OSM Raw Data:")
print(f"  Highways available: {len(osm_highways)}")
print(f"  Railways available: {len(osm_railways)}")
print(f"  Buildings in OSM:    {len(osm_buildings)}")
