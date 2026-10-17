const fs = require('fs');
const out = fs.readFileSync('scratch/chrome_out.txt', 'utf8');
const search = (tag) => {
  let idx = 0;
  while (true) {
    idx = out.indexOf(tag, idx);
    if (idx === -1) break;
    console.log('--- ' + tag + ' at ' + idx + ' ---');
    console.log(out.substring(idx - 20, idx + 200));
    idx += tag.length;
  }
};
search('cursor-coords');
search('scale-bar-text');
