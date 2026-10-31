import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=await fs.readFile(path.join(root,'viewer/renderer.js'),'utf8');
const {ObjectRenderer,assemblyTransform,dampedStep}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const catalog=JSON.parse(await fs.readFile(path.join(root,'catalog.json'),'utf8'));
let parts=0;
for(const asset of catalog.assets){
 const b=await fs.readFile(path.join(root,asset.model));const doc=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)));
 const vectors=new Set();
 for(const mesh of doc.meshes){
  const e=mesh.extras;assert.deepEqual(e.explosionOffset,[0,0,0]);assert(e.blastGroup?.length);
  assert(e.blastOffset?.length===3&&e.blastOffset.every(Number.isFinite));vectors.add(JSON.stringify(e.blastOffset));
  const p={explosion:e.explosionOffset,motion:0,spinPhase:0,kinematics:e.motion,blastOffset:e.blastOffset,blast:0};
  const before=assemblyTransform(p,0);p.blast=1;const after=assemblyTransform(p,0);
  for(let k=0;k<3;k++)assert(Math.abs(after[12+k]-before[12+k]-e.blastOffset[k])<1e-5);
  assert([...after].every(Number.isFinite));parts++;
 }
 assert(vectors.size>=2,asset.id+' needs distinct authored inspection offsets');
}
// Inspect defaults without creating a WebGL context.
assert(source.includes('blastHold:false'));
let p=0,v=0;for(let i=0;i<120;i++){[p,v]=dampedStep(p,v,1,1/60);assert(p>=0&&p<=1.000001);}assert(p>.9999);
for(let i=0;i<120;i++){[p,v]=dampedStep(p,v,0,1/60);assert(p>=-.000001&&p<=1);}assert(p<.0001);
const report={models:catalog.assets.length,parts,authoredInspectionOffsets:true,defaultHoverOffsetsZero:true,blastDefaultOff:true,interruptibleDamping:true,finiteTransforms:true};
await fs.writeFile(path.join(root,'reports/validation/BLAST-VALIDATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
