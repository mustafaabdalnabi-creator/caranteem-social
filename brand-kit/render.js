// usage: node render.js <page.html> <out.mp4>   (page must define window.TOTAL and frame(t))
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [,,page,out]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('file://'+path.resolve(page));await p.waitForTimeout(900);
const T=await p.evaluate(()=>window.TOTAL);const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p',out+'.tmp.mp4']);
const n=Math.round(T*30);for(let i=0;i<n;i++){await p.evaluate(t=>frame(t),i/30);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));require('fs').renameSync(out+'.tmp.mp4',out);if(errs.length)console.log(errs.slice(0,3));await b.close();console.log('done',T);})();
