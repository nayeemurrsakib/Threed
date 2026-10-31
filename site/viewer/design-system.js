// threed® design system page: renders tokens live from tokens.css and wires the component specimens.
import './little-object.js';
import {bindMagneticButtons} from './buttons.js';
import {lightChip} from './chips.js?v=1';
import {exportMenu} from './export-menu.js?v=9-note';

const $ = id => document.getElementById(id);
const root = document.documentElement;
const token = name => getComputedStyle(root).getPropertyValue(name).trim();
const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };

/* Theme — same behaviour as the studio and guide. */
function applyTheme(theme){root.dataset.theme=theme;$('site-icon').href=`assets/brand/favicon-${theme}.svg?v=1`;document.querySelectorAll('[data-theme-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.themeChoice===theme)));try{localStorage.setItem('little-things-theme-v1',theme);}catch{}}
applyTheme(root.dataset.theme||'light');
document.querySelectorAll('[data-theme-choice]').forEach(b=>b.addEventListener('click',()=>{const change=()=>applyTheme(b.dataset.themeChoice);if(document.startViewTransition&&!matchMedia('(prefers-reduced-motion: reduce)').matches&&!document.hidden)document.startViewTransition(change).ready.catch(()=>{});else change();}));

/* Colour */
const COLORS = [
 ['--bone','Background','Page background'],['--stage','Stage','Object stage, inputs, wells'],['--paper','Paper','Raised surfaces, menus'],
 ['--ink','Ink','Text and selected states'],['--muted','Muted','Secondary text and labels'],['--line','Line','Hairlines and borders'],
 ['--leaf','Leaf','Hover and selected fills'],['--accent','Accent','Primary action and focus'],['--on-accent','On accent','Text on the accent'],
 ['--track','Track','Switch, off'],['--track-on','Track on','Switch, on'],['--status-ok','Status OK','Live status, healthy'],['--status-error','Status error','Live status, problem'],
];
function renderColors(){
 $('swatches').replaceChildren(...COLORS.map(([name,label,role])=>{
  const card=el('div','ds-swatch');const chip=el('span','ds-swatch-chip');chip.style.background=`var(${name})`;
  const value=token(name).toLowerCase(),twin=COLORS.find(([n])=>n!==name&&COLORS.indexOf(COLORS.find(c=>c[0]===n))<COLORS.findIndex(c=>c[0]===name)&&token(n).toLowerCase()===value);if(twin)card.classList.add('ds-alias');const text=el('div');text.append(el('strong',null,label),el('span','t-body-sm ds-muted',twin?`${role} · uses ${twin[1]} in this theme`:role),el('code',null,`${name} · ${twin?'= '+twin[0]:token(name)}`));
  card.append(chip,text);return card;}));
 renderLayout();
 const ex=document.querySelectorAll('[aria-label="Appearance example"] button');if(ex.length===2){ex[0].setAttribute('aria-pressed',String(root.dataset.theme!=='dark'));ex[1].setAttribute('aria-pressed',String(root.dataset.theme==='dark'));}
}

/* Type scale */
const SIZES=['2xs','xs','sm','md','lg','xl','2xl','3xl','4xl','5xl'];
$('type-scale').replaceChildren(...SIZES.map(s=>{const row=el('div','ds-scale-row');const a=el('span','ds-scale-sample','Aa');a.style.fontSize=`var(--fs-${s})`;row.append(a,el('code',null,`--fs-${s} · ${token(`--fs-${s}`)}`));return row;}));

/* Spacing */
const SPACES=[2,4,6,8,12,16,20,24,32,40,48,64];
$('spaces').replaceChildren(...SPACES.map(n=>{const row=el('div','ds-space-row');const bar=el('span','ds-space-bar');bar.style.width=`var(--space-${n})`;row.append(el('code',null,`--space-${n}`),bar,el('span','t-meta',`${n}px`));return row;}));

/* Shape */
const RADII=[['--radius-xs','Swatches'],['--radius-sm','Tiles, inputs, stage'],['--radius-md','Cards, menus'],['--radius-pill','Buttons, chips, switches'],['--radius-round','Dots, avatars, icon buttons']];
$('radii').replaceChildren(...RADII.map(([name,use])=>{const box=el('div','ds-radius');const s=el('span','ds-radius-shape');s.style.borderRadius=`var(${name})`;box.append(s,el('code',null,`${name} · ${token(name)}`),el('span','t-body-sm ds-muted',use));return box;}));

/* Layout */
function renderLayout(){
 const facts=[['--page-max','Maximum page width'],['--page-gutter','Gutter at this screen size'],['--header-h','Header height'],['--control-h','Header control height'],['--button-h','Action button height']];
 $('layout-facts').replaceChildren(...facts.map(([name,label])=>{const f=el('div','ds-fact');f.append(el('span','t-title',token(name)),el('span','t-body-sm ds-muted',label),el('code',null,name));return f;}));
}
new MutationObserver(renderColors).observe(root,{attributes:true,attributeFilter:['data-theme']});
addEventListener('resize',renderLayout);
renderColors();

/* Specimens that share the studio's markup */
const pressGroup=(box,selector)=>box.addEventListener('click',e=>{const b=e.target.closest(selector);if(!b)return;box.querySelectorAll(selector).forEach(x=>x.setAttribute('aria-pressed',String(x===b)));});
$('ds-chips').replaceChildren(...['All','Desk','Devices','Kitchen'].map((n,i)=>{const b=el('button','chip',n);b.type='button';b.setAttribute('aria-pressed',String(i===0));return b;}));pressGroup($('ds-chips'),'.chip');
fetch('presets/lighting.json').then(r=>r.json()).then(lights=>{$('ds-lights').replaceChildren(...Object.entries(lights).map(([n,v],i)=>lightChip(n,v,i===0)));pressGroup($('ds-lights'),'.light-option');}).catch(()=>{});
$('ds-range').addEventListener('input',e=>{$('ds-range-out').value=Number(e.target.value).toFixed(1);});
fetch('presets/palettes.json').then(r=>r.json()).then(palettes=>{
 const names=Object.keys(palettes).slice(0,6);
 $('ds-palettes').replaceChildren(...names.map((name,i)=>{const b=el('button','palette');b.type='button';b.setAttribute('aria-pressed',String(i===1));const sw=el('span','palette-swatch');for(const k of ['body','accent','secondary','ink']){const c=el('i');c.style.setProperty('--color',palettes[name][k]);sw.append(c);}b.append(sw,el('span','palette-name',name));return b;}));
 pressGroup($('ds-palettes'),'.palette');
 const p=palettes[names[1]];$('ds-colors').replaceChildren(...['accent','body','ink','secondary'].map(k=>{const l=el('label','color-control chip-option');const inp=el('input');inp.type='color';inp.value=p[k];const hex=el('span','color-hex',p[k].toUpperCase());inp.addEventListener('input',()=>{hex.textContent=inp.value.toUpperCase();});l.append(inp,el('span','color-name',k),hex);return l;}));
}).catch(()=>{});
fetch('catalog.json').then(r=>r.json()).then(catalog=>{
 $('ds-tiles').replaceChildren(...catalog.assets.slice(0,4).map((a,i)=>{const b=el('button','object-tile');b.type='button';b.setAttribute('aria-pressed',String(i===0));const t=el('div','thumb');const img=el('img');img.src=a.thumbnail;img.alt='';img.width=img.height=256;t.append(img,el('span','selected-dot'));b.append(t,el('span','tile-name',a.name),el('span','tile-index',String(i+1).padStart(2,'0')));return b;}));
 pressGroup($('ds-tiles'),'.object-tile');
}).catch(()=>{});
let toastTimer;$('ds-toast-button').addEventListener('click',()=>{const t=$('toast');t.textContent='Saved calculator-cobalt.glb';t.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('visible'),2200);});

/* Button kit (formerly buttons.html) */
bindMagneticButtons();
const object=$('example'),status=$('button-status');let spinning=false,index=0;const models=['tiny-robot','rangefinder-camera','pour-over-kettle','wind-up-bird'];
document.querySelectorAll('[data-color]').forEach(button=>button.addEventListener('click',()=>{object.setAttribute('accent',button.dataset.color);document.querySelectorAll('[data-color]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));status.textContent='Accent changed. Same object, a different personality.';}));
$('demo-spin').addEventListener('click',e=>{spinning=!spinning;object.setAttribute('spin',String(spinning));e.currentTarget.setAttribute('aria-pressed',String(spinning));e.currentTarget.textContent=spinning?'Pause the turntable Ⅱ':'Give it a spin ↻';status.textContent=spinning?'Turntable on. Reduced-motion settings take priority.':'Turntable paused.';});
$('demo-magnet').addEventListener('click',()=>{index=(index+1)%models.length;object.setAttribute('src',`models/${models[index]}.glb`);status.textContent=`Now showing: ${models[index].replaceAll('-',' ')}.`;});
$('demo-reset').addEventListener('click',()=>{index=0;spinning=false;object.setAttribute('src','models/tiny-robot.glb');object.setAttribute('accent','#e66e45');object.setAttribute('spin','false');object.resetView?.();const b=$('demo-spin');b.setAttribute('aria-pressed','false');b.textContent='Give it a spin ↻';document.querySelectorAll('[data-color]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.color==='#e66e45')));status.textContent='Back to the beginning.';});

/* Table of contents highlight */
const links=[...document.querySelectorAll('.guide-toc nav a')];
const io=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting)links.forEach(a=>a.setAttribute('aria-current',String(a.hash===`#${e.target.id}`)));},{rootMargin:'-20% 0px -70% 0px'});
document.querySelectorAll('.guide-section[id]').forEach(s=>io.observe(s));

/* Buttons use the studio's own export menu, so these specimens always match the studio. */
const say=msg=>()=>{const t=$('toast');t.textContent=msg;t.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('visible'),1800);};
exportMenu($('ds-glb'),{label:'3D object export',note:'ds-glb-facts',items:[{label:'Full detail',detail:'Original geometry · 4.6 MB',run:say('Full detail chosen')},{label:'Light',detail:'Same look, smaller file · 449 KB',run:say('Light chosen')}]});
exportMenu($('ds-png'),{download:say('Download PNG'),copy:say('Copy PNG')});
exportMenu($('ds-json'),{download:say('Download JSON'),copy:say('Copy code')});
$('ds-reset').addEventListener('click',e=>{const b=e.currentTarget;b.classList.remove('is-spinning');void b.offsetWidth;b.classList.add('is-spinning');});
document.getElementById('ds-glb-facts').textContent='140,376 triangles · 37 parts · glTF 2.0';
