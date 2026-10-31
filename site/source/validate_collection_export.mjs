// Round-trip all actual master files through the same exporter used by the studio.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=await fs.readFile(path.join(root,'viewer/renderer.js'),'utf8');
const {ObjectRenderer}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const catalog=JSON.parse(await fs.readFile(path.join(root,'catalog.json'),'utf8'));
let transparent=0;
for(const asset of catalog.assets){
  const bytes=await fs.readFile(path.join(root,asset.model));
  const original=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength);
  const length=new DataView(original).getUint32(12,true);
  const document=JSON.parse(new TextDecoder().decode(new Uint8Array(original,20,length)));
  const renderer=Object.create(ObjectRenderer.prototype);
  Object.assign(renderer,{original,document,materials:structuredClone(document.materials),binOffset:28+length,state:{roughness:-1,metalness:-1}});
  for(const material of document.materials)renderer.color(material.name,'#a4b3dd');
  const exported=await renderer.glb().arrayBuffer();
  const view=new DataView(exported);assert.equal(view.getUint32(8,true),exported.byteLength);
  const result=JSON.parse(new TextDecoder().decode(new Uint8Array(exported,20,view.getUint32(12,true))));
  assert.deepEqual(result.meshes.map(m=>m.extras),document.meshes.map(m=>m.extras));
  assert.deepEqual(result.accessors,document.accessors);
  assert.equal(result.extras.qualityStandard,'camera-craft-v1');
  for(const [i,material] of result.materials.entries()){
    const before=document.materials[i];
    assert.equal(material.pbrMetallicRoughness.baseColorFactor[3],before.pbrMetallicRoughness.baseColorFactor[3]);
    assert.equal(material.alphaMode,before.alphaMode);
    if(material.alphaMode==='BLEND')transparent++;
  }
  // A finish override must survive as well, without changing the master file.
  renderer.state={roughness:.42,metalness:.17};
  const overridden=await renderer.glb().arrayBuffer();
  const ov=new DataView(overridden);const od=JSON.parse(new TextDecoder().decode(new Uint8Array(overridden,20,ov.getUint32(12,true))));
  for(const material of od.materials){assert.equal(material.pbrMetallicRoughness.roughnessFactor,.42);assert.equal(material.pbrMetallicRoughness.metallicFactor,.17);}
}
const report={models:catalog.assetCount,recolorRoundTrips:catalog.assetCount,finishRoundTrips:catalog.assetCount,alphaMaterialsPreserved:transparent,assemblyMetadataPreserved:true,accessorsPreserved:true};
await fs.writeFile(path.join(root,'reports/validation/EXPORT-VALIDATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
