/* 体验探针：按「孩子此刻会不会不知道该干什么／白做了」逐屏查阻碍点与损耗点。
 * 对应文档 12-答题动线审计-阻碍点与体验损耗.md 的九条，全部修完后应当一条都不报。
 *
 *   node tools/friction.js "$(pwd)/index.html"     （需先起 headless Chrome，见 e2e.js 头部）
 */
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const t=(await (await fetch('http://127.0.0.1:9222/json')).json()).find(x=>x.type==='page');
const ws=new WebSocket(t.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r));
let id=0;const w=new Map();ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&w.has(m.id)){w.get(m.id)(m);w.delete(m.id);}});
const send=(m,p={})=>new Promise(r=>{const i=++id;w.set(i,r);ws.send(JSON.stringify({id:i,method:m,params:p}));});
const ev=async e=>(await send('Runtime.evaluate',{expression:e,returnByValue:true})).result.result.value;
await send('Page.enable');await send('Runtime.enable');
await send('Page.navigate',{url:'file://'+process.argv[2]});await sleep(900);
const chk=(t,v)=>console.log(`  ${v?'⚠️':'  '} ${t}`);
// 1 答题页能不能看到原文
await ev(`MODE='kid';S.ans=[];go('q',0)`);await sleep(250);
chk('答题页看不到原文，且没有一句话说明「凭印象答」', !(await ev(`/原文|凭印象|等会儿/.test(document.querySelector('#main').textContent)`)));
// 2 多选题点第三个
await ev(`go('q',7)`);await sleep(250);
await ev(`[0,1,2].forEach(i=>document.querySelectorAll('.opt')[i].click())`);await sleep(150);
chk('多选点第 3 个时静默忽略，没有提示', (await ev(`document.querySelectorAll('.opt[aria-pressed="true"]').length`))===2 && !(await ev(`/最多/.test(document.querySelector('#main').textContent)`)));
// 3 证据句有没有段号
await ev(`go('q',6)`);await sleep(250);
await ev(`document.querySelectorAll('.opt')[0].click()`);await sleep(200);
chk('六句证据没有段号，得凭记忆定位', (await ev(`document.querySelectorAll('#ev .sent .pn').length`)) < 6);
// 4 复述到点会不会被强制打断
await ev(`go('retell')`);await sleep(200);
chk('复述 60 秒到点直接跳走，正在打字会被打断', (await ev(`(()=>{const s=scRetell.toString();return /runClock\\(-1, 60, 0, \\(\\) => \\{ done\\(\\); \\}\\)/.test(s)})()`)));
// 5 词义速判有没有起步缓冲
chk('词义速判进页面立刻 3 秒倒计时，第一题常常没看清', (await ev(`/runClock\\(-1, 3, 0/.test(scVocab.toString())`)));
// 6 训练第 2 步有没有「都懂」的出路
await ev(`S.tr={};go('train',1)`);await sleep(250);
chk('必须标一处没看懂，真都懂的孩子只能乱标', !(await ev(`/都懂|没有不懂/.test(document.querySelector('#main').textContent)`)));
// 7 第 3 步第③关能不能看到第④⑤段
await ev(`S.tr={ask:{phase:3,cnt:2,pts:[],ev:null,slotIdx:3,filled:['说说','第④⑤段','答两点'],used:[2,1,6]}};go('train',2)`);await sleep(300);
chk('第③关要求「结合第④⑤段」，但页面上看不到那两段', !(await ev(`document.querySelector('#g2') && /被取用得越多|每取出来一次/.test(document.querySelector('#g2').textContent)`)));
// 8 写完之后有没有对「那句话」的回应
await ev(`S.tr={write:true,writeText:'我记得一年级掉了第一颗牙，可能是我妈讲得太多次了'};go('wfb')`);await sleep(300);
chk('写完那句话没有任何回应', !(await ev(`document.querySelector('#main').textContent.includes('第一颗牙')`)));
await ev(`go('tdone')`);await sleep(300);
chk('写完那句话，结算页一个字都没提它', !(await ev(`document.querySelector('#main').textContent.includes('第一颗牙')`)));
chk('结算页没留住今天写的那句', !(await ev(`document.querySelector('#main').textContent.includes('第一颗牙')`)));
process.exit(0);})();
