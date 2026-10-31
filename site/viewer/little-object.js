import {ObjectRenderer} from './renderer.js?v=0.8.0-offscreen';

/** Plain HTML component. Serve over HTTP(S); no dependencies or network calls beyond local assets. */
export class LittleObject extends HTMLElement {
 static get observedAttributes(){return ['blast','src','body','accent','secondary','background','azimuth','elevation','intensity','fill','warmth','shadow','softness','follow','spin','explode','hold-open','separation','label'];}
 constructor(){
  super();this.attachShadow({mode:'open'});this.shadowRoot.innerHTML=`<style>:host{display:block;min-height:240px;position:relative;overflow:hidden}canvas{width:100%;height:100%;min-height:inherit;display:block;cursor:grab;touch-action:pan-y}canvas:focus-visible{outline:2px solid currentColor;outline-offset:-4px}.message{position:absolute;inset:0;display:grid;place-items:center;padding:24px;font:12px/1.5 sans-serif;text-align:center;pointer-events:none}</style><canvas tabindex="0" role="img"></canvas><div class="message" role="status">Loading object…</div>`;
 }
 connectedCallback(){try{if(!this.renderer)this.renderer=new ObjectRenderer(this.shadowRoot.querySelector('canvas'));this.sync();this.load();}catch(e){this.message(e.message);}}
 disconnectedCallback(){this.renderer?.dispose();this.renderer=null;}
 attributeChangedCallback(name){if(!this.renderer)return;this.sync();if(name==='src')this.load();}
 message(value){const el=this.shadowRoot.querySelector('.message');el.textContent=value;el.hidden=!value;el.style.display=value?'grid':'none';}
 async load(){const src=this.getAttribute('src');if(!src){this.message('Set a src attribute to one of the pack’s GLB files.');return;}this.message('Loading object…');try{const loaded=await this.renderer.load(new URL(src,document.baseURI).href);if(loaded){this.sync();this.message('');this.dispatchEvent(new CustomEvent('object-ready',{bubbles:true}));}}catch(e){this.message(e.message);this.dispatchEvent(new CustomEvent('object-error',{detail:e.message,bubbles:true}));}}
 sync(){
  const r=this.renderer;if(!r)return;const values={};for(const key of ['azimuth','elevation','intensity','fill','warmth','shadow','softness']){if(this.hasAttribute(key)){const n=Number(this.getAttribute(key));if(Number.isFinite(n))values[key]=n;}}
  for(const key of ['body','accent','secondary']){const color=this.getAttribute(key);if(/^#[0-9a-f]{6}$/i.test(color||''))r.color(key,color);}
  if(/^#[0-9a-f]{6}$/i.test(this.getAttribute('background')||''))values.background=this.getAttribute('background');
  values.blastHold=this.getAttribute('blast')==='true';values.follow=this.getAttribute('follow')!=='false';values.spin=this.hasAttribute('spin')&&this.getAttribute('spin')!=='false';r.set(values);
  values.explodeOnHover=this.getAttribute('explode')!=='false';values.explodeHold=this.hasAttribute('hold-open')&&this.getAttribute('hold-open')!=='false';
  if(this.hasAttribute('separation')){const n=Number(this.getAttribute('separation'));if(Number.isFinite(n))values.explodeStrength=Math.max(0,Math.min(1.5,n));}r.set(values);
  this.shadowRoot.querySelector('canvas').setAttribute('aria-label',this.getAttribute('label')||'Interactive 3D object. Drag or use arrow keys to rotate. Home resets the view.');
 }
 setMaterial(slot,hex){if(!/^#[0-9a-f]{6}$/i.test(hex))throw Error('Use a six-digit hex color.');this.renderer?.color(slot,hex);}
 setOptions(options){this.renderer?.set(options);}
 resetView(){this.renderer?.resetView();}
}
if(!customElements.get('little-object'))customElements.define('little-object',LittleObject);
