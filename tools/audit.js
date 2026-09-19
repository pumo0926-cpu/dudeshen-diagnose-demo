/* 黑话体检：把孩子视角的每一屏都渲染一遍，检查有没有漏出内部术语。
 * 孩子看到的任何一屏，都不该出现靶点/微技能/画像/校准/L1/O1/效应量这类词。
 *
 *   node tools/audit.js "$(pwd)/index.html"      （需先起 headless Chrome，见 e2e.js 头部）
 */
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const t=(await (await fetch('http://127.0.0.1:9222/json')).json()).find(x=>x.type==='page');
const ws=new WebSocket(t.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r));
let id=0;const w=new Map();ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}});
const send=(method,params={})=>new Promise(res=>{const i=++id;w.set(i,res);ws.send(JSON.stringify({id:i,method,params}));});
const ev=async e=>(await send('Runtime.evaluate',{expression:e,returnByValue:true})).result.result.value;
await send('Page.enable');await send('Runtime.enable');
await send('Page.navigate',{url:'file://'+process.argv[2]});await sleep(900);
// 黑话清单：产品内部术语 / 教研术语 / 研究术语
const JARGON=['靶点','微技能','校准','闸门','分诊','画像','探针','效应量','ES≈','踩点给分','赋分','指令动词','范围限定','数量限定','元认知','盲测','北极星','处方','判定','文本证据','迁移','达标','L1','L2','L3','O1','O2','O4','P4','P5','P7','对接口','可判定'];
const screens=[['intro',''],['read',''],['retell',''],['vocab',''],['report','S.ans=D.dx.probe.map((p,i)=>({conf:0,right:i%2===0}));S.read={sec:180,over:false};S.retell.hit=[1,1,1,0];S.vocab.right=8;S.bj={redone:2,fixed:1};'],
 ['train0','S.tr={};'],['train1','S.tr={};'],['train2','S.tr={};'],['train3','S.tr={};'],['train4','S.tr={};'],['tdone','S.tr={markWhy:1,o1:1,o2:1,o4:1,p4:1,p5:1,write:1};']];
let bad=0;
for(const [name,setup] of screens){
  const isTrain=name.startsWith('train');
  const expr=`MODE='kid';${setup}${isTrain?`go('train',${name.slice(5)})`:`go('${name}')`};'ok'`;
  await ev(expr); await sleep(350);
  const txt=await ev(`document.querySelector('#main').textContent+' '+document.querySelector('#brand').textContent`);
  const hits=JARGON.filter(j=>txt.includes(j));
  console.log((hits.length?'  ✗ ':'  ✓ ')+name.padEnd(8)+(hits.length?'  出现黑话: '+hits.join('、'):''));
  if(hits.length)bad++;
}
console.log(bad?`\n孩子视角仍有 ${bad} 屏含黑话`:'\n✅ 孩子视角全程无内部术语');
process.exit(bad?1:0);})();
