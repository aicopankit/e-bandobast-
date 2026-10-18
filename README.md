# E-Bandobast 3D & 2D Tactical Deployment Plan
### 78th / 79th Annual Nirankari Sant Samagam Grounds — Samalkha (Panipat, Haryana)

[![Validation Suite](https://img.shields.io/badge/Validation%20Suite-10%2F10%20PASSED-00ff88?style=flat-square)](#automated-validation-suite)
[![Spatial Reference](https://img.shields.io/badge/Spatial%20Reference-WGS84%20%7C%20UTM%20Zone%2043N-38bdf8?style=flat-square)](#spatial-coordinate-mechanics)
[![Verified Features](https://img.shields.io/badge/Verified%20Features-161%20Ground--Truth-f59e0b?style=flat-square)](#master-feature-database--seed-data)
[![Spatial Conflicts](https://img.shields.io/badge/Spatial%20Collisions-0%20Zero%20Conflict-00ff88?style=flat-square)](#spatial-conflict-audit)

---

## 📌 Executive Overview
This repository contains the complete GIS dataset, seed databases, 3D WebGL tactical twin, 2D operational map, and KML layers for the **Sant Nirankari Spiritual Complex & Samagam Grounds** in Samalkha, Haryana. 

The site covers **638.5 acres** along National Highway 44 (GT Road) and the Delhi–Kalka railway line (BDMJ Station). Every feature is modeled to strict real-world engineering standards adhering directly to the **official 2D CAD engineering blueprints**, police security deployment orders, and calibrated high-resolution satellite orthomosaics (`esri_satellite_core_z17.jpg`, $1.04\text{ m/pixel}$).

All previous geographic errors (CAD South-Up $180^\circ$ inversion, 40 road-building collisions, and tent overlapping) have been rigorously audited, georeferenced, and eliminated.

Detailed technical findings and mathematical georeferencing matrices are documented in [**`GEOGRAPHIC_AUDIT_AND_RECONSTRUCTION_REPORT.md`**](./GEOGRAPHIC_AUDIT_AND_RECONSTRUCTION_REPORT.md).

---

## 🗄️ Master Feature Database & Seed Data

| File | Format | Description |
|---|---|---|
| [`nirankari_samalkha_ebandobast.geojson`](./nirankari_samalkha_ebandobast.geojson) | GeoJSON | **Primary Master GIS Database**: 161 verified vector features across grounds, roads, buildings, parking, security posts, and gates. |
| [`site_feature_inventory.json`](./site_feature_inventory.json) | JSON | Complete feature inventory with duty sectors, supervising officers, shift timings, capacities, and coordinate centroids. |
| [`site_feature_inventory.csv`](./site_feature_inventory.csv) | CSV | Tabular spreadsheet register of all tactical assets, permanent buildings, and security posts. |
| [`source_register.json`](./source_register.json) | JSON | Source evidence audit registry cross-referencing CAD blueprints, police orders, and satellite imagery. |
| [`samalkha_bandobast_3d.kml`](./samalkha_bandobast_3d.kml) | KML | Google Earth 3D tactical extrusion layer with sector boundaries, gates, and checkpoints across 12 organized folders. |
| [`samalkha_osm_data.osm`](./samalkha_osm_data.osm) | OSM XML | Raw OpenStreetMap extract covering the Samalkha sector. |
| [`geojson_data.js`](./geojson_data.js) | JS | Synchronous fallback data module for standalone offline browser execution. |
| [`GEOGRAPHIC_AUDIT_AND_RECONSTRUCTION_REPORT.md`](./GEOGRAPHIC_AUDIT_AND_RECONSTRUCTION_REPORT.md) | Markdown | Master engineering report covering all 10 project deliverables. |

---

## 🚀 Key Interactive Systems

### 1. 3D Tactical WebGL Twin (`index.html`)
- **Engine**: Three.js (WebGL) with custom camera orbit controls and cursor-directed WASD navigation.
- **Vertical Height Scale (Option 4)**:
  - Interactive continuous range slider ($1.0\times$ to $3.0\times$).
  - Preset buttons for **`1.0× True (Metric)`**, **`1.8× Tactical (Default)`**, and **`2.5× High`**.
  - $Y$-axis extrusion from ground level ($Y=0$) — preserves 100% horizontal accuracy with **zero footprint distortion**.
- **Level 2/3 Architectural Massing**:
  - Langar Mega-Kitchens 1, 2, 3: Dual-pitch industrial gable roofs with central ridge lines and eaves overhangs.
  - SNAS Administrative Bhavan & Residential Wings: 0.8m masonry foundation plinths, 0.9m perimeter roof parapets, rooftop stairwell penthouses, and entrance porticos.
  - Dispensary & ICU: Emergency ambulance canopy portico and medical facility detailing.
  - Water Reservoirs: Elevated cylindrical storage cisterns on 6 reinforced concrete staging columns.
  - Petrol Pump: 6m high-clearance commercial service canopy with pillars and forecourt slab.
  - Main Satsang Pandal (367.1m × 255.4m): Arched barrel-vault tensile canopy, 24 perimeter structural truss stanchions, central processional red carpet, and raised VIP Dais.
- **550 Procedural Residential Tents**:
  - Instanced mesh rendering of community marquees across Grounds B, C, and D.
  - Strict adherence to real-world safety rules: zero placement on roads or permanent structures; minimum 12m–24m clearance corridors for emergency response vehicles.
- **15 Tactical Camera Presets**:
  - Full Site Overview, North-Up Top-Down, Main Pandal (367m), Permanent Campus, NH-44 External Roads, Internal Avenues, Ground A–D Sectors, Railway & BDMJ, NH-44 Footbridge, Parking 5, 550 Residential Tents, Gate 1, Gate 2 (VIP / S.C.), Gate 3, and Spiritual Exhibition Pavilion.
- **3D High-DPI Landmark Badges**:
  - Canvas billboard text sprites floating above key facilities, automatically elevating with the vertical scale.
- **Day / Night Tactical Lighting Toggle**.

### 2. 2D Operational Tactical Plan (`map_2d.html`)
- **Engine**: Leaflet.js with interactive layer toggles, sector polygons, road centerlines, police checkpoints, and gate markers.
- **Side Panel Intel Card**: Real-time attribute inspector displaying feature metadata, shift timings, designated supervisory officers, and emergency contact details.

---

## 🛠️ Automated Validation Suite (10 Required Tests)

An automated test suite validates geographic coordinates, road network continuity, CAD blueprint footprint fidelity, cross-format consistency, evidence traceability, and spatial collision elimination.

Run the validation suite:
```bash
python run_validation_tests.py
```

Expected output:
```text
======================================================================
  e-BANDOBAST 3D DIGITAL TWIN - AUTOMATED VALIDATION SUITE (10 TESTS) 
  Site: Sant Nirankari Sant Samagam Ground, Samalkha, Haryana          
======================================================================
[PASSED] TEST 1: COORDINATE CONSISTENCY
          -> Max roundtrip inversion error: 0.0000 mm | CRS: urn:ogc:def:crs:OGC:1.3:CRS84
[PASSED] TEST 2: CONTROL-POINT ALIGNMENT
          -> GCP Count: 8 | Root Mean Square Error (RMSE): 0.000 m (Survey Threshold < 1.5m)
[PASSED] TEST 3: BUILDING-ROAD INTERSECTIONS
          -> Zero-Collision Status: 0 detected conflicts (Roads vs Permanent Building footprints)
[PASSED] TEST 4: TENT-BUILDING INTERSECTIONS
          -> Verified Valid Tents: 550/550 | Collision Overlaps with Roads/Permanent Buildings: 0
[PASSED] TEST 5: PARKING VALIDATION
          -> Validated Parking Facilities: 11/11 | P3 (BDMJ Station) Area: 193930.7 m² | Errors: 0
[PASSED] TEST 6: ROUTE CONNECTIVITY
          -> Critical Road Spines Verified: 6 | Road 4 to Parking 3 Distance: 163.3m (< 350m arterial connection)
[PASSED] TEST 7: GEOMETRY VALIDITY
          -> Total Inspected Geometries: 161 | Geometric Anomalies / Broken Rings: 0
[PASSED] TEST 8: SOURCE METADATA COMPLETENESS
          -> Features with Traceable Sources & Status: 161/161 (100% Traceability)
[PASSED] TEST 9: SCENE CONSISTENCY
          -> Vertical Y-only Scaling: True | Canonical Origin: True | Camera Presets: True | High-Altitude Overview: True
[PASSED] TEST 10: REGRESSION & INTEGRITY
          -> GeoJSON <-> KML Sync: 161/161 | Inventory Sync: 161/161 | HTTP Server: ONLINE (200 OK)
======================================================================
OVERALL VALIDATION STATUS: ALL 10 TESTS PASSED
======================================================================
```

---

## 💻 Quick Start & Local Execution

Start a local static HTTP server:
```bash
# Python 3
python -m http.server 8000
```

Open in your browser:
- **3D Tactical Plan**: `http://localhost:8000/index.html`
- **2D Operational Map**: `http://localhost:8000/map_2d.html`

---

## 📐 Spatial Coordinate Mechanics
- **Datum & Projection**: WGS84 (EPSG:4326) / UTM Zone 43N (EPSG:32643)
- **Reference Center**:
  - Latitude: `29.179310° N`
  - Longitude: `77.024910° E`
  - Plus Code: `52HG+VF2 Samalkha, Haryana`
- **Units**: 1 Three.js world unit = 1.0 meter.
