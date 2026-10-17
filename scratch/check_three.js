const fs = require('fs');
const s = fs.readFileSync('three.min.js', 'utf8');
console.log('File size:', s.length);
console.log('First 200 chars:', s.substring(0, 200));
const m = s.match(/REVISION:"([^"]+)"/);
console.log('Revision match:', m ? m[1] : 'none');
console.log('Has BufferAttribute:', s.includes('BufferAttribute'));
console.log('Has Float32BufferAttribute:', s.includes('Float32BufferAttribute'));
console.log('Has PCFSoftShadowMap:', s.includes('PCFSoftShadowMap'));
