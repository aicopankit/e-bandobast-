const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function run() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu-sandbox',
    '--enable-webgl',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--user-data-dir=e:\\e bando bast plan\\scratch\\chrome_dbg_user4'
  ]);

  await new Promise(r => setTimeout(r, 2000));
  const targets = await new Promise((res, rej) => http.get('http://127.0.0.1:9225/json', r => {
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
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  };
  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Page.navigate', { url: 'http://localhost:8000/index.html' });
  await new Promise(r => setTimeout(r, 3000));

  // Switch to Tents
  await send('Runtime.evaluate', { expression: "setCameraView('tents')" });
  await new Promise(r => setTimeout(r, 1200));

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('scratch/render_tents.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved render_tents.png successfully');

  ws.close();
  chrome.kill();
}
run().catch(console.error);
