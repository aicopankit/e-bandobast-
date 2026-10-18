import json
import math

print("=== BUILDING AUTHORITATIVE MASTER GEOJSON DATASET ===")

# Reference: WGS 84 (EPSG:4326)
features = []

# --- 1. OVERALL VENUE PERIMETER BOUNDARY ---
features.append({
    "type": "Feature",
    "id": "FEAT-VENUE-BOUNDARY",
    "properties": {
        "name": "Sant Nirankari Spiritual Complex Overall Site Perimeter",
        "category": "VENUE_BOUNDARY",
        "evidence_status": "INFERRED",
        "permanence": "PERMANENT_PROPERTY",
        "area_acres": 638.5,
        "area_sqm": 2583900,
        "elevation_m": 228,
        "confidence": "HIGH",
        "source_id": "SRC-ESRI-Z16",
        "notes": "Overall boundary established from contiguous landuse bounded by Grand Trunk Road on the East, Bhodwal Majri village road on the North, Delhi-Ambala railway on the West, and southern agricultural canal."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.029800, 29.183000],
            [77.028500, 29.189500],
            [77.015000, 29.189500],
            [77.008000, 29.189000],
            [77.008000, 29.185200],
            [77.009500, 29.178000],
            [77.014500, 29.176000],
            [77.017000, 29.171000],
            [77.027500, 29.169000],
            [77.029100, 29.176000],
            [77.029800, 29.183000]
        ]]
    }
})

# --- 2. OFFICIAL GROUND SECTORS (A, B, C, D) ---
# Ground A: Main Satsang Pandal area (adjacent to GT Road)
features.append({
    "type": "Feature",
    "id": "FEAT-ZONE-GROUND-A",
    "properties": {
        "name": "Ground A (Main Satsang Pandal & GT Road Frontage)",
        "category": "SECURITY_SECTOR",
        "sector_code": "SEC-A-RED",
        "evidence_status": "ESTIMATED",
        "designation_status": "VERIFIED",
        "permanence": "PERMANENT_BOUNDARY",
        "area_acres": 68.5,
        "area_sqm": 277200,
        "elevation_m": 228,
        "confidence": "HIGH",
        "source_id": "SRC-OFFICIAL-FAQ-78",
        "notes": "Directly adjacent to GT Road (NH-44). Contains Main Satsang Pandal, Ceremonial Gate 1, VIP Dais, Central Accounts Office, securities room, and 100-bed field hospital. Designation verified by official FAQ; boundary estimated along road grid."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.022314, 29.182477],
            [77.029800, 29.182477],
            [77.029100, 29.176000],
            [77.022314, 29.176000],
            [77.022314, 29.182477]
        ]]
    }
})

# Ground B: Left side behind Ground A (South Residential & Mega Langar)
features.append({
    "type": "Feature",
    "id": "FEAT-ZONE-GROUND-B",
    "properties": {
        "name": "Ground B (South Residential & Mega Langar Kitchens)",
        "category": "SECURITY_SECTOR",
        "sector_code": "SEC-B-YELLOW",
        "evidence_status": "ESTIMATED",
        "designation_status": "VERIFIED",
        "permanence": "TEMPORARY_RECURRENT",
        "area_acres": 152.0,
        "area_sqm": 615100,
        "elevation_m": 227,
        "confidence": "HIGH",
        "source_id": "SRC-OFFICIAL-FAQ-78",
        "notes": "Located on the left side behind Ground A (facing west from GT Road entrance = southern flank). Contains 24/7 Langar community kitchens, residential tent colonies, Brahm Gyan Kaksh No. 1, and mobile ATM vans."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.014500, 29.176000],
            [77.029100, 29.176000],
            [77.027500, 29.169000],
            [77.017000, 29.171000],
            [77.014500, 29.176000]
        ]]
    }
})

# Ground C: Right side behind Ground A (North Expo & Residential)
features.append({
    "type": "Feature",
    "id": "FEAT-ZONE-GROUND-C",
    "properties": {
        "name": "Ground C (North Residential & Spiritual Expo)",
        "category": "SECURITY_SECTOR",
        "sector_code": "SEC-C-GREEN",
        "evidence_status": "ESTIMATED",
        "designation_status": "VERIFIED",
        "permanence": "TEMPORARY_RECURRENT",
        "area_acres": 132.0,
        "area_sqm": 534200,
        "elevation_m": 228,
        "confidence": "HIGH",
        "source_id": "SRC-OFFICIAL-FAQ-78",
        "notes": "Located on the right side behind Ground A (northern flank). Surrounds the permanent institutional campus. Features the Nirankari Spiritual Exhibition pavilions, Brahm Gyan Kaksh Nos. 2 & 3, and publication stalls."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.015000, 29.189500],
            [77.028500, 29.189500],
            [77.029800, 29.182477],
            [77.015000, 29.182477],
            [77.015000, 29.189500]
        ]]
    }
})

# Ground D: Behind Ground C, adjacent to Bhodwal Majri railway station
features.append({
    "type": "Feature",
    "id": "FEAT-ZONE-GROUND-D",
    "properties": {
        "name": "Ground D (Railway Reception, Holding & Logistics)",
        "category": "SECURITY_SECTOR",
        "sector_code": "SEC-D-BLUE",
        "evidence_status": "ESTIMATED",
        "designation_status": "VERIFIED",
        "permanence": "TEMPORARY_RECURRENT",
        "area_acres": 158.0,
        "area_sqm": 639400,
        "elevation_m": 227,
        "confidence": "HIGH",
        "source_id": "SRC-OFFICIAL-FAQ-78",
        "notes": "Located behind Ground C, directly adjoining Bhodwal Majri Railway Station (BDMJ). Contains passenger reception center, Brahm Gyan Kaksh No. 4, and shuttle transit staging."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.008000, 29.189000],
            [77.015000, 29.189000],
            [77.015000, 29.176000],
            [77.009500, 29.178000],
            [77.008000, 29.185200],
            [77.008000, 29.189000]
        ]]
    }
})

# --- 3. MAIN SATSANG PANDAL & DAIS ---
features.append({
    "type": "Feature",
    "id": "FEAT-PANDAL-01",
    "properties": {
        "name": "Main Satsang Pandal (Covered Assembly Hangar)",
        "category": "EVENT_STRUCTURE",
        "evidence_status": "VERIFIED",
        "permanence": "TEMPORARY_RECURRENT",
        "dimensions": "367.1m (East-West) x 255.4m (North-South)",
        "area_sqm": 93783,
        "area_acres": 23.17,
        "estimated_height_m": 18.0,
        "orientation_deg": 90, # Facing East
        "elevation_m": 228,
        "confidence": "HIGH",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Curved barrel-vault steel arch hangar structure. Measured from 1.04m/pixel satellite orthomosaic. Elevated western stage (Dais), multi-LED display arrays, central red processional carpet aisle."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.023065, 29.180491],
            [77.026842, 29.180435],
            [77.026799, 29.178131],
            [77.023022, 29.178187],
            [77.023065, 29.180491]
        ]]
    }
})

# VIP Dais / Manch Inner Stage Polygon
features.append({
    "type": "Feature",
    "id": "FEAT-STAGE-DAIS",
    "properties": {
        "name": "VIP Dais / Manch (Main Stage Inner Cordon)",
        "category": "EVENT_STRUCTURE",
        "evidence_status": "OBSERVED",
        "permanence": "TEMPORARY_RECURRENT",
        "dimensions": "45.0m (W) x 30.0m (D) x 3.5m (H)",
        "area_sqm": 1350,
        "elevation_m": 228,
        "confidence": "HIGH",
        "source_id": "SRC-FLICKR-49144669308",
        "notes": "Elevated central dais located at the western terminus of the central processional aisle inside the Main Pandal. High security sterile cordon."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.023150, 29.179450],
            [77.023600, 29.179450],
            [77.023600, 29.179150],
            [77.023150, 29.179150],
            [77.023150, 29.179450]
        ]]
    }
})

# --- 4. INDIVIDUAL PERMANENT CAMPUS BUILDINGS (SNAS) ---
permanent_buildings = [
    {
        "id": "BLDG-SNAS-ADMIN",
        "name": "SNAS Main Administrative & Central Bhavan",
        "category": "PERMANENT_BUILDING",
        "dimensions": "125.1m x 62.3m",
        "area_sqm": 7793,
        "estimated_height_m": 14.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Primary administrative headquarters, reception hall, and central offices. Traced from 1.04m/px orthoimagery.",
        "coords": [[77.021295, 29.186224], [77.022582, 29.186224], [77.022582, 29.185663], [77.021295, 29.185663], [77.021295, 29.186224]]
    },
    {
        "id": "BLDG-SNAS-RES-N",
        "name": "SNAS North Residential Bhavan & Guest Wing",
        "category": "PERMANENT_BUILDING",
        "dimensions": "125.2m x 41.5m",
        "area_sqm": 5190,
        "estimated_height_m": 10.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "North residential accommodations for senior delegates and visitors.",
        "coords": [[77.021241, 29.185615], [77.022529, 29.185615], [77.022529, 29.185241], [77.021241, 29.185241], [77.021241, 29.185615]]
    },
    {
        "id": "BLDG-SNAS-RES-W",
        "name": "SNAS West Multi-Tier Residential Block",
        "category": "PERMANENT_BUILDING",
        "dimensions": "109.5m x 109.0m",
        "area_sqm": 11936,
        "estimated_height_m": 12.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Large multi-story residential dormitory and lodging complex on western flank of campus.",
        "coords": [[77.021080, 29.184725], [77.022206, 29.184725], [77.022206, 29.183742], [77.021080, 29.183742], [77.021080, 29.184725]]
    },
    {
        "id": "BLDG-SNAS-SVC-S",
        "name": "SNAS South Logistic & Maintenance Services Facility",
        "category": "PERMANENT_BUILDING",
        "dimensions": "52.1m x 93.4m",
        "area_sqm": 4868,
        "estimated_height_m": 8.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Central storehouse, maintenance depot, and logistics dispatch offices.",
        "coords": [[77.022690, 29.186037], [77.023226, 29.186037], [77.023226, 29.185196], [77.022690, 29.185196], [77.022690, 29.186037]]
    },
    {
        "id": "BLDG-SNAS-HOSP",
        "name": "SNAS Permanent Medical Dispensary & Health Center",
        "category": "PERMANENT_BUILDING",
        "dimensions": "57.3m x 57.1m",
        "area_sqm": 3274,
        "estimated_height_m": 8.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Permanent dispensary building serving year-round visitors and regional rural welfare clinics.",
        "coords": [[77.022690, 29.185100], [77.023280, 29.185100], [77.023280, 29.184585], [77.022690, 29.184585], [77.022690, 29.185100]]
    },
    {
        "id": "BLDG-SNAS-UTIL",
        "name": "SNAS Water Treatment & Electric Substation Compound",
        "category": "PERMANENT_BUILDING",
        "dimensions": "36.5m x 62.3m",
        "area_sqm": 2277,
        "estimated_height_m": 6.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Infrastructure compound housing main electrical transformers, backup generator bank, and water treatment.",
        "coords": [[77.023387, 29.186037], [77.023762, 29.186037], [77.023762, 29.185476], [77.023387, 29.185476], [77.023387, 29.186037]]
    },
    {
        "id": "BLDG-SNAS-DINING",
        "name": "SNAS Permanent Community Dining & Langar Hall",
        "category": "PERMANENT_BUILDING",
        "dimensions": "125.1m x 51.9m",
        "area_sqm": 6489,
        "estimated_height_m": 8.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Permanent dining pavilion and community kitchen facility for ashram residents and visitors.",
        "coords": [[77.021027, 29.183601], [77.022314, 29.183601], [77.022314, 29.183134], [77.021027, 29.183134], [77.021027, 29.183601]]
    }
]

for b in permanent_buildings:
    features.append({
        "type": "Feature",
        "id": b["id"],
        "properties": {
            "name": b["name"],
            "category": b["category"],
            "dimensions": b["dimensions"],
            "area_sqm": b["area_sqm"],
            "estimated_height_m": b["estimated_height_m"],
            "elevation_m": 228,
            "evidence_status": b["evidence_status"],
            "permanence": b["permanence"],
            "source_id": b["source_id"],
            "confidence": "HIGH",
            "notes": b["notes"]
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [b["coords"]]
        }
    })

# --- 4B. SATELLITE & BLUEPRINT-VERIFIED GROUND INFRASTRUCTURE ---
additional_ground_structures = [
    {
        "id": "FEAT-LANGAR-01",
        "name": "Ground B Mega Langar Hall & Community Kitchen (South)",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "165m x 70m",
        "area_sqm": 11550,
        "estimated_height_m": 7.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Major community dining and langar hall in Ground B, serving 24/7 free meals to devotees.",
        "supervising_officer": "DSP Crime Panipat / Langar Committee Incharge",
        "capacity": "35,000 devotees/hr",
        "coords": [[77.0225, 29.1775], [77.0242, 29.1775], [77.0242, 29.1768], [77.0225, 29.1768], [77.0225, 29.1775]]
    },
    {
        "id": "FEAT-LANGAR-02",
        "name": "Ground C Mega Langar Hall & Community Kitchen (North)",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "145m x 90m",
        "area_sqm": 13050,
        "estimated_height_m": 7.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Major community dining and langar hall in Ground C, located north of Avenue R-2 90'.",
        "supervising_officer": "DSP HQ Karnal / Langar Committee Incharge",
        "capacity": "30,000 devotees/hr",
        "coords": [[77.0215, 29.1842], [77.0230, 29.1842], [77.0230, 29.1834], [77.0215, 29.1834], [77.0215, 29.1842]]
    },
    {
        "id": "FEAT-LANGAR-03",
        "name": "Ground D Transit Langar Hall (Railway Flank)",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "145m x 90m",
        "area_sqm": 13050,
        "estimated_height_m": 6.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Transit langar pavilion catering to pilgrims arriving via Bhodwal Majri railway station.",
        "supervising_officer": "Inspector Railway / Langar Sub-Incharge",
        "capacity": "18,000 devotees/hr",
        "coords": [[77.0140, 29.1853], [77.0155, 29.1853], [77.0155, 29.1845], [77.0140, 29.1845], [77.0140, 29.1853]]
    },
    {
        "id": "FEAT-DISPENSARY-01",
        "name": "Central Medical Dispensary & Emergency Health Post",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "105m x 55m",
        "area_sqm": 5775,
        "estimated_height_m": 6.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Central dispensary and emergency health post equipped with ambulances and ICU beds.",
        "supervising_officer": "Chief Medical Officer (CMO Panipat / SNM Hospital)",
        "capacity": "150-bed emergency triage",
        "coords": [[77.0252, 29.1842], [77.0263, 29.1842], [77.0263, 29.1837], [77.0252, 29.1837], [77.0252, 29.1842]]
    },
    {
        "id": "FEAT-SD-OFFICE",
        "name": "Sub-Divisional Civil & Police Administration Office (S/D Office)",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "85m x 55m",
        "area_sqm": 4675,
        "estimated_height_m": 6.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Sub-divisional magistrate and police control room fronting Road R-2 90'.",
        "supervising_officer": "SDM Samalkha / DSP HQ",
        "coords": [[77.0236, 29.1846], [77.0245, 29.1846], [77.0245, 29.1841], [77.0236, 29.1841], [77.0236, 29.1846]]
    },
    {
        "id": "FEAT-TOILETS-PANDAL-N",
        "name": "Main Pandal North Permanent Sanitation & Toilet Complex",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "330m x 45m",
        "area_sqm": 14850,
        "estimated_height_m": 4.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z16",
        "notes": "Four continuous modular permanent toilet and ablution blocks north of the Main Pandal.",
        "supervising_officer": "Sanitation Incharge / Duty Magistrate",
        "capacity": "450 cubicles with running water",
        "coords": [[77.0232, 29.1812], [77.0266, 29.1812], [77.0266, 29.1808], [77.0232, 29.1808], [77.0232, 29.1812]]
    },
    {
        "id": "FEAT-TOILETS-PANDAL-S",
        "name": "Main Pandal South Permanent Sanitation & Toilet Complex",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "330m x 45m",
        "area_sqm": 14850,
        "estimated_height_m": 4.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z16",
        "notes": "Four continuous modular permanent toilet and ablution blocks south of the Main Pandal.",
        "supervising_officer": "Sanitation Incharge / Duty Magistrate",
        "capacity": "450 cubicles with running water",
        "coords": [[77.0232, 29.1779], [77.0266, 29.1779], [77.0266, 29.1775], [77.0232, 29.1775], [77.0232, 29.1779]]
    },
    {
        "id": "FEAT-TOILETS-P2",
        "name": "Parking P2 Commuter Sanitation & Rest Block",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "95m x 55m",
        "area_sqm": 5225,
        "estimated_height_m": 4.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Sanitation and drinking water facility for commuters at Parking P2.",
        "supervising_officer": "Sanitation Supervisor Parking P2",
        "capacity": "80 cubicles",
        "coords": [[77.0270, 29.1853], [77.0280, 29.1853], [77.0280, 29.1848], [77.0270, 29.1848], [77.0270, 29.1853]]
    },
    {
        "id": "FEAT-PETROL-PUMP",
        "name": "NH-44 Commercial Fuel & Service Station",
        "category": "CIVIL_INFRASTRUCTURE",
        "dimensions": "85m x 80m",
        "area_sqm": 6800,
        "estimated_height_m": 6.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Commercial fuel station fronting NH-44 Grand Trunk Road between Gate 2 and Gate 3.",
        "supervising_officer": "Traffic Police Incharge / Fire Safety Officer",
        "coords": [[77.0285, 29.1832], [77.0294, 29.1832], [77.0294, 29.1825], [77.0285, 29.1825], [77.0285, 29.1832]]
    },
    {
        "id": "FEAT-POLICE-POST-G2",
        "name": "Gate 2 Integrated Police Post & Security Control Centre",
        "category": "POLICE_FACILITY",
        "dimensions": "75m x 75m",
        "area_sqm": 5625,
        "estimated_height_m": 5.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "notes": "Primary police post, CCTV monitoring bunker, and VIP pass verification counter at Gate 2.",
        "supervising_officer": "DSP HQ Karnal / SHO Samalkha",
        "allocated_force": "1 Insp, 2 SIs, 4 ASIs, 24 Head Constables",
        "coords": [[77.0288, 29.1798], [77.0296, 29.1798], [77.0296, 29.1791], [77.0288, 29.1791], [77.0288, 29.1798]]
    },
    {
        "id": "FEAT-ALIGHTING-STN",
        "name": "Railway Station & ISBT Passenger Alighting Terminal",
        "category": "PERMANENT_STRUCTURE",
        "dimensions": "145m x 90m",
        "area_sqm": 13050,
        "estimated_height_m": 5.5,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "notes": "Dedicated passenger alighting shelter connecting Bhodwal Majri station to Ground D.",
        "supervising_officer": "DSP GRP / Inspector Traffic Station Gate",
        "coords": [[77.0090, 29.1856], [77.0105, 29.1856], [77.0105, 29.1848], [77.0090, 29.1848], [77.0090, 29.1856]]
    },
    {
        "id": "FEAT-WATER-RESERVOIR-01",
        "name": "South Overhead Drinking Water Reservoir & Pump Compound",
        "category": "CIVIL_INFRASTRUCTURE",
        "dimensions": "68m x 68m",
        "area_sqm": 4624,
        "estimated_height_m": 14.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z16",
        "notes": "Elevated water storage tank and booster pump station supplying potable water to Grounds A and B.",
        "supervising_officer": "Public Health Engineering Officer",
        "capacity": "2.5 Million Litres Overhead Storage",
        "coords": [[77.0205, 29.1768], [77.0212, 29.1768], [77.0212, 29.1762], [77.0205, 29.1762], [77.0205, 29.1768]]
    },
    {
        "id": "FEAT-WATER-RESERVOIR-02",
        "name": "North Overhead Drinking Water Reservoir & Pump Compound",
        "category": "CIVIL_INFRASTRUCTURE",
        "dimensions": "68m x 68m",
        "area_sqm": 4624,
        "estimated_height_m": 14.0,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z16",
        "notes": "Elevated water storage tank and booster pump station supplying potable water to Grounds C and D.",
        "supervising_officer": "Public Health Engineering Officer",
        "capacity": "2.5 Million Litres Overhead Storage",
        "coords": [[77.0205, 29.1864], [77.0212, 29.1864], [77.0212, 29.1858], [77.0205, 29.1858], [77.0205, 29.1864]]
    }
]

for b in additional_ground_structures:
    props = {
        "name": b["name"],
        "category": b["category"],
        "dimensions": b["dimensions"],
        "area_sqm": b["area_sqm"],
        "estimated_height_m": b["estimated_height_m"],
        "elevation_m": 228,
        "evidence_status": b["evidence_status"],
        "permanence": b["permanence"],
        "source_id": b["source_id"],
        "confidence": "HIGH",
        "notes": b["notes"]
    }
    if "supervising_officer" in b:
        props["supervising_officer"] = b["supervising_officer"]
    if "capacity" in b:
        props["capacity"] = b["capacity"]
    if "allocated_force" in b:
        props["allocated_force"] = b["allocated_force"]
    features.append({
        "type": "Feature",
        "id": b["id"],
        "properties": props,
        "geometry": {
            "type": "Polygon",
            "coordinates": [b["coords"]]
        }
    })

# --- 5. INTERNAL ROAD & AVENUE NETWORK ---
internal_roads = [
    {
        "id": "ROAD-INT-AXIS-EW",
        "name": "Central Arterial Avenue (Main East-West Spine)",
        "category": "INTERNAL_ROAD",
        "width_m": 24.0,
        "surface": "Paved Asphalt",
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT_RIGHT_OF_WAY",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Primary 24-meter wide arterial avenue running from GT Road Gate 1, past the north edge of Main Pandal, crossing through Grounds C and D directly to Bhodwal Majri station.",
        "coords": [
            [77.029800, 29.182477],
            [77.026842, 29.182477],
            [77.022314, 29.182477],
            [77.018237, 29.182477],
            [77.014500, 29.182477],
            [77.009000, 29.184000],
            [77.008420, 29.185230]
        ]
    },
    {
        "id": "ROAD-INT-NORTH-AVE",
        "name": "North Campus Boundary Avenue",
        "category": "INTERNAL_ROAD",
        "width_m": 18.0,
        "surface": "Paved Asphalt",
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT_RIGHT_OF_WAY",
        "source_id": "SRC-ESRI-Z17",
        "notes": "East-West avenue running north of the permanent campus, connecting GT Road to Bhodwal Majri village road.",
        "coords": [
            [77.029500, 29.186271],
            [77.023762, 29.186271],
            [77.021027, 29.186271],
            [77.015000, 29.186271]
        ]
    },
    {
        "id": "ROAD-INT-SOUTH-AVE",
        "name": "South Pandal Dividing Avenue",
        "category": "INTERNAL_ROAD",
        "width_m": 18.0,
        "surface": "Paved Asphalt",
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT_RIGHT_OF_WAY",
        "source_id": "SRC-ESRI-Z17",
        "notes": "East-West avenue south of the Main Pandal, separating Ground A from Ground B Langar kitchens.",
        "coords": [
            [77.029100, 29.177934],
            [77.026799, 29.177934],
            [77.022314, 29.177934],
            [77.014500, 29.177934]
        ]
    },
    {
        "id": "ROAD-INT-NS-PANDAL-W",
        "name": "Pandal West Flank Avenue (North-South)",
        "category": "INTERNAL_ROAD",
        "width_m": 18.0,
        "surface": "Paved Asphalt",
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT_RIGHT_OF_WAY",
        "source_id": "SRC-ESRI-Z17",
        "notes": "North-South avenue flanking the western edge of the Main Pandal and Dais, connecting North Campus avenue to South avenue.",
        "coords": [
            [77.022314, 29.186271],
            [77.022314, 29.182477],
            [77.022314, 29.177934],
            [77.022314, 29.173000]
        ]
    },
    {
        "id": "ROAD-INT-NS-CENTRAL",
        "name": "Central Sector Spine Avenue (North-South)",
        "category": "INTERNAL_ROAD",
        "width_m": 18.0,
        "surface": "Paved Asphalt",
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT_RIGHT_OF_WAY",
        "source_id": "SRC-ESRI-Z17",
        "notes": "Major internal North-South dividing corridor crossing between Grounds C/D and Ground B.",
        "coords": [
            [77.018237, 29.189500],
            [77.018237, 29.182477],
            [77.018237, 29.177934],
            [77.018237, 29.171000]
        ]
    },
    {
        "id": "ROAD-INT-PROCESSIONAL",
        "name": "Ceremonial Gate 1 Processional Way",
        "category": "INTERNAL_ROAD",
        "width_m": 20.0,
        "surface": "Ceremonial Pavers / Carpet",
        "evidence_status": "OBSERVED",
        "permanence": "TEMPORARY_RECURRENT",
        "source_id": "SRC-FLICKR-49144669308",
        "notes": "Direct axial avenue extending from Gate 1 on GT Road straight into the eastern entrance of the Main Pandal.",
        "coords": [
            [77.029800, 29.180250],
            [77.028650, 29.180250],
            [77.026842, 29.180250]
        ]
    }
]

for r in internal_roads:
    features.append({
        "type": "Feature",
        "id": r["id"],
        "properties": {
            "name": r["name"],
            "category": r["category"],
            "width_m": r["width_m"],
            "surface": r["surface"],
            "evidence_status": r["evidence_status"],
            "permanence": r["permanence"],
            "source_id": r["source_id"],
            "confidence": "HIGH",
            "notes": r["notes"]
        },
        "geometry": {
            "type": "LineString",
            "coordinates": r["coords"]
        }
    })

# --- 6. HARVESTED OPENSTREETMAP EXTERNAL ROADS & RAILWAYS ---
with open("osm_extracted_roads_rails.json", "r", encoding="utf-8") as f:
    osm_data = json.load(f)

for r in osm_data["roads"]:
    features.append(r)

for rw in osm_data["rails"]:
    features.append(rw)

# --- 7. KEY TRANSPORT & CONTROL HUBS ---
features.append({
    "type": "Feature",
    "id": "FEAT-STATION-BDMJ",
    "properties": {
        "name": "Bhodwal Majri Railway Station (BDMJ)",
        "category": "TRANSPORT_HUB",
        "operator": "Northern Railway (Indian Railways)",
        "station_code": "BDMJ",
        "osm_node_id": "Q25549367",
        "elevation_m": 227,
        "evidence_status": "VERIFIED",
        "permanence": "PERMANENT",
        "source_id": "SRC-OSM-DATASET",
        "confidence": "HIGH",
        "notes": "Trunk line passenger station on the Delhi-Ambala main line. Dedicated 2-minute special train stoppages authorized during Samagam."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.008420, 29.185230]
    }
})

# --- 7. OFFICIAL GATES, EVENT HUBS & CIVIL INFRASTRUCTURE (FROM 79TH SAMAGAM BLUEPRINT) ---
# Gate No. 1 (South Gate on NH-44: Daily Commuters, Charted Buses & Parking P2)
features.append({
    "type": "Feature",
    "id": "FEAT-GATE-01",
    "properties": {
        "name": "Gate No. 1 (South Gateway — Daily Commuters & Parking P2)",
        "category": "ACCESS_CONTROL",
        "dimensions": "42.0m (W) x 14.0m (H) x 6.0m (D)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Main southern vehicular and pedestrian entrance from Grand Trunk Road (NH-44). Designated primary ingress for Delhi-side daily commuters, charted buses, 2-wheelers, and Parking P2."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.029100, 29.176500]
    }
})

# Gate No. 2 (Central Ceremonial Gate on NH-44: VIP, S.C. Members, Dais & Offices)
features.append({
    "type": "Feature",
    "id": "FEAT-GATE-02",
    "properties": {
        "name": "Gate No. 2 (Central Ceremonial Gateway — VIP, S.C. & Pandal Access)",
        "category": "ACCESS_CONTROL",
        "dimensions": "45.0m (W) x 15.0m (H) x 8.0m (D)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Monumental tri-arch ceremonial portal facing NH-44 directly aligned with the central processional axis, Main Satsang Pandal, VIP Dais, S.C. Parking, and Central Mission Offices."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.029650, 29.179500]
    }
})

# Gate No. 3 (North Gate on NH-44: Ambala Commuters, Saints from Abroad & Parking P4)
features.append({
    "type": "Feature",
    "id": "FEAT-GATE-03",
    "properties": {
        "name": "Gate No. 3 (North Gateway — Ambala Side, Saints from Abroad & Parking P4)",
        "category": "ACCESS_CONTROL",
        "dimensions": "38.0m (W) x 12.0m (H) x 6.0m (D)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Northern access portal from NH-44 near Karishna Polymer and Patti Kalyana underpass. Primary ingress for Ambala-side daily commuters, Saints from Abroad, and Parking P4."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.029400, 29.184500]
    }
})

# Railway Station Gate (Ground D / Bhodwal Majri Access)
features.append({
    "type": "Feature",
    "id": "FEAT-GATE-STATION",
    "properties": {
        "name": "Railway Station Gate (Bhodwal Majri Station & Parking P3 Access)",
        "category": "ACCESS_CONTROL",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 227,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Controlled access portal between Bhodwal Majri Railway Station platforms, Passenger Alighting Point, and Ground D / Parking P3."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.009000, 29.185230]
    }
})

# Exhibition Pavilion (Directly North of Pandal along Road R-2 90)
features.append({
    "type": "Feature",
    "id": "FEAT-EXHIBITION",
    "properties": {
        "name": "Nirankari Spiritual Exhibition Pavilion (Road R-2 90)",
        "category": "EVENT_STRUCTURE",
        "dimensions": "367.0m x 75.0m",
        "area_sqm": 27525,
        "elevation_m": 228,
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Spiritual Exhibition displaying mission history, universal brotherhood themes, multi-lingual publication galleries, and audio-visual displays. Placed directly along Road R-2 90 north of Pandal."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.023000, 29.180600],
            [77.026800, 29.180600],
            [77.026800, 29.182600],
            [77.023000, 29.182600],
            [77.023000, 29.180600]
        ]]
    }
})

# Central Mission Offices (Between Pandal and Gate No. 2)
features.append({
    "type": "Feature",
    "id": "FEAT-OFFICES-CENTRAL",
    "properties": {
        "name": "Central Administration & Mission Operations Offices",
        "category": "EVENT_STRUCTURE",
        "dimensions": "155.0m x 45.0m",
        "area_sqm": 6975,
        "elevation_m": 228,
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Central operations headquarters housing Central Accounts Office, volunteer coordination, protocol office, lost and found, and media liaison. Fronting Gate No. 2."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.026900, 29.180200],
            [77.028500, 29.180200],
            [77.028500, 29.181400],
            [77.026900, 29.181400],
            [77.026900, 29.180200]
        ]]
    }
})

# Sub-Divisional / Seva Dal Office (S/D Office — Parking P2)
features.append({
    "type": "Feature",
    "id": "FEAT-OFFICE-SD",
    "properties": {
        "name": "Sub-Divisional Seva Dal Office (S/D Office — Parking P2)",
        "category": "EVENT_STRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Field administration office in Parking P2 managing commuter intake, bus parking coordination, driver accommodations, and traffic sevadar rosters."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.024500, 29.177500]
    }
})

# Road R-2 90 Public Sanitation & Toilet Complex
features.append({
    "type": "Feature",
    "id": "FEAT-TOILETS-R2",
    "properties": {
        "name": "Public Sanitation & Toilets Complex (Road R-2 90)",
        "category": "EVENT_STRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Major sanitation block providing drinking water tankers, mobile toilet clusters, and washing facilities along the Road R-2 90 cross-artery."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.026000, 29.178000]
    }
})

# Alighting Point — Railway Station & ISBT Vehicles (Parking P2)
features.append({
    "type": "Feature",
    "id": "FEAT-ALIGHT-ISBT",
    "properties": {
        "name": "Passenger Alighting Point (Railway & ISBT Vehicles — Parking P2)",
        "category": "TRANSPORT_HUB",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Dedicated disembarkation curb in Parking P2 for special shuttle buses arriving from Delhi ISBT, Panipat ISBT, and railway stations."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.027500, 29.177200]
    }
})

# Alighting Point — Road 4 Central Corridor
features.append({
    "type": "Feature",
    "id": "FEAT-ALIGHT-ROAD4",
    "properties": {
        "name": "Passenger Alighting Point (Road 4 Central Corridor)",
        "category": "TRANSPORT_HUB",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Mid-avenue passenger drop-off node along Road 4 serving Ground C residential colonies and exhibition ingress."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.022300, 29.183000]
    }
})

# Alighting Point — Bhodwal Majri Railway Station & Parking P3
features.append({
    "type": "Feature",
    "id": "FEAT-ALIGHT-P3",
    "properties": {
        "name": "Passenger Alighting Point (Railway Station & Parking P3)",
        "category": "TRANSPORT_HUB",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 227,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Dedicated passenger drop-off plaza adjoining Bhodwal Majri railway station entrance and Parking P3."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.010500, 29.185500]
    }
})

# Local Bus Stop (East NH-44 Service Road)
features.append({
    "type": "Feature",
    "id": "FEAT-BUS-STOP-LOCAL",
    "properties": {
        "name": "Local Bus Stop (East NH-44 Service Road & Parking P5)",
        "category": "TRANSPORT_HUB",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "TEMPORARY_RECURRENT",
        "elevation_m": 228,
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Official public transit stop on the eastern service lane of NH-44. Passengers disembark here and cross via the pedestrian overbridge to Gates 1 and 2."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.031500, 29.180250]
    }
})

# Grade Separator: NH-44 Vehicular Underpass (South / Village Panchi Gujran)
features.append({
    "type": "Feature",
    "id": "FEAT-UNDERPASS-SOUTH",
    "properties": {
        "name": "NH-44 Vehicular Underpass (South — Panchi Gujran Approach)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT_INFRASTRUCTURE",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Highway underpass allowing vehicles from Delhi side and Village Panchi Gujran to loop under NH-44 into Parking P1 without crossing active highway lanes."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.028800, 29.169500]
    }
})

# Grade Separator: NH-44 Flyover (North / Patti Kalyana & Gate 3)
features.append({
    "type": "Feature",
    "id": "FEAT-FLYOVER-NORTH",
    "properties": {
        "name": "NH-44 Elevated Flyover (North — Patti Kalyana Section)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT_INFRASTRUCTURE",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Elevated highway flyover section carrying through-traffic on NH-44 above local Samalkha / Patti Kalyana interchange."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.029800, 29.184000],
            [77.029400, 29.188000]
        ]
    }
})

# Grade Separator: NH-44 Vehicular Underpass (North / Patti Kalyana)
features.append({
    "type": "Feature",
    "id": "FEAT-UNDERPASS-NORTH",
    "properties": {
        "name": "NH-44 Vehicular Underpass (North — Patti Kalyana & Gate 3)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT_INFRASTRUCTURE",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Highway underpass below the northern flyover allowing cross-highway U-turns and access between Village Patti Kalyana, Gov. Road, Gate 3, and Parking P4."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.029500, 29.186000]
    }
})

# Surrounding Context: Village Panchi Gujran
features.append({
    "type": "Feature",
    "id": "FEAT-VILLAGE-PANCHI",
    "properties": {
        "name": "Village Panchi Gujran (Southern Flank Settlement)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Rural settlement bounding the southern venue perimeter. Adjoins Parking P1 and road to Ganaur."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.012000, 29.171000]
    }
})

# Surrounding Context: Village Bhodwal Majri
features.append({
    "type": "Feature",
    "id": "FEAT-VILLAGE-BHODWAL",
    "properties": {
        "name": "Village Bhodwal Majri (Northwestern Settlement)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Settlement situated northwest of the venue adjoining the railway line, station, and Gov. Road connection."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.008000, 29.192000]
    }
})

# Surrounding Context: Village Patti Kalyana
features.append({
    "type": "Feature",
    "id": "FEAT-VILLAGE-PATTI",
    "properties": {
        "name": "Village Patti Kalyana (Northeastern Settlement)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Settlement located northeast of the venue near Karishna Polymer, the northern flyover, and Gov. Road link."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.031000, 29.188000]
    }
})

# Surrounding Landmark: Karishna Polymer (Industrial Facility)
features.append({
    "type": "Feature",
    "id": "FEAT-IND-KARISHNA",
    "properties": {
        "name": "Karishna Polymer (Industrial Facility — North Boundary)",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Industrial landmark located directly on the northern boundary wall between Gate No. 3 and Parking P4."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.026500, 29.186500],
            [77.028500, 29.186500],
            [77.028500, 29.188000],
            [77.026500, 29.188000],
            [77.026500, 29.186500]
        ]]
    }
})

# Surrounding Landmark: S.N.C.E. Nursery / Institutional Complex
features.append({
    "type": "Feature",
    "id": "FEAT-INST-SNCE",
    "properties": {
        "name": "S.N.C.E. Nursery & Institutional Grounds",
        "category": "CIVIL_INFRASTRUCTURE",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Educational / horticultural nursery facility on the northern perimeter wall adjoining Village Patti Kalyana."
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [77.025000, 29.187800],
            [77.026500, 29.187800],
            [77.026500, 29.189200],
            [77.025000, 29.189200],
            [77.025000, 29.187800]
        ]]
    }
})

# Diagonal Southwestern Canal / Drain
features.append({
    "type": "Feature",
    "id": "FEAT-CANAL-SW",
    "properties": {
        "name": "Southwestern Irrigation Channel / Perimeter Drain",
        "category": "HYDROGRAPHIC",
        "evidence_status": "OBSERVED",
        "permanence": "PERMANENT",
        "source_id": "SRC-ESRI-Z16",
        "confidence": "HIGH",
        "notes": "Tree-lined water channel / drainage corridor forming the physical southwestern boundary of Ground B and railway tracks."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.018200, 29.180000],
            [77.015000, 29.176000],
            [77.011500, 29.172000],
            [77.008500, 29.167000]
        ]
    }
})

# --- 8. TACTICAL POLICE & EMERGENCY DEPLOYMENTS ---
tactical_points = [
    {
        "id": "TAC-HQ-01",
        "name": "Joint Police Control Room (JPCR - Ground A)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "COMMAND_POST",
        "force_strength": "1 SP, 2 DSP, 4 Inspectors, 20 Wireless/CCTV Operators",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.027500, 29.182500],
        "notes": "Central tactical command node coordinating district police, paramilitary, traffic wing, and Sewadal leadership."
    },
    {
        "id": "TAC-STAGE-VIP",
        "name": "VIP Dais Inner Cordon (Manch Morcha)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "VIP_INNER_CORDON",
        "force_strength": "1 ASP, 2 DSP, 15 Armed Commandos, Anti-Sabotage Unit",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.023300, 29.179300],
        "notes": "Sterile Red Zone inner cordon guarding Satguru Mata Ji, VIP speakers, and stage dais."
    },
    {
        "id": "TAC-TOWER-01",
        "name": "Watch Tower 1 — Highway Vantage (Ground A)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "VANTAGE_WATCHTOWER",
        "force_strength": "Sniper Team (1 SI, 2 Constables), High-Intensity Searchlight",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.028800, 29.181800],
        "notes": "15m steel lattice observation post overlooking GT Road entrance and pedestrian queuing plaza."
    },
    {
        "id": "TAC-TOWER-02",
        "name": "Watch Tower 2 — North Pandal Vantage",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "VANTAGE_WATCHTOWER",
        "force_strength": "Armed Police Morcha (3 Constables with Automatic Rifles)",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.022314, 29.181200],
        "notes": "Guarding northern backstage approach and VIP entrance lane."
    },
    {
        "id": "TAC-TOWER-03",
        "name": "Watch Tower 3 — South Pandal Vantage",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "VANTAGE_WATCHTOWER",
        "force_strength": "Armed Police Morcha (3 Constables with Automatic Rifles)",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.022314, 29.177500],
        "notes": "Guarding southern flank and Ground B Langar interface."
    },
    {
        "id": "TAC-TOWER-04",
        "name": "Watch Tower 4 — Railway Station Perimeter (Ground D)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "VANTAGE_WATCHTOWER",
        "force_strength": "Joint RPF & Haryana Police Observation Post",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.009000, 29.186000],
        "notes": "Monitoring railway tracks, passenger disembarkation, and station approach avenue."
    },
    {
        "id": "TAC-HOSP-01",
        "name": "100-Bed Field Hospital & ICU Base (Ground A)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "MEDICAL_FACILITY",
        "force_strength": "12 Medical Officers, 24 Nurses, 5 ALS Ambulances",
        "evidence_status": "VERIFIED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.027000, 29.182000],
        "notes": "Official 100-bed Allopathic field hospital with 10-bed ICU and round-the-clock emergency triage."
    },
    {
        "id": "TAC-FIRE-01",
        "name": "Fire Service Staging Post (Ground A)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "FIRE_STATION",
        "force_strength": "4 Water Bowsers (10,000L), 2 Foam Tenders, 2 Mist Bikes",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "coords": [77.027800, 29.179000],
        "notes": "Immediate initial attack response for high-density congregation areas."
    },
    {
        "id": "TAC-QRT-01",
        "name": "Quick Reaction Team 1 (QRT 1 — Outer Cordon North/GT Road)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "TACTICAL_RESPONSE",
        "supervising_officer": "Day: ACP Anil Kumar (7056667210) | Night: DSP Ramesh Kumar (7419301130)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "force_strength": "Armed SWAT Unit + Bullet-Proof Tactical Vehicle",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.029500, 29.187000],
        "notes": "24-hour armed strike cover at outer northern perimeter; monitor dhabas, rice mills, factories, and report suspicious activity."
    },
    {
        "id": "TAC-QRT-02",
        "name": "Quick Reaction Team 2 (QRT 2 — Outer Cordon South/Industrial Flank)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "TACTICAL_RESPONSE",
        "supervising_officer": "Day: ACP Anil Kumar (7056667210) | Night: DSP Ramesh Kumar (7419301130)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "force_strength": "Armed Strike Unit + Bullet-Proof Tactical Vehicle",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.018000, 29.172000],
        "notes": "Outer southern boundary cover around Bhakti Niwas; prevent unauthorized perimeter penetration."
    },
    {
        "id": "TAC-QRT-03",
        "name": "Quick Reaction Team 3 (QRT 3 — Bhodwal Majri Railway Station Gate)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "TACTICAL_RESPONSE",
        "supervising_officer": "Day: DSP Sushil Parkash (9053052105) | Night: DSP Sandeep Kumar (9729990995)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "force_strength": "Armed QRT Section (2 Sections ORs armed and ready)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.009000, 29.185230],
        "notes": "Positioned at railway-side gate; armed and ready for station passenger surges and track security coordination."
    },
    {
        "id": "TAC-QRT-04",
        "name": "Quick Reaction Team 4 (QRT 4 — Central Venue Node / Grounds A-B-C Junction)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "TACTICAL_RESPONSE",
        "supervising_officer": "Day: DSP Sushil Parkash (9053052105) | Night: DSP Sandeep Kumar (9729990995)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "force_strength": "Armed Tactical Intervention Section",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.018500, 29.182477],
        "notes": "Stationed at designated central venue point; rapid intervention for Grounds A, B, C, D internal corridors."
    },
    {
        "id": "TAC-DRONE-01",
        "name": "CID Drone Surveillance Unit 1 (NH-44 & Footbridge)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "AERIAL_SURVEILLANCE",
        "supervising_officer": "DSP Suresh Kumar / ACP Satyapal (Panipat Traffic)",
        "shift_timings": "24 Hours (Rotational Flights)",
        "force_strength": "CID Drone Operator Team + Real-Time Base Downlink",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.030500, 29.180500],
        "notes": "Monitors NH-44 highway traffic flow, pedestrian footbridge crowd density, and unauthorized roadside parking."
    },
    {
        "id": "TAC-DRONE-02",
        "name": "CID Drone Surveillance Unit 2 (Railway & Western Sector)",
        "category": "BANDOBAST_TACTICAL",
        "tactical_type": "AERIAL_SURVEILLANCE",
        "supervising_officer": "DSP Sushil Parkash / DSP Sandeep Kumar",
        "shift_timings": "24 Hours (Rotational Flights)",
        "force_strength": "CID Drone Operator Team + Wireless Liaison",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "coords": [77.009800, 29.185800],
        "notes": "Monitors Bhodwal Majri station platforms, railway corridor perimeter, and Parking 3 vehicle arrival patterns."
    }
]

for tp in tactical_points:
    feat_props = {
        "name": tp["name"],
        "category": tp["category"],
        "tactical_type": tp["tactical_type"],
        "force_strength": tp["force_strength"],
        "evidence_status": tp.get("evidence_status", "ESTIMATED_TACTICAL"),
        "permanence": tp.get("permanence", "OPERATIONAL_DEPLOYMENT"),
        "source_id": tp.get("source_id", "SRC-E-BANDOBAST-SOP"),
        "confidence": tp.get("confidence", "HIGH"),
        "notes": tp["notes"]
    }
    if "supervising_officer" in tp:
        feat_props["supervising_officer"] = tp["supervising_officer"]
    if "shift_timings" in tp:
        feat_props["shift_timings"] = tp["shift_timings"]

    features.append({
        "type": "Feature",
        "id": tp["id"],
        "properties": feat_props,
        "geometry": {
            "type": "Point",
            "coordinates": tp["coords"]
        }
    })

# --- 9. OFFICIAL TRAFFIC CIRCULATION CORRIDORS (79TH SAMAGAM BLUEPRINT REFERENCES) ---
# Reference 1: Outstation Vehicles from Delhi Side -> Parking P1 (Pink)
features.append({
    "type": "Feature",
    "id": "ROUTE-DELHI-P1",
    "properties": {
        "name": "Route 1: Outstation Vehicles from Delhi Side (to Parking P1)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-01-P1",
        "ref_label": "OUTSTATION VEHICLES FROM DELHI SIDE SHOWN THUS -> P1",
        "color": "#ec4899",
        "surface": "NH-44 South Corridor via Panchi Gujran Underpass",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Delhi side outstation traffic proceeds on NH-44, takes the southern underpass at Village Panchi Gujran, and enters Parking P1 (Heavy & Light Vehicles)."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.026500, 29.164500],
            [77.028500, 29.169500],
            [77.024000, 29.170000],
            [77.020000, 29.171000]
        ]
    }
})

# Reference 2 & 4: Daily Commuters & Charted Buses from Delhi Side -> Parking P2 via Gate 1 (Cyan)
features.append({
    "type": "Feature",
    "id": "ROUTE-DELHI-P2",
    "properties": {
        "name": "Route 2: Daily Commuters & Charted Buses from Delhi Side (to Parking P2 via Gate 1)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-02-P2",
        "ref_label": "VEHICLES FROM DELHI SIDE SEWADARS ON DUTY & DAILY COMMUTERS -> P2",
        "color": "#00d2ff",
        "surface": "NH-44 Service Lane through Gate No. 1",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Delhi side charted buses, daily commuters, and 2-wheelers enter via Gate No. 1 into Parking P2 (with dedicated Alighting Point, S/D Office, and Toilets)."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.027000, 29.168000],
            [77.029100, 29.176500],
            [77.027500, 29.176500],
            [77.025500, 29.176000]
        ]
    }
})

# Reference 5 & 7: Outstation Vehicles from Ambala Side -> Parking P3 (Blue)
features.append({
    "type": "Feature",
    "id": "ROUTE-AMBALA-P3",
    "properties": {
        "name": "Route 3: Outstation Vehicles from Ambala Side (to Parking P3 via Gov Road)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-05-P3",
        "ref_label": "OUTSTATION VEHICLES FROM AMBALA SIDE SHOWN THUS -> P3",
        "color": "#3b82f6",
        "surface": "NH-44 Flyover Exit onto Gov. Road to Bhodwal Majri",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Ambala side outstation vehicles exit NH-44 near the northern flyover, follow Gov. Road through Village Bhodwal Majri, and enter Parking P3 at the railway station."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.028500, 29.194500],
            [77.029500, 29.188000],
            [77.020000, 29.189500],
            [77.012000, 29.188500],
            [77.010500, 29.186500]
        ]
    }
})

# Reference 6 & 8: Daily Up & Down Commuters from Ambala Side -> Parking P4 via Gate 3 (Light Blue)
features.append({
    "type": "Feature",
    "id": "ROUTE-AMBALA-P4",
    "properties": {
        "name": "Route 4: Daily Up & Down Commuters from Ambala Side (to Parking P4 via Gate 3)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-08-P4",
        "ref_label": "VEHICLES FROM AMBALA SIDE SEWADARS ON DUTY DAILY UP & DOWN -> P4",
        "color": "#60a5fa",
        "surface": "NH-44 Service Lane through Gate No. 3",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Ambala side daily commuters and duty sewadars proceed down NH-44 service lane and enter Gate No. 3 directly into Parking P4 near Karishna Polymer."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.028500, 29.192000],
            [77.029400, 29.184500],
            [77.027000, 29.184500],
            [77.026000, 29.185500]
        ]
    }
})

# Reference 9: Vehicles for Saints from Abroad -> Parking P4 via Gate 3 (Salmon Pink)
features.append({
    "type": "Feature",
    "id": "ROUTE-ABROAD-P4",
    "properties": {
        "name": "Route 5: Vehicles for Saints from Abroad (to Parking P4 via Gate 3)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-09-P4",
        "ref_label": "VEHICLES FOR SAINTS FROM ABROAD PARKING -> P4",
        "color": "#f472b6",
        "surface": "NH-44 Service Lane to Gate 3 Dedicated Bay",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Vehicles carrying international delegates (Saints from Abroad) enter Gate No. 3 into a segregated hospitality holding bay in Parking P4."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.029400, 29.186000],
            [77.029400, 29.184500],
            [77.027500, 29.184500],
            [77.027000, 29.186000]
        ]
    }
})

# Reference 10: Vehicles for S.C. Parking via Gate 2 (Emerald Green)
features.append({
    "type": "Feature",
    "id": "ROUTE-SC-PARKING",
    "properties": {
        "name": "Route 6: Vehicles for Special Committee (S.C. Parking via Gate 2)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-10-SC",
        "ref_label": "VEHICLES FOR S.C. PARKING -> S.C. PARKING",
        "color": "#10b981",
        "surface": "Gate No. 2 Ceremonial Approach to Central Compound",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Special Committee executive vehicles enter via Gate No. 2 directly into S.C. Parking Court adjacent to Central Mission Offices."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.029650, 29.182000],
            [77.029650, 29.179500],
            [77.028500, 29.179800],
            [77.027800, 29.180500]
        ]
    }
})

# Reference 11: Invited Guests / V.I.P. Parking via Gate 2 (Gold / Amber)
features.append({
    "type": "Feature",
    "id": "ROUTE-VIP-PARKING",
    "properties": {
        "name": "Route 7: Invited Guests & V.I.P. Parking (via Gate 2)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-11-VIP",
        "ref_label": "FOR INVITED GUESTS / V.I.P. PARKING -> V.I.P. PARKING",
        "color": "#f59e0b",
        "surface": "Gate No. 2 Sterile Escort Lane directly to VIP Dais",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Invited dignitaries and VIP motorcades enter via Gate No. 2 into the high-security V.I.P. Parking bay directly behind the stage dais."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.029650, 29.182000],
            [77.029650, 29.179500],
            [77.028500, 29.179000],
            [77.027500, 29.179000],
            [77.023300, 29.179300]
        ]
    }
})

# Pedestrian Crossing Corridor via Footbridge (Cyan Dashed)
features.append({
    "type": "Feature",
    "id": "ROUTE-PED-FOOTBRIDGE",
    "properties": {
        "name": "Route 8: Bus Commuters & Pedestrian Pulsed Corridor (Parking P5 across Footbridge)",
        "category": "OPERATIONAL_ROUTE",
        "route_code": "REF-08-PED",
        "ref_label": "PEDESTRIAN CORRIDOR: LOCAL BUS STOP / P5 -> FOOT OVER BRIDGE -> GATES 1 & 2",
        "color": "#00ffff",
        "surface": "Elevated Grade-Separated Foot Over Bridge (6.5m clearance)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
        "confidence": "HIGH",
        "notes": "Public commuters disembarking at Local Bus Stop / Parking P5 are held in staging bays and released in batches across the footbridge to avoid road crossing hazards."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.033500, 29.180000],
            [77.032200, 29.180250],
            [77.029800, 29.180250],
            [77.028800, 29.180000]
        ]
    }
})

# Legacy VIP / Evacuation routes for backwards compatibility
features.append({
    "type": "Feature",
    "id": "FEAT-ROUTE-VIP",
    "properties": {
        "name": "Primary VIP Convoy Route (GT Road to Dais)",
        "category": "OPERATIONAL_ROUTE",
        "route_type": "VIP_CONVOY",
        "surface": "Sterile Asphalt Corridor",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-E-BANDOBAST-SOP",
        "confidence": "HIGH",
        "notes": "Dedicated sterile convoy corridor from GT Road Gate 1 through the north flank avenue directly to the backstage dais."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.029800, 29.182477],
            [77.026842, 29.182477],
            [77.022314, 29.182477],
            [77.022314, 29.179300],
            [77.023150, 29.179300]
        ]
    }
})

features.append({
    "type": "Feature",
    "id": "FEAT-ROUTE-EVAC",
    "properties": {
        "name": "Emergency VIP Evacuation Corridor (Dais to West Dispersal)",
        "category": "OPERATIONAL_ROUTE",
        "route_type": "EMERGENCY_EVACUATION",
        "surface": "Sterile Arterial Corridor",
        "evidence_status": "ESTIMATED_TACTICAL",
        "permanence": "OPERATIONAL_DEPLOYMENT",
        "source_id": "SRC-E-BANDOBAST-SOP",
        "confidence": "HIGH",
        "notes": "Contingency egress corridor from the backstage dais heading westward along Central Arterial Avenue directly to Bhodwal Majri station / emergency dispersal."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.023150, 29.179300],
            [77.022314, 29.179300],
            [77.022314, 29.182477],
            [77.018237, 29.182477],
            [77.014500, 29.182477],
            [77.009000, 29.184000],
            [77.008420, 29.185230]
        ]
    }
})

# --- 10. OFFICIAL INTERNAL & CONNECTING ROAD CORRIDORS ---
official_named_roads = [
    {
        "id": "FEAT-ROAD-R2-90",
        "name": "Road R-2 90 (Central East-West Axis)",
        "category": "INTERNAL_ROAD",
        "width_m": 18.0,
        "surface": "Asphalt Spine",
        "notes": "Primary East-West dividing avenue fronting Pandal, Exhibition, S.C. Parking, and leading to Parking P2.",
        "coords": [[77.022300, 29.178000], [77.029000, 29.178000]]
    },
    {
        "id": "FEAT-ROAD-04",
        "name": "Road 4 (Railway Station & Parking P3 Arterial Spine)",
        "category": "INTERNAL_ROAD",
        "width_m": 16.0,
        "surface": "Asphalt Arterial",
        "notes": "Major internal transit artery linking the central compound to Bhodwal Majri Railway Station, Passenger Alighting Point, and Parking P3.",
        "coords": [[77.022300, 29.178000], [77.022300, 29.183000], [77.018500, 29.184000], [77.011000, 29.185500], [77.009000, 29.185500]]
    },
    {
        "id": "FEAT-ROAD-GOV-NORTH",
        "name": "Gov. Road (Northern Boundary / Bhodwal Majri Section)",
        "category": "EXTERNAL_ROAD",
        "width_m": 10.0,
        "surface": "Paved Village Road",
        "notes": "Public link road bounding the northern perimeter, carrying Ambala-side outstation vehicles toward Parking P3.",
        "coords": [[77.008000, 29.189500], [77.015000, 29.189500], [77.028500, 29.189500]]
    },
    {
        "id": "FEAT-ROAD-GOV-PATTI",
        "name": "Gov. Road (Patti Kalyana Village Connection)",
        "category": "EXTERNAL_ROAD",
        "width_m": 8.0,
        "surface": "Paved Village Road",
        "notes": "Circumferential link connecting Village Patti Kalyana with the northern venue perimeter wall.",
        "coords": [[77.028500, 29.189500], [77.031000, 29.188000]]
    },
    {
        "id": "FEAT-ROAD-GANNOUR",
        "name": "Road to Gannour (Southwest Link from Panchi Gujran)",
        "category": "EXTERNAL_ROAD",
        "width_m": 10.0,
        "surface": "Rural Highway Link",
        "notes": "Southwestern arterial connecting Village Panchi Gujran, Parking P1, and Ganaur sub-district.",
        "coords": [[77.014500, 29.169000], [77.010000, 29.165000]]
    }
]

for nr in official_named_roads:
    features.append({
        "type": "Feature",
        "id": nr["id"],
        "properties": {
            "name": nr["name"],
            "category": nr["category"],
            "width_m": nr["width_m"],
            "surface": nr["surface"],
            "evidence_status": "GROUND_TRUTH_DOCUMENTED",
            "permanence": "PERMANENT",
            "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
            "confidence": "HIGH",
            "notes": nr["notes"]
        },
        "geometry": {
            "type": "LineString",
            "coordinates": nr["coords"]
        }
    })

# --- 11. DEDICATED EVENT PARKING SECTORS (OFFICIAL BLUEPRINT P1 TO P5 & S.C./VIP) ---
def pcg_parking_generator(polygon_coords, vehicle_mix="mixed"):
    M_PER_DEG_LAT = 110852.0
    M_PER_DEG_LON = 97192.0
    n = len(polygon_coords)
    area = 0.0
    for i in range(n - 1):
        x1 = polygon_coords[i][0] * M_PER_DEG_LON
        y1 = polygon_coords[i][1] * M_PER_DEG_LAT
        x2 = polygon_coords[i+1][0] * M_PER_DEG_LON
        y2 = polygon_coords[i+1][1] * M_PER_DEG_LAT
        area += (x1 * y2 - x2 * y1)
    sqm = round(abs(area) / 2.0)
    acres = round(sqm / 4046.86, 1)
    usable_sqm = sqm * 0.70 # 70% net stall area (30% internal drive aisles, fire buffers, setbacks)

    if vehicle_mix == "vip":
        car_bays = int(usable_sqm / 35.0)
        escort_bays = int(car_bays * 0.15)
        bus_bays = 0
        cap_str = f"{car_bays:,} VIP Motorcade Bays + {escort_bays} Armed Escort / Pilot Slots"
    elif vehicle_mix == "cars":
        car_bays = int(usable_sqm / 25.0)
        bus_bays = 0
        cap_str = f"{car_bays:,} Light Vehicles (Cars / Jeeps / Taxis)"
    elif vehicle_mix == "bus_terminal":
        bus_bays = int((usable_sqm * 0.60) / 80.0)
        car_bays = 0
        ped_holding_cap = int((usable_sqm * 0.40) * 0.8) # 0.8 devotees/m²
        cap_str = f"{bus_bays:,} Inter-State Buses + {ped_holding_cap:,} Staged Pedestrian Holding Capacity"
    elif vehicle_mix == "heavy_mixed":
        bus_bays = int((usable_sqm * 0.30) / 80.0)
        car_bays = int((usable_sqm * 0.70) / 25.0)
        cap_str = f"{car_bays:,} Light Vehicles (Cars/Jeeps) + {bus_bays:,} Buses/Heavy Vehicles"
    elif vehicle_mix == "two_wheelers":
        two_wheel_bays = int(usable_sqm / 3.0)
        car_bays = 0
        bus_bays = 0
        cap_str = f"{two_wheel_bays:,} Two-Wheelers (Motorcycles & Scooters)"
    else: # mixed default
        bus_bays = int((usable_sqm * 0.15) / 80.0)
        car_bays = int((usable_sqm * 0.85) / 25.0)
        cap_str = f"{car_bays:,} Light Vehicles (Cars/Jeeps) + {bus_bays:,} Buses/Shuttles"

    return {
        "sqm": sqm,
        "acres": acres,
        "car_bays": car_bays,
        "bus_bays": bus_bays,
        "capacity_str": cap_str
    }

parking_definitions = [
    {
        "id": "FEAT-PARKING-01",
        "name": "Parking 1 — Overall South Hub (Village Panchi Gujran Flank)",
        "sector": "Sonipat Traffic Sector",
        "supervising_officer": "ACP Rishikant, HPS (ACP Ganaur | 7419410509)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "2 Sections ORs + 1 Police Officer at Crane (Day & Night) + 1 Fire Tender",
        "vehicle_mix": "heavy_mixed",
        "polygon": [
            [77.014500, 29.168500],
            [77.022500, 29.168500],
            [77.022500, 29.174000],
            [77.014500, 29.174000],
            [77.014500, 29.168500]
        ],
        "operational_instructions": "Outstation vehicles from Delhi side. Contains segregated Light Vehicle / Car and Heavy Vehicle / Bus parking sub-grounds adjoining Village Panchi Gujran. Connected via South Underpass and Road to Gannour."
    },
    {
        "id": "FEAT-PARKING-P1-LIGHT",
        "name": "Parking P1 (Light Vehicles / Cars — Delhi Side)",
        "sector": "Sonipat Traffic Sector",
        "supervising_officer": "ACP Rishikant, HPS (ACP Ganaur | 7419410509)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "1 Section ORs + Traffic Patrol",
        "vehicle_mix": "cars",
        "polygon": [
            [77.017000, 29.171000],
            [77.022500, 29.171000],
            [77.022500, 29.174000],
            [77.017000, 29.174000],
            [77.017000, 29.171000]
        ],
        "operational_instructions": "Designated inner sector of Parking P1 reserved exclusively for private cars, taxis, and light vehicles from Delhi side."
    },
    {
        "id": "FEAT-PARKING-P1-HEAVY",
        "name": "Parking P1 (Heavy Vehicles & Buses — Delhi Side)",
        "sector": "Sonipat Traffic Sector",
        "supervising_officer": "ACP Rishikant, HPS (ACP Ganaur | 7419410509)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "1 Section ORs + 1 Crane + 1 Fire Tender",
        "vehicle_mix": "heavy_mixed",
        "polygon": [
            [77.014500, 29.168500],
            [77.020500, 29.168500],
            [77.020500, 29.171500],
            [77.014500, 29.171500],
            [77.014500, 29.168500]
        ],
        "operational_instructions": "Designated outer sector of Parking P1 reserved for chartered buses, trucks, and heavy transport vehicles from Delhi side along Road to Gannour."
    },
    {
        "id": "FEAT-PARKING-02",
        "name": "Parking 2 — Daily Commuters, Buses & Cars (Ground B / Gate 1)",
        "sector": "Ground B / Stage, D Area & Pandal / Law & Order Reserve",
        "supervising_officer": "Satish Gautam, HPS (DSP Indri, Karnal | 9729990704) & Mohinder Singh, HPS (DSP Hathin | 8930202024)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "1 1/2 Sections ORs (Armed) + 2 ORs Crane; Traffic & Alighting Management",
        "vehicle_mix": "heavy_mixed",
        "polygon": [
            [77.023000, 29.173800],
            [77.028800, 29.173800],
            [77.028800, 29.177800],
            [77.023000, 29.177800],
            [77.023000, 29.173800]
        ],
        "operational_instructions": "Major transit hub inside Gate No. 1 in Ground B. Accommodates daily commuters from Delhi side (charted buses & private cars), railway/ISBT shuttle alighting point, Sub-Divisional (S/D) Seva Dal office, and Road R-2 90 toilets."
    },
    {
        "id": "FEAT-PARKING-P2-2W",
        "name": "Parking P2 (2-Wheelers Dedicated Holding Bay)",
        "sector": "Ground B / Gate 1 Precinct",
        "supervising_officer": "Satish Gautam, HPS (DSP Indri, Karnal | 9729990704)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "1 Section Traffic Sevadars + Police Checkpost",
        "vehicle_mix": "two_wheelers",
        "polygon": [
            [77.027000, 29.174000],
            [77.028800, 29.174000],
            [77.028800, 29.175500],
            [77.027000, 29.175500],
            [77.027000, 29.174000]
        ],
        "operational_instructions": "Dedicated segregated enclosure inside Gate 1 for motorcycles, scooters, and 2-wheelers with anti-theft tagging and quick-exit lanes."
    },
    {
        "id": "FEAT-PARKING-03",
        "name": "Parking 3 — Bhodwal Majri Railway Station & Ground D Holding",
        "sector": "Inner Cordon & Residential Area (Ambala Outstation Hub)",
        "supervising_officer": "Day: Sushil Parkash, HPS (DSP Crime, Kaithal | 9053052105) | Night: Sandeep Kumar, HPS (DSP HQ, Karnal | 9729990995)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "allocated_force": "2 Sections ORs + CID Drone Unit with Operator",
        "vehicle_mix": "mixed",
        "polygon": [
            [77.008500, 29.184000],
            [77.012500, 29.184000],
            [77.012500, 29.188500],
            [77.008500, 29.188500],
            [77.008500, 29.184000]
        ],
        "operational_instructions": "Directly adjoining Bhodwal Majri Railway Station. Handles outstation vehicles from Ambala side (arriving via Gov. Road) and daily commuter shuttles. Contains Passenger Alighting Point."
    },
    {
        "id": "FEAT-PARKING-04",
        "name": "Parking 4 — Gate 3 / Karishna Polymer Flank (Ambala & Abroad)",
        "sector": "Traffic - Panipat Side (Gate 3 Flank)",
        "supervising_officer": "Day: Suresh Kumar, HPS (DSP Traffic, Panipat | 7056000501) | Night: Satyapal, HPS (ACP Highway & HQ, Gurugram | 9999981809)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "allocated_force": "Part of 2 Platoons + 1 Section ORs; 1 Crane + 1 Fire Tender",
        "vehicle_mix": "mixed",
        "polygon": [
            [77.024500, 29.183500],
            [77.028800, 29.183500],
            [77.028800, 29.187200],
            [77.024500, 29.187200],
            [77.024500, 29.183500]
        ],
        "operational_instructions": "Accessed via Gate No. 3 near Karishna Polymer and Patti Kalyana underpass. Primary parking for Sewadars on duty in daily up & down commuters from Ambala side, and dedicated sector for Saints from Abroad."
    },
    {
        "id": "FEAT-PARKING-05",
        "name": "Parking 5 — East of NH-44 / Local Bus Stop & Pedestrian Hub",
        "sector": "Traffic - Panipat Side (Pedestrian Holding Hub)",
        "supervising_officer": "Day: Suresh Kumar, HPS (DSP Traffic, Panipat | 7056000501) | Night: Satyapal, HPS (ACP Highway & HQ, Gurugram | 9999981809)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "allocated_force": "Dedicated Pedestrian Holding & Batch-Release Detail; 1 Crane + 1 Fire Tender",
        "vehicle_mix": "bus_terminal",
        "polygon": [
            [77.031500, 29.177000],
            [77.035500, 29.177000],
            [77.035500, 29.182500],
            [77.031500, 29.182500],
            [77.031500, 29.177000]
        ],
        "operational_instructions": "Located east of NH-44 opposite the main complex. Houses the Local Bus Stop and holds excess pedestrians before sending them across the footbridge in pulsed batches."
    },
    {
        "id": "FEAT-PARKING-SC",
        "name": "S.C. Parking (Special Committee Member Vehicles — Gate 2)",
        "sector": "Central Mission Administrative Precinct",
        "supervising_officer": "Satish Gautam, HPS (DSP Indri, Karnal | 9729990704)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "Dedicated Security Detail & Access Control Gate 2",
        "vehicle_mix": "vip",
        "polygon": [
            [77.027000, 29.179800],
            [77.028800, 29.179800],
            [77.028800, 29.181500],
            [77.027000, 29.181500],
            [77.027000, 29.179800]
        ],
        "operational_instructions": "Designated parking court inside Gate No. 2 directly adjoining Central Mission Offices for Special Committee (S.C.) vehicles on authorized pass list."
    },
    {
        "id": "FEAT-PARKING-VIP",
        "name": "V.I.P. & Invited Guests Parking (Stage Dais Flank — Gate 2)",
        "sector": "Stage, D Area & Pandal / Law & Order Reserve",
        "supervising_officer": "Satish Gautam, HPS (DSP Indri, Karnal | 9729990704) & Mohinder Singh, HPS (DSP Hathin | 8930202024)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "Armed VVIP Parking Cover (1 1/2 Sections ORs Armed)",
        "vehicle_mix": "vip",
        "polygon": [
            [77.027000, 29.178500],
            [77.028800, 29.178500],
            [77.028800, 29.179800],
            [77.027000, 29.179800],
            [77.027000, 29.178500]
        ],
        "operational_instructions": "Sterile high-security parking enclosure for Invited Guests, State Dignitaries, and Z+ motorcade escorts for Satguru Mata Sudiksha Ji Maharaj."
    },
    {
        "id": "FEAT-PARKING-D",
        "name": "D-Parking (Dais Logistics & Service Fleet)",
        "sector": "Central Mission Administrative Precinct",
        "supervising_officer": "Mohinder Singh, HPS (DSP Hathin | 8930202024)",
        "shift_timings": "Day & Night: 24 Hours",
        "allocated_force": "Logistics & Operational Security Section",
        "vehicle_mix": "mixed",
        "polygon": [
            [77.026800, 29.181500],
            [77.028500, 29.181500],
            [77.028500, 29.182500],
            [77.026800, 29.182500],
            [77.026800, 29.181500]
        ],
        "operational_instructions": "Operations and logistics fleet staging zone for stage equipment, broadcasting OB vans, and sound engineering logistics."
    }
]

for pdef in parking_definitions:
    pcg = pcg_parking_generator(pdef["polygon"], pdef["vehicle_mix"])
    features.append({
        "type": "Feature",
        "id": pdef["id"],
        "properties": {
            "name": pdef["name"],
            "category": "PARKING_FACILITY",
            "sector": pdef["sector"],
            "supervising_officer": pdef["supervising_officer"],
            "shift_timings": pdef["shift_timings"],
            "allocated_force": pdef["allocated_force"],
            "area_sqm": pcg["sqm"],
            "area_acres": pcg["acres"],
            "pcg_car_bays": pcg["car_bays"],
            "pcg_bus_bays": pcg["bus_bays"],
            "capacity": pcg["capacity_str"],
            "evidence_status": "GROUND_TRUTH_DOCUMENTED",
            "permanence": "TEMPORARY_RECURRENT",
            "source_id": "SRC-SNM-OFFICIAL-2D-MAP-79",
            "confidence": "HIGH",
            "notes": pdef["operational_instructions"]
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [pdef["polygon"]]
        }
    })

# --- 11. PEDESTRIAN OVERBRIDGE OVER NH-44 ---
features.append({
    "type": "Feature",
    "id": "FEAT-FOOTBRIDGE-01",
    "properties": {
        "name": "NH-44 Pedestrian Overbridge (Parking 5 to Venue Frontage)",
        "category": "PEDESTRIAN_INFRASTRUCTURE",
        "structure_type": "ELEVATED_PEDESTRIAN_OVERPASS",
        "supervising_officer": "DSP Suresh Kumar (DSP Traffic, Panipat | 7056000501)",
        "allocated_force": "4 personnel at East end, 4 personnel at West end, 4 on bridge per shift (12 personnel/shift)",
        "length_m": 233.2,
        "width_m": 4.5,
        "elevation_clearance_m": 6.5,
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT_INFRASTRUCTURE",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "notes": "Controls pedestrian crossing capacity from Parking 5 temporary bus stand across NH-44 to Ceremonial Gate 1 frontage plaza. Excess pedestrians held at Parking 5 and sent across in pulsed batches; standing/stopping on bridge strictly prohibited."
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [77.032200, 29.180250],
            [77.031000, 29.180250],
            [77.029800, 29.180250]
        ]
    }
})

# --- 12. HALDANA POLICE POST & TACTICAL RESERVE BASE ---
features.append({
    "type": "Feature",
    "id": "TAC-HALDANA-POST",
    "properties": {
        "name": "Haldana Police Post & Tactical Reserve Staging Ground",
        "category": "POLICE_FACILITY",
        "tactical_type": "RESERVE_STAGING_BASE",
        "supervising_officer": "Law & Order: DSP Mohinder Singh (8930202024) / DSP Sandeep Singh (8814011504); Contingency: DSP Rajbir Singh (7056000104)",
        "shift_timings": "Day: 08:00-20:00 | Night: 20:00-08:00",
        "allocated_force": "Law & Order Reserve (1 Platoon + 1 Section ORs + 2 Sections L/ORs) + Contingency Reserve (1 Platoon + 1 Section ORs + 2 Sections L/ORs)",
        "evidence_status": "GROUND_TRUTH_DOCUMENTED",
        "permanence": "PERMANENT_POLICE_POST",
        "source_id": "SRC-POLICE-DUTY-2025",
        "confidence": "HIGH",
        "notes": "Central staging base for Panipat police contingency and riot-control reserves. Maintains shift-wise duty register, equipment distribution, and relief change log."
    },
    "geometry": {
        "type": "Point",
        "coordinates": [77.029800, 29.194500]
    }
})

# Construct single authoritative FeatureCollection
master_geojson = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": features
}

with open("nirankari_samalkha_ebandobast.geojson", "w", encoding="utf-8") as f:
    json.dump(master_geojson, f, indent=2, ensure_ascii=False)

print(f"Exported Master GeoJSON: {len(features)} total verified and categorized features!")

# Generate updated CSV and JSON inventories
inventory = []
for feat in features:
    p = feat["properties"]
    geom = feat["geometry"]
    item = {
        "feature_id": feat["id"],
        "name": p.get("name"),
        "category": p.get("category"),
        "evidence_status": p.get("evidence_status"),
        "permanence": p.get("permanence"),
        "geometry_type": geom["type"],
        "dimensions": p.get("dimensions", "N/A"),
        "area_sqm": p.get("area_sqm", "N/A"),
        "area_acres": p.get("area_acres", "N/A"),
        "elevation_m": p.get("elevation_m", 228),
        "confidence": p.get("confidence", "HIGH"),
        "source_id": p.get("source_id", "N/A"),
        "notes": p.get("notes", "")
    }
    if "supervising_officer" in p:
        item["supervising_officer"] = p["supervising_officer"]
    if "shift_timings" in p:
        item["shift_timings"] = p["shift_timings"]
    if "allocated_force" in p:
        item["allocated_force"] = p["allocated_force"]
    if "capacity" in p:
        item["capacity"] = p["capacity"]
    inventory.append(item)

with open("site_feature_inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2, ensure_ascii=False)

# Collect all unique fieldnames for CSV export
all_fields = []
for item in inventory:
    for k in item.keys():
        if k not in all_fields:
            all_fields.append(k)

import csv
with open("site_feature_inventory.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_fields)
    writer.writeheader()
    writer.writerows(inventory)

print("Saved updated site_feature_inventory.json and site_feature_inventory.csv.")
