const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function testVerification() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9228',
    '--disable-gpu-sandbox',
    '--enable-webgl',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--user-data-dir=e:\\e bando bast plan\\scratch\\chrome_dbg_user_steps'
  ]);

  await new Promise(r => setTimeout(r, 2000));
  const targets = await new Promise((res, rej) => http.get('http://127.0.0.1:9228/json', r => {
    let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d)));
  }).on('error', rej));

  const page = targets.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 1;
  const pending = new Map();
  function send(method, params = {}) {
    return new Promise(r => {
      const msgId = id++;
      pending.set(msgId, r);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }
  const consoleLogs = [];
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.method === 'Runtime.consoleAPICalled') {
      consoleLogs.push(m.params.args.map(a => a.value || a.description).join(' '));
    }
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  };
  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Page.navigate', { url: 'http://localhost:8000/index.html' });
  await new Promise(r => setTimeout(r, 3500));

  // Check feature count and tent count
  const evalInfo = await send('Runtime.evaluate', {
    expression: `(function() {
      return JSON.stringify({
        campusChildren: layerGroups.campus.children.length,
        pandalChildren: layerGroups.pandal.children.length,
        tentsCount: layerGroups.tents.children.length,
        exclusionCount: pcgExclusionPolygons.length,
        labelsCount: layerGroups.labels.children.length
      });
    })()`
  });
  console.log("Scene Metrics:", evalInfo.result.value);

  // Switch to pandal view and capture
  await send('Runtime.evaluate', { expression: "setCameraView('pandal')" });
  await new Promise(r => setTimeout(r, 1200));
  const shotPandal = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scratch/render_realigned_pandal.png', Buffer.from(shotPandal.data, 'base64'));

  // Switch to campus view and capture
  await send('Runtime.evaluate', { expression: "setCameraView('campus')" });
  await new Promise(r => setTimeout(r, 1200));
  const shotCampus = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scratch/render_realigned_campus.png', Buffer.from(shotCampus.data, 'base64'));

  // Switch to overview
  await send('Runtime.evaluate', { expression: "setCameraView('overview')" });
  await new Promise(r => setTimeout(r, 1200));
  const shotOverview = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scratch/render_realigned_overview.png', Buffer.from(shotOverview.data, 'base64'));

  console.log("Console errors/warnings count:", consoleLogs.filter(l => l.includes('Error') || l.includes('error')).length);

  ws.close();
  chrome.kill();
  console.log("CDP Verification finished successfully!");
}

testVerification().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
