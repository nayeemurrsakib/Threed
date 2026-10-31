import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
// Import the browser ES module without changing the pack's package semantics.
const source=readFileSync(new URL('../viewer/embed-config.js',import.meta.url),'utf8');
const {normalizeScene,embedURL,sceneFromHash,iframeMarkup,libraryURL}=await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const scene={id:'rangefinder-camera',label:'Camera "&" <test>',theme:'dark',transparent:true,motion:'loop',view:{yaw:.8,pitch:-.2},state:{azimuth:-65,intensity:2.1,background:'#28302d',shadow:.7,explodeStrength:.85,blastHold:true},materials:[{name:'glass',pbrMetallicRoughness:{baseColorFactor:[.2,.3,.4,.08],roughnessFactor:.055,metallicFactor:.1}}],colors:{accent:'#f08040'}};
const normalized=normalizeScene(scene),url=embedURL('https://example.com/icons/',scene),decoded=sceneFromHash(new URL(url).hash);
assert.deepEqual(decoded,normalized);assert.equal(new URL(url).pathname,'/icons/embed.html');assert.equal(decoded.materials[0].pbrMetallicRoughness.baseColorFactor[3],.08);assert.equal(decoded.state.blastHold,false);assert.equal(decoded.view.yaw,.8);assert.equal(decoded.motion,'loop');
assert.equal(normalizeScene({state:{intensity:99,shadow:-4}}).state.intensity,7);assert.equal(normalizeScene({state:{shadow:-4}}).state.shadow,0);
assert.throws(()=>libraryURL('javascript:alert(1)'));assert.throws(()=>libraryURL('https://user:password@example.com/'));
const html=iframeMarkup('https://example.com/',scene);assert.ok(html.includes('Camera &quot;&amp;&quot; &lt;test&gt;'));assert.ok(!html.includes('<test>'));
const all=JSON.parse(readFileSync(new URL('../catalog.json',import.meta.url))).assets;
for(const asset of all){const result=sceneFromHash(new URL(embedURL('https://example.com/',{...scene,id:asset.id})).hash);assert.equal(result.id,asset.id);}
const result={sceneRoundTrip:true,glassAlphaPreserved:true,viewPreserved:true,explodedViewDisabled:true,unsafeURLRejected:true,escapedMarkup:true,modelIDs:all.length};
writeFileSync(new URL('../reports/validation/EMBED-VALIDATION.json',import.meta.url),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
