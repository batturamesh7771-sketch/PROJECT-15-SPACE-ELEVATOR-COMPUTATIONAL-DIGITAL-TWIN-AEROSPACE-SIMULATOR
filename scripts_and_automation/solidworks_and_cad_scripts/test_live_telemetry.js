const { spawn } = require('child_process');
const http = require('http');

async function testTelemetry() {
  console.log('Testing Live Backend Telemetry Integration in Chrome...');
  const chromeProc = spawn(
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--user-data-dir=C:\\Users\\user\\AppData\\Local\\Temp\\chrome_test_profile_2',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      'http://127.0.0.1:8090/'
    ]
  );

  await new Promise(r => setTimeout(r, 2000));

  const tabs = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9222/json', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });

  const pageTab = tabs.find(t => t.url.includes('8090'));
  if (!pageTab) {
    console.error('Tab 8090 not found');
    chromeProc.kill();
    return;
  }
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

  await new Promise(r => ws.onopen = r);
  await send('Runtime.enable');
  await new Promise(r => setTimeout(r, 1000));

  // Query live DOM values
  const getValues = () => send('Runtime.evaluate', {
    expression: `(() => {
      return {
        altitude: document.getElementById('se-t-alt')?.innerText,
        effectiveG: document.getElementById('se-t-geff')?.innerText,
        coriolisF: document.getElementById('se-t-coriolis')?.innerText,
        tension: document.getElementById('se-t-tens')?.innerText,
        stress: document.getElementById('se-t-stress')?.innerText,
        c3: document.getElementById('se-t-c3')?.innerText,
        orbitalEscape: document.getElementById('se-orb-escape-val')?.innerText,
        orbitalMars: document.getElementById('se-orb-mars-val')?.innerText,
        orbitalC3: document.getElementById('se-orb-c3-val')?.innerText,
        envSolar: document.getElementById('se-env-solar-val')?.innerText,
        envDebris: document.getElementById('se-env-debris-val')?.innerText,
        envTemp: document.getElementById('se-env-temp-val')?.innerText,
        envRadiation: document.getElementById('se-env-rad-val')?.innerText,
        riskBadge: document.getElementById('se-risk-badge')?.innerText,
        tetherHealth: document.getElementById('se-health-pct')?.innerText,
        tetherMass: document.getElementById('se-deck-mass')?.innerText
      };
    })()`,
    returnByValue: true
  });

  const initialVals = await getValues();
  console.log('Telemetry at T=0:', initialVals.result.value);

  // Advance altitude to 60,000 km
  console.log('Simulating ascent to 60,000 km...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      climbAltitudeKm = 60000.0;
      nominalSpeedKmh = 450.0;
      climbDirection = 1;
    })()`
  });

  await new Promise(r => setTimeout(r, 600));

  const advancedVals = await getValues();
  console.log('Telemetry at 60,000 km (Super-GEO):', advancedVals.result.value);

  // Test Material Switch to Graphene
  console.log('Switching material to Graphene...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      const gTab = Array.from(document.querySelectorAll('.se-mat-tab')).find(t => t.innerText.includes('Graphene'));
      if (gTab) gTab.click();
    })()`
  });

  await new Promise(r => setTimeout(r, 400));

  const grapheneVals = await getValues();
  console.log('Telemetry with Graphene:', grapheneVals.result.value);

  ws.close();
  chromeProc.kill();
  console.log('Live Telemetry Verification Complete!');
}

testTelemetry().catch(console.error);
