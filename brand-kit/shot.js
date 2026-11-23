// usage: node shot.js <page.html> t1 t2 ...  -> f<t>.jpg previews
const {chromium}=require('playwright');const path=require('path');
(async()=>{const [,,page,...ts]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(page));await p.waitForTimeout(900);for(const t of ts){await p.evaluate(t=>frame(t),+t);await p.waitForTimeout(120);await p.screenshot({path:'f'+t+'.jpg',type:'jpeg',quality:80});}await b.close();})();
