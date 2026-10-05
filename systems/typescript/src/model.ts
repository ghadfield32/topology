namespace Shape {
 export interface Point {time:number;x:number;y:number;z:number;confidence?:number|null}
 export interface Trajectory {schema:'shape.systems.trajectory.v1';units:'m';observed:Point[];predicted:Point[];metadata:{limitations:string[];[key:string]:unknown}}
 export type State={status:'loading'}|{status:'success';trajectory:Trajectory}|{status:'failure';error:string};
 const record=(x:unknown):x is Record<string,unknown>=>typeof x==='object'&&x!==null&&!Array.isArray(x);
 const number=(x:unknown):x is number=>typeof x==='number'&&Number.isFinite(x);
 function points(x:unknown):Point[]{
  if(!Array.isArray(x)||x.length===0||x.length>1_000_000)throw Error('A bounded nonempty trajectory is required');
  let last=-Infinity;return x.map((p:unknown)=>{
   if(!record(p)||!number(p.time)||!number(p.x)||!number(p.y)||!number(p.z)||p.time<=last)throw Error('Point must have finite coordinates and increasing time');
   if(p.confidence!==undefined&&p.confidence!==null&&(!number(p.confidence)||p.confidence<0||p.confidence>1))throw Error('Confidence must be null or in [0,1]');
   last=p.time;return {time:p.time,x:p.x,y:p.y,z:p.z,confidence:p.confidence as number|null|undefined};
  });
 }
 export function validate(x:unknown):Trajectory{
  if(!record(x)||x.schema!=='shape.systems.trajectory.v1'||x.units!=='m')throw Error('Expected shape.systems.trajectory.v1 in metres');
  if(!record(x.metadata)||!Array.isArray(x.metadata.limitations)||!x.metadata.limitations.every(v=>typeof v==='string'))throw Error('Documented limitations required');
  return {schema:x.schema,units:x.units,observed:points(x.observed),predicted:points(x.predicted),metadata:{...x.metadata,limitations:x.metadata.limitations as string[]}};
 }
 export function project(p:Point,yaw:number):[number,number]{return [Math.cos(yaw)*p.x+Math.sin(yaw)*p.y,p.z]}
 export function describe(s:State):string {switch(s.status){case 'loading':return 'Loading';case 'failure':return s.error;case 'success':return `${s.trajectory.observed.length} observed records; ${s.trajectory.predicted.length} predicted records`;}}
}
