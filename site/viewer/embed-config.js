// Shared, portable scene format for website and Framer embeds.
const limits={azimuth:[-180,180],elevation:[10,85],intensity:[0,7],fill:[0,1.5],warmth:[-1,1],shadow:[0,1],softness:[.3,6],roughness:[-1,1],metalness:[-1,1],explodeStrength:[0,1.5]};
export function normalizeScene(input={}){
 const state={};for(const [key,[min,max]]of Object.entries(limits)){const n=Number(input.state?.[key]);if(Number.isFinite(n))state[key]=Math.max(min,Math.min(max,n));}
 state.background=/^#[\da-f]{6}$/i.test(input.state?.background||'')?input.state.background:'#ebe9e2';state.follow=input.state?.follow!==false;state.spin=input.state?.spin===true;state.blastHold=false;
 const colors={};for(const [slot,color]of Object.entries(input.colors||{})){if(/^[a-z][a-z0-9-]{0,40}$/i.test(slot)&&/^#[\da-f]{6}$/i.test(color))colors[slot]=color;}
 const materials=Array.isArray(input.materials)?input.materials.filter(m=>typeof m?.name==='string').map(m=>{
  const p=m.pbrMetallicRoughness||{},base=p.baseColorFactor;
  return{name:m.name,pbrMetallicRoughness:{...(Array.isArray(base)&&base.length===4&&base.every(n=>typeof n==='number'&&Number.isFinite(n))?{baseColorFactor:base.map(n=>Math.max(0,Math.min(1,n)))}:{}),...(Number.isFinite(p.roughnessFactor)?{roughnessFactor:Math.max(0,Math.min(1,p.roughnessFactor))}:{}),...(Number.isFinite(p.metallicFactor)?{metallicFactor:Math.max(0,Math.min(1,p.metallicFactor))}:{})}};
 }):[];
 const finite=(v,min,max)=>Number.isFinite(Number(v))?Math.max(min,Math.min(max,Number(v))):0;
 return{version:1,id:typeof input.id==='string'?input.id:'rangefinder-camera',label:typeof input.label==='string'?input.label:'Interactive 3D object',theme:input.theme==='dark'?'dark':'light',transparent:input.transparent!==false,motion:['still','hover','loop'].includes(input.motion)?input.motion:'hover',state,materials,colors,view:{yaw:finite(input.view?.yaw,-Math.PI*4,Math.PI*4),pitch:finite(input.view?.pitch,-1.1,1.1)}};
}
export function libraryURL(value){const url=new URL(value);if(!['http:','https:'].includes(url.protocol)||url.username||url.password)throw Error('Enter an HTTP or HTTPS library address.');url.search='';url.hash='';if(!url.pathname.endsWith('/'))url.pathname+='/';return url;}
export function embedURL(base,scene){const url=new URL('embed.html',libraryURL(base));url.hash=new URLSearchParams({scene:JSON.stringify(normalizeScene(scene))}).toString();return url.href;}
export function sceneFromHash(hash){return normalizeScene(JSON.parse(new URLSearchParams(hash.replace(/^#/, '')).get('scene')||'{}'));}
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function iframeMarkup(base,scene){return `<iframe src="${escape(embedURL(base,scene))}" title="${escape(scene.label)}" width="480" height="480" style="width:100%;height:100%;border:0;background:transparent" loading="lazy"></iframe>`;}
