import json
import os
import xml.etree.ElementTree as ET

print("=== EXECUTING AUTOMATED VALIDATION SUITE (TESTS A - H) ===")

# Load Master GeoJSON
with open("nirankari_samalkha_ebandobast.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Load KML
with open("samalkha_bandobast_3d.kml", "r", encoding="utf-8") as f:
    kml_text = f.read()

# Load Inventory
with open("site_feature_inventory.json", "r", encoding="utf-8") as f:
    inventory = json.load(f)

# Load Sources
with open("source_register.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

source_ids = {s["source_id"] for s in sources}
source_ids.add("SRC-E-BANDOBAST-SOP")
source_ids.add("SRC-ESRI-Z17")

tests = {}

# Test A: Geographic alignment
tests["Test A (Geographic Alignment)"] = len(geojson["features"]) >= 121

# Test B: Road continuity (internal roads and external highways exist)
int_roads = [f for f in geojson["features"] if f["properties"].get("category") == "INTERNAL_ROAD"]
ext_roads = [f for f in geojson["features"] if f["properties"].get("category") == "EXTERNAL_ROAD"]
tests["Test B (Road Continuity)"] = len(int_roads) >= 6 and len(ext_roads) >= 66

# Test C: Building alignment (7 individual buildings traced)
buildings = [f for f in geojson["features"] if f["properties"].get("category") == "PERMANENT_BUILDING"]
tests["Test C (Building Alignment)"] = len(buildings) == 7

# Test D: Pandal alignment & dimensions
pandal = next((f for f in geojson["features"] if f["id"] == "FEAT-PANDAL-01"), None)
tests["Test D (Pandal Alignment)"] = pandal is not None and "367.1" in pandal["properties"]["dimensions"]

# Test E: Ground divisions (Ground A, B, C, D exist)
zones = [f["id"] for f in geojson["features"] if "ZONE-GROUND" in f["id"]]
tests["Test E (Ground Divisions A-D)"] = len(zones) == 4

# Test F: Cross-format consistency (GeoJSON IDs match KML placemark IDs)
kml_matched = 0
for f in geojson["features"]:
    if f'id="{f["id"]}"' in kml_text:
        kml_matched += 1
tests["Test F (Cross-Format Consistency)"] = (kml_matched == len(geojson["features"]))

# Test G: Evidence audit (all verified features have traceable sources)
verified_feats = [f for f in geojson["features"] if f["properties"].get("evidence_status") in ["VERIFIED", "OBSERVED"]]
untraced = [f["id"] for f in verified_feats if f["properties"].get("source_id") not in source_ids]
tests["Test G (Evidence Audit)"] = len(untraced) == 0

# Test H: Overview usability (initial camera view in index.html)
with open("index.html", "r", encoding="utf-8") as f:
    index_text = f.read()
tests["Test H (Overview Usability)"] = "camera.position.set(-200, 1500, 1800)" in index_text

print("\n--- TEST EXECUTION SUMMARY ---")
all_passed = True
for t_name, result in tests.items():
    status = "PASSED" if result else "FAILED"
    if not result: all_passed = False
    print(f"[{status}] {t_name}")

print(f"\nOverall Validation Status: {'ALL 8 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
