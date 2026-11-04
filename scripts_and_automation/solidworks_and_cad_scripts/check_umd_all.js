const fs = require('fs');
const matCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\materials_environment.js', 'utf8');
console.log('Top 25 lines of materials_environment.js:');
console.log(matCode.split('\n').slice(0, 25).join('\n'));
console.log('Bottom 15 lines:');
console.log(matCode.split('\n').slice(-15).join('\n'));

const orbCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\orbital_missions.js', 'utf8');
console.log('Top 25 lines of orbital_missions.js:');
console.log(orbCode.split('\n').slice(0, 25).join('\n'));
console.log('Bottom 15 lines:');
console.log(orbCode.split('\n').slice(-15).join('\n'));
