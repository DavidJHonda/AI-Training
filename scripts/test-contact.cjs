const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict'),crypto=require('crypto'),path=require('path');
const source=fs.readFileSync(path.join(__dirname,'..','google-apps-script.gs'),'utf8');
function fixture(){const props={},cache={},sent=[];let fail=false,quota=100,released=0;
const context={console:{error(){}},ContentService:{MimeType:{JSON:'json'},createTextOutput:v=>({value:v,setMimeType(){return this;}})},LockService:{getScriptLock:()=>({waitLock(){},releaseLock(){released++}})},PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k]||null,setProperty:(k,v)=>props[k]=v,getProperties:()=>({...props}),deleteProperty:k=>delete props[k]})},CacheService:{getScriptCache:()=>({get:k=>cache[k]||null,put:(k,v)=>cache[k]=v})},Utilities:{DigestAlgorithm:{SHA_256:'sha256'},computeDigest:(_,text)=>crypto.createHash('sha256').update(text).digest(),base64EncodeWebSafe:b=>Buffer.from(b).toString('base64url')},MailApp:{getRemainingDailyQuota:()=>quota,sendEmail:(...args)=>{if(fail)throw Error('mail error');sent.push(args)}}};
vm.createContext(context);vm.runInContext(source,context);
return {context,props,cache,sent,setFail:v=>fail=v,setQuota:v=>quota=v,get released(){return released},post:data=>context.doPost({postData:{contents:JSON.stringify(data)}}).value};}

const payload=()=>({eventType:'course_contact',reportId:crypto.randomUUID(),clientId:crypto.randomUUID(),name:'Test Teacher',email:'teacher@example.com',message:'Can our class use the course?',website:''});
let f=fixture(),p=payload();
assert.equal(f.context.doGet({parameter:{action:'contact_status'}}).value,'contact-ready');
assert.equal(f.post(p),'contact-ok');
assert.equal(f.sent.length,1);
assert.equal(f.sent[0][0].to,'besmarterthanthetool@gmail.com');
assert.equal(f.sent[0][0].replyTo,p.email);
assert(f.sent[0][0].body.includes(p.message));
assert.equal(f.post({...p,to:'elsewhere@example.com'}),'contact-ok');
assert.equal(f.sent.length,1,'Retries do not send twice');
assert.equal(f.post({...p,email:'other@example.com'}),'error');
assert(!JSON.stringify(f.props).includes(p.email),'No email stored in script properties');
assert(!JSON.stringify(f.props).includes(p.message),'No message stored in script properties');
for(const bad of [{email:''},{email:'invalid'},{email:'a@example.com,b@example.com'},{email:'a@example.com\r\nBcc: b@example.com'},{name:'Name\nHeader'},{name:'x'.repeat(101)},{message:''},{message:'x'.repeat(5001)},{website:'spam'},{reportId:''},{clientId:''}]) {
 assert.equal(f.post({...payload(),...bad}),'error');
}
assert.equal(f.sent.length,1,'Invalid requests do not send');
f=fixture(); assert.equal(f.post({...payload(),name:''}),'contact-ok');
f=fixture();p=payload();f.setFail(true);assert.equal(f.post(p),'error');assert.equal(Object.keys(f.props).length,0);f.setFail(false);assert.equal(f.post(p),'contact-ok');assert.equal(f.sent.length,1);assert.equal(f.released,2);
f=fixture();const client=crypto.randomUUID();for(let i=0;i<3;i++)assert.equal(f.post({...payload(),clientId:client}),'contact-ok');assert.equal(f.post({...payload(),clientId:client}),'error');
f=fixture();f.props['course-contact-budget']=JSON.stringify({day:new Date().toISOString().slice(0,10),count:20});assert.equal(f.post(payload()),'error');assert.equal(f.sent.length,0);
f=fixture();f.setQuota(10);assert.equal(f.post(payload()),'error');assert.equal(f.sent.length,0);
console.log('PASS: contact readiness, fixed recipient, Reply-To, validation, retry deduplication, failed-send retry, privacy and sending limits.');
