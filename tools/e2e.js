/* 全流程自测：用系统自带的 Chrome（headless）+ CDP 走完孩子视角与大人视角，逐项断言。
 * 不需要 playwright/puppeteer —— Node 22+ 自带 WebSocket，直连 CDP 即可。
 *
 *   CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
 *   "$CH" --headless=new --remote-debugging-port=9222 --user-data-dir=/tmp/cdp --no-first-run &
 *   node tools/e2e.js "$(pwd)/index.html"                                      # 本地文件
 *   node tools/e2e.js https://pumo0926-cpu.github.io/dudeshen-diagnose-demo/   # 线上
 *
 * 截图落在 /tmp/shot-*.png；退出码非 0 即有断言失败。
 */
const fs = require('fs');
const BASE = 'http://127.0.0.1:9222';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const targets = await (await fetch(BASE + '/json')).json();
  const page = targets.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r));
  let id = 0; const waits = new Map(); const pageErrors = [];
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
    if (m.method === 'Runtime.exceptionThrown') pageErrors.push(JSON.stringify(m.params.exceptionDetails).slice(0, 200));
    if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
  });
  const send = (method, params = {}) => new Promise(res => {
    const i = ++id; waits.set(i, res); ws.send(JSON.stringify({id: i, method, params}));
  });
  const ev = async expr => {
    const r = await send('Runtime.evaluate', {expression: expr, returnByValue: true, awaitPromise: true});
    if (r.result && r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 400));
    return r.result.result.value;
  };
  const txt = () => ev(`document.querySelector('#main').textContent`);
  const shot = async name => {
    const r = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync('/tmp/shot-' + name + '.png', Buffer.from(r.result.data, 'base64'));
  };
  const fails = [];
  const ok = (cond, label, extra) => { console.log((cond ? '  ✓ ' : '  ✗ ') + label + (extra ? '  ' + extra : '')); if (!cond) fails.push(label); };

  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', {width: 414, height: 896, deviceScaleFactor: 2, mobile: true});
  await send('Page.navigate', {url: process.argv[2].startsWith('http') ? process.argv[2] : 'file://' + process.argv[2]});
  await sleep(1000);

  console.log('\n[1] 封面（默认＝孩子视角）');
  ok(await ev(`MODE === 'kid'`), '默认进孩子视角');
  let t = await txt();
  ok(t.includes('先读一篇'), '孩子版标题');
  ok(!/闸门|分诊|画像|测评/.test(t), '孩子封面无「闸门／分诊／画像／测评」等词');
  ok(await ev(`!document.querySelector('#mode').classList.contains('hide')`), '有「给大人看」入口');
  await shot('k01-intro');
  await ev(`document.querySelector('#mode').click()`); await sleep(200);
  ok((await txt()).includes('三道闸门') || (await txt()).includes('先定位'), '切到大人视角看到方案层');
  await ev(`document.querySelector('#mode').click()`); await sleep(200);
  ok(await ev(`MODE === 'kid'`), '能切回孩子视角');

  console.log('\n[2] 读（孩子视角不显示秒数）');
  await ev(`[...document.querySelectorAll('button')].find(b=>/开始/.test(b.textContent)).click()`);
  await sleep(300);
  ok(await ev(`document.querySelector('#clock').classList.contains('hide')`), '倒计时数字已隐藏');
  ok(await ev(`!!document.querySelector('#sf')`), '改用无数字的柔和进度条');
  ok(await ev(`[...document.querySelectorAll('.steps .lb')].map(x=>x.textContent).join('/')`) === '读一篇/答八题/说一遍/再来一次/十个词',
     '步骤条有名字，不是五根没名字的横线');
  ok(await ev(`document.querySelectorAll('.steps div')[0].classList.contains('on')`), '当前这一步高亮');
  ok(await ev(`document.querySelectorAll('.txt .pn').length === 24`), '正文 24 段都有段号①②③');
  ok(await ev(`!!document.querySelector('#quit')`), '有「读不下去了」出口');
  await shot('k02-read');
  await sleep(2000);
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);

  console.log('\n[3] 八道题（孩子视角无 L1/L2 标签）');
  t = await txt();
  ok(!/L1|L2|L3|探针|校准/.test(t), '题面不出现 L1/L2/探针/校准');
  ok(t.includes('看不到原文') && t.includes('翻回去重做'), '第 1 题先说清「凭印象答，等会儿能翻回去」');
  for (let i = 0; i < 8; i++) {
    const view = await ev(`(D.dx.probe[${i}].view||'single')`);
    if (view === 'multi') await ev(`document.querySelectorAll('.opt')[2].click();document.querySelectorAll('.opt')[3].click()`);
    else if (view === 'evid') { await ev(`document.querySelectorAll('.opt')[0].click()`); await sleep(60);
                                await ev(`document.querySelectorAll('.sent')[1].click()`); }
    else {
      const right = await ev(`D.dx.probe[${i}].ans`);
      const pick = (i >= 3 && i <= 5) ? (right + 1) % 4 : right;   // L2 三题全错
      await ev(`document.querySelectorAll('.opt')[${pick}].click()`);
    }
    await sleep(80);
    if (i === 0) ok((await txt()).includes('心里有底'), '自评问法改成「心里有底吗」');
    await ev(`document.querySelectorAll('.conf button')[0].click()`); await sleep(100);
    if (i === 2) {                                     // 返回上一题：能改，且上次选的还在
      ok(await ev(`!document.querySelector('#back').classList.contains('hide')`), '题目页有「‹ 上一步」');
      await ev(`document.querySelector('#back').click()`); await sleep(220);
      ok((await txt()).includes('这题你刚才答过'), '返回上一题：提示可以改');
      ok(await ev(`document.querySelectorAll('.opt[aria-pressed="true"]').length >= 1`), '返回上一题：上次的选择还在');
      ok(await ev(`document.querySelectorAll('.conf button[aria-pressed="true"]').length === 1`), '返回上一题：自评也恢复了');
      await ev(`document.querySelectorAll('.conf button')[0].click()`); await sleep(160);
      ok((await ev(`document.querySelector('#brand').textContent`)).includes('第 4 题'), '改完确认后回到原来的进度');
    }
  }

  console.log('\n[4] 说一遍 → 再来一次 → 十个词');
  ok(await ev(`!!document.querySelector('#rt')`), '复述输入框');
  await ev(`(()=>{const a=document.querySelector('#rt');a.value='我第一次值日，先扫地，遇到桌椅没对齐、垃圾在桌兜里的困难，然后陈可来了，她退着拖地，最后第二天早上什么也看不出来，我才明白干净是有人做的';a.dispatchEvent(new Event('input'))})()`);
  await sleep(150);
  ok(await ev(`document.querySelectorAll('#hits .chip.hit').length === 4`), '四组关键词全命中');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  let guard = 0;
  while ((await txt()).includes('这题再想一次') && guard++ < 8) {
    if (guard === 1) {
      ok((await txt()).includes('翻回去看'), '「再来一次」用孩子话说明可翻原文');
      ok((await ev(`document.querySelector('#barbtn').textContent`)).includes('先选一个'), 'B 卷未选时按钮说明为什么点不动');
    }
    const hasSent = await ev(`!!document.querySelector('.sent')`);
    await ev(`document.querySelectorAll('.opt')[0].click()`); await sleep(60);
    if (hasSent) { await ev(`document.querySelectorAll('.sent')[1].click()`); await sleep(60); }
    if ((await txt()).includes('请选两点')) { await ev(`document.querySelectorAll('.opt')[1].click()`); await sleep(60); }
    await ev(`document.querySelector('#barbtn').click()`); await sleep(160);
  }
  ok(guard > 0, '错题进入「再来一次」', guard + ' 题');
  ok((await txt()).includes('准备好了再开始'), '词义速判先给起步页，不一进来就倒计时');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok((await txt()).includes('第一题给 5 秒'), '第一题多给 2 秒');
  for (let i = 0; i < 10; i++) {
    if (!(await ev(`!!document.querySelector('.opt') && /别想太久|3 秒内选/.test(document.querySelector('#main').textContent)`))) break;
    await ev(`document.querySelectorAll('.opt')[0].click()`); await sleep(190);
  }
  await sleep(500);

  console.log('\n[5] 孩子看到的报告');
  t = await txt();
  ok(t.includes('具体做到了哪几件') && t.includes('今天最值得练的一件事'), '孩子版报告：做到了哪几件 ＋ 今天练哪一件');
  ok(!/失校准型|跳读型|散点型|三道闸门|输入闸|加工闸|输出闸|判定|处方/.test(t), '不出现画像名／闸门／判定／处方');
  ok(await ev(`document.querySelectorAll('.did').length === 5`), '五条具体行为');
  ok(await ev(`document.querySelectorAll('[data-self]').length === 5`), '有「你自己觉得呢」自评');
  await shot('k03-report');
  await ev(`document.querySelectorAll('[data-self]')[1].click()`); await sleep(200);
  ok((await txt()).includes('按你说的') || (await txt()).includes('一样'), '自评后给回应');
  ok(await ev(`S.self === 1`), '自评被记录');

  console.log('\n[5.5] 说好要讲的八道，讲评与订正');
  ok((await txt()).includes('刚才那八道，一起看一遍'), '报告页给出讲评入口');
  await ev(`document.querySelector('#toReview').click()`); await sleep(350);
  t = await txt();
  ok(t.includes('八道题，对了'), '逐题讲评页');
  ok(await ev(`document.querySelectorAll('.card .qh').length === 8`), '八道题全部列出');
  ok(await ev(`[...document.querySelectorAll('.fb.ok')].filter(x=>x.textContent.includes('正解')).length === 8`), '每道都给正解');
  ok(await ev(`document.querySelectorAll('details.ex').length >= 6`), '能展开原文出处');
  ok(await ev(`[...document.querySelectorAll('.pill')].some(x=>x.textContent.includes('你说过有底'))`), '标出「说有底却答错」的题');
  await shot('k05b-review');
  const nWrong = await ev(`S.ans.filter(a=>a&&!a.right).length`);
  ok((await ev(`document.querySelector('#barbtn').textContent`)).includes('订正'), '底部按钮进入订正', nWrong + ' 道错题');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(320);
  ok((await txt()).includes('再做一遍'), '进入订正');
  for (let k = 0; k < nWrong; k++) {
    const view = await ev(`(()=>{const w=S.ans.map((a,i)=>a&&!a.right?i:-1).filter(i=>i>=0);return D.dx.probe[w[S.fix.at]].view||'single'})()`);
    const ansIdx = await ev(`(()=>{const w=S.ans.map((a,i)=>a&&!a.right?i:-1).filter(i=>i>=0);return JSON.stringify(D.dx.probe[w[S.fix.at]].ans)})()`);
    if (view === 'multi') { const a = JSON.parse(ansIdx);
      await ev(`document.querySelectorAll('.opt')[` + a[0] + `].click()`); await sleep(80);
      await ev(`document.querySelectorAll('.opt')[` + a[1] + `].click()`);
    } else if (view === 'evid') {
      await ev(`document.querySelectorAll('.opt')[` + ansIdx + `].click()`); await sleep(80);
      await ev(`document.querySelectorAll('.sent')[1].click()`);
    } else await ev(`document.querySelectorAll('.opt')[` + ansIdx + `].click()`);
    await sleep(260);
    if (k === 0) ok((await txt()).includes('这次对了'), '订正当场给对错与解析');
    await ev(`document.querySelector('#barbtn').click()`); await sleep(300);
  }
  ok((await txt()).includes('订正完了'), '订正完成页');
  ok((await ev(`S.fix.ok`)) === nWrong, '订正结果如实统计');
  await shot('k05c-fix');
  await ev(`go('report')`); await sleep(320);

  console.log('\n[6] 同一份作答 → 大人那一层');
  await ev(`document.querySelector('#toPro').click()`); await sleep(300);
  t = await txt();
  ok(t.includes('大人看到的那一层') && t.includes('给家长看的那一页'), '大人页标明这是给家长看的，并说明孩子看到的不是这页');
  const plain = await ev(`(()=>{const c=document.querySelector('#main').cloneNode(true);c.querySelectorAll('details').forEach(d=>d.remove());return c.textContent})()`);
  ok(!/L1|L2|L3|B−A|字·分|闸门|画像|微技能|校准度/.test(plain), '家长直接看到的部分不出现 L1／B−A／闸门这类内部写法');
  ok(!plain.includes(await ev(`S.prof.name`)), '类型名不出现在家长页，只留在折叠的判定细节里');
  ok(await ev(`document.querySelectorAll('.did').length === 8`), '八件事逐条说，每条带一句「这说明什么」');
  ok(plain.includes('不预测分数') && plain.includes('不排名') && plain.includes('不给孩子贴类型'), '三条红线写在家长页上');
  ok(await ev(`!!document.querySelector('details.ex')`), '判定细节收在折叠区');
  ok(plain.includes('八道题的逐题讲评'), '家长页也能进讲评');
  ok(await ev(`document.querySelectorAll('.rules tr.hit').length === 1`), '判定规则只标一条');
  ok(await ev(`document.querySelectorAll('.meter').length >= 6`), '三闸门 + 处方条');
  ok(await ev(`!!S.prof.name`), '画像仍在内部算出', await ev(`S.prof.name`));
  await shot('k04-report-pro');
  await ev(`document.querySelector('#toKid').click()`); await sleep(300);
  ok(await ev(`MODE === 'kid'`), '能切回孩子视角');
  ok((await txt()).includes('今天最值得练的一件事'), '切回后仍是同一份作答的孩子版');

  console.log('\n[7] 训练块（孩子视角无微技能编号）');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(300);
  ok((await txt()).includes('先押一个答案'), '第 1 步 猜');
  await ev(`document.querySelectorAll('.opt')[1].click()`); await sleep(200);
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  t = await txt();
  ok(t.includes('没看懂') && !/P7|理解监控/.test(t), '第 2 步：说「标一处没看懂」，不说 P7');
  ok(t.includes('还差：') && t.includes('点一下任意一段'), '第 2 步没标时明说还差什么');
  ok(await ev(`document.querySelectorAll('.txt .pn').length === 10`), '训练篇也有段号');
  await ev(`document.querySelectorAll('.txt p')[4].click()`); await sleep(150);
  await ev(`document.querySelectorAll('[data-w]')[1].click()`); await sleep(200);
  ok(await ev(`!!document.querySelector('#kfb')`), '标完给一句正向回应');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`[...document.querySelectorAll('.steps .lb')].map(x=>x.textContent).join('')`) === '猜读问辨写', '训练块步骤条：猜读问辨写');
  await ev(`document.querySelector('#back').click()`); await sleep(250);
  ok(await ev(`!!document.querySelector('.txt p.mark')`), '返回第 2 步：标记还在');
  ok(await ev(`document.querySelectorAll('[data-w][aria-pressed="true"]').length === 1`), '返回第 2 步：归类也还在');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  t = await txt();
  ok(t.includes('一道题在问什么') && !/O1|O2|O4|题干拆解|指令动词|范围限定|数量限定/.test(t),
     '第 3 步：白话标题，无 O1／指令动词／范围限定等黑话');
  ok(await ev(`document.querySelectorAll('.slot').length === 3`), '三件事拆成三个空，一件一件填');
  ok(await ev(`document.querySelectorAll('.slot')[0].classList.contains('on')`), '当前该填哪一个有高亮');
  ok(await ev(`!!document.querySelector('.ex')`), '有「没做过？先看一个例子」');
  await ev(`(()=>{const s=D.tr.stem;const i=s.findIndex(x=>x.k==='count');document.querySelector('[data-s="'+i+'"]').click()})()`);
  await sleep(220);
  ok((await txt()).includes('等会儿才轮到它'), '顺序点错 → 告诉他现在该找哪一件');
  ok(await ev(`S.tr.o1 !== true`), '顺序错不算过');
  await ev(`(()=>{const s=D.tr.stem;const i=s.findIndex(x=>x.t==='4 分');document.querySelector('[data-s="'+i+'"]').click()})()`);
  await sleep(220);
  ok((await txt()).includes('这是分数'), '点「4 分」→ 解释为什么不是它');
  await shot('k05a-stem-slots');
  for (const kk of ['verb','range','count']) {
    await ev(`(()=>{const s=D.tr.stem;const i=s.findIndex(x=>x.k==='${kk}');document.querySelector('[data-s="'+i+'"]').click()})()`);
    await sleep(260);
  }
  ok(await ev(`S.tr.o1 === true`), '三件按顺序填齐 → 判过');
  ok(await ev(`document.querySelectorAll('.slot.done').length === 3`), '三个空都填上了');
  ok(await ev(`!!document.querySelector('#g1')`), '第 ② 关出现了');
  ok((await txt()).includes('这一关过了，下面是第 ② 关'), '明说「下面是第 ② 关」');
  ok(await ev(`[...document.querySelectorAll('#fb1 ~ button, .cta.ghost')].some(b=>/去第 ② 关/.test(b.textContent))`), '给了「去第 ② 关」按钮');
  ok(await ev(`document.querySelector('#g0 .pill').textContent.includes('完成')`), '第 ① 关标成「✓ 完成」');
  ok(await ev(`document.querySelector('#g1 .pill').textContent.includes('现在')`), '第 ② 关标成「现在这关」');
  await ev(`document.querySelector('[data-n="2"]').click()`); await sleep(900);
  ok(await ev(`S.tr.o2 === true`), '4 分 → 2 点');
  await ev(`document.querySelectorAll('[data-p]')[0].click();document.querySelectorAll('[data-p]')[1].click()`); await sleep(1100);
  ok(await ev(`S.tr.pts === true`), '两点选对');
  await shot('k05-train-ask');
  await ev(`document.querySelectorAll('[data-v]')[0].click()`); await sleep(250);
  ok(await ev(`S.tr.o4 === true`), '证据句挂对');
  ok(await ev(`document.querySelectorAll('#g2 details, #g3 details').length >= 2`), '第③④关能就地翻到第⑤⑥段');
  ok(await ev(`document.querySelectorAll('#g3 .sent .pn').length === 4`), '证据句标了段号');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(300);
  ok((await txt()).includes('切成三块'), '第 4 步 辨');
  await ev(`document.querySelector('#back').click()`); await sleep(280);
  ok(await ev(`document.querySelectorAll('.slot.done').length === 3 && !!document.querySelector('#g3')`), '返回第 3 步：四关进度全在');
  ok(await ev(`document.querySelectorAll('.sent[aria-pressed="true"]').length === 1`), '返回第 3 步：选过的证据句还在');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(280);
  ok((await txt()).includes('切成三块'), '再前进回第 4 步');
  await ev(`document.querySelector('[data-c="2"]').click()`); await sleep(150);
  await ev(`document.querySelector('[data-c="5"]').click()`); await sleep(500);
  ok(await ev(`S.tr.p4 === true`), '切块判过');
  await ev(`document.querySelectorAll('[data-t]').forEach((x,i)=>{x.value=['提出问题','三个原因','两面'][i];x.dispatchEvent(new Event('input'))})`);
  await ev(`(()=>{const a=document.querySelector('#main1');a.value='童年的事记得牢，是因为第一次多、情绪强、被反复讲述';a.dispatchEvent(new Event('input'))})()`);
  await sleep(250);
  ok(await ev(`S.tr.p5 === true`), '一句话主旨判过');
  // 曾经静默卡死的三条路径：不含关键词 / 超 30 字 / 少填一个小标题
  const sortCase = async (titles, main) => {
    await ev(`document.querySelectorAll('[data-t]').forEach((x,i)=>{x.value=${JSON.stringify(titles)}[i];x.dispatchEvent(new Event('input'))})`);
    await ev(`(()=>{const a=document.querySelector('#main1');a.value=${JSON.stringify(main)};a.dispatchEvent(new Event('input'))})()`);
    await sleep(200);
    return {blocked: await ev(`document.querySelector('#bar').classList.contains('hide')`),
            hint: await ev(`['#need','#fb6'].map(q=>document.querySelector(q)?document.querySelector(q).textContent.trim():'').filter(Boolean).join(' ')`)};
  };
  let c = await sortCase(['提出问题','三个原因','两面'], '小时候的事记得特别清楚，因为第一次多、情绪强、常被提起');
  ok(!c.blocked && c.hint.includes('够了，可以往下走'), '主旨没带关键词：能走，并说明怎样更好');
  c = await sortCase(['提出问题','三个原因','两面'], '童年的事之所以记得特别牢，是因为第一次特别多、情绪来得猛，而且总是被家里人反复提起');
  ok(!c.blocked && /删到 30 字以内/.test(c.hint), '主旨写太长：能走，并提示删到 30 字内');
  c = await sortCase(['提出问题','三个原因',''], '童年的事记得牢，是因为第一次多');
  ok(c.blocked && c.hint.includes('还有 1 块没起名字'), '少填一个小标题：挡住，但说清还差什么');
  c = await sortCase(['提出问题','三个原因','两面'], '童年的事记得牢，是因为第一次多、情绪强、被反复讲述');
  ok(!c.blocked, '填齐后恢复可继续');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(300);
  t = await txt();
  ok(t.includes('写一句') && !/效应量|ES≈/.test(t), '第 5 步：不对孩子讲效应量');
  ok(await ev(`document.querySelector('#bar').classList.contains('hide')`), '不满 15 字不能收工');
  await ev(`(()=>{const a=document.querySelector('#w');a.value='才写了几个字';a.dispatchEvent(new Event('input'))})()`);
  await sleep(150);
  ok((await txt()).includes('还差'), '第 5 步告诉还差几个字');
  await ev(`(()=>{const a=document.querySelector('#w');a.value='我记得一年级掉了第一颗牙，可能是我妈讲得太多次了';a.dispatchEvent(new Event('input'))})()`);
  await sleep(200);
  ok(!(await ev(`document.querySelector('#bar').classList.contains('hide')`)), '满 15 字可收工');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(350);

  console.log('\n[7.5] 写完那句话，先有回应');
  t = await txt();
  ok(t.includes('第一颗牙'), '把孩子写的那句原样摆出来');
  ok(await ev(`document.querySelectorAll('.did').length === 3`), '针对这句话给三条回应');
  ok(t.includes('别人写了什么'), '给同龄人样例做对照');
  ok(t.includes('Demo 不联网、不接 AI'), '如实说明这几条是按字面算的');
  await shot('k06a-writeback');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(350);

  console.log('\n[8] 孩子看到的收尾');
  t = await txt();
  ok((await ev(`document.querySelector('.big .n').textContent`)) === '今天读完了', '收尾是「今天读完了」而不是分数');
  ok(await ev(`document.querySelectorAll('.did').length === 7`), '七件具体做到的事');
  ok(await ev(`document.querySelectorAll('.did .m:not(.no)').length === 7`), '七件全做到');
  ok(!/P7|O1|O2|O4|P4|P5|微技能|达标/.test(t), '不出现微技能编号与「达标」');
  ok(t.includes('断一天也不清零'), '明确「断了能接上」');
  ok(t.includes('第一颗牙'), '结算页留住今天写的那句话');
  ok(t.includes('今天要钉正的'), '结算页有钉正区');
  const nTodo = await ev(`document.querySelectorAll('[data-fix]').length`);
  ok(t.includes('七件全做到了') || nTodo > 0, '没做到的每件都给正解与「回去改一下」入口', nTodo + ' 件待钉正');
  await shot('k06-train-done');

  console.log('\n[9] 大人那一层：面板与疗程');
  await ev(`document.querySelector('#toPro').click()`); await sleep(300);
  ok(await ev(`MODE === 'pro'`), '进入大人视角');
  ok(await ev(`document.querySelectorAll('.sk').length === 17`), '17 个微技能');
  ok(await ev(`document.querySelectorAll('.sk .st.on').length === 6`), '6 项标已达标');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(300);
  ok(await ev(`document.querySelectorAll('.tl .ph').length === 4`), '12 周疗程四阶段');
  await shot('k07-plan');

  console.log('\n[10] 判定规则单元测试（注入极端数据）');
  const cases = [
    ['基础薄弱型', `S.read={sec:120,over:false};S.vocab.right=3;S.ans=D.dx.probe.map((p,i)=>({conf:0,right:i>2}));S.retell.hit=[1,1,0,0];S.bj={redone:2,fixed:0}`],
    ['失校准型',   `S.read={sec:120,over:false};S.vocab.right=9;S.ans=D.dx.probe.map((p,i)=>({conf:1,right:i>4}));S.retell.hit=[1,1,1,1];S.bj={redone:0,fixed:0}`],
    ['慢读型',     `S.read={sec:400,over:true};S.vocab.right=9;S.ans=D.dx.probe.map((p,i)=>({conf:0,right:i>1}));S.retell.hit=[1,1,1,0];S.bj={redone:2,fixed:0}`],
    ['散点型',     `S.read={sec:150,over:false};S.vocab.right=9;S.ans=D.dx.probe.map((p,i)=>({conf:0,right:i<3||i>5}));S.retell.hit=[1,0,0,0];S.bj={redone:1,fixed:0}`],
    ['搬运型',     `S.read={sec:150,over:false};S.vocab.right=9;S.ans=D.dx.probe.map((p,i)=>({conf:0,right:i<6}));S.retell.hit=[1,1,1,1];S.bj={redone:1,fixed:0}`],
    ['暂未偏科',   `S.read={sec:150,over:false};S.vocab.right=9;S.ans=D.dx.probe.map(()=>({conf:0,right:true}));S.retell.hit=[1,1,1,1];S.bj={redone:0,fixed:0}`],
  ];
  for (const [want, setup] of cases) {
    const got = await ev(setup + `;D.profiles.find(p=>p.k===judge(metrics()).key).name`);
    ok(got === want, '判定 → ' + want, got === want ? '' : '得到 ' + got);
  }
  console.log('\n[11] 孩子版文案完整性');
  for (const k of ['slow','skim','scatter','copy','miscal','base','even']) {
    const has = await ev(`(()=>{const p=D.profiles.find(x=>x.k==='${k}');return !!(p.kid&&p.kidwhy&&p.kid.length>6&&p.kidwhy.length>10)})()`);
    ok(has, '画像 ' + k + ' 有孩子版说法');
  }
  ok(pageErrors.length === 0, '全程无页面异常', pageErrors[0] || '');

  console.log('\n' + (fails.length ? '❌ 失败 ' + fails.length + ' 项：\n - ' + fails.join('\n - ') : '✅ 全部通过'));
  ws.close();
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('驱动异常：', e.message); process.exit(2); });
