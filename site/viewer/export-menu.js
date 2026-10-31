// Two explicit export choices, with keyboard navigation and viewport-safe placement.
export function exportMenu(button,{download,copy,items,label,note}={}){
 const wrapper=document.createElement('span');wrapper.className='export-choice';button.before(wrapper);wrapper.append(button);
 const menu=document.createElement('div');menu.className='export-dropdown';menu.id=button.id+'-menu';menu.hidden=true;menu.setAttribute('role','menu');menu.setAttribute('aria-label',label||(button.id==='export-png'?'Cutout export':'Scene settings export'));
 const isImage=button.id==='export-png';
 const chevron=document.createElementNS('http://www.w3.org/2000/svg','svg');chevron.setAttribute('viewBox','0 0 16 16');chevron.setAttribute('width','12');chevron.setAttribute('height','12');chevron.setAttribute('fill','none');chevron.setAttribute('stroke','currentColor');chevron.setAttribute('stroke-width','1.5');chevron.setAttribute('stroke-linecap','round');chevron.setAttribute('stroke-linejoin','round');chevron.setAttribute('aria-hidden','true');chevron.classList.add('export-chevron');const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d','m4 6 4 4 4-4');chevron.append(path);button.append(chevron);
 const entries=items||[{label:'Download',detail:isImage?'PNG · 2048 × 2048':'JSON scene recipe',run:download},{label:isImage?'Copy PNG':'Copy code',detail:isImage?'Transparent image':'Live 3D · paste into Embed HTML',run:copy}];
 for(const entry of entries){
  const item=document.createElement('button');item.type='button';item.setAttribute('role','menuitem');const name=document.createElement('span');name.textContent=entry.label;const hint=document.createElement('small');hint.textContent=entry.detail;if(entry.id)hint.id=entry.id;item.append(name,hint);
  item.addEventListener('click',()=>{close(true);entry.run();});menu.append(item);
 }
 if(note){const n=document.createElement('p');n.className='export-note';n.id=note;menu.append(n);}
 wrapper.append(menu);button.setAttribute('aria-haspopup','menu');button.setAttribute('aria-controls',menu.id);button.setAttribute('aria-expanded','false');
 function close(focus=false){if(menu.hidden)return;menu.hidden=true;button.setAttribute('aria-expanded','false');if(focus)button.focus({preventScroll:true});}
 function open(last=false){
  document.dispatchEvent(new CustomEvent('export-menu-open',{detail:button.id}));menu.hidden=false;button.setAttribute('aria-expanded','true');
  const rect=button.getBoundingClientRect(),width=menu.offsetWidth,height=menu.offsetHeight;
  const anchor=wrapper.getBoundingClientRect(),left=Math.max(12,Math.min(rect.left,innerWidth-width-12)),top=innerHeight-rect.bottom>=height+20?rect.bottom+10:Math.max(12,rect.top-height-10);menu.style.left=(left-anchor.left)+'px';menu.style.top=(top-anchor.top)+'px';
  {const all=menu.querySelectorAll('button');all[last?all.length-1:0].focus({preventScroll:true});}
 }
 button.addEventListener('click',()=>menu.hidden?open():close());button.addEventListener('keydown',event=>{if(['ArrowDown','ArrowUp'].includes(event.key)){event.preventDefault();open(event.key==='ArrowUp');}});
 menu.addEventListener('keydown',event=>{const items=[...menu.querySelectorAll('button')],index=items.indexOf(document.activeElement);if(event.key==='Tab'){close(true);}else if(event.key==='Escape'){event.preventDefault();close(true);}else if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?items.length-1:(index+(event.key==='ArrowDown'?1:-1)+items.length)%items.length;items[next].focus();}});
 document.addEventListener('pointerdown',event=>{if(!wrapper.contains(event.target))close();});document.addEventListener('export-menu-open',event=>{if(event.detail!==button.id)close();});
 menu.addEventListener('pointerdown',event=>event.preventDefault());window.addEventListener('resize',()=>close());
 return{close};
}

export async function copyExportCode(code,toast){
 try{await navigator.clipboard.writeText(code);toast('Code copied.');}
 catch{
  let box=document.querySelector('#export-copy-fallback');
  if(!box){box=document.createElement('section');box.id='export-copy-fallback';box.className='export-copy-fallback';box.setAttribute('aria-label','Export code');const label=document.createElement('label');label.textContent='Copy this code';const field=document.createElement('textarea');field.readOnly=true;field.rows=4;field.setAttribute('aria-label','Export code');label.append(field);const close=document.createElement('button');close.type='button';close.textContent='Close';close.addEventListener('click',()=>{box.hidden=true;});box.append(label,close);document.querySelector('.export-bar').after(box);}
  box.hidden=false;const field=box.querySelector('textarea');field.value=code;field.focus();field.select();toast('Copy the selected code below.');
 }
}
