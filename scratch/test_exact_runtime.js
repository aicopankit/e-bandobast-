const fs = require('fs');
const THREE = require('../three.min.js');

const geojson = JSON.parse(fs.readFileSync('nirankari_samalkha_ebandobast.geojson', 'utf8'));
const html = fs.readFileSync('index.html', 'utf8');

// Environment setup
const scene = new THREE.Scene();
const REF_LAT = 29.17931;
const REF_LON = 77.02491;
const M_PER_DEG_LAT = 110852.0;
const M_PER_DEG_LON = 97192.0;

function geoToWorld(lat, lon) {
  const x = (lon - REF_LON) * M_PER_DEG_LON;
  const z = -(lat - REF_LAT) * M_PER_DEG_LAT;
  return { x, z };
}

function worldToGeo(x, z) {
  const lon = REF_LON + (x / M_PER_DEG_LON);
  const lat = REF_LAT - (z / M_PER_DEG_LAT);
  return { lat, lon };
}

const layerGroups = {
  boundary: new THREE.Group(),
  groundA: new THREE.Group(),
  groundB: new THREE.Group(),
  groundC: new THREE.Group(),
  groundD: new THREE.Group(),
  pandal: new THREE.Group(),
  campus: new THREE.Group(),
  internalRoads: new THREE.Group(),
  externalRoads: new THREE.Group(),
  railway: new THREE.Group(),
  tactical: new THREE.Group(),
  parking: new THREE.Group(),
  footbridge: new THREE.Group(),
  tents: new THREE.Group(),
  routes: new THREE.Group(),
  sat: new THREE.Group()
};

const interactiveObjects = [];
const pcgRoadSegments = [];
const pcgExclusionPolygons = [];
const pcgSectorPolygons = {};

// Mock document for canvas text sprites
const document = {
  createElement: function(tag) {
    if (tag === 'canvas') {
      return {
        width: 0,
        height: 0,
        getContext: function() {
          return {
            font: '',
            fillStyle: '',
            strokeStyle: '',
            lineWidth: 0,
            textAlign: '',
            textBaseline: '',
            shadowColor: '',
            shadowBlur: 0,
            measureText: function(txt) { return { width: (txt || '').length * 10 }; },
            beginPath: function() {},
            roundRect: function() {},
            fill: function() {},
            stroke: function() {},
            fillText: function() {}
          };
        }
      };
    }
    return {};
  },
  getElementById: function() {
    return {
      style: {},
      innerText: '',
      innerHTML: '',
      classList: { add: ()=>{}, remove: ()=>{}, toggle: ()=>{}, contains: ()=>false }
    };
  }
};

const window = {
  innerWidth: 1920,
  innerHeight: 1080,
  devicePixelRatio: 1,
  addEventListener: ()=>{}
};

// Extract lines 826 to 1492 (the fetch callback body)
const lines = html.split('\n');
// Let's find exactly lines where fetch begins and ends
const fetchStartLine = lines.findIndex(l => l.includes("fetch('nirankari_samalkha_ebandobast.geojson')"));
const tentFnLine = lines.findIndex(l => l.includes("function generateProceduralTentCity()"));
const setCamLine = lines.findIndex(l => l.includes("function setCameraView("));

console.log("Lines:", { fetchStartLine, tentFnLine, setCamLine });

const fetchCallbackLines = lines.slice(fetchStartLine + 2, tentFnLine - 25);
// tentFn is lines tentFnLine to setCamLine
const tentFnLines = lines.slice(tentFnLine, setCamLine);

console.log("Extracted lines: fetchCallback =", fetchCallbackLines.length, "tentFn =", tentFnLines.length);

const fullCode = `
  ${tentFnLines.join('\n')}

  const data = geojson;
  ${fetchCallbackLines.join('\n')}
`;

try {
  const fn = new Function(
    'THREE', 'geojson', 'scene', 'layerGroups', 'interactiveObjects',
    'pcgRoadSegments', 'pcgExclusionPolygons', 'pcgSectorPolygons',
    'geoToWorld', 'worldToGeo', 'REF_LAT', 'REF_LON', 'M_PER_DEG_LAT', 'M_PER_DEG_LON',
    'document', 'window',
    fullCode
  );
  fn(
    THREE, geojson, scene, layerGroups, interactiveObjects,
    pcgRoadSegments, pcgExclusionPolygons, pcgSectorPolygons,
    geoToWorld, worldToGeo, REF_LAT, REF_LON, M_PER_DEG_LAT, M_PER_DEG_LON,
    document, window
  );
  console.log("SUCCESS! All features and procedural tents generated without error!");
  console.log("Interactive objects count:", interactiveObjects.length);
  console.log("PCG Road segments:", pcgRoadSegments.length);
  console.log("PCG Exclusion polygons:", pcgExclusionPolygons.length);
  console.log("PCG Sector polygons keys:", Object.keys(pcgSectorPolygons));
  let totalChildren = 0;
  Object.entries(layerGroups).forEach(([k, g]) => {
    console.log("Group", k, "children:", g.children.length);
    totalChildren += g.children.length;
  });
  console.log("Total 3D objects in layer groups:", totalChildren);
} catch (err) {
  console.error("ERROR during execution:", err);
}
