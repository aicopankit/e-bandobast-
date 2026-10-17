import urllib.request
import math
import os
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

zoom = 17
# Center at the permanent campus & pandal: lat ~ 29.183, lon ~ 77.024
center_lat, center_lon = 29.183, 77.024
cx, cy = deg2num(center_lat, center_lon, zoom)

print(f"Zoom {zoom} Center Tile: ({cx}, {cy})")

# Download a 6x6 grid around campus and pandal (~1.8 km x 1.8 km at 1m/pixel)
tiles = []
for dy in range(-3, 3):
    for dx in range(-3, 3):
        tx = cx + dx
        ty = cy + dy
        url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ty}/{tx}"
        tile_path = f"tile_z17_{tx}_{ty}.jpg"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(tile_path, 'wb') as f:
                    f.write(data)
                tiles.append((dx, dy, tx, ty, tile_path))
        except Exception as e:
            print(f"Failed {tx}, {ty}: {e}")

print(f"Downloaded {len(tiles)} zoom-17 tiles.")

composite_w = 256 * 6
composite_h = 256 * 6
composite = Image.new('RGB', (composite_w, composite_h))
for dx, dy, tx, ty, tile_path in tiles:
    if os.path.exists(tile_path):
        img = Image.open(tile_path)
        px = (dx + 3) * 256
        py = (dy + 3) * 256
        composite.paste(img, (px, py))

composite.save("esri_satellite_core_z17.jpg")
print("Saved ultra-high-res composite to esri_satellite_core_z17.jpg!")

top_left_lat, top_left_lon = num2deg(cx - 3, cy - 3, zoom)
bot_right_lat, bot_right_lon = num2deg(cx + 3, cy + 3, zoom)
print(f"Zoom 17 Bounding Box:")
print(f"  North: {top_left_lat:.6f}, South: {bot_right_lat:.6f}")
print(f"  West:  {top_left_lon:.6f}, East:  {bot_right_lon:.6f}")
print(f"Pixel dimensions: {composite_w} x {composite_h}")
