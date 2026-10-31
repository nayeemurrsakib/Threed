/** Optional pointer magnetism for .lt-magnetic buttons. Safe to call repeatedly. */
export function bindMagneticButtons(root=document){
 const reduce=matchMedia('(prefers-reduced-motion: reduce)');
 root.querySelectorAll('.lt-magnetic').forEach(button=>{
  if(button.dataset.ltBound)return;button.dataset.ltBound='true';
  button.addEventListener('pointermove',event=>{if(reduce.matches||event.pointerType==='touch')return;const r=button.getBoundingClientRect();button.style.setProperty('--lt-x',`${((event.clientX-r.left)/r.width-.5)*9}px`);button.style.setProperty('--lt-y',`${((event.clientY-r.top)/r.height-.5)*7}px`);});
  button.addEventListener('pointerleave',()=>{button.style.setProperty('--lt-x','0px');button.style.setProperty('--lt-y','0px');});
 });
}
