// Smile the actual EE lips and squint the crescent eyes without folding the surface.
const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
export function smileLift(x,y){const edge=Math.min(1,Math.abs(x)/.95);const mouth=smooth(.12,.24,y)*(1-smooth(.53,.72,y));const eyes=smooth(.62,.73,y)*(1-smooth(.90,1.02,y));return mouth*(.075*edge**1.6-.018*(1-edge))-eyes*.18*(y-.78);}
export function smileStrength(time,greeting,reduced=false){return reduced?0:.12+.18*(.5-.5*Math.cos(time*Math.PI*2/4.4))+.7*Math.max(0,Math.min(1,greeting));}
