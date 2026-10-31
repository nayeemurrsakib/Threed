import {ObjectRenderer} from './renderer.js?v=0.8.0-offscreen';
import {sceneFromHash} from './embed-config.js?v=1';
const canvas=document.querySelector('#object'),status=document.querySelector('#status');
let engine,loopTimer,loadVersion=0,scene;
const catalog=fetch('catalog.json').then(r=>{if(!r.ok)throw Error('The library catalog could not load.');return r.json();});
async function load(){
 const version=++loadVersion;clearInterval(loopTimer);
 try{
  scene=sceneFromHash(location.hash);document.documentElement.dataset.theme=scene.theme;canvas.setAttribute('aria-label',`${scene.label}. Drag or use arrow keys to rotate. Home resets the view.`);status.hidden=false;status.textContent='Loading object…';
  const {assets}=await catalog;if(version!==loadVersion)return;const asset=assets.find(a=>a.id===scene.id);if(!asset)throw Error('This object is not in the library.');
  if(!engine)engine=new ObjectRenderer(canvas);engine.set({...scene.state,explodeOnHover:false,explodeHold:false,blastHold:false});engine.transparent=scene.transparent;
  if(!await engine.load(asset.model)||version!==loadVersion)return;
  for(const saved of scene.materials){const material=engine.materials.find(m=>m.name===saved.name);if(material)Object.assign(material.pbrMetallicRoughness,saved.pbrMetallicRoughness);}
  engine.palette(scene.colors);engine.baseYaw=engine.targetYaw=engine.yaw=scene.view.yaw;engine.basePitch=engine.targetPitch=engine.pitch=scene.view.pitch;
  engine.set({explodeOnHover:scene.motion==='hover',explodeHold:false,...(scene.motion==='still'?{follow:false,spin:false}:{})});
  if(scene.motion==='loop'){
   const started=performance.now();let previous;
   const cycle=()=>{const active=!engine.reduced.matches&&!document.hidden&&(performance.now()-started)%6400<3800;if(active!==previous){engine.set({explodeHold:active});previous=active;}};cycle();loopTimer=setInterval(cycle,120);
  }
  status.hidden=true;canvas.dataset.ready='true';canvas.dataset.motion=scene.motion;canvas.dataset.transparent=String(scene.transparent);document.title=`${asset.name} — threed®`;
 }catch(error){status.hidden=false;status.textContent=error.message;canvas.dataset.ready='error';}
}
window.addEventListener('hashchange',load);window.addEventListener('pagehide',event=>{if(!event.persisted){clearInterval(loopTimer);engine?.dispose();}});load();
