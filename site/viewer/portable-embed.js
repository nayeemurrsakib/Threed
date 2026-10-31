// A pasteable live object: renderer, edited mesh and settings travel together.
// No localhost/public asset URL is needed by the pasted result.
const escapeHTML=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const json=value=>JSON.stringify(value).replace(/</g,'\\u003c');
function base64(bytes){let text='';for(let i=0;i<bytes.length;i+=32768)text+=String.fromCharCode(...bytes.subarray(i,i+32768));return btoa(text);}
export async function portableEmbed(model,scene,rendererSource){
 let compressed=false,bytes=new Uint8Array(await model.arrayBuffer());
 if(typeof CompressionStream!=='undefined'){bytes=new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer());compressed=true;}
 const runtime=rendererSource.replace(/^export /gm,'');
 const script=`(async()=>{${runtime}
 const scene=${json(scene)},canvas=document.querySelector('#object'),status=document.querySelector('#status');let engine,timer;
 try{
  const bytes=Uint8Array.from(atob(${json(base64(bytes))}),c=>c.charCodeAt(0));
  let model=new Blob([bytes],{type:'model/gltf-binary'});
  if(${compressed}){if(typeof DecompressionStream==='undefined')throw Error('This browser cannot unpack the 3D model. Use the PNG instead.');model=new Blob([await new Response(model.stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer()],{type:'model/gltf-binary'});}
  engine=new ObjectRenderer(canvas,{...scene.state,blastHold:false,explodeOnHover:false,explodeHold:false});engine.transparent=scene.transparent!==false;
  const url=URL.createObjectURL(model);try{await engine.load(url);}finally{URL.revokeObjectURL(url);}
  engine.baseYaw=engine.targetYaw=engine.yaw=scene.view?.yaw||0;engine.basePitch=engine.targetPitch=engine.pitch=scene.view?.pitch||0;
  engine.set({explodeOnHover:scene.motion==='hover',explodeHold:false,...(scene.motion==='still'?{follow:false,spin:false}:{})});
  if(scene.motion==='loop'){const start=performance.now();let previous;const cycle=()=>{const active=!engine.reduced.matches&&!document.hidden&&(performance.now()-start)%6400<3800;if(active!==previous){engine.set({explodeHold:active});previous=active;}};cycle();timer=setInterval(cycle,120);}
  status.hidden=true;canvas.dataset.ready='true';canvas.dataset.motion=scene.motion;
 }catch(error){status.textContent=error.message;canvas.dataset.ready='error';}
 window.addEventListener('pagehide',()=>{clearInterval(timer);engine?.dispose();},{once:true});
 })();`;
 const doc=`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHTML(scene.label)} — threed®</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:transparent}canvas{display:block;width:100%;height:100%;touch-action:pan-y;cursor:grab}canvas:focus-visible{outline:2px solid #d96b32;outline-offset:-3px}#status{position:absolute;inset:0;display:grid;place-items:center;padding:24px;text-align:center;font:14px/1.5 Arial;color:${scene.theme==='dark'?'#e7e9df':'#29332d'}}[hidden]{display:none!important}</style><canvas id="object" role="img" tabindex="0" aria-label="${escapeHTML(scene.label)}. Drag or use arrow keys to rotate. Home resets the view."></canvas><div id="status" role="status">Loading object…</div><script>${script.replace(/<\/script/gi,'<\\/script')}</script></html>`;
 return `<iframe title="${escapeHTML(scene.label)} — threed®" srcdoc="${escapeHTML(doc)}" style="width:100%;height:100%;min-height:240px;border:0;display:block;background:transparent" loading="lazy"></iframe>`;
}
