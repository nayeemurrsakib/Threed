import {smileLift,smileStrength} from './brand-expression.js?v=0.7.1';
import {ObjectRenderer} from './renderer.js?v=0.8.0-offscreen';
// Brand motion is independent of object palette and studio interaction controls.
async function start(canvas){
 const link=canvas?.closest('.wordmark'),container=canvas?.parentElement;
 if(!canvas||!link)return;
 let renderer;
 try{
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  renderer=new ObjectRenderer(canvas,{follow:false,spin:false,explodeOnHover:false,explodeHold:!reduced.matches,explodeStrength:.3,shadow:0,intensity:1.8,fill:.45,warmth:.08});
  renderer.transparent=true;
  await renderer.load(new URL('../assets/brand/ee-soft-keys.glb',import.meta.url));
  installSmile(renderer,reduced,canvas);
  const theme=()=>{const dark=document.documentElement.dataset.theme==='dark';renderer.color('secondary','#d96b32');renderer.set({background:dark?'#161c19':'#f5f3ed'});};
  const greet=()=>{const active=!reduced.matches&&(link.matches(':hover')||document.activeElement===link);renderer.set({explodeHold:!reduced.matches,explodeStrength:active ? .85 : .3});renderer.targetYaw=0;renderer.targetPitch=0;renderer.invalidate();canvas.dataset.greeting=String(active);};
  for(const event of ['pointerenter','pointerleave','focus','blur'])link.addEventListener(event,greet);
  reduced.addEventListener('change',greet);
  const appearance=new MutationObserver(theme);appearance.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  theme();greet();container.dataset.ready='true';link.dataset.brandReady='true';
  window.addEventListener('pagehide',event=>{if(!event.persisted){appearance.disconnect();reduced.removeEventListener('change',greet);renderer.dispose();}},{once:true});
 }catch{renderer?.dispose();container.dataset.ready='fallback';}
}
for(const canvas of document.querySelectorAll('#brand-canvas,[data-brand-canvas]')){const begin=()=>start(canvas);if('requestIdleCallback' in window)requestIdleCallback(begin,{timeout:1200});else setTimeout(begin,0);}

// Deform the actual cutout lips and crescents, retaining correctly transformed normals.
function installSmile(renderer,reduced,canvas){
 const data=renderer.parts.map((part,i)=>{
  const mesh=renderer.document.meshes[i],acc=renderer.document.accessors[mesh.primitives[0].attributes.NORMAL],view=renderer.document.bufferViews[acc.bufferView];
  const normals=new Float32Array(renderer.original,renderer.binOffset+(view.byteOffset||0)+(acc.byteOffset||0),acc.count*3).slice();
  const base=part.positions.slice(),positions=base.slice(),posedNormals=normals.slice(),weight=new Float32Array(base.length/3),dx=weight.slice(),dy=weight.slice(),eps=.001;
  for(let j=0;j<weight.length;j++){const x=base[j*3],y=base[j*3+1];weight[j]=smileLift(x,y);dx[j]=(smileLift(x+eps,y)-smileLift(x-eps,y))/(2*eps);dy[j]=(smileLift(x,y+eps)-smileLift(x,y-eps))/(2*eps);}
  return{part,base,normals,positions,posedNormals,weight,dx,dy};
 });
 const originalRender=renderer.render.bind(renderer);
 renderer.render=()=>{
  const greeting=Math.max(0,Math.min(1,(renderer.explosion-.3)/.55));const amount=smileStrength(renderer.actionTime||0,greeting,reduced.matches);
  for(const d of data){for(let j=0;j<d.weight.length;j++){const i=j*3;d.positions[i+1]=d.base[i+1]+d.weight[j]*amount;const ny=d.normals[i+1]/(1+d.dy[j]*amount),nx=d.normals[i]-d.dx[j]*amount*ny,nz=d.normals[i+2],length=Math.hypot(nx,ny,nz);d.posedNormals[i]=nx/length;d.posedNormals[i+1]=ny/length;d.posedNormals[i+2]=nz/length;}
   const gl=renderer.gl;gl.bindBuffer(gl.ARRAY_BUFFER,d.part.buffers[0]);gl.bufferSubData(gl.ARRAY_BUFFER,0,d.positions);gl.bindBuffer(gl.ARRAY_BUFFER,d.part.buffers[1]);gl.bufferSubData(gl.ARRAY_BUFFER,0,d.posedNormals);
  }
  canvas.dataset.smile=amount.toFixed(2);originalRender();
 };
}
