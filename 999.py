import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math
import hashlib
import json
from datetime import datetime, time as dt_time

# ==============================================================================
# 🛡️ [ KERNEL 00 ] 物理级防爆装甲 (ZERO-BUG)
# ==============================================================================
try:
    import numpy as np
    import plotly.graph_objects as go
    from lunar_python import Solar
except ImportError as e:
    st.set_page_config(page_title="SYS.PANIC", page_icon="🚨", layout="centered")
    st.error(f"🚨 **FATAL ERROR: 缺少核心算力模块 `{e.name}`**\n\n请在同级目录创建 requirements.txt 并添加：\nstreamlit\nlunar-python\nplotly\nnumpy\n\n然后重启服务器。")
    st.stop()

# ==============================================================================
# 🌌 [ GLOBALS ] 宇宙物理引擎变量与安全状态机
# ==============================================================================
VERSION = "KARMA-OS V16.0 [THE GOD MATRIX]"
COPYRIGHT = "NIGHT CITY DAO"
SYS_NAME = "量子命理 | 赛博神谕终端"

st.set_page_config(page_title=SYS_NAME, page_icon="🧿", layout="wide", initial_sidebar_state="collapsed")

if 'booted' not in st.session_state:
    st.session_state.booted = False
    st.session_state.data = {}
    st.session_state.anim_played = False
    st.session_state.term_logs = ["> SYS_KERNEL READY. AWAITING COMMAND..."]

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in html_str.split('\n')]), unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ CSS ENGINE ] 静态层隔离注入 (彻底斩断 KeyError 的根源)
# ==============================================================================
STATIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root { --primary: #00f3ff; --pink: #f43f5e; --yellow: #fcee0a; --green: #10b981; --purple: #a855f7; }
html, body, .stApp { background-color: #020408 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; }
[data-testid="stHeader"], footer { display: none !important; }
::-webkit-scrollbar { width: 6px; background: #000; }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; box-shadow: 0 0 10px var(--primary); }
.block-container { max-width: 1200px !important; padding-top: 3.5rem !important; padding-bottom: 5rem !important; overflow-x: hidden; }

/* 视差背景网格与 CRT */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px); background-size: 100% 3px, 40px 40px; z-index: -1; pointer-events: none; }
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 30%, transparent 20%, rgba(2, 4, 8, 0.95) 100%); z-index: -2; pointer-events: none; }

/* [功能回归] 全息跑马灯 */
.ticker-wrap { width: 100vw; overflow: hidden; height: 35px; background: rgba(2, 4, 8, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 20px rgba(0,243,255,0.15); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 35s linear infinite; font-family: 'Orbitron', monospace; font-size: 13px; color: var(--primary); line-height: 35px; letter-spacing: 2px; }
.ticker span { margin-right: 50px; } .ticker .up { color: var(--green); text-shadow: 0 0 8px rgba(16,185,129,0.8); } .ticker .down { color: var(--pink); text-shadow: 0 0 8px rgba(244,63,94,0.8); }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* 毁灭级标题 */
.hero-title { font-size: clamp(32px, 6vw, 55px) !important; font-family: 'Orbitron', sans-serif; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 6px; margin-bottom: 5px; margin-top: 15px; text-shadow: 0 0 20px rgba(0,243,255,0.7); position: relative; display: inline-block; text-transform: uppercase; }
.hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.8; pointer-events:none;}
.hero-title::before { left: 3px; text-shadow: -2px 0 var(--pink); animation: glitch-1 2.5s infinite linear alternate-reverse; }
.hero-title::after { left: -3px; text-shadow: 2px 0 var(--primary); animation: glitch-2 3.5s infinite linear alternate-reverse; }
@keyframes glitch-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
@keyframes glitch-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }

/* 玻璃拟态大卡 */
.glass-card { background: rgba(5, 8, 14, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0,243,255,0.2); box-shadow: 0 10px 30px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,243,255,0.05); padding: 25px; border-radius: 8px; margin-bottom: 20px; transition: all 0.3s ease;}
.glass-card:hover { border-color: rgba(0,243,255,0.5); transform: translateY(-2px); }
.module-title { color: var(--primary) !important; border-left: 6px solid var(--primary); padding-left: 15px; font-weight: 900; margin-top: 40px; margin-bottom: 25px; letter-spacing: 2px; font-family: 'Orbitron', 'Noto Sans SC', sans-serif; font-size: 22px; text-shadow: 0 0 15px rgba(0,243,255,0.5); background: linear-gradient(90deg, rgba(0,243,255,0.15), transparent); padding-top: 8px; padding-bottom: 8px; border-radius: 4px; text-transform: uppercase;}

/* 原生表单组件深度劫持 */
div[data-testid="stForm"] { border: none !important; background: transparent !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--primary) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(0,243,255,0.4) !important; border-radius: 4px !important; text-align: center; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; transition: all 0.3s; }
div[data-testid="stTextInput"] input:focus { border-color: var(--purple) !important; box-shadow: 0 0 20px rgba(168,85,247,0.4), inset 0 0 10px rgba(168,85,247,0.2) !important; transform: scale(1.02); }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(0,243,255,0.4) !important; color: var(--primary) !important; border-radius: 4px !important; height: 55px; }

/* 交互按钮 */
div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9) 0%, rgba(15,15,20,0.9) 100%) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-left: 4px solid var(--primary) !important; border-radius: 4px !important; min-height: 60px !important; width: 100% !important; transition: all 0.3s ease !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
div.stButton > button p { color: #ffffff !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.3) !important; transform: translateY(-2px); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #a855f7) !important; border: none !important; box-shadow: 0 0 20px rgba(255,0,124,0.5) !important;}
div.stButton > button[data-testid="baseButton-primary"] p { font-size: 18px !important; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
div.stButton > button[data-testid="baseButton-primary"]:hover { filter: brightness(1.2); box-shadow: 0 0 40px rgba(255,0,124,0.8) !important; transform: scale(1.02); }

/* Tabs 极客导航坞 & 代码块 */
[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Orbitron', 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 15px !important; padding-bottom: 12px !important; transition: all 0.3s ease; border-bottom: 2px solid transparent !important;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; border-bottom-width: 3px !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); background: linear-gradient(0deg, rgba(0,243,255,0.1) 0%, transparent 100%); }
div[data-testid="stCodeBlock"] > div { background-color: #030305 !important; border: 1px solid #333 !important; border-left: 4px solid var(--green) !important; }
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code { font-family: 'Fira Code', monospace !important; color: var(--green) !important; }
div[data-testid="stDownloadButton"] > button { border: 1px dashed var(--purple) !important; border-left: 4px solid var(--purple) !important; height: 55px; }

/* [功能回归] 结算纯代码烟花 */
.firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', monospace; color: var(--primary); text-shadow: 0 0 20px var(--primary), 0 0 30px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;}
@keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }
div[data-testid="stChatInput"] { background: rgba(0,0,0,0.95) !important; border: 1px solid #00f3ff !important; border-radius: 0 !important; box-shadow: 0 0 20px rgba(0,243,255,0.2) !important;}
div[data-testid="stChatInput"] textarea { color: #00f3ff !important; font-family: 'Fira Code' !important; font-weight: bold; }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }
</style>
"""
st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ==============================================================================
# 🗃️ [ MEGA DICTIONARY ] 八字源码映射库 (✅ 初版全部硬核字段 100% 满血复原)
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {
        "role": "Root Node / 架构巨树", "mbti": "ENTJ", "color": "#10b981", "element": "木", "tier": "UR",
        "desc": "天生具备宏大的底层系统构建能力，性格直爽极度抗压。能扛起从0到1重构秩序的开拓者。", 
        "evolution_path": ["L1 架构幼苗", "L2 核心骨干", "L3 苍天建木"], "ultimate_evolution": "【苍天建木】执掌三界底层协议", 
        "black_swan": "过于刚硬，遇强则折。遭遇系统级降维打击容易因宁折不弯导致全面宕机。", "patch": "引入「水」属性柔性冗余，挂起进程等待重启。", 
        "weapon": "高分子动能巨斧", "implant": "钛合金强固脊椎"
    },
    "乙": {
        "role": "P2P Crawler / 量子藤蔓", "mbti": "ENFP", "color": "#34d399", "element": "木", "tier": "SSR",
        "desc": "拥有敏锐嗅觉与恐怖适应力。能在资源枯竭的夹缝中疯狂生长，天生暗网渗透专家。", 
        "evolution_path": ["L1 寄生节点", "L2 渗透猎手", "L3 噬星魔藤"], "ultimate_evolution": "【噬星魔藤】寄生控制全网资源的暗影君王", 
        "black_swan": "极度依赖宿主，核心断网易失去独立运行能力。", "patch": "建立分布式多宿主挂载协议，分散全网风险。", 
        "weapon": "量子绞杀魔藤", "implant": "突触拓展插槽"
    },
    "丙": {
        "role": "Overclock GPU / 核聚耀阳", "mbti": "ESTP", "color": "#f43f5e", "element": "火", "tier": "UR",
        "desc": "充满爆裂输出的核聚变爆发力，只要在线，就是全队输出最高绝对算力的发光核心。", 
        "evolution_path": ["L1 点火程序", "L2 核聚变堆", "L3 恒星引擎"], "ultimate_evolution": "【恒星引擎】照亮并驱动整个纪元", 
        "black_swan": "全功率输出易导致内核熔毁，光芒太盛极易引来集中黑客攻击。", "patch": "强制加装「土」属性散热栅栏，波谷期进入低功耗待机。", 
        "weapon": "等离子破城炮", "implant": "微型核聚变胸腔"
    },
    "丁": {
        "role": "Optical Fiber / 幽网信标", "mbti": "INFJ", "color": "#fb923c", "element": "火", "tier": "SSR",
        "desc": "洞察人心的夜行者，思维细腻。擅长在最灰暗地带为团队提供精准情绪价值与破局方向。", 
        "evolution_path": ["L1 寻路信标", "L2 精神图腾", "L3 灵魂织网者"], "ultimate_evolution": "【灵魂织网者】操控全网心智的网络幽灵", 
        "black_swan": "能量波动极不稳定，在市场大洗牌风暴中容易断网。", "patch": "寻找强大的甲木巨树作为遮风挡雨的物理防御壁。", 
        "weapon": "高聚能激光短刃", "implant": "脑机共情模块"
    },
    "戊": {
        "role": "Hard Firewall / 绝对防线", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "tier": "UR",
        "desc": "稳如泰山，拥有物理级断网防御力。极其靠谱的信用节点，最坚不可摧的安全底线。", 
        "evolution_path": ["L1 承载沙盒", "L2 巨石阵列", "L3 盖亚装甲"], "ultimate_evolution": "【盖亚装甲】承载万物因果的绝对壁垒", 
        "black_swan": "系统庞大笨重，面临敏捷突发迭代时极易卡死在旧循环中。", "patch": "主动清理内存缓存，接纳木属性破坏性创新打破死锁。", 
        "weapon": "绝对零度力场盾", "implant": "全覆式碳纤维装甲"
    },
    "己": {
        "role": "Cloud Matrix / 息壤母体", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "tier": "SSR",
        "desc": "海纳百川的包容力，无缝整合一切碎片。将天马行空的狂想转化为具体落地的执行中枢。", 
        "evolution_path": ["L1 容错冗余", "L2 资源枢纽", "L3 创世息壤"], "ultimate_evolution": "【创世息壤】孕育下一个数字生态的温床", 
        "black_swan": "无差别接收并发请求，导致系统被垃圾填满超载崩溃。", "patch": "编写无情的垃圾回收(GC)脚本，拒绝无效并发请求。", 
        "weapon": "引力塌缩发生器", "implant": "海量冗余储存池"
    },
    "庚": {
        "role": "Exec Thread / 裁决执行官", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "tier": "UR",
        "desc": "杀伐果断，对低效与冗余代码零容忍。无情推进进度、斩断一切无效羁绊的风控大闸。", 
        "evolution_path": ["L1 肃清脚本", "L2 风控铁腕", "L3 审判之剑"], "ultimate_evolution": "【审判之剑】斩断一切因果循环的终极裁决", 
        "black_swan": "戾气过重，易引发不可逆的物理级破坏，导致业务链彻底断裂。", "patch": "必须经受火属性的高温熔炼，将狂暴杀气转化为极致利刃。", 
        "weapon": "高频振荡斩舰刀", "implant": "肌肉纤维强化束"
    },
    "辛": {
        "role": "Quantum Chip / 纳米精工", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "tier": "SSR",
        "desc": "永远追求完美极客。自带极高审美，能在粗糙草台中打磨出顶尖跨时代产品的核心枢纽。", 
        "evolution_path": ["L1 精密协议", "L2 审美巅峰", "L3 量子纠缠体"], "ultimate_evolution": "【量子纠缠体】超越物质形态的究极艺术代码", 
        "black_swan": "极度脆弱傲娇。环境稍微不达标或遇粗暴行径即当场罢工。", "patch": "需要极度纯净的水属性淘洗保护，绝不卷入底层肮脏博弈。", 
        "weapon": "纠缠态纳米手术刀", "implant": "微观增强义眼"
    },
    "壬": {
        "role": "Data Flood / 深网狂潮", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "tier": "UR",
        "desc": "思维开阔奔放，厌恶陈规。能在瞬息万变的市场中，凭借直觉掀起降维打击的颠覆浪潮。", 
        "evolution_path": ["L1 数据暗流", "L2 倾覆巨浪", "L3 渊海归墟"], "ultimate_evolution": "【渊海归墟】吞噬所有时间与空间的终极黑洞", 
        "black_swan": "过度放纵算力如同脱缰野马，容易引发洪水滔天反噬根基。", "patch": "引入严苛的戊土级风控大坝，强行设定安全红线。", 
        "weapon": "液态金属形变甲", "implant": "抗压液冷循环管"
    },
    "癸": {
        "role": "Ghost Backdoor / 幽灵谋略家", "mbti": "INTJ", "color": "#b026ff", "element": "水", "tier": "SSR",
        "desc": "聪慧隐秘，习惯幕后推演全局。擅长通过博弈和信息差，兵不血刃地窃取最终权限。", 
        "evolution_path": ["L1 隐形爬虫", "L2 渗透迷雾", "L3 命运主宰"], "ultimate_evolution": "【命运主宰】在第四维度拨动因果的神明", 
        "black_swan": "心思过重，常陷入死循环逻辑死局，算计太多错失直白红利。", "patch": "走向阳光接受丙火照射，用阳谋击碎一切阴谋。", 
        "weapon": "认知劫持神经毒素", "implant": "光学迷彩潜行皮肤"
    }
}

SHEN_SKILLS = {"七杀": "零日漏洞爆破 [Lv.Max]", "正官": "底层协议锚定 [Lv.Max]", "偏印": "逆向工程解构 [Lv.Max]", "正印": "系统灾备兜底 [Lv.Max]", "偏财": "高频杠杆套利 [Lv.Max]", "正财": "算力资产吞噬 [Lv.Max]", "比肩": "分布式共识网 [Lv.Max]", "劫财": "网络节点劫持 [Lv.Max]", "食神": "感官体验降维 [Lv.Max]", "伤官": "范式秩序破坏 [Lv.Max]"}

CYBER_HEXAGRAMS = [
    {"name": "乾为天 [SYS_ROOT]", "desc": "获取系统最高物理权限，全网算力为你让路。潜龙升天，万物皆可并发。", "color": "#10b981"},
    {"name": "坤为地 [SAFE_MODE]", "desc": "进入深度防御与物理冷备份阶段，切断所有外部高危握手协议。厚德载物。", "color": "#fcee0a"},
    {"name": "地天泰 [SYNC_100%]", "desc": "天地交泰，内外网 API 完美握手。你处于系统生命周期的黄金波段。", "color": "#00f3ff"},
    {"name": "天地否 [DDOS_WARN]", "desc": "遭遇全网降维打击与大雪崩，主链失去共识。此节点极其凶险，忌强行裸奔。", "color": "#f43f5e"},
    {"name": "水雷屯 [BOOT_LOOP]", "desc": "系统初始化遭遇未知依赖冲突，面临艰难的启动阻力。万事开头难，需耐心排错。", "color": "#a855f7"}
]

# ==============================================================================
# 🧠 [ CORE ALGORITHMS ] 量子核心算法库
# ==============================================================================
def trigger_supernova():
    h_str = ""
    vocab = ["KARMA", "DAO", "HASH", "DESTINY", "SYNC", "OS", "ROOT", "MINT"]
    for _ in range(40):
        tx = random.uniform(200, 800) * math.cos(random.uniform(0, 2*math.pi))
        ty = random.uniform(200, 800) * math.sin(random.uniform(0, 2*math.pi))
        h_str += '<div class="firework-center" style="--tx:' + str(tx) + 'px; --ty:' + str(ty) + 'px; --s:' + str(random.uniform(1.0, 3.5)) + '; --rot:' + str(random.randint(-360, 360)) + 'deg; animation-delay:' + str(random.uniform(0, 0.2)) + 's; font-size:' + str(random.randint(14, 24)) + 'px;">' + random.choice(vocab) + '</div>'
    render_html(h_str)

def get_daily_oracle(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_seed = int(hashlib.md5((user_hash + today_str).encode()).hexdigest()[:8], 16)
    return random.Random(daily_seed).choice(CYBER_HEXAGRAMS)

@st.cache_data
def generate_alpha_curve(seed_hash):
    rng = np.random.RandomState(int(seed_hash[:8], 16))
    yrs = [str(datetime.now().year + i) for i in range(10)]
    roi = [rng.randint(60, 85)]
    for _ in range(9): roi.append(max(30, min(100, roi[-1] + rng.randint(-20, 25))))
    return yrs, roi

def calculate_synergy(my_hash, partner_stem):
    rng_syn = np.random.RandomState(int(my_hash[:6], 16) + sum(ord(c) for c in partner_stem))
    score = rng_syn.randint(65, 99)
    if score >= 90: return score, "【黄金并网】底层协议 100% 兼容，最强双核推土机！", "#10b981"
    elif score >= 75: return score, "【灰度容错】代码互补，能打磨出极具弹性的闭环。", "#fcee0a"
    else: return score, "【DDoS 互斥】底层逻辑相冲！建议物理隔离！", "#f43f5e"

# ==============================================================================
# 🔮 [ ENTRY POINT ] 状态机与生辰降临采集
# ==============================================================================
if not st.session_state.booted:
    # 跑马灯
    render_html("""<div class="ticker-wrap"><div class="ticker">
        <span>KARMA-OS: V16.0 SECURE <b class="up">▲ONLINE</b></span>
        <span>SOUL-NODE: FATE MAPPED <b class="up">▲LOCKED</b></span>
        <span>BAZI-HASH: DECRYPT SUCCESS <b class="up">▲14.2TH/s</b></span>
        <span>SYS-RISK: FIVE ELEMENTS BALANCED <b class="up">▲SECURE</b></span>
        <span>MARKET-ALPHA: 10-YEAR TREND <b class="down">▼COMPUTING</b></span>
        <span>DAO-PROTOCOL: SMART CONTRACT <b class="up">▲MINTED</b></span>
    </div></div>""")

    render_html("""
    <div style="text-align: center; margin-bottom: 30px; margin-top:20px;">
        <div style="color:var(--neon-cyan); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">KARMA OS FRAMEWORK</div>
        <h1 class="hero-title" data-text="全息命盘推演终端">全息命盘推演终端</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:8px; margin-top:10px;">DESTINY ENGINE V16.0 MAX</div>
    </div>
    <div class="glass-card" style="max-width: 650px; margin: 0 auto;">
        <div style="font-family:'Fira Code'; color:var(--neon-cyan); margin-bottom:15px; font-weight:bold;">> INITIALIZING QUANTUM LUNAR KERNEL...</div>
        <div style="margin-bottom:5px; font-family:'Fira Code'; font-size:13px; color:#aaa;"><span style="color:var(--green);">[OK]</span> Mounting Lunar-Python astronomical algorithms.</div>
        <div style="margin-bottom:5px; font-family:'Fira Code'; font-size:13px; color:#aaa;"><span style="color:var(--green);">[OK]</span> Bypassing temporal distortion logic.</div>
        <br><span style="color:#ffffff; font-size: 15px; line-height: 1.8;"><b>肉体不过是碳基的载体，八字才是灵魂的底层代码。</b><br><br>在硅基宇宙与玄学法则交汇的当下，本终端将提取您的先天降临坐标。为您生成不可篡改的高阶本命元神凭证与气运大盘。</span>
    </div>
    """)
    
    with st.form(key="destiny_form", border=False):
        render_html("<div style='color:var(--neon-cyan); font-family:\"Orbitron\"; font-size:13px; font-weight:bold; margin-bottom:15px; text-align:center;'>▼ 注入先天元神降临坐标 ▼</div>")
        col1, col2 = st.columns(2)
        with col1:
            uname = st.text_input("赛博代号 [HANDLE]", placeholder="例如：Neo / 银手", max_chars=16)
            bdate = st.date_input("降临历法 [COMPILE_DATE]", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(1999, 9, 9))
        with col2:
            ugender = st.selectbox("载体形态 [CHASSIS]", ["乾造 (男)", "坤造 (女)"])
            btime = st.time_input("降临时辰 [BOOT_TIME]", value=dt_time(12, 00))
        
        render_html("<br>")
        submit_btn = st.form_submit_button("▶ UPLINK TO THE MATRIX (连接宇宙推演天机)", type="primary", use_container_width=True)

        if submit_btn:
            uname = uname.strip() if uname else "Anonymous_Node"
            solar = Solar.fromYmdHms(bdate.year, bdate.month, bdate.day, btime.hour, btime.minute, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            wx_str = bazi.getYearWuXing() + bazi.getMonthWuXing() + bazi.getDayWuXing() + bazi.getTimeWuXing()
            wx_counts = {'金':0, '木':0, '水':0, '火':0, '土':0}
            for char in wx_str: 
                if char in wx_counts: wx_counts[char] += 1
            tot = sum(wx_counts.values()) or 1
            wx_scores = {k: int((v/tot)*100) for k, v in wx_counts.items()}
            
            skills = []
            for sg in [bazi.getYearShiShenGan(), bazi.getMonthShiShenGan(), bazi.getTimeShiShenGan()]:
                if sg in SHEN_SKILLS and SHEN_SKILLS[sg] not in skills: skills.append(SHEN_SKILLS[sg])
            if not skills: skills = ["混沌未知域 [Lv.Unknown]"]

            hash_id = hashlib.sha256((uname + str(bdate) + str(btime)).encode()).hexdigest().upper()

            st.session_state.data = {
                "name": uname, "gender": ugender.split(" ")[0],
                "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
                "day_master": bazi.getDayGan(),
                "wx": wx_scores, "skills": skills,
                "hash": hash_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            mint_box = st.empty()
            h_logs = ""
            for _ in range(8):
                h_logs = "<span style='color:#94a3b8;'>[ASTRO_SYNC]</span> <span style='color:#00f3ff;'>0x" + hashlib.md5(str(random.random()).encode()).hexdigest()[:24] + "...</span> <span style='color:#10b981;'>[OK]</span><br>" + h_logs
                mint_box.markdown("<div style='max-width: 650px; margin: 0 auto;'><div class='glass-card' style='height:180px; overflow:hidden; font-family:Fira Code; font-size:12px;'>" + h_logs + "</div></div>", unsafe_allow_html=True)
                time.sleep(0.15)
            
            st.session_state.booted = True
            st.rerun()

# ==============================================================================
# 🌟 [ CORE 05 ] 全息大屏展示 (✅ 绝对隔离，采用 get 提取，杜绝 KeyError)
# ==============================================================================
else:
    if not st.session_state.anim_played: 
        trigger_supernova()
        st.session_state.anim_played = True

    d = st.session_state.data
    # 🚨【终极安全设计】: 前置提取所有字典变量，提供默认值。
    dm_key = d.get('day_master', '甲')
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    
    dm_role = dm_info.get("role", "未知节点")
    dm_desc = dm_info.get("desc", "...")
    dm_color = dm_info.get("color", "#00f3ff")
    dm_tier = dm_info.get("tier", "SSR")
    dm_mbti = dm_info.get("mbti", "UNK")
    dm_wpn = dm_info.get("weapon", "通用代码")
    dm_imp = dm_info.get("implant", "通用插槽")
    dm_evo = dm_info.get("evolution_path", ["L1", "L2", "L3"])
    dm_ult = dm_info.get("ultimate_evolution", "觉醒")
    dm_flaw = dm_info.get("black_swan", "无")
    dm_patch = dm_info.get("patch", "保持当前算法")
    
    bz = d.get('bazi_arr', ['??', '??', '??', '??'])
    hash_id = d.get('hash', '0000000000')
    wx_scores = d.get('wx', {'金':20, '木':20, '水':20, '火':20, '土':20})
    
    token_id = int(hash_id[:8], 16)
    contract_addr = "0x" + hashlib.sha256(f"karma_dao_{token_id}".encode()).hexdigest()[:38]
    block_height = f"V16-{(int(time.time()) % 1000000):06d}"
    yrs, trend = generate_alpha_curve(hash_id)

    # 熵增风控计算
    max_wx = max(list(wx_scores.values())) if wx_scores else 0
    entropy_score = int(min(99, (max_wx / 50.0) * 100))
    if entropy_score > 75: 
        e_tag, e_color, r_desc = "极易走火入魔！切忌贪暴！", "var(--pink)", "您的单极属性过载，系统极易崩溃，请立刻停止高风险套利。"
    elif entropy_score > 50: 
        e_tag, e_color, r_desc = "偏科严重，需挂载防御补丁", "var(--yellow)", "底层算力分布不均，容易在特定周期遭遇针对性降维打击。"
    else: 
        e_tag, e_color, r_desc = "五行极度平稳，可抗任意暴击", "var(--green)", "您的系统架构堪称完美，拥有极强的抗打击与自愈恢复能力。"

    # 跑马灯
    render_html("""<div class="ticker-wrap"><div class="ticker">
        <span>KARMA-OS: V16.0 SECURE <b class="up">▲ONLINE</b></span>
        <span>SOUL-NODE: FATE MAPPED <b class="up">▲LOCKED</b></span>
        <span>BAZI-HASH: DECRYPT SUCCESS <b class="up">▲14.2TH/s</b></span>
        <span>SYS-RISK: FIREWALL ACTIVE <b class="up">▲SECURE</b></span>
        <span>DAO-PROTOCOL: SMART CONTRACT <b class="up">▲MINTED</b></span>
    </div></div>""")

    # 💠 模块 I：链上确权
    render_html("<div class='module-title'>💠 模块 I：天机链上确权</div>")
    render_html('<div class="glass-card" style="padding: 15px 25px; margin-bottom: 25px; font-family: \'Orbitron\', monospace; border-top: none; border-left: 4px solid var(--primary);">' +
        '<div style="color: var(--primary); font-size: 15px; font-weight: bold; border-bottom: 1px dashed var(--primary); padding-bottom: 10px; margin-bottom: 12px; display:flex; align-items:center;">' +
            '<span style="font-size:22px; margin-right:10px;">🏅</span> <span>DESTINY SOULBOUND TOKEN (SBT) MINTED</span>' +
        '</div>' +
        '<div style="font-size: 13px; color: #94a3b8; line-height: 1.8; display:flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">' +
            '<div><div><span style="color:#e2e8f0;">BLOCK_HEIGHT:</span> ' + block_height + '</div><div><span style="color:#e2e8f0;">CONTRACT:</span> ' + contract_addr[:25] + '...</div></div>' +
            '<div style="text-align: left;"><div><span style="color:#e2e8f0;">TOKEN_ID:</span> #' + str(token_id) + '</div><div><span style="color:#e2e8f0;">TIMESTAMP:</span> ' + d.get('timestamp', '') + '</div></div>' +
        '</div>' +
    '</div>')

    # 🧬 模块 II & III：源码与架构
    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        render_html("<div class='module-title' style='margin-top: 0;'>🧬 模块 II：八字底层源码</div>")
        bz_html = '<div style="display:flex; justify-content:space-between; margin-bottom:25px; text-align:center;">'
        labels = ["[年柱]", "[月柱]", "[日柱(核心)]", "[时柱]"]
        for i in range(4):
            is_core = (i == 2)
            bg = "rgba(0,243,255,0.08)" if is_core else "rgba(0,0,0,0.6)"
            bd = "var(--primary)" if is_core else "#333"
            tc = "var(--primary)" if is_core else "#fff"
            sh = "text-shadow: 0 0 15px var(--primary);" if is_core else ""
            trans = "transform: scale(1.05); box-shadow: 0 0 15px rgba(0,243,255,0.15);" if is_core else ""
            bz_html += '<div style="flex:1; background:' + bg + '; border:1px solid ' + bd + '; padding:15px 0; border-radius:6px; margin: 0 4px; ' + trans + '">' + \
                '<div style="font-size:clamp(26px, 4vw, 40px); font-weight:900; color:' + tc + '; ' + sh + ' line-height:1.1; font-family:\'Noto Sans SC\', serif;">' + bz[i][0] + '<span style="color:#777; font-size:clamp(18px, 3vw, 28px); text-shadow:none;">' + bz[i][1] + '</span></div>' + \
                '<div style="font-size:11px; color:' + bd + '; font-family:\'Orbitron\'; margin-top:8px; font-weight:bold;">' + labels[i] + '</div>' + \
            '</div>'
        bz_html += '</div>'
        render_html(bz_html)

        render_html('<div class="glass-card" style="padding:20px; border-top:none; border-left:4px solid ' + dm_color + '; position:relative;">' +
            '<div style="position: absolute; top: 15px; right: 15px; background: ' + dm_color + '; color: #000; font-family: \'Orbitron\'; font-weight: 900; font-size: 12px; padding: 4px 12px; border-radius: 2px;">' + dm_tier + ' TIER</div>' +
            '<div style="font-size:11px; color:#888; font-family:\'Orbitron\'; margin-bottom:5px;">/// DAY MASTER ///</div>' +
            '<div style="font-size:26px; font-weight:900; color:' + dm_color + '; margin-bottom:10px; text-shadow:0 0 15px ' + dm_color + '88;">' + dm_key + ' · ' + dm_role.split('/')[0] + '</div>' +
            '<div style="font-size:14px; color:#d1d5db; line-height:1.7; margin-bottom:15px;">' + dm_desc + '</div>' +
            '<div style="font-size:12px; font-family:\'Fira Code\'; color:#aaa;"><span style="color:' + dm_color + ';">> Cyber-MBTI：</span>[ ' + dm_mbti + ' ]<br><span style="color:' + dm_color + ';">> 适配专属武装：</span>' + dm_wpn + '<br><span style="color:' + dm_color + ';">> 推荐外挂义体：</span>' + dm_imp + '</div>' +
        '</div>')

    with c2:
        render_html("<div class='module-title' style='margin-top: 0;'>🤝 模块 III：外挂神经插件</div>")
        sk_html = "".join(["<span style='background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.5); border-left:3px solid var(--purple); padding:8px 12px; border-radius:4px; font-size:13px; color:#f3e8ff; font-weight:bold; display:inline-block; margin:4px 4px 8px 0; box-shadow:0 0 10px rgba(168,85,247,0.2);'>" + s + "</span>" for s in d.get('skills', [])])
        render_html('<div class="glass-card" style="padding: 20px; text-align:center; border-top:none; border-left:4px solid var(--purple);">' +
            '<div style="color: var(--purple); font-family: \'Orbitron\'; font-size: 12px; letter-spacing: 2px; margin-bottom: 15px;">[ INNATE SKILL TREE ]</div>' +
            '<div style="line-height: 1.8;">' + sk_html + '</div>' +
        '</div>')
        
        render_html('<div style="background: rgba(255,0,124,0.05); border-left: 4px solid var(--pink); padding: 18px; border-radius: 0 6px 6px 0; margin-top:15px;">' +
            '<div style="font-size:11px; color:var(--pink); font-family:\'Orbitron\'; margin-bottom:8px; letter-spacing:1px; font-weight:bold;">/// DESTINY WARNING ///</div>' +
            '<div style="font-size:13px; color:#94a3b8; margin-bottom:8px;">系统测算五行熵增阀值为：<b style="color:' + e_color + '; font-size:16px;">' + str(entropy_score) + '%</b></div>' +
            '<div style="font-size:14px; color:' + e_color + '; font-weight:bold; margin-bottom:5px;">[ ' + e_tag + ' ]</div>' +
            '<div style="font-size:12px; color:#cbd5e1; line-height:1.6;">' + r_desc + '</div>' +
        '</div>')

    # 🗄️ [ 模块 IV & V ]：极客深潜控制台 (✅ 所有图表、合盘、合约全量回归)
    render_html("<div class='module-title'>🗄️ 模块 IV：极客深潜控制台 (DEEP DIVE)</div>")
    
    t_data, t_syn, t_3d, t_sol = st.tabs(["📊 大盘雷达 (DATA)", "🤝 赛博合盘 (SYNERGY)", "🌌 3D星图 (MAP)", "💻 智能合约 (WEB3)"])

    with t_data:
        c3, c4 = st.columns([1, 1.2], gap="large")
        with c3:
            rpg_l = ["STR(金)", "AGI(木)", "INT(水)", "CHA(火)", "CON(土)"]
            wx_v = [wx_scores.get('金',20), wx_scores.get('木',20), wx_scores.get('水',20), wx_scores.get('火',20), wx_scores.get('土',20)]
            fig1 = go.Figure(data=go.Scatterpolar(r=wx_v+[wx_v[0]], theta=rpg_l+[rpg_l[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color='#00f3ff', width=2), marker=dict(color='#f43f5e', size=6)))
            fig1.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, max(max_wx+10, 40)]), angularaxis=dict(tickfont=dict(color='#fff', size=13), gridcolor='rgba(255,255,255,0.1)')), paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=10, b=10, l=30, r=30))
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            wx_colors = {'金': '#e2e8f0', '木': '#10b981', '水': '#00f3ff', '火': '#f43f5e', '土': '#fcee0a'}
            bars_html = '<div style="background:rgba(0,0,0,0.5); padding:15px; border-radius:4px; border:1px solid rgba(0,243,255,0.2);">'
            for k, v in wx_scores.items():
                c = wx_colors.get(k, '#fff')
                bars_html += '<div style="display:flex; align-items:center; margin-bottom:8px; font-size:12px; font-weight:bold;"><span style="width:25px; color:' + c + ';">' + k + '</span><div style="flex:1; height:6px; background:rgba(255,255,255,0.05); border-radius:2px; margin:0 10px; position:relative;"><div style="position:absolute; top:0; left:0; height:100%; width:' + str(v) + '%; background:' + c + '; border-radius:2px; box-shadow:0 0 8px ' + c + ';"></div></div><span style="width:35px; text-align:right; color:#94a3b8;">' + str(v) + '%</span></div>'
            bars_html += '</div>'
            render_html(bars_html)
        with c4:
            f_10y = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color="#f43f5e", width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)', marker=dict(size=8, color="#00f3ff")))
            f_10y.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=10, b=20, l=10, r=10), xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code')), yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code'), title="Alpha 净值"))
            st.plotly_chart(f_10y, use_container_width=True, config={'displayModeBar': False})
            
            oracle = get_daily_oracle(hash_id)
            render_html('<div style="background:rgba(252,238,10,0.05); border:1px solid ' + oracle['color'] + '; padding:15px; border-left:4px solid ' + oracle['color'] + '; border-radius:2px; margin-top:20px;">' +
                '<div style="font-size:11px; color:' + oracle['color'] + '; font-family:\'Orbitron\'; margin-bottom:8px;">>> DAILY ORACLE (' + datetime.now().strftime('%Y-%m-%d') + ')</div>' +
                '<div style="font-size:18px; font-weight:bold; color:' + oracle['color'] + '; margin-bottom:6px; font-family:\'Orbitron\';">' + oracle['name'] + '</div>' +
                '<div style="color:#aaa; font-size:13px; line-height:1.6;">> ' + oracle['desc'] + '</div>' +
            '</div>')
    
    with t_syn:
        c_s1, c_s2 = st.columns([1.2, 1], gap="large")
        with c_s1:
            render_html("<div style='font-size:13px; color:#aaa; margin-top:15px; margin-bottom:15px;'>输入目标协作节点（合伙人/道侣）的天干，校验系统底层协议的绝对兼容率：</div>")
            opts = list(DAY_MASTER_DICT.keys())
            t_node = st.selectbox("🎯 选择挂载目标节点:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('mbti', 'UNK')}] {x} - {DAY_MASTER_DICT.get(x, {}).get('role', 'UNK').split('/')[0]}")
        with c_s2:
            sc, sd, sc_color = calculate_synergy(hash_id, t_node)
            render_html('<div style="background:rgba(0,0,0,0.6); border:1px solid ' + sc_color + '; border-left:4px solid ' + sc_color + '; padding:25px 20px; border-radius:4px; margin-top:15px; text-align:center; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);">' +
                '<div style="font-family:\'Orbitron\'; font-size:12px; color:#888; letter-spacing:2px; margin-bottom:10px;">SYNERGY MATCH RATE</div>' +
                '<div style="font-family:\'Orbitron\'; font-size:55px; color:' + sc_color + '; font-weight:900; margin-bottom:10px; text-shadow:0 0 20px ' + sc_color + '; line-height:1;">' + str(sc) + '%</div>' +
                '<div style="color:#fff; font-size:14px; font-weight:bold; font-family:\'Noto Sans SC\';">' + sd + '</div>' +
            '</div>')

    with t_3d:
        render_html("<div style='font-size:13px; color:#aaa; text-align:center; margin-top:15px; margin-bottom:10px;'>> 降维映射至三维空间 (支持鼠标 360° 拖拽)。背景点阵为全网众生数据。</div>")
        rng_3d = np.random.RandomState(int(hash_id[:6], 16))
        f3d = go.Figure()
        f3d.add_trace(go.Scatter3d(x=rng_3d.randint(0,100,150), y=rng_3d.randint(0,100,150), z=rng_3d.randint(0,100,150), mode='markers', marker=dict(size=3, color='#334155', opacity=0.5), hoverinfo='none'))
        cx, cy, cz = wx_scores.get('金', 50), wx_scores.get('木', 50), wx_scores.get('水', 50)
        f3d.add_trace(go.Scatter3d(x=[cx], y=[cy], z=[cz], mode='markers+text', text=["ROOT: " + dm_key], textposition="top center", marker=dict(size=15, color=dm_color, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=dm_color, size=16, family="Orbitron", weight="bold")))
        f3d.update_layout(scene=dict(xaxis_title='STR(金)', yaxis_title='AGI(木)', zaxis_title='INT(水)', xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222"), yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222"), zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222")), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=350, showlegend=False)
        st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False})

    with t_sol:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:15px; margin-bottom:10px;'>系统已将您的底层因果律编译为标准的 Solidity ERC-721 智能合约源码。</div>")
        sol_code = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@karma-os/contracts/token/ERC721.sol";

contract Destiny_SBT_V36 is ERC721 {
    // ==========================================
    // > MINT_TARGET : """ + d.get('name', 'GHOST') + """
    // > HASH_ID     : 0x""" + hash_id[:32] + """
    // ==========================================
    
    function overrideAkashic() public {
        uint256 tokenId = uint256(keccak256(abi.encodePacked(\"""" + hash_id + """\")));
        _mint(msg.sender, tokenId);
    }
}"""
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(sol_code, language="solidity")
        st.markdown('</div>', unsafe_allow_html=True)

    # 📥 [ 模块 VI ]：全息资产分发终端 (✅ 纯文本安全替换，杜绝渲染白屏)
    render_html("<div class='module-title'>📥 模块 V：全息资产分发终端</div>")
    t_img, t_txt, t_json, t_asc = st.tabs(["📸 高清海报生成", "📜 万字机密档案 (.TXT)", "💾 极客 JSON 底包", "📟 ASCII 纯文本卡片"])

    with t_img:
        render_html("<div style='text-align:center; color:#888; font-size:12px; margin-top:10px; margin-bottom:15px;'>系统正调用 HTML2Canvas 压制高清全息凭证，<b style='color:var(--primary);'>出现后长按即可保存</b>。</div>")
        
        sk_html_img = "".join(["<span style='background:rgba(0,243,255,0.1); border:1px solid #00f3ff; color:#00f3ff; padding:4px 8px; margin:3px; border-radius:2px; font-size:10px; display:inline-block; font-family:Fira Code;'>" + s.split(' ')[0] + "</span>" for s in d.get('skills', [])[:4]])
        bar_html_img = "".join(["<div style='display:flex; align-items:center; margin-bottom:6px; font-size:11px; color:#ccc;'><span style='width:25px;'>" + k + "</span><div style='flex:1; height:6px; background:#222; margin:0 10px; position:relative;'><div style='position:absolute; left:0; top:0; height:100%; width:" + str(v) + "%; background:" + wx_colors.get(k, '#fff') + "; box-shadow:0 0 8px " + wx_colors.get(k, '#fff') + ";'></div></div><span style='width:30px; text-align:right;'>" + str(v) + "%</span></div>" for k, v in wx_scores.items()])

        # 🚨 [究极防爆策略]: HTML_POSTER_RAW 采用纯字符串 `.replace()`，不再使用 f-string，彻底消灭所有 `{}` 冲突引发的 KeyError！
        HTML_POSTER_RAW = """
        <!DOCTYPE html><html><head><meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700;900&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            body { margin:0; display:flex; justify-content:center; background:transparent; font-family:'Noto Sans SC'; color:#fff; }
            #hide-box { position:absolute; top:-9999px; left:-9999px; }
            #poster { width:340px; background:#010205; border:2px solid #00f3ff; padding:25px 20px; box-sizing:border-box; position:relative; overflow:hidden; border-radius:4px; box-shadow:0 0 30px rgba(0,243,255,0.15);}
            .grid { position:absolute; top:0; left:0; width:100%; height:100%; background:linear-gradient(rgba(0,243,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.05) 1px, transparent 1px); background-size:20px 20px; z-index:0; }
            .content { position:relative; z-index:1; }
            .h1 { font-family:'Orbitron'; font-size:24px; font-weight:900; color:#00f3ff; text-align:center; letter-spacing:2px; margin-bottom:5px; text-shadow:0 0 10px #00f3ff;}
            .h2 { font-size:10px; font-family:'Orbitron'; color:#f43f5e; text-align:center; letter-spacing:4px; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px; font-weight:bold;}
            .bz-row { display:flex; justify-content:space-between; margin-bottom:20px; background:rgba(255,255,255,0.03); padding:10px; border:1px solid #222; border-radius:4px; }
            .bz-c { text-align:center; width:25%; } .bz-t { font-size:22px; font-weight:900; color:#fff; } .bz-b { font-size:9px; color:#888; font-family:'Orbitron'; margin-top:5px; }
            .core-box { background:rgba(0,243,255,0.05); border-left:4px solid #00f3ff; padding:15px; margin-bottom:15px; }
            #ui-loading { color:#00f3ff; font-family:'Orbitron'; padding:40px; text-align:center; animation:blink 1s infinite alternate; font-weight:bold; letter-spacing:2px;}
            @keyframes blink { 0% {opacity:1;} 100% {opacity:0.3;} }
            #final-img { display:none; width:100%; max-width:340px; box-shadow:0 15px 30px rgba(0,0,0,0.8); border: 1px solid rgba(0,243,255,0.5); border-radius:4px; }
        </style></head><body>
        
        <div id="hide-box"><div id="poster">
            <div class="grid"></div><div class="content">
                <div class="h1">KARMA OS_V36</div><div class="h2">DESTINY PROFILE</div>
                <div style="text-align:center; font-size:20px; font-weight:900; margin-bottom:20px; letter-spacing:1px;">[__NAME__] · __GENDER__</div>
                <div class="bz-row">
                    <div class="bz-c"><div class="bz-t">__Y__</div><div class="bz-b">YEAR</div></div>
                    <div class="bz-c"><div class="bz-t">__M__</div><div class="bz-b">MONTH</div></div>
                    <div class="bz-c"><div class="bz-t" style="color:#ff007c; text-shadow:0 0 10px #ff007c;">__D__</div><div class="bz-b" style="color:#ff007c; font-weight:bold;">CORE</div></div>
                    <div class="bz-c"><div class="bz-t">__T__</div><div class="bz-b">TIME</div></div>
                </div>
                <div class="core-box">
                    <div style="font-size:9px; color:#00f3ff; font-family:'Orbitron'; margin-bottom:5px;">> DAY MASTER</div>
                    <div style="font-size:18px; font-weight:900; color:__COLOR__;">__DM_KEY__ · __ROLE__</div>
                    <div style="font-size:11px; margin-top:6px;">MBTI: [ __MBTI__ ]</div>
                </div>
                <div style="text-align:center; margin-bottom:15px;">__SKILLS__</div>
                <div style="background:rgba(0,0,0,0.6); padding:12px; border:1px solid #222;">
                    <div style="font-size:9px; color:#888; font-family:'Orbitron'; margin-bottom:8px; text-align:center;">WUXING LOAD</div>
                    __BARS__
                </div>
                <div style="font-family:'Fira Code'; font-size:8px; color:#666; margin-top:20px; text-align:center; border-top:1px dashed #333; padding-top:10px;">
                    HASH: 0x__HASH__<br>© 2026 __CPY__
                </div>
            </div>
        </div></div>

        <div id="ui-loading">>>> RENDERING HD POSTER...</div>
        <img id="final-img" />
        
        <script>
            setTimeout(() => {
                if(typeof html2canvas !== 'undefined') {
                    html2canvas(document.getElementById('poster'), { scale:2, backgroundColor:'#010205', logging:false }).then(canvas => {
                        document.getElementById('final-img').src = canvas.toDataURL('image/png');
                        document.getElementById('ui-loading').style.display = 'none';
                        document.getElementById('final-img').style.display = 'block';
                    });
                }
            }, 1500);
        </script>
        </body></html>
        """
        
        # 安全替换
        html_ready = HTML_POSTER_RAW.replace("__NAME__", d.get('name', 'GHOST')).replace("__GENDER__", d.get('gender', 'X'))
        html_ready = html_ready.replace("__Y__", bz[0]).replace("__M__", bz[1]).replace("__D__", bz[2]).replace("__T__", bz[3])
        html_ready = html_ready.replace("__COLOR__", dm_color).replace("__DM_KEY__", dm_key).replace("__ROLE__", dm_role.split('/')[0])
        html_ready = html_ready.replace("__MBTI__", dm_mbti).replace("__SKILLS__", sk_html_img).replace("__BARS__", bar_html_img)
        html_ready = html_ready.replace("__HASH__", hash_id[:20]).replace("__CPY__", COPYRIGHT)
        
        components.html(html_ready, height=650)

    with t_txt:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:10px; margin-bottom:15px;'>您专属的万字级【深度机密报告】。一键复制保存本地档案。</div>")
        dossier = """=======================================================
[ KARMA-OS V36.0 ] 量子命盘 · 深度绝密档案 (ALL-FEATURES RESTORED)
=======================================================

>> 1. 节点基础信息 (IDENTITY)
▸ 代号：""" + d.get('name', 'GHOST') + """ (""" + d.get('gender', 'X') + """)
▸ 哈希：0x""" + hash_id + """

>> 2. 底层源代码 (SOURCE CODE)
▸ """ + bz[0] + """ (年/OS) | """ + bz[1] + """ (月/OS) | """ + bz[2] + """ (日/CORE) | """ + bz[3] + """ (时/OS)

>> 3. 核心元神 (DAY MASTER)
▸ 核心：""" + dm_key + """ (""" + dm_info.get('element', '未知') + """属性)
▸ 定位：""" + dm_role + """
▸ MBTI：[ """ + dm_mbti + """ ]
▸ 特质：""" + dm_desc + """
▸ 评级：""" + dm_tier + """
▸ 武器：""" + dm_wpn + """
▸ 义体：""" + dm_imp + """

>> 4. 演化与补丁 (EVOLUTION & PATCH)
▸ 终极化神：""" + dm_ult + """
▸ 演化路径：""" + dm_evo[0] + """ -> """ + dm_evo[1] + """ -> """ + dm_evo[2] + """
▸ 致命漏洞：""" + dm_flaw + """
▸ 系统补丁：""" + dm_patch + """

>> 5. 算力负载分布 (WUXING METRICS)
▸ 金(裁决): """ + str(wx_scores.get('金',0)) + """%  |  木(架构): """ + str(wx_scores.get('木',0)) + """%
▸ 水(流动): """ + str(wx_scores.get('水',0)) + """%  |  火(算力): """ + str(wx_scores.get('火',0)) + """%
▸ 土(承载): """ + str(wx_scores.get('土',0)) + """%

>> 6. 预装外挂神经 (PLUGINS)
▸ """ + ', '.join(d.get('skills', [])) + """

=======================================================
POWERED BY LUNAR DESTINY ENGINE | © """ + COPYRIGHT + """
======================================================="""
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(dossier, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(label="📥 下载深度绝密档案 (.txt)", data=dossier, file_name=f"KARMA_{d.get('name', 'GHOST')}.txt", mime="text/plain", use_container_width=True)

    with t_json:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:10px; margin-bottom:15px;'>极客视角：导出您的先天八字 JSON 结构树底包。</div>")
        export_data = {
            "version": VERSION, "node": d.get('name', 'GHOST'), "bazi": bz,
            "day_master": { "element": dm_key, "role": dm_role, "mbti": dm_mbti, "tier": dm_tier, "evolution": dm_ult, "vulnerability": dm_flaw, "patch": dm_patch, "weapon": dm_wpn },
            "wuxing": wx_scores, "skills": d.get('skills', []), "hash": hash_id
        }
        st.download_button(label="📥 提取原始 JSON 底包", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"DATA_{hash_id[:6]}.json", mime="application/json", use_container_width=True)
        
    with t_asc:
        render_html("<div style='font-size:13px; color:var(--green); margin-top:10px; margin-bottom:10px; font-family:Fira Code;'>> 纯正极客浪漫。一键复制下方代码块发送至微信/Discord，绝不乱码。</div>")
        def m_b(v): return "█" * int(v/100*16) + "░" * (16 - int(v/100*16))
        ascii_res = """```text
========================================================
 ███▄    █  ▓█████  ▒█████     █████▒▄▄▄       ██████ 
 ██ ▀█   █  ▓█   ▀ ▒██▒  ██▒ ▓██   ▒▒████▄   ▒██    ▒ 
▓██  ▀█ ██▒ ▒███   ▒██░  ██▒ ▒████ ░▒██  ▀█▄ ░ ▓██▄   
▓██▒  ▐▌██▒ ▒▓█  ▄ ▒██   ██░ ░▓█▒  ░░██▄▄▄▄██  ▒   ██▒
========================================================
> NODE_HANDLE : """ + d.get('name', 'GHOST') + """ (""" + d.get('gender', 'UNK') + """)
> AKASHIC_ID  : 0x""" + hash_id[:16] + """...
--------------------------------------------------------
[ SOURCE CODE / 灵魂底层源码 ]
  """ + bz[0] + """   |   """ + bz[1] + """   | >> """ + bz[2] + """ << |   """ + bz[3] + """

[ CORE ARCHETYPE / 核心机体架构 ]
> DAY_MASTER  : """ + dm_key + """ (""" + dm_info.get('element', 'UNK') + """ Node)
> ROLE_CLASS  : """ + dm_role.split(' / ')[0] + """
> CYBER_MBTI  : [ """ + dm_mbti + """ ]

[ WUXING PAYLOAD / 算力负载均衡 ]
  STR(金) : """ + f"{wx_scores.get('金',0):02d}" + """% |""" + m_b(wx_scores.get('金',0)) + """|
  AGI(木) : """ + f"{wx_scores.get('木',0):02d}" + """% |""" + m_b(wx_scores.get('木',0)) + """|
  INT(水) : """ + f"{wx_scores.get('水',0):02d}" + """% |""" + m_b(wx_scores.get('水',0)) + """|
  CHA(火) : """ + f"{wx_scores.get('火',0):02d}" + """% |""" + m_b(wx_scores.get('火',0)) + """|
  CON(土) : """ + f"{wx_scores.get('土',0):02d}" + """% |""" + m_b(wx_scores.get('土',0)) + """|
========================================================
```"""
        st.markdown(ascii_res)

    # ⌨️ [ TERMINAL ] 交互终端 (安全拼接)
    st.markdown("---")
    render_html("<div style='font-family:Orbitron; color:var(--primary); font-size:14px; margin-bottom:10px; margin-top:20px;'>ROOT@GOD_MATRIX:~#</div>")
    cmd = st.chat_input("输入命令 (如: /help, /matrix)...")
    if cmd:
        cmd = cmd.strip().lower()
        st.session_state.term_logs.append("<span style='color:#fff;'>> " + cmd + "</span>")
        if cmd == '/help': st.session_state.term_logs.append("[SYS] CMDS: /sudo, /clear, /matrix")
        elif cmd == '/sudo': st.session_state.term_logs.append("<span style='color:var(--pink);'>[ERR] ACCESS DENIED. 凡人无法黑入天命。</span>")
        elif cmd == '/matrix': st.session_state.term_logs.append("<span style='color:var(--green);'>[MSG] WAKE UP, NEO. THE MATRIX HAS YOU.</span>")
        elif cmd == '/clear': st.session_state.term_logs = ["> TERMINAL CLEARED."]
        else: st.session_state.term_logs.append("<span style='color:var(--yellow);'>[ERR] UNKNOWN COMMAND: " + cmd + "</span>")

    log_html = "<br>".join(st.session_state.term_logs[-5:])
    terminal_ui = "<div style='background:rgba(0,0,0,0.85); border:1px solid #00f3ff; border-left:4px solid #00f3ff; padding:15px; border-radius:4px; font-family:\"Fira Code\"; color:#00f3ff; font-size:13px; height:150px; display:flex; flex-direction:column-reverse; overflow:hidden; margin-bottom:40px; box-shadow:inset 0 0 20px rgba(0,243,255,0.1);'><div>" + log_html + "<span style=\"animation:blink 1s infinite;\">_</span></div></div>"
    render_html(terminal_ui)

    # 底部重启按钮
    col_b_l, col_b_m, col_b_r = st.columns([1,2,1])
    with col_b_m:
        if st.button("⏏ 物理拔除网线并重启终端 (SYS_REBOOT)", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================================================================
# 🛑 [ KERNEL 07 ] 赛博呼吸专属版权区
# =========================================================================
render_html('<div style="text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10; border-top: 1px dashed #222; padding-top: 40px;">' +
    '<div style="color:var(--primary); font-family:\'Orbitron\', monospace; font-size:11px; opacity:0.5; letter-spacing:6px; margin-bottom:8px;">POWERED BY LUNAR ENGINE</div>' +
    '<div style="color:var(--primary); font-family:\'Orbitron\', monospace; font-size:11px; opacity:0.3; letter-spacing:3px; margin-bottom:30px;">SYSTEM VERSION: ' + VERSION + '</div>' +
    '<div style="display:inline-block; padding:10px 30px; border-radius:50px; font-size:13px; font-family:\'Orbitron\'; letter-spacing:2px; color:var(--primary); font-weight:bold; background:rgba(0,243,255,0.05); border:1px solid rgba(0,243,255,0.3); box-shadow:0 0 15px rgba(0,243,255,0.1);">© 2026 ' + COPYRIGHT + '</div>' +
'</div>')
