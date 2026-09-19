/* 全流程自测：用系统自带的 Chrome（headless）+ CDP 走完分诊与训练块，逐项断言。
 * 不需要 playwright/puppeteer —— Node 22+ 自带 WebSocket，直连 CDP 即可。
 *
 *   CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
 *   "$CH" --headless=new --remote-debugging-port=9222 --user-data-dir=/tmp/cdp --no-first-run &
 *   node tools/e2e.js "$(pwd)/index.html"                              # 测本地文件
 *   node tools/e2e.js https://pumo0926-cpu.github.io/dudeshen-diagnose-demo/   # 测线上
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
  let id = 0; const waits = new Map();
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
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
  const shot = async name => {
    const r = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync('/tmp/shot-' + name + '.png', Buffer.from(r.result.data, 'base64'));
  };
  const fails = [];
  const ok = (cond, label, extra) => { console.log((cond ? '  ✓ ' : '  ✗ ') + label + (extra ? '  ' + extra : '')); if (!cond) fails.push(label); };

  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', {width: 414, height: 896, deviceScaleFactor: 2, mobile: true});
  await send('Page.navigate', {url: process.argv[2].startsWith('http') ? process.argv[2] : 'file://' + process.argv[2]});
  await sleep(900);

  console.log('\n[1] 封面');
  ok(await ev(`document.querySelector('#main').textContent.includes('先定位')`), '封面渲染');
  ok(await ev(`document.querySelectorAll('.gate').length===3`), '三道闸门卡片');
  await shot('01-intro');

  console.log('\n[2] 限时默读');
  await ev(`[...document.querySelectorAll('button')].find(b=>b.textContent.includes('开始分诊')).click()`);
  await sleep(200);
  const np = await ev(`document.querySelectorAll('.txt p').length`);
  ok(np === 24, '正文段落数=24', '实际 ' + np);
  ok(await ev(`!document.querySelector('#clock').classList.contains('hide')`), '计时器出现');
  await shot('02-read');
  await sleep(2200);                                   // 读 ~2 秒，制造「跳读型」
  await ev(`document.querySelector('#barbtn').click()`);
  await sleep(200);

  console.log('\n[3] 八道探针（故意错 L2 推断题，测跳读型判定）');
  for (let i = 0; i < 8; i++) {
    const view = await ev(`(D.dx.probe[${i}].view||'single')`);
    if (view === 'multi') {
      await ev(`document.querySelectorAll('.opt')[2].click();document.querySelectorAll('.opt')[3].click()`);
    } else if (view === 'evid') {
      await ev(`document.querySelectorAll('.opt')[0].click()`); await sleep(60);
      await ev(`document.querySelectorAll('.sent')[1].click()`);
    } else {
      const right = await ev(`D.dx.probe[${i}].ans`);
      const pick = (i >= 3 && i <= 5) ? (right + 1) % 4 : right;   // L2 三题全错
      await ev(`document.querySelectorAll('.opt')[${pick}].click()`);
    }
    await sleep(80);
    ok(await ev(`!document.querySelector('#conf').classList.contains('hide')`), '第 ' + (i+1) + ' 题出现自信度自评');
    await ev(`document.querySelectorAll('.conf button')[0].click()`);   // 全选「有把握」
    await sleep(80);
  }

  console.log('\n[4] 60 秒复述');
  ok(await ev(`!!document.querySelector('#rt')`), '复述输入框');
  await ev(`(()=>{const t=document.querySelector('#rt');t.value='我第一次值日，先扫地，遇到桌椅没对齐、垃圾在桌兜里的困难，然后陈可来了，她退着拖地，最后第二天早上什么也看不出来，我才明白干净是有人做的';t.dispatchEvent(new Event('input'))})()`);
  await sleep(150);
  const hits = await ev(`document.querySelectorAll('#hits .chip.hit').length`);
  ok(hits === 4, '复述四组关键词全命中', hits + '/4');
  await shot('03-retell');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(200);

  console.log('\n[5] B 卷重做');
  const bjTxt = await ev(`document.querySelector('#main').textContent`);
  ok(bjTxt.includes('这题再想一次') || bjTxt.includes('B 卷跳过'), 'B 卷页面');
  let guard = 0;
  while (await ev(`document.querySelector('#main').textContent.includes('这题再想一次')`) && guard++ < 8) {
    const hasSent = await ev(`!!document.querySelector('.sent')`);
    await ev(`document.querySelectorAll('.opt')[0].click()`); await sleep(60);
    if (hasSent) { await ev(`document.querySelectorAll('.sent')[1].click()`); await sleep(60); }
    const multi = await ev(`document.querySelectorAll('.opt[aria-pressed="true"]').length===1 && document.querySelector('#main').textContent.includes('请选两点')`);
    if (multi) { await ev(`document.querySelectorAll('.opt')[1].click()`); await sleep(60); }
    ok(!(await ev(`document.querySelector('#barbtn').disabled`)), 'B 卷第 ' + guard + ' 题可提交');
    await ev(`document.querySelector('#barbtn').click()`); await sleep(150);
  }
  ok(guard > 0, 'B 卷确实有重做题', guard + ' 题');

  console.log('\n[6] 词义速判');
  for (let i = 0; i < 10; i++) {
    const has = await ev(`!!document.querySelector('.opt')&&document.querySelector('#main').textContent.includes('3 秒内选')`);
    if (!has) break;
    await ev(`document.querySelectorAll('.opt')[0].click()`);
    await sleep(190);
  }
  await sleep(400);
  const repTxt = await ev(`document.querySelector('#main').textContent`);
  ok(repTxt.includes('三道闸门'), '进入诊断报告');

  console.log('\n[7] 诊断报告');
  const prof = await ev(`S.prof.name`);
  ok(!!prof, '判出画像', prof);
  ok(await ev(`document.querySelectorAll('.rules tr.hit').length===1`), '规则表只标一条判定');
  ok(await ev(`document.querySelectorAll('.meter').length>=6`), '三闸门条 + 处方条');
  ok(repTxt.includes('画像不给孩子看'), '家长/孩子话术对照');
  const M = await ev(`JSON.stringify(metrics())`);
  console.log('    实测 metrics:', M);
  await shot('04-report');
  await ev(`window.scrollTo(0,1400)`); await sleep(250); await shot('05-report-rules');

  console.log('\n[8] 训练块');
  await ev(`window.scrollTo(0,0);document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`document.querySelector('#main').textContent.includes('先押一个答案')`), '第 1 步 猜');
  await ev(`document.querySelectorAll('.opt')[1].click()`); await sleep(150);
  ok(await ev(`document.querySelectorAll('#peer .r').length===4`), '同龄人分布条');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(200);
  ok(await ev(`document.querySelector('#main').textContent.includes('理解监控')`), '第 2 步 读（P7）');
  await ev(`document.querySelectorAll('.txt p')[4].click()`); await sleep(120);
  ok(await ev(`!document.querySelector('#why').classList.contains('hide')`), '标记后出现归类');
  await ev(`document.querySelectorAll('[data-w]')[1].click()`); await sleep(120);
  await shot('06-train-read');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(200);
  ok(await ev(`document.querySelector('#main').textContent.includes('把题干圈开')`), '第 3 步 问（O1）');
  // O1 反例：多点一个无关词 → 不应判过
  await ev(`(()=>{const s=D.tr.stem;const i=s.findIndex(x=>!x.k);document.querySelector('[data-s="'+i+'"]').click()})()`);
  await ev(`(()=>{const s=D.tr.stem;['range','verb','count'].forEach(k=>{const i=s.findIndex(x=>x.k===k);document.querySelector('[data-s="'+i+'"]').click()})})()`);
  await sleep(300);
  ok(await ev(`S.tr.o1!==true && document.querySelector('#fb1').textContent.includes('还不对')`), 'O1 多点了无关词 → 判不过');
  // 取消那个无关词 → 应判过
  await ev(`(()=>{const s=D.tr.stem;const i=s.findIndex(x=>!x.k);document.querySelector('[data-s="'+i+'"]').click()})()`);
  await sleep(1100);
  ok(await ev(`S.tr.o1===true`), 'O1 三样圈全判定通过');
  ok(await ev(`document.querySelector('#main').textContent.includes('4 分，写几点')`), 'O2 关出现');
  await ev(`document.querySelector('[data-n="2"]').click()`); await sleep(900);
  ok(await ev(`S.tr.o2===true`), 'O2 判定通过');
  await ev(`document.querySelectorAll('[data-p]')[0].click();document.querySelectorAll('[data-p]')[1].click()`); await sleep(1100);
  ok(await ev(`S.tr.pts===true`), '两点选对');
  ok(await ev(`!!document.querySelector('[data-v]')`), 'O4 证据句出现');
  await shot('07-train-ask');
  await ev(`document.querySelectorAll('[data-v]')[0].click()`); await sleep(200);
  ok(await ev(`S.tr.o4===true`), 'O4 判定通过');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`document.querySelector('#main').textContent.includes('切块')`), '第 4 步 辨（P4）');
  await ev(`document.querySelector('[data-c="2"]').click()`); await sleep(120);
  await ev(`document.querySelector('[data-c="5"]').click()`); await sleep(400);
  ok(await ev(`S.tr.p4===true`), 'P4 切块判定通过');
  ok(await ev(`document.querySelectorAll('[data-t]').length===3`), '三个小标题输入框');
  await ev(`document.querySelectorAll('[data-t]').forEach((x,i)=>{x.value=['提出问题','三个原因','两面'][i];x.dispatchEvent(new Event('input'))})`);
  await ev(`(()=>{const t=document.querySelector('#main1');t.value='童年的事记得牢，是因为第一次多、情绪强、被反复讲述';t.dispatchEvent(new Event('input'))})()`);
  await sleep(250);
  ok(await ev(`S.tr.p5===true`), 'P5 主旨压缩判定通过');
  await shot('08-train-sort');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`document.querySelector('#main').textContent.includes('不可跳过')`), '第 5 步 写');
  ok(await ev(`document.querySelector('#barbtn')&&document.querySelector('#bar').classList.contains('hide')`), '未达门槛时无法继续');
  await ev(`(()=>{const t=document.querySelector('#w');t.value='我记得一年级掉了第一颗牙，可能是我妈讲得太多次了';t.dispatchEvent(new Event('input'))})()`);
  await sleep(200);
  ok(!(await ev(`document.querySelector('#bar').classList.contains('hide')`)), '满 15 字后可提交');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);

  console.log('\n[9] 收尾与面板');
  const dn = await ev(`document.querySelector('.big .n').textContent`);
  ok(dn === '6/6', '今日 6 项微技能全达标', dn);
  await shot('09-train-done');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`document.querySelectorAll('.sk').length===17`), '微技能面板 17 项');
  ok(await ev(`document.querySelectorAll('.sk .st.on').length===6`), '6 项显示已达标');
  await shot('10-skills');
  await ev(`document.querySelector('#barbtn').click()`); await sleep(250);
  ok(await ev(`document.querySelectorAll('.tl .ph').length===4`), '12 周疗程四阶段');
  await shot('11-plan');

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

  console.log('\n' + (fails.length ? '❌ 失败 ' + fails.length + ' 项：\n - ' + fails.join('\n - ') : '✅ 全部通过'));
  ws.close();
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('驱动异常：', e.message); process.exit(2); });
