const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function main() {
  console.log('Starting headless Chrome...');
  const chromeProc = spawn(
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--disable-gpu',
      '--window-size=1920,1080',
      '--no-first-run',
      '--no-default-browser-check',
      'http://127.0.0.1:8090/'
    ]
  );

  await new Promise(r => setTimeout(r, 2000));

  function getTabs() {
    return new Promise((resolve, reject) => {
      http.get('http://127.0.0.1:9222/json', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      }).on('error', reject);
    });
  }

  const tabs = await getTabs();
  const pageTab = tabs.find(t => t.url.includes('8090'));
  if (!pageTab) {
    console.error('Target tab not found:', tabs);
    chromeProc.kill();
    return;
  }

  console.log('Connecting to DevTools WS:', pageTab.webSocketDebuggerUrl);
  const ws = new WebSocket(pageTab.webSocketDebuggerUrl);

  let msgId = 1;
  const pending = new Map();

  function send(method, params = {}) {
    return new Promise((resolve) => {
      const id = msgId++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  const logs = [];
  const errors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const resolve = pending.get(msg.id);
      pending.delete(msg.id);
      resolve(msg.result);
    }

    if (msg.method === 'Runtime.consoleAPICalled') {
      const text = msg.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
      console.log(`[CONSOLE ${msg.params.type.toUpperCase()}] ${text}`);
      if (msg.params.type === 'error') errors.push(text);
      else logs.push(text);
    }

    if (msg.method === 'Runtime.exceptionThrown') {
      const desc = msg.params.exceptionDetails.exception ? msg.params.exceptionDetails.exception.description : msg.params.exceptionDetails.text;
      console.error(`[EXCEPTION THROWN] ${desc}`);
      errors.push(desc);
    }
  };

  await new Promise((resolve) => { ws.onopen = resolve; });

  await send('Runtime.enable');
  await send('Console.enable');
  await send('Page.enable');

  console.log('Reloading page to capture initial logs and exceptions...');
  await send('Page.reload');

  // Wait 3.5 seconds for scripts and loading timeout to settle
  await new Promise(r => setTimeout(r, 3500));

  // Evaluate state inside the browser
  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const canvas = document.querySelector('canvas');
      const loader = document.getElementById('loader-overlay');
      const hud = document.getElementById('se-hud-overlay');
      const centerEl = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
      
      return {
        hasCanvas: !!canvas,
        canvasWidth: canvas ? canvas.width : 0,
        canvasHeight: canvas ? canvas.height : 0,
        loaderDisplay: loader ? window.getComputedStyle(loader).display : 'none',
        loaderOpacity: loader ? window.getComputedStyle(loader).opacity : '0',
        loaderPointerEvents: loader ? window.getComputedStyle(loader).pointerEvents : '',
        hudDisplay: hud ? window.getComputedStyle(hud).display : 'none',
        hudPointerEvents: hud ? window.getComputedStyle(hud).pointerEvents : '',
        centerElement: centerEl ? centerEl.outerHTML.slice(0, 200) : 'none',
        centerElementTag: centerEl ? centerEl.tagName + (centerEl.id ? '#' + centerEl.id : '') + (centerEl.className ? '.' + centerEl.className : '') : 'none',
        cameraMode: typeof cameraMode !== 'undefined' ? cameraMode : 'undefined',
        cameraPos: typeof camera !== 'undefined' ? [camera.position.x, camera.position.y, camera.position.z] : null,
        controlsTarget: typeof controls !== 'undefined' ? [controls.target.x, controls.target.y, controls.target.z] : null,
        earthPos: typeof earthGroup !== 'undefined' ? [earthGroup.position.x, earthGroup.position.y, earthGroup.position.z] : null,
        tetherPos: typeof tetherMesh !== 'undefined' ? [tetherMesh.position.x, tetherMesh.position.y, tetherMesh.position.z] : null,
        climberPos: typeof climberNode !== 'undefined' ? [climberNode.position.x, climberNode.position.y, climberNode.position.z] : null,
        spaceElevatorUIDefined: typeof window.SpaceElevatorUI !== 'undefined',
        physicsEngineDefined: typeof window.SpaceElevatorPhysics !== 'undefined'
      };
    })()`,
    returnByValue: true
  });

  console.log('Browser Evaluation Result:');
  console.log(JSON.stringify(evalRes.result.value, null, 2));

  // Capture screenshot
  const screenshot = await send('Page.captureScreenshot', { format: 'png' });
  if (screenshot && screenshot.data) {
    fs.writeFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\browser_snapshot.png', Buffer.from(screenshot.data, 'base64'));
    console.log('Saved screenshot to browser_snapshot.png');
  }

  ws.close();
  chromeProc.kill();
  console.log('Inspection complete. Total errors found:', errors.length);
}

main().catch(console.error);
