# -*- coding: utf-8 -*-
"""生成「三道闸门 · 初一分诊与训练 Demo」单文件 H5。
选文与题目取自 ../content/month01.json（08 内容库），分诊探针与训练靶点按 09 方案手写。
用法：python3 tools/build.py   （路径由脚本位置推出，可在任意 cwd 下运行）
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)                     # h5-diagnose-demo/
ROOT = os.path.dirname(OUT_DIR)                     # 项目根
CONTENT = os.path.join(ROOT, 'content', 'month01.json')

db = json.load(open(CONTENT, encoding='utf-8'))
item = lambda i: [x for x in db['items'] if x['id'] == i][0]
DX, TR = item('4-1'), item('2-3')

# ── 分诊探针（8 题，全部可自动判定；L1×3 事实 / L2×3 推断与结构 / L3×2 证据与要点）──
PROBE = [
 dict(layer="L1", tag="事实检索", q="「我」扫地时遇到的困难，下面哪一项<b>不是</b>文中提到的？",
      opts=["桌椅不是摆好的，要先对齐","垃圾不在地上，在桌兜里","垃圾桶满了，扫拢的一堆没处放","扫把太短，弯腰太累"], ans=3,
      why="文章用「第一、第二、第三」明明白白列了三个困难：桌椅要先对齐、垃圾在桌兜里、垃圾桶满了没处放。「扫把太短」全文没出现——这种题就是考你有没有真的按顺序读下来。", src=[4,5,6]),
 dict(layer="L1", tag="事实检索", q="陈可把拖把挂回墙角时，说了哪四个字？",
      opts=["「你扫你的」","「下次好拿」","「拖之前」","「我没看见」"], ans=1,
      why="挂拖把时她把把手朝外，说的是「下次好拿」。别的三句她也说过，但都在前面的对话里——这题考的是能不能把话和场景对上。", src=[18]),
 dict(layer="L1", tag="事实检索", q="陈可拖地的方向是——",
      opts=["从门口往最里面拖","等「我」全部扫完再从头拖","从最里面往外退着拖","和「我」一起从中间往两边拖"], ans=2,
      why="原文写「一排一排往外退，退到哪儿，哪儿的地就变成干净的深色」。退着拖，才不会踩脏刚拖过的地——她做事的顺序感就藏在这一句里。", src=[11]),
 dict(layer="L2", tag="动机推断", q="「我」问「你什么时候摆的？」陈可答「拖之前」。这段对话让你看出陈可做事的什么特点？",
      opts=["她想抢在「我」前面表现","她心里有顺序，而且做在别人看见之前","她怕老师检查不合格","她想早点做完回家"], ans=1,
      why="「我」问她什么时候摆的，她答「拖之前」；「我」说没看见，她答「你在扫第三排」——她不但做了，还清楚地知道自己什么时候做的。<b>做在别人看见之前</b>，这是全篇写她的核心。", src=[12,13,14,15,16]),
 dict(layer="L2", tag="段落作用", q="第二天早上「结果什么也看不出来」这一段，在全文里起什么作用？",
      opts=["交代时间，让故事有头有尾","说明这间教室平时就很干净","用「看不出来」反过来显出这件事的性质：做得好的值日是不留痕迹的","为了写「我」比平时早到十分钟"], ans=2,
      why="如果第二天一眼就能看出「昨天有人打扫过」，这件事反而不值得写。正因为<b>什么也看不出来</b>，才显出：干净是天天有人做出来的，只是没人看见。段落作用题，要问的是「去掉这一段，文章少了什么」。", src=[20,21,22]),
 dict(layer="L2", tag="结构顺序", q="全文是按什么顺序写的？",
      opts=["倒叙：先写第二天早上，再回头写值日那天","按时间顺序：值日表 → 扫地遇到困难 → 陈可来了 → 第二天早上","插叙：中间插入陈可平时的表现","按空间顺序：从教室后面写到讲台"], ans=1,
      why="从「开学第三周，轮到我值日」一路写到「第二天早上」，中间没有回跳，是<b>顺叙</b>。判断顺序最快的办法：找时间词（放学铃响、等我扫到最后一排、全部弄完、第二天早上）。", src=[0,2,17,20]),
 dict(layer="L3", tag="证据挂钩", q="作者靠什么把「话极少」的陈可写清楚？<br>先选观点，再从原文里<b>点一句</b>作证据。",
      view="evid", opts=["靠动作和做事的顺序","靠外貌描写","靠别人对她的评价"], ans=0,
      why="她全文只说了四句话。作者写她，靠的全是动作：退着拖、拖把拧到一滴水不掉、把手朝外挂回去、踮脚擦最上面一行。<b>写人不一定靠写话，动作更耐看。</b>", src=[11,17,18]),
 dict(layer="L3", tag="要点数", q="「每一个『本来』的背后，都有一个人。」这句话在说什么？<br><b>本题 4 分，请选两点。</b>",
      view="multi", opts=["我们习以为常的「干净」，其实都是有人做出来的",
                          "这些人做完就走，不被看见，所以才成了「本来」",
                          "教室每天都需要有人打扫",
                          "陈可比「我」更会做值日"], ans=[0,1],
      why="4 分题要写两点，而且这两点必须是<b>一句话的两层意思</b>：①「本来就干净」其实是有人做的；②做的人做完就走、不被看见，所以才会被当成「本来」。选项三只是常识，选项四跑题了——<b>要点不是想到什么写什么，是把原句拆成几层。</b>", src=[22]),
]
# L3-1 可点选的候选句（支持集＝动作/顺序类）
EVID = [
 dict(t="她坐在第一排，个子小，上课总把背挺得很直。", p=1, ok=False, why="这是外貌与坐姿，不是「动作和顺序」。"),
 dict(t="她拖的是我已经扫过的那几排，一排一排往外退，退到哪儿，哪儿的地就变成干净的深色。", p=11, ok=True, why="退着拖、跟着进度走——动作里藏着顺序。"),
 dict(t="她把拖把在水池里涮干净，拧到一滴水都不掉，挂回墙角，挂的时候把把手朝外。", p=18, ok=True, why="一连串动作，收尾还替下一个人想好了。"),
 dict(t="她说：「你扫你的。」", p=9, ok=False, why="这是语言，而且正说明她话少——证明不了「靠动作写人」。"),
 dict(t="我去倒垃圾，回来的时候她正踮着脚擦黑板的最上面一行。", p=17, ok=True, why="够不着也要擦——动作替她说话。"),
 dict(t="我跟她没说过话。", p=1, ok=False, why="这是「我」的情况，与陈可怎么做事无关。"),
]
# ── 60 秒复述：四组关键词，命中几组＝结构成形到什么程度 ──
RETELL = [
 dict(name="谁", kws=["我","陈可","她"], tip="主体"),
 dict(name="做了什么", kws=["值日","扫","拖","桌椅","对齐","垃圾","黑板","擦"], tip="主要事件"),
 dict(name="先后", kws=["先","然后","后来","接着","再","第二天","最后","开始"], tip="顺序词"),
 dict(name="为什么值得写", kws=["干净","本来","没人","看不出","痕迹","有人","习惯"], tip="主旨"),
]
# ── 词义速判（每题 3 秒；真实版 20 题，Demo 取 10 题）──
VOCAB = [
 ("她把拖把在水池里<b>涮</b>干净", ["在水里来回晃动洗净","用力拧干","用刷子使劲刷"], 0),
 ("桌兜里<b>探</b>出来的纸团", ["伸出来","探望","试探"], 0),
 ("一件在大人看来<b>微</b>不足道的事", ["细小","稍微","隐秘"], 0),
 ("《咏雪》：俄而雪<b>骤</b>", ["急、猛","停止","变小"], 0),
 ("《陈太丘与友期行》：太丘<b>舍</b>去", ["丢下、不再等","房屋","施舍"], 0),
 ("《陈太丘与友期行》：尊君在<b>不</b>", ["同「否」，表疑问","不是","不要"], 0),
 ("《陈太丘与友期行》：相<b>委</b>而去", ["丢下、舍弃","委托","觉得委屈"], 0),
 ("《陈太丘与友期行》：下车<b>引</b>之", ["拉","引用","带路"], 0),
 ("《陈太丘与友期行》：入门不<b>顾</b>", ["回头看","照顾","顾虑"], 0),
 ("她<b>踮</b>着脚擦黑板", ["抬起脚跟用脚尖站","用力跺脚","蹲下去"], 0),
]
# ── 六种画像与处方（09 §3.3）──
PROFILES = [
 dict(k="slow",  name="慢读型",   gate="输入闸", why="读得懂，但读不完",
      rx=[("配速与流畅 I1", 40), ("结构切块 P4·P5", 30), ("输出 O1·O2·O4", 30)],
      act="今天这篇，定个闹钟：两分钟读完前半段，不回头。", kid="今天这篇，前半段给自己定两分钟，读完再回头。", kidwhy="你读得挺细，就是时间不太够用。慢本身不是毛病，但卷子上得有个节奏。", pname="读得慢，时间不够用", pwhy="他读得挺细，问题是速度——卷面文字量一大就做不完，后面的题只能赶。"),
 dict(k="skim",  name="跳读型",   gate="加工闸", why="快，但只抓表层，靠猜",
      rx=[("推断 P2·P3", 50), ("理解监控 P7", 20), ("输出 O1·O4", 30)],
      act="读人物的时候，多问一句：他为什么这么做？从哪句看出来？", kid="今天这篇，碰到人物就多问一句：他为什么这么做？", kidwhy="你读得快，不过有几处是猜的。猜对了也不算真的会。", pname="读得快，但读得浅", pwhy="他读得很快，可有几处是猜的。猜对也不算会，换一篇陌生文章就露出来。"),
 dict(k="scatter",name="散点型",  gate="加工闸", why="细节都懂，抓不住整体",
      rx=[("结构切块＋概括 P4·P5", 50), ("推断 P2·P3", 20), ("输出 O2·O5", 30)],
      act="今天这篇，试着把它切成三块，每块起个六个字以内的小标题。", kid="今天这篇，试着切成三块，每块起个六个字以内的小标题。", kidwhy="文章里发生了什么你都记得，但串不成一条线——概括题就是丢在这儿。", pname="记得住细节，抓不住整体", pwhy="文章里发生了什么他都记得，但串不成一条线——概括题、主旨题最容易丢分。"),
 dict(k="copy",  name="搬运型",   gate="输出闸", why="读懂了，但答案全是原文",
      rx=[("要点化＋证据句 O4·O5", 50), ("审题 O1·O2", 30), ("推断 P3", 20)],
      act="每写一点，后面挂一句原文；挂不住的那点，八成不是答案。", kid="今天这篇，每写一点，后面挂一句原文。", kidwhy="你其实读懂了。写下来的时候整句照搬了原文，老师想看的是你自己的话，再挂一句原文。", pname="读懂了，但写不出来", pwhy="他其实读懂了，写下来却整句照搬原文。阅卷要的是自己的话＋一句原文作证。"),
 dict(k="miscal",name="失校准型", gate="加工闸", why="自我感觉良好，一对答案全错",
      rx=[("理解监控 P7", 40), ("推断 P2·P3", 30), ("输出 O4", 30)],
      act="每篇必须标出一处「我这里没懂」——标不出来才是问题。", kid="今天这篇，标出一处你没看懂的地方。", kidwhy="有几道题你觉得挺有底，其实答错了。这不是粗心——是读的时候有个地方没懂，你自己没发现。", pname="自我感觉和实际有差距", pwhy="有几道题他答完说「有把握」，其实错了。这一条最值得注意：他不知道自己没懂，也就不会回头再看。"),
 dict(k="base",  name="基础薄弱型",gate="输入闸", why="词卡住了，全线受影响",
      rx=[("词汇·语素 I2·I3", 40), ("短文流畅 I1", 30), ("最低门槛输出", 30)],
      act="遇到不认识的词先别停，用上下文换个词读下去，读完再回头查。", kid="今天这篇，遇到不认识的词先别停，用上下文猜一个，读完再回头查。", kidwhy="有几个词把你卡住了，后面一整段就跟着糊过去了。", pname="词上卡住，拖累了整篇", pwhy="有几个书面语／文言词把他卡住，后面一整段就跟着糊过去了。"),
 dict(k="even",  name="暂未偏科", gate="三闸门均衡", why="单次分诊没有测出明显短板",
      rx=[("全员必练六项", 60), ("推断 P2·P3", 20), ("知识建构（主题簇连读）", 20)],
      act="保持每篇一次输出；真实版会用两周滚动数据再判一次。", kid="今天这篇，读完写一句话，就算完成。", kidwhy="这一篇看不出明显的短板。再读两篇才作数。", pname="这次没看出明显短板", pwhy="单次分诊没测出明显弱项。再读两篇才作数——这一条我们不会拿来下结论。"),
]
# ── 17 个微技能（09 §5）──
SKILLS = [
 ("I","输入闸",[("I1","默读配速","2 分钟读完 800 字，3 道事实题对 2"),
                ("I2","难词绕行","5 处生词中 3 处能用上下文替换"),
                ("I3","实词迁移","课内实词放进新语境，连续两次 ≥80%")]),
 ("P","加工闸",[("P1","指代还原","3 处「这／其」还原全对"),
                ("P2","关系推断","3 组相邻句关系对 2，并指得出信号词"),
                ("P3","动机推断","说出动机，且挂得住一句原文"),
                ("P4","结构切块","切块与标准差 ≤1 块，小标题含动作"),
                ("P5","主旨压缩","≤30 字，含主体与主事件，不含套话"),
                ("P6","信号词扫描","圈全 ≥80%，并说得出各领起什么"),
                ("P7","理解监控","每篇标出一处没懂，并归类正确"),
                ("P8","图文互证","找出 1 处图文对应关系")]),
 ("O","输出闸",[("O1","题干拆解","指令动词／范围／数量三样圈全，连续 3 次"),
                ("O2","分值→要点数","要点数与分值匹配 ≥80%"),
                ("O3","定位区间","答前先标段落，命中 ≥70%"),
                ("O4","证据句挂钩","每点挂得住原文，空挂不算"),
                ("O5","要点表述","主体＋动作＋结果，≤25 字，不照抄"),
                ("O6","单篇配速","≤12 分钟做完，开放题不空")]),
]
STAR = {"P3","P4","P5","P7","O1","O2","O4"}
CORE = ["P4","P5","P7","O1","O2","O4"]

DATA = dict(
  dx=dict(title=DX['title'], words=DX['words'], paras=DX['text'], notes=DX['scaffold']['notes'],
          probe=PROBE, evid=EVID, retell=RETELL, vocab=VOCAB),
  tr=dict(title=TR['title'], words=TR['words'], paras=TR['text'], guess=TR['guess'],
          cuts=[2,5], tol=1,
          stemText="结合第⑤⑥段，说说这样安排有什么好处。（4 分，答两点）",
          stem=[dict(t="结合",k="",why="「结合」说的是怎么答（要用到那几段），不是让你干什么。真正的动作词在后面。"),
                dict(t="第⑤⑥段",k="range",why=""),
                dict(t="说说",k="verb",why=""),
                dict(t="这样安排",k="",why="这是题目在说「哪件事」，不是让你干的动作。"),
                dict(t="有什么好处",k="",why="这是要你回答的内容，不是动作词。"),
                dict(t="4 分",k="",why="这是分数。它能帮你推出写几点，但它本身不是「要写几点」那句话。"),
                dict(t="答两点",k="count",why="")],
          slots=[dict(k="verb",  q="要你干什么", hint="一个动词：说说 / 分析 / 概括 / 赏析…"),
                 dict(k="range", q="去哪儿找",   hint="哪几段，还是全文"),
                 dict(k="count", q="要写几点",   hint="题目直接说了几点，或者从分数推")],
          example=dict(stem="联系全文，分析题目「藤野先生」的含义。（6 分，答三点）",
                       marks=[["分析", "要你干什么"], ["联系全文", "去哪儿找"], ["答三点", "要写几点"]]),
          pts=dict(q="这样安排的好处，选两点（4 分）",
                   opts=["同一个机制的两面：先说它让记忆更牢，再说它也让记忆被改动",
                         "先立后破，把话说完整，避免「童年记忆一定准」的绝对化",
                         "说明作者也不确定，留给读者判断",
                         "为了凑够三个原因，让结构更整齐"], ans=[0,1]),
          src=[4, 5],
          evid=[dict(t="被取用得越多的记忆，越不容易丢失。", p=4, ok=True, why="这是「牢」的那一半的直接依据。"),
                dict(t="每取出来一次，记忆都有可能被改一点。", p=5, ok=True, why="这是「准」要打问号的直接依据。"),
                dict(t="童年的情绪往往来得又快又猛。", p=3, ok=False, why="这说的是第二个原因，与第三个原因的两面无关。"),
                dict(t="你可能有过这样的体验。", p=0, ok=False, why="这是开头的引入句，不是论据。")],
          mainkw=["记忆","童年","牢","准","讲","取"]),
  profiles=PROFILES, skills=SKILLS, star=sorted(STAR), core=CORE,
)

CSS = """
:root{color-scheme:light dark;
 --plane:#f9f9f7;--surface:#fcfcfb;--surface-2:#f3f2ef;
 --ink:#0b0b0b;--ink-2:#52514e;--ink-muted:#898781;
 --grid:#e1e0d9;--axis:#c3c2b7;--border:rgba(11,11,11,.10);
 --accent:#2a78d6;--accent-soft:#86b6ef;--track:#cde2fb;--wash:#eaf2fd;
 --ok:#0a7a3d;--ok-wash:#e6f4ec;--warn:#9a5b00;--warn-wash:#fbf0dd;--bad:#b3261e;--bad-wash:#fbe9e7;--r:14px}
@media (prefers-color-scheme:dark){:root{
 --plane:#0d0d0d;--surface:#1a1a19;--surface-2:#232321;
 --ink:#fff;--ink-2:#c3c2b7;--ink-muted:#898781;
 --grid:#2c2c2a;--axis:#383835;--border:rgba(255,255,255,.10);
 --accent:#3987e5;--accent-soft:#6da7ec;--track:#2c2c2a;--wash:#141c26;
 --ok:#38c172;--ok-wash:#12231a;--warn:#e0a44a;--warn-wash:#241d10;--bad:#f2685e;--bad-wash:#251413}}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{background:var(--plane);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
.app{max-width:480px;margin:0 auto;padding:0 16px 110px;min-height:100vh}
h1,h2,h3{margin:0;line-height:1.35}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
.hide{display:none!important}
.top{position:sticky;top:0;z-index:20;background:var(--plane);padding:13px 16px 10px;margin:0 -16px;border-bottom:1px solid var(--border)}
.top .row{display:flex;align-items:center;gap:10px}
.brand{font-size:16.5px;font-weight:680;letter-spacing:-.01em;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.brand s{text-decoration:none;color:var(--ink-muted);font-weight:400;font-size:12px;margin-left:6px}
.back{font-size:13.5px;color:var(--accent);flex:0 0 auto}
.clock{font-variant-numeric:tabular-nums;font-size:13px;color:var(--ink-2);background:var(--surface-2);border-radius:999px;padding:3px 10px;flex:0 0 auto}
.clock.hot{background:var(--bad-wash);color:var(--bad);font-weight:620}
.steps{display:flex;gap:5px;margin:10px 0 2px}
.steps div{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0}
.steps .bar{width:100%;height:3px;border-radius:2px;background:var(--grid)}
.steps .lb{font-size:10.5px;color:var(--ink-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.steps div.past .bar{background:var(--accent-soft)}
.steps div.past .lb{color:var(--ink-2)}
.steps div.on .bar{background:var(--accent);height:4px;margin-top:-.5px}
.steps div.on .lb{color:var(--accent);font-weight:680}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:16px;margin:12px 0}
.card.tight{padding:13px 15px}
.eyebrow{font-size:11px;letter-spacing:.14em;color:var(--ink-muted);margin:0 0 7px;text-transform:uppercase}
h2.sec{font-size:19px;font-weight:660;margin:0 0 4px;letter-spacing:-.01em}
h3.sub3{font-size:15.5px;font-weight:640;margin:18px 0 6px}
.sub{font-size:12.5px;color:var(--ink-muted);margin:0 0 12px}
p{margin:0 0 10px;font-size:15px;color:var(--ink-2)}
.hero{padding:26px 0 4px}
.hero h1{font-size:30px;font-weight:720;letter-spacing:-.02em}
.hero .lead{font-size:15px;color:var(--ink-2);margin:10px 0 0;line-height:1.75}
.tag{display:inline-block;font-size:11px;letter-spacing:.12em;color:var(--accent);background:var(--wash);border-radius:999px;padding:4px 11px;margin:0 0 12px}
.gates{display:flex;gap:8px;margin:14px 0 4px}
.gate{flex:1;background:var(--surface-2);border-radius:11px;padding:11px 9px;text-align:center}
.gate b{display:block;font-size:13.5px;font-weight:650;color:var(--ink)}
.gate span{font-size:11px;color:var(--ink-muted);line-height:1.5;display:block;margin-top:2px}
.gate i{font-style:normal;font-size:20px;font-weight:700;color:var(--accent);font-variant-numeric:tabular-nums}
.txt p{font-size:16.5px;color:var(--ink);margin:0 0 14px;line-height:2.05;text-indent:2em}
.txt p.q{position:relative}
.txt p.mark{background:var(--warn-wash);border-radius:6px;box-shadow:0 0 0 4px var(--warn-wash)}
.txt p.pick{cursor:pointer}
.txt p.pick:active{opacity:.6}
.notes{font-size:12.5px;color:var(--ink-2);background:var(--surface-2);border-left:2px solid var(--accent-soft);padding:8px 11px;border-radius:0 8px 8px 0;margin:0 0 14px}
.opt{display:block;width:100%;text-align:left;border:1px solid var(--border);background:var(--surface);border-radius:11px;padding:12px 13px;margin:0 0 8px;font-size:14.5px;color:var(--ink-2)}
.opt[aria-pressed="true"]{border-color:var(--accent);background:var(--wash);color:var(--ink)}
.opt.right{border-color:var(--ok);background:var(--ok-wash);color:var(--ink)}
.opt.wrong{border-color:var(--bad);background:var(--bad-wash);color:var(--ink)}
.opt small{display:block;font-size:11.5px;color:var(--ink-muted);margin-top:3px}
.qh{font-size:15.5px;color:var(--ink);font-weight:620;margin:14px 0 10px;line-height:1.6}
.qh small{display:block;font-weight:400;font-size:11px;color:var(--ink-muted);letter-spacing:.1em;margin-bottom:5px}
.conf{display:flex;gap:8px;margin:14px 0 0}
.conf button{flex:1;border:1px solid var(--border);background:var(--surface);border-radius:11px;padding:11px 0;font-size:14px;color:var(--ink-2);text-align:center}
.conf button:active{background:var(--wash)}
.conf button[aria-pressed="true"]{border-color:var(--accent);background:var(--wash);color:var(--ink);font-weight:620}
.cta{display:block;width:100%;background:var(--accent);color:#fff;font-size:15.5px;font-weight:620;padding:13px;border-radius:12px;margin:16px 0 0;text-align:center}
.cta[disabled]{opacity:.35}
.cta.ghost{background:var(--surface);color:var(--accent);border:1px solid var(--accent-soft)}
.link{display:block;width:100%;text-align:center;font-size:13.5px;color:var(--accent);padding:11px 0 0}
.fb{font-size:13px;border-radius:10px;padding:10px 12px;margin:10px 0 0;background:var(--surface-2);color:var(--ink-2)}
.fb.ok{background:var(--ok-wash);color:var(--ok)}
.fb.bad{background:var(--bad-wash);color:var(--bad)}
.fb b{color:inherit}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 4px;line-height:2.2}
.chip{border:1px dashed var(--axis);border-radius:8px;padding:4px 8px;font-size:14.5px;color:var(--ink-2);background:var(--surface)}
.chip[aria-pressed="true"]{border-style:solid;border-color:var(--accent);background:var(--wash);color:var(--ink);font-weight:600}
.chip.hit{border-color:var(--ok);background:var(--ok-wash);color:var(--ok)}
.chip.miss{border-color:var(--bad);background:var(--bad-wash);color:var(--bad)}
.chip.plain{border:0;padding:4px 2px;background:none}
.sent{display:block;width:100%;text-align:left;border:1px solid var(--border);background:var(--surface);border-radius:11px;padding:11px 12px;margin:0 0 7px;font-size:14px;color:var(--ink-2);line-height:1.75}
.sent[aria-pressed="true"]{border-color:var(--accent);background:var(--wash);color:var(--ink)}
.sent.right{border-color:var(--ok);background:var(--ok-wash)}
.sent.wrong{border-color:var(--bad);background:var(--bad-wash)}
textarea,input[type=text]{width:100%;border:1px solid var(--border);border-radius:11px;background:var(--surface);padding:11px;font:inherit;font-size:15px;color:var(--ink);resize:vertical}
textarea{min-height:92px}
textarea:focus,input:focus{outline:2px solid var(--accent);outline-offset:-1px}
.cnt{font-size:11.5px;color:var(--ink-muted);text-align:right;margin:4px 0 0;font-variant-numeric:tabular-nums}
.meter{margin:0 0 11px}
.meter .lab{display:flex;justify-content:space-between;font-size:12.5px;color:var(--ink-2);margin-bottom:5px}
.meter .lab b{color:var(--ink);font-variant-numeric:tabular-nums}
.meter .track{height:9px;border-radius:5px;background:var(--track);overflow:hidden}
.meter .fill{display:block;height:100%;background:var(--accent);border-radius:5px;transition:width .5s}
.meter.g .fill{background:var(--ok)}
.meter.w .fill{background:var(--warn)}
.rules{width:100%;border-collapse:collapse;font-size:13px}
.rules td{padding:9px 4px;border-bottom:1px solid var(--grid);color:var(--ink-2);vertical-align:top}
.rules tr:last-child td{border-bottom:0}
.rules .nm{color:var(--ink);font-weight:600;white-space:nowrap}
.rules .vl{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.rules tr.hit .nm{color:var(--accent)}
.rules tr.hit{background:var(--wash)}
.pill{display:inline-block;font-size:10.5px;padding:2px 7px;border-radius:999px;background:var(--surface-2);color:var(--ink-2);margin-left:6px}
.pill.on{background:var(--accent);color:#fff;font-weight:600}
.pill.ok{background:var(--ok-wash);color:var(--ok);font-weight:600}
.cut{display:flex;align-items:center;gap:8px;margin:2px 0 12px}
.cut button{flex:1;border:1px dashed var(--axis);border-radius:8px;padding:5px 0;font-size:11.5px;color:var(--ink-muted)}
.cut.on button{border-style:solid;border-color:var(--accent);color:var(--accent);background:var(--wash);font-weight:600}
.blk{border-left:3px solid var(--accent-soft);padding-left:11px;margin:0 0 12px}
.blk b{font-size:12px;color:var(--accent);display:block;margin-bottom:4px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.kv{background:var(--surface-2);border-radius:10px;padding:10px 11px}
.kv b{display:block;font-size:18px;font-weight:660;color:var(--ink);font-variant-numeric:tabular-nums}
.kv span{font-size:11px;color:var(--ink-muted)}
.sk{display:flex;align-items:flex-start;gap:9px;padding:9px 0;border-bottom:1px solid var(--grid);font-size:13.5px}
.sk:last-child{border-bottom:0}
.sk .id{flex:0 0 34px;font-size:11.5px;font-weight:660;color:var(--accent);background:var(--wash);border-radius:7px;text-align:center;padding:3px 0}
.sk .b{flex:1;min-width:0}
.sk .b b{color:var(--ink);font-size:14px;font-weight:600}
.sk .b span{display:block;font-size:11.5px;color:var(--ink-muted);line-height:1.6}
.sk .st{flex:0 0 auto;font-size:10.5px;padding:2px 7px;border-radius:999px;background:var(--surface-2);color:var(--ink-muted)}
.sk .st.on{background:var(--ok-wash);color:var(--ok);font-weight:620}
.sk .st.tr{background:var(--wash);color:var(--accent);font-weight:620}
.tl{border-left:2px solid var(--grid);margin:6px 0 0 6px;padding:0 0 0 15px}
.tl .ph{position:relative;padding:0 0 16px}
.tl .ph:before{content:"";position:absolute;left:-21px;top:5px;width:9px;height:9px;border-radius:50%;background:var(--accent)}
.tl .ph b{font-size:14.5px;color:var(--ink);font-weight:620}
.tl .ph i{font-style:normal;font-size:11.5px;color:var(--ink-muted);margin-left:6px}
.tl .ph p{margin:3px 0 0;font-size:13px}
.peer .r{display:flex;align-items:center;gap:9px;margin:0 0 6px;font-size:13px}
.peer .bar{flex:1;height:16px;border-radius:4px;background:var(--surface-2);overflow:hidden}
.peer .bar i{display:block;height:100%;background:var(--accent-soft);border-radius:0 4px 4px 0}
.peer .r.me .bar i{background:var(--accent)}
.peer .v{flex:0 0 32px;text-align:right;color:var(--ink-2);font-variant-numeric:tabular-nums}
.vs{display:grid;grid-template-columns:1fr;gap:8px}
.vs .b{border-radius:11px;padding:11px 12px;font-size:13.5px;line-height:1.7}
.vs .b.no{background:var(--bad-wash);color:var(--ink-2)}
.vs .b.yes{background:var(--ok-wash);color:var(--ink-2)}
.vs .b em{font-style:normal;display:block;font-size:11px;letter-spacing:.1em;margin-bottom:4px;color:var(--ink-muted)}
.big{text-align:center;padding:22px 0 2px}
.big .n{font-size:42px;font-weight:720;color:var(--accent);line-height:1.1}
.big .t{font-size:14px;color:var(--ink-muted);margin-top:4px}
.note{font-size:11.5px;color:var(--ink-muted);margin:10px 0 0;line-height:1.8}
.foot{font-size:11.5px;color:var(--ink-muted);text-align:center;line-height:1.95;padding:24px 0 0}
.foot a{color:var(--ink-2)}
.bar-fixed{position:fixed;left:0;right:0;bottom:0;background:var(--plane);border-top:1px solid var(--border);padding:10px 16px calc(10px + env(safe-area-inset-bottom));z-index:30}
.bar-fixed .in{max-width:480px;margin:0 auto}
.bar-fixed .cta{margin:0}
.mode{flex:0 0 auto;font-size:11.5px;color:var(--ink-muted);border:1px solid var(--border);border-radius:999px;padding:4px 10px;background:var(--surface);white-space:nowrap}
.mode b{color:var(--accent);font-weight:620}
.pn{color:var(--ink-muted);font-size:12.5px;margin-right:2px;font-variant-numeric:tabular-nums}
.soft{height:3px;border-radius:2px;background:var(--grid);overflow:hidden;margin:10px 0 0}
.soft i{display:block;height:100%;background:var(--accent-soft);width:0}
.said{background:var(--wash);border-radius:12px;padding:13px 15px;font-size:15.5px;color:var(--ink);line-height:1.8;margin:0 0 12px}
.did{display:flex;gap:10px;align-items:flex-start;padding:11px 0;border-bottom:1px solid var(--grid)}
.did:last-child{border-bottom:0}
.did .m{flex:0 0 22px;height:22px;border-radius:50%;background:var(--ok-wash);color:var(--ok);display:grid;place-items:center;font-size:12px;font-weight:700}
.did .m.no{background:var(--surface-2);color:var(--ink-muted)}
.did .t{flex:1;font-size:14.5px;color:var(--ink-2);line-height:1.65}
.did .t b{color:var(--ink);font-weight:620;display:block;font-size:15px}
.kidfoot{font-size:12px;color:var(--ink-muted);text-align:center;line-height:1.9;padding:22px 0 0}
.kidfoot a{color:var(--ink-2)}
.slot{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:11px;margin:0 0 8px;background:var(--surface)}
.slot.on{border-color:var(--accent);background:var(--wash)}
.slot.done{border-color:var(--ok);background:var(--ok-wash)}
.slot b{flex:1;font-size:14.5px;font-weight:620;color:var(--ink);line-height:1.45}
.slot b i{font-style:normal;font-size:11.5px;color:var(--ink-muted);display:block;font-weight:400;margin-top:1px}
.slot .v{flex:0 0 auto;font-size:14.5px;color:var(--ink-muted);border-bottom:1px dashed var(--axis);min-width:72px;text-align:center;padding:0 6px}
.slot.on .v{color:var(--accent)}
.slot.done .v{color:var(--ok);font-weight:620;border-bottom-color:transparent}
.chip[disabled]{opacity:.32}
.ex{border:1px solid var(--border);border-radius:11px;background:var(--surface-2);margin:0 0 12px;overflow:hidden}
.ex>summary{cursor:pointer;list-style:none;padding:10px 13px;font-size:13.5px;color:var(--accent)}
.ex>summary::-webkit-details-marker{display:none}
.ex .in{padding:0 13px 12px;font-size:13.5px;color:var(--ink-2)}
.mk{border-radius:6px;padding:1px 6px;font-weight:620;background:var(--wash);color:var(--accent)}
"""

JS = r"""
const D = __DATA__;
const $ = s => document.querySelector(s);
const main = $('#main'), bar = $('#bar'), barbtn = $('#barbtn'), clk = $('#clock'), stp = $('#steps');
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const S = {read:{sec:0,over:false}, ans:[], retell:{txt:'',hit:[]}, bj:{redone:0,fixed:0},
           vocab:{right:0}, prof:null, tr:{}, quit:false};

/* 默认是孩子视角：孩子看不到画像名、分数、微技能编号，只看到「今天做什么」。
   「给大人看」才展开三道闸门、判定规则、处方与疗程。同一套采集，两层呈现。 */
let MODE = 'kid';
const K = (kid, pro) => MODE === 'kid' ? kid : pro;
let CUR = ['intro', undefined];

/* ── 顶栏 / 计时 ── */
let tick = null;
function stopClock(){ if(tick){clearInterval(tick);tick=null;} clk.classList.add('hide'); clk.classList.remove('hot'); }
function runClock(dir, from, limit, onEnd){
  stopClock(); let t = from; clk.classList.remove('hide');
  const show = () => { const m = Math.floor(Math.abs(t)/60), s = Math.abs(t)%60;
    clk.textContent = m + ':' + String(s).padStart(2,'0');
    if (dir < 0 && t <= 10) clk.classList.add('hot'); };
  show();
  tick = setInterval(() => { t += dir; show();
    if (dir > 0 && limit && t >= limit) { stopClock(); onEnd && onEnd(true); }
    if (dir < 0 && t <= 0) { stopClock(); onEnd && onEnd(true); } }, 1000);
  return () => t;
}
function setTop(title, sub, backTo, withMode){
  $('#brand').innerHTML = esc(title) + (sub ? '<s>' + esc(sub) + '</s>' : '');
  const b = $('#back'); b.classList.toggle('hide', !backTo);
  b.textContent = '‹ 上一步';
  b.onclick = () => { if (typeof backTo === 'function') backTo(); else go(backTo); };
  const m = $('#mode');
  m.classList.toggle('hide', !withMode);
  m.innerHTML = K('给大人看 ›', '<b>大人视角</b> · 回到孩子视角');
  m.onclick = () => { MODE = MODE === 'kid' ? 'pro' : 'kid'; go(CUR[0], CUR[1]); };
}
const DXSTEPS = ['读一篇', '答八题', '说一遍', '再来一次', '十个词'];
const TRSTEPS2 = ['猜', '读', '问', '辨', '写'];
function steps(list, idx){
  if (!list) { stp.classList.add('hide'); return; }
  stp.classList.remove('hide');
  stp.innerHTML = list.map((t, i) => '<div class="' + (i === idx ? 'on' : (i < idx ? 'past' : '')) + '">'
    + '<span class="bar"></span><span class="lb">' + esc(t) + '</span></div>').join('');
}
function foot(){ return '<div class="foot">读得深 · 初一阅读分诊与训练 Demo · 2026-09<br>'
  + '本页数据只存在于你的浏览器里，不上传、不保存<br>'
  + '<a href="https://pumo0926-cpu.github.io/dudeshen-docs/doc-09.html">方案全文 09</a> · '
  + '<a href="https://pumo0926-cpu.github.io/dudeshen-docs/">项目资料站</a></div>'; }
function cta(txt, fn, ghost){
  bar.classList.remove('hide');
  barbtn.className = 'cta' + (ghost ? ' ghost' : ''); barbtn.textContent = txt;
  barbtn.disabled = false; barbtn.onclick = fn;
}
function noCta(){ bar.classList.add('hide'); }
function paint(html, after, keep){
  const y = window.scrollY;
  main.innerHTML = html;
  window.scrollTo(0, keep ? y : 0);
  after && after();
}
const CN = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕';
const paras = (arr, cls, num) => arr.map((p, i) => '<p class="' + (cls || '') + '" data-i="' + i + '">'
  + (num ? '<span class="pn">' + (CN[i] || (i+1)) + '</span>' : '')
  + p.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') + '</p>').join('');

/* ══ 0. 封面 ══ */
function scIntro(){
  stopClock(); steps(null); setTop(K('读得深', '三道闸门'), K('初一', '初一分诊 Demo'), null, true); noCta();
  if (MODE === 'kid') return scIntroKid();
  paint('<div class="hero"><span class="tag">DEMO · 初一（七年级上）</span>'
   + '<h1>先定位，<br>再施治。</h1>'
   + '<p class="lead">同样是「阅读不好」，卡的可能是三道完全不同的闸门。这个 Demo 让你亲手走一遍分诊，'
   + '看见自己卡在哪一道，再领一份当天就能练的处方。</p></div>'
   + '<div class="gates">'
   + '<div class="gate"><i>I</i><b>输入闸</b><span>认字·词义<br>默读速度</span></div>'
   + '<div class="gate"><i>P</i><b>加工闸</b><span>推断·结构<br>理解监控</span></div>'
   + '<div class="gate"><i>O</i><b>输出闸</b><span>审题·要点<br>证据·配速</span></div></div>'
   + '<div class="card"><div class="eyebrow">这一趟要花</div>'
   + '<h2 class="sec">约 8 分钟</h2>'
   + '<p class="sub">真实版首测 20 分钟；Demo 压缩了篇幅与题量，规则完全一致。</p>'
   + '<table class="rules"><tr><td class="nm">① 限时默读</td><td>' + D.dx.words + ' 字 · 上限 6 分钟</td><td class="vl">测配速</td></tr>'
   + '<tr><td class="nm">② 八道探针</td><td>每题追一句「有把握吗」</td><td class="vl">测三闸门 ＋ 校准</td></tr>'
   + '<tr><td class="nm">③ 60 秒复述</td><td>真实版是语音，这里打字</td><td class="vl">测结构成形</td></tr>'
   + '<tr><td class="nm">④ B 卷重做</td><td>错题重来，可回看原文</td><td class="vl">分开「不会」与「来不及」</td></tr>'
   + '<tr><td class="nm">⑤ 词义速判</td><td>10 题 · 每题 3 秒</td><td class="vl">测词汇底座</td></tr></table>'
   + '<p class="note">分诊过程<b>不给对错</b>——给了，B 卷就白做了。所有反馈在报告里一次说清。</p></div>'
   + '<button class="cta" onclick="go(\'read\')">开始分诊</button>'
   + '<button class="link" onclick="go(\'skills\')">先看 17 个微技能与 12 周疗程 ›</button>'
   + foot());
}

/* 孩子看到的封面：不出现「测评／诊断／画像」，只说今天做什么、要多久 */
function scIntroKid(){
  paint('<div class="hero"><span class="tag">七年级 · 今天这一篇</span>'
   + '<h1>先读一篇，<br>再说说你怎么想。</h1>'
   + '<p class="lead">不打分，也不排名。读完你会知道自己哪一步最费劲——然后今天就练那一步，十五分钟。</p></div>'
   + '<div class="card"><div class="eyebrow">一共五件事 · 大概 8 分钟</div>'
   + '<table class="rules">'
   + '<tr><td class="nm">读一篇</td><td>一个男生第一次值日的事，读完点一下</td></tr>'
   + '<tr><td class="nm">答八题</td><td>每题后面问你一句：心里有底吗</td></tr>'
   + '<tr><td class="nm">说一遍</td><td>合上文章，用自己的话讲这篇讲了什么</td></tr>'
   + '<tr><td class="nm">再来一次</td><td>刚才没答对的，可以翻回去看着重做</td></tr>'
   + '<tr><td class="nm">十个词</td><td>一个词 3 秒，快闪</td></tr></table>'
   + '<p class="note">做的时候<b>不告诉你对错</b>——不然「再来一次」就白给了。最后一起讲清楚。</p></div>'
   + '<button class="cta" onclick="go(\'read\')">开始读</button>'
   + '<div class="kidfoot">做完的东西只留在这台手机里，不会传走，也不会拿去跟别人比。</div>');
}

/* ══ 1. 限时默读 ══ */
function scRead(){
  steps(DXSTEPS, 0); setTop(K('先读一遍', '① 限时默读'), D.dx.title, 'intro');
  const LIMIT = 360;
  paint(K('<div class="card tight"><div class="eyebrow">第 1 件事</div>'
        + '<h2 class="sec">' + esc(D.dx.title) + '</h2>'
        + '<p class="sub">读完点下面那个按钮。不用赶，也不用回头重读。</p>'
        + '<div class="soft"><i id="sf"></i></div></div>',
        '<div class="card tight"><div class="eyebrow">环节一 / 五</div>'
        + '<h2 class="sec">' + esc(D.dx.title) + '</h2>'
        + '<p class="sub">' + D.dx.words + ' 字 · 上限 6 分钟 · 读完就点底部按钮，别回头重读</p></div>')
   + (D.dx.notes ? '<div class="notes">' + K('<b>先看一眼这几个词</b>：', '<b>词语</b>：') + esc(D.dx.notes) + '</div>' : '')
   + '<div class="txt">' + paras(D.dx.paras, '', true) + '</div>'
   + K('<button class="link" id="quit">读不下去了，先跳过 ›</button>', ''), () => {
    const get = runClock(1, 0, LIMIT, over => finish(over));
    if (MODE === 'kid') {                       // 孩子视角不显示秒数：跳字的倒计时会让人越读越慌
      clk.classList.add('hide');
      const sf = $('#sf');
      requestAnimationFrame(() => { sf.style.transition = 'width ' + LIMIT + 's linear'; sf.style.width = '100%'; });
    }
    const finish = over => { stopClock(); S.read = {sec: over ? LIMIT : get(), over: !!over}; go('q'); };
    const q = $('#quit');
    if (q) q.onclick = () => { S.quit = true; finish(true); };
    cta(K('读完了', '我读完了'), () => finish(false));
  });
}

/* ══ 2. 八道探针 ══ */
function scQ(i){
  i = i || 0; stopClock();
  if (i >= D.dx.probe.length) { go('retell'); return; }
  const p = D.dx.probe[i]; steps(DXSTEPS, 1);
  setTop(K('第 ' + (i+1) + ' 题 / 8', '② 探针 ' + (i+1) + '/8'), K('', p.tag),
         i > 0 ? (() => go('q', i - 1)) : (() => go('read')));
  const prev = S.ans[i];
  let pick = prev ? prev.pick : ((p.view === 'multi') ? [] : null);
  let sent = prev ? prev.sent : null;
  const optHtml = p.opts.map((o, k) => '<button class="opt" data-k="' + k + '">' + o + '</button>').join('');
  const evidHtml = '<div id="ev" class="hide"><p class="sub" style="margin:14px 0 8px">'
    + K('那从文章里<b>点一句</b>出来，证明你说的对：', '从下面六句里<b>点一句</b>能支持你的判断的原文：') + '</p>'
    + D.dx.evid.map((e, k) => '<button class="sent" data-e="' + k + '"><span class="pn">' + (CN[e.p] || '') + '</span>'
        + esc(e.t) + '</button>').join('')
    + '<p class="note">句子前面的圈号是它在文章里的第几段。</p></div>';
  paint((i === 0 && !prev ? '<div class="fb" style="margin:12px 0 0">这一轮<b>看不到原文</b>，凭印象答就行——'
      + '等会儿还有一次<b>翻回去重做</b>的机会。</div>' : '')
   + (prev ? '<div class="fb" style="margin:12px 0 0">这题你刚才答过，可以改：改完再点一次下面的「' + K('有底', '有把握') + ' / ' + K('说不好', '不确定') + '」就行。</div>' : '')
   + '<div class="qh">' + K('', '<small>' + p.layer + ' · ' + p.tag + '</small>') + p.q + '</div>'
   + optHtml + (p.view === 'multi' ? '<div id="mtip"></div>' : '') + (p.view === 'evid' ? evidHtml : '')
   + '<div id="conf" class="hide"><p class="sub" style="margin:18px 0 6px">'
   + K('这题，你心里有底吗？', '这题你有把握吗？<b>（必答，用来算校准度）</b>') + '</p>'
   + '<div class="conf"><button data-c="1">' + K('有底', '有把握') + '</button>'
   + '<button data-c="0">' + K('说不好', '不确定') + '</button></div></div>'
   + '<p class="note">' + K('先不说对错，最后一起讲。', '分诊阶段不显示对错。') + '</p>', () => {
    noCta();
    if (prev) {                                   // 返回改答案：把上次选的恢复出来
      const sel = (p.view === 'multi') ? pick : [pick];
      main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', sel.includes(+x.dataset.k)));
      if (p.view === 'evid') {
        $('#ev').classList.remove('hide');
        main.querySelectorAll('.sent').forEach(x => x.setAttribute('aria-pressed', +x.dataset.e === sent));
      }
      $('#conf').classList.remove('hide');
      main.querySelectorAll('.conf button').forEach(x => x.setAttribute('aria-pressed', +x.dataset.c === prev.conf));
    }
    main.querySelectorAll('.opt').forEach(b => b.onclick = () => {
      const k = +b.dataset.k;
      if (p.view === 'multi') {
        const at = pick.indexOf(k);
        let full = false;
        if (at >= 0) pick.splice(at, 1); else if (pick.length < 2) pick.push(k); else full = true;
        main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', pick.includes(+x.dataset.k)));
        const mt = $('#mtip');
        if (mt) mt.innerHTML = full ? '<div class="fb bad">最多选两点。想换的话，先把选中的点一下取消。</div>' : '';
        if (pick.length === 2) $('#conf').classList.remove('hide');
      } else {
        pick = k;
        main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', +x.dataset.k === k));
        if (p.view === 'evid') { $('#ev').classList.remove('hide'); if (sent !== null) $('#conf').classList.remove('hide'); }
        else $('#conf').classList.remove('hide');
      }
    });
    main.querySelectorAll('.sent').forEach(b => b.onclick = () => {
      sent = +b.dataset.e;
      main.querySelectorAll('.sent').forEach(x => x.setAttribute('aria-pressed', +x.dataset.e === sent));
      if (pick !== null) $('#conf').classList.remove('hide');
    });
    main.querySelectorAll('.conf button').forEach(b => b.onclick = () => {
      let right;
      if (p.view === 'multi') right = pick.length === 2 && p.ans.every(a => pick.includes(a));
      else if (p.view === 'evid') right = (pick === p.ans) && sent !== null && D.dx.evid[sent].ok;
      else right = pick === p.ans;
      S.ans[i] = {pick, sent, conf: +b.dataset.c, right, layer: p.layer, tag: p.tag};
      go('q', i + 1);
    });
  });
}

/* ══ 3. 60 秒复述 ══ */
function scRetell(){
  steps(DXSTEPS, 2); setTop(K('说一遍', '③ 60 秒复述'), K('一分钟', '不看原文'), () => go('q', D.dx.probe.length - 1));
  paint('<div class="card tight"><div class="eyebrow">' + K('第 3 件事', '环节三 / 五') + '</div>'
   + '<h2 class="sec">合上文章，说一遍</h2>'
   + '<p class="sub">' + K('别翻回去看。想到哪写到哪，写不完整也没关系。',
       '真实版是 60 秒语音，这里用打字。<b>不要回看原文</b>——这一环节测的是结构有没有在脑子里成形。') + '</p></div>'
   + '<p style="margin:0 0 8px"><b>这篇文章讲了什么？按顺序说。</b></p>'
   + '<textarea id="rt" placeholder="谁、做了什么、先后顺序、为什么这件事值得写……"></textarea>'
   + '<div class="cnt"><span id="rc">0</span> 字</div>'
   + '<div id="hits" class="chips" style="margin-top:10px"></div><div id="tmo"></div>'
   + '<p class="note">' + K('只看这四样说到没有，不看你写得好不好看。', '判定只看四样东西有没有出现，不看文采。') + '</p>', () => {
    const ta = $('#rt');
    const render = () => {
      const t = ta.value; $('#rc').textContent = t.length;
      S.retell.txt = t;
      S.retell.hit = D.dx.retell.map(g => g.kws.some(k => t.includes(k)));
      $('#hits').innerHTML = D.dx.retell.map((g, i) => '<span class="chip ' + (S.retell.hit[i] ? 'hit' : '') + '">'
        + (S.retell.hit[i] ? '✓ ' : '') + g.name + '</span>').join('');
    };
    ta.oninput = render; render(); ta.focus();
    const done = () => { stopClock(); go('bj'); };
    runClock(-1, 60, 0, () => {                 // 到点只提醒，不抢走正在打的字
      const el = $('#tmo');
      if (el) el.innerHTML = '<div class="fb">一分钟到了。<b>不用急</b>，写完点下面的「说完了」就行。</div>';
    });
    cta('说完了', done);
  });
}

/* ══ 4. B 卷重做 ══ */
function scBJ(){
  stopClock(); steps(DXSTEPS, 3); setTop(K('再来一次', '④ B 卷重做'), K('这回能翻回去看', '可回看原文'), () => go('retell'));
  const wrong = S.ans.map((a, i) => a && !a.right ? i : -1).filter(i => i >= 0);
  S.bj.redone = wrong.length; S.bj.fixed = 0;   // 允许返回重做，重入时清零免得重复计数
  if (!wrong.length) {
    paint(K('<div class="card"><div class="eyebrow">第 4 件事</div><h2 class="sec">刚才全对，这步跳过</h2>'
          + '<p>这一步本来是给没答对的题留的第二次机会。你没有，那就直接往下走。</p></div>',
          '<div class="card"><div class="eyebrow">环节四 / 五</div><h2 class="sec">A 卷全对，B 卷跳过</h2>'
          + '<p>B 卷的用处是分开「不会」与「来不及」。你没有错题，说明这道分离器在你身上用不上——'
          + '差值记 0，判定时按「不是速度问题」处理。</p></div>'), () => cta('继续', () => go('vocab')));
    return;
  }
  let idx = 0, showText = false;
  const one = () => {
    const i = wrong[idx], p = D.dx.probe[i];
    let pick = (p.view === 'multi') ? [] : null, sent = null;
    paint('<div class="card tight"><div class="eyebrow">' + K('再来一次 · 第 ', '环节四 / 五 · 第 ') + (idx+1) + '/' + wrong.length + ' 题</div>'
     + '<h2 class="sec">这题再想一次</h2><p class="sub">'
     + K('这回可以翻回去看，也不赶时间。', '不限时，可以回看原文。想清楚再选。') + '</p></div>'
     + '<button class="cta ghost" id="tg" style="margin:0 0 12px">' + (showText ? '收起原文' : K('翻回去看', '查看原文')) + '</button>'
     + '<div id="tx" class="txt ' + (showText ? '' : 'hide') + '" style="max-height:44vh;overflow:auto;border:1px solid var(--border);border-radius:14px;padding:12px">'
     + paras(D.dx.paras) + '</div>'
     + '<div class="qh"><small>' + p.layer + ' · ' + p.tag + '</small>' + p.q + '</div>'
     + p.opts.map((o, k) => '<button class="opt" data-k="' + k + '">' + o + '</button>').join('')
     + (p.view === 'evid' ? '<p class="sub" style="margin:14px 0 8px">再点一句原文作证据：</p>'
        + D.dx.evid.map((e, k) => '<button class="sent" data-e="' + k + '"><span class="pn">' + (CN[e.p] || '') + '</span>'
            + esc(e.t) + '</button>').join('') : ''), () => {
      $('#tg').onclick = () => { showText = !showText; $('#tx').classList.toggle('hide', !showText); $('#tg').textContent = showText ? '收起原文' : K('翻回去看', '查看原文'); };
      const ready = () => {
        let ok;
        if (p.view === 'multi') ok = pick.length === 2; else if (p.view === 'evid') ok = pick !== null && sent !== null; else ok = pick !== null;
        barbtn.disabled = !ok;
        barbtn.textContent = ok ? K('就选这个', '这次就这样') : K('先选一个答案', '先选一个答案');
      };
      main.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        const k = +b.dataset.k;
        if (p.view === 'multi') { const at = pick.indexOf(k); if (at >= 0) pick.splice(at,1); else if (pick.length < 2) pick.push(k);
          main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', pick.includes(+x.dataset.k))); }
        else { pick = k; main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', +x.dataset.k === k)); }
        ready();
      });
      main.querySelectorAll('.sent').forEach(b => b.onclick = () => { sent = +b.dataset.e;
        main.querySelectorAll('.sent').forEach(x => x.setAttribute('aria-pressed', +x.dataset.e === sent)); ready(); });
      cta(K('先选一个答案', '先选一个答案'), () => {
        let right;
        if (p.view === 'multi') right = pick.length === 2 && p.ans.every(a => pick.includes(a));
        else if (p.view === 'evid') right = (pick === p.ans) && sent !== null && D.dx.evid[sent].ok;
        else right = pick === p.ans;
        if (right) S.bj.fixed++;
        idx++; if (idx < wrong.length) one(); else go('vocab');
      });
      barbtn.disabled = true; barbtn.textContent = K('先选一个答案', '先选一个答案');
    });
  };
  one();
}

/* ══ 5. 词义速判 ══ */
function scVocab(){
  steps(DXSTEPS, 4); setTop(K('十个词', '⑤ 词义速判'), K('一个 3 秒', '每题 3 秒'), () => go('bj')); noCta();
  let i = 0; S.vocab.right = 0;
  const startPage = () => paint('<div class="card"><div class="eyebrow">最后一件事</div>'
   + '<h2 class="sec">十个词，一个 3 秒</h2>'
   + '<p>' + K('看加粗那个词是什么意思，凭第一反应选。<b>来不及也没关系</b>——这一轮本来就测「反应过来的快慢」，不是考你背没背过。',
       '书面语与课内文言实词的速判，测词汇底座；3 秒上限是刻意的。') + '</p>'
   + '<p class="sub">准备好了再开始，倒计时从你点「开始」那一刻算。</p></div>',
   () => cta('开始', () => one()));
  const one = () => {
    if (i >= D.dx.vocab.length) { stopClock(); go('report'); return; }
    const v = D.dx.vocab[i];
    const secs = i === 0 ? 5 : 3;              // 第一题多给 2 秒，别一进来就丢分
    paint('<div class="card tight"><div class="eyebrow">' + K('十个词 · ', '环节五 / 五 · ') + (i+1) + '/' + D.dx.vocab.length + '</div>'
     + '<h2 class="sec">' + v[0] + '</h2><p class="sub">'
     + K('加粗那个词是什么意思？别想太久。', '划线词是什么意思？3 秒内选。') + (i === 0 ? '<p class="note">第一题给 5 秒，后面每题 3 秒。</p>' : '') + '</p></div>'
     + v[1].map((o, k) => '<button class="opt" data-k="' + k + '">' + esc(o) + '</button>').join(''), () => {
      let done = false;
      const next = ok => { if (done) return; done = true; stopClock(); if (ok) S.vocab.right++; i++; setTimeout(one, 120); };
      runClock(-1, secs, 0, () => next(false));
      main.querySelectorAll('.opt').forEach(b => b.onclick = () => next(+b.dataset.k === v[2]));
    });
  };
  startPage();
}
"""

JS2 = r"""
/* ══ 6. 诊断报告 ══ */
function metrics(){
  const w = D.dx.words, sec = Math.max(S.read.sec, 1);
  const wpm = Math.round(w / (sec / 60));
  const R = (a, b) => S.ans.slice(a, b).filter(x => x && x.right).length;
  const L1 = R(0,3), L2 = R(3,6), L3 = R(6,8);
  const mis = S.ans.filter(x => x && x.conf === 1 && !x.right).length;
  const cov = S.retell.hit.filter(Boolean).length;
  const ba = S.bj.redone ? S.bj.fixed / D.dx.probe.length : 0;
  const voc = S.vocab.right, vn = D.dx.vocab.length;
  const spd = S.read.over ? 0.45 : Math.min(1, wpm / 300);
  const I = Math.round((0.55 * spd + 0.45 * (voc / vn)) * 100);
  const P = Math.round((0.55 * (L2/3) + 0.25 * (cov/4) + 0.20 * (1 - mis/8)) * 100);
  const O = Math.round((0.60 * (L3/2) + 0.25 * (L1/3) + 0.15 * (1 - Math.min(ba,.4)/.4)) * 100);
  const wtxt = S.read.over ? '超时未读完' : (wpm > 1200 ? '＞1200 字·分（几乎没读）' : wpm + ' 字·分');
  return {wpm, wtxt, sec, L1, L2, L3, mis, cov, ba, voc, vn, I, P, O, over: S.read.over,
          fixed: S.bj.fixed, redone: S.bj.redone,
          structWrong: (S.ans[4] && !S.ans[4].right) || (S.ans[5] && !S.ans[5].right)};
}
function judge(m){
  const pct = x => Math.round(x * 100) + '%';
  const rows = [
    {k:'base',   c:'词义速判 < 6/10 且 L1 事实题有错', v: m.voc + '/' + m.vn + ' · L1 ' + m.L1 + '/3',
     hit: m.voc < 6 && m.L1 < 3},
    {k:'miscal', c:'「有把握却答错」≥ 3 题（真实版 ≥40%）', v: m.mis + '/8 题',
     hit: m.mis >= 3},
    {k:'slow',   c:'没读完 ／ 默读 < 150 字·分 ／ B−A ≥ 25%', v: (m.over ? '超时未读完' : m.wpm + ' 字·分') + ' · B−A ' + pct(m.ba),
     hit: m.over || m.wpm < 150 || m.ba >= .25},
    {k:'skim',   c:'默读 ≥ 400 字·分，且 L2 推断题错 ≥ 2', v: m.wpm + ' 字·分 · L2 ' + m.L2 + '/3',
     hit: m.wpm >= 400 && m.L2 <= 1},
    {k:'scatter',c:'L1 ≥ 2/3，但结构题错 或 复述覆盖 < 50%', v: 'L1 ' + m.L1 + '/3 · 复述 ' + m.cov + '/4',
     hit: m.L1 >= 2 && (m.structWrong || m.cov < 2)},
    {k:'copy',   c:'复述覆盖 ≥ 3/4，但 L3 证据·要点题错 ≥ 1', v: '复述 ' + m.cov + '/4 · L3 ' + m.L3 + '/2',
     hit: m.cov >= 3 && m.L3 <= 1},
  ];
  const first = rows.find(r => r.hit);
  return {rows, key: first ? first.k : 'even'};
}
function scReport(){
  stopClock(); steps(null); setTop(K('今天这一篇', '诊断报告'), K('读完了', 'Demo'), null, true);
  const m = metrics(), j = judge(m);
  S.prof = D.profiles.find(p => p.k === j.key);
  if (MODE === 'kid') return scReportKid(m);

  /* 家长那一页：先给一句人话的结论，再给一张「我们看了什么·他的结果·这说明什么」的表。
     L1/L2/B−A 这类内部写法一律翻译；判定规则与闸门分数收进最后的折叠区。 */
  const meter = (n2, v, cls) => '<div class="meter ' + (cls||'') + '"><div class="lab"><span>' + n2 + '</span><b>' + v + '</b></div>'
    + '<div class="track"><i class="fill" style="width:' + v + '%"></i></div></div>';
  const cls = v => v >= 70 ? 'g' : (v >= 50 ? '' : 'w');
  const rows = [
    ['读得快不快',
     m.over ? '6 分钟没读完' : (m.wpm > 1200 ? '几乎没读就开始答' : m.wpm + ' 字/分钟'),
     m.over ? '这篇 ' + D.dx.words + ' 字，他没读完。先不谈快慢，要先解决「读不完」。'
       : (m.wpm > 1200 ? '他几乎没读就开始答题了——下面几行的结果要按这个前提看。'
       : (m.wpm < 300 ? '课标要求初中生默读每分钟不少于 500 字。他偏慢，卷面字数一多就会做不完。'
       : (m.wpm > 600 ? '比课标要求快。快本身不是问题，要看下面几行跟不跟得上。' : '速度够用，不是问题。')))],
    ['读完记住了多少', m.L1 + ' / 3 道',
     '问的是文章里发生了什么（他遇到哪三个困难、她说了哪四个字）。'
     + (m.L1 >= 2 ? '这一项没问题。' : '细节留不住，多半是读的时候没真读进去。')],
    ['能不能想深一层', m.L2 + ' / 3 道',
     '问的是「人物为什么这么做」「这一段起什么作用」——中考现代文的主要失分区。'
     + (m.L2 >= 2 ? '这一项还行。' : '这一项偏弱，是接下来要练的。')],
    ['答题能不能扣住原文', m.L3 + ' / 2 道',
     '中考主观题按要点给分，每一点都要挂得住原文。'
     + (m.L3 >= 1 ? '他知道要找依据。' : '他现在答题挂不住原文，容易答了一堆不得分。')],
    ['合上书能不能讲清楚', m.cov + ' / 4 样',
     '四样是：谁、做了什么、先后顺序、为什么这件事值得写。'
     + (m.cov >= 3 ? '结构在他脑子里是成形的。' : '说不全，说明读完没形成一条线。')],
    ['认字词有没有卡住', m.voc + ' / ' + m.vn + ' 个',
     '书面语与课内文言词（骤、舍、委、引、顾……）。'
     + (m.voc >= 6 ? '词上没卡。' : '词上卡住会拖累整篇理解，要先补这一块。')],
    ['自我感觉准不准', m.mis + ' / 8 道',
     '这几道他答完说「有把握」，实际答错了。'
     + (m.mis >= 3 ? '<b>这是最值得注意的一条</b>：他不知道自己没懂，所以也不会回头再看。' : '他对自己的判断比较准。')],
    ['给时间、允许翻回原文再做一遍',
     (m.redone ? m.fixed + ' 道改对（共 ' + m.redone + ' 道）' : '没有错题，跳过'),
     m.redone === 0 ? '第一遍就全对，这一项用不上。'
       : (m.ba >= .25 ? '差别明显：<b>不少题是「来不及／没细看」，不是真不会</b>——先练配速和审题最划算。'
       : '差别不大：<b>错的那些是真的不会</b>，给再多时间也一样，要从读懂那一步补。')],
  ];
  paint('<div class="fb" style="margin:14px 0 0">这是<b>给家长看的那一页</b>（也是大人看到的那一层）。孩子在同一次作答后看到的是另一页：没有类型名、没有分数，只有「你做到的五件事」和今天练哪一件。'
   + '<a href="javascript:void(0)" id="toKid" style="color:var(--accent)">看看孩子那页 ›</a></div>'
   + '<div class="big"><div class="n" style="font-size:30px;line-height:1.25">' + esc(S.prof.pname) + '</div>'
   + '<div class="t">这次分诊的结论 · 8 分钟 · 一篇 ' + D.dx.words + ' 字的文章</div></div>'
   + '<div class="said">' + S.prof.pwhy + '</div>'
   + '<div class="card"><div class="eyebrow">这 8 分钟测了什么</div><h2 class="sec">八件事，逐条说</h2>'
   + '<p class="sub">左边是我们看的东西，中间是他这次的结果，下面一行是这代表什么</p>'
   + rows.map(r => '<div class="did" style="flex-direction:column;align-items:stretch;gap:4px">'
       + '<div style="display:flex;gap:10px;align-items:baseline">'
       + '<b style="flex:1;color:var(--ink);font-size:15px">' + r[0] + '</b>'
       + '<span style="font-variant-numeric:tabular-nums;font-weight:680;color:var(--accent);white-space:nowrap">' + esc(r[1]) + '</span></div>'
       + '<div style="font-size:13px;color:var(--ink-2);line-height:1.7">' + r[2] + '</div></div>').join('')
   + '</div>'
   + '<div class="card"><div class="eyebrow">本月建议</div><h2 class="sec">只主攻一件事</h2>'
   + '<div class="fb ok" style="margin:0 0 12px"><b>' + esc(S.prof.act) + '</b></div>'
   + '<p class="sub" style="margin:0 0 10px">时间大致这么分（同时在练的不超过 3 项，多了 15 分钟装不下）</p>'
   + S.prof.rx.map(r => meter(r[0].replace(/\s*[A-Z]\d(·[A-Z]\d)*\s*$/, ''), r[1])).join('')
   + '<p class="note">孩子那边看到的只有一句：「' + esc(S.prof.kid) + '」——不会出现类型名，也不会出现分数。</p></div>'
   + '<div class="card"><div class="eyebrow">四周后怎么知道有没有用</div>'
   + '<table class="rules"><tr><td class="nm">看什么</td><td>同样的八件事，换一篇没读过的文章再测一次</td></tr>'
   + '<tr><td class="nm">算有进展</td><td>这次弱的那两项（' + esc(rows.filter((r,i) => [2,3,6].includes(i)).map(r => r[0]).join('、')) + '）里，至少一项明显变好</td></tr>'
   + '<tr><td class="nm">不算数</td><td>只是「做得多了」「打卡天数长了」——那是习惯，不是理解力</td></tr></table></div>'
   + '<div class="card"><div class="eyebrow">我们不做的三件事</div>'
   + '<table class="rules"><tr><td class="nm">不预测分数</td><td>没有任何产品能从一次阅读测出中考能考多少分</td></tr>'
   + '<tr><td class="nm">不排名</td><td>不和别的孩子比，只和他自己四周前比</td></tr>'
   + '<tr><td class="nm">不给孩子贴类型</td><td>我们内部有一个类型名，只用来挑练习；孩子看不到，你也不必记（想看可展开下面的判定细节）</td></tr></table></div>'
   + '<div class="card"><div class="eyebrow">讲评与订正</div><h2 class="sec">八道题的逐题讲评</h2>'
   + '<p>孩子答题时不给对错（否则「再来一次」那一步就失效了），讲评和订正放在这里：'
   + '每道题的正解、为什么、原文在第几段，错的可以当场再做一遍。</p>'
   + '<button class="cta ghost" id="toReview2" style="margin-top:4px">看逐题讲评 ›</button></div>'
   + '<details class="ex"><summary>判定细节：我们内部是怎么算的 ›</summary><div class="in">'
   + '<p style="margin:10px 0 6px;color:var(--ink)"><b>三道闸门</b>（串联，任何一道堵住卷面都是低分）</p>'
   + meter('I　输入闸　认字·词义·默读速度', m.I, cls(m.I))
   + meter('P　加工闸　推断·结构·理解监控', m.P, cls(m.P))
   + meter('O　输出闸　审题·要点·证据·配速', m.O, cls(m.O))
   + '<p style="margin:14px 0 6px;color:var(--ink)"><b>六条规则，逐条对</b>（命中的第一条即为判定）</p>'
   + '<table class="rules">'
   + j.rows.map(r => {
       const pf = D.profiles.find(x => x.k === r.k), win = r.k === j.key;
       return '<tr class="' + (win ? 'hit' : '') + '"><td class="nm">' + esc(pf.name)
         + (win ? '<span class="pill on">判定</span>' : (r.hit ? '<span class="pill">也触发</span>' : ''))
         + '<br><span style="font-weight:400;font-size:11.5px;color:var(--ink-muted)">' + esc(r.c) + '</span></td>'
         + '<td class="vl">' + esc(r.v) + '</td></tr>'; }).join('')
   + '</table>'
   + '<p class="note">L1＝事实检索题，L2＝推断与结构题，L3＝证据与要点题；B−A＝同一批错题「允许翻回原文重做」后改对的比例。'
   + '<b>多条同时触发是常态</b>——闸门串联，一处堵住会把下游一起拖低，所以判定取最靠前的那一条，先治底层。'
   + '单次分诊只是起点：真实版允许类型两周后才稳定，并每 4 周重判一次。</p>'
   + '</div></details>'
   + foot(), () => { cta('领今天的 15 分钟训练块', () => go('train'));
     $('#toKid').onclick = () => { MODE = 'kid'; go('report'); };
     $('#toReview2').onclick = () => go('review'); });
}

/* 孩子看到的报告：只说「你做到了什么」和「今天练哪一件」。
   画像名、三道闸门分数、判定规则、处方配比，全部留在大人那一层。 */
function scReportKid(m){
  const line = m.over ? '这篇有点长，你没读完。先不说快慢——下次试试前半段一口气读到底，不回头。'
    : (m.wpm > 1200 ? '你几乎没怎么读就开始答了。'
    : (m.wpm < 150 ? '你读得很细，就是慢了点。'
    : (m.wpm >= 400 ? '你读得挺快。' : '你的速度正合适。')));
  const did = [
    ['读完了整篇', !m.over],
    ['文章里发生的事，记住了', m.L1 >= 2],
    ['看出了人物为什么这么做', m.L2 >= 2],
    ['能按先后顺序讲一遍', m.cov >= 3],
    ['答案挂住了原文里的句子', m.L3 >= 1],
  ];
  const good = did.filter(d => d[1]).length;
  const self = ['读得慢，读不完', '字都认识，意思没读懂', '想到了，但写不出来', '记不住前面写了什么', '都还行'];
  paint('<div class="big"><div class="n">做到 ' + good + ' 件</div>'
   + '<div class="t">今天这一篇' + (good < did.length ? ' · 另外 ' + (did.length - good) + ' 件，接下来慢慢练' : ' · 五件都做到了') + '</div></div>'
   + '<div class="said">' + esc(line) + esc(m.mis >= 3 ? '有几道题你觉得有底，其实答错了——那几处值得回头看看。' : '') + '</div>'
   + '<div class="card"><div class="eyebrow">具体做到了哪几件</div>'
   + did.map(d => '<div class="did"><span class="m ' + (d[1] ? '' : 'no') + '">' + (d[1] ? '✓' : '–') + '</span>'
     + '<span class="t">' + d[0] + '</span></div>').join('')
   + '<p class="note">这里不打分，也不跟别人比。没做到的那几件，就是接下来要练的。</p></div>'
   + '<div class="card"><div class="eyebrow">今天最值得练的一件事</div>'
   + '<h2 class="sec">' + esc(S.prof.kid) + '</h2>'
   + '<p style="margin-top:8px">' + esc(S.prof.kidwhy) + '</p></div>'
   + '<div class="card"><div class="eyebrow">你自己觉得呢</div>'
   + '<h3 class="sub3" style="margin-top:0">刚才最费劲的是哪一步？</h3>'
   + '<p class="sub">这一条只有你知道，选了我们就按你说的调。</p>'
   + self.map((t, i) => '<button class="opt" data-self="' + i + '">' + t + '</button>').join('')
   + '<div id="sfb"></div></div>'
   + '<div class="card"><div class="eyebrow">说好了要讲的</div><h2 class="sec">刚才那八道，一起看一遍</h2>'
   + '<p>答题的时候没告诉你对错，是怕影响「再来一次」那一步。现在可以看了：<b>每道题的正解、为什么、原文在第几段</b>，错的还能当场订正。</p>'
   + '<button class="cta ghost" id="toReview" style="margin-top:4px">看这八道的讲评 ›</button></div>'
   + '<div class="kidfoot">今天这篇到这儿就结束了，不用再往下刷。<br>'
   + '<a href="javascript:void(0)" id="redo">想重做一遍？从头再来 ›</a><br>'
   + '<a href="javascript:void(0)" id="toPro">这份结果大人看到的是什么样 ›</a></div>', () => {
    main.querySelectorAll('[data-self]').forEach(b => b.onclick = () => {
      S.self = +b.dataset.self;
      main.querySelectorAll('[data-self]').forEach(x => x.setAttribute('aria-pressed', +x.dataset.self === S.self));
      const agree = (S.self === 0 && ['slow'].includes(S.prof.k)) || (S.self === 1 && ['skim','base'].includes(S.prof.k))
        || (S.self === 2 && S.prof.k === 'copy') || (S.self === 3 && S.prof.k === 'scatter') || (S.self === 4 && S.prof.k === 'even');
      $('#sfb').innerHTML = '<div class="fb ' + (agree ? 'ok' : '') + '">'
        + (agree ? '✓ 跟我们看到的一样，那就照这个练。' : '跟我们看到的不完全一样——没关系，先按你说的练一周，下周再看一次。') + '</div>';
      cta('开始今天的 15 分钟', () => go('train'));
    });
    cta('开始今天的 15 分钟', () => go('train'));
    $('#toPro').onclick = () => { MODE = 'pro'; go('report'); };
    $('#redo').onclick = () => location.reload();
    $('#toReview').onclick = () => go('review');
  });
}

/* 分诊时答应过「先不说对错，最后一起讲」——这里兑现：
   八道题逐题给你选的／正解／为什么／原文在第几段，再把错的那几道当场订正一遍。 */
function ansText(p, a){
  if (!a) return '没作答';
  if (p.view === 'multi') return (a.pick || []).map(k => p.opts[k]).join('　＋　') || '没作答';
  if (p.view === 'evid') return (a.pick === null || a.pick === undefined ? '没选观点' : p.opts[a.pick])
    + (a.sent === null || a.sent === undefined ? '' : '　＋　「' + D.dx.evid[a.sent].t + '」');
  return a.pick === null || a.pick === undefined ? '没作答' : p.opts[a.pick];
}
function rightText(p){
  if (p.view === 'multi') return p.ans.map(k => p.opts[k]).join('　＋　');
  if (p.view === 'evid') return p.opts[p.ans] + '　＋　文中任意一句写动作的句子（如「' + D.dx.evid[1].t + '」）';
  return p.opts[p.ans];
}
function srcFoldDX(idxs){
  if (!idxs || !idxs.length) return '';
  return '<details class="ex"><summary>看原文 ›</summary><div class="in">'
   + idxs.map(i => '<p style="margin:0 0 8px;color:var(--ink);line-height:1.9"><span class="pn">' + (CN[i] || (i+1)) + '</span>'
       + esc(D.dx.paras[i]) + '</p>').join('') + '</div></details>';
}
function scReview(){
  stopClock(); steps(null); setTop('一起看这八道', '讲完可以订正', () => go('report'), true);
  const right = S.ans.filter(a => a && a.right).length;
  const wrong = S.ans.map((a, i) => a && !a.right ? i : -1).filter(i => i >= 0);
  const mis = S.ans.map((a, i) => a && a.conf === 1 && !a.right ? i : -1).filter(i => i >= 0);
  paint('<div class="card"><div class="eyebrow">答应过要讲的</div>'
   + '<h2 class="sec">八道题，对了 ' + right + ' 道</h2>'
   + '<p class="sub" style="margin:0">' + (wrong.length === 0 ? '全对。下面还是逐题看一眼为什么这么选。'
       : '错的 ' + wrong.length + ' 道' + (mis.length ? '，其中 <b>' + mis.length + ' 道你说过「有底」</b>——这几道最值得看。' : '。')) + '</p></div>'
   + D.dx.probe.map((p, i) => {
       const a = S.ans[i], okk = a && a.right, flag = a && a.conf === 1 && !a.right;
       return '<div class="card"><div class="eyebrow">第 ' + (i+1) + ' 题'
         + '<span class="pill ' + (okk ? 'ok' : '') + '">' + (okk ? '✓ 对了' : '✗ 错了') + '</span>'
         + (flag ? '<span class="pill on">你说过有底</span>' : '') + '</div>'
         + '<div class="qh" style="margin-top:0">' + p.q + '</div>'
         + (okk ? '' : '<div class="fb bad" style="margin:0 0 8px"><b>你选的：</b>' + esc(ansText(p, a)) + '</div>')
         + '<div class="fb ok" style="margin:0 0 10px"><b>正解：</b>' + esc(rightText(p)) + '</div>'
         + '<p style="font-size:14px;line-height:1.8">' + p.why + '</p>'
         + srcFoldDX(p.src) + '</div>'; }).join('')
   + (wrong.length ? '<div class="card"><div class="eyebrow">订正</div><h2 class="sec">错的 ' + wrong.length + ' 道，现在再做一遍</h2>'
       + '<p class="sub" style="margin:0">讲过了才算数——自己再做对一次，这道题才真的过去了。</p></div>' : '')
   + foot(), () => {
    if (wrong.length) cta('开始订正这 ' + wrong.length + ' 道', () => go('fix'));
    else cta('回报告', () => go('report'), true);
  });
}
/* 订正：只做错题，这一次当场给对错；改对了才算订完 */
function scFix(){
  stopClock(); steps(null); setTop('订正', '这次会告诉你对错', () => go('review'), true);
  const wrong = S.ans.map((a, i) => a && !a.right ? i : -1).filter(i => i >= 0);
  S.fix = S.fix || {ok: 0, at: 0};
  const one = () => {
    if (S.fix.at >= wrong.length) {
      paint('<div class="big"><div class="n">订正完了</div><div class="t">' + S.fix.ok + '/' + wrong.length + ' 道这次做对了</div></div>'
       + '<div class="said">' + (S.fix.ok === wrong.length ? '全部改对。错过一次又自己改对的题，比一开始就做对的题记得牢。'
           : '还有 ' + (wrong.length - S.fix.ok) + ' 道没改对——回去把解析再看一遍，特别看「原文在第几段」那一段。') + '</div>'
       + '<div class="kidfoot">今天的分诊到这儿就结束了。</div>',
       () => { cta('去今天的训练', () => go('train')); });
      return;
    }
    const i = wrong[S.fix.at], p = D.dx.probe[i];
    let pick = (p.view === 'multi') ? [] : null, sent = null, judged = false;
    paint('<div class="card tight"><div class="eyebrow">订正 · 第 ' + (S.fix.at+1) + '/' + wrong.length + ' 道</div>'
     + '<h2 class="sec">再做一遍</h2><p class="sub" style="margin:0">想清楚再选，这次会立刻告诉你对错。</p></div>'
     + srcFoldDX(p.src)
     + '<div class="qh">' + p.q + '</div>'
     + p.opts.map((o, k) => '<button class="opt" data-k="' + k + '">' + o + '</button>').join('')
     + (p.view === 'evid' ? '<p class="sub" style="margin:14px 0 8px">再点一句原文作证据：</p>'
         + D.dx.evid.map((e, k) => '<button class="sent" data-e="' + k + '"><span class="pn">' + (CN[e.p] || '') + '</span>'
             + esc(e.t) + '</button>').join('') : '')
     + '<div id="fx"></div>', () => {
      noCta();
      const judge2 = () => {
        let ok;
        if (p.view === 'multi') { if (pick.length !== 2) return; ok = p.ans.every(x => pick.includes(x)); }
        else if (p.view === 'evid') { if (pick === null || sent === null) return; ok = pick === p.ans && D.dx.evid[sent].ok; }
        else { if (pick === null) return; ok = pick === p.ans; }
        if (judged) return; judged = true;
        if (ok) S.fix.ok++;
        $('#fx').innerHTML = '<div class="fb ' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓ 这次对了。' : '✗ 还是不对。')
          + '<br><b>正解：</b>' + esc(rightText(p)) + '<br>' + p.why + '</div>';
        cta(S.fix.at + 1 >= wrong.length ? '看订正结果' : '下一道', () => { S.fix.at++; one(); });
      };
      main.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        if (judged) return;
        const k = +b.dataset.k;
        if (p.view === 'multi') { const at = pick.indexOf(k); if (at >= 0) pick.splice(at,1); else if (pick.length < 2) pick.push(k);
          main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', pick.includes(+x.dataset.k))); }
        else { pick = k; main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', +x.dataset.k === k)); }
        judge2();
      });
      main.querySelectorAll('.sent').forEach(b => b.onclick = () => {
        if (judged) return;
        sent = +b.dataset.e;
        main.querySelectorAll('.sent').forEach(x => x.setAttribute('aria-pressed', +x.dataset.e === sent));
        judge2();
      });
    });
  };
  one();
}

/* ══ 7. 训练块（15 分钟五步，按画像挂靶点）══ */
const TSTEPS = ['猜','读','问','辨','写'];
function scTrain(k){
  k = k || 0; stopClock();
  if (k >= 5) { go('tdone'); return; }
  steps(TRSTEPS2, k);
  setTop(TSTEPS[k] + '　第 ' + (k+1) + ' 步 / 5', D.tr.title,
         k > 0 ? (() => go('train', k - 1)) : (() => go('report')));
  [tGuess, tRead, tAsk, tSort, tWrite][k]();
}
function stepHead(min, title, codes, desc){
  return '<div class="card tight"><div class="eyebrow">' + min + '</div>'
   + '<h2 class="sec">' + (title || K('先热个身', '常规')) + '</h2>'
   + (codes && MODE === 'pro' ? '<p class="sub" style="margin:3px 0 6px;color:var(--accent)">靶点：' + codes + '</p>' : '')
   + '<p class="sub" style="margin:0">' + desc + '</p></div>';
}
function tGuess(){
  let pick = (S.tr.guess === undefined) ? null : S.tr.guess;
  const g = D.tr.guess;
  const peerHTML = () => '<p class="sub" style="margin:0 0 8px">' + K('别人都押了什么', '同龄人怎么押的') + '（模拟数据）</p>'
    + g.options.map((o, i) => '<div class="r ' + (i === pick ? 'me' : '') + '">'
      + '<span style="flex:0 0 96px;font-size:12px;color:var(--ink-muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + esc(o) + '</span>'
      + '<span class="bar"><i style="width:' + g.peer[i] + '%"></i></span><span class="v">' + g.peer[i] + '%</span></div>').join('');
  paint(stepHead('第 1 步 · 约 1 分钟', '', '', K('先押一个答案。读的时候你就有事可做了——这题不算对错。',
        '先押一个答案，读的时候就有事可做——这一步不判对错。'))
   + '<div class="qh">' + esc(g.q) + '</div>'
   + g.options.map((o, i) => '<button class="opt" data-k="' + i + '"' + (i === pick ? ' aria-pressed="true"' : '') + '>' + esc(o) + '</button>').join('')
   + '<div id="peer" class="peer ' + (pick === null ? 'hide' : '') + '" style="margin-top:14px">' + (pick === null ? '' : peerHTML()) + '</div>'
   + (pick === null ? '<div class="fb">选一个就能往下走，这题不算对错。</div>' : ''), () => {
    noCta();
    if (pick !== null) cta('开始读', () => go('train', 1));
    main.querySelectorAll('.opt').forEach(b => b.onclick = () => {
      pick = +b.dataset.k; S.tr.guess = pick;
      main.querySelectorAll('.opt').forEach(x => x.setAttribute('aria-pressed', +x.dataset.k === pick));
      $('#peer').classList.remove('hide'); $('#peer').innerHTML = peerHTML();
      cta('开始读', () => go('train', 1));
    });
  });
}
function tRead(){
  const marked = S.tr.mark !== undefined;
  paint(stepHead('第 2 步 · 约 5 分钟', '标一处你没看懂的地方', 'P7 理解监控',
        K('随便哪一段都行，<b>必须标一处</b>。「全都懂」反而最危险——不懂的地方你自己不知道。',
          '读的时候<b>必须标出一处「我这里没懂」</b>——全篇都懂，本身就是一个失校准信号。'))
   + '<div class="txt">' + paras(D.tr.paras, 'pick', true) + '</div>'
   + '<div id="why" class="' + (marked ? '' : 'hide') + '"><p class="sub" style="margin:12px 0 6px">'
   + K('是哪种不懂？', '这一处是哪种不懂？') + '</p>'
   + ['词不懂','关系不懂（句与句之间）','背景不懂'].map((t, i) => '<button class="opt" data-w="' + i + '"'
       + (S.tr.markWhy === i ? ' aria-pressed="true"' : '') + '>' + t + '</button>').join('')
   + (S.tr.markWhy !== undefined ? '<div id="kfb" class="fb ok">标出来就行。这一处先记着，等会儿答题时再回来看一眼。</div>' : '')
   + '</div>'
   + (S.tr.allClear ? '<div class="fb ok">你说这篇没有不懂的地方——那等会儿答题时留意一下，看是不是真的都懂了。</div>'
       : '<button class="link" id="allclear">这篇我真的没有不懂的地方 ›</button>')
   + '<div id="rneed"></div>', () => {
    const need = () => { const el = $('#rneed'); if (!el) return;
      el.innerHTML = (S.tr.markWhy !== undefined) ? ''
        : '<div class="fb">还差：' + (S.tr.mark === undefined ? '<b>点一下任意一段</b>，标出你没看懂的地方' : '再选一下<b>是哪种不懂</b>') + '</div>'; };
    noCta();
    if (marked) { const el = main.querySelectorAll('.txt p')[S.tr.mark]; if (el) el.classList.add('mark'); }
    if (S.tr.markWhy !== undefined) cta('去答题', () => go('train', 2));
    need();
    main.querySelectorAll('.txt p').forEach(p2 => p2.onclick = () => {
      main.querySelectorAll('.txt p').forEach(x => x.classList.remove('mark'));
      p2.classList.add('mark'); S.tr.mark = +p2.dataset.i;
      $('#why').classList.remove('hide'); need();
      $('#why').scrollIntoView({behavior:'smooth', block:'center'});
    });
    const ac = $('#allclear');
    if (ac) ac.onclick = () => { S.tr.allClear = true; S.tr.markWhy = 3; go('train', 1); };
    main.querySelectorAll('[data-w]').forEach(b => b.onclick = () => {
      S.tr.markWhy = +b.dataset.w; S.tr.allClear = false;
      main.querySelectorAll('[data-w]').forEach(x => x.setAttribute('aria-pressed', +x.dataset.w === S.tr.markWhy));
      if (!$('#kfb')) $('#why').insertAdjacentHTML('beforeend',
        '<div id="kfb" class="fb ok">标出来就行。这一处先记着，等会儿答题时再回来看一眼。</div>');
      need(); cta('去答题', () => go('train', 2));
    });
  });
}

/* 四关做成一张张带状态的卡：哪关完了、现在哪关、还有几关，一眼看得见；
   过关后自动滚到下一关，并给一个「去第 ② 关」的按钮——不靠用户自己发现页面下面多了东西。 */
const GN = '①②③④';
function gateHead(k, title, code, state){
  return '<div class="eyebrow">第 ' + GN[k] + ' 关' + (MODE === 'pro' && code ? ' · ' + code : '')
   + '<span class="pill ' + (state === 2 ? 'ok' : (state === 1 ? 'on' : '')) + '">'
   + (state === 2 ? '✓ 完成' : (state === 1 ? '现在这关' : '还没开')) + '</span></div>'
   + '<h3 class="sub3" style="margin-top:0">' + title + '</h3>';
}
/* 答题时能随手翻到要用的那两段——原来只能退回上一步去找 */
function srcFold(idxs, label){
  return '<details class="ex"><summary>' + label + ' ›</summary><div class="in">'
   + idxs.map(i => '<p style="margin:0 0 10px;color:var(--ink);line-height:1.9"><span class="pn">' + (CN[i] || (i+1)) + '</span>'
       + D.tr.paras[i].replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') + '</p>').join('')
   + '</div></details>';
}
const goGate = k => '<button class="cta ghost" style="margin-top:10px" '
  + 'onclick="document.getElementById(\'g' + k + '\').scrollIntoView({behavior:\'smooth\',block:\'start\'})">'
  + '去第 ' + GN[k] + ' 关 ›</button>';

function tAsk(){
  const st = S.tr.ask = S.tr.ask || {phase:0, cnt:null, pts:[], ev:null, slotIdx:0, filled:[null,null,null], used:[]};
  const stem = D.tr.stem, SL = D.tr.slots;
  const fb2 = c => '<div class="fb ' + (c === 2 ? 'ok' : 'bad') + '">' + (c === 2
      ? '✓ 4 分 → 2 点。' + K('老师是按「点」给分的，不是按你写得多长给。', '踩点给分：要点数由分值决定，不由你写了多长决定。')
      : K('4 分一般拆成 <b>2 点</b>写。只写 1 点，等于先丢一半分。', '4 分题按 2 分一点拆，应是 <b>2 点</b>。只写 1 点，先丢一半。'))
    + '</div>';
  const fb3 = ok => '<div class="fb ' + (ok ? 'ok' : 'bad') + '">' + (ok
      ? '✓ 两点正好是同一个机制的两面——这就是第三个原因被放在最后的理由。'
      : '再想想：作者把第三个原因放最后，是因为它<b>同时</b>解释了「为什么牢」和「为什么不准」。') + '</div>';
  const fb4 = e => '<div class="fb ' + (e.ok ? 'ok' : 'bad') + '">' + (e.ok ? '✓ ' : '✗ ') + esc(e.why) + '</div>';
  const state = k => {
    const done = [st.slotIdx >= SL.length, st.cnt !== null, st.pts.length === 2, st.ev !== null];
    if (done[k]) return 2;
    return (k === 0 || done[k-1]) ? 1 : 0;
  };
  const render = (keep) => {
    let h = stepHead('第 3 步 · 约 4 分钟', '把题看懂，再动笔', 'O1 题干拆解 · O2 分值→要点数 · O4 证据句',
        K('这一步有四小关，做完一关下面自动出现下一关。', '中考主观题的三个对接口，全部可判定。四关顺序推进。'));
    h += '<div class="card" id="g0">' + gateHead(0, '一道题在问什么，其实就三件事', 'O1', state(0))
      + '<p class="sub">下面这句是题目。把它拆开，看它到底要你做什么。</p>'
      + '<div class="notes" style="margin:0 0 10px">' + esc(D.tr.stemText) + '</div>'
      + '<details class="ex"><summary>没做过？先看一个例子 ›</summary><div class="in">'
      + '<p style="margin:0 0 8px;color:var(--ink)">' + esc(D.tr.example.stem) + '</p>'
      + D.tr.example.marks.map(m => '<div style="margin:0 0 4px"><span class="mk">' + esc(m[0]) + '</span>'
          + ' <span style="color:var(--ink-muted)">←&nbsp;' + esc(m[1]) + '</span></div>').join('')
      + '<p style="margin:8px 0 0;font-size:12.5px;color:var(--ink-muted)">每道大题都能这么拆。下面轮到你。</p>'
      + '</div></details>'
      + SL.map((sl, i) => '<div class="slot ' + (st.filled[i] ? 'done' : (i === st.slotIdx ? 'on' : '')) + '">'
          + '<b>' + (i+1) + '. ' + esc(sl.q) + '？<i>' + esc(sl.hint) + '</i></b>'
          + '<span class="v">' + (st.filled[i] ? esc(st.filled[i]) : (i === st.slotIdx ? '点下面的词' : '　')) + '</span></div>').join('')
      + '<div class="chips" id="stem" style="margin-top:10px">'
      + stem.map((t, i) => '<button class="chip" data-s="' + i + '"'
          + (st.used.includes(i) ? ' disabled aria-pressed="true"' : '') + '>' + esc(t.t) + '</button>').join('')
      + '</div><div id="fb1"></div></div>';
    if (st.phase >= 1) h += '<div class="card" id="g1">' + gateHead(1, '4 分，写几点？', 'O2', state(1))
      + [1,2,3,4].map(n => '<button class="opt' + (st.cnt === n ? (n === 2 ? ' right' : ' wrong') : '') + '"'
          + ' data-n="' + n + '" style="display:inline-block;width:auto;margin-right:8px">' + n + ' 点</button>').join('')
      + '<div id="fb2">' + (st.cnt !== null ? fb2(st.cnt) : '') + '</div></div>';
    if (st.phase >= 2) h += '<div class="card" id="g2">' + gateHead(2, esc(D.tr.pts.q), '', state(2))
      + '<p class="sub">题目让你「结合第⑤⑥段」——就在下面，点开看一眼再选。</p>'
      + srcFold(D.tr.src, '看第⑤⑥段')
      + D.tr.pts.opts.map((o, i) => '<button class="opt" data-p="' + i + '"'
          + (st.pts.includes(i) ? ' aria-pressed="true"' : '') + '>' + esc(o) + '</button>').join('')
      + '<div id="fb3">' + (st.pts.length === 2 ? fb3(D.tr.pts.ans.every(a => st.pts.includes(a))) : '') + '</div></div>';
    if (st.phase >= 3) h += '<div class="card" id="g3">' + gateHead(3, K('给你选的两点，各找一句原文撑着', '给你的要点挂一句原文'), 'O4', state(3))
      + '<p class="sub">' + K('找不到句子撑的那一点，多半不是答案。', '挂不住的那一点，八成不是答案。') + '</p>'
      + srcFold(D.tr.src, '再看一眼第⑤⑥段')
      + D.tr.evid.map((e, i) => '<button class="sent" data-v="' + i + '"'
          + (st.ev === i ? ' aria-pressed="true"' : '') + '><span class="pn">' + (CN[e.p] || '') + '</span>'
          + esc(e.t) + '</button>').join('')
      + '<div id="fb4">' + (st.ev !== null ? fb4(D.tr.evid[st.ev]) : '') + '</div></div>';
    paint(h, wire, keep);
  };
  const toNext = k => setTimeout(() => {
    const el = document.getElementById('g' + k);
    if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
  }, 260);
  const wire = () => {
    noCta();
    main.querySelectorAll('#stem .chip').forEach(b => b.onclick = () => {
      const i = +b.dataset.s; if (st.used.includes(i) || st.slotIdx >= SL.length) return;
      const kind = stem[i].k, want = SL[st.slotIdx];
      if (kind === want.k) {
        st.filled[st.slotIdx] = stem[i].t; st.used.push(i); st.slotIdx++;
        const all = st.slotIdx >= SL.length;
        if (all) { S.tr.o1 = true; st.phase = Math.max(st.phase, 1); }
        render(true);
        $('#fb1').innerHTML = all
          ? '<div class="fb ok">✓ 三件都找齐了：<b>说说</b>（干什么）· <b>第⑤⑥段</b>（去哪找）· <b>答两点</b>（写几点）。'
            + K('以后每道大题，动笔前先这么问自己三遍。', '连续 3 次拆全才算过关。')
            + '<br><b>这一关过了，下面是第 ② 关。</b></div>' + goGate(1)
          : '<div class="fb ok">✓ 对。接着找第 ' + (st.slotIdx+1) + ' 件：<b>' + esc(SL[st.slotIdx].q) + '</b></div>';
        if (all) toNext(1);
      } else {
        const other = SL.findIndex(x => x.k === kind);
        $('#fb1').innerHTML = '<div class="fb bad">' + (other >= 0
          ? '「' + esc(stem[i].t) + '」是<b>' + esc(SL[other].q) + '</b>那一件，等会儿才轮到它。现在先找<b>' + esc(want.q) + '</b>。'
          : esc(stem[i].why)) + '</div>';
      }
    });
    main.querySelectorAll('[data-n]').forEach(b => b.onclick = () => {
      st.cnt = +b.dataset.n; S.tr.o2 = st.cnt === 2; st.phase = Math.max(st.phase, 2);
      render(true);
      $('#fb2').innerHTML = fb2(st.cnt) + '<div style="font-size:12.5px;color:var(--ink-muted);margin-top:6px">这一关过了，下面是第 ③ 关。</div>' + goGate(2);
      toNext(2);
    });
    main.querySelectorAll('[data-p]').forEach(b => b.onclick = () => {
      const i = +b.dataset.p, at = st.pts.indexOf(i);
      if (at >= 0) st.pts.splice(at, 1); else if (st.pts.length < 2) st.pts.push(i);
      main.querySelectorAll('[data-p]').forEach(x => x.setAttribute('aria-pressed', st.pts.includes(+x.dataset.p)));
      if (st.pts.length === 2) {
        const ok = D.tr.pts.ans.every(a => st.pts.includes(a)); S.tr.pts = ok;
        st.phase = Math.max(st.phase, 3);
        render(true);
        $('#fb3').innerHTML = fb3(ok) + '<div style="font-size:12.5px;color:var(--ink-muted);margin-top:6px">这一关过了，下面是最后一关。</div>' + goGate(3);
        toNext(3);
      }
    });
    main.querySelectorAll('[data-v]').forEach(b => b.onclick = () => {
      st.ev = +b.dataset.v; const e = D.tr.evid[st.ev]; S.tr.o4 = e.ok;
      main.querySelectorAll('[data-v]').forEach(x => x.setAttribute('aria-pressed', +x.dataset.v === st.ev));
      $('#fb4').innerHTML = fb4(e);
      cta('四关做完了，下一步：把文章切开', () => go('train', 3));
    });
    if (st.ev !== null) cta('四关做完了，下一步：把文章切开', () => go('train', 3));
  };
  render(false);
}
function tSort(){
  const so = S.tr.sort = S.tr.sort || {cuts:[], titles:['','',''], main:''};
  const fb5 = ok => '<div class="fb ' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓ ' : '△ ')
    + '标准切法是 <b>第①②段｜第③④⑤段｜第⑥段起</b>：提出问题 ｜ 三个原因 ｜ 牢与准的两面。'
    + (ok ? '你的切法在容差内。' : '你的两刀差得有点远——再看一眼哪里出现了「但是」「所以」这类转折词。') + '</div>';
  const render = (keep) => {
    let h = stepHead('第 4 步 · 约 2 分钟', '切成三块，再压成一句话', 'P4 结构切块 · P5 主旨压缩',
        K('概括题写不准，多半是没先把文章切开。', '概括题抓不准，十有八九是结构没切开。先切块，再压一句话。'));
    h += '<div class="card" id="c0"><div class="eyebrow">这一步有两件事 · 第 1 件'
      + '<span class="pill ' + (S.tr.p4 !== undefined ? 'ok' : 'on') + '">' + (S.tr.p4 !== undefined ? '✓ 完成' : '现在这件') + '</span></div>'
      + '<h3 class="sub3" style="margin-top:0">把文章切成三块</h3>'
      + '<p class="sub">在段落之间切<b>两刀</b>。已经切了 <b>' + so.cuts.length + '/2</b> 刀。</p><div class="txt" style="font-size:15px">';
    D.tr.paras.forEach((p, i) => {
      if (i > 0) h += '<div class="cut ' + (so.cuts.includes(i) ? 'on' : '') + '"><button data-c="' + i + '">'
        + (so.cuts.includes(i) ? '✂︎ 已切（再点一下取消）' : '＋ 在这里切一刀') + '</button></div>';
      h += '<p style="font-size:15px;line-height:1.9"><span class="pn">' + (CN[i] || (i+1)) + '</span>'
        + p.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') + '</p>';
    });
    h += '</div><div id="fb5">' + (S.tr.p4 !== undefined ? fb5(S.tr.p4) : '') + '</div></div>';
    if (S.tr.p4 !== undefined) h += '<div class="card" id="c1"><div class="eyebrow">第 2 件'
      + '<span class="pill ' + (S.tr.p5 ? 'ok' : 'on') + '">' + (S.tr.p5 ? '✓ 完成' : '现在这件') + '</span></div>'
      + '<h3 class="sub3" style="margin-top:0">' + K('给每块起个名字，再压成一句话', '小标题 ＋ 主旨压缩') + '</h3>'
      + '<p class="sub">' + K('每块起个名字，六个字以内', '给每块起一个 ≤6 字、<b>带动作</b>的小标题') + '</p>'
      + [0,1,2].map(i => '<input type="text" maxlength="6" data-t="' + i + '" value="' + esc(so.titles[i]) + '" placeholder="第 ' + (i+1) + ' 块，如「三个原因」" style="margin-bottom:8px">').join('')
      + '<h3 class="sub3">' + K('一句话说清这篇讲了什么', 'P5 一句话说清全文') + '</h3><p class="sub">'
      + K('30 字以内。别写「表达了作者的思想感情」——那句话放哪篇都通，等于没说。',
          '≤30 字，要有主体和主事件，不要「表达了作者的思想感情」这类套话') + '</p>'
      + '<textarea id="main1" style="min-height:70px" placeholder="童年的事记得牢，是因为……">' + esc(so.main) + '</textarea>'
      + '<div class="cnt"><span id="mc">' + so.main.length + '</span> 字 · 8 字起，30 字以内最好</div>'
      + '<details class="ex"><summary>不知道怎么写？看看写法 ›</summary><div class="in">'
      + '<p style="margin:0 0 6px"><b>骨架：</b>谁／什么　＋　怎么样　＋　结果或原因</p>'
      + '<p style="margin:0 0 6px">换一篇举例——《我的第一次值日》：<br>'
      + '<span class="mk">一次值日让我发现，教室的干净是有人做出来的。</span></p>'
      + '<p style="margin:6px 0 0;font-size:12.5px;color:var(--ink-muted)">别写「表达了作者的思想感情」：这句话放哪篇都通，等于没说。</p>'
      + '</div></details>'
      + '<div id="need"></div><div id="fb6"></div></div>';
    paint(h, wire, keep);
  };
  const wire = () => {
    noCta();
    main.querySelectorAll('[data-c]').forEach(b => b.onclick = () => {
      const i = +b.dataset.c, at = so.cuts.indexOf(i);
      if (at >= 0) so.cuts.splice(at, 1); else if (so.cuts.length < 2) so.cuts.push(i);
      so.cuts.sort((a, b2) => a - b2);
      if (so.cuts.length === 2) {
        const [c1, c2] = so.cuts, [s1, s2] = D.tr.cuts, t = D.tr.tol;
        S.tr.p4 = Math.abs(c1 - s1) <= t && Math.abs(c2 - s2) <= t;
        render(true);
        $('#fb5').innerHTML = fb5(S.tr.p4) + '<div style="font-size:12.5px;color:var(--ink-muted);margin-top:6px">切好了，下面还有第 2 件事。</div>'
          + '<button class="cta ghost" style="margin-top:10px" onclick="document.getElementById(\'c1\').scrollIntoView({behavior:\'smooth\',block:\'start\'})">去起小标题 ›</button>';
        setTimeout(() => { const el = document.getElementById('c1'); if (el) el.scrollIntoView({behavior:'smooth', block:'start'}); }, 280);
      } else render(true);
    });
    const inp = main.querySelectorAll('[data-t]');
    const ta = $('#main1');
    const check = () => {
      so.titles = [...inp].map(x => x.value.trim());
      so.main = ta ? ta.value.trim() : '';
      const L = so.main.length;
      if (ta) { $('#mc').textContent = L; $('#mc').style.color = L > 30 ? 'var(--warn)' : ''; }
      const filledT = so.titles.filter(x => x.length >= 1).length;
      const cliche = /表达了作者|思想感情|中心思想/.test(so.main);
      // 达标（内部判定，进微技能记录）
      const okT = filledT === 3 && so.titles.every(x => x.length >= 2 && x.length <= 6);
      const okM = L >= 8 && L <= 30 && !cliche && D.tr.mainkw.some(k => so.main.includes(k));
      // 放行（能不能去第 5 步）：门槛压到最低，不把人卡死
      const pass = filledT === 3 && L >= 8;
      S.tr.titles = okT; S.tr.p5 = okM;
      if (!$('#need')) return;
      if (!pass) {                                   // 还差什么，逐条说清楚
        const need = [];
        if (filledT < 3) need.push('还有 <b>' + (3 - filledT) + '</b> 块没起名字');
        if (L < 8) need.push('一句话还差 <b>' + (8 - L) + '</b> 字');
        $('#need').innerHTML = '<div class="fb">还差：' + need.join(' ｜ ') + '<br>'
          + '<span style="color:var(--ink-muted)">填齐就能去下一步。</span></div>';
        $('#fb6').innerHTML = ''; noCta();
        return;
      }
      const tips = [];
      if (!okT) tips.push('小标题最好每块 2–6 个字');
      if (cliche) tips.push('把「表达了作者的思想感情」这类套话换掉——放哪篇都通，等于没说');
      else if (L > 30) tips.push('这句 ' + L + ' 字，删到 30 字以内更好');
      else if (L >= 8 && !D.tr.mainkw.some(k => so.main.includes(k))) tips.push('最好把这篇的关键词带进去（记忆／童年／牢／准）');
      $('#need').innerHTML = '';
      $('#fb6').innerHTML = (okT && okM)
        ? '<div class="fb ok">✓ 三块都起了名字，一句话也压进 30 字了。'
          + K('这件事得连着三篇都做到才算真会——今天是第一篇。', '同一项技能在<b>三篇不同文本</b>上连续达标，才算过关。') + '</div>'
        : '<div class="fb">够了，可以往下走。<br><span style="color:var(--ink-muted)">要更好的话：' + tips.join('；') + '。</span></div>';
      cta('最后一步：写一句', () => go('train', 4));
    };
    inp.forEach(x => x.oninput = check); if (ta) { ta.oninput = check; check(); }
  };
  render(false);
}
function tWrite(){
  paint(stepHead('第 5 步 · 约 2 分钟', '写一句就收工', '一次最低门槛输出 · 写作回应文本 ES≈+0.40',
        K('这一步不能跳。但真的只要一句话，写完今天就结束了。',
          '证据最强的一环（写作回应文本 ES≈+0.40），所以它<b>不可跳过</b>——但门槛只有一句话。'))
   + '<div class="qh">读完这篇，你想起自己小时候的哪件事？你觉得它更像是「记得牢」的那一半，还是「记不准」的那一半？</div>'
   + '<textarea id="w" placeholder="写一句就行，15 个字起步。">' + esc(S.tr.writeText || '') + '</textarea>'
   + '<div class="cnt"><span id="wc">' + (S.tr.writeText || '').length + '</span> 字 · ' + K('满 15 字就能收工', '门槛 15 字') + '</div>'
   + '<div id="wneed"></div>'
   + K('<div class="fb">写完这句，今天这一篇就完了。不用写长，写你真想到的那件事就行。</div>',
       '<div class="fb">产品里这里原本有一个「跳过」按钮。07 的审查结论是：<b>把效应量最大的零件做成选项，等于没做。</b>'
       + '所以「跳过」被改成了「只写一句」——退出通道还在，但退出的终点仍然是一次输出。</div>'), () => {
    const ta = $('#w');
    const check = () => { const v = ta.value.trim(); S.tr.writeText = ta.value;
      $('#wc').textContent = v.length; S.tr.write = v.length >= 15;
      const nd = $('#wneed');
      if (nd) nd.innerHTML = S.tr.write ? '' : '<div class="fb">还差 <b>' + (15 - v.length) + '</b> 字就能收工。</div>';
      S.tr.write ? cta('写好了', () => go('wfb')) : noCta(); };
    ta.oninput = check; noCta(); check();
  });
}
function scTDone(){
  stopClock(); steps(TRSTEPS2, 5); setTop('今天读完了', D.tr.title, () => go(S.tr.writeText ? 'wfb' : 'train', S.tr.writeText ? undefined : 4), true);
  if (MODE === 'kid') return scTDoneKid();
  const done = [
    ['P7','理解监控', S.tr.markWhy !== undefined],
    ['O1','题干拆解', !!S.tr.o1],
    ['O2','分值→要点数', !!S.tr.o2],
    ['O4','证据句挂钩', !!S.tr.o4],
    ['P4','结构切块', !!S.tr.p4],
    ['P5','主旨压缩', !!S.tr.p5],
  ];
  const n = done.filter(d => d[2]).length;
  paint('<div class="big"><div class="n">' + n + '/6</div><div class="t">今天这一篇上达标的微技能</div></div>'
   + '<div class="card"><div class="eyebrow">判定</div>'
   + done.map(d => '<div class="sk"><span class="id">' + d[0] + '</span><span class="b"><b>' + d[1] + '</b>'
     + '<span>' + (d[2] ? '本篇达标 · 进度 1/3' : '本篇未达标 · 进度 0/3') + '</span></span>'
     + '<span class="st ' + (d[2] ? 'on' : '') + '">' + (d[2] ? '✓ 达标' : '再来') + '</span></div>').join('')
   + '<p class="note"><b>过关＝在三篇不同文本上连续达标</b>（防止「这篇正好会」）。过关后第 2 周、第 6 周各回测一次；回测失败就降级回训练池，但进度不清零。</p></div>'
   + '<div class="card"><div class="eyebrow">这 15 分钟里发生了什么</div>'
   + '<table class="rules"><tr><td class="nm">猜</td><td>先押一个答案，读的时候有事可做</td></tr>'
   + '<tr><td class="nm">读</td><td>必须标一处没懂 —— 理解监控</td></tr>'
   + '<tr><td class="nm">问</td><td>审题 → 要点数 → 答点 → 挂证据</td></tr>'
   + '<tr><td class="nm">辨</td><td>切块 → 起标题 → 压一句话</td></tr>'
   + '<tr><td class="nm">写</td><td>一次最低门槛输出，不可跳过</td></tr></table>'
   + '<p class="note">五步没变（05 的猜·读·问·辨·写），变的只是每一步挂了什么靶点。靶点按画像轮换，篇目不变、时长不变。</p></div>'
   + foot(), () => cta('看 17 个微技能与 12 周疗程', () => go('skills')));
}

/* 写完那一句之后，先回应「你写的这句」，再去结算。
   判定全部按字面算（Demo 不接 AI），并如实告诉孩子这一点。 */
function scWriteBack(){
  stopClock(); steps(TRSTEPS2, 4); setTop('你写的这句', D.tr.title, () => go('train', 4), true);
  const t = (S.tr.writeText || '').trim();
  const self = /我|我们|咱|自己/.test(t);
  const half = /牢|记得住|记得清|清楚|准|记错|不一定|改/.test(t);
  const detail = t.length >= 25 || /年级|岁|那年|第一次|夏天|冬天|奶奶|外婆|妈妈|爸爸|同学/.test(t);
  const rows = [
    [self, '写的是你自己的事', '这一点最关键——把读到的东西接到自己身上，比复述文章有用得多。',
           '下次试试写自己身上的一件事。哪怕很小，也比转述文章里的例子强。'],
    [half, '说清了是「牢」还是「准」', '你没有只停在「我记得」，而是说了它属于哪一半——这正是这篇文章的分法。',
           '可以再补半句：这件事你是记得特别牢，还是其实不一定准？'],
    [detail, '带了具体的细节', '有时间、有场景，别人读了能看见画面。',
           '再加一个细节——几年级、在哪儿、谁在场——这句就立起来了。'],
  ];
  const got = rows.filter(r => r[0]).length;
  paint('<div class="card"><div class="eyebrow">你刚才写的</div>'
   + '<div class="said" style="margin:0">' + esc(t) + '</div></div>'
   + '<div class="card"><div class="eyebrow">读了你这句，说三点</div>'
   + rows.map(r => '<div class="did"><span class="m ' + (r[0] ? '' : 'no') + '">' + (r[0] ? '✓' : '+') + '</span>'
     + '<span class="t"><b>' + r[1] + '</b>' + (r[0] ? r[2] : r[3]) + '</span></div>').join('')
   + '<p class="note">' + (got === 3 ? '三样都有了。这句话可以直接放进作文里。'
       : (got === 0 ? '这三样一样都还没有——不着急，明天那篇再试一次。' : '有了 ' + got + ' 样，剩下的下次补。')) + '</p></div>'
   + '<div class="card"><div class="eyebrow">别人写了什么（模拟）</div>'
   + '<div class="quote"><b>初一 · 同龄人</b>三年级我被狗追过，现在还记得那条巷子的味道，但我妈说那狗根本没追我。</div>'
   + '<div class="quote"><b>初一 · 同龄人</b>我记得幼儿园毕业照我哭了，可照片上我在笑——大概是听我爸讲了太多遍。</div>'
   + '<p class="note">拿自己那句跟这两句比一下：差在细节，还是差在「哪一半」？</p></div>'
   + '<div class="fb">这三条是按你写的字面算的（Demo 不联网、不接 AI）。'
   + '真实产品里这一步由 AI 读你写的<b>内容</b>——你的看法站不站得住、漏了文章里的哪一处——那是整套里最值得花钱的一环。</div>'
   + '<div class="kidfoot">写完这句，今天这一篇就真的结束了。</div>',
   () => cta('看看今天做到了什么', () => go('tdone')));
}

/* 孩子看到的收尾：做到了什么 ＋ 明天还有一篇。没有编号，没有进度条式的评分 */
function scTDoneKid(){
  const done = [
    ['标出了一处没看懂的地方', S.tr.markWhy !== undefined, '不懂的地方能被你自己揪出来，比全篇点头有用得多',
      '读的时候点任意一段，再选是「词不懂／关系不懂／背景不懂」。', 1],
    ['把题目要什么拆清楚了', !!S.tr.o1, '要你干什么、去哪儿找、写几点',
      '这道题的三样是：<b>说说</b>（干什么）· <b>第⑤⑥段</b>（去哪找）· <b>答两点</b>（写几点）。', 2],
    ['按分数定了写几点', !!S.tr.o2, '4 分写两点，这条以后每道大题都用得上',
      '<b>4 分 → 写 2 点</b>。老师按「点」给分，不按你写得多长给。', 2],
    ['给答案找了原文撑着', !!S.tr.o4, '找不到句子撑的那点，多半不是答案',
      '能撑住的是这两句之一：「被取用得越多的记忆，越不容易丢失」「每取出来一次，记忆都有可能被改一点」。', 2],
    ['把文章切成了三块', !!S.tr.p4, '切开了，概括就不会抓瞎',
      '标准切法：<b>第①②段｜第③④⑤段｜第⑥段起</b> —— 提出问题 ｜ 三个原因 ｜ 牢与准的两面。', 3],
    ['一句话说清了全文', !!S.tr.p5, '30 字以内，还不是套话',
      '照这个样子写就行：<b>「童年的事记得牢，但不一定准，因为它被反复讲述。」</b>（23 字，有主体、有原因，不是套话）', 3],
    ['写了一句自己的话', !!S.tr.write, '今天这篇真正属于你的那部分',
      '写自己身上的一件小事，15 个字起步——写完那一步会逐句回应你。', 4],
  ];
  const good = done.filter(d => d[1]).length;
  const todo = done.filter(d => !d[1]);
  paint('<div class="big"><div class="n">今天读完了</div><div class="t">' + D.tr.title + ' · 用了五步</div></div>'
   + '<div class="said">这一篇里你做到了 <b>' + good + '</b> 件事。'
   + (good >= 6 ? '挺稳的，明天换一篇再来一次。' : '没做到的那几件，明天那篇还会再遇到，不用着急。') + '</div>'
   + '<div class="card"><div class="eyebrow">具体是哪几件</div>'
   + done.map(d => '<div class="did"><span class="m ' + (d[1] ? '' : 'no') + '">' + (d[1] ? '✓' : '–') + '</span>'
     + '<span class="t"><b>' + d[0] + '</b>' + d[2] + '</span></div>').join('')
   + '<p class="note">同一件事连着三篇都做到，才算真的会了。今天是第一篇。</p></div>'
   + (todo.length ? '<div class="card"><div class="eyebrow">今天要钉正的</div>'
       + '<h2 class="sec">' + todo.length + ' 件没做到，正解在这儿</h2>'
       + '<p class="sub">看完可以当场回去改一次——改过的才算今天真做到了。</p>'
       + todo.map((d, k) => '<div class="did" style="flex-direction:column;align-items:stretch;gap:6px">'
           + '<b style="color:var(--ink);font-size:15px">' + d[0] + '</b>'
           + '<div style="font-size:13.5px;color:var(--ink-2);line-height:1.75">' + d[3] + '</div>'
           + '<button class="cta ghost" data-fix="' + d[4] + '" style="margin:2px 0 0">现在回去改一下 ›</button></div>').join('')
       + '</div>' : '<div class="card"><div class="eyebrow">今天要钉正的</div><h2 class="sec">没有</h2>'
       + '<p style="margin:0">七件全做到了，今天不用回头。</p></div>')
   + (S.tr.writeText ? '<div class="card"><div class="eyebrow">今天你留下的一句话</div>'
       + '<div class="said" style="margin:0">' + esc(S.tr.writeText.trim()) + '</div>'
       + '<p class="note">这些句子会一句句攒起来。攒够一学期，就是一本只属于你的读书笔记。</p></div>' : '')
   + '<div class="card"><div class="eyebrow">明天</div><h2 class="sec">还有一篇，一样十五分钟</h2>'
   + '<p>今天到这儿就结束了，不用再往下刷。<b>断一天也不清零</b>，回来接着读就行。</p></div>'
   + '<div class="kidfoot"><a href="javascript:void(0)" id="toPro">这些练的是什么，给大人看 ›</a></div>',
   () => { noCta(); $('#toPro').onclick = () => { MODE = 'pro'; go('skills'); };
     main.querySelectorAll('[data-fix]').forEach(b => b.onclick = () => go('train', +b.dataset.fix)); });
}

/* ══ 8. 微技能面板 / 疗程 / 说明 ══ */
function scSkills(){
  MODE = 'pro';
  stopClock(); steps(null); setTop('17 个微技能', '可训练＝可判定', () => go('tdone'), true);
  const doneMap = {P7: S.tr.markWhy !== undefined, O1: !!S.tr.o1, O2: !!S.tr.o2, O4: !!S.tr.o4, P4: !!S.tr.p4, P5: !!S.tr.p5};
  const rx = S.prof ? S.prof.rx.map(r => r[0]).join(' ') : '';
  paint('<div class="card"><div class="eyebrow">规则</div><h2 class="sec">写不出过关标准的，不写进课表</h2>'
   + '<p>一项能力如果说不出「做到什么算过关」，它就不可训练，只能被消费。下面每一项都带判定条件，'
   + '其中 <b>6 项全员必练</b>，其余按画像启用。</p></div>'
   + D.skills.map(g => '<div class="card"><div class="eyebrow">闸门 ' + g[0] + ' · ' + g[1] + '</div>'
     + g[2].map(s => {
         const star = D.star.includes(s[0]), core = D.core.includes(s[0]);
         const st = doneMap[s[0]] ? 'on' : (rx.includes(s[0]) ? 'tr' : '');
         const lab = doneMap[s[0]] ? '✓ 1/3' : (rx.includes(s[0]) ? '在训' : (core ? '必练' : '未测'));
         return '<div class="sk"><span class="id">' + s[0] + '</span><span class="b"><b>' + s[1]
           + (star ? ' ⭐' : '') + '</b><span>' + esc(s[2]) + '</span></span><span class="st ' + st + '">' + lab + '</span></div>'; }).join('')
     + '</div>').join('')
   + '<p class="note">⭐ ＝主干技能；同时在训 ≤3 个。全员必练六项：P4 结构切块 · P5 主旨压缩 · P7 理解监控 · O1 题干拆解 · O2 分值→要点数 · O4 证据句挂钩。</p>'
   + foot(), () => cta('看 12 周疗程', () => go('plan')));
}
function scPlan(){
  MODE = 'pro';
  stopClock(); steps(null); setTop('12 周疗程', '每天 15 分钟', () => go('skills'), true);
  const ph = [
    ['定位期','第 1–2 周','画像成形、建立输出习惯','全员：P7 ＋ O1 ＋ 每篇一句话输出','画像稳定；输出率 ≥70%'],
    ['主攻期','第 3–8 周','攻画像的主病因','按处方，同时在训 ≤3 项','每 4 周至少 2 个微技能过关'],
    ['合拢期','第 9–11 周','三闸门串起来','审题→定位→切块→要点→证据 跑单篇','周测 O2/O4 达标率 ≥80%'],
    ['回测期','第 12 周','迁移验证','产品外陌生文本盲测','与第 1 周同难度基线对比'],
  ];
  paint('<div class="card"><div class="eyebrow">节奏</div><h2 class="sec">每天 15 分钟 × 5 天 ＋ 1 次周测</h2>'
   + '<p class="sub">嵌进首月已定的内容节奏（12 篇精读 ＋ 16 则晨读），<b>不新增时长，只换靶点</b>。</p>'
   + '<div class="tl">' + ph.map(p => '<div class="ph"><b>' + p[0] + '</b><i>' + p[1] + '</i>'
     + '<p>' + p[2] + '<br><span style="color:var(--ink-muted)">靶点：' + p[3] + '</span>'
     + '<br><span style="color:var(--accent)">验收：' + p[4] + '</span></p></div>').join('') + '</div></div>'
   + '<div class="card"><div class="eyebrow">怎么知道有没有用</div><h2 class="sec">四层指标</h2>'
   + '<table class="rules"><tr><td class="nm">诊断</td><td>两周内画像稳定率</td><td class="vl">≥80%</td></tr>'
   + '<tr><td class="nm">过程</td><td>带证据的输出率</td><td class="vl">≥70%</td></tr>'
   + '<tr><td class="nm">训练</td><td>月度微技能过关数</td><td class="vl">≥2 个</td></tr>'
   + '<tr><td class="nm">迁移</td><td>12 周产品外盲测 vs 第 1 周基线</td><td class="vl">显著优于</td></tr></table>'
   + '<p class="note">完成率仍是北极星（它决定商业存活），但效果指标是输出率与过关数——两套指标不能混用。</p></div>'
   + '<div class="card"><div class="eyebrow">怎么杀死这个方案</div><h2 class="sec">分诊值不值得做，要能被证伪</h2>'
   + '<p>A 组分诊施治，B 组不分诊走统一课表，12 周后比微技能过关数与盲测迁移分。'
   + '<b>A 组不显著优于 B 组，就砍掉分诊</b>——它是纯成本，不产生内容价值。</p>'
   + '<p class="note">样本量：预期 d≈0.3、α=0.05、power=0.8 → 每组约 175 人。</p></div>'
   + '<div class="card"><div class="eyebrow">关于这个 Demo</div>'
   + '<p>选文与练习取自首月内容库（原创选文版权自持；课内篇目与公版名著另行标注）。'
   + '分诊探针、靶点交互、判定阈值按方案 09 实现，为便于试玩做了压缩：首测 20 分钟→8 分钟，词义速判 20 题→10 题。</p>'
   + '<p>同龄人分布为模拟数据。你的作答只留在本机内存里，刷新即清空，不上传任何服务器。</p></div>'
   + foot(), () => cta('再测一次', () => { location.reload(); }, true));
}

/* ══ 路由 ══ */
const R = {intro: scIntro, read: scRead, q: scQ, retell: scRetell, bj: scBJ, vocab: scVocab,
           report: scReport, review: scReview, fix: scFix,
           train: scTrain, wfb: scWriteBack, tdone: scTDone, skills: scSkills, plan: scPlan};
function go(name, arg){ CUR = [name, arg]; (R[name] || scIntro)(arg); }
go('intro');
"""

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>读得深 · 三道闸门：初一分诊与训练 Demo</title>
<meta name="description" content="初中生阅读问题诊断与可训练提升方案的可试玩版：20 分钟分诊分出三道闸门与六种画像，再领一份 15 分钟训练块。">
<meta name="theme-color" content="#f9f9f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d0d0d" media="(prefers-color-scheme: dark)">
<style>__CSS__</style>
</head>
<body>
<div class="app">
  <div class="top">
    <div class="row">
      <button class="back hide" id="back">‹ 返回</button>
      <div class="brand" id="brand">三道闸门</div>
      <div class="clock hide" id="clock">0:00</div>
      <button class="mode hide" id="mode"></button>
    </div>
    <div class="steps hide" id="steps"></div>
  </div>
  <div id="main"></div>
</div>
<div class="bar-fixed hide" id="bar"><div class="in"><button class="cta" id="barbtn">继续</button></div></div>
<script>__JS__</script>
</body>
</html>
"""

js = (JS + JS2).replace('__DATA__', json.dumps(DATA, ensure_ascii=False))
html = HTML.replace('__CSS__', CSS).replace('__JS__', js)
path = os.path.join(OUT_DIR, 'index.html')
open(path, 'w', encoding='utf-8').write(html)
print('生成 %s（%.1f KB）' % (path, len(html.encode('utf-8')) / 1024))
