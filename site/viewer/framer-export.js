import {normalizeScene,libraryURL,embedURL,iframeMarkup} from './embed-config.js?v=1';
export function setupFramer({getScene,toast,download}){
 const $=id=>document.getElementById(id),panel=$('framer-panel');let scene,baseScene,platform='framer';
 const template=fetch('integrations/framer/Threed.tsx').then(r=>{if(!r.ok)throw Error('The component file could not load.');return r.text();});
 function update(){
  if(!baseScene)return;
  scene=normalizeScene({...baseScene,theme:$('embed-theme').value,motion:$('embed-motion').value,transparent:$('embed-transparent').checked,state:{...baseScene.state,background:$('embed-background').value}});
  try{const base=libraryURL($('embed-host').value);$('embed-code').value=iframeMarkup(base,scene);$('embed-error').hidden=true;for(const id of ['copy-embed','copy-embed-link','download-framer'])$(id).disabled=false;
   const local=['localhost','127.0.0.1','[::1]'].includes(base.hostname);$('embed-host-help').textContent=local?`This address works on your computer. For your published ${platform==='framer'?'Framer':'Webflow'} site, host the library and enter its HTTPS address.`:`Use this library address in ${platform==='framer'?'Framer':'Webflow'}. Keep the viewer, embed page, catalog and models together on this host.`;
  }catch(error){$('embed-error').textContent=error.message;$('embed-error').hidden=false;for(const id of ['copy-embed','copy-embed-link','download-framer'])$(id).disabled=true;$('embed-code').value='';}
  $('embed-background').disabled=scene.transparent;
  // Preview uses the local runtime; the supplied production URL is only used in exports.
  $('embed-preview').src=embedURL(new URL('./',location.href),scene);
 }
 $('use-framer').addEventListener('click',()=>{
  const open=panel.hidden;panel.hidden=!open;$('use-framer').setAttribute('aria-expanded',String(open));
  if(open){baseScene=getScene();$('embed-object-name').textContent=baseScene.label;$('embed-host').value=new URL('./',location.href).href;$('embed-theme').value=baseScene.theme;$('embed-motion').value=baseScene.motion;$('embed-background').value=baseScene.state.background;$('embed-transparent').checked=true;update();$('embed-motion').focus();}
  else $('embed-preview').removeAttribute('src');
 });
 $('close-framer').addEventListener('click',()=>{panel.hidden=true;$('use-framer').setAttribute('aria-expanded','false');$('embed-preview').removeAttribute('src');$('use-framer').focus();});
 for(const id of ['embed-host','embed-motion','embed-transparent','embed-background'])$(id).addEventListener('change',update);
 $('embed-theme').addEventListener('change',()=>{$('embed-background').value=$('embed-theme').value==='dark'?'#28302d':'#ebe9e2';update();});
 $('refresh-embed').addEventListener('click',()=>{baseScene=getScene();$('embed-object-name').textContent=baseScene.label;update();toast('Current colors, light and view applied.');});
 document.querySelectorAll('[data-export-platform]').forEach(button=>button.addEventListener('click',()=>{platform=button.dataset.exportPlatform;document.querySelectorAll('[data-export-platform]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));$('download-framer').hidden=platform!=='framer';$('embed-steps').innerHTML=platform==='framer'?'<li>In Framer, insert an <strong>Embed</strong> and paste the code into its HTML field.</li><li>For controls in Framer, create a code file, paste the downloaded <strong>Threed.tsx</strong>, then add it to your canvas.</li>':'<li>In Webflow, add a <strong>Code Embed</strong> element and paste the copied iframe code.</li><li>Save and close. Set a height on the Embed’s parent, then preview your page. Check the published page before sharing.</li>';update(); }));
 async function copy(value){try{await navigator.clipboard.writeText(value);toast(platform==='framer'?'Copied. Paste it into Framer’s Embed component.':'Copied. Paste it into Webflow’s Code Embed element.');}catch{$('embed-code').closest('details').open=true;$('embed-code').focus();$('embed-code').select();toast('Select and copy the code below.');}}
 $('copy-embed').addEventListener('click',()=>copy($('embed-code').value));$('copy-embed-link').addEventListener('click',()=>copy(embedURL($('embed-host').value,scene)));
 $('download-framer').addEventListener('click',async()=>{try{const source=(await template).replace(/\/\* THREED_SCENE \*\/[\s\S]*?\/\* END_SCENE \*\//,()=>JSON.stringify(scene)).replace(/\/\* THREED_LIBRARY \*\/[\s\S]*?\/\* END_LIBRARY \*\//,()=>JSON.stringify(libraryURL($('embed-host').value).href));download(new Blob([source],{type:'text/plain'}),'Threed.tsx');}catch(error){toast(error.message);}});
 return{refresh(){if(!panel.hidden){baseScene=getScene();$('embed-object-name').textContent=baseScene.label;update();}}};
}
