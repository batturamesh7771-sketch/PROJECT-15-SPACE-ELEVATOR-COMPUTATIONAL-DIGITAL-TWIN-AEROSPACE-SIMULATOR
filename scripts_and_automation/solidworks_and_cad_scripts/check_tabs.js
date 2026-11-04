const { spawn } = require('child_process');
const http = require('http');

async function check() {
  const chromeProc = spawn(
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      'http://127.0.0.1:8090/'
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

  console.log('Tabs:', tabs.map(t => ({ title: t.title, url: t.url })));
  chromeProc.kill();
}

check();
