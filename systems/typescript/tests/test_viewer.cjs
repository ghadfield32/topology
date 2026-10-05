const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const context={console};vm.runInNewContext(fs.readFileSync(process.argv[2]||'build/shape.js','utf8'),context);const S=context.Shape;
const p={time:0,x:1,y:2,z:3,confidence:null};const valid={schema:'shape.systems.trajectory.v1',units:'m',observed:[p],predicted:[p],metadata:{limitations:['small excerpt']}};
assert.equal(S.validate(valid).observed.length,1);
for(const modify of [v=>v.units='ft',v=>v.observed[0].x=NaN,v=>v.observed[0].confidence=2,v=>v.predicted=[],v=>v.schema='bad',v=>v.observed.push({...v.observed[0]})]){const v=JSON.parse(JSON.stringify(valid));modify(v);assert.throws(()=>S.validate(v));}
assert.equal(S.describe({status:'loading'}),'Loading');assert.equal(S.describe({status:'failure',error:'bad'}),'bad');
const q=S.project({time:0,x:1,y:2,z:3},0);assert.equal(q[0],1);assert.equal(q[1],3);
console.log('10 TypeScript runtime-contract checks passed');
