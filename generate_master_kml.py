import json

with open("nirankari_samalkha_ebandobast.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>e-Bandobast 3D Comprehensive Site Model — Sant Nirankari Samalkha</name>
  <open>1</open>
  <description>
    <![CDATA[
      <h2>e-Bandobast Comprehensive Geospatial Digital Twin</h2>
      <p><b>Venue:</b> Sant Nirankari Sant Samagam Ground (Sant Nirankari Adhyatmik Sthal — SNAS)</p>
      <p><b>Location:</b> Bhodwal Majri, Samalkha, Panipat, Haryana, India</p>
      <p><b>Georeference:</b> Lat 29.1805° N, Lon 77.0249° E | Plus Code: 52HG+VF2</p>
      <p><b>Scope:</b> Complete site reconstruction including 650+ acre grounds, 7 individual campus buildings, 367m Main Pandal, 66 external roads, internal avenues, and Delhi-Ambala railway line.</p>
    ]]>
  </description>

  <!-- STYLES -->
  <Style id="stylePandal3D">
    <LineStyle><color>ffffaa00</color><width>3</width></LineStyle>
    <PolyStyle><color>aa442211</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleBuilding3D">
    <LineStyle><color>ffffdd88</color><width>2</width></LineStyle>
    <PolyStyle><color>dd995522</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleGroundA">
    <LineStyle><color>ff0000ff</color><width>3</width></LineStyle>
    <PolyStyle><color>220000ff</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleGroundB">
    <LineStyle><color>ff00ffff</color><width>3</width></LineStyle>
    <PolyStyle><color>2200ffff</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleGroundC">
    <LineStyle><color>ff00ff00</color><width>3</width></LineStyle>
    <PolyStyle><color>2200ff00</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleGroundD">
    <LineStyle><color>ffffaa00</color><width>3</width></LineStyle>
    <PolyStyle><color>22ffaa00</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleBoundary">
    <LineStyle><color>ffffffff</color><width>4</width></LineStyle>
    <PolyStyle><color>11ffffff</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleInternalRoad">
    <LineStyle><color>ffffffff</color><width>4</width></LineStyle>
  </Style>

  <Style id="styleExternalRoad">
    <LineStyle><color>ff00aaff</color><width>3</width></LineStyle>
  </Style>

  <Style id="styleHighwayNH44">
    <LineStyle><color>ff0066ff</color><width>5</width></LineStyle>
  </Style>

  <Style id="styleRailway">
    <LineStyle><color>ff222222</color><width>4</width></LineStyle>
  </Style>

  <Style id="styleCanal">
    <LineStyle><color>ffff6600</color><width>4</width></LineStyle>
  </Style>

  <Style id="styleVIPRoute">
    <LineStyle><color>ff00ff00</color><width>6</width></LineStyle>
  </Style>

  <Style id="styleEvacRoute">
    <LineStyle><color>ff0000ff</color><width>5</width></LineStyle>
  </Style>
  <Style id="styleParking">
    <LineStyle><color>ffffaa00</color><width>3</width></LineStyle>
    <PolyStyle><color>44ffaa00</color><fill>1</fill><outline>1</outline></PolyStyle>
  </Style>

  <Style id="styleFootbridge">
    <LineStyle><color>ff00ffff</color><width>6</width></LineStyle>
  </Style>

  <Style id="stylePolicePost">
    <IconStyle>
      <color>ff0000ff</color>
      <scale>1.2</scale>
    </IconStyle>
  </Style>
"""

folders = {
    "Boundaries & Sectors": [],
    "Dedicated Event Parking (Parking 1-5 & VIP)": [],
    "Pedestrian Infrastructure & Footbridge": [],
    "3D Event & Campus Buildings": [],
    "Internal Avenues & Lanes": [],
    "External Roads & Highways": [],
    "Civil Infrastructure & Surroundings": [],
    "Railway Infrastructure": [],
    "Hydrographic Features": [],
    "Police & Emergency Deployments": [],
    "Police Facilities & Reserve Posts": [],
    "VIP Convoy & Evacuation Corridors": []
}

for feat in geo["features"]:
    p = feat["properties"]
    geom = feat["geometry"]
    gtype = geom["type"]
    cat = p.get("category", "")
    fid = feat["id"]
    name = p.get("name", fid)
    desc = f"<![CDATA[<b>{name}</b><br/><b>ID:</b> {fid}<br/><b>Category:</b> {cat}<br/><b>Status:</b> {p.get('evidence_status', 'N/A')}<br/>"
    if "dimensions" in p: desc += f"<b>Dimensions:</b> {p['dimensions']}<br/>"
    if "area_sqm" in p: desc += f"<b>Area:</b> {p['area_sqm']} m²<br/>"
    if "force_strength" in p: desc += f"<b>Force Strength:</b> {p['force_strength']}<br/>"
    if "notes" in p: desc += f"<p>{p['notes']}</p>"
    desc += "]]>"

    if cat == "VENUE_BOUNDARY" or cat == "SECURITY_SECTOR":
        style = "#styleBoundary"
        if "GROUND-A" in fid: style = "#styleGroundA"
        elif "GROUND-B" in fid: style = "#styleGroundB"
        elif "GROUND-C" in fid: style = "#styleGroundC"
        elif "GROUND-D" in fid: style = "#styleGroundD"

        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"][0]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>{style}</styleUrl>
      <description>{desc}</description>
      <Polygon>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>{coords_str}</coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
        folders["Boundaries & Sectors"].append(placemark)

    elif cat == "EVENT_STRUCTURE" or cat == "PERMANENT_BUILDING":
        if gtype == "Polygon":
            h = p.get("estimated_height_m", 10.0)
            style = "#stylePandal3D" if "PANDAL" in fid else "#styleBuilding3D"
            coords_str = "\n".join([f"{pt[0]},{pt[1]},{h}" for pt in geom["coordinates"][0]])
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>{style}</styleUrl>
      <description>{desc}</description>
      <Polygon>
        <extrude>1</extrude>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>{coords_str}</coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
        elif gtype == "Point":
            c = geom["coordinates"]
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{c[0]},{c[1]},0</coordinates>
      </Point>
    </Placemark>"""
        folders["3D Event & Campus Buildings"].append(placemark)

    elif cat == "INTERNAL_ROAD":
        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleInternalRoad</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        folders["Internal Avenues & Lanes"].append(placemark)

    elif cat == "EXTERNAL_ROAD":
        hw = p.get("highway_type", "")
        style = "#styleHighwayNH44" if hw == "trunk" else "#styleExternalRoad"
        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>{style}</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        folders["External Roads & Highways"].append(placemark)

    elif cat == "RAILWAY_INFRASTRUCTURE" or cat == "TRANSPORT_HUB":
        if gtype == "LineString":
            coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleRailway</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        elif gtype == "Point":
            c = geom["coordinates"]
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{c[0]},{c[1]},0</coordinates>
      </Point>
    </Placemark>"""
        folders["Railway Infrastructure"].append(placemark)

    elif cat == "HYDROGRAPHIC":
        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleCanal</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        folders["Hydrographic Features"].append(placemark)

    elif cat == "BANDOBAST_TACTICAL" or cat == "ACCESS_CONTROL":
        c = geom["coordinates"]
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{c[0]},{c[1]},0</coordinates>
      </Point>
    </Placemark>"""
        folders["Police & Emergency Deployments"].append(placemark)

    elif cat == "PARKING_FACILITY":
        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"][0]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleParking</styleUrl>
      <description>{desc}</description>
      <Polygon>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>{coords_str}</coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
        folders["Dedicated Event Parking (Parking 1-5 & VIP)"].append(placemark)

    elif cat == "CIVIL_INFRASTRUCTURE":
        if gtype == "Polygon":
            coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"][0]])
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleBuilding3D</styleUrl>
      <description>{desc}</description>
      <Polygon>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>{coords_str}</coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
        elif gtype == "LineString":
            coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleHighwayNH44</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        else:
            c = geom["coordinates"]
            placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{c[0]},{c[1]},0</coordinates>
      </Point>
    </Placemark>"""
        folders["Civil Infrastructure & Surroundings"].append(placemark)

    elif cat == "PEDESTRIAN_INFRASTRUCTURE":
        coords_str = "\n".join([f"{pt[0]},{pt[1]},6.5" for pt in geom["coordinates"]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>#styleFootbridge</styleUrl>
      <description>{desc}</description>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        folders["Pedestrian Infrastructure & Footbridge"].append(placemark)

    elif cat == "POLICE_FACILITY":
        c = geom["coordinates"]
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{c[0]},{c[1]},0</coordinates>
      </Point>
    </Placemark>"""
        folders["Police Facilities & Reserve Posts"].append(placemark)

    elif cat == "OPERATIONAL_ROUTE":
        style = "#styleVIPRoute" if ("VIP" in fid or "SC" in fid) else "#styleEvacRoute"
        coords_str = "\n".join([f"{pt[0]},{pt[1]},0" for pt in geom["coordinates"]])
        placemark = f"""
    <Placemark id="{fid}">
      <name>{name}</name>
      <styleUrl>{style}</styleUrl>
      <description>{desc}</description>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>{coords_str}</coordinates>
      </LineString>
    </Placemark>"""
        folders["VIP Convoy & Evacuation Corridors"].append(placemark)

# Assemble KML
kml_body = ""
for fname, pmarks in folders.items():
    if pmarks:
        kml_body += f"\n  <Folder>\n    <name>{fname} ({len(pmarks)})</name>\n    <open>1</open>\n"
        kml_body += "\n".join(pmarks)
        kml_body += "\n  </Folder>\n"

kml_footer = "\n</Document>\n</kml>"

with open("samalkha_bandobast_3d.kml", "w", encoding="utf-8") as f:
    f.write(kml_header + kml_body + kml_footer)

print("Exported updated samalkha_bandobast_3d.kml with all 109 master features!")
