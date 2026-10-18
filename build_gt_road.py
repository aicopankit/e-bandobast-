import os
import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Read index.html: {len(html)} bytes")

    # Marker 1: Helper functions before loadMasterGeoJSON
    m1_target = "    // --- REAL-WORLD SPATIAL CONSTRAINTS & PCG GEOMETRY STORES ---\n    const pcgRoadSegments = [];\n    const pcgExclusionPolygons = [];\n    const pcgSectorPolygons = {};"
    assert m1_target in html, "m1_target not found"

    helper_code = """    // --- REAL-WORLD SPATIAL CONSTRAINTS & PCG GEOMETRY STORES ---
    const pcgRoadSegments = [];
    const pcgExclusionPolygons = [];
    const pcgSectorPolygons = {};

    // --- HIGHWAY (NH-44 / GT ROAD) DUAL CARRIAGEWAY & INFRASTRUCTURE SYSTEM ---
    const trafficVehicles = [];
    let curveNorthbound = null;
    let curveSouthbound = null;
    const collectedNorthboundPts = [];
    const collectedSouthboundPts = [];

    // Continuous real-world flyover elevation profile
    function getHighwayElevation(z, isBridge) {
      if (!isBridge) return 1.15;
      // Patti Kalyana Flyover: Z = -450 (South ramp) to Z = -1035 (North ramp)
      const zSouthGround = -450;
      const zSouthDeck = -510;
      const zNorthDeck = -975;
      const zNorthGround = -1035;
      const deckH = 6.8;
      const groundH = 1.15;

      if (z > zSouthGround || z < zNorthGround) {
        return groundH;
      } else if (z <= zSouthGround && z > zSouthDeck) {
        const t = (zSouthGround - z) / (zSouthGround - zSouthDeck);
        return groundH + (deckH - groundH) * t;
      } else if (z <= zSouthDeck && z >= zNorthDeck) {
        return deckH;
      } else if (z < zNorthDeck && z >= zNorthGround) {
        const t = (z - zNorthGround) / (zNorthDeck - zNorthGround);
        return groundH + (deckH - groundH) * t;
      }
      return groundH;
    }

    // High-precision road ribbon mesh generator
    function buildRoadRibbonMesh(pts, width, getY, options = {}) {
      const n = pts.length;
      if (n < 2) return null;

      const normals = [];
      for (let i = 0; i < n; i++) {
        const p = pts[i];
        let dx = 0, dz = 0;
        if (i === 0) {
          dx = pts[1].x - p.x;
          dz = pts[1].z - p.z;
        } else if (i === n - 1) {
          dx = p.x - pts[n - 2].x;
          dz = p.z - pts[n - 2].z;
        } else {
          const d1x = p.x - pts[i - 1].x, d1z = p.z - pts[i - 1].z;
          const d2x = pts[i + 1].x - p.x, d2z = pts[i + 1].z - p.z;
          const l1 = Math.hypot(d1x, d1z) || 1.0;
          const l2 = Math.hypot(d2x, d2z) || 1.0;
          dx = d1x / l1 + d2x / l2;
          dz = d1z / l1 + d2z / l2;
        }
        const len = Math.hypot(dx, dz) || 1.0;
        normals.push(new THREE.Vector2(-dz / len, dx / len));
      }

      const vertices = [];
      const uvs = [];
      let cumDist = 0;

      for (let i = 0; i < n; i++) {
        const p = pts[i];
        const norm = normals[i];
        const yVal = (typeof getY === 'function') ? getY(p.z, p) : (getY !== undefined ? getY : p.y);

        if (i > 0) cumDist += p.distanceTo(pts[i - 1]);

        const halfW = width * 0.5;
        const lx = p.x + norm.x * halfW;
        const lz = p.z + norm.y * halfW;
        const rx = p.x - norm.x * halfW;
        const rz = p.z - norm.y * halfW;

        vertices.push(lx, yVal, lz);
        vertices.push(rx, yVal, rz);
        uvs.push(0, cumDist / 20.0);
        uvs.push(1, cumDist / 20.0);
      }

      const indices = [];
      for (let i = 0; i < n - 1; i++) {
        const v0 = i * 2, v1 = i * 2 + 1, v2 = (i + 1) * 2, v3 = (i + 1) * 2 + 1;
        indices.push(v0, v1, v2);
        indices.push(v2, v1, v3);
      }

      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      geo.setIndex(indices);
      geo.computeVertexNormals();

      const mat = options.material || new THREE.MeshStandardMaterial({
        color: options.color || 0x1f242d,
        roughness: options.roughness !== undefined ? options.roughness : 0.88,
        metalness: options.metalness !== undefined ? options.metalness : 0.08,
        side: THREE.DoubleSide
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.receiveShadow = true;
      return mesh;
    }

    // Offset point sequence for markings and barriers
    function getRibbonOffsetPoints(pts, width, alpha, getY, yOffset = 0.04) {
      const n = pts.length;
      const normals = [];
      for (let i = 0; i < n; i++) {
        const p = pts[i];
        let dx = 0, dz = 0;
        if (i === 0) {
          dx = pts[1].x - p.x; dz = pts[1].z - p.z;
        } else if (i === n - 1) {
          dx = p.x - pts[n - 2].x; dz = p.z - pts[n - 2].z;
        } else {
          const d1x = p.x - pts[i - 1].x, d1z = p.z - pts[i - 1].z;
          const d2x = pts[i + 1].x - p.x, d2z = pts[i + 1].z - p.z;
          const l1 = Math.hypot(d1x, d1z) || 1.0;
          const l2 = Math.hypot(d2x, d2z) || 1.0;
          dx = d1x / l1 + d2x / l2; dz = d1z / l1 + d2z / l2;
        }
        const len = Math.hypot(dx, dz) || 1.0;
        normals.push(new THREE.Vector2(-dz / len, dx / len));
      }

      const result = [];
      const halfW = width * 0.5;
      const offset = halfW - alpha * width;
      for (let i = 0; i < n; i++) {
        const p = pts[i];
        const norm = normals[i];
        const yVal = ((typeof getY === 'function') ? getY(p.z, p) : (getY !== undefined ? getY : p.y)) + yOffset;
        result.push(new THREE.Vector3(p.x + norm.x * offset, yVal, p.z + norm.y * offset));
      }
      return result;
    }

    // Extruded Concrete Jersey Barrier with anti-glare screen
    function createJerseyBarrierMesh(pts, width, alpha, getY) {
      const group = new THREE.Group();
      const bPts = getRibbonOffsetPoints(pts, width, alpha, getY, 0.0);
      if (bPts.length < 2) return group;

      const barrierMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.75 });
      const hedgeMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.85 });

      for (let i = 0; i < bPts.length - 1; i++) {
        const p1 = bPts[i];
        const p2 = bPts[i + 1];
        const len = p1.distanceTo(p2);
        if (len < 0.1) continue;

        const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
        const dir = new THREE.Vector3().subVectors(p2, p1).normalize();
        const rotY = Math.atan2(dir.x, dir.z);

        const bGeo = new THREE.BoxGeometry(0.55, 0.85, len);
        const bMesh = new THREE.Mesh(bGeo, barrierMat);
        bMesh.position.set(mid.x, mid.y + 0.425, mid.z);
        bMesh.rotation.y = rotY;
        group.add(bMesh);

        const hGeo = new THREE.BoxGeometry(0.22, 0.55, len);
        const hMesh = new THREE.Mesh(hGeo, hedgeMat);
        hMesh.position.set(mid.x, mid.y + 0.85 + 0.275, mid.z);
        hMesh.rotation.y = rotY;
        group.add(hMesh);
      }
      return group;
    }

    // Outer Galvanized Steel W-Beam Guardrails
    function createGuardrailMesh(pts, width, alpha, getY) {
      const group = new THREE.Group();
      const rPts = getRibbonOffsetPoints(pts, width, alpha, getY, 0.0);
      if (rPts.length < 2) return group;

      const railMat = new THREE.MeshStandardMaterial({ color: 0xcfd6dc, metalness: 0.85, roughness: 0.25 });
      const postMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.7, roughness: 0.4 });
      const postGeo = new THREE.BoxGeometry(0.12, 0.9, 0.12);

      for (let i = 0; i < rPts.length - 1; i++) {
        const p1 = rPts[i];
        const p2 = rPts[i + 1];
        const len = p1.distanceTo(p2);
        if (len < 0.1) continue;

        const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
        const dir = new THREE.Vector3().subVectors(p2, p1).normalize();
        const rotY = Math.atan2(dir.x, dir.z);

        const rGeo = new THREE.BoxGeometry(0.15, 0.35, len);
        const rMesh = new THREE.Mesh(rGeo, railMat);
        rMesh.position.set(mid.x, mid.y + 0.65, mid.z);
        rMesh.rotation.y = rotY;
        group.add(rMesh);

        const numPosts = Math.max(1, Math.floor(len / 12.0));
        for (let k = 0; k <= numPosts; k++) {
          const frac = k / numPosts;
          const postPos = new THREE.Vector3().lerpVectors(p1, p2, frac);
          const post = new THREE.Mesh(postGeo, postMat);
          post.position.set(postPos.x, postPos.y + 0.45, postPos.z);
          group.add(post);
        }
      }
      return group;
    }

    // 12m Dual Outreach Arm Highway Light Pole
    function createStreetlightGroup() {
      const poleGroup = new THREE.Group();
      const poleMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.8, roughness: 0.3 });
      const headMat = new THREE.MeshStandardMaterial({ color: 0xfffaed, emissive: 0xfffaed, emissiveIntensity: 0.9 });

      const base = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.5, 0.7), poleMat);
      base.position.y = 0.25;
      poleGroup.add(base);

      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.24, 11.5, 8), poleMat);
      mast.position.y = 6.0;
      poleGroup.add(mast);

      [-1, 1].forEach(side => {
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 3.8, 6), poleMat);
        arm.rotation.z = side * (Math.PI / 3);
        arm.position.set(side * 1.6, 11.5, 0);
        poleGroup.add(arm);

        const head = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.2, 0.35), headMat);
        head.position.set(side * 3.3, 12.4, 0);
        poleGroup.add(head);
      });
      return poleGroup;
    }

    // High-Resolution NHAI Green Signboard Texture
    function createHighwayGantryTexture(signW, signH, leftTitle, leftLines, rightTitle, rightLines) {
      const canvas = document.createElement('canvas');
      canvas.width = signW;
      canvas.height = signH;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#006a4e';
      ctx.fillRect(0, 0, signW, signH);

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 10;
      ctx.strokeRect(8, 8, signW - 16, signH - 16);
      ctx.lineWidth = 3;
      ctx.strokeRect(20, 20, signW - 40, signH - 40);

      const divX = Math.floor(signW * 0.56);
      ctx.beginPath();
      ctx.moveTo(divX, 20);
      ctx.lineTo(divX, signH - 20);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 4;
      ctx.stroke();

      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 28px sans-serif';
      ctx.fillText(leftTitle, 36, 62);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 36px sans-serif';
      let y = 120;
      leftLines.forEach(line => {
        ctx.fillText(line, 36, y);
        y += 56;
      });

      ctx.fillStyle = '#facc15';
      ctx.font = 'bold 28px sans-serif';
      ctx.fillText(rightTitle, divX + 28, 62);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 34px sans-serif';
      y = 120;
      rightLines.forEach(line => {
        ctx.fillText(line, divX + 28, y);
        y += 56;
      });

      const tex = new THREE.CanvasTexture(canvas);
      tex.anisotropy = 4;
      return tex;
    }

    // 3D Overhead Highway Steel Space Truss Gantry
    function buildGantryStructure(x, z, rotY, tex) {
      const gantryG = new THREE.Group();
      const trussMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.7, roughness: 0.3 });

      const spanW = 38.0;
      const trussH = 8.8;

      [-spanW / 2, spanW / 2].forEach(px => {
        const tower = new THREE.Mesh(new THREE.BoxGeometry(1.2, trussH, 1.2), trussMat);
        tower.position.set(px, trussH / 2, 0);
        gantryG.add(tower);
        const foot = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.6, 2.0), trussMat);
        foot.position.set(px, 0.3, 0);
        gantryG.add(foot);
      });

      const beam = new THREE.Mesh(new THREE.BoxGeometry(spanW + 2, 1.4, 1.2), trussMat);
      beam.position.y = trussH;
      gantryG.add(beam);

      const signMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(32, 7.5),
        new THREE.MeshStandardMaterial({ map: tex, roughness: 0.4 })
      );
      signMesh.position.set(0, trussH + 0.5, 0.65);
      gantryG.add(signMesh);

      const lumBar = new THREE.Mesh(
        new THREE.BoxGeometry(32, 0.25, 0.8),
        new THREE.MeshStandardMaterial({ color: 0xfffaed, emissive: 0xfffaed, emissiveIntensity: 0.8 })
      );
      lumBar.position.set(0, trussH + 4.4, 0.8);
      gantryG.add(lumBar);

      gantryG.position.set(x, 0, z);
      gantryG.rotation.y = rotY;
      return gantryG;
    }

    // 3D Vehicle Models (Low-Poly, High-Realism Indian Highway Vehicles)
    function createBusMesh() {
      const busG = new THREE.Group();
      const blueMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.4 });
      const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 });
      const glassMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.1, metalness: 0.8 });
      const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
      const tarpMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.7 });
      const headMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, emissive: 0xfffbeb, emissiveIntensity: 0.9 });
      const tailMat = new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 });

      const lower = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.4, 11.0), blueMat);
      lower.position.y = 1.1;
      busG.add(lower);

      const upper = new THREE.Mesh(new THREE.BoxGeometry(2.55, 1.5, 10.9), whiteMat);
      upper.position.y = 2.45;
      busG.add(upper);

      const win = new THREE.Mesh(new THREE.BoxGeometry(2.62, 0.7, 10.2), glassMat);
      win.position.y = 2.45;
      busG.add(win);

      const rack = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.25, 7.0), new THREE.MeshStandardMaterial({ color: 0x94a3b8 }));
      rack.position.set(0, 3.3, 0);
      busG.add(rack);

      const tarp1 = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.6, 3.2), tarpMat);
      tarp1.position.set(0, 3.65, -1.0);
      busG.add(tarp1);

      const tarp2 = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.5, 2.4), new THREE.MeshStandardMaterial({ color: 0x15803d }));
      tarp2.position.set(0, 3.6, 1.8);
      busG.add(tarp2);

      const wheelGeo = new THREE.CylinderGeometry(0.48, 0.48, 0.35, 12);
      wheelGeo.rotateZ(Math.PI / 2);
      [-1.25, 1.25].forEach(wx => {
        [-3.6, 2.6, 3.8].forEach(wz => {
          const wMesh = new THREE.Mesh(wheelGeo, wheelMat);
          wMesh.position.set(wx, 0.48, wz);
          busG.add(wMesh);
        });
      });

      [-0.9, 0.9].forEach(lx => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.2, 0.1), headMat);
        hl.position.set(lx, 1.1, -5.55);
        busG.add(hl);
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.3, 0.1), tailMat);
        tl.position.set(lx, 1.2, 5.55);
        busG.add(tl);
      });
      return busG;
    }

    function createTruckMesh(cabColorHex = 0xea580c) {
      const truckG = new THREE.Group();
      const cabMat = new THREE.MeshStandardMaterial({ color: cabColorHex, roughness: 0.4 });
      const woodMat = new THREE.MeshStandardMaterial({ color: 0x9a3412, roughness: 0.8 });
      const chassisMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.6 });
      const wheelMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.8 });
      const headMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, emissive: 0xfffbeb, emissiveIntensity: 0.9 });
      const tailMat = new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 });

      const chassis = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.5, 9.5), chassisMat);
      chassis.position.y = 0.8;
      truckG.add(chassis);

      const cab = new THREE.Mesh(new THREE.BoxGeometry(2.45, 2.4, 2.6), cabMat);
      cab.position.set(0, 2.0, -3.2);
      truckG.add(cab);

      const body = new THREE.Mesh(new THREE.BoxGeometry(2.5, 2.6, 6.4), woodMat);
      body.position.set(0, 2.3, 1.4);
      truckG.add(body);

      const wheelGeo = new THREE.CylinderGeometry(0.5, 0.5, 0.4, 12);
      wheelGeo.rotateZ(Math.PI / 2);
      [-1.2, 1.2].forEach(wx => {
        [-3.2, 2.2, 3.4].forEach(wz => {
          const wMesh = new THREE.Mesh(wheelGeo, wheelMat);
          wMesh.position.set(wx, 0.5, wz);
          truckG.add(wMesh);
        });
      });

      [-0.8, 0.8].forEach(lx => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.25, 0.1), headMat);
        hl.position.set(lx, 1.1, -4.55);
        truckG.add(hl);
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.25, 0.1), tailMat);
        tl.position.set(lx, 1.0, 4.65);
        truckG.add(tl);
      });
      return truckG;
    }

    function createCarMesh(isPolice = false, colorHex = 0xf8fafc) {
      const carG = new THREE.Group();
      const bodyMat = new THREE.MeshStandardMaterial({ color: isPolice ? 0xf8fafc : colorHex, roughness: 0.3 });
      const glassMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.1, metalness: 0.8 });
      const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
      const headMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, emissive: 0xfffbeb, emissiveIntensity: 0.9 });
      const tailMat = new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0xef4444, emissiveIntensity: 0.9 });

      const bodyLower = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.85, 4.8), bodyMat);
      bodyLower.position.y = 0.75;
      carG.add(bodyLower);

      const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.8, 2.6), bodyMat);
      cabin.position.set(0, 1.45, 0.2);
      carG.add(cabin);

      const win = new THREE.Mesh(new THREE.BoxGeometry(1.72, 0.5, 2.4), glassMat);
      win.position.set(0, 1.45, 0.2);
      carG.add(win);

      if (isPolice) {
        const stripeMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a });
        const stripe = new THREE.Mesh(new THREE.BoxGeometry(1.92, 0.25, 4.6), stripeMat);
        stripe.position.y = 0.75;
        carG.add(stripe);

        const strobeR = new THREE.Mesh(
          new THREE.BoxGeometry(0.35, 0.15, 0.2),
          new THREE.MeshStandardMaterial({ color: 0xff0033, emissive: 0xff0033, emissiveIntensity: 1.0 })
        );
        strobeR.position.set(-0.4, 1.95, 0.2);
        carG.add(strobeR);

        const strobeB = new THREE.Mesh(
          new THREE.BoxGeometry(0.35, 0.15, 0.2),
          new THREE.MeshStandardMaterial({ color: 0x0066ff, emissive: 0x0066ff, emissiveIntensity: 1.0 })
        );
        strobeB.position.set(0.4, 1.95, 0.2);
        carG.add(strobeB);

        carG.userData.strobeR = strobeR;
        carG.userData.strobeB = strobeB;
      }

      const wheelGeo = new THREE.CylinderGeometry(0.35, 0.35, 0.25, 12);
      wheelGeo.rotateZ(Math.PI / 2);
      [-0.95, 0.95].forEach(wx => {
        [-1.5, 1.5].forEach(wz => {
          const wMesh = new THREE.Mesh(wheelGeo, wheelMat);
          wMesh.position.set(wx, 0.35, wz);
          carG.add(wMesh);
        });
      });

      [-0.65, 0.65].forEach(lx => {
        const hl = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.18, 0.08), headMat);
        hl.position.set(lx, 0.75, -2.42);
        carG.add(hl);
        const tl = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.18, 0.08), tailMat);
        tl.position.set(lx, 0.75, 2.42);
        carG.add(tl);
      });
      return carG;
    }

    // Initialize 38 Highway Simulation Vehicles along NH-44
    function initHighwayTraffic() {
      if (!curveNorthbound || !curveSouthbound) return;

      const corridorLen = 4050.0;
      // 18 Northbound vehicles (Heading towards -Z)
      const nbVehicles = [
        { type: 'bus', speed: 19.0, lane: 0.0, prog: 0.05 },
        { type: 'bus', speed: 18.5, lane: 0.0, prog: 0.38 },
        { type: 'bus', speed: 19.2, lane: 0.0, prog: 0.72 },
        { type: 'truck', speed: 16.0, lane: -3.6, prog: 0.12, color: 0xea580c },
        { type: 'truck', speed: 16.5, lane: -3.6, prog: 0.45, color: 0x0284c7 },
        { type: 'truck', speed: 15.8, lane: -3.6, prog: 0.82, color: 0xdc2626 },
        { type: 'truck', speed: 16.2, lane: -3.6, prog: 0.95, color: 0x059669 },
        { type: 'car', speed: 22.0, lane: 3.6, prog: 0.18, color: 0xf8fafc },
        { type: 'car', speed: 23.0, lane: 3.6, prog: 0.28, color: 0x94a3b8 },
        { type: 'car', speed: 21.5, lane: 0.0, prog: 0.52, color: 0xf1f5f9 },
        { type: 'car', speed: 22.5, lane: 3.6, prog: 0.65, color: 0x334155 },
        { type: 'car', speed: 23.5, lane: 3.6, prog: 0.88, color: 0xffffff },
        { type: 'police', speed: 25.0, lane: 3.6, prog: 0.22 },
        { type: 'bus', speed: 19.0, lane: 0.0, prog: 0.60 },
        { type: 'truck', speed: 16.0, lane: -3.6, prog: 0.25, color: 0xca8a04 },
        { type: 'car', speed: 22.0, lane: 3.6, prog: 0.40, color: 0xf8fafc },
        { type: 'car', speed: 22.8, lane: 0.0, prog: 0.78, color: 0x94a3b8 },
        { type: 'car', speed: 21.0, lane: 3.6, prog: 0.98, color: 0xf1f5f9 }
      ];

      // 20 Southbound vehicles (Heading towards +Z)
      const sbVehicles = [
        { type: 'bus', speed: 19.0, lane: 0.0, prog: 0.08 },
        { type: 'bus', speed: 18.8, lane: 0.0, prog: 0.32 },
        { type: 'bus', speed: 19.3, lane: 0.0, prog: 0.62 },
        { type: 'bus', speed: 19.1, lane: 0.0, prog: 0.85 },
        { type: 'truck', speed: 16.0, lane: 3.6, prog: 0.15, color: 0xea580c },
        { type: 'truck', speed: 16.4, lane: 3.6, prog: 0.42, color: 0x0284c7 },
        { type: 'truck', speed: 15.9, lane: 3.6, prog: 0.70, color: 0xdc2626 },
        { type: 'truck', speed: 16.3, lane: 3.6, prog: 0.92, color: 0x059669 },
        { type: 'truck', speed: 16.1, lane: 3.6, prog: 0.55, color: 0xca8a04 },
        { type: 'car', speed: 22.0, lane: -3.6, prog: 0.04, color: 0xf8fafc },
        { type: 'car', speed: 23.2, lane: -3.6, prog: 0.24, color: 0x94a3b8 },
        { type: 'car', speed: 21.8, lane: 0.0, prog: 0.48, color: 0xf1f5f9 },
        { type: 'car', speed: 22.6, lane: -3.6, prog: 0.66, color: 0x334155 },
        { type: 'car', speed: 23.4, lane: -3.6, prog: 0.80, color: 0xffffff },
        { type: 'police', speed: 25.0, lane: -3.6, prog: 0.50 },
        { type: 'bus', speed: 19.0, lane: 0.0, prog: 0.45 },
        { type: 'car', speed: 22.2, lane: 0.0, prog: 0.19, color: 0xf8fafc },
        { type: 'car', speed: 21.5, lane: -3.6, prog: 0.37, color: 0x94a3b8 },
        { type: 'car', speed: 22.9, lane: -3.6, prog: 0.75, color: 0xf1f5f9 },
        { type: 'car', speed: 23.1, lane: -3.6, prog: 0.96, color: 0xffffff }
      ];

      nbVehicles.forEach(cfg => {
        let mesh = null;
        if (cfg.type === 'bus') mesh = createBusMesh();
        else if (cfg.type === 'truck') mesh = createTruckMesh(cfg.color);
        else if (cfg.type === 'police') mesh = createCarMesh(true);
        else mesh = createCarMesh(false, cfg.color);

        layerGroups.externalRoads.add(mesh);
        trafficVehicles.push({
          mesh: mesh,
          curve: curveNorthbound,
          corridorLen: corridorLen,
          speed: cfg.speed,
          laneOffset: cfg.lane,
          progress: cfg.prog,
          isPolice: cfg.type === 'police'
        });
      });

      sbVehicles.forEach(cfg => {
        let mesh = null;
        if (cfg.type === 'bus') mesh = createBusMesh();
        else if (cfg.type === 'truck') mesh = createTruckMesh(cfg.color);
        else if (cfg.type === 'police') mesh = createCarMesh(true);
        else mesh = createCarMesh(false, cfg.color);

        layerGroups.externalRoads.add(mesh);
        trafficVehicles.push({
          mesh: mesh,
          curve: curveSouthbound,
          corridorLen: corridorLen,
          speed: cfg.speed,
          laneOffset: cfg.lane,
          progress: cfg.prog,
          isPolice: cfg.type === 'police'
        });
      });
    }

    // Dynamic Traffic Animation Update
    function updateHighwayTraffic(currentTime, dt) {
      if (!trafficVehicles || trafficVehicles.length === 0) return;
      const flashCycle = Math.floor(currentTime * 0.008) % 2;

      for (let i = 0; i < trafficVehicles.length; i++) {
        const v = trafficVehicles[i];
        v.progress = (v.progress + (v.speed * dt) / v.corridorLen) % 1.0;

        const pos = v.curve.getPointAt(v.progress);
        const tan = v.curve.getTangentAt(v.progress);
        const norm = new THREE.Vector3(-tan.z, 0, tan.x);

        const x = pos.x + norm.x * v.laneOffset;
        const z = pos.z + norm.z * v.laneOffset;
        const yBase = getHighwayElevation(z, true);

        v.mesh.position.set(x, yBase, z);
        v.mesh.rotation.y = Math.atan2(tan.x, tan.z);

        if (v.isPolice && v.mesh.userData.strobeR && v.mesh.userData.strobeB) {
          if (flashCycle === 0) {
            v.mesh.userData.strobeR.material.emissiveIntensity = 2.2;
            v.mesh.userData.strobeB.material.emissiveIntensity = 0.1;
          } else {
            v.mesh.userData.strobeR.material.emissiveIntensity = 0.1;
            v.mesh.userData.strobeB.material.emissiveIntensity = 2.2;
          }
        }
      }
    }

    // Build 3 Overhead Highway Direction Gantries
    function buildHighwayGantries() {
      // 1. South Approach (Northbound at Z = +750m, X = 590m)
      const tex1 = createHighwayGantryTexture(
        1024, 384,
        "🛣️ NH-44 / AH1 NORTHBOUND THROUGH",
        ["⬆️ PANIPAT       18 km", "⬆️ AMBALA      125 km", "⬆️ CHANDIGARH  170 km"],
        "↗️ EXIT 500m (SERVICE ROAD)",
        ["🚪 GATE 1 (SOUTH GATEWAY)", "🅿️ PARKING P1 / P2", "🏘️ SAMALKHA TOWN"]
      );
      const gantry1 = buildGantryStructure(588, 750, 0, tex1);
      layerGroups.externalRoads.add(gantry1);

      // 2. VIP Ceremonial Approach (At Z = -20m, X = 470m)
      const tex2 = createHighwayGantryTexture(
        1024, 384,
        "🛣️ NH-44 EXPRESSWAY THROUGH",
        ["⬆️ THROUGH TRAFFIC KEEP STRAIGHT", "⬆️ PANIPAT / KARNAL / AMBALA"],
        "⭐ VIP / CEREMONIAL EXIT",
        ["⭐ GATE 2 (STAGE DAIS / S.C.)", "⚠️ PROTOCOL PASS REQUIRED", "🚫 NO GENERAL ADMISSION"]
      );
      const gantry2 = buildGantryStructure(470, -20, 0, tex2);
      layerGroups.externalRoads.add(gantry2);

      // 3. North Approach (Southbound at Z = -650m, X = 280m)
      const tex3 = createHighwayGantryTexture(
        1024, 384,
        "🛣️ NH-44 / AH1 SOUTHBOUND THROUGH",
        ["⬇️ DELHI          72 km", "⬇️ SONIPAT        28 km", "⬇️ IGI AIRPORT    85 km"],
        "↘️ EXIT (SERVICE ROAD)",
        ["🚪 GATE 3 (NORTH GATEWAY)", "🅿️ PARKING P4 / P5", "🍲 MEGA LANGAR GROUND C"]
      );
      const gantry3 = buildGantryStructure(280, -650, Math.PI, tex3);
      layerGroups.externalRoads.add(gantry3);
    }
"""

    html = html.replace(m1_target, helper_code)
    print("Marker 1 replaced successfully.")

    # Marker 2: Replace cat === 'EXTERNAL_ROAD'
    m2_old = """          // 5. EXTERNAL ROADS & HIGHWAYS (NH-44)
          else if (cat === 'EXTERNAL_ROAD') {
            const coords = geom.coordinates;
            const pts = coords.map(c => {
              const w = geoToWorld(c[1], c[0]);
              return new THREE.Vector3(w.x, 1.1, w.z);
            });
            const isTrunk = p.highway_type === 'trunk';

            const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
            const lineMat = new THREE.LineBasicMaterial({
              color: isTrunk ? 0xf59e0b : 0x38bdf8,
              linewidth: isTrunk ? 4 : 2
            });
            const line = new THREE.Line(lineGeo, lineMat);
            layerGroups.externalRoads.add(line);
          }"""
    assert m2_old in html, "m2_old not found"

    m2_new = """          // 5. EXTERNAL ROADS & HIGHWAYS (NH-44 / GRAND TRUNK ROAD)
          else if (cat === 'EXTERNAL_ROAD') {
            const coords = geom.coordinates;
            const isTrunk = (p.highway_type === 'trunk');
            const isTrunkLink = (p.highway_type === 'trunk_link');
            const isBridge = (p.bridge === 'yes' || fid.includes('FLYOVER'));

            const pts = coords.map(c => {
              const w = geoToWorld(c[1], c[0]);
              const yVal = getHighwayElevation(w.z, isBridge);
              return new THREE.Vector3(w.x, yVal, w.z);
            });

            if (isTrunk) {
              const roadWidth = 14.0; // 3 lanes divided carriageway

              // Collect points for dynamic traffic splines
              if (pts[0].z > pts[pts.length - 1].z) {
                // Moving North (Z decreasing)
                pts.forEach(pt => {
                  if (!collectedNorthboundPts.some(cp => cp.distanceTo(pt) < 1.0)) {
                    collectedNorthboundPts.push(pt.clone());
                  }
                });
              } else {
                // Moving South (Z increasing)
                pts.forEach(pt => {
                  if (!collectedSouthboundPts.some(cp => cp.distanceTo(pt) < 1.0)) {
                    collectedSouthboundPts.push(pt.clone());
                  }
                });
              }

              // Asphalt deck ribbon
              const asphaltMesh = buildRoadRibbonMesh(pts, roadWidth, (z) => getHighwayElevation(z, isBridge), {
                color: 0x1f242d,
                roughness: 0.88,
                metalness: 0.08
              });
              asphaltMesh.userData = { ...p, feature_id: fid };
              interactiveObjects.push(asphaltMesh);
              layerGroups.externalRoads.add(asphaltMesh);

              // Surface markings: Outer solid white, Inner solid yellow, Dashed lane dividers
              const outerWhitePts = getRibbonOffsetPoints(pts, roadWidth, 0.03, (z) => getHighwayElevation(z, isBridge), 0.03);
              const outerWhiteLine = buildRoadRibbonMesh(outerWhitePts, 0.35, (z) => getHighwayElevation(z, isBridge) + 0.03, { color: 0xffffff, roughness: 0.5 });
              layerGroups.externalRoads.add(outerWhiteLine);

              const innerYellowPts = getRibbonOffsetPoints(pts, roadWidth, 0.97, (z) => getHighwayElevation(z, isBridge), 0.03);
              const innerYellowLine = buildRoadRibbonMesh(innerYellowPts, 0.35, (z) => getHighwayElevation(z, isBridge) + 0.03, { color: 0xfacc15, roughness: 0.5 });
              layerGroups.externalRoads.add(innerYellowLine);

              [0.333, 0.666].forEach(alpha => {
                const lanePts = getRibbonOffsetPoints(pts, roadWidth, alpha, (z) => getHighwayElevation(z, isBridge), 0.03);
                const lGeo = new THREE.BufferGeometry().setFromPoints(lanePts);
                const lMat = new THREE.LineDashedMaterial({ color: 0xffffff, dashSize: 4.5, gapSize: 4.5, linewidth: 2 });
                const lMesh = new THREE.Line(lGeo, lMat);
                lMesh.computeLineDistances();
                layerGroups.externalRoads.add(lMesh);
              });

              // Central Concrete Jersey Barrier with anti-glare screen along inner edge
              const barrierGroup = createJerseyBarrierMesh(pts, roadWidth, 1.0, (z) => getHighwayElevation(z, isBridge));
              layerGroups.externalRoads.add(barrierGroup);

              // Outer Galvanized Steel Guardrails along outer shoulder
              const guardrailGroup = createGuardrailMesh(pts, roadWidth, 0.0, (z) => getHighwayElevation(z, isBridge));
              layerGroups.externalRoads.add(guardrailGroup);

              // Median streetlights spaced every ~45m
              const medianPts = getRibbonOffsetPoints(pts, roadWidth, 1.0, (z) => getHighwayElevation(z, isBridge), 0.0);
              let cumDist = 0;
              for (let i = 0; i < medianPts.length - 1; i++) {
                const segLen = medianPts[i].distanceTo(medianPts[i + 1]);
                if (cumDist === 0 || cumDist >= 45.0) {
                  const light = createStreetlightGroup();
                  light.position.set(medianPts[i].x, medianPts[i].y, medianPts[i].z);
                  const dir = new THREE.Vector3().subVectors(medianPts[i + 1], medianPts[i]).normalize();
                  light.rotation.y = Math.atan2(dir.x, dir.z);
                  layerGroups.externalRoads.add(light);
                  cumDist = 0;
                }
                cumDist += segLen;
              }

              // Elevated Flyover Support Piers & Parapets
              if (isBridge) {
                // Parapet walls on deck outer edge
                const parapetMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.6 });
                const parapetPts = getRibbonOffsetPoints(pts, roadWidth, 0.0, (z) => getHighwayElevation(z, isBridge), 0.0);
                for (let i = 0; i < parapetPts.length - 1; i++) {
                  const p1 = parapetPts[i];
                  const p2 = parapetPts[i + 1];
                  if (p1.y > 2.5 && p2.y > 2.5) {
                    const len = p1.distanceTo(p2);
                    const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
                    const dir = new THREE.Vector3().subVectors(p2, p1).normalize();
                    const pMesh = new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.15, len), parapetMat);
                    pMesh.position.set(mid.x, mid.y + 0.57, mid.z);
                    pMesh.rotation.y = Math.atan2(dir.x, dir.z);
                    layerGroups.externalRoads.add(pMesh);
                  }
                }

                // Cylindrical bridge piers with crossheads underneath deck
                const pierMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.65 });
                const pierGeo = new THREE.CylinderGeometry(0.7, 0.7, 6.8, 12);
                const capGeo = new THREE.BoxGeometry(roadWidth - 1.0, 1.0, 2.2);

                for (let i = 0; i < pts.length; i++) {
                  const pt = pts[i];
                  if (pt.y > 5.5) {
                    // Twin columns
                    const cap = new THREE.Mesh(capGeo, pierMat);
                    cap.position.set(pt.x, pt.y - 0.5, pt.z);
                    layerGroups.externalRoads.add(cap);

                    [-roadWidth * 0.25, roadWidth * 0.25].forEach(px => {
                      const pier = new THREE.Mesh(pierGeo, pierMat);
                      pier.position.set(pt.x + px, (pt.y - 1.0) / 2, pt.z);
                      layerGroups.externalRoads.add(pier);
                    });
                  }
                }
              }

              // Special handling for OSM-ROAD-228423351: generate parallel Southbound carriageway (+17m East)
              if (fid === 'OSM-ROAD-228423351') {
                const sbOffset = 17.0;
                const sbPts = pts.map(p => new THREE.Vector3(p.x + sbOffset, p.y, p.z));

                sbPts.forEach(pt => {
                  if (!collectedSouthboundPts.some(cp => cp.distanceTo(pt) < 1.0)) {
                    collectedSouthboundPts.push(pt.clone());
                  }
                });

                const sbMesh = buildRoadRibbonMesh(sbPts, roadWidth, (z) => getHighwayElevation(z, isBridge), {
                  color: 0x1f242d, roughness: 0.88, metalness: 0.08
                });
                sbMesh.userData = { ...p, feature_id: fid + "-SB", name: "Grand Trunk Road (Southbound Carriageway)" };
                interactiveObjects.push(sbMesh);
                layerGroups.externalRoads.add(sbMesh);

                const sbWhitePts = getRibbonOffsetPoints(sbPts, roadWidth, 0.03, (z) => getHighwayElevation(z, isBridge), 0.03);
                const sbWhiteLine = buildRoadRibbonMesh(sbWhitePts, 0.35, (z) => getHighwayElevation(z, isBridge) + 0.03, { color: 0xffffff, roughness: 0.5 });
                layerGroups.externalRoads.add(sbWhiteLine);

                const sbYellowPts = getRibbonOffsetPoints(sbPts, roadWidth, 0.97, (z) => getHighwayElevation(z, isBridge), 0.03);
                const sbYellowLine = buildRoadRibbonMesh(sbYellowPts, 0.35, (z) => getHighwayElevation(z, isBridge) + 0.03, { color: 0xfacc15, roughness: 0.5 });
                layerGroups.externalRoads.add(sbYellowLine);

                const sbGuardrail = createGuardrailMesh(sbPts, roadWidth, 0.0, (z) => getHighwayElevation(z, isBridge));
                layerGroups.externalRoads.add(sbGuardrail);
              }

            } else if (isTrunkLink) {
              // 7.5m Paved slip ramp connector
              const rampMesh = buildRoadRibbonMesh(pts, 7.5, (z) => getHighwayElevation(z, false), {
                color: 0x1f242d, roughness: 0.85
              });
              rampMesh.userData = { ...p, feature_id: fid };
              interactiveObjects.push(rampMesh);
              layerGroups.externalRoads.add(rampMesh);

              const edgeWhitePts = getRibbonOffsetPoints(pts, 7.5, 0.05, (z) => getHighwayElevation(z, false), 0.03);
              const edgeWhiteLine = buildRoadRibbonMesh(edgeWhitePts, 0.3, (z) => getHighwayElevation(z, false) + 0.03, { color: 0xffffff });
              layerGroups.externalRoads.add(edgeWhiteLine);

            } else {
              // 7.5m Paved service roads, tertiary roads, and village connectors
              const servMesh = buildRoadRibbonMesh(pts, 7.5, 1.1, {
                color: 0x2b323d, roughness: 0.9
              });
              servMesh.userData = { ...p, feature_id: fid };
              interactiveObjects.push(servMesh);
              layerGroups.externalRoads.add(servMesh);

              // Dashed center divider
              const cGeo = new THREE.BufferGeometry().setFromPoints(pts);
              const cMat = new THREE.LineDashedMaterial({ color: 0xffffff, dashSize: 4, gapSize: 4, linewidth: 2 });
              const cLine = new THREE.Line(cGeo, cMat);
              cLine.computeLineDistances();
              layerGroups.externalRoads.add(cLine);
            }
          }"""

    html = html.replace(m2_old, m2_new)
    print("Marker 2 (cat === 'EXTERNAL_ROAD') replaced successfully.")

    # Marker 3: Replace cat === 'PEDESTRIAN_INFRASTRUCTURE'
    m3_target = "          // 10. PEDESTRIAN FOOTBRIDGE OVER NH-44\n          else if (cat === 'PEDESTRIAN_INFRASTRUCTURE') {"
    assert m3_target in html, "m3_target not found"

    # Find the end of this block
    m3_end = html.find("          // 11. CIVIL INFRASTRUCTURE (FLYOVER, UNDERPASSES & SURROUNDINGS)", html.find(m3_target))
    assert m3_end > 0, "m3_end not found"

    m3_new = """          // 10. PEDESTRIAN FOOTBRIDGE SKYWALK OVER NH-44
          else if (cat === 'PEDESTRIAN_INFRASTRUCTURE') {
            const pts = geom.coordinates.map(c => {
              const w = geoToWorld(c[1], c[0]);
              return new THREE.Vector3(w.x, 7.0, w.z);
            });
            const p1 = pts[0];
            const p2 = pts[pts.length - 1];
            const bridgeLen = p1.distanceTo(p2);
            const bridgeMid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);

            // Elevated skywalk deck
            const deck = new THREE.Mesh(
              new THREE.BoxGeometry(bridgeLen, 0.8, 4.5),
              new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.8, roughness: 0.25 })
            );
            deck.position.set(bridgeMid.x, 7.0, bridgeMid.z);
            deck.userData = { ...p, feature_id: fid };
            interactiveObjects.push(deck);
            layerGroups.footbridge.add(deck);

            // Steel truss side cages with diagonal web members
            const trussMat = new THREE.MeshStandardMaterial({ color: 0x0369a1, metalness: 0.85, roughness: 0.2 });
            [-2.2, 2.2].forEach(sideZ => {
              const railTop = new THREE.Mesh(new THREE.BoxGeometry(bridgeLen, 0.25, 0.25), trussMat);
              railTop.position.set(bridgeMid.x, 9.4, bridgeMid.z + sideZ);
              layerGroups.footbridge.add(railTop);

              const railBot = new THREE.Mesh(new THREE.BoxGeometry(bridgeLen, 0.25, 0.25), trussMat);
              railBot.position.set(bridgeMid.x, 7.5, bridgeMid.z + sideZ);
              layerGroups.footbridge.add(railBot);

              // Vertical and diagonal truss struts every 6m
              const numBays = Math.floor(bridgeLen / 6.0);
              for (let b = 0; b <= numBays; b++) {
                const bx = p1.x + (p2.x - p1.x) * (b / numBays);
                const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.9, 6), trussMat);
                strut.position.set(bx, 8.45, bridgeMid.z + sideZ);
                layerGroups.footbridge.add(strut);
              }
            });

            // Translucent protective arched canopy roof
            const canopyGeo = new THREE.CylinderGeometry(2.4, 2.4, bridgeLen, 16, 1, false, 0, Math.PI);
            canopyGeo.rotateZ(Math.PI / 2);
            const canopyMat = new THREE.MeshStandardMaterial({
              color: 0x38bdf8, transparent: true, opacity: 0.65, roughness: 0.2, side: THREE.DoubleSide
            });
            const canopy = new THREE.Mesh(canopyGeo, canopyMat);
            canopy.position.set(bridgeMid.x, 9.4, bridgeMid.z);
            layerGroups.footbridge.add(canopy);

            // Heavy structural bridge piers
            const pierMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.6 });
            [p1.x, p1.x + (p2.x - p1.x) * 0.35, bridgeMid.x, p1.x + (p2.x - p1.x) * 0.75, p2.x].forEach(px => {
              const pier = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 7.0, 12), pierMat);
              pier.position.set(px, 3.5, bridgeMid.z);
              layerGroups.footbridge.add(pier);
            });

            // Terminal stair towers & switchback ramps
            [p1, p2].forEach(pt => {
              const tower = new THREE.Mesh(
                new THREE.BoxGeometry(9, 8.0, 9),
                new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 })
              );
              tower.position.set(pt.x, 4.0, pt.z);
              tower.userData = { ...p, feature_id: fid };
              interactiveObjects.push(tower);
              layerGroups.footbridge.add(tower);
            });

            // 3D Footbridge Badge
            const bridgeBadge = makeTextSprite("🚶 PEDESTRIAN OVERPASS SKYWALK (NH-44 / PARKING 5 ⇄ GATE 1)", {
              borderColor: '#00ff88',
              backgroundColor: 'rgba(6, 78, 59, 0.94)',
              textColor: '#ffffff',
              fontSize: 24,
              scaleFactor: 0.16
            });
            bridgeBadge.position.set(bridgeMid.x, 14, bridgeMid.z);
            layerGroups.labels.add(bridgeBadge);
          }\n\n"""

    html = html[:html.find(m3_target)] + m3_new + html[m3_end:]
    print("Marker 3 (PEDESTRIAN_INFRASTRUCTURE) replaced successfully.")

    # Marker 4: Replace cat === 'CIVIL_INFRASTRUCTURE'
    m4_target = "          // 11. CIVIL INFRASTRUCTURE (FLYOVER, UNDERPASSES & SURROUNDINGS)\n          else if (cat === 'CIVIL_INFRASTRUCTURE') {"
    assert m4_target in html, "m4_target not found"

    m4_end = html.find("          // 12. OPERATIONAL TRAFFIC CORRIDORS & EVACUATION PATHS", html.find(m4_target))
    assert m4_end > 0, "m4_end not found"

    m4_new = """          // 11. CIVIL INFRASTRUCTURE (FLYOVER, UNDERPASSES & SURROUNDINGS)
          else if (cat === 'CIVIL_INFRASTRUCTURE') {
            if (geom.type === 'Polygon') {
              if (fid === 'FEAT-PETROL-PUMP') {
                const coords = geom.coordinates[0];
                let cX = 0, cZ = 0;
                coords.forEach(pt => { const w = geoToWorld(pt[1], pt[0]); cX += w.x; cZ += w.z; });
                cX /= coords.length; cZ /= coords.length;

                // High-clearance illuminated commercial fuel canopy
                const canopyGeo = new THREE.BoxGeometry(42, 1.4, 28);
                const canopyMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.7, roughness: 0.2 });
                const canopy = new THREE.Mesh(canopyGeo, canopyMat);
                canopy.position.set(cX, 6.2, cZ);
                canopy.castShadow = true;
                layerGroups.campus.add(canopy);

                // 6 structural support pillars
                const pillarGeo = new THREE.CylinderGeometry(0.6, 0.6, 5.5, 8);
                const pillarMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.4 });
                [-14, 0, 14].forEach(px => {
                  [-8, 8].forEach(pz => {
                    const pil = new THREE.Mesh(pillarGeo, pillarMat);
                    pil.position.set(cX + px, 2.75, cZ + pz);
                    layerGroups.campus.add(pil);
                  });
                });

                // 4 modern fuel dispensing pump islands with digital price LED meters
                const islandMat = new THREE.MeshStandardMaterial({ color: 0x475569 });
                const pumpMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.3 });
                const pumpScreenMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x00f0ff, emissiveIntensity: 0.8 });
                [-10, 10].forEach(ix => {
                  [-5, 5].forEach(iz => {
                    const island = new THREE.Mesh(new THREE.BoxGeometry(6.0, 0.3, 2.0), islandMat);
                    island.position.set(cX + ix, 0.15, cZ + iz);
                    layerGroups.campus.add(island);

                    const pump = new THREE.Mesh(new THREE.BoxGeometry(1.4, 2.2, 0.8), pumpMat);
                    pump.position.set(cX + ix, 1.25, cZ + iz);
                    layerGroups.campus.add(pump);

                    const screen = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.4, 0.82), pumpScreenMat);
                    screen.position.set(cX + ix, 1.7, cZ + iz);
                    layerGroups.campus.add(screen);
                  });
                });

                // Forecourt asphalt slab
                const slabGeo = new THREE.BoxGeometry(50, 0.4, 36);
                const slabMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.8 });
                const slab = new THREE.Mesh(slabGeo, slabMat);
                slab.position.set(cX, 0.2, cZ);
                slab.userData = { ...p, feature_id: fid };
                interactiveObjects.push(slab);
                layerGroups.campus.add(slab);

                // Roadside tall price totem pole on highway shoulder
                const totemGroup = new THREE.Group();
                const pole = new THREE.Mesh(new THREE.BoxGeometry(0.6, 10, 0.6), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
                pole.position.y = 5.0;
                totemGroup.add(pole);
                const board = new THREE.Mesh(new THREE.BoxGeometry(2.8, 4.5, 0.8), new THREE.MeshStandardMaterial({ color: 0x0284c7 }));
                board.position.y = 7.5;
                totemGroup.add(board);
                totemGroup.position.set(cX + 24, 0, cZ);
                layerGroups.campus.add(totemGroup);

                // 3D Landmark Badge
                const ppBadge = makeTextSprite("⛽ COMMERCIAL FUEL & SERVICE STATION (NH-44)", {
                  borderColor: '#38bdf8', backgroundColor: 'rgba(2, 132, 199, 0.94)', textColor: '#ffffff', fontSize: 20
                });
                ppBadge.position.set(cX, 14, cZ);
                layerGroups.labels.add(ppBadge);
              } else {
                const coords = geom.coordinates[0];
                const shape = new THREE.Shape();
                coords.forEach((pt, idx) => {
                  const w = geoToWorld(pt[1], pt[0]);
                  if (idx === 0) shape.moveTo(w.x, -w.z);
                  else shape.lineTo(w.x, -w.z);
                });
                const polyGeo = new THREE.ExtrudeGeometry(shape, { depth: 7.0, bevelEnabled: false });
                const polyMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 });
                const polyMesh = new THREE.Mesh(polyGeo, polyMat);
                polyMesh.rotation.x = -Math.PI / 2;
                polyMesh.position.y = 0;
                polyMesh.castShadow = true;
                polyMesh.userData = { ...p, feature_id: fid };
                interactiveObjects.push(polyMesh);
                layerGroups.campus.add(polyMesh);
              }
            } else if (geom.type === 'LineString') {
              // FEAT-FLYOVER-NORTH: Elevated Flyover Deck & Badge
              const pts = geom.coordinates.map(c => {
                const w = geoToWorld(c[1], c[0]);
                return new THREE.Vector3(w.x, 6.8, w.z);
              });
              const midIdx = Math.floor(pts.length / 2);
              const badgePos = pts[midIdx];

              const flyoverBadge = makeTextSprite("🌉 PATTI KALYANA ELEVATED FLYOVER (NH-44 THROUGH TRAFFIC)", {
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(15, 23, 42, 0.94)',
                textColor: '#ffffff',
                fontSize: 22,
                scaleFactor: 0.16
              });
              flyoverBadge.position.set(badgePos.x, 16.0, badgePos.z);
              layerGroups.labels.add(flyoverBadge);

            } else if (geom.type === 'Point') {
              const w = geoToWorld(geom.coordinates[1], geom.coordinates[0]);

              if (fid === 'FEAT-UNDERPASS-SOUTH' || fid === 'FEAT-UNDERPASS-NORTH') {
                // 3D Concrete Vehicular Subway Tunnel Portal
                const portalG = new THREE.Group();
                const portalMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.7 });
                const hazardMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0x854d0e, emissiveIntensity: 0.5 });
                const darkMat = new THREE.MeshBasicMaterial({ color: 0x090d16 });

                // Outer portal box (16m wide, 5.6m high, 28m deep)
                const wallL = new THREE.Mesh(new THREE.BoxGeometry(2.0, 5.6, 28.0), portalMat);
                wallL.position.set(-8.0, 2.8, 0);
                portalG.add(wallL);

                const wallR = new THREE.Mesh(new THREE.BoxGeometry(2.0, 5.6, 28.0), portalMat);
                wallR.position.set(8.0, 2.8, 0);
                portalG.add(wallR);

                const roof = new THREE.Mesh(new THREE.BoxGeometry(18.0, 1.2, 28.0), portalMat);
                roof.position.set(0, 5.6, 0);
                portalG.add(roof);

                // Flared concrete wingwalls (30 degree splay)
                [-1, 1].forEach(side => {
                  const wing = new THREE.Mesh(new THREE.BoxGeometry(1.2, 5.6, 12.0), portalMat);
                  wing.rotation.y = side * (Math.PI / 6);
                  wing.position.set(side * 12.0, 2.8, -18.0);
                  portalG.add(wing);
                });

                // Clearance bar with warning sign
                const clearBar = new THREE.Mesh(new THREE.BoxGeometry(14.5, 0.6, 0.5), hazardMat);
                clearBar.position.set(0, 4.6, -14.2);
                portalG.add(clearBar);

                // Tunnel dark interior
                const tunnelVoid = new THREE.Mesh(new THREE.BoxGeometry(14.0, 4.6, 26.0), darkMat);
                tunnelVoid.position.set(0, 2.3, 0);
                portalG.add(tunnelVoid);

                // Concrete roadway through underpass
                const subRoad = new THREE.Mesh(new THREE.BoxGeometry(14.0, 0.4, 48.0), new THREE.MeshStandardMaterial({ color: 0x1f242d }));
                subRoad.position.set(0, 0.2, 0);
                portalG.add(subRoad);

                portalG.position.set(w.x, 0, w.z);
                portalG.userData = { ...p, feature_id: fid };
                interactiveObjects.push(wallL);
                layerGroups.tactical.add(portalG);

                const badgeTitle = (fid === 'FEAT-UNDERPASS-SOUTH')
                  ? "🚗 PANCHI GUJRAN VEHICULAR UNDERPASS (NH-44 SUBWAY)"
                  : "🚗 PATTI KALYANA / GATE 3 VEHICULAR SUBWAY";

                const underpassBadge = makeTextSprite(badgeTitle, {
                  borderColor: '#facc15',
                  backgroundColor: 'rgba(30, 41, 59, 0.94)',
                  textColor: '#fef08a',
                  fontSize: 22,
                  scaleFactor: 0.16
                });
                underpassBadge.position.set(w.x, 14.0, w.z);
                layerGroups.labels.add(underpassBadge);

              } else {
                const marker = new THREE.Mesh(
                  new THREE.CylinderGeometry(4, 4, 2, 12),
                  new THREE.MeshStandardMaterial({ color: 0xa855f7, roughness: 0.5 })
                );
                marker.position.set(w.x, 1, w.z);
                marker.userData = { ...p, feature_id: fid };
                interactiveObjects.push(marker);
                layerGroups.tactical.add(marker);
              }
            }
          }\n\n"""

    html = html[:html.find(m4_target)] + m4_new + html[m4_end:]
    print("Marker 4 (CIVIL_INFRASTRUCTURE) replaced successfully.")

    # Marker 5: Post-features loop: construct CatmullRom splines, build gantries, init traffic
    m5_target = "        // Generate 550 PCG Residential Tents City (Police Deployment Order Ground Truth)"
    assert m5_target in html, "m5_target not found"

    m5_code = """        // Build CatmullRom splines along verified highway corridors for dynamic traffic
        try {
          if (collectedNorthboundPts.length >= 2) {
            // Sort by Z descending (South to North)
            collectedNorthboundPts.sort((a, b) => b.z - a.z);
            curveNorthbound = new THREE.CatmullRomCurve3(collectedNorthboundPts, false, 'catmullrom', 0.15);
          }
          if (collectedSouthboundPts.length >= 2) {
            // Sort by Z ascending (North to South)
            collectedSouthboundPts.sort((a, b) => a.z - b.z);
            curveSouthbound = new THREE.CatmullRomCurve3(collectedSouthboundPts, false, 'catmullrom', 0.15);
          }

          // Build authentic NHAI destination gantries
          buildHighwayGantries();

          // Initialize realistic 3D highway traffic simulation
          initHighwayTraffic();
        } catch (trafficErr) {
          console.error("Warning initializing highway traffic & gantries:", trafficErr);
        }

        // Generate 550 PCG Residential Tents City (Police Deployment Order Ground Truth)"""

    html = html.replace(m5_target, m5_code)
    print("Marker 5 (Gantries & Traffic Init) replaced successfully.")

    # Marker 6: In animate(now), add updateHighwayTraffic
    m6_target = "      const currentTime = now || performance.now();\n      const dt = Math.min((currentTime - lastFrameTime) / 1000, 0.1);\n      lastFrameTime = currentTime;"
    assert m6_target in html, "m6_target not found"

    m6_code = """      const currentTime = now || performance.now();
      const dt = Math.min((currentTime - lastFrameTime) / 1000, 0.1);
      lastFrameTime = currentTime;

      // Update dynamic highway traffic simulation (NH-44)
      if (typeof updateHighwayTraffic === 'function') {
        updateHighwayTraffic(currentTime, dt);
      }"""

    html = html.replace(m6_target, m6_code)
    print("Marker 6 (Traffic Animation Update) replaced successfully.")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Successfully wrote upgraded index.html: {len(html)} bytes")

if __name__ == '__main__':
    main()
