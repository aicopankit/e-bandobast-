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

zoom = 16
# Center at the Pandal and campus: lat ~ 29.182, lon ~ 77.022
center_lat, center_lon = 29.182, 77.022
cx, cy = deg2num(center_lat, center_lon, zoom)

print(f"Zoom {zoom} Center Tile: ({cx}, {cy})")

# Download 4x4 grid (covering ~2 km x 2 km at high res)
tiles = []
for dy in range(-1, 3):
    for dx in range(-2, 2):
        tx = cx + dx
        ty = cy + dy
        url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ty}/{tx}"
        tile_path = f"tile_z16_{tx}_{ty}.jpg"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(tile_path, 'wb') as f:
                    f.write(data)
                tiles.append((dx, dy, tx, ty, tile_path))
        except Exception as e:
            print(f"Failed {tx}, {ty}: {e}")

print(f"Downloaded {len(tiles)} zoom-16 tiles.")

composite = Image.new('RGB', (256 * 4, 256 * 4))
for dx, dy, tx, ty, tile_path in tiles:
    if os.path.exists(tile_path):
        img = Image.open(tile_path)
        # dx ranges -2 to 1 (add 2 -> 0 to 3)
        # dy ranges -1 to 2 (add 1 -> 0 to 3)
        composite.paste(img, ((dx + 2) * 256, (dy + 1) * 256))

composite.save("esri_satellite_detail_z16.jpg")
print("Saved high-res composite to esri_satellite_detail_z16.jpg!")

top_left_lat, top_left_lon = num2deg(cx - 2, cy - 1, zoom)
bot_right_lat, bot_right_lon = num2deg(cx + 2, cy + 3, zoom)
print(f"Zoom 16 Bounding Box:")
print(f"  North: {top_left_lat:.6f}, South: {bot_right_lat:.6f}")
print(f"  West:  {top_left_lon:.6f}, East:  {bot_right_lon:.6f}")
