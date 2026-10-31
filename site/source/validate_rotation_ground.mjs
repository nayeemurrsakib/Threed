import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=await fs.readFile(path.join(root,'viewer/renderer.js'),'utf8');
const {assemblyTransform,studioModel,stageGroundHeight,pageCurvature}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const multiply=(a,b)=>{const out=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)out[c*4+r]+=a[k*4+r]*b[c*4+k];return out;};
const catalog=JSON.parse(await fs.readFile(path.join(root,'catalog.json'),'utf8'));
let scenarios=0,reproducedOldKeyboardClip=false;
for(const asset of catalog.assets){
 const bytes=await fs.readFile(path.join(root,asset.model));const length=bytes.readUInt32LE(12),doc=JSON.parse(bytes.subarray(20,20+length));
 const parts=[];
 for(const mesh of doc.meshes)for(const primitive of mesh.primitives){
  const acc=doc.accessors[primitive.attributes.POSITION],view=doc.bufferViews[acc.bufferView];
  const positions=new Float32Array(bytes.buffer,bytes.byteOffset+28+length+(view.byteOffset||0)+(acc.byteOffset||0),acc.count*3);
  parts.push({positions,kinematics:mesh.extras.motion,explosion:mesh.extras.explosionOffset,blastOffset:mesh.extras.blastOffset});
 }
 const cy=asset.dimensions[1]*.48;
 for(const pitch of [-1.1,-.6,0,.6,1.1])for(const yaw of [0,1.5])for(const pose of ["rest","hover","blast"]){
  const amount=pose==='hover'?.85:0;
  const model=studioModel(pitch,yaw,cy);
  // Rotating around the object center must not shift that center.
  assert(Math.abs(model[5]*cy+model[13]-cy)<1e-6);
  for(const p of parts){p.motion=amount;p.blast=pose==='blast'?1:0;p.transform=multiply(model,assemblyTransform(p,2));}
  const ground=stageGroundHeight(parts,model);assert(Number.isFinite(ground));
  let minY=Infinity;
  for(const p of parts){const v=p.positions,m=p.transform,curve=pageCurvature(p);for(let i=0;i<v.length;i+=3){
   const bend=curve[2]*Math.sin(Math.PI*Math.max(0,Math.min(1,(v[i]-curve[0])/curve[1])))*curve[3];
   minY=Math.min(minY,m[1]*v[i]+m[5]*(v[i+1]+bend)+m[9]*v[i+2]+m[13]);
  }}
  assert(ground<=minY+1e-6,`${asset.id}: floor intersects the rotated geometry`);
  if(pitch===0&&pose==='rest')assert(Math.abs(ground)<1e-5);
  if(asset.id==='mechanical-keyboard'&&pitch===1.1&&pose==='rest'&&minY<-.015)reproducedOldKeyboardClip=true;
  if(asset.id==='little-rocket'&&pitch===0&&amount===.85)assert(Math.abs(ground)<1e-5,'Launch must retain its resting ground plane');
  scenarios++;
 }
}
assert(reproducedOldKeyboardClip,'The regression must include the reported keyboard failure');
const report={models:catalog.assetCount,rotatedPoses:scenarios,oldKeyboardFailureReproduced:true,floorBelowAllRotatedVertices:true,orbitCenterStable:true,rocketRetainsLaunchClearance:true};
await fs.writeFile(path.join(root,'reports/validation/ROTATION-VALIDATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
