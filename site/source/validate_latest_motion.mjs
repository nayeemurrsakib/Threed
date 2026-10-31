import fs from 'node:fs/promises';import path from 'node:path';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const moduleFrom=async p=>import('data:text/javascript;base64,'+Buffer.from(await fs.readFile(path.join(root,p),'utf8')).toString('base64'));
const {assemblyTransform}=await moduleFrom('viewer/renderer.js');const {smileLift,smileStrength}=await moduleFrom('viewer/brand-expression.js');
async function load(file){const b=await fs.readFile(path.join(root,file));const jl=b.readUInt32LE(12),doc=JSON.parse(b.subarray(20,20+jl));const acc=i=>{const a=doc.accessors[i],v=doc.bufferViews[a.bufferView];return new Float32Array(b.buffer,b.byteOffset+28+jl+(v.byteOffset||0)+(a.byteOffset||0),a.count*3);};return{doc,acc};}
const mat=(mesh,time=0,amount=.85)=>assemblyTransform({kinematics:mesh.extras.motion,explosion:mesh.extras.explosionOffset,motion:amount},time);
const speaker=await load('models/bookshelf-speaker.glb');const moving=speaker.doc.meshes.filter(m=>m.extras.layer==='Vibrating speaker cone');assert.equal(moving.length,3,'Cone, dust cap and surround must pulse together');
for(const t of [0,.08,.19,.33])for(const m of moving)assert.deepEqual([...mat(m,t)],[...mat(moving[0],t)]);
for(const m of speaker.doc.meshes.filter(m=>/Rounded speaker cabinet|Acoustic baffle|Cabinet feet|Woofer basket/.test(m.extras.layer)))assert.equal(mat(m,.33)[14],0);
assert.notEqual(mat(moving[0],.08)[14],mat(moving[0],.19)[14]);
const scale=await load('models/kitchen-scale.glb');assert(scale.doc.extras.presentation.restartMotionOnActivate);const platform=scale.doc.meshes.filter(m=>m.extras.layer==='Weighing platform');assert(platform.length>=2);
const resting=platform[0].extras.motion.translate[1];assert(resting<0);assert(Math.abs(mat(platform[0],.3)[13]-resting)>.001);assert(Math.abs(mat(platform[0],3)[13]-resting)<1e-6);assert.equal(mat(platform[0],0,0)[13],0);
for(const m of platform)assert.deepEqual([...mat(m,.3)],[...mat(platform[0],.3)]);
const cap=await load('models/sun-cap.glb');const bill=cap.doc.meshes.find(m=>m.name==='attached-curved-bill-with-solid-edge'),band=cap.doc.meshes.find(m=>m.name==='attached-inner-sweatband');assert(bill&&band);
const bp=cap.acc(bill.primitives[0].attributes.POSITION),sp=cap.acc(band.primitives[0].attributes.POSITION);let low=Infinity,high=-Infinity;
for(let i=1;i<sp.length;i+=3){low=Math.min(low,sp[i]);high=Math.max(high,sp[i]);}
const row=73,rows=25,face=row*rows;
for(let side=0;side<2;side++)for(let i=0;i<row;i++){const y=bp[(side*face+i)*3+1];assert(y>=low&&y<=high,'The bill root must sit within the sewn sweatband');}
for(let side=0;side<2;side++)for(const edge of [0,row-1])for(let j=1;j<rows;j++)for(let k=0;k<3;k++)assert.equal(bp[(side*face+j*row+edge)*3+k],bp[(side*face+edge)*3+k],'Bill tips must taper into the crown instead of ending in square tabs');
const logo=await load('assets/brand/ee-soft-keys.glb');let minimumJacobian=Infinity;
for(const m of logo.doc.meshes){const p=logo.acc(m.primitives[0].attributes.POSITION),n=logo.acc(m.primitives[0].attributes.NORMAL);for(let i=0;i<p.length;i+=3){const x=p[i],y=p[i+1],e=.001,dy=(smileLift(x,y+e)-smileLift(x,y-e))/(2*e);minimumJacobian=Math.min(minimumJacobian,1+dy);assert(Number.isFinite(y+smileLift(x,y)));assert(Math.abs(Math.hypot(n[i],n[i+1],n[i+2])-1)<.001);assert(y+smileLift(x,y)>=-.00001);}}
assert(minimumJacobian>.2,'Smile deformation must not fold the surface');assert.equal(smileStrength(1,1,true),0);assert(smileStrength(1,1)>smileStrength(1,0));
const report={speakerConeDustCapSurroundTogether:true,cabinetFixed:true,scaleDipsAndSettles:true,scaleReplaysOnActivation:true,capRootSeatedInSweatband:true,capTipsTapered:true,smileMinimumJacobian:minimumJacobian,reducedMotionSmileOff:true};await fs.writeFile(path.join(root,'reports/validation/LATEST-MOTION-VALIDATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
