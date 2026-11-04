const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

async function main() {
  console.log('Testing live UI interactivity in Chrome...');
  const chromeProc = spawn(
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--disable-gpu',
      '--window-size=1920,1080',
      '--no-first-run',
      '--no-default-browser-check',
      'about:blank'
    ]
  );

  await new Promise(r => setTimeout(r, 2000));

  const tabs = await new Promise((resolve) => {
    http.get('http://127.0.0.1:9222/json', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    });
  });

  const pageTab = tabs.find(t => t.url.includes('about:blank') || t.url.includes('8090')) || tabs[0];
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
      if (msg.params.type === 'error') errors.push(text);
      else logs.push(text);
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      const desc = msg.params.exceptionDetails.exception ? msg.params.exceptionDetails.exception.description : msg.params.exceptionDetails.text;
      errors.push(desc);
      console.error('[PAGE ERROR]', desc);
    }
  };

  await new Promise(r => ws.onopen = r);
  await send('Runtime.enable');
  await send('Page.enable');

  console.log('Navigating to http://127.0.0.1:8090/ ...');
  await send('Page.navigate', { url: 'http://127.0.0.1:8090/' });
  await new Promise(r => setTimeout(r, 3500));

  // Check center element & canvas
  const centerRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const centerEl = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
      const canvas = document.querySelector('canvas');
      return {
        centerTag: centerEl ? centerEl.tagName + (centerEl.id ? '#' + centerEl.id : '') + (centerEl.className ? '.' + centerEl.className : '') : 'none',
        canvasExists: !!canvas,
        canvasWidth: canvas ? canvas.width : 0,
        canvasHeight: canvas ? canvas.height : 0
      };
    })()`,
    returnByValue: true
  });
  console.log('Center Element & Canvas:', centerRes.result.value);

  // Test Clicking "Physics" Tab
  const clickPhysics = await send('Runtime.evaluate', {
    expression: `(() => {
      const tab = Array.from(document.querySelectorAll('.se-nav-tab')).find(t => t.innerText.includes('Physics'));
      if (tab) {
        tab.click();
        const backdrop = document.getElementById('se-modal-backdrop');
        const title = document.getElementById('se-modal-title');
        return {
          clicked: true,
          modalOpen: backdrop ? backdrop.classList.contains('open') : false,
          modalTitle: title ? title.innerText : null
        };
      }
      return { clicked: false, tabsCount: document.querySelectorAll('.se-nav-tab').length };
    })()`,
    returnByValue: true
  });
  console.log('Clicked Physics Tab Result:', clickPhysics.result.value);

  // Close modal
  await send('Runtime.evaluate', {
    expression: `(() => {
      const closeBtn = document.getElementById('se-modal-close');
      if (closeBtn) closeBtn.click();
    })()`
  });

  // Test Clicking Mission Control "Pause" / "Resume"
  const clickMissionControl = await send('Runtime.evaluate', {
    expression: `(() => {
      const btnPause = document.getElementById('se-btn-pause');
      const btnResume = document.getElementById('se-btn-resume');
      let paused = false;
      if (btnPause) {
        btnPause.click();
        paused = btnPause.classList.contains('active');
      }
      return { btnPauseExists: !!btnPause, paused };
    })()`,
    returnByValue: true
  });
  console.log('Clicked Pause Result:', clickMissionControl.result.value);

  // Test View Modes "Earth View"
  const clickViewMode = await send('Runtime.evaluate', {
    expression: `(() => {
      const earthTile = document.querySelector('.se-view-tile[data-mode="base"]');
      if (earthTile) {
        earthTile.click();
        return {
          clicked: true,
          cameraMode: typeof cameraMode !== 'undefined' ? cameraMode : null,
          cameraPos: typeof camera !== 'undefined' ? [Math.round(camera.position.x), Math.round(camera.position.y), Math.round(camera.position.z)] : null
        };
      }
      return { clicked: false };
    })()`,
    returnByValue: true
  });
  console.log('Clicked Earth View Tile Result:', clickViewMode.result.value);

  // Test View Modes "Full System"
  const clickFull = await send('Runtime.evaluate', {
    expression: `(() => {
      const fullTile = document.querySelector('.se-view-tile[data-mode="full"]');
      if (fullTile) {
        fullTile.click();
        return {
          clicked: true,
          cameraMode: typeof cameraMode !== 'undefined' ? cameraMode : null,
          cameraPos: typeof camera !== 'undefined' ? [Math.round(camera.position.x), Math.round(camera.position.y), Math.round(camera.position.z)] : null
        };
      }
      return { clicked: false };
    })()`,
    returnByValue: true
  });
  console.log('Clicked Full System Tile Result:', clickFull.result.value);

  // Take screenshot of live interactive dashboard
  const screenshot = await send('Page.captureScreenshot', { format: 'png' });
  if (screenshot && screenshot.data) {
    fs.writeFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\final_dashboard_live.png', Buffer.from(screenshot.data, 'base64'));
    console.log('Saved live screenshot to final_dashboard_live.png');
  }

  ws.close();
  chromeProc.kill();
  console.log('All tests completed. Total errors:', errors.length);
}

main().catch(console.error);
