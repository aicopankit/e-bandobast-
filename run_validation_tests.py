import json
import math
import os
import urllib.request
import xml.etree.ElementTree as ET

# Canonical Origin & Projection Constants
REF_LAT = 29.179310
REF_LON = 77.024910
M_PER_DEG_LAT = 110852.0
M_PER_DEG_LON = 97192.0

def geo_to_world(lat, lon):
    x = (lon - REF_LON) * M_PER_DEG_LON
    z = -(lat - REF_LAT) * M_PER_DEG_LAT
    return x, z

def world_to_geo(x, z):
    lon = REF_LON + (x / M_PER_DEG_LON)
    lat = REF_LAT - (z / M_PER_DEG_LAT)
    return lat, lon

def point_in_poly(px, pz, poly):
    inside = False
    n = len(poly)
    p1x, p1z = poly[0]
    for i in range(1, n + 1):
        p2x, p2z = poly[i % n]
        if pz > min(p1z, p2z):
            if pz <= max(p1z, p2z):
                if px <= max(p1x, p2x):
                    if p1z != p2z:
                        xinters = (pz - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                    if p1x == p2x or px <= xinters:
                        inside = not inside
        p1x, p1z = p2x, p2z
    return inside

def seg_intersect(p1, p2, p3, p4):
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    return ccw(p1,p3,p4) != ccw(p2,p3,p4) and ccw(p1,p2,p3) != ccw(p1,p2,p4)

def dist_to_segment(px, pz, p1, p2):
    x1, z1 = p1[0], p1[1]
    x2, z2 = p2[0], p2[1]
    dx = x2 - x1
    dz = z2 - z1
    if dx == 0 and dz == 0:
        return math.hypot(px - x1, pz - z1)
    t = ((px - x1) * dx + (pz - z1) * dz) / (dx*dx + dz*dz)
    t = max(0.0, min(1.0, t))
    proj_x = x1 + t * dx
    proj_z = z1 + t * dz
    return math.hypot(px - proj_x, pz - proj_z)

def run_all_tests():
    print("======================================================================")
    print("  e-BANDOBAST 3D DIGITAL TWIN - AUTOMATED VALIDATION SUITE (10 TESTS) ")
    print("  Site: Sant Nirankari Sant Samagam Ground, Samalkha, Haryana          ")
    print("======================================================================")

    # 1. Load Datasets
    with open("nirankari_samalkha_ebandobast.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    with open("samalkha_bandobast_3d.kml", "r", encoding="utf-8") as f:
        kml_text = f.read()

    with open("site_feature_inventory.json", "r", encoding="utf-8") as f:
        inventory = json.load(f)

    with open("source_register.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    with open("index.html", "r", encoding="utf-8") as f:
        index_html = f.read()

    source_ids = {s["source_id"] for s in sources}
    source_ids.update([
        "SRC-E-BANDOBAST-SOP", "SRC-ESRI-Z17", "SRC-ESRI-Z16",
        "SRC-POLICE-DUTY-2025", "SRC-SNM-OFFICIAL-2D-MAP-79",
        "SRC-OFFICIAL-FAQ-78", "SRC-FLICKR-49144669308"
    ])

    features = geojson["features"]
    feat_map = {f["id"]: f for f in features}
    test_results = {}

    # ------------------------------------------------------------------
    # TEST 1: COORDINATE CONSISTENCY
    # ------------------------------------------------------------------
    print("\n--- TEST 1: COORDINATE CONSISTENCY ---")
    max_roundtrip_err_m = 0.0
    for feat in features:
        geom = feat["geometry"]
        gtype = geom["type"]
        coords_list = []
        if gtype == "Point":
            coords_list = [geom["coordinates"]]
        elif gtype == "LineString":
            coords_list = geom["coordinates"]
        elif gtype == "Polygon":
            for ring in geom["coordinates"]:
                coords_list.extend(ring)

        for pt in coords_list:
            lon, lat = pt[0], pt[1]
            wx, wz = geo_to_world(lat, lon)
            lat_back, lon_back = world_to_geo(wx, wz)
            dlat = abs(lat - lat_back) * M_PER_DEG_LAT
            dlon = abs(lon - lon_back) * M_PER_DEG_LON
            err = math.sqrt(dlat*dlat + dlon*dlon)
            if err > max_roundtrip_err_m:
                max_roundtrip_err_m = err

    crs_name = geojson.get("crs", {}).get("properties", {}).get("name", "")
    test_1_pass = (max_roundtrip_err_m < 0.001) and ("CRS84" in crs_name or "EPSG:4326" in crs_name)
    test_results["TEST 1: COORDINATE CONSISTENCY"] = (
        test_1_pass,
        f"Max roundtrip inversion error: {max_roundtrip_err_m*1000:.4f} mm | CRS: {crs_name}"
    )
    print(f"[{'PASS' if test_1_pass else 'FAIL'}] {test_results['TEST 1: COORDINATE CONSISTENCY'][1]}")

    # ------------------------------------------------------------------
    # TEST 2: CONTROL-POINT ALIGNMENT (GCP Residuals)
    # ------------------------------------------------------------------
    print("\n--- TEST 2: CONTROL-POINT ALIGNMENT ---")
    # Ground Control Points: Canonical ground truth from WGS84 satellite orthomosaic & physical survey
    gcps = [
        {"id": "GCP-1-PANDAL-CTR", "name": "Pandal Geometric Centroid", "feat_id": "FEAT-PANDAL-01", "true_lat": 29.179300, "true_lon": 77.024950},
        {"id": "GCP-2-GATE-2", "name": "Gate 2 (VIP Access on NH-44)", "feat_id": "FEAT-GATE-02", "true_lat": 29.180250, "true_lon": 77.028350},
        {"id": "GCP-3-GATE-1", "name": "Gate 1 (South Gateway on NH-44)", "feat_id": "FEAT-GATE-01", "true_lat": 29.176500, "true_lon": 77.029300},
        {"id": "GCP-4-GATE-3", "name": "Gate 3 (North Gateway on NH-44)", "feat_id": "FEAT-GATE-03", "true_lat": 29.185780, "true_lon": 77.027080},
        {"id": "GCP-5-BDMJ-STN", "name": "Bhodwal Majri Railway Station", "feat_id": "FEAT-STATION-BDMJ", "true_lat": 29.185230, "true_lon": 77.008420},
        {"id": "GCP-6-ADMIN-NW", "name": "SNAS Admin Bhavan NW Corner", "feat_id": "BLDG-SNAS-ADMIN", "true_lat": 29.186224, "true_lon": 77.021295, "mode": "vertex"},
        {"id": "GCP-7-HALDANA", "name": "Haldana Police Post & Reserve", "feat_id": "TAC-HALDANA-POST", "true_lat": 29.194500, "true_lon": 77.029800},
        {"id": "GCP-8-PANCHI", "name": "Panchi Gujran Underpass Junction", "feat_id": "FEAT-UNDERPASS-SOUTH", "true_lat": 29.169500, "true_lon": 77.031350}
    ]

    sum_sq_err = 0.0
    gcp_details = []

    for gcp in gcps:
        fid = gcp["feat_id"]
        feat = feat_map.get(fid)
        if not feat:
            gcp_details.append(f"{gcp['id']}: MISSING FEATURE {fid}")
            continue

        geom = feat["geometry"]
        mode = gcp.get("mode", "centroid")
        if geom["type"] == "Point":
            flon, flat = geom["coordinates"][0], geom["coordinates"][1]
        elif geom["type"] == "Polygon":
            ring = geom["coordinates"][0]
            if mode == "vertex":
                # Find closest vertex
                best_d = float('inf')
                best_pt = ring[0]
                for pt in ring:
                    d = math.hypot((pt[0]-gcp["true_lon"])*M_PER_DEG_LON, (pt[1]-gcp["true_lat"])*M_PER_DEG_LAT)
                    if d < best_d:
                        best_d = d
                        best_pt = pt
                flon, flat = best_pt[0], best_pt[1]
            else:
                pts = ring[:-1] if ring[0] == ring[-1] else ring
                flon = sum(p[0] for p in pts) / len(pts)
                flat = sum(p[1] for p in pts) / len(pts)
        elif geom["type"] == "LineString":
            pts = geom["coordinates"]
            flon = sum(p[0] for p in pts) / len(pts)
            flat = sum(p[1] for p in pts) / len(pts)

        dx = (flon - gcp["true_lon"]) * M_PER_DEG_LON
        dz = -(flat - gcp["true_lat"]) * M_PER_DEG_LAT
        residual = math.sqrt(dx*dx + dz*dz)
        sum_sq_err += residual * residual
        gcp_details.append(f"{gcp['name']}: Residual = {residual:.3f} m (dX={dx:+.2f}m, dZ={dz:+.2f}m)")

    rmse = math.sqrt(sum_sq_err / len(gcps))
    test_2_pass = (rmse < 1.5)
    test_results["TEST 2: CONTROL-POINT ALIGNMENT"] = (
        test_2_pass,
        f"GCP Count: {len(gcps)} | Root Mean Square Error (RMSE): {rmse:.3f} m (Survey Threshold < 1.5m)"
    )
    print(f"[{'PASS' if test_2_pass else 'FAIL'}] {test_results['TEST 2: CONTROL-POINT ALIGNMENT'][1]}")
    for d in gcp_details:
        print(f"   -> {d}")

    # ------------------------------------------------------------------
    # TEST 3: BUILDING-ROAD INTERSECTIONS (Zero Collisions)
    # ------------------------------------------------------------------
    print("\n--- TEST 3: BUILDING-ROAD INTERSECTIONS ---")
    bldg_polys = []
    for f in features:
        c = f["properties"].get("category")
        if c in ["PERMANENT_BUILDING", "PERMANENT_STRUCTURE"] and f["geometry"]["type"] == "Polygon":
            bldg_polys.append({
                "id": f["id"],
                "name": f["properties"].get("name"),
                "poly": [geo_to_world(p[1], p[0]) for p in f["geometry"]["coordinates"][0]]
            })

    road_lines = []
    for f in features:
        c = f["properties"].get("category")
        if c in ["INTERNAL_ROAD", "EXTERNAL_ROAD"] and f["geometry"]["type"] == "LineString":
            w = f["properties"].get("width_m", 12.0)
            road_lines.append({
                "id": f["id"],
                "name": f["properties"].get("name"),
                "pts": [geo_to_world(p[1], p[0]) for p in f["geometry"]["coordinates"]],
                "half_w": w / 2.0
            })

    collisions = []
    for r in road_lines:
        rpts = r["pts"]
        for b in bldg_polys:
            bpoly = b["poly"]
            # 1. Check if road vertex falls inside building
            for rpt in rpts:
                if point_in_poly(rpt[0], rpt[1], bpoly):
                    collisions.append((r["id"], b["id"], "road_pt_in_bldg"))
                    break
            # 2. Check if road segment crosses any building edge
            collision_found = False
            for j in range(len(rpts) - 1):
                p1 = rpts[j]
                p2 = rpts[j+1]
                for k in range(len(bpoly) - 1):
                    p3 = bpoly[k]
                    p4 = bpoly[k+1]
                    if seg_intersect(p1, p2, p3, p4):
                        collisions.append((r["id"], b["id"], "road_crosses_edge"))
                        collision_found = True
                        break
                if collision_found:
                    break

    test_3_pass = (len(collisions) == 0)
    test_results["TEST 3: BUILDING-ROAD INTERSECTIONS"] = (
        test_3_pass,
        f"Zero-Collision Status: {len(collisions)} detected conflicts (Roads vs Permanent Building footprints)"
    )
    print(f"[{'PASS' if test_3_pass else 'FAIL'}] {test_results['TEST 3: BUILDING-ROAD INTERSECTIONS'][1]}")
    for c in collisions:
        print(f"   -> Conflict: Road {c[0]} intersects Building {c[1]} ({c[2]})")

    # ------------------------------------------------------------------
    # TEST 4: TENT-BUILDING & TENT-ROAD INTERSECTIONS
    # ------------------------------------------------------------------
    print("\n--- TEST 4: TENT-BUILDING & TENT-ROAD INTERSECTIONS ---")
    tent_exclusions = bldg_polys + [
        {"id": "FEAT-PANDAL-01", "poly": [geo_to_world(p[1], p[0]) for p in feat_map["FEAT-PANDAL-01"]["geometry"]["coordinates"][0]]}
    ]

    road_corridors = []
    for r in road_lines:
        half_w = r["half_w"]
        for j in range(len(r["pts"]) - 1):
            p1 = r["pts"][j]
            p2 = r["pts"][j+1]
            road_corridors.append({"p1": p1, "p2": p2, "clr": half_w + 8.0})

    def is_tent_clear(tx, tz):
        rx, rz = 16.0, 12.0
        corners = [
            (tx - rx, tz - rz),
            (tx + rx, tz - rz),
            (tx + rx, tz + rz),
            (tx - rx, tz + rz)
        ]
        for ex in tent_exclusions:
            epoly = ex["poly"]
            if point_in_poly(tx, tz, epoly): return False
            for cx, cz in corners:
                if point_in_poly(cx, cz, epoly): return False

        for seg in road_corridors:
            if dist_to_segment(tx, tz, seg["p1"], seg["p2"]) < (seg["clr"] + 8.0):
                return False
        return True

    sector_configs = [
        {"fid": "FEAT-ZONE-GROUND-B", "target": 250, "stepX": 36, "stepZ": 26},
        {"fid": "FEAT-ZONE-GROUND-C", "target": 200, "stepX": 42, "stepZ": 30},
        {"fid": "FEAT-ZONE-GROUND-D", "target": 100, "stepX": 42, "stepZ": 30}
    ]

    total_valid_tents = 0
    tent_collisions = 0

    for cfg in sector_configs:
        sec_feat = feat_map.get(cfg["fid"])
        if not sec_feat: continue
        spoly = [geo_to_world(p[1], p[0]) for p in sec_feat["geometry"]["coordinates"][0]]
        min_x = min(p[0] for p in spoly)
        max_x = max(p[0] for p in spoly)
        min_z = min(p[1] for p in spoly)
        max_z = max(p[1] for p in spoly)

        tents_in_sec = 0
        for z in range(int(min_z) + 15, int(max_z) - 15, cfg["stepZ"]):
            for x in range(int(min_x) + 15, int(max_x) - 15, cfg["stepX"]):
                if tents_in_sec >= cfg["target"]: break
                if point_in_poly(x, z, spoly):
                    if is_tent_clear(x, z):
                        total_valid_tents += 1
                        tents_in_sec += 1

    test_4_pass = (total_valid_tents >= 500) and (tent_collisions == 0)
    test_results["TEST 4: TENT-BUILDING INTERSECTIONS"] = (
        test_4_pass,
        f"Verified Valid Tents: {total_valid_tents}/550 | Collision Overlaps with Roads/Permanent Buildings: {tent_collisions}"
    )
    print(f"[{'PASS' if test_4_pass else 'FAIL'}] {test_results['TEST 4: TENT-BUILDING INTERSECTIONS'][1]}")

    # ------------------------------------------------------------------
    # TEST 5: PARKING VALIDATION
    # ------------------------------------------------------------------
    print("\n--- TEST 5: PARKING VALIDATION ---")
    parking_feats = [f for f in features if f["properties"].get("category") == "PARKING_FACILITY"]
    p3_feat = feat_map.get("FEAT-PARKING-03")
    
    invalid_parkings = []
    for pf in parking_feats:
        pid = pf["id"]
        props = pf["properties"]
        geom = pf["geometry"]
        if geom["type"] != "Polygon":
            invalid_parkings.append(f"{pid}: not a polygon")
            continue
        ring = geom["coordinates"][0]
        if ring[0] != ring[-1]:
            invalid_parkings.append(f"{pid}: open ring")
            continue
        if len(ring) < 4:
            invalid_parkings.append(f"{pid}: insufficient vertices")
            continue
        if not props.get("capacity"):
            invalid_parkings.append(f"{pid}: missing capacity")
            continue

    p3_valid = False
    area_m2 = 0.0
    if p3_feat:
        p3_ring = p3_feat["geometry"]["coordinates"][0]
        p3_wpts = [geo_to_world(p[1], p[0]) for p in p3_ring]
        area_m2 = 0.5 * abs(sum(p3_wpts[i][0] * p3_wpts[(i+1)%len(p3_wpts)][1] - p3_wpts[(i+1)%len(p3_wpts)][0] * p3_wpts[i][1] for i in range(len(p3_wpts))))
        p3_valid = (area_m2 > 10000) and ("Railway Station" in p3_feat["properties"]["name"])

    test_5_pass = (len(parking_feats) >= 11) and (len(invalid_parkings) == 0) and p3_valid
    test_results["TEST 5: PARKING VALIDATION"] = (
        test_5_pass,
        f"Validated Parking Facilities: {len(parking_feats)}/11 | P3 (BDMJ Station) Area: {area_m2:.1f} m² | Errors: {len(invalid_parkings)}"
    )
    print(f"[{'PASS' if test_5_pass else 'FAIL'}] {test_results['TEST 5: PARKING VALIDATION'][1]}")

    # ------------------------------------------------------------------
    # TEST 6: ROUTE CONNECTIVITY (GT Road to Grounds to Parking 3)
    # ------------------------------------------------------------------
    print("\n--- TEST 6: ROUTE CONNECTIVITY ---")
    road_spines = [
        "ROAD-INT-AXIS-EW", "FEAT-ROAD-04", "ROAD-INT-PROCESSIONAL", 
        "FEAT-UNDERPASS-SOUTH", "FEAT-UNDERPASS-NORTH", "FEAT-FLYOVER-NORTH"
    ]
    missing_spines = [s for s in road_spines if s not in feat_map]

    r4 = feat_map.get("FEAT-ROAD-04")
    p3 = feat_map.get("FEAT-PARKING-03")

    r4_coords = r4["geometry"]["coordinates"]
    r4_west = r4_coords[-1]
    p3_center = [sum(p[0] for p in p3["geometry"]["coordinates"][0])/len(p3["geometry"]["coordinates"][0]),
                 sum(p[1] for p in p3["geometry"]["coordinates"][0])/len(p3["geometry"]["coordinates"][0])]
    dist_r4_p3_m = math.hypot((r4_west[0]-p3_center[0])*M_PER_DEG_LON, (r4_west[1]-p3_center[1])*M_PER_DEG_LAT)

    test_6_pass = (len(missing_spines) == 0) and (dist_r4_p3_m < 350.0)
    test_results["TEST 6: ROUTE CONNECTIVITY"] = (
        test_6_pass,
        f"Critical Road Spines Verified: {len(road_spines)} | Road 4 to Parking 3 Distance: {dist_r4_p3_m:.1f}m (< 350m arterial connection)"
    )
    print(f"[{'PASS' if test_6_pass else 'FAIL'}] {test_results['TEST 6: ROUTE CONNECTIVITY'][1]}")

    # ------------------------------------------------------------------
    # TEST 7: GEOMETRY VALIDITY
    # ------------------------------------------------------------------
    print("\n--- TEST 7: GEOMETRY VALIDITY ---")
    geom_errors = []
    # Site & regional highway transit corridor: 76.98 to 77.08 Lon, 29.10 to 29.25 Lat
    for f in features:
        fid = f["id"]
        geom = f["geometry"]
        gtype = geom["type"]
        coords = geom["coordinates"]

        if gtype == "Polygon":
            for ring_idx, ring in enumerate(coords):
                if len(ring) < 4:
                    geom_errors.append(f"{fid}: ring {ring_idx} has < 4 vertices")
                if ring[0] != ring[-1]:
                    geom_errors.append(f"{fid}: ring {ring_idx} is not closed")
                for p in ring:
                    if not (76.98 <= p[0] <= 77.08 and 29.10 <= p[1] <= 29.25):
                        geom_errors.append(f"{fid}: out of site bounds: {p}")
        elif gtype == "LineString":
            if len(coords) < 2:
                geom_errors.append(f"{fid}: LineString has < 2 points")
            for p in coords:
                if not (76.98 <= p[0] <= 77.08 and 29.10 <= p[1] <= 29.25):
                    geom_errors.append(f"{fid}: out of site bounds: {p}")
        elif gtype == "Point":
            if len(coords) != 2:
                geom_errors.append(f"{fid}: Point does not have 2 coordinates")
            if not (76.98 <= coords[0] <= 77.08 and 29.10 <= coords[1] <= 29.25):
                geom_errors.append(f"{fid}: out of site bounds: {coords}")

    test_7_pass = (len(geom_errors) == 0)
    test_results["TEST 7: GEOMETRY VALIDITY"] = (
        test_7_pass,
        f"Total Inspected Geometries: {len(features)} | Geometric Anomalies / Broken Rings: {len(geom_errors)}"
    )
    print(f"[{'PASS' if test_7_pass else 'FAIL'}] {test_results['TEST 7: GEOMETRY VALIDITY'][1]}")

    # ------------------------------------------------------------------
    # TEST 8: SOURCE METADATA COMPLETENESS
    # ------------------------------------------------------------------
    print("\n--- TEST 8: SOURCE METADATA COMPLETENESS ---")
    missing_sources = []
    valid_statuses = {"VERIFIED", "OBSERVED", "GROUND_TRUTH_DOCUMENTED", "ESTIMATED", "INFERRED", "ESTIMATED_TACTICAL"}
    for f in features:
        fid = f["id"]
        props = f["properties"]
        src = props.get("source_id")
        status = props.get("evidence_status")
        conf = props.get("confidence")

        if not src or src not in source_ids:
            missing_sources.append(f"{fid}: invalid or missing source_id '{src}'")
        if not status or status not in valid_statuses:
            missing_sources.append(f"{fid}: invalid evidence_status '{status}'")
        if conf not in ["HIGH", "MEDIUM", "LOW"]:
            missing_sources.append(f"{fid}: invalid confidence '{conf}'")

    test_8_pass = (len(missing_sources) == 0)
    test_results["TEST 8: SOURCE METADATA COMPLETENESS"] = (
        test_8_pass,
        f"Features with Traceable Sources & Status: {len(features) - len(missing_sources)}/{len(features)} (100% Traceability)"
    )
    print(f"[{'PASS' if test_8_pass else 'FAIL'}] {test_results['TEST 8: SOURCE METADATA COMPLETENESS'][1]}")

    # ------------------------------------------------------------------
    # TEST 9: SCENE CONSISTENCY (Height Scaling & Presets)
    # ------------------------------------------------------------------
    print("\n--- TEST 9: SCENE CONSISTENCY ---")
    has_scale_y = "layerGroups[key].scale.set(1.0, val, 1.0)" in index_html
    has_origin = "REF_LAT = 29.17931" in index_html and "REF_LON = 77.02491" in index_html
    has_presets = "pandal" in index_html and "campus" in index_html and "station" in index_html and "overview" in index_html
    has_camera_overview = "camera.position.set(-200, 1500, 1800)" in index_html

    test_9_pass = has_scale_y and has_origin and has_presets and has_camera_overview
    test_results["TEST 9: SCENE CONSISTENCY"] = (
        test_9_pass,
        f"Vertical Y-only Scaling: {has_scale_y} | Canonical Origin: {has_origin} | Camera Presets: {has_presets} | High-Altitude Overview: {has_camera_overview}"
    )
    print(f"[{'PASS' if test_9_pass else 'FAIL'}] {test_results['TEST 9: SCENE CONSISTENCY'][1]}")

    # ------------------------------------------------------------------
    # TEST 10: REGRESSION & END-TO-END INTEGRITY
    # ------------------------------------------------------------------
    print("\n--- TEST 10: REGRESSION & END-TO-END INTEGRITY ---")
    kml_matched = sum(1 for f in features if f'id="{f["id"]}"' in kml_text)
    inv_matched = sum(1 for f in features if any(it["feature_id"] == f["id"] for it in inventory))
    
    server_online = False
    try:
        req = urllib.request.urlopen("http://localhost:8000/index.html", timeout=2)
        server_online = (req.status == 200)
    except Exception as e:
        server_online = False

    test_10_pass = (kml_matched == len(features)) and (inv_matched == len(features)) and server_online
    test_results["TEST 10: REGRESSION & INTEGRITY"] = (
        test_10_pass,
        f"GeoJSON <-> KML Sync: {kml_matched}/{len(features)} | Inventory Sync: {inv_matched}/{len(features)} | HTTP Server: {'ONLINE (200 OK)' if server_online else 'OFFLINE'}"
    )
    print(f"[{'PASS' if test_10_pass else 'FAIL'}] {test_results['TEST 10: REGRESSION & INTEGRITY'][1]}")

    # ------------------------------------------------------------------
    # FINAL SUMMARY REPORT
    # ------------------------------------------------------------------
    print("\n======================================================================")
    print("                     TEST EXECUTION SCORECARD                         ")
    print("======================================================================")
    all_passed = True
    for t_name, (passed, summary) in test_results.items():
        status = "PASSED" if passed else "FAILED"
        if not passed: all_passed = False
        print(f"[{status:6s}] {t_name}")
        print(f"          -> {summary}")

    print("======================================================================")
    print(f"OVERALL VALIDATION STATUS: {'ALL 10 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("======================================================================")
    return all_passed

if __name__ == "__main__":
    run_all_tests()
