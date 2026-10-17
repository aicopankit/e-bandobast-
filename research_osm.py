import urllib.request
import json
import os

overpass_url = 'https://overpass-api.de/api/interpreter'
query = """
[out:json][timeout:30];
(
  node(around:3000, 29.180, 77.026);
  way(around:3000, 29.180, 77.026);
  relation(around:3000, 29.180, 77.026);
);
out tags;
"""

req = urllib.request.Request(
    overpass_url, 
    data=query.encode('utf-8'), 
    headers={'User-Agent': 'eBandobastResearch/1.0 (contact@research.local)'}
)

try:
    print("Fetching OSM data...")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        elements = data.get('elements', [])
        print(f"Total elements fetched: {len(elements)}")
        
        # Save raw data for GIS processing
        with open('osm_raw_tags.json', 'w', encoding='utf-8') as f:
            json.dump(elements, f, indent=2)
            
        print("\n--- Key Named Features ---")
        for e in elements:
            tags = e.get('tags', {})
            name = tags.get('name', tags.get('name:en', ''))
            amenity = tags.get('amenity', '')
            highway = tags.get('highway', '')
            railway = tags.get('railway', '')
            landuse = tags.get('landuse', '')
            place = tags.get('place', '')
            
            if name or amenity or railway or place:
                print(f"[{e['type']} {e['id']}] {name} | amenity={amenity} | railway={railway} | highway={highway} | landuse={landuse} | place={place}")

except Exception as ex:
    print("Error querying Overpass API:", ex)
