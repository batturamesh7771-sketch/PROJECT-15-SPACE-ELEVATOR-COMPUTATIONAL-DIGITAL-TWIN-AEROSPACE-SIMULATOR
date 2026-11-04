const fs = require('fs');
const physCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\physics_engine.js', 'utf8');
console.log('Top 20 lines of physics_engine.js:');
console.log(physCode.split('\n').slice(0, 25).join('\n'));
console.log('Bottom 20 lines:');
console.log(physCode.split('\n').slice(-25).join('\n'));
