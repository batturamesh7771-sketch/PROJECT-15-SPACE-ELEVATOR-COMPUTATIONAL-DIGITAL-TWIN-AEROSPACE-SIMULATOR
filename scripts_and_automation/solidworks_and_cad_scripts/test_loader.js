const { spawn } = require('child_process');
const http = require('http');

async function test() {
  const chromeProc = spawn(
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--disable-gpu',
      '--window-size=1920,1080',
      'http://127.0.0.1:8090/'
    ]
  );

  await new Promise(r => setTimeout(r, 1500));

  const tabs = await new Promise((resolve) => {
    http.get('http://127.0.0.1:9222/json', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    });
  });

  const pageTab = tabs.find(t => t.url.includes('8090'));
  const ws = new WebSocket(pageTab.webSocketDebuggerUrl);

  let id = 1;
  const send = (method, params = {}) => new Promise((resolve) => {
    const curId = id++;
    const handler = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id === curId) {
        ws.removeEventListener('message', handler);
        resolve(msg.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });

  await new Promise(r => ws.onopen = r);
  await send('Runtime.enable');

  // Let's check what's going on with loader-overlay right now
  const res = await send('Runtime.evaluate', {
    expression: `(() => {
      const overlay = document.getElementById('loader-overlay');
      return {
        overlayExists: !!overlay,
        styleOpacity: overlay ? overlay.style.opacity : null,
        styleDisplay: overlay ? overlay.style.display : null,
        computedOpacity: overlay ? window.getComputedStyle(overlay).opacity : null,
        computedDisplay: overlay ? window.getComputedStyle(overlay).display : null,
        loadedModels: typeof loadedModels !== 'undefined' ? loadedModels : null
      };
    })()`,
    returnByValue: true
  });

  console.log('Loader status after 1.5s:', res.result.value);

  // Wait another 2 seconds
  await new Promise(r => setTimeout(r, 2000));
  const res2 = await send('Runtime.evaluate', {
    expression: `(() => {
      const overlay = document.getElementById('loader-overlay');
      return {
        styleOpacity: overlay ? overlay.style.opacity : null,
        styleDisplay: overlay ? overlay.style.display : null,
        computedOpacity: overlay ? window.getComputedStyle(overlay).opacity : null,
        computedDisplay: overlay ? window.getComputedStyle(overlay).display : null
      };
    })()`,
    returnByValue: true
  });

  console.log('Loader status after 3.5s:', res2.result.value);

  ws.close();
  chromeProc.kill();
}

test().catch(console.error);
