import math
from PIL import Image

# Image bounds:
# North: 29.190533, South: 29.171349
# West:  77.008667, East:  77.030640
# Image dimensions: 1024 x 1024 pixels

NORTH = 29.190533
SOUTH = 29.171349
WEST = 77.008667
EAST = 77.030640
IMG_W = 1024
IMG_H = 1024

def pixel_to_latlon(px, py):
    lon = WEST + (px / IMG_W) * (EAST - WEST)
    lat = NORTH - (py / IMG_H) * (NORTH - SOUTH)
    return lat, lon

# Simple flat earth / UTM projection around 29.18 deg N
# 1 deg lat = 110,852 meters
# 1 deg lon = 111,320 * cos(29.18 deg) = 97,192 meters
M_PER_DEG_LAT = 110852.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(29.181))

def latlon_to_xy(lat, lon, ref_lat=29.171349, ref_lon=77.008667):
    x = (lon - ref_lon) * M_PER_DEG_LON
    y = (lat - ref_lat) * M_PER_DEG_LAT
    return x, y

def distance_m(lat1, lon1, lat2, lon2):
    dx = (lon2 - lon1) * M_PER_DEG_LON
    dy = (lat2 - lat1) * M_PER_DEG_LAT
    return math.hypot(dx, dy)

# Key pixel coordinates measured from esri_satellite_detail_z16.jpg:
# Pandal (blue/grey rectangle in center-right):
# Top-Left: around px=670, py=535
# Top-Right: around px=846, py=540
# Bottom-Left: around px=668, py=658
# Bottom-Right: around px=844, py=663

tl_lat, tl_lon = pixel_to_latlon(670, 535)
tr_lat, tr_lon = pixel_to_latlon(846, 540)
bl_lat, bl_lon = pixel_to_latlon(668, 658)
br_lat, br_lon = pixel_to_latlon(844, 663)

pandal_width = distance_m(tl_lat, tl_lon, tr_lat, tr_lon)
pandal_length = distance_m(tl_lat, tl_lon, bl_lat, bl_lon)
pandal_area_sqm = pandal_width * pandal_length
pandal_area_acres = pandal_area_sqm / 4046.86

print(f"=== MAIN SATSANG PANDAL MEASUREMENTS ===")
print(f"Top-Left (NW): {tl_lat:.6f} N, {tl_lon:.6f} E")
print(f"Top-Right (NE): {tr_lat:.6f} N, {tr_lon:.6f} E")
print(f"Bottom-Left (SW): {bl_lat:.6f} N, {bl_lon:.6f} E")
print(f"Bottom-Right (SE): {br_lat:.6f} N, {br_lon:.6f} E")
print(f"Width (East-West): {pandal_width:.1f} meters")
print(f"Length (North-South): {pandal_length:.1f} meters")
print(f"Area: {pandal_area_sqm:.1f} m² ({pandal_area_acres:.2f} acres / {pandal_area_sqm * 10.7639:.0f} sq ft)")

# Permanent Core Campus (Top-Center, px=575 to 700, py=220 to 365)
c_tl_lat, c_tl_lon = pixel_to_latlon(575, 220)
c_br_lat, c_br_lon = pixel_to_latlon(700, 365)
campus_w = distance_m(c_tl_lat, c_tl_lon, c_tl_lat, c_br_lon)
campus_h = distance_m(c_tl_lat, c_tl_lon, c_br_lat, c_tl_lon)
print(f"\n=== PERMANENT CAMPUS (ADMIN / COMPLEX) ===")
print(f"NW: {c_tl_lat:.6f} N, {c_tl_lon:.6f} E | SE: {c_br_lat:.6f} N, {c_br_lon:.6f} E")
print(f"Footprint: {campus_w:.1f} m x {campus_h:.1f} m (~{(campus_w*campus_h)/4046.86:.1f} acres)")

# Ground A (Area between Pandal/Campus and GT Road, px=846 to 970, py=420 to 720)
ga_w = distance_m(tl_lat, tr_lon, tl_lat, pixel_to_latlon(970, 540)[1])
print(f"\n=== GROUND A (FRONTAGE / CEREMONIAL PLAZA) ===")
print(f"Frontage depth along GT Road: {ga_w:.1f} meters")

# Distance from Main Gate / Pandal to Bhodwal Majri Railway Station
station_lat, station_lon = 29.18523, 77.00842
pandal_center_lat, pandal_center_lon = (tl_lat + br_lat)/2, (tl_lon + br_lon)/2
dist_to_station = distance_m(pandal_center_lat, pandal_center_lon, station_lat, station_lon)
print(f"\nDistance from Pandal Center to BDMJ Station: {dist_to_station:.1f} meters ({dist_to_station/1000:.2f} km)")
