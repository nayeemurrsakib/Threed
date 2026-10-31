// One reusable background renderer for custom material colors; presets use PNGs.
import {ObjectRenderer} from './renderer.js?v=0.8.0-offscreen';
export class GalleryColors {
 constructor(){this.key='';this.urls=new Map();this.request=0;this.running=false;}
 update(assets,colors,lighting,apply){
  const key=JSON.stringify(colors);if(key!==this.key){this.key=key;for(const url of this.urls.values())URL.revokeObjectURL(url);this.urls.clear();this.request++;}
  this.pending={assets,colors:{...colors},lighting,apply};if(!this.running)this.run();
 }
 cancel(){this.request++;this.pending=null;}
 async run(){
  this.running=true;const canvas=document.createElement('canvas');canvas.hidden=true;document.body.append(canvas);let renderer;
  try{
   renderer=new ObjectRenderer(canvas);renderer.set({follow:false,spin:false,explodeOnHover:false,explodeHold:false});
   while(this.pending){
    const job=this.pending,revision=this.request;this.pending=null;renderer.set(job.lighting);
    for(const asset of job.assets){
     if(revision!==this.request)break;
     if(!this.urls.has(asset.id)){await renderer.load(asset.model);if(revision!==this.request)break;renderer.palette(job.colors);const blob=await renderer.png(256);if(revision!==this.request)break;if(blob)this.urls.set(asset.id,URL.createObjectURL(blob));}
     const url=this.urls.get(asset.id);if(url)job.apply(asset.id,url);
    }
   }
  }catch(error){console.warn('Custom gallery preview could not finish:',error.message);}
  finally{renderer?.dispose();canvas.remove();this.running=false;}
 }
 get(id){return this.urls.get(id);}
}
