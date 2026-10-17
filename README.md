# E-Bandobast 3D & 2D Tactical Deployment Plan
### 78th / 79th Annual Nirankari Sant Samagam Grounds — Samalkha (Panipat, Haryana)

[![Validation Suite](https://img.shields.io/badge/Validation%20Suite-8%2F8%20PASSED-00ff88?style=flat-square)](#automated-validation-suite)
[![Spatial Reference](https://img.shields.io/badge/Spatial%20Reference-WGS84%20%7C%20UTM%20Zone%2043N-38bdf8?style=flat-square)](#spatial-coordinate-mechanics)
[![Verified Features](https://img.shields.io/badge/Verified%20Features-159%20Ground--Truth-f59e0b?style=flat-square)](#master-feature-database--seed-data)

---

## 📌 Executive Overview
This repository contains the complete GIS dataset, seed databases, 3D WebGL tactical twin, 2D operational map, and KML layers for the **Sant Nirankari Spiritual Complex & Samagam Grounds** in Samalkha, Haryana. 

The site covers **638.5 acres** along National Highway 44 (GT Road) and the Delhi–Kalka railway line (BDMJ Station). Every feature is modeled to strict real-world engineering standards adhering directly to the **official 2D CAD engineering blueprint**, police security deployment orders, and high-resolution satellite orthomosaics.

---

## 🗄️ Master Feature Database & Seed Data

| File | Format | Description |
|---|---|---|
| [`nirankari_samalkha_ebandobast.geojson`](./nirankari_samalkha_ebandobast.geojson) | GeoJSON | **Primary Master GIS Database**: 159 verified vector features across grounds, roads, buildings, parking, security posts, and gates. |
| [`site_feature_inventory.json`](./site_feature_inventory.json) | JSON | Complete feature inventory with duty sectors, supervising officers, shift timings, capacities, and coordinate centroids. |
| [`site_feature_inventory.csv`](./site_feature_inventory.csv) | CSV | Tabular spreadsheet register of all tactical assets and security posts. |
| [`source_register.json`](./source_register.json) | JSON | Source evidence audit registry cross-referencing CAD blueprints, police orders, and satellite imagery. |
| [`samalkha_bandobast_3d.kml`](./samalkha_bandobast_3d.kml) | KML | Google Earth 3D tactical extrusion layer with sector boundaries, gates, and checkpoints. |
| [`samalkha_osm_data.osm`](./samalkha_osm_data.osm) | OSM XML | Raw OpenStreetMap extract covering the Samalkha sector. |
| [`geojson_data.js`](./geojson_data.js) | JS | Synchronous fallback data module for standalone offline browser execution. |

---

## 🚀 Key Interactive Systems

### 1. 3D Tactical WebGL Twin (`index.html`)
- **Engine**: Three.js (WebGL) with custom camera orbit controls and cursor-directed WASD navigation.
- **Vertical Height Scale (Option 4)**:
  - Interactive continuous range slider ($1.0\times$ to $3.0\times$).
  - Preset buttons for **`1.0× True (Metric)`**, **`1.8× Tactical (Default)`**, and **`2.5× High`**.
  - $Y$-axis extrusion from ground level ($Y=0$) — preserves 100% horizontal accuracy with zero footprint distortion.
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

## 🛠️ Automated Validation Suite

An automated test suite validates geographic coordinates, road network continuity, CAD blueprint footprint fidelity, cross-format consistency, and evidence traceability.

Run the validation suite:
```bash
python run_validation_tests.py
```

Expected output:
```text
=== EXECUTING AUTOMATED VALIDATION SUITE (TESTS A - H) ===

--- TEST EXECUTION SUMMARY ---
[PASSED] Test A (Geographic Alignment)
[PASSED] Test B (Road Continuity)
[PASSED] Test C (Building Alignment)
[PASSED] Test D (Pandal Alignment)
[PASSED] Test E (Ground Divisions A-D)
[PASSED] Test F (Cross-Format Consistency)
[PASSED] Test G (Evidence Audit)
[PASSED] Test H (Overview Usability)

Overall Validation Status: ALL 8 TESTS PASSED
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
  - Latitude: `29.1805° N`
  - Longitude: `77.0249° E`
  - Plus Code: `52HG+VF2 Samalkha, Haryana`
- **Units**: 1 Three.js world unit = 1.0 meter.
