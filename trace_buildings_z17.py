import math

# Image parameters for esri_satellite_core_z17.jpg:
# North: 29.190533, South: 29.176145
# West:  77.014160, East:  77.030640
# Pixel dimensions: 1536 x 1536

NORTH = 29.190533
SOUTH = 29.176145
WEST = 77.014160
EAST = 77.030640
W_PX = 1536.0
H_PX = 1536.0

def px_to_latlon(px, py):
    lon = WEST + (px / W_PX) * (EAST - WEST)
    lat = NORTH - (py / H_PX) * (NORTH - SOUTH)
    return round(lat, 6), round(lon, 6)

M_PER_DEG_LAT = 110852.0
M_PER_DEG_LON = 97192.0

def dist_m(lat1, lon1, lat2, lon2):
    dx = (lon2 - lon1) * M_PER_DEG_LON
    dy = (lat2 - lat1) * M_PER_DEG_LAT
    return math.hypot(dx, dy)

# 1. Main Satsang Pandal in Z17:
# Top-Left: px=830, py=1072
# Top-Right: px=1182, py=1078
# Bottom-Left: px=826, py=1318
# Bottom-Right: px=1178, py=1324
p_tl = px_to_latlon(830, 1072)
p_tr = px_to_latlon(1182, 1078)
p_bl = px_to_latlon(826, 1318)
p_br = px_to_latlon(1178, 1324)

print("=== MAIN PANDAL IN Z17 ===")
print("NW:", p_tl, "NE:", p_tr)
print("SW:", p_bl, "SE:", p_br)
p_w = dist_m(p_tl[0], p_tl[1], p_tr[0], p_tr[1])
p_h = dist_m(p_tl[0], p_tl[1], p_bl[0], p_bl[1])
print(f"Width: {p_w:.1f}m, Length: {p_h:.1f}m, Area: {p_w*p_h:.0f} m² ({(p_w*p_h)/4046.86:.2f} acres)")

# 2. Individual Buildings in Permanent Campus (Z17 upper-center):
# Campus Bounds: X ~ px=630 to 890, Y ~ px=450 to 730
buildings = [
    {
        "id": "BLDG-SNAS-ADMIN",
        "name": "SNAS Main Administrative & Central Bhavan",
        "px_box": [665, 460, 785, 520], # [xmin, ymin, xmax, ymax]
        "desc": "Primary administrative headquarters and reception hall of the spiritual complex."
    },
    {
        "id": "BLDG-SNAS-RES-N",
        "name": "SNAS North Residential Bhavan & Guest Wing",
        "px_box": [660, 525, 780, 565],
        "desc": "North residential accommodations for senior mission functionaries and delegates."
    },
    {
        "id": "BLDG-SNAS-RES-W",
        "name": "SNAS West Multi-Tier Residential Block",
        "px_box": [645, 620, 750, 725],
        "desc": "Multi-story residential dormitories and permanent lodging complex."
    },
    {
        "id": "BLDG-SNAS-SVC-S",
        "name": "SNAS South Logistic & Maintenance Services Facility",
        "px_box": [795, 480, 845, 570],
        "desc": "Central storehouse, maintenance depot, and utility management offices."
    },
    {
        "id": "BLDG-SNAS-HOSP",
        "name": "SNAS Medical Dispensary & Health Center (Permanent Building)",
        "px_box": [795, 580, 850, 635],
        "desc": "Permanent dispensary building serving year-round visitors and rural healthcare."
    },
    {
        "id": "BLDG-SNAS-UTIL",
        "name": "SNAS Water Treatment & Electric Substation Compound",
        "px_box": [860, 480, 895, 540],
        "desc": "Infrastructure block housing transformers, generators, and filtration plants."
    },
    {
        "id": "BLDG-SNAS-DINING",
        "name": "SNAS Permanent Community Dining & Langar Hall",
        "px_box": [640, 740, 760, 790],
        "desc": "Permanent dining pavilion and community kitchen for ashram residents."
    }
]

print("\n=== TRACED INDIVIDUAL PERMANENT BUILDINGS ===")
for b in buildings:
    xmin, ymin, xmax, ymax = b["px_box"]
    nw = px_to_latlon(xmin, ymin)
    ne = px_to_latlon(xmax, ymin)
    se = px_to_latlon(xmax, ymax)
    sw = px_to_latlon(xmin, ymax)
    bw = dist_m(nw[0], nw[1], ne[0], ne[1])
    bh = dist_m(nw[0], nw[1], sw[0], sw[1])
    b["coords"] = [nw, ne, se, sw]
    b["width_m"] = round(bw, 1)
    b["length_m"] = round(bh, 1)
    b["area_sqm"] = round(bw * bh, 1)
    print(f"* {b['id']}: {b['name']} | {bw:.1f}m x {bh:.1f}m ({bw*bh:.0f} m²) | NW: {nw}")

# 3. Tracing Internal Orthogonal Avenues:
# Central Arterial Axis (East-West avenue north of Pandal):
# py ~ 860 in Z17, spanning from GT Road (px=1480) to West (px=0 and beyond)
axis_lat = px_to_latlon(800, 860)[0]
print(f"\nCentral Arterial Avenue Latitude: {axis_lat:.6f}")

# North Avenue (running north of Campus):
north_ave_lat = px_to_latlon(800, 455)[0]
print(f"North Campus Avenue Latitude: {north_ave_lat:.6f}")

# South Avenue (running south of Pandal):
south_ave_lat = px_to_latlon(800, 1345)[0]
print(f"South Avenue Latitude: {south_ave_lat:.6f}")

# North-South Avenue 1 (West of Pandal):
ns1_lon = px_to_latlon(760, 860)[1]
# North-South Avenue 2 (Central Sector Avenue):
ns2_lon = px_to_latlon(380, 860)[1]
print(f"North-South Avenue 1 (Pandal West): {ns1_lon:.6f}")
print(f"North-South Avenue 2 (Central Grid): {ns2_lon:.6f}")
