import urllib.request
import math
import os
import sys

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

zoom = 15
center_lat, center_lon = 29.182, 77.018 # between GT road and railway station
cx, cy = deg2num(center_lat, center_lon, zoom)

print(f"Center tile for Zoom {zoom}: ({cx}, {cy})")

# Download 3x3 grid
tiles = []
for dy in [-1, 0, 1]:
    for dx in [-1, 0, 1]:
        tx = cx + dx
        ty = cy + dy
        url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ty}/{tx}"
        tile_path = f"tile_{zoom}_{tx}_{ty}.jpg"
        print(f"Downloading tile {tx}, {ty}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(tile_path, 'wb') as f:
                    f.write(data)
                tiles.append((dx, dy, tx, ty, tile_path))
        except Exception as e:
            print(f"Failed to fetch tile {tx}, {ty}: {e}")

print(f"Downloaded {len(tiles)} tiles successfully.")

# Check if PIL is available
try:
    from PIL import Image
    # Tile size is 256x256
    composite = Image.new('RGB', (256 * 3, 256 * 3))
    for dx, dy, tx, ty, tile_path in tiles:
        if os.path.exists(tile_path):
            img = Image.open(tile_path)
            composite.paste(img, ((dx + 1) * 256, (dy + 1) * 256))
    composite.save("esri_satellite_overview.jpg")
    print("Saved composite satellite image to esri_satellite_overview.jpg!")
    
    # Calculate bounding box of composite
    top_left_lat, top_left_lon = num2deg(cx - 1, cy - 1, zoom)
    bot_right_lat, bot_right_lon = num2deg(cx + 2, cy + 2, zoom)
    print(f"Composite Bounding Box:")
    print(f"  North: {top_left_lat:.6f}, South: {bot_right_lat:.6f}")
    print(f"  West:  {top_left_lon:.6f}, East:  {bot_right_lon:.6f}")
except ImportError:
    print("PIL not installed, tiles saved individually.")
