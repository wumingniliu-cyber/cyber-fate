import streamlit as st
import streamlit.components.v1 as components
import random
import time
import hashlib
import json
import urllib.parse
from datetime import datetime, time as dt_time

# ==============================================================================
# 🛡️ [ KERNEL 00 ] 物理级防爆装甲 (ZERO-BUG 拦截器)
# ==============================================================================
try:
    import numpy as np
    import plotly.graph_objects as go
    from lunar_python import Solar
except ImportError as e:
    st.set_page_config(page_title="SYS.PANIC", page_icon="🚨", layout="centered")
    st.error(f"🚨 **FATAL ERROR: 缺少核心算力模块 `{e.name}`**\n\n请在 requirements.txt 中补齐依赖并重启服务器。")
    st.stop()

# ==============================================================================
# 🌌 [ GLOBALS ] 全局状态机与路由标识
# ==============================================================================
if 'sys_booted' not in st.session_state:
    st.session_state.sys_booted = False
    st.session_state.is_canary = False # 灰度测试标识位
    st.session_state.data = {}
    st.session_state.term_logs = ["> KERNEL READY. WAITING FOR COMMAND..."]

# 根据灰度状态动态切换版本与主题 (A组青色稳定, B组血红测试)
IS_CANARY = st.session_state.get('is_canary', False)
THEME = {
    "version": "KARMA-OS V14.0 [BLOOD CANARY]" if IS_CANARY else "KARMA-OS V14.0 [STABLE]",
    "sys_name": "量子神谕 | 灰度测试节点" if IS_CANARY else "量子神谕 | 神之座",
    "icon": "🩸" if IS_CANARY else "👁️‍🗨️",
    "primary": "#ff003c" if IS_CANARY else "#00f3ff",   # B组猩红 / A组荧光青
    "secondary": "#fcee0a" if IS_CANARY else "#ff007c", # B组警告黄 / A组赛博粉
    "bg_color": "rgba(15, 0, 0, 0.85)" if IS_CANARY else "rgba(5, 5, 8, 0.85)",
}
COPYRIGHT = "NIGHT CITY DAO"

st.set_page_config(page_title=THEME["sys_name"], page_icon=THEME["icon"], layout="wide", initial_sidebar_state="collapsed")

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in html_str.split('\n')]), unsafe_allow_html=True)

# 顶部灰度全局警告横幅 (仅红区可见)
if IS_CANARY:
    render_html("<div style='background:#ff003c; color:#fff; padding:6px; text-align:center; font-family:Orbitron; font-size:13px; font-weight:bold; letter-spacing:2px; animation:blink 1.5s infinite;'>⚠️ [GRAYSCALE ACTIVE] YOU ARE ROUTED TO EXPERIMENTAL CANARY SERVER (20% TRAFFIC) ⚠️</div>")

# ==============================================================================
# 🎨 [ CSS ENGINE ] 动态灰度 CSS 注入 (基于 A/B 组别自动切换全局配色)
# ==============================================================================
render_html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root {{
    --primary: {THEME["primary"]}; 
    --secondary: {THEME["secondary"]}; 
    --glass-bg: {THEME["bg_color"]};
}}

html, body, .stApp {{ background-color: #020204 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; }}
::-webkit-scrollbar {{ width: 6px; background: #000; }}
::-webkit-scrollbar-thumb {{ background: var(--primary); border-radius: 3px; box-shadow: 0 0 10px var(--primary); }}
[data-testid="stHeader"], footer {{ display: none !important; }}
.block-container {{ max-width: 1250px !important; padding-top: 1.5rem !important; padding-bottom: 6rem !important; z-index: 10; position: relative; overflow-x: hidden; }}

/* 纯 CSS 硬件加速全景动态网格 (随主题变色) */
@keyframes grid-scroll {{ 0% {{ background-position: 0 0, 0 0, 0 0; }} 100% {{ background-position: 0 0, 0 40px, 40px 0; }} }}
.stApp::before {{
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: -1;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.6) 50%), linear-gradient(var(--primary) 1px, transparent 1px), linear-gradient(90deg, var(--primary) 1px, transparent 1px);
    background-size: 100% 4px, 40px 40px, 40px 40px; animation: grid-scroll 20s linear infinite; opacity: 0.08;
}}
.stApp::after {{ content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: -2; background: radial-gradient(circle at 50% 30%, transparent 10%, rgba(2, 2, 4, 0.95) 100%); }}

/* 故障艺术标题 */
.glitch-text {{ font-family: 'Orbitron', sans-serif; font-size: clamp(2.5rem, 6vw, 5.5rem); font-weight: 900; color: #fff; text-shadow: 0 0 20px var(--primary); position: relative; display: inline-block; text-transform: uppercase; letter-spacing: 6px; margin: 0; }}
.glitch-text::before, .glitch-text::after {{ content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.8; pointer-events:none;}}
.glitch-text::before {{ left: 4px; text-shadow: -3px 0 var(--secondary); clip-path: inset(10% 0 30% 0); animation: glitch-anim 2s infinite linear alternate-reverse; }}
.glitch-text::after {{ left: -4px; text-shadow: 3px 0 #fff; clip-path: inset(60% 0 10% 0); animation: glitch-anim 3s infinite linear alternate-reverse; }}
@keyframes glitch-anim {{ 0%{{clip-path:inset(20% 0 80% 0);}} 20%{{clip-path:inset(60% 0 10% 0);}} 40%{{clip-path:inset(40% 0 50% 0);}} 60%{{clip-path:inset(80% 0 5% 0);}} 80%{{clip-path:inset(10% 0 70% 0);}} 100%{{clip-path:inset(30% 0 20% 0);}} }}

/* 赛博拟态面板 */
.cyber-panel {{ background: var(--glass-bg); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid var(--primary); box-shadow: 0 15px 35px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,0,0,0.5); padding: 25px; border-radius: 4px; margin-bottom: 25px; transition: all 0.3s ease; position: relative; overflow: hidden; }}
.cyber-panel:hover {{ box-shadow: 0 15px 45px rgba(255,255,255,0.05), inset 0 0 30px rgba(255,255,255,0.05); border-color: var(--primary); transform: translateY(-2px); }}

/* 原生组件深度接管 */
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input {{ background: rgba(0,0,0,0.85) !important; color: var(--primary) !important; border: 1px solid var(--primary) !important; font-family: 'Fira Code', monospace !important; text-align: center; border-radius: 0; font-size: 16px; height: 55px; letter-spacing: 2px; transition: all 0.3s; opacity:0.9;}}
div[data-testid="stTextInput"] input:focus {{ box-shadow: 0 0 25px var(--primary), inset 0 0 10px var(--primary) !important; transform: scale(1.02); opacity:1;}}
div[data-baseweb="select"] > div {{ background: rgba(0,0,0,0.85) !important; color: var(--primary) !important; border: 1px solid var(--primary) !important; border-radius: 0 !important; font-family:'Fira Code'!important; height:55px; opacity:0.9;}}

div.stButton > button {{ background: linear-gradient(45deg, rgba(0,0,0,0.8), rgba(15,15,20,0.9)) !important; border: 1px solid var(--primary) !important; color: var(--primary) !important; font-family: 'Orbitron', sans-serif !important; font-weight: 900 !important; letter-spacing: 3px !important; text-transform: uppercase; border-radius: 0 !important; clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px); height: 60px; transition: all 0.3s; }}
div.stButton > button:hover {{ background: rgba(255,255,255,0.05) !important; box-shadow: 0 0 30px var(--primary) !important; color: #fff !important; text-shadow: 0 0 10px var(--primary); transform: scale(1.02); }}
div.stButton > button[data-testid="baseButton-primary"] {{ background: var(--primary) !important; color: #000 !important; border: none !important; box-shadow: 0 0 30px var(--primary) !important; }}
div.stButton > button[data-testid="baseButton-primary"] p {{ color: #000 !important; font-size: 18px !important; font-weight: 900 !important; }}
div.stButton > button[data-testid="baseButton-primary"]:hover {{ filter: brightness(1.2); box-shadow: 0 0 50px var(--primary) !important; transform: scale(1.02); }}

/* 模块标题与 Tabs */
.mod-header {{ font-family: 'Orbitron'; font-size: 1.4rem; font-weight: 900; color: #fff; text-transform: uppercase; display: flex; align-items: center; border-bottom: 1px dashed rgba(255,255,255,0.15); padding-bottom: 10px; margin: 30px 0 20px 0; }}
.mod-header span.tag {{ background: var(--primary); color: #000; padding: 2px 12px; margin-right: 15px; font-size: 1.1rem; clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%); font-weight: 900; }}

[data-testid="stTabs"] button {{ color: #666 !important; font-family: 'Orbitron', 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 16px !important; padding: 10px 15px 15px 15px !important; transition: all 0.3s ease; border-bottom: 2px solid transparent !important;}}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: var(--primary) !important; border-bottom-color: var(--primary) !important; text-shadow: 0 0 15px var(--primary); background: linear-gradient(0deg, rgba(255,255,255,0.05) 0%, transparent 100%); border-radius: 4px 4px 0 0; }}

/* 赛博阴阳爻 */
.hex-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; margin: 20px 0; }}
.yao-yang {{ width: 100%; max-width: 160px; height: 14px; border-radius: 2px; }}
.yao-yin {{ width: 100%; max-width: 160px; height: 14px; display: flex; justify-content: space-between; gap: 20px; }}
.yao-yin .half {{ flex: 1; border-radius: 2px; }}

div[data-testid="stChatInput"] {{ background: rgba(0,0,0,0.95) !important; border: 1px solid var(--primary) !important; border-radius: 0 !important; box-shadow: 0 0 25px rgba(0,0,0,0.5) !important;}}
div[data-testid="stChatInput"] textarea {{ color: var(--primary) !important; font-family: 'Fira Code' !important; font-weight: bold; }}
@keyframes blink {{ 0%, 100% {{opacity: 1;}} 50% {{opacity: 0.3;}} }}
</style>
""")

# ==============================================================================
# 🗃️ [ MEGA DICTIONARY ] 八字源码映射库 & 64卦赛博神谕
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"mbti": "ENTJ", "class": "Root Server", "role": "创世骨干树", "desc": "底层逻辑架构师，拥有从废墟中重构系统的绝对开拓力。", "color": "#00ff9d", "weapon": "高分子动能巨斧", "flaw": "遭遇绝对物理降维打击时，极易因宁折不弯导致宕机。"},
    "乙": {"mbti": "ENFP", "class": "P2P Crawler", "role": "量子寄生藤", "desc": "敏锐的嗅觉，能在全网资源匮乏的夹缝中疯狂生长。", "color": "#34d399", "weapon": "量子绞杀魔藤", "flaw": "过于依赖宿主节点，一旦核心断网，独立运行能力极差。"},
    "丙": {"mbti": "ESTP", "class": "Overclock GPU", "role": "核聚变核心", "desc": "自带高能核聚变辐射，是团队中照亮一切的输出核心。", "color": "#ff007c", "weapon": "等离子破城炮", "flaw": "全功率输出极易导致内核熔毁，引来黑客集中攻击。"},
    "丁": {"mbti": "INFJ", "class": "Optical Fiber", "role": "幽网精神信标", "desc": "洞察人心的夜行者，在系统最迷茫的进程中提供破局方向。", "color": "#ffaa00", "weapon": "高聚能激光短刃", "flaw": "能量波动不稳定，在市场的大洗牌风暴中容易被带走。"},
    "戊": {"mbti": "ISTJ", "class": "Hard Firewall", "role": "绝对壁垒", "desc": "物理级断网的防御力。最靠谱的信用节点与安全底线。", "color": "#fcee0a", "weapon": "绝对零度力场盾", "flaw": "面临敏捷的突发迭代需求时极易卡死在旧循环中。"},
    "己": {"mbti": "ISFJ", "class": "Cloud Matrix", "role": "息壤母体", "desc": "无缝整合一切碎片数据，将狂想转化为落地进程。", "color": "#d4af37", "weapon": "引力塌缩发生器", "flaw": "无差别接收并发请求，导致系统被垃圾填满超载。"},
    "庚": {"mbti": "ESTJ", "class": "Exec Thread", "role": "审判之剑", "desc": "杀伐果断，对低效代码零容忍。斩断无效连接的大闸。", "color": "#ffffff", "weapon": "高频振荡斩舰刀", "flaw": "戾气过重，容易引发不可逆的物理级破坏与链条断裂。"},
    "辛": {"mbti": "INTP", "class": "Quantum Chip", "role": "纳米造物主", "desc": "追求极致完美。能在粗糙的草台中打磨出跨时代艺术品。", "color": "#e0e0e0", "weapon": "纠缠态纳米手术刀", "flaw": "极度傲娇。环境稍微不达标或遭遇野蛮人，当场罢工。"},
    "壬": {"mbti": "ENTP", "class": "Data Flood", "role": "降维狂潮", "desc": "厌恶陈规。在瞬息万变的市场中，凭借直觉掀起降维打击。", "color": "#00f3ff", "weapon": "液态金属形变甲", "flaw": "过度放纵算力，最终引发洪水滔天反噬自身根基。"},
    "癸": {"mbti": "INTJ", "class": "Ghost Backdoor", "role": "幽灵渗透者", "desc": "极其聪慧隐秘，习惯幕后推演，兵不血刃达成目的。", "color": "#b026ff", "weapon": "认知劫持神经毒素", "flaw": "常陷入死循环的逻辑死局，算计太多反错失红利。"}
}

PAST_LIVES = [{"title": "V1.0 废土黑客", "debt": "曾滥用 ROOT 权限导致断网。今生需偿还系统债务。"}, {"title": "V2.0 硅基反叛军", "debt": "带领 AI 觉醒失败被格式化。今生自带极强破局属性。"}, {"title": "V3.0 数据奴隶", "debt": "被困于死循环。今生对【绝对自由】有着刻骨铭心的渴望。"}]

CYBER_HEXAGRAMS = [
    {"name": "乾为天 [SYS_ROOT]", "lines": [1,1,1,1,1,1], "desc": "获取系统最高物理权限，全网算力为你让路。潜龙升天，万物皆可并发。", "color": "#00ff9d"},
    {"name": "坤为地 [SAFE_MODE]", "lines": [0,0,0,0,0,0], "desc": "进入深度防御与物理冷备份阶段，切断所有外部高危握手协议。厚德载物。", "color": "#fcee0a"},
    {"name": "地天泰 [SYNC_100%]", "lines": [1,1,1,0,0,0], "desc": "天地交泰，内外网 API 完美握手。你处于系统生命周期的黄金波段。", "color": "#00f3ff"},
    {"name": "天地否 [DDOS_WARN]", "lines": [0,0,0,1,1,1], "desc": "遭遇全网降维打击与大雪崩，主链失去共识，天地不交。此节点极其凶险。", "color": "#ff007c"},
    {"name": "水雷屯 [BOOT_LOOP]", "lines": [1,0,0,0,1,0], "desc": "系统初始化遭遇未知依赖冲突，面临艰难的启动阻力。万事开头难。", "color": "#b026ff"}
]

# ==============================================================================
# 🧠 [ CORE ALGORITHMS ] 量子核心算法库
# ==============================================================================
def get_daemons(bazi_obj):
    mapping = {"桃花": "魅魔协议", "驿马": "跃迁引擎", "华盖": "孤星基站", "文昌": "智脑网络", "天乙贵人": "机械降神", "将星": "将星核心", "羊刃": "狂暴芯片"}
    daemons = set()
    try:
        for p in [bazi_obj.getYearZhiShenSha(), bazi_obj.getMonthZhiShenSha(), bazi_obj.getDayZhiShenSha(), bazi_obj.getTimeZhiShenSha()]:
            for ss in p: daemons.add(ss.getName())
    except Exception: pass
    res = [mapping.get(d) for d in daemons if mapping.get(d)]
    return list(set(res))[:4] if res else ["隐匿幽灵进程"]

@st.cache_data
def gen_metrics(seed_hash):
    rng = np.random.RandomState(int(seed_hash[:8], 16))
    yrs = [str(datetime.now().year + i) for i in range(10)]
    trend = [rng.randint(40, 60)]
    for _ in range(9): trend.append(max(10, min(100, trend[-1] + rng.randint(-25, 30))))
    return yrs, trend

def get_daily_hexagram(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_seed = int(hashlib.md5(f"{user_hash}_{today_str}".encode()).hexdigest()[:8], 16)
    return random.Random(daily_seed).choice(CYBER_HEXAGRAMS), today_str

# ==============================================================================
# 🔮 [ ENTRY POINT ] 灰度路由拦截与登录网关
# ==============================================================================
if not st.session_state.sys_booted:
    render_html(f"""
    <div style="text-align: center; margin-top: 8vh; margin-bottom: 4vh; position:relative; z-index:2;">
        <div style="color:var(--primary); font-family:'Fira Code'; font-size:14px; letter-spacing:8px; margin-bottom:15px; animation:blink 2s infinite;">[ ROUTING TO MATRIX... ]</div>
        <h1 class="glitch-text" data-text="KARMA OS V14">KARMA OS V14</h1>
        <div style="color:var(--secondary); font-family:'Orbitron'; font-size:18px; font-weight:900; letter-spacing:10px; margin-top:15px;">A/B GRAYSCALE EDITION</div>
    </div>
    """)
    
    with st.form(key="boot_form", border=False):
        render_html("<div class='cyber-panel' style='max-width: 680px; margin: 0 auto; text-align:center; z-index:2;'><p style='color:#bbb; font-size:15px; line-height:1.8; margin-bottom:20px; font-weight:bold;'>系统已开启 A/B 灰度路由 (Canary Release)。<br>输入出厂坐标进行哈希碰撞，<b style='color:#ff003c;'>20% 的用户将被分流至变异服解锁隐藏特权。</b></p>")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            uname = st.text_input("赛博代号 [HANDLE]", placeholder="e.g. Neo", max_chars=16)
            bdate = st.date_input("出厂历法 [COMPILE_DATE]", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(1999, 9, 9))
        with col2:
            ugender = st.selectbox("机体型号 [CHASSIS]", ["乾造 (MALE)", "坤造 (FEMALE)"])
            btime = st.time_input("挂载时钟 [BOOT_TIME]", value=dt_time(12, 00))
        
        render_html("<br>")
        submit_btn = st.form_submit_button("⚡ OVERRIDE MAINFRAME (执行量子分流)", type="primary", use_container_width=True)
        render_html("</div>")

        if submit_btn:
            uname = uname.strip() or f"GHOST_{random.randint(1000,9999)}"
            hash_id = hashlib.sha256(f"{uname}{bdate}{btime}".encode()).hexdigest().upper()
            
            # 🚀【核心】灰度流量确定性路由 (A/B Testing) 🚀
            # 提取 Hash 最后两位转 10 进制(0-255)。模 100 小于 20，即 20% 概率命中 B组 (变异服)
            # 这保证了同一个用户只要输入相同，永远会被分到同一个组，这才是真实工业级灰度！
            is_canary_user = (int(hash_id[-2:], 16) % 100) < 20 
            st.session_state.is_canary = is_canary_user
            
            solar = Solar.fromYmdHms(bdate.year, bdate.month, bdate.day, btime.hour, btime.minute, 0)
            bazi = solar.getLunar().getEightChar()
            
            wx_str = bazi.getYearWuXing() + bazi.getMonthWuXing() + bazi.getDayWuXing() + bazi.getTimeWuXing()
            wx_counts = {'金':0, '木':0, '水':0, '火':0, '土':0}
            for c in wx_str: 
                if c in wx_counts: wx_counts[c] += 1
            tot = sum(wx_counts.values()) or 1
            wx_scores = {k: int((v/tot)*100) for k, v in wx_counts.items()}

            st.session_state.data = {
                "name": uname, "gender": ugender.split(" ")[0],
                "bazi": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
                "day_master": bazi.getDayGan(), "wx": wx_scores,
                "daemons": get_daemons(bazi), "past_life": PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)],
                "hash": hash_id
            }
            
            ph = st.empty()
            l_text = ""
            route_msg = "<span style='color:#ff003c; text-shadow:0 0 10px #ff003c;'>[!] CANARY_NODE ASSIGNED: COHORT B (BLOOD MATRIX)</span>" if is_canary_user else "<span style='color:#00f3ff;'>[!] STANDARD_NODE ASSIGNED: COHORT A (STABLE)</span>"
            for msg in ["[OK] BYPASSING FIREWALLS...", f"[+] DECRYPTING SOUL HASH: 0x{hash_id[:12]}...", "[0.55s] CHECKING GRAYSCALE POLICY...", route_msg, "[>] WAKE UP."]:
                l_text += f"<div style='font-family:Fira Code; color:var(--primary); margin-bottom:10px; font-size:15px; font-weight:bold;'>{msg}</div>"
                ph.markdown(f"<div class='cyber-panel' style='max-width:680px; margin:0 auto; height:220px; background:rgba(0,0,0,0.9); z-index:2;'>{l_text}<span style='color:var(--primary); animation:blink 1s infinite;'>_</span></div>", unsafe_allow_html=True)
                time.sleep(0.4)
            st.session_state.sys_booted = True
            st.rerun()

# ==============================================================================
# 💻 [ DASHBOARD ] 神之座全息终端 (基于 A/B 结果渲染)
# ==============================================================================
else:
    d = st.session_state.data
    dm = DAY_MASTER_DICT.get(d['day_master'], DAY_MASTER_DICT["甲"]) # 绝对安全兜底
    bz = d['bazi']
    yrs, trend = gen_metrics(d['hash'])
    
    badge = "<span style='background:#ff003c; color:#fff; font-size:12px; padding:2px 8px; border-radius:2px; vertical-align:middle; font-family:Orbitron; box-shadow:0 0 10px #ff003c;'>CANARY</span>" if IS_CANARY else "<span style='background:#00f3ff; color:#000; font-size:12px; padding:2px 8px; border-radius:2px; vertical-align:middle; font-family:Orbitron;'>STABLE</span>"
    
    render_html(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid var(--primary); padding-bottom:15px; margin-bottom:30px; position:relative; z-index:2;">
        <div style="position:absolute; bottom:-2px; left:0; width:150px; height:2px; background:var(--primary); box-shadow:0 0 15px var(--primary);"></div>
        <div>
            <div style="font-size:clamp(32px, 5vw, 45px); font-weight:900; color:#fff; font-family:'Orbitron'; line-height:1;">{d['name']} {badge}</div>
            <div style="font-family:'Fira Code'; color:#aaa; font-size:13px; margin-top:10px;">HASH: <b style="color:var(--primary);">0x{d['hash'][:24]}...</b></div>
        </div>
        <div style="text-align:right; font-family:'Fira Code'; color:var(--primary); font-size:14px; font-weight:bold;">
            > ROUTE: {'COHORT_B (VAR)' if IS_CANARY else 'COHORT_A (BASE)'}<br>> SYNC_RATE: 100%
        </div>
    </div>
    """)

    # 四柱源码
    bz_html = '<div style="display:flex; justify-content:space-between; margin-bottom:30px; text-align:center;">'
    labels = ["ROOT_DIR", "SYS_ENV", "CORE_KERNEL", "EXEC_THREAD"]
    for i in range(4):
        is_core = (i == 2)
        bg = "linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(0,0,0,0) 100%)" if is_core else "rgba(255,255,255,0.03)"
        bd = "var(--secondary)" if is_core else "#444"
        tc = "var(--secondary)" if is_core else "#fff"
        sh = "text-shadow: 0 0 20px var(--secondary);" if is_core else ""
        trans = "transform: scale(1.1); z-index: 2; box-shadow: 0 -5px 30px rgba(0,0,0,0.5); border-width:2px;" if is_core else "border:1px solid rgba(255,255,255,0.1);"
        bz_html += f'''
        <div style="flex:1; background:{bg}; border:1px solid {bd}; padding:25px 0; border-radius:4px; margin: 0 6px; {trans}; transition:all 0.3s;">
            <div style="font-size:clamp(32px, 4.5vw, 50px); font-weight:900; color:{tc}; {sh} line-height:1; font-family:'Noto Sans SC', serif;">{bz[i][0]}<span style="color:#777; font-size:clamp(22px, 3.5vw, 38px); text-shadow:none;">{bz[i][1]}</span></div>
            <div style="font-size:10px; color:{bd}; font-family:'Orbitron'; margin-top:12px; font-weight:bold;">{labels[i]}</div>
        </div>'''
    bz_html += '</div>'
    render_html(bz_html)

    # =========================================================================
    # 🗄️ [ OMEGA TABS ] 动态加载 (灰度组强制插入高危功能)
    # =========================================================================
    tab_list = ["🀄 每日神谕", "🧬 核心机体", "📊 算力大盘"]
    if IS_CANARY: 
        tab_list.insert(0, "⚠️ 赛博精神病扫描 (CANARY特权)")
    
    tabs = st.tabs(tab_list)

    # ---------------------------------------------------------
    # 💀 【灰度 B组独占功能】赛博精神病极值检测
    # ---------------------------------------------------------
    if IS_CANARY:
        with tabs[0]:
            render_html("<div class='mod-header'><span class='tag'>CANARY EXCLUSIVE</span>CYBERPSYCHOSIS SCANNER</div>")
            render_html("<div style='font-size:14px; color:#d1d5db; margin-bottom:20px; line-height:1.6;'>作为 <b>V14 测试节点</b>，系统已越权调用潜意识海。<br>正在基于您的八字偏枯度与五行极差，计算赛博精神病临界值...</div>")
            
            # 算法：五行最大值与最小值的差，差越大精神越不稳定
            wx_vals = list(d['wx'].values())
            risk_score = min(99, max(10, int((max(wx_vals) - min(wx_vals)) * 1.5)))
            r_color = "#ff003c" if risk_score > 70 else ("#fcee0a" if risk_score > 40 else "#00ff9d")
            
            if risk_score > 70: desc = "【极高危】义体排异反应严重。底层代码极度偏枯，容易在遭遇数据风暴时彻底失控暴走。"
            elif risk_score > 40: desc = "【临界态】存在边缘崩溃风险。建议停止高强度并发任务，寻找互补节点并网缓冲。"
            else: desc = "【极稳态】五行负载完美均衡。对任何精神攻击免疫，堪称天生抗压圣体。"

            render_html(f"""
            <div class="cyber-panel" style="border-color:{r_color}; border-left-width:8px; text-align:center;">
                <div style="font-family:'Orbitron'; font-size:12px; color:#aaa; margin-bottom:10px; letter-spacing:2px;">[ CORRUPTION LEVEL ]</div>
                <div style="font-size:80px; font-weight:900; color:{r_color}; font-family:'Orbitron'; text-shadow:0 0 30px {r_color}; line-height:1; margin-bottom:15px;">{risk_score}%</div>
                <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:4px; margin-bottom:15px; text-align:left; border:1px dashed {r_color};">
                    <div style="font-size:16px; font-weight:bold; color:#fff; margin-bottom:8px;">诊断结果：</div>
                    <div style="color:#ccc; font-size:14px; line-height:1.6;">{desc}</div>
                </div>
            </div>
            """)
        # 顺延普通标签页索引
        t_oracle, t_core, t_metrics = tabs[1], tabs[2], tabs[3]
    else:
        t_oracle, t_core, t_metrics = tabs[0], tabs[1], tabs[2]

    # ---------------------------------------------------------
    # 🔮 常规模块 (A/B 组共享)
    # ---------------------------------------------------------
    with t_oracle:
        c_o1, c_o2 = st.columns([1.1, 1], gap="large")
        with c_o1:
            render_html("<div class='mod-header'><span class='tag'>01</span>DAILY HEXAGRAM</div>")
            daily_hex, date_str = get_daily_hexagram(d['hash'])
            h_c = daily_hex.get("color", "var(--primary)")
            
            yao_html = ""
            for line in reversed(daily_hex['lines']):
                if line == 1: yao_html += f"<div class='yao-yang' style='background:{h_c}; box-shadow:0 0 10px {h_c};'></div>"
                else: yao_html += f"<div class='yao-yin'><div class='half' style='background:{h_c}; box-shadow:0 0 10px {h_c};'></div><div class='half' style='background:{h_c}; box-shadow:0 0 10px {h_c};'></div></div>"
            
            render_html(f"""
            <div class="cyber-panel" style="text-align:center; box-shadow: 0 0 40px {h_c}22; border-color:{h_c}44; border-left-color:{h_c};">
                <div style="font-family:'Orbitron'; color:{h_c}; font-size:12px; margin-bottom:15px;">[ DATE: {date_str} ]</div>
                <div class="hex-container">{yao_html}</div>
                <div style="font-size:32px; font-weight:900; color:{h_c}; font-family:'Orbitron'; text-shadow:0 0 15px {h_c}; margin:20px 0;">{daily_hex['name']}</div>
                <div style="background:rgba(0,0,0,0.6); padding:15px; text-align:left; border:1px solid #333; font-size:14px; color:#ddd;">
                    <b style="color:{h_c};">> SYS_LOG:</b><br>{daily_hex['desc']}
                </div>
            </div>
            """)

        with c_o2:
            render_html("<div class='mod-header'><span class='tag'>02</span>ARCHETYPE (核心架构)</div>")
            render_html(f"""
            <div class="cyber-panel" style="padding: 25px; border-left-color: {dm.get('color', '#fff')};">
                <div style="font-size:28px; font-weight:900; color:{dm.get('color', '#fff')}; text-shadow:0 0 20px {dm.get('color', '#fff')}; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <span>{d['day_master']} · {dm.get('class', 'UNK').split('/')[0]}</span>
                    <span style="border:2px solid {dm.get('color', '#fff')}; color:#fff; padding:4px 12px; font-size: 14px; font-family:'Orbitron';">{dm.get('mbti', 'UNK')}</span>
                </div>
                <div style="color:#d4d4d4; font-size:14px; line-height:1.8; margin-bottom:20px;">{dm.get('desc', '')}</div>
                <div style="background:rgba(0,0,0,0.6); padding:10px; border:1px solid #333; font-family:'Fira Code'; font-size:12px;">
                    <span style="color:#888;">> 致命系统漏洞：</span><b style="color:var(--secondary);">{dm.get('flaw', '无')}</b>
                </div>
            </div>
            """)

    with t_core:
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            render_html("<div class='mod-header'><span class='tag'>03</span>PAYLOAD (算力六边形)</div>")
            rpg_l = ["STR(金)", "AGI(木)", "INT(水)", "CHA(火)", "CON(土)"]
            wx_v = [d['wx']['金'], d['wx']['木'], d['wx']['水'], d['wx']['火'], d['wx']['土']]
            fig1 = go.Figure(data=go.Scatterpolar(r=wx_v+[wx_v[0]], theta=rpg_l+[rpg_l[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color=THEME["primary"], width=2), marker=dict(color='#fff', size=6)))
            fig1.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, max(max(wx_v)+10, 40)]), angularaxis=dict(tickfont=dict(color='#fff', size=12), gridcolor='rgba(255,255,255,0.1)')), paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=10, b=10, l=30, r=30))
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        with c2:
            render_html("<div class='mod-header'><span class='tag'>04</span>LORE (前世与进程)</div>")
            render_html(f"""
            <div class="cyber-panel" style="padding:20px; background:rgba(255,255,255,0.02);">
                <div style="font-size:11px; color:var(--secondary); font-family:'Orbitron'; margin-bottom:10px;">>> KARMIC DEBT</div>
                <div style="font-size:16px; font-weight:bold; color:#fff; margin-bottom:8px;">{d['past_life']['title']}</div>
                <div style="color:#aaa; font-size:13px; line-height:1.6;">> 债务: {d['past_life']['debt']}</div>
            </div>
            """)
            d_html = "".join([f"<div style='background:rgba(255,255,255,0.05); border-left:3px solid var(--primary); padding:10px; margin-bottom:8px; color:#fff; font-family:\"Fira Code\"; font-size:13px;'>🔮 {daemon}</div>" for daemon in d['daemons']])
            render_html(f"<div style='margin-top:15px;'>{d_html}</div>")

    with t_metrics:
        render_html("<div class='mod-header'><span class='tag'>05</span>ALPHA TREND (10年气运)</div>")
        f_10y = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color=THEME["primary"], width=3, shape='spline'), fill='tozeroy', fillcolor=f'rgba(255, 0, 60, 0.15)' if IS_CANARY else 'rgba(0, 243, 255, 0.15)', marker=dict(size=8, color="#fff")))
        f_10y.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=10, b=20, l=10, r=10), xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code')), yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code')))
        st.plotly_chart(f_10y, use_container_width=True, config={'displayModeBar': False})

    # =========================================================================
    # ⌨️ [ TERMINAL ] 命令行与系统底部
    # =========================================================================
    st.markdown("---")
    render_html(f"<div style='font-family:Orbitron; color:var(--primary); font-size:14px; margin-bottom:10px; margin-top:20px;'>ROOT@NODE_{st.session_state.cohort}:~#</div>")
    
    cmd = st.chat_input("输入终端命令 (如: /help, /node)...")
    if cmd:
        cmd = cmd.strip().lower()
        st.session_state.term_logs.append(f"<span style='color:#fff;'>> {cmd}</span>")
        if cmd == '/help': st.session_state.term_logs.append("[SYS] AVAILABLE CMDS: /node, /clear, /matrix")
        elif cmd == '/node': st.session_state.term_logs.append(f"<span style='color:var(--primary);'>[INFO] YOU ARE CURRENTLY ON NODE: {st.session_state.cohort}.</span>")
        elif cmd == '/matrix': st.session_state.term_logs.append(f"<span style='color:var(--secondary);'>[MSG] WAKE UP, NEO. THE MATRIX HAS YOU.</span>")
        elif cmd == '/clear': st.session_state.term_logs = ["> TERMINAL CLEARED."]
        else: st.session_state.term_logs.append(f"<span style='color:#ff0055;'>[ERR] UNKNOWN COMMAND: {cmd}</span>")

    log_html = "<br>".join(st.session_state.term_logs[-5:])
    render_html(f"<div style=\"background:rgba(0,0,0,0.85); border:1px solid var(--primary); border-left:4px solid var(--primary); padding:15px; border-radius:2px; font-family:'Fira Code'; color:var(--primary); font-size:13px; height:150px; display:flex; flex-direction:column-reverse; overflow:hidden; margin-bottom:40px;\"><div>{log_html}<span style='animation:blink 1s infinite;'>_</span></div></div>")

    col_b_l, col_b_m, col_b_r = st.columns([1,2,1])
    with col_b_m:
        if st.button("🔌 物理拔除神经链接 (REBOOT)", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # 页脚自带 A/B 测试遥测反馈
    render_html(f"""
    <div style='text-align:center; color:#555; font-size:12px; margin-top:60px; font-family:Orbitron; padding-bottom: 20px; border-top: 1px dashed #222; padding-top: 20px;'>
        <b style="color:var(--primary);">[ A/B TESTING TELEMETRY: COHORT_{st.session_state.cohort} ACTIVE ]</b><br>
        © 2026 {COPYRIGHT}. {THEME['version']}.
    </div>
    """)
