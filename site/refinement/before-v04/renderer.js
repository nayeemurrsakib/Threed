/* Little Things viewer. Original, dependency-free WebGL2 renderer for this pack's GLBs.
 * Implements metallic/roughness shading, a hemisphere fill, studio highlights and PCF shadows.
 * Intentionally bounded: static indexed triangle meshes, POSITION + NORMAL, solid PBR materials.
 * This is not a general-purpose glTF engine. See README for production integration guidance.
 */
const I=()=>new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]);
function mul(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o;}
function translate(x,y,z){const m=I();m[12]=x;m[13]=y;m[14]=z;return m;}
function rotate(x,y){const a=I(),b=I();a[5]=Math.cos(x);a[6]=Math.sin(x);a[9]=-Math.sin(x);a[10]=Math.cos(x);b[0]=Math.cos(y);b[2]=-Math.sin(y);b[8]=Math.sin(y);b[10]=Math.cos(y);return mul(b,a);}
const sub=(a,b)=>a.map((v,i)=>v-b[i]);
const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
const norm=a=>{const l=Math.hypot(...a)||1;return a.map(v=>v/l);};
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
function lookAt(eye,target){const z=norm(sub(eye,target)),x=norm(cross([0,1,0],z)),y=cross(z,x);return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1]);}
function ortho(l,r,b,t,n,f){return new Float32Array([2/(r-l),0,0,0,0,2/(t-b),0,0,0,0,-2/(f-n),0,-(r+l)/(r-l),-(t+b)/(t-b),-(f+n)/(f-n),1]);}
export function hexLinear(hex){return [1,3,5].map(i=>{const v=parseInt(hex.slice(i,i+2),16)/255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;});}
export function linearHex(c){return '#'+c.slice(0,3).map(v=>{v=v<=.0031308?v*12.92:1.055*v**(1/2.4)-.055;return Math.round(Math.max(0,Math.min(1,v))*255).toString(16).padStart(2,'0');}).join('');}

const vertex=`#version 300 es
precision highp float;
layout(location=0) in vec3 position;
layout(location=1) in vec3 normal;
uniform mat4 model, vp, lightVP;
out vec3 worldPos, worldNormal;
out vec4 shadowPos;
void main(){vec4 w=model*vec4(position,1.);worldPos=w.xyz;worldNormal=mat3(model)*normal;shadowPos=lightVP*w;gl_Position=vp*w;}`;
const fragment=`#version 300 es
precision highp float;
in vec3 worldPos,worldNormal;in vec4 shadowPos;
uniform vec3 baseColor,eye,lightDirection,lightColor,groundColor;
uniform float roughness,metalness,intensity,fill,shadowStrength,softness;
uniform bool floorPass,transparent;
uniform sampler2D shadowMap;
out vec4 outColor;
const float PI=3.14159265;
float visibility(vec3 N){
 vec3 p=shadowPos.xyz/shadowPos.w*.5+.5;
 if(p.x<0.||p.x>1.||p.y<0.||p.y>1.||p.z>1.)return 1.;
 float bias=max(.0006,.0025*(1.-max(dot(N,lightDirection),0.)));float sum=0.;
 for(int x=-2;x<=2;x++)for(int y=-2;y<=2;y++){
  float d=texture(shadowMap,p.xy+vec2(float(x),float(y))*softness/512.).r;
  sum+=(p.z-bias>d)?0.:1.;
 }return mix(1.,sum/25.,shadowStrength);
}
vec3 brdf(vec3 N,vec3 V,vec3 L,vec3 light,float strength){
 vec3 H=normalize(V+L);float NoL=max(dot(N,L),0.);float NoV=max(dot(N,V),.001);float NoH=max(dot(N,H),0.);float VoH=max(dot(V,H),0.);
 float a=max(.065,roughness*roughness);float a2=a*a;float d=NoH*NoH*(a2-1.)+1.;float D=a2/(PI*d*d);
 float k=pow(roughness+1.,2.)/8.;float G=NoV/(NoV*(1.-k)+k)*NoL/(NoL*(1.-k)+k);
 vec3 F0=mix(vec3(.04),baseColor,metalness);vec3 F=F0+(1.-F0)*pow(1.-VoH,5.);
 vec3 spec=D*G*F/max(4.*NoV*NoL,.001);
 vec3 diffuse=(1.-F)*(1.-metalness)*baseColor/PI;
 // The direct lamp supplies diffuse illumination. Its broad studio reflection is
 // evaluated below, avoiding the tiny point-source glints of the first edition.
 return diffuse*light*strength*NoL;
}
float softbox(vec3 direction,vec3 axis,float width,float height,float blur){
 vec3 tangent=normalize(cross(abs(axis.y)>.97?vec3(0.,0.,1.):vec3(0.,1.,0.),axis));
 vec3 bitangent=cross(axis,tangent);float facing=dot(direction,axis);
 if(facing<=.001)return 0.;
 vec2 uv=abs(vec2(dot(direction,tangent),dot(direction,bitangent))/facing);
 vec2 edge=1.-smoothstep(vec2(width,height)-blur,vec2(width,height)+blur,uv);
 return edge.x*edge.y;
}
vec3 studioReflection(vec3 R,float rough){
 float blur=.028+rough*rough*1.15;
 vec3 sky=mix(vec3(.09,.10,.12),vec3(.32,.35,.39),smoothstep(-.6,.9,R.y));
 float key=softbox(R,lightDirection,.34,.62,blur);
 float strip=softbox(R,normalize(vec3(1.8,1.4,-2.4)),.12,.68,blur);
 float fillbox=softbox(R,normalize(vec3(-2.6,1.2,-.3)),.36,.5,blur);
 return sky+lightColor*key*intensity*1.6+vec3(.82,.89,1.)*strip*fill*2.3+vec3(1.,.97,.92)*fillbox*fill*1.2;
}
vec3 aces(vec3 x){return clamp((x*(2.51*x+.03))/(x*(2.43*x+.59)+.14),0.,1.);}
vec3 srgb(vec3 x){return mix(12.92*x,1.055*pow(max(x,vec3(0)),vec3(1./2.4))-.055,step(vec3(.0031308),x));}
void main(){
 vec3 N=normalize(worldNormal);if(!gl_FrontFacing)N=-N;vec3 V=normalize(eye-worldPos);float shade=visibility(N);
 if(floorPass){outColor=transparent?vec4(vec3(0.),(1.-shade)*.58):vec4(srgb(groundColor*(1.-(1.-shade)*.58)),1.);return;}
 vec3 hemi=mix(vec3(.37,.40,.44),vec3(.86,.89,.94),N.y*.5+.5);
 vec3 ambient=baseColor*hemi*fill*(1.-metalness*.8);
 vec3 R=reflect(-V,N);float NoV=max(dot(N,V),0.);
 vec3 F0=mix(vec3(.04),baseColor,metalness);
 vec3 F=F0+(max(vec3(1.-roughness),F0)-F0)*pow(1.-NoV,5.);
 ambient+=studioReflection(R,roughness)*F*(1.-roughness*.57);
 vec3 color=ambient+brdf(N,V,lightDirection,lightColor,intensity)*shade;
 color+=brdf(N,V,normalize(vec3(2.,3.,-4.)),vec3(.76,.85,1.),fill*1.6);
 outColor=vec4(srgb(aces(color)),1.);
}`;
const depthVertex=`#version 300 es
layout(location=0) in vec3 position;uniform mat4 model,lightVP;void main(){gl_Position=lightVP*model*vec4(position,1.);}`;
const depthFragment=`#version 300 es
precision highp float;void main(){}`;

export class ObjectRenderer {
 constructor(canvas,options={}){
  this.canvas=canvas;this.options=options;this.state={azimuth:-40,elevation:48,intensity:3,fill:.65,warmth:.15,shadow:.55,softness:2.5,roughness:-1,metalness:-1,background:'#ebe9e2',follow:true,spin:false,explodeOnHover:true,explodeHold:false,explodeStrength:.85,...options};
  const gl=this.gl=canvas.getContext('webgl2',{antialias:true,alpha:true,preserveDrawingBuffer:true});
  if(!gl)throw Error('This preview requires WebGL 2. Try a browser with hardware acceleration enabled.');
  this.main=this.program(vertex,fragment);this.depth=this.program(depthVertex,depthFragment);
  this.uniforms={};this.parts=[];this.materials=[];this.height=2;this.yaw=0;this.pitch=0;this.targetYaw=0;this.targetPitch=0;this.baseYaw=0;this.basePitch=0;this.explosion=0;this.explosionVelocity=0;this.hovered=false;this.dirty=true;this.visible=true;this.dead=false;this.loadToken=0;
  this.reduced=matchMedia('(prefers-reduced-motion: reduce)');this.motionChange=()=>this.invalidate();this.reduced.addEventListener('change',this.motionChange);
  this.createShadow();this.floor=this.geometry(new Float32Array([-12,-.015,-12,12,-.015,-12,12,-.015,12,-12,-.015,12]),new Float32Array([0,1,0,0,1,0,0,1,0,0,1,0]),new Uint32Array([0,2,1,0,3,2]));
  gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);
  this.resize=new ResizeObserver(()=>this.invalidate());this.resize.observe(canvas);
  this.intersection=new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting;this.invalidate();});this.intersection.observe(canvas);
  this.bindInput();this.frame=0;this.tick=this.tick.bind(this);this.frame=requestAnimationFrame(this.tick);
 }
 program(vs,fs){
  const gl=this.gl,compile=(type,src)=>{const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;};
  const v=compile(gl.VERTEX_SHADER,vs),f=compile(gl.FRAGMENT_SHADER,fs),p=gl.createProgram();gl.attachShader(p,v);gl.attachShader(p,f);gl.linkProgram(p);gl.deleteShader(v);gl.deleteShader(f);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));return p;
 }
 u(program,name){const id=(program===this.main?'main:':'depth:')+name;return this.uniforms[id]??(this.uniforms[id]=this.gl.getUniformLocation(program,name));}
 geometry(p,n,idx){
  const g=this.gl,vao=g.createVertexArray();g.bindVertexArray(vao);const buffers=[];
  [p,n].forEach((data,i)=>{const b=g.createBuffer();buffers.push(b);g.bindBuffer(g.ARRAY_BUFFER,b);g.bufferData(g.ARRAY_BUFFER,data,g.STATIC_DRAW);g.enableVertexAttribArray(i);g.vertexAttribPointer(i,3,g.FLOAT,false,0,0);});
  const b=g.createBuffer();buffers.push(b);g.bindBuffer(g.ELEMENT_ARRAY_BUFFER,b);g.bufferData(g.ELEMENT_ARRAY_BUFFER,idx,g.STATIC_DRAW);g.bindVertexArray(null);return{vao,buffers,count:idx.length,type:idx instanceof Uint16Array?g.UNSIGNED_SHORT:g.UNSIGNED_INT};
 }
 disposePart(p){const g=this.gl;g.deleteVertexArray(p.vao);p.buffers.forEach(b=>g.deleteBuffer(b));}
 createShadow(){
  const g=this.gl;this.shadowTexture=g.createTexture();g.bindTexture(g.TEXTURE_2D,this.shadowTexture);g.texImage2D(g.TEXTURE_2D,0,g.DEPTH_COMPONENT24,2048,2048,0,g.DEPTH_COMPONENT,g.UNSIGNED_INT,null);
  g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,g.NEAREST);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MAG_FILTER,g.NEAREST);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_S,g.CLAMP_TO_EDGE);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_T,g.CLAMP_TO_EDGE);
  this.shadowFB=g.createFramebuffer();g.bindFramebuffer(g.FRAMEBUFFER,this.shadowFB);g.framebufferTexture2D(g.FRAMEBUFFER,g.DEPTH_ATTACHMENT,g.TEXTURE_2D,this.shadowTexture,0);g.drawBuffers([g.NONE]);g.readBuffer(g.NONE);
  if(g.checkFramebufferStatus(g.FRAMEBUFFER)!==g.FRAMEBUFFER_COMPLETE)throw Error('Unable to initialize the shadow buffer.');g.bindFramebuffer(g.FRAMEBUFFER,null);
 }
 async load(url){
  const token=++this.loadToken;const response=await fetch(url);if(!response.ok)throw Error(`Could not load model (${response.status})`);const buffer=await response.arrayBuffer();if(token!==this.loadToken||this.dead)return false;
  const dv=new DataView(buffer);if(dv.getUint32(0,true)!==0x46546c67||dv.getUint32(4,true)!==2)throw Error('Expected a binary glTF 2.0 file.');
  const length=dv.getUint32(12,true),doc=JSON.parse(new TextDecoder().decode(new Uint8Array(buffer,20,length))),binOffset=28+length;
  const accessor=(i)=>{const a=doc.accessors[i],v=doc.bufferViews[a.bufferView],offset=binOffset+(v.byteOffset||0)+(a.byteOffset||0),count=a.count*({VEC3:3,SCALAR:1}[a.type]||1);const T={5126:Float32Array,5125:Uint32Array,5123:Uint16Array}[a.componentType];if(!T)throw Error('Unsupported component type');return new T(buffer,offset,count);};
  this.parts.forEach(p=>this.disposePart(p));this.parts=[];this.materials=structuredClone(doc.materials);this.original=buffer;this.document=doc;this.binOffset=binOffset;this.height=0;
  for(const mesh of doc.meshes)for(const p of mesh.primitives){const pos=accessor(p.attributes.POSITION);let minY=Infinity;for(let i=1;i<pos.length;i+=3){this.height=Math.max(this.height,pos[i]);minY=Math.min(minY,pos[i]);}const part=this.geometry(pos,accessor(p.attributes.NORMAL),accessor(p.indices));part.minY=minY;part.material=p.material;part.explosion=mesh.extras?.explosionOffset||[0,0,0];part.layer=mesh.extras?.layer||'Object part';part.transform=I();this.parts.push(part);}
  this.baseYaw=this.targetYaw=this.yaw=0;this.basePitch=this.targetPitch=this.pitch=0;this.explosion=0;this.explosionVelocity=0;this.invalidate();return true;
 }
 set(values){Object.assign(this.state,values);this.invalidate();}
 color(slot,hex){const m=this.materials.find(m=>m.name===slot);if(m)m.pbrMetallicRoughness.baseColorFactor=[...hexLinear(hex),1];this.invalidate();}
 palette(colors){for(const [slot,hex]of Object.entries(colors))this.color(slot,hex);}
 invalidate(){this.dirty=true;}
 resetView(){this.baseYaw=this.targetYaw=0;this.basePitch=this.targetPitch=0;this.invalidate();}
 bindInput(){
  const c=this.canvas;let drag=null;
  this.onDown=e=>{drag={x:e.clientX,y:e.clientY,yaw:this.baseYaw,pitch:this.basePitch};c.setPointerCapture(e.pointerId);c.style.cursor='grabbing';};
  this.onMove=e=>{if(drag){this.baseYaw=drag.yaw+(e.clientX-drag.x)*.009;this.basePitch=Math.max(-1.1,Math.min(1.1,drag.pitch+(e.clientY-drag.y)*.006));this.targetYaw=this.baseYaw;this.targetPitch=this.basePitch;}
   else if(this.state.follow&&!this.reduced.matches&&e.pointerType!=='touch'){const r=c.getBoundingClientRect();this.targetYaw=this.baseYaw+((e.clientX-r.left)/r.width-.5)*.65;this.targetPitch=this.basePitch+((e.clientY-r.top)/r.height-.5)*.23;}this.invalidate();};
  this.onUp=()=>{drag=null;c.style.cursor='grab';};this.onLeave=()=>{if(!drag){this.targetYaw=this.baseYaw;this.targetPitch=this.basePitch;this.invalidate();}};
  this.onEnter=e=>{if(e.pointerType!=='touch'){this.hovered=true;this.invalidate();}};
  const leave=this.onLeave;this.onLeave=()=>{this.hovered=false;leave();this.invalidate();};
  this.onKey=e=>{const amount=e.shiftKey ? .35 : .12;if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home'].includes(e.key)){e.preventDefault();if(e.key==='Home')this.resetView();else{this.baseYaw+=(e.key==='ArrowLeft'?-amount:e.key==='ArrowRight'?amount:0);this.basePitch=Math.max(-1.1,Math.min(1.1,this.basePitch+(e.key==='ArrowUp'?-amount:e.key==='ArrowDown'?amount:0)));this.targetYaw=this.baseYaw;this.targetPitch=this.basePitch;this.invalidate();}}};
  c.addEventListener('pointerenter',this.onEnter);c.addEventListener('pointerdown',this.onDown);c.addEventListener('pointermove',this.onMove);c.addEventListener('pointerup',this.onUp);c.addEventListener('pointercancel',this.onUp);c.addEventListener('pointerleave',this.onLeave);c.addEventListener('keydown',this.onKey);
 }
 tick(t){
  if(this.dead)return;const delta=Math.min((t-(this.lastTime||t))/1000,.05);this.lastTime=t;
  if(this.visible&&!document.hidden){
   const explosionTarget=(this.state.explodeHold||(this.state.explodeOnHover&&this.hovered&&!this.reduced.matches))?this.state.explodeStrength:0;
   if(Math.abs(this.explosion-explosionTarget)>.0001||Math.abs(this.explosionVelocity)>.0001){
    if(this.reduced.matches){this.explosion=explosionTarget;this.explosionVelocity=0;}
    else{const dt=Math.min(delta,.025);this.explosionVelocity+=(150*(explosionTarget-this.explosion)-24*this.explosionVelocity)*dt;this.explosion+=this.explosionVelocity*dt;}
    this.dirty=true;
   }
   if(this.state.spin&&!this.reduced.matches){this.baseYaw+=delta*.3;this.targetYaw=this.baseYaw;this.dirty=true;}
   const diff=Math.abs(this.targetYaw-this.yaw)+Math.abs(this.targetPitch-this.pitch);if(diff>.0001){const k=this.reduced.matches?1:1-Math.exp(-delta*13);this.yaw+=(this.targetYaw-this.yaw)*k;this.pitch+=(this.targetPitch-this.pitch)*k;this.dirty=true;}
   if(this.dirty){this.render();this.dirty=false;}
  }this.frame=requestAnimationFrame(this.tick);
 }
 render(){
  const g=this.gl,c=this.canvas,s=this.state,dpr=Math.min(devicePixelRatio||1,2),w=this.exportSize||Math.max(1,Math.round(c.clientWidth*dpr)),h=this.exportSize||Math.max(1,Math.round(c.clientHeight*dpr));
  if(c.width!==w||c.height!==h){c.width=w;c.height=h;}
  const cy=this.height*.48,lowest=Math.min(0,...this.parts.map(p=>p.minY+p.explosion[1]*this.explosion));
  const lift=-lowest+this.explosion*.025,model=mul(translate(0,cy+lift,0),mul(rotate(this.pitch,this.yaw),translate(0,-cy,0)));
  c.dataset.layers=this.explosion>.05?'separated':'assembled';c.dataset.separation=this.explosion.toFixed(2);
  for(const part of this.parts){const [x,y,z]=part.explosion.map(v=>v*this.explosion),m=part.transform;m.set(model);m[12]+=model[0]*x+model[4]*y+model[8]*z;m[13]+=model[1]*x+model[5]*y+model[9]*z;m[14]+=model[2]*x+model[6]*y+model[10]*z;}
  const a=s.azimuth*Math.PI/180,e=s.elevation*Math.PI/180,ld=[Math.sin(a)*Math.cos(e),Math.sin(e),Math.cos(a)*Math.cos(e)];
  const lightEye=ld.map((v,i)=>v*7+(i===1?cy:0)),lightVP=mul(ortho(-3.2,3.2,-3.2,3.2,.1,16),lookAt(lightEye,[0,cy,0]));
  const eye=[3.6,cy+2.7,5.7],aspect=w/h,extent=1.55+this.explosion*.45;
  const vp=mul(ortho(-extent*Math.max(1,aspect),extent*Math.max(1,aspect),-extent/Math.min(1,aspect),extent/Math.min(1,aspect),.1,30),lookAt(eye,[0,cy,0]));
  g.bindFramebuffer(g.FRAMEBUFFER,this.shadowFB);g.viewport(0,0,2048,2048);g.clear(g.DEPTH_BUFFER_BIT);g.useProgram(this.depth);g.uniformMatrix4fv(this.u(this.depth,'lightVP'),false,lightVP);g.uniformMatrix4fv(this.u(this.depth,'model'),false,model);
  for(const p of this.parts){g.uniformMatrix4fv(this.u(this.depth,'model'),false,p.transform);g.bindVertexArray(p.vao);g.drawElements(g.TRIANGLES,p.count,p.type,0);}
  g.bindFramebuffer(g.FRAMEBUFFER,null);g.viewport(0,0,w,h);const bg=hexLinear(s.background),srgb=[1,3,5].map(i=>parseInt(s.background.slice(i,i+2),16)/255);g.clearColor(...(this.transparent?[0,0,0]:srgb),this.transparent?0:1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(this.main);
  const U=(n)=>this.u(this.main,n);g.uniform1i(U('transparent'),this.transparent?1:0);g.uniformMatrix4fv(U('vp'),false,vp);g.uniformMatrix4fv(U('lightVP'),false,lightVP);g.uniform3fv(U('eye'),eye);g.uniform3fv(U('lightDirection'),ld);
  g.uniform3fv(U('lightColor'),[1+s.warmth*.12,1-s.warmth*.09,1-s.warmth*.28]);g.uniform3fv(U('groundColor'),bg);
  for(const [name,value]of Object.entries({intensity:s.intensity,fill:s.fill,shadowStrength:s.shadow,softness:s.softness}))g.uniform1f(U(name),value);
  g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,this.shadowTexture);g.uniform1i(U('shadowMap'),0);
  g.uniformMatrix4fv(U('model'),false,I());g.uniform1i(U('floorPass'),1);g.bindVertexArray(this.floor.vao);g.drawElements(g.TRIANGLES,this.floor.count,this.floor.type,0);
  g.uniform1i(U('floorPass'),0);g.uniformMatrix4fv(U('model'),false,model);
  for(const p of this.parts){const m=this.materials[p.material].pbrMetallicRoughness;g.uniformMatrix4fv(U('model'),false,p.transform);g.uniform3fv(U('baseColor'),m.baseColorFactor.slice(0,3));g.uniform1f(U('roughness'),s.roughness<0?m.roughnessFactor:s.roughness);g.uniform1f(U('metalness'),s.metalness<0?m.metallicFactor:s.metalness);g.bindVertexArray(p.vao);g.drawElements(g.TRIANGLES,p.count,p.type,0);}g.bindVertexArray(null);
 }
 async png(size=2048){this.exportSize=size;this.transparent=true;this.render();return new Promise(resolve=>this.canvas.toBlob(blob=>{this.exportSize=0;this.transparent=false;this.render();resolve(blob);},'image/png'));}
 glb(){
  if(!this.original)throw Error('Load an object first.');const doc=structuredClone(this.document);doc.materials=structuredClone(this.materials);
  for(const m of doc.materials){if(this.state.roughness>=0)m.pbrMetallicRoughness.roughnessFactor=this.state.roughness;if(this.state.metalness>=0)m.pbrMetallicRoughness.metallicFactor=this.state.metalness;}
  const js=new TextEncoder().encode(JSON.stringify(doc)),jl=(js.length+3)&~3,binary=this.original.slice(this.binOffset),total=12+8+jl+8+binary.byteLength;
  const out=new ArrayBuffer(total),v=new DataView(out),bytes=new Uint8Array(out);v.setUint32(0,0x46546c67,true);v.setUint32(4,2,true);v.setUint32(8,total,true);v.setUint32(12,jl,true);v.setUint32(16,0x4e4f534a,true);bytes.fill(32,20,20+jl);bytes.set(js,20);v.setUint32(20+jl,binary.byteLength,true);v.setUint32(24+jl,0x004e4942,true);bytes.set(new Uint8Array(binary),28+jl);return new Blob([out],{type:'model/gltf-binary'});
 }
 dispose(){this.dead=true;cancelAnimationFrame(this.frame);this.loadToken++;this.resize.disconnect();this.intersection.disconnect();this.reduced.removeEventListener('change',this.motionChange);const c=this.canvas;[['pointerenter',this.onEnter],['pointerdown',this.onDown],['pointermove',this.onMove],['pointerup',this.onUp],['pointercancel',this.onUp],['pointerleave',this.onLeave],['keydown',this.onKey]].forEach(([n,f])=>c.removeEventListener(n,f));this.parts.forEach(p=>this.disposePart(p));this.disposePart(this.floor);this.gl.deleteTexture(this.shadowTexture);this.gl.deleteFramebuffer(this.shadowFB);this.gl.deleteProgram(this.main);this.gl.deleteProgram(this.depth);}
}
