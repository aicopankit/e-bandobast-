const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function run() {
  console.log("Starting Chrome with remote debugging...");
  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  const chrome = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--disable-gpu-sandbox',
    '--enable-webgl',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=e:\\e bando bast plan\\scratch\\chrome_dbg_user'
  ]);

  // Wait 2 seconds for port 9222
  await new Promise(r => setTimeout(r, 2000));

  function getJson(url) {
    return new Promise((resolve, reject) => {
      http.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      }).on('error', reject);
    });
  }

  let targets = [];
  try {
    targets = await getJson('http://127.0.0.1:9222/json');
    console.log("Targets found:", targets.length);
  } catch(e) {
    console.error("Failed to connect to CDP:", e.message);
    chrome.kill();
    return;
  }

  const page = targets.find(t => t.type === 'page');
  if (!page) {
    console.error("No page target found");
    chrome.kill();
    return;
  }

  console.log("Connecting to WebSocket:", page.webSocketDebuggerUrl);
  const ws = new WebSocket(page.webSocketDebuggerUrl);

  let id = 1;
  const pending = new Map();
  function send(method, params = {}) {
    return new Promise((resolve) => {
      const msgId = id++;
      pending.set(msgId, resolve);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  const logs = [];
  const errors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id)(msg.result);
      pending.delete(msg.id);
    }
    if (msg.method === 'Console.messageAdded') {
      logs.push(msg.params.message);
      console.log("[CONSOLE]", msg.params.message.level, msg.params.message.text);
    }
    if (msg.method === 'Runtime.consoleAPICalled') {
      const args = msg.params.args.map(a => a.value || a.description).join(' ');
      console.log("[CONSOLE_API]", msg.params.type, args);
      logs.push({ type: msg.params.type, text: args });
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      console.error("[RUNTIME EXCEPTION]:", msg.params.exceptionDetails);
      errors.push(msg.params.exceptionDetails);
    }
  };

  await new Promise(r => ws.onopen = r);
  console.log("WebSocket connected. Enabling domains...");
  await send('Page.enable');
  await send('Console.enable');
  await send('Runtime.enable');
  await send('Log.enable');

  console.log("Navigating to http://localhost:8000/index.html ...");
  await send('Page.navigate', { url: 'http://localhost:8000/index.html' });

  // Wait 4 seconds for everything to load and render
  await new Promise(r => setTimeout(r, 4000));

  // Capture screenshot
  console.log("Capturing screenshot...");
  const screenshot = await send('Page.captureScreenshot', { format: 'png' });
  if (screenshot && screenshot.data) {
    fs.writeFileSync('scratch/real_render.png', Buffer.from(screenshot.data, 'base64'));
    console.log("Saved screenshot to scratch/real_render.png (size:", screenshot.data.length, "bytes)");
  } else {
    console.log("No screenshot data received");
  }

  // Check scene objects via Runtime.evaluate
  const evalRes = await send('Runtime.evaluate', {
    expression: `({
      objectsInScene: scene.children.length,
      layerChildren: Object.fromEntries(Object.entries(layerGroups).map(([k, g]) => [k, g.children.length])),
      camPos: camera.position,
      target: controls.target
    })`,
    returnByValue: true
  });
  console.log("Scene evaluation:", JSON.stringify(evalRes.result ? evalRes.result.value : evalRes, null, 2));

  ws.close();
  chrome.kill();
  console.log("Done! Total logs:", logs.length, "Errors:", errors.length);
}

run().catch(console.error);
