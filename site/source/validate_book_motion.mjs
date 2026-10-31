import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=await fs.readFile(path.join(root,'viewer/renderer.js'),'utf8');
const {assemblyTransform,pageCurvature}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const apply=(m,p)=>[0,1,2].map(r=>m[r]*p[0]+m[4+r]*p[1]+m[8+r]*p[2]+m[12+r]);
const near=(a,b)=>a.forEach((v,i)=>assert(Math.abs(v-b[i])<1e-6));
const results=[];
for(const id of ['pocket-notebook','passport-wallet']){
  const bytes=await fs.readFile(path.join(root,'models',id+'.glb'));const length=bytes.readUInt32LE(12);
  const doc=JSON.parse(bytes.subarray(20,20+length).toString());
  assert(doc.meshes.every(m=>m.extras.explosionOffset.every(v=>v===0)),'A bound book must never use floating layer translations');
  const leaves=new Set();let frontCover=false;
  for(const mesh of doc.meshes){
    const k=mesh.extras.motion;if(!k)continue;
    const part={kinematics:k,explosion:mesh.extras.explosionOffset,motion:0};
    const pivot=k.pivot;const sample=[pivot[0]+.5,pivot[1],pivot[2]];
    near(apply(assemblyTransform(part),sample),sample);
    for(const amount of [.17,.425,.85,1.5]){
      part.motion=amount;const transform=assemblyTransform(part);
      near(apply(transform,pivot),pivot);near(apply(transform,[pivot[0],pivot[1],pivot[2]+.5]),[pivot[0],pivot[1],pivot[2]+.5]);
      assert(apply(transform,sample).every(Number.isFinite));
      if(k.page){const curve=pageCurvature(part);assert(curve[2]>0&&curve[3]>=0);assert.equal(curve[0],pivot[0]);leaves.add(mesh.extras.layer);}
    }
    if(mesh.extras.layer==='Front cover')frontCover=true;
  }
  assert(frontCover&&leaves.size===3);
  results.push({id,boundLeaves:leaves.size,spineInvariantAtFourProgressValues:true,translationFallbacks:0});
}
await fs.writeFile(path.join(root,'reports/validation/BOOK-MOTION-VALIDATION.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results,null,2));
