// Exports project + news data from assets/*.js to JSON for tools/build.py
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.join(__dirname,'..');
const ctx={window:{}};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root,'assets/projects.js'),'utf8'),ctx);
const js=fs.readFileSync(path.join(root,'assets/pud.js'),'utf8');
const a=js.indexOf('const NEWS=['),b=js.indexOf('].map(n=>Object.assign',a);
const NEWS=vm.runInNewContext('('+js.slice(a+11,b+1)+')');
fs.writeFileSync(path.join(__dirname,'data.json'),JSON.stringify({projects:ctx.window.PUD_PROJECTS,news:NEWS}));
console.log(ctx.window.PUD_PROJECTS.length,'projects',NEWS.length,'news');
