import {portableEmbed} from './portable-embed.js?v=1';
import {exportMenu,copyExportCode} from './export-menu.js?v=9-note';
import {ObjectRenderer,linearHex} from './renderer.js?v=0.9.0-light';
import {lightChip} from './chips.js?v=1';
import {GalleryColors} from './gallery-colors.js?v=0.7.1';
const galleryColors=new GalleryColors();
const portableRenderer=fetch(new URL('./renderer.js?v=0.9.0-light',import.meta.url)).then(r=>{if(!r.ok)throw Error('The 3D renderer could not load.');return r.text();});
const $=id=>document.getElementById(id);
let catalog,palettes,lights,engine,current,category='All',paletteName='Workshop',lightName='Softbox',loadVersion=0,toastTimer,loadTimer,customColors={};
const lightKeys=['azimuth','elevation','intensity','fill','warmth','shadow','softness'];
function toast(message){$('toast').textContent=message;$('toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('visible'),3000);}
function download(blob,name){if(!blob){toast('The export could not be created.');return;}const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);toast(`Saved ${name}`);}
function jsonDownload(data,name){download(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),name);}
function persist(){try{if(!current)return;localStorage.setItem('little-things-studio-v1',JSON.stringify({version:catalog.version,id:current.id,paletteName,customColors,lightName,state:engine.state,materials:engine.materials,view:{yaw:engine.baseYaw,pitch:engine.basePitch},finish:$('finish').value}));}catch{}}
function pressed(container,dataKey,value){container.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset[dataKey]===value)));}
function paintRange(input){const min=Number(input.min)||0,max=Number(input.max)||100;const percent=Math.max(0,Math.min(100,100*(Number(input.value)-min)/(max-min)));input.style.setProperty('--range-fill',percent+'%');}
function syncLightControls(){for(const key of lightKeys){$(key).value=engine.state[key];$(key+'-out').value=['azimuth','elevation'].includes(key)?`${Math.round(engine.state[key])}°`:Number(engine.state[key]).toFixed(key==='fill'||key==='warmth'||key==='shadow'?2:1);}pressed($('lights'),'light',lightName);document.querySelectorAll('input[type=range]').forEach(paintRange);}
function materialControls(){
 $('material-colors').replaceChildren();
 for(const slot of current.materialSlots){const material=engine.materials.find(m=>m.name===slot);if(!material)continue;const label=document.createElement('label');label.className='color-control chip-option';const input=document.createElement('input');input.type='color';input.value=linearHex(material.pbrMetallicRoughness.baseColorFactor);input.setAttribute('aria-label',`${slot} material color`);input.dataset.slot=slot;const text=document.createElement('span');text.className='color-name';text.textContent=slot;const hex=document.createElement('span');hex.className='color-hex';hex.textContent=input.value.toUpperCase();label.title=`Change ${slot} colour`;label.append(input,text,hex);$('material-colors').append(label);
  input.addEventListener('input',()=>{hex.textContent=input.value.toUpperCase();engine.color(slot,input.value);if(palettes[paletteName])customColors={...palettes[paletteName]};customColors[slot]=input.value;paletteName='Custom';pressed($('palettes'),'palette',paletteName);refreshGalleryColors();persist();});}
}
function thumbnail(asset){return palettes?.[paletteName]?`previews/palettes/${encodeURIComponent(paletteName)}/${asset.id}.png?v=${catalog.version}-${asset.bytes}`:(galleryColors.get(asset.id)||asset.thumbnail);}
function renderCustomGallery(){if(paletteName!=='Custom'){galleryColors.cancel();return;}galleryColors.update(catalog.assets,customColors,lights['Product studio'],(id,url)=>{if(paletteName==='Custom'){const image=$('gallery').querySelector(`[data-object="${id}"] img`);if(image)image.src=url;}});}
function refreshGalleryColors(){renderCustomGallery();for(const tile of $('gallery').querySelectorAll('[data-object]')){const asset=catalog.assets.find(a=>a.id===tile.dataset.object);if(asset)tile.querySelector('img').src=thumbnail(asset);}}
function gallery(){
 const query=$('search').value.toLowerCase().trim();const list=catalog.assets.filter(a=>(category==='All'||category===a.category)&&(`${a.name} ${a.description}`).toLowerCase().includes(query));$('count').textContent=list.length;{const sc=document.getElementById('search-count');if(sc){sc.textContent=query?`${list.length} of ${catalog.assets.length}`:'';sc.hidden=!query;}}$('collection-range').textContent=catalog.assets.length?`01—${catalog.assets.length}`:'—';$('empty').hidden=!!list.length;$('gallery').replaceChildren();
 for(const asset of list){const b=document.createElement('button');b.type='button';b.className='object-tile';b.dataset.object=asset.id;b.setAttribute('aria-pressed',String(asset.id===current?.id));b.setAttribute('aria-label',asset.name);const thumb=document.createElement('div');thumb.className='thumb';const img=document.createElement('img');img.src=thumbnail(asset);img.alt='';img.loading='lazy';img.width=256;img.height=256;const dot=document.createElement('span');dot.className='selected-dot';thumb.append(img,dot);const name=document.createElement('span');name.className='tile-name';name.textContent=asset.name;const index=document.createElement('span');index.className='tile-index';index.textContent=String(catalog.assets.indexOf(asset)+1).padStart(2,'0');b.append(thumb,name,index);b.addEventListener('click',()=>selectObject(asset));$('gallery').append(b);}
 renderCustomGallery();revealSelected();
}
// Keep the selected tile visible inside the gallery scroller without moving the page.
function revealSelected(){const box=document.querySelector('.gallery-scroll'),tile=box?.querySelector('[aria-pressed="true"]');if(!tile)return;requestAnimationFrame(()=>{const b=box.getBoundingClientRect(),t=tile.getBoundingClientRect(),pad=10;if(t.left<b.left+pad)box.scrollLeft-=b.left+pad-t.left;else if(t.right>b.right-pad)box.scrollLeft+=t.right-b.right+pad;if(t.top<b.top+pad)box.scrollTop-=b.top+pad-t.top;else if(t.bottom>b.bottom-pad)box.scrollTop+=t.bottom-b.bottom+pad;});}
function setBlast(active){engine.set({blastHold:active});$('blast-toggle').checked=!!active;persist();}
function applyTheme(theme){document.documentElement.dataset.theme=theme;$('site-icon').href=`assets/brand/favicon-${theme}.svg?v=1`;try{localStorage.setItem('little-things-theme-v1',theme);}catch{}document.querySelectorAll('[data-theme-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.themeChoice===theme)));if(engine){setBackground(theme==='dark'?'#28302d':'#ebe9e2');}gallery();}
function setTheme(theme){if(document.documentElement.dataset.theme===theme)return;if(document.startViewTransition&&!matchMedia('(prefers-reduced-motion: reduce)').matches)document.startViewTransition(()=>applyTheme(theme));else applyTheme(theme);}
async function selectObject(asset,restore=null){
 setBlast(false);
 const version=++loadVersion;current=asset;document.documentElement.dataset.ready='loading';clearTimeout(loadTimer);$('stage').classList.add('is-switching');$('loading').hidden=true;loadTimer=setTimeout(()=>{if(version===loadVersion){$('loading').textContent='Preparing the object…';$('loading').hidden=false;}},1200);['export-glb','export-png','export-recipe'].forEach(id=>$(id).disabled=true);
 $('object-name').textContent=asset.name;$('description').textContent=asset.description;$('description').title=asset.description;document.querySelector('.stage-hint').textContent=sentence(asset.hint||(asset.interaction==='Open the cover & turn the pages'?'Hover to open and turn the pages · drag to explore':'Hover to explore · drag to rotate'));$('object-category').textContent=asset.category.toUpperCase();$('object-index').textContent=`${String(catalog.assets.indexOf(asset)+1).padStart(2,'0')} / ${catalog.assets.length}`;{const facts=document.getElementById('glb-facts');if(facts)facts.textContent=`${asset.triangles.toLocaleString()} triangles · ${asset.parts} parts · glTF 2.0`;}
 $('canvas').setAttribute('aria-label',`Interactive ${asset.name}. Drag to rotate, or use arrow keys. Home resets the view.`);gallery();
 try{const loaded=await engine.load(asset.model);if(!loaded||version!==loadVersion)return;
  if(restore?.materials){for(const saved of restore.materials){const m=engine.materials.find(m=>m.name===saved.name);if(m)m.pbrMetallicRoughness=structuredClone(saved.pbrMetallicRoughness);}engine.invalidate();}
  else {if(palettes[paletteName])engine.palette(palettes[paletteName]);else engine.palette(customColors);}
  pressed($('palettes'),'palette',paletteName);
  materialControls();exportSizes(asset);clearTimeout(loadTimer);$('loading').hidden=true;requestAnimationFrame(()=>$('stage').classList.remove('is-switching'));['export-glb','export-png','export-recipe'].forEach(id=>$(id).disabled=false);document.documentElement.dataset.ready='true';history.replaceState(null,'',`#${asset.id}`);persist();
 }catch(error){if(version!==loadVersion)return;clearTimeout(loadTimer);$('stage').classList.remove('is-switching');$('loading').hidden=false;$('loading').textContent=error.message;document.documentElement.dataset.ready='error';}
}
function kb(bytes){return bytes>=1048576?`${(bytes/1048576).toFixed(1)} MB`:`${Math.round(bytes/1024)} KB`;}
async function exportSizes(asset){const full=$('glb-full-size'),light=$('glb-light-size');if(full)full.textContent=`Original geometry · ${kb(asset.bytes)}`;if(!light)return;light.textContent='Same look, smaller file · best for websites';try{const r=await fetch(asset.model.replace(/^models\//,'models-light/'),{method:'HEAD'});const n=Number(r.headers.get('content-length'));if(r.ok&&n&&asset===current)light.textContent=`Same look, smaller file · ${kb(n)}`;}catch{}}
function setBackground(value){if(!document.querySelector(`[data-bg="${value}"]`))value=document.documentElement.dataset.theme==='dark'?'#28302d':'#ebe9e2';engine.set({background:value});$('stage').style.setProperty('--stage-color',value);$('stage').classList.toggle('dark-stage',value!=='#ebe9e2');document.querySelectorAll('[data-bg]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.bg===value)));persist();}
function setFinish(value){const values={original:{roughness:-1,metalness:-1},ceramic:{roughness:.38,metalness:0},matte:{roughness:.9,metalness:0},gloss:{roughness:.13,metalness:0},metal:{roughness:.27,metalness:.85}};engine.set(values[value]||values.original);persist();}
function recipe(){return {schema:'little-things-scene/1',model:current.model,id:current.id,palette:paletteName,lightPreset:lightName,render:{...engine.state},view:{yaw:engine.baseYaw,pitch:engine.basePitch},materials:engine.materials.map(m=>({name:m.name,...m.pbrMetallicRoughness})),note:'Pointer motion, lighting and shadows belong to the viewer. The GLB export contains geometry and edited material values.'};}
async function boot(){
 try{
  [catalog,palettes,lights]=await Promise.all(['catalog.json','presets/palettes.json','presets/lighting.json'].map(async url=>{const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw Error(`Unable to load ${url}`);return r.json();}));
  engine=new ObjectRenderer($('canvas'));let saved=null;try{saved=JSON.parse(localStorage.getItem('little-things-studio-v1'));if(saved?.version!==catalog.version&&saved){saved.version=catalog.version;}}catch{}
  if(saved?.paletteName){paletteName=palettes[saved.paletteName]?saved.paletteName:'Custom';customColors=saved.customColors||{};lightName=lights[saved.lightName]?saved.lightName:'Softbox';}
  else {paletteName='Cobalt';lightName='Product studio';engine.set(lights[lightName]);}
  if(saved?.state){engine.set(saved.state);paletteName=palettes[saved.paletteName]?saved.paletteName:'Custom';lightName=lights[saved.lightName]?saved.lightName:'Custom';$('finish').value=saved.finish||'original';$('follow').checked=!!engine.state.follow;$('spin').checked=!!engine.state.spin;setBackground(engine.state.background);}
  engine.set({blastHold:false});
  document.querySelectorAll('[data-theme-choice]').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.themeChoice)));
  $('blast-toggle').addEventListener('change',event=>setBlast(event.currentTarget.checked));
  const theme=document.documentElement.dataset.theme||'light';document.querySelectorAll('[data-theme-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.themeChoice===theme)));if(theme==='dark'&&(!saved?.state?.background||saved.state.background==='#ebe9e2'))setBackground('#28302d');
  for(const key of ['explodeOnHover','explodeHold'])$(key).checked=!!engine.state[key];$('explodeStrength').value=engine.state.explodeStrength;$('explodeStrength-out').value=Number(engine.state.explodeStrength).toFixed(2);
  for(const name of ['All',...catalog.categories]){const b=document.createElement('button');b.type='button';b.className='chip';b.textContent=name;b.dataset.category=name;b.setAttribute('aria-pressed',String(name==='All'));b.addEventListener('click',()=>{category=name;pressed($('filters'),'category',name);gallery();});$('filters').append(b);}
  for(const [name,colors]of Object.entries(palettes)){const b=document.createElement('button');b.className='palette';b.type='button';b.dataset.palette=name;b.setAttribute('aria-label',`${name} palette`);b.setAttribute('aria-pressed',String(name===paletteName));const swatch=document.createElement('span');swatch.className='palette-swatch';for(const slot of ['body','secondary','accent','ink']){const dot=document.createElement('i');dot.style.setProperty('--color',colors[slot]);swatch.append(dot);}const label=document.createElement('span');label.className='palette-name';label.textContent=name;b.append(swatch,label);b.addEventListener('click',()=>{paletteName=name;customColors={...colors};engine.palette(colors);refreshGalleryColors();pressed($('palettes'),'palette',name);materialControls();persist();});$('palettes').append(b);}
  for(const [name,values]of Object.entries(lights)){const b=lightChip(name,values,name===lightName);b.addEventListener('click',()=>{engine.set(values);lightName=name;syncLightControls();persist();});$('lights').append(b);}
  for(const key of lightKeys)$(key).addEventListener('input',()=>{engine.set({[key]:Number($(key).value)});lightName='Custom';syncLightControls();persist();});
  document.querySelectorAll('input[type=range]').forEach(input=>{paintRange(input);input.addEventListener('input',()=>paintRange(input));});
  $('search').addEventListener('input',gallery);$('finish').addEventListener('change',()=>setFinish($('finish').value));
  for(const key of ['follow','spin','explodeOnHover','explodeHold'])$(key).addEventListener('change',()=>{engine.set({[key]:$(key).checked});persist();});
  $('explodeStrength').addEventListener('input',()=>{const value=Number($('explodeStrength').value);engine.set({explodeStrength:value});$('explodeStrength-out').value=value.toFixed(2);persist();});
  $('frame').addEventListener('change',()=>$('orbit').hidden=!$('frame').checked);
  document.querySelectorAll('[data-bg]').forEach(b=>b.addEventListener('click',()=>setBackground(b.dataset.bg)));
  $('reset-view').addEventListener('click',()=>engine.resetView());
  $('reset-all').addEventListener('click',async()=>{const rb=$('reset-all');rb.classList.remove('is-spinning');void rb.offsetWidth;rb.classList.add('is-spinning');paletteName='Workshop';customColors={...palettes.Workshop};refreshGalleryColors();lightName='Softbox';engine.set({...lights.Softbox,roughness:-1,metalness:-1,follow:true,spin:false,explodeOnHover:true,explodeHold:false,explodeStrength:.85});$('finish').value='original';$('follow').checked=true;$('spin').checked=false;$('explodeOnHover').checked=true;$('explodeHold').checked=false;$('explodeStrength').value=.85;$('explodeStrength-out').value='0.85';$('frame').checked=false;$('orbit').hidden=true;setBackground('#ebe9e2');syncLightControls();pressed($('palettes'),'palette','Workshop');await selectObject(current);toast('Back to the original.');});
  $('canvas').addEventListener('pointerup',persist);$('canvas').addEventListener('keydown',persist);document.querySelector('.guide-button').addEventListener('click',persist);
  const glbName=suffix=>`${current.id}-${paletteName.toLowerCase()}${suffix}.glb`;
  const lightUrl=asset=>asset.model.replace(/^models\//,'models-light/');
  exportMenu($('export-glb'),{label:'3D object export',note:'glb-facts',items:[
   {label:'Full detail',detail:'Original geometry · best for Blender',id:'glb-full-size',run:()=>{try{download(engine.glb(),glbName(''));}catch(error){toast(error.message);}}},
   {label:'Light',detail:'Same look, smaller file · best for websites',id:'glb-light-size',run:async()=>{const asset=current;try{const r=await fetch(lightUrl(asset));if(!r.ok)throw Error('The light file is not available for this object yet.');const buffer=await r.arrayBuffer();if(asset!==current)return;download(engine.glb(buffer),glbName('-light'));}catch(error){toast(error.message);}}}]});

  async function cutout(action){const id=current.id;$('export-png').disabled=true;try{if(action==='copy'){if(!navigator.clipboard?.write||!window.ClipboardItem)throw Error('Image copying is unavailable in this browser. Use Download instead.');const image=engine.png().then(blob=>{if(!blob)throw Error('The cutout could not be created.');return blob;});await navigator.clipboard.write([new ClipboardItem({'image/png':image})]);toast('PNG copied. Paste it into your design.');}else{const blob=await engine.png();if(!blob)throw Error('The cutout could not be created.');download(blob,`${id}-cutout-2048.png`);}}catch(error){toast(error.message||'The image could not be copied. Use Download instead.');}finally{$('export-png').disabled=false;}}
  exportMenu($('export-png'),{download:()=>cutout('download'),copy:()=>cutout('copy')});
  async function copySceneEmbed(){const button=$('export-recipe');button.disabled=true;toast('Preparing a live 3D embed…');try{const scene={id:current.id,label:current.name,theme:document.documentElement.dataset.theme,transparent:true,state:{...engine.state,blastHold:false},view:{yaw:engine.baseYaw,pitch:engine.basePitch},motion:engine.state.explodeHold?'loop':engine.state.explodeOnHover?'hover':'still'};const model=engine.glb();const code=portableEmbed(model,scene,await portableRenderer);if(navigator.clipboard?.write&&window.ClipboardItem){await navigator.clipboard.write([new ClipboardItem({'text/plain':code.then(value=>new Blob([value],{type:'text/plain'}))})]);toast('3D embed copied. Paste into Framer’s Embed → HTML.');}else await copyExportCode(await code,toast);}catch(error){toast(error.message||'The embed could not be copied.');}finally{button.disabled=false;}}
  exportMenu($('export-recipe'),{download:()=>jsonDownload(recipe(),`${current.id}-scene.json`),copy:copySceneEmbed});
  window.addEventListener('hashchange',()=>{const id=decodeURIComponent(location.hash.slice(1));const asset=catalog.assets.find(a=>a.id===id);if(asset&&asset.id!==current?.id)selectObject(asset);});
  syncLightControls();const hash=decodeURIComponent(location.hash.slice(1));const asset=catalog.assets.find(a=>a.id===hash)||catalog.assets.find(a=>a.id===saved?.id)||catalog.assets[0];await selectObject(asset,asset.id===saved?.id?saved:null);
 }catch(error){$('loading').hidden=false;$('loading').textContent=`${error.message}. Start this folder with python3 serve.py, then open http://localhost:8765.`;document.documentElement.dataset.ready='error';}
}
boot();

// First-visit hint: shown until the visitor first hovers, drags or uses the keyboard on the object, then never again.
(()=>{const hint=document.querySelector('.stage-hint'),canvas=document.getElementById('canvas');if(!hint||!canvas)return;
 let seen=false;try{seen=localStorage.getItem('threed-hint-seen')==='1';}catch{}
 if(seen){hint.classList.add('is-hidden');return;}
 let timer;const done=()=>{clearTimeout(timer);hint.classList.add('is-hidden');try{localStorage.setItem('threed-hint-seen','1');}catch{}['pointerdown','keydown'].forEach(n=>canvas.removeEventListener(n,done));};
 canvas.addEventListener('pointerenter',()=>{timer=setTimeout(done,2200);});canvas.addEventListener('pointerleave',()=>clearTimeout(timer));
 ['pointerdown','keydown'].forEach(n=>canvas.addEventListener(n,done));})();

// Fine-tune remembers whether the visitor left it open.
(()=>{const ft=document.getElementById('fine-tune');if(!ft)return;try{ft.open=localStorage.getItem('threed-fine-tune-open')==='1';}catch{}
 ft.addEventListener('toggle',()=>{try{localStorage.setItem('threed-fine-tune-open',ft.open?'1':'0');}catch{}});})();

// Sentence case for interface copy; keeps format names and 3D in capitals.
function sentence(text){const t=String(text).toLowerCase().replace(/\b(3d|png|glb|json|gltf)\b/g,m=>m.toUpperCase());return t.charAt(0).toUpperCase()+t.slice(1);}

// Catalogue browsing: previous / next on the stage and arrow keys through the visible collection.
function stepObject(dir){const tiles=[...document.querySelectorAll('#gallery [data-object]')];if(!tiles.length||!catalog)return;let i=tiles.findIndex(t=>t.dataset.object===current?.id);i=i<0?0:(i+dir+tiles.length)%tiles.length;const asset=catalog.assets.find(a=>a.id===tiles[i].dataset.object);if(asset)selectObject(asset);}
document.getElementById('stage-prev')?.addEventListener('click',()=>stepObject(-1));
document.getElementById('stage-next')?.addEventListener('click',()=>stepObject(1));
document.addEventListener('keydown',e=>{
 const t=e.target,typing=t.closest?.('input,select,textarea,[contenteditable]');
 if(e.key==='/'&&!typing&&!e.metaKey&&!e.ctrlKey){e.preventDefault();$('search').focus();$('search').select();return;}
 if(typing||t.id==='canvas'||e.metaKey||e.ctrlKey||e.altKey)return;
 if(e.key==='ArrowRight'||e.key==='ArrowLeft'){if(t.closest?.('.export-dropdown,[role=menu]'))return;e.preventDefault();stepObject(e.key==='ArrowRight'?1:-1);}
});


