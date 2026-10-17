import json
import csv

# 1. GENERATE SOURCE REGISTER
sources = [
    {
        "source_id": "SRC-OFFICIAL-FAQ-78",
        "title": "78th Annual Nirankari Sant Samagam - Frequently Asked Questions",
        "publisher": "Sant Nirankari Mandal (Regd.)",
        "url": "https://nirankari.org/faqs-78thsamagam/",
        "source_type": "Primary Event Organization & Ground Layout Documentation",
        "publication_date": "2025-10-05",
        "imagery_date": "N/A (Textual Blueprint)",
        "access_date": "2026-10-17",
        "licence": "Public Information / Official Mission Announcement",
        "reliability_rating": "A1 (Highest Primary Reliability)",
        "geographic_coverage": "Complete Samagam Venue (Grounds A, B, C, D)",
        "what_it_confirms": "Confirms the 4 primary ground designations: Ground A (Main Satsang Pandal area adjacent to GT Road), Ground B (Left side behind Ground A), Ground C (Right side behind Ground A), Ground D (Behind Ground C adjacent to Bhodwal Majri railway station). Confirms 100-bed hospital + 10-bed ICU, Central Accounts office, securities room, ATM placements, Langar service, and train stoppage arrangements.",
        "what_it_does_not_confirm": "Does not give CAD/DWG coordinates or centimetre-level fencing dimensions."
    },
    {
        "source_id": "SRC-OFFICIAL-PAGE-79",
        "title": "79th Nirankari Sant Samagam Information & Schedules",
        "publisher": "Sant Nirankari Mandal (Regd.)",
        "url": "https://nirankari.org/79th-nirankari-sant-samagam/",
        "source_type": "Primary Event Official Portal",
        "publication_date": "2026-10-11",
        "imagery_date": "2026",
        "access_date": "2026-10-17",
        "licence": "Public Information / Official Mission Portal",
        "reliability_rating": "A1 (Highest Primary Reliability)",
        "geographic_coverage": "Venue Complex & Railway Connectivity",
        "what_it_confirms": "Confirms continuity of venue at Sant Nirankari Adhyatmik Sthal, Samalkha, Brahm Gyan Kaksh distributions across Grounds B, C, D, and Bhodwal Majri (BDMJ) station train stoppage schedules.",
        "what_it_does_not_confirm": "Specific internal barrier line geometry."
    },
    {
        "source_id": "SRC-FLICKR-49144669308",
        "title": "Aerial view of Samagam Ground (Daylight)",
        "publisher": "Sant Nirankari Mission Official Flickr",
        "url": "https://www.flickr.com/photos/santnirankarimission/49144669308",
        "source_type": "Official Drone / Aerial Photographic Evidence",
        "publication_date": "2019-11-16",
        "imagery_date": "2019-11-16 17:16:29",
        "access_date": "2026-10-17",
        "licence": "Official Mission Media Archive",
        "reliability_rating": "A1 (Direct Visual Photographic Proof)",
        "geographic_coverage": "Ground A, Ceremonial Entrance Gate, Main Satsang Pandal, Stage Axis",
        "what_it_confirms": "Confirms tri-arch monumental Ceremonial Entrance Portal, axial central processional carpeted aisle, massive arched barrel-vault curved steel truss Pandal roof, dais location at west end, LED wall positions, and high-mast floodlight towers.",
        "what_it_does_not_confirm": "Western remote tent perimeter near railway tracks."
    },
    {
        "source_id": "SRC-FLICKR-49144669063",
        "title": "Aerial view of Samagam Ground (Dusk / Night Grid)",
        "publisher": "Sant Nirankari Mission Official Flickr",
        "url": "https://www.flickr.com/photos/santnirankarimission/49144669063",
        "source_type": "Official Drone / Aerial Photographic Evidence",
        "publication_date": "2019-11-16",
        "imagery_date": "2019-11-16 18:47:02",
        "access_date": "2026-10-17",
        "licence": "Official Mission Media Archive",
        "reliability_rating": "A1 (Direct Visual Grid Structure Proof)",
        "geographic_coverage": "Entire Township Grid, Pandal Roof, Illuminated Sector Avenues",
        "what_it_confirms": "Confirms the orthogonal grid of roads and illuminated streets extending westward behind the pandal across the entire residential tent city; confirms roof vents/slots and marquee warehouses along northern flank.",
        "what_it_does_not_confirm": "Sub-surface utilities."
    },
    {
        "source_id": "SRC-FLICKR-54897551677",
        "title": "Samagam Sewa in Full Swing - Preparation of Samagam Gates",
        "publisher": "Sant Nirankari Mission Official Flickr Album (72177720330063925)",
        "url": "https://www.flickr.com/photos/santnirankarimission/54897551677",
        "source_type": "Official Ground-Level Site Construction Imagery",
        "publication_date": "2025-10-10",
        "imagery_date": "2025-10-10 07:13:05",
        "access_date": "2026-10-17",
        "licence": "Official Mission Media Archive",
        "reliability_rating": "A1 (Ground Truth Verification)",
        "geographic_coverage": "Ceremonial Gate 1 footprint and frontage plaza",
        "what_it_confirms": "Confirms monumental gate construction scale (~14m high, multi-tiered), brick edging, alluvial sandy soil terrain, and Sewadal security operations.",
        "what_it_does_not_confirm": "Internal Pandal acoustics."
    },
    {
        "source_id": "SRC-ESRI-Z16",
        "title": "Esri World Imagery (High-Resolution Satellite Orthomosaic)",
        "publisher": "Esri, Maxar, Earthstar Geographics",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
        "source_type": "Calibrated Top-Down Satellite Orthoimagery (Zoom 15 & 16)",
        "publication_date": "2024-2025",
        "imagery_date": "Recent cloud-free Maxar acquisition (~2023-2024)",
        "access_date": "2026-10-17",
        "licence": "Esri Geospatial Data Usage Terms",
        "reliability_rating": "A1 (Georeferenced Metric Measurement)",
        "geographic_coverage": "Complete Samalkha Venue (29.171°N to 29.191°N, 77.008°E to 77.031°E)",
        "what_it_confirms": "Direct visual measurement of Main Pandal footprint (367.2m x 255.5m), permanent institutional campus (260.7m x 301.1m), NH-44 highway frontage, internal road grid corridors, and distance to Bhodwal Majri station (1.73 km).",
        "what_it_does_not_confirm": "Live temporary event tents when captured during off-season."
    },
    {
        "source_id": "SRC-OSM-DATASET",
        "title": "OpenStreetMap Geographic Vector Dataset (Samalkha Sub-district)",
        "publisher": "OpenStreetMap Contributors",
        "url": "https://www.openstreetmap.org",
        "source_type": "Collaborative Geospatial Database (Vector XML)",
        "publication_date": "2026",
        "imagery_date": "Continuously updated vector data",
        "access_date": "2026-10-17",
        "licence": "Open Database License (ODbL)",
        "reliability_rating": "A2 (Authoritative for Public Linear Infrastructure)",
        "geographic_coverage": "NH-44 Corridor, Northern Railway Delhi-Ambala Trunk Line, BDMJ Station",
        "what_it_confirms": "Confirms BDMJ railway station node (lat 29.18523, lon 77.00842), NH-44 Grand Trunk Road dual carriageway alignment, fuel stations, and surrounding rural road rights-of-way.",
        "what_it_does_not_confirm": "Internal event-specific temporary security barricades."
    }
]

with open("source_register.json", "w", encoding="utf-8") as f:
    json.dump(sources, f, indent=2, ensure_ascii=False)

print("Saved source_register.json.")

# 2. GENERATE SITE FEATURE INVENTORY CSV & JSON
with open("nirankari_samalkha_ebandobast.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

inventory = []
for feat in geo["features"]:
    p = feat["properties"]
    geom = feat["geometry"]
    inventory.append({
        "feature_id": feat["id"],
        "name": p.get("name"),
        "category": p.get("category"),
        "evidence_status": p.get("evidence_status"),
        "permanence": p.get("permanence"),
        "geometry_type": geom["type"],
        "dimensions": p.get("dimensions", "N/A"),
        "area_acres": p.get("area_acres", "N/A"),
        "elevation_m": p.get("elevation_m", 228),
        "confidence": p.get("confidence"),
        "source_id": p.get("source_id"),
        "notes": p.get("notes")
    })

with open("site_feature_inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2, ensure_ascii=False)

with open("site_feature_inventory.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(inventory[0].keys()))
    writer.writeheader()
    writer.writerows(inventory)

print("Saved site_feature_inventory.json and site_feature_inventory.csv.")
