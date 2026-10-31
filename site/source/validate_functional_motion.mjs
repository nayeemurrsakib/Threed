// Verify the requested relationships and frame-rate invariance, using actual assets.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=await fs.readFile(path.join(root,'viewer/renderer.js'),'utf8');
const {assemblyTransform,motionEmission,dampedStep}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const ids=JSON.parse(await fs.readFile(path.join(root,'catalog.json'),'utf8')).assets.map(a=>a.id);
const docs={};
const identity=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];
const matrix=(mesh,amount=.85,time=2)=>assemblyTransform({kinematics:mesh.extras.motion,explosion:mesh.extras.explosionOffset,motion:amount},time);
const near=(a,b,tolerance=1e-6)=>a.forEach((v,i)=>assert(Math.abs(v-b[i])<tolerance));
for(const id of ids){
 const bytes=await fs.readFile(path.join(root,'models',id+'.glb'));const d=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());docs[id]=d;
 assert(d.meshes.every(m=>m.extras.explosionOffset.every(v=>v===0)),id+' retains a generic explosion');
 for(const mesh of d.meshes)for(const amount of [0,.2,.5,.85,1.5])for(const time of [0,.23,2,7.9,12])assert(Array.from(matrix(mesh,amount,time)).every(Number.isFinite));
}
const fixed=(id,test)=>{const matches=docs[id].meshes.filter(test);assert(matches.length,id+' fixed parts were not found');for(const m of matches)near(matrix(m),identity);};
fixed('tape-dispenser',m=>/Fixed serrated cutter|Connected feed span|Weighted enamel base/.test(m.extras.layer));
assert(!docs['alarm-clock'].materials.some(m=>m.name==='glass'),'Clock must not contain the extra glass material');
fixed('sand-timer',m=>/Fixed turned frame|Fitted glass vessel/.test(m.extras.layer));
fixed('calculator',m=>/Closed calculator case|Recessed LCD/.test(m.extras.layer));
fixed('lidded-pot',m=>/Side handles|Hollow enamel body|Rolled rim/.test(m.extras.layer));
fixed('ribbon-gift',m=>m.extras.layer==='Satin ribbon');
fixed('delivery-parcel',m=>m.extras.layer==='Paper sealing tape');
fixed('receipt-printer',m=>m.extras.layer==='Closed printer enclosure');
fixed('camp-lantern',m=>m.extras.layer!=='Illuminated lantern diffuser');
for(const id of ['shopping-tote','sun-cap']){const first=matrix(docs[id].meshes[0]);for(const mesh of docs[id].meshes)near(matrix(mesh),first);}
assert(docs['two-slot-toaster'].meshes.some(m=>m.extras.layer==='Popping toast slice 1'));
assert(docs['two-slot-toaster'].meshes.some(m=>m.extras.layer==='Popping toast slice 2'));
assert(docs['fountain-pen'].meshes.some(m=>m.name==='hollow-pen-barrel-with-open-bore'));
assert(docs['portable-radio'].meshes.some(m=>m.name==='matching-radius-rounded-radio-front'));
assert(docs['web-camera'].meshes.some(m=>m.name==='fitted-dark-optical-front-window'));
const glow=docs['camp-lantern'].meshes.find(m=>m.extras.motion?.glow);assert(motionEmission({kinematics:glow.extras.motion,motion:.85},2)[0]>1);
const wave=docs.calculator.meshes.find(m=>m.extras.motion?.wave);assert.notDeepEqual(Array.from(matrix(wave,.85,.1)),Array.from(matrix(wave,.85,.5)));
const upper=docs['sand-timer'].meshes.find(m=>m.extras.layer==='Draining upper sand');assert(matrix(upper,.85,7)[0]<matrix(upper,.85,1)[0]);
const lower=docs['sand-timer'].meshes.find(m=>m.extras.layer==='Growing lower sand');assert(matrix(lower,.85,7)[0]>matrix(lower,.85,1)[0]);
const blender=docs['countertop-blender'];
assert(blender.meshes.some(m=>m.name==='closed-rounded-blender-motor-base'));
assert(blender.meshes.some(m=>m.name==='fitted-blender-base-top'));
const blade=blender.meshes.find(m=>m.extras.motion?.spin);
assert(blade);assert.notDeepEqual(Array.from(matrix(blade,.85,.1)),Array.from(matrix(blade,.85,.5)));
assert(docs['payment-terminal'].meshes.some(m=>m.extras.layer==='Sliding payment card'));
assert(docs['payment-terminal'].meshes.filter(m=>m.extras.layer.startsWith('Payment keys')).every(m=>m.extras.motion.wave));
for(const d of Object.values(docs))assert(d.meshes.some(m=>m.extras.motion),'Each object needs an explicit gesture');
// A late frame must not change the trajectory or cause a pop in the spring.
const run=steps=>{let p=0,v=0;for(const dt of steps)[p,v]=dampedStep(p,v,.85,dt);return [p,v];};
const reference=run(Array(60).fill(1/60));for(const hz of [30,90,144])near(run(Array(hz).fill(1/hz)),reference,1e-10);
near(run([.01,.04,.02,.03,...Array(30).fill(.03)]),reference,1e-10);
let [p,v]=dampedStep(0,0,.85,.2);for(let i=0;i<60;i++){[p,v]=dampedStep(p,v,0,1/60);assert(Number.isFinite(p)&&Number.isFinite(v));}assert(p<.00001);
const report={objects:ids.length,noGenericExplosions:true,fixedAttachments:true,frameRateInvariantSpring:true,continuousKeyWave:true,sandTransfersDownward:true,toasts:2,clockGlassRemoved:true,frontFitsAndPenBorePresent:true};
await fs.writeFile(path.join(root,'reports/validation/FUNCTIONAL-MOTION-VALIDATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
