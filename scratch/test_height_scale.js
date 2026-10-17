const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function testScale() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--disable-gpu-sandbox',
    '--enable-webgl',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--user-data-dir=e:\\e bando bast plan\\scratch\\chrome_dbg_user_scale'
  ]);

  await new Promise(r => setTimeout(r, 2000));
  const targets = await new Promise((res, rej) => http.get('http://127.0.0.1:9226/json', r => {
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

  // Check initial scale (should be 1.8)
  const evalInitial = await send('Runtime.evaluate', {
    expression: `JSON.stringify({
      campusScaleY: layerGroups.campus.scale.y,
      pandalScaleY: layerGroups.pandal.scale.y,
      tentsScaleY: layerGroups.tents.scale.y,
      badgeText: document.getElementById('vertical-scale-badge').innerText,
      sliderVal: document.getElementById('vertical-scale-slider').value
    })`
  });
  console.log("Initial state:", evalInitial.result.value);

  // Switch camera to campus view
  await send('Runtime.evaluate', { expression: "setCameraView('campus')" });
  await new Promise(r => setTimeout(r, 1200));

  // Test setVerticalScale(2.5)
  const evalScaled = await send('Runtime.evaluate', {
    expression: `(function() {
      setVerticalScale(2.5);
      return JSON.stringify({
        campusScaleY: layerGroups.campus.scale.y,
        pandalScaleY: layerGroups.pandal.scale.y,
        tentsScaleY: layerGroups.tents.scale.y,
        badgeText: document.getElementById('vertical-scale-badge').innerText,
        sliderVal: document.getElementById('vertical-scale-slider').value
      });
    })()`
  });
  console.log("After setVerticalScale(2.5):", evalScaled.result.value);

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scratch/render_scaled_campus.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved render_scaled_campus.png successfully');

  console.log("Console errors/warnings count:", consoleLogs.filter(l => l.includes('Error') || l.includes('error')).length);

  ws.close();
  chrome.kill();
}

testScale().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
