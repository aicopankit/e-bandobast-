const fs = require('fs');
const geo = JSON.parse(fs.readFileSync('nirankari_samalkha_ebandobast.geojson', 'utf8'));

// Mock Three.js minimally
const THREE = {
  Shape: function() { this.moveTo = ()=>{}; this.lineTo = ()=>{}; this.closePath = ()=>{}; this.getPoints = ()=>([{x:0,y:0},{x:1,y:1}]); },
  ShapeGeometry: function() {},
  MeshBasicMaterial: function() {},
  MeshStandardMaterial: function() {},
  LineBasicMaterial: function() {},
  LineDashedMaterial: function() {},
  Mesh: function() { this.position = { set: ()=>{} }; this.rotation = {}; },
  Line: function() { this.computeLineDistances = ()=>{}; },
  BufferGeometry: function() { this.setFromPoints = ()=>{}; this.computeLineDistances = ()=>{}; },
  Vector3: function(x,y,z) {
    this.x = x || 0; this.y = y || 0; this.z = z || 0;
    this.subVectors = function(a,b) { return new THREE.Vector3(a.x-b.x, a.y-b.y, a.z-b.z); };
    this.cross = function() { return this; };
    this.normalize = function() { return this; };
    this.multiplyScalar = function() { return this; };
    this.add = function() { return this; };
    this.clone = function() { return new THREE.Vector3(this.x, this.y, this.z); };
  },
  CubicBezierCurve3: function() { this.getPoints = ()=>([{x:0,y:0},{x:1,y:1}]); },
  ExtrudeGeometry: function() { this.center = ()=>{}; },
  CylinderGeometry: function() {},
  PlaneGeometry: function() {},
  BoxGeometry: function() {},
  ConeGeometry: function() {},
  CircleGeometry: function() {},
  Group: function() { this.add = ()=>{}; this.position = { set: ()=>{} }; },
  CatmullRomCurve3: function() {},
  TubeGeometry: function() {},
  Color: function() {},
  InstancedMesh: function() { this.setMatrixAt = ()=>{}; this.setColorAt = ()=>{}; this.instanceMatrix = { needsUpdate: false }; }
};

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
const REF_LAT = 29.17931;
const REF_LON = 77.02491;
const M_PER_DEG_LAT = 110852.0;
const M_PER_DEG_LON = 97192.0;

function geoToWorld(lat, lon) {
  const x = (lon - REF_LON) * M_PER_DEG_LON;
  const z = -(lat - REF_LAT) * M_PER_DEG_LAT;
  return { x, z };
}

const pcgRoadSegments = [];
const pcgExclusionPolygons = [];
const pcgSectorPolygons = {};

const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/data\.features\.forEach\(feat => \{([\s\S]*?)\}\);\s*\/\/\s*Generate 550 PCG/);
if (!match) {
  console.error('Could not match loop!');
  process.exit(1);
}

const loopBody = match[1];
const fn = new Function('geo', 'THREE', 'layerGroups', 'interactiveObjects', 'pcgRoadSegments', 'pcgExclusionPolygons', 'pcgSectorPolygons', 'geoToWorld', 'REF_LAT', 'REF_LON', 'M_PER_DEG_LAT', 'M_PER_DEG_LON', 'data', `
  data.features.forEach((feat, idx) => {
    try {
      ${loopBody}
    } catch(err) {
      console.error('Error on feature index ' + idx + ' (id: ' + feat.id + '):', err);
      throw err;
    }
  });
`);

try {
  fn(geo, THREE, layerGroups, interactiveObjects, pcgRoadSegments, pcgExclusionPolygons, pcgSectorPolygons, geoToWorld, REF_LAT, REF_LON, M_PER_DEG_LAT, M_PER_DEG_LON, geo);
  console.log('Features loop passed successfully! Total features processed:', geo.features.length);
} catch(e) {
  console.error('FAILED in loop:', e);
}
