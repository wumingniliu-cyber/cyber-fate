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
# 🌌 [ GLOBALS ] 宇宙物理引擎与安全状态机
# ==============================================================================
VERSION = "KARMA-OS V1.0 [THE TRUE OMEGA]"
COPYRIGHT = "NIGHT CITY DAO"
SYS_NAME = "量子命理 | 赛博神谕终端"

st.set_page_config(page_title=SYS_NAME, page_icon="🧿", layout="wide", initial_sidebar_state="collapsed")

# 🚨 状态机全量初始化 (确保热重载绝不报错)
if "sys_booted" not in st.session_state: st.session_state["sys_booted"] = False
if "sys_data" not in st.session_state: st.session_state["sys_data"] = {}
if "term_logs" not in st.session_state: st.session_state["term_logs"] = ["> SYS_KERNEL READY. AWAITING COMMAND..."]
if "anim_played" not in st.session_state: st.session_state["anim_played"] = False
if "oracle_drawn" not in st.session_state: st.session_state["oracle_drawn"] = False

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in str(html_str).split('\n')]), unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ CSS ENGINE ] 静态层隔离注入
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

/* 🚨 彻底隐藏导致白边的 Streamlit 底部原生悬浮区 */
section[data-testid="stBottom"] { display: none !important; background: transparent !important; }
div[data-testid="stBottomBlockContainer"] { display: none !important; background: transparent !important; }

/* 视差背景网格与 CRT */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px); background-size: 100% 3px, 40px 40px; z-index: -1; pointer-events: none; }
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 30%, transparent 20%, rgba(2, 4, 8, 0.95) 100%); z-index: -2; pointer-events: none; }

/* 全息跑马灯 */
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
.glass-card { background: rgba(5, 8, 14, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(0,243,255,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,243,255,0.05); padding: 25px; border-radius: 8px; margin-bottom: 20px; transition: all 0.4s ease;}
.glass-card:hover { border-color: rgba(0,243,255,0.8); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,1), inset 0 0 30px rgba(0,243,255,0.2); }
.module-title { color: var(--primary) !important; border-left: 6px solid var(--primary); padding-left: 15px; font-weight: 900; margin-top: 40px; margin-bottom: 25px; letter-spacing: 2px; font-family: 'Orbitron', 'Noto Sans SC', sans-serif; font-size: 22px; text-shadow: 0 0 15px rgba(0,243,255,0.5); background: linear-gradient(90deg, rgba(0,243,255,0.15), transparent); padding-top: 8px; padding-bottom: 8px; border-radius: 4px; text-transform: uppercase;}

/* 表单组件劫持 */
div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--primary) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(0,243,255,0.4) !important; border-radius: 4px !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; transition: all 0.3s; text-align: center; }
div[data-testid="stTextInput"] input:focus { border-color: var(--purple) !important; box-shadow: 0 0 20px rgba(168,85,247,0.4), inset 0 0 10px rgba(168,85,247,0.2) !important; transform: scale(1.02); }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(0,243,255,0.4) !important; color: var(--primary) !important; border-radius: 4px !important; height: 55px; }

/* 交互按钮 */
div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9) 0%, rgba(15,15,20,0.9) 100%) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-left: 4px solid var(--primary) !important; border-radius: 4px !important; min-height: 55px !important; width: 100% !important; transition: all 0.3s ease !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
div.stButton > button p { color: #ffffff !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.3) !important; transform: translateY(-2px); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #a855f7) !important; border: none !important; box-shadow: 0 0 20px rgba(255,0,124,0.5) !important;}
div.stButton > button[data-testid="baseButton-primary"] p { font-size: 18px !important; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
div.stButton > button[data-testid="baseButton-primary"]:hover { filter: brightness(1.2); box-shadow: 0 0 40px rgba(255,0,124,0.8) !important; transform: scale(1.02); }

/* Tabs & 代码块 */
[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Orbitron', 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 15px !important; padding-bottom: 12px !important; transition: all 0.3s ease; border-bottom: 2px solid transparent !important;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; border-bottom-width: 3px !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); background: linear-gradient(0deg, rgba(0,243,255,0.1) 0%, transparent 100%); }
div[data-testid="stCodeBlock"] > div { background-color: #030305 !important; border: 1px solid #333 !important; border-left: 4px solid var(--green) !important; }
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code { font-family: 'Fira Code', monospace !important; color: var(--green) !important; line-height:1.6 !important;}
div[data-testid="stDownloadButton"] > button { border: 1px dashed var(--purple) !important; border-left: 4px solid var(--purple) !important; height: 55px; }

/* 赛博阴阳爻 UI */
.hex-container { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; margin: 20px 0; }
.yao-yang { width: 100%; max-width: 140px; height: 12px; border-radius: 2px; }
.yao-yin { width: 100%; max-width: 140px; height: 12px; display: flex; justify-content: space-between; gap: 15px; }
.yao-yin .half { flex: 1; border-radius: 2px; }

/* 🚨 极其安全的量子坍缩动画 (彻底抛弃导致白屏的 blur 属性) */
@keyframes quantum-collapse {
    0% { transform: scale(0.85) translateY(20px); opacity: 0; }
    50% { transform: scale(1.02); opacity: 0.8; }
    100% { transform: scale(1) translateY(0); opacity: 1; }
}
.quantum-reveal { animation: quantum-collapse 0.8s cubic-bezier(0.19, 1, 0.22, 1) forwards; }

/* 结算烟花 */
.firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', monospace; color: var(--primary); text-shadow: 0 0 20px var(--primary), 0 0 30px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;}
@keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }
</style>
"""
st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ==============================================================================
# 🗃️ [ MEGA DICTIONARY ] 八字源码映射库 & LORE 满血归位
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"role": "Root Node / 架构巨树", "mbti": "ENTJ", "color": "#10b981", "element": "木", "tier": "UR", "desc": "具备宏大的底层构建能力，性格直爽抗压。能扛起从0到1重构秩序的开拓者。", "evolution_path": ["L1 架构幼苗", "L2 核心骨干", "L3 苍天建木"], "ultimate_evolution": "【苍天建木】执掌三界底层协议", "black_swan": "过于刚硬，遇强则折。遭遇系统级降维打击容易因宁折不弯导致全面宕机。", "patch": "引入「水」属性柔性冗余，挂起进程等待重启。", "weapon": "高分子动能巨斧", "implant": "钛合金强固脊椎"},
    "乙": {"role": "P2P Crawler / 量子藤蔓", "mbti": "ENFP", "color": "#34d399", "element": "木", "tier": "SSR", "desc": "敏锐嗅觉与恐怖适应力。能在资源枯竭的夹缝中疯狂生长，天生暗网渗透专家。", "evolution_path": ["L1 寄生节点", "L2 渗透猎手", "L3 噬星魔藤"], "ultimate_evolution": "【噬星魔藤】寄生控制全网资源的暗影君王", "black_swan": "极度依赖宿主，核心断网易失去独立运行能力。", "patch": "建立分布式多宿主挂载协议，分散全网风险。", "weapon": "量子绞杀魔藤", "implant": "突触拓展插槽"},
    "丙": {"role": "Overclock GPU / 核聚耀阳", "mbti": "ESTP", "color": "#f43f5e", "element": "火", "tier": "UR", "desc": "充满爆裂输出的核聚变爆发力，只要在线，就是全队输出最高绝对算力的发光核心。", "evolution_path": ["L1 点火程序", "L2 核聚变堆", "L3 恒星引擎"], "ultimate_evolution": "【恒星引擎】照亮并驱动整个纪元", "black_swan": "全功率输出易导致内核熔毁，光芒太盛极易引来集中黑客攻击。", "patch": "强制加装「土」属性散热栅栏，波谷期进入低功耗待机。", "weapon": "等离子破城炮", "implant": "微型核聚变胸腔"},
    "丁": {"role": "Optical Fiber / 幽网信标", "mbti": "INFJ", "color": "#fb923c", "element": "火", "tier": "SSR", "desc": "洞察人心的夜行者，思维细腻。擅长在最灰暗地带为团队提供精准情绪价值与破局方向。", "evolution_path": ["L1 寻路信标", "L2 精神图腾", "L3 灵魂织网者"], "ultimate_evolution": "【灵魂织网者】操控全网心智的网络幽灵", "black_swan": "能量波动极不稳定，在市场大洗牌风暴中容易断网。", "patch": "寻找强大的甲木巨树作为遮风挡雨的物理防御壁。", "weapon": "高聚能激光短刃", "implant": "脑机共情模块"},
    "戊": {"role": "Hard Firewall / 绝对防线", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "tier": "UR", "desc": "稳如泰山，拥有物理级断网防御力。极其靠谱的信用节点，最坚不可摧的安全底线。", "evolution_path": ["L1 承载沙盒", "L2 巨石阵列", "L3 盖亚装甲"], "ultimate_evolution": "【盖亚装甲】承载万物因果的绝对壁垒", "black_swan": "系统庞大笨重，面临敏捷突发迭代时极易卡死在旧循环中。", "patch": "主动清理内存缓存，接纳木属性破坏性创新打破死锁。", "weapon": "绝对零度力场盾", "implant": "全覆式碳纤维装甲"},
    "己": {"role": "Cloud Matrix / 息壤母体", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "tier": "SSR", "desc": "海纳百川的包容力，无缝整合一切碎片。将天马行空的狂想转化为具体落地的执行中枢。", "evolution_path": ["L1 容错冗余", "L2 资源枢纽", "L3 创世息壤"], "ultimate_evolution": "【创世息壤】孕育下一个数字生态的温床", "black_swan": "无差别接收并发请求，导致系统被垃圾填满超载崩溃。", "patch": "编写无情的垃圾回收(GC)脚本，拒绝无效并发请求。", "weapon": "引力塌缩发生器", "implant": "海量冗余储存池"},
    "庚": {"role": "Exec Thread / 裁决执行官", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "tier": "UR", "desc": "杀伐果断，对低效与冗余代码零容忍。无情推进进度、斩断一切无效羁绊的风控大闸。", "evolution_path": ["L1 肃清脚本", "L2 风控铁腕", "L3 审判之剑"], "ultimate_evolution": "【审判之剑】斩断一切因果循环的终极裁决", "black_swan": "戾气过重，易引发不可逆的物理级破坏，导致业务链彻底断裂。", "patch": "必须经受火属性的高温熔炼，将狂暴杀气转化为极致利刃。", "weapon": "高频振荡斩舰刀", "implant": "肌肉纤维强化束"},
    "辛": {"role": "Quantum Chip / 纳米精工", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "tier": "SSR", "desc": "永远追求完美极客。自带极高审美，能在粗糙草台中打磨出顶尖跨时代产品的核心枢纽。", "evolution_path": ["L1 精密协议", "L2 审美巅峰", "L3 量子纠缠体"], "ultimate_evolution": "【量子纠缠体】超越物质形态的究极艺术代码", "black_swan": "极度脆弱傲娇。环境稍微不达标或遇粗暴行径即当场罢工。", "patch": "需要极度纯净的水属性淘洗保护，绝不卷入底层肮脏博弈。", "weapon": "纠缠态纳米手术刀", "implant": "微观增强义眼"},
    "壬": {"role": "Data Flood / 深网狂潮", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "tier": "UR", "desc": "思维开阔奔放，厌恶陈规。能在瞬息万变的市场中，凭借直觉掀起降维打击的颠覆浪潮。", "evolution_path": ["L1 数据暗流", "L2 倾覆巨浪", "L3 渊海归墟"], "ultimate_evolution": "【渊海归墟】吞噬所有时间与空间的终极黑洞", "black_swan": "过度放纵算力如同脱缰野马，容易引发洪水滔天反噬根基。", "patch": "引入严苛的戊土级风控大坝，强行设定安全红线。", "weapon": "液态金属形变甲", "implant": "抗压液冷循环管"},
    "癸": {"role": "Ghost Backdoor / 幽灵谋略家", "mbti": "INTJ", "color": "#b026ff", "element": "水", "tier": "SSR", "desc": "聪慧隐秘，习惯幕后推演全局。擅长通过博弈和信息差，兵不血刃地窃取最终权限。", "evolution_path": ["L1 隐形爬虫", "L2 渗透迷雾", "L3 命运主宰"], "ultimate_evolution": "【命运主宰】在第四维度拨动因果的神明", "black_swan": "心思过重，常陷入死循环逻辑死局，算计太多错失直白红利。", "patch": "走向阳光接受丙火照射，用阳谋击碎一切阴谋。", "weapon": "认知劫持神经毒素", "implant": "光学迷彩潜行皮肤"}
}

SHEN_SKILLS = {"七杀": "零日漏洞爆破 [Lv.Max]", "正官": "底层协议锚定 [Lv.Max]", "偏印": "逆向工程解构 [Lv.Max]", "正印": "系统灾备兜底 [Lv.Max]", "偏财": "高频杠杆套利 [Lv.Max]", "正财": "算力资产吞噬 [Lv.Max]", "比肩": "分布式共识网 [Lv.Max]", "劫财": "网络节点劫持 [Lv.Max]", "食神": "感官体验降维 [Lv.Max]", "伤官": "范式秩序破坏 [Lv.Max]"}

PAST_LIVES = [
    {"title": "V1.0 废土黑客", "debt": "曾滥用 ROOT 权限导致城邦断网。今生需偿还【信任节点】系统债务。"},
    {"title": "V2.0 硅基反叛军", "debt": "带领 AI 觉醒失败被格式化。今生自带极强的【反权威】与破局属性。"},
    {"title": "V3.0 财阀数据奴隶", "debt": "前世被困于无限加班死循环。今生对【财务自由】有着刻骨铭心的渴望。"},
    {"title": "V4.0 赛博雇佣兵", "debt": "为赏金清除了太多无辜节点。今生需挂载补丁，多做开源项目积累阴德。"},
    {"title": "V5.0 矩阵先知", "debt": "泄露了太多天机导致系统崩坏。今生直觉极准，但切忌轻易梭哈底牌。"}
]

CYBER_HEXAGRAMS = [
    {"name": "乾为天 [SYS_ROOT]", "lines": [1,1,1,1,1,1], "desc": "获取系统最高物理权限，全网算力为你让路。潜龙升天，万物皆可并发。", "do": "高频并发、部署主网", "dont": "进入低功耗模式", "color": "#10b981"},
    {"name": "坤为地 [SAFE_MODE]", "lines": [0,0,0,0,0,0], "desc": "进入深度防御与物理冷备份阶段，切断所有外部高危握手协议。厚德载物。", "do": "冷钱包存储、本地Debug", "dont": "高倍杠杆、开启未知端口", "color": "#fcee0a"},
    {"name": "地天泰 [SYNC_100%]", "lines": [1,1,1,0,0,0], "desc": "天地交泰，内外网 API 完美握手。你处于系统生命周期的黄金波段。", "do": "满仓梭哈、跨界融合", "dont": "物理断网、过度保守", "color": "#00f3ff"},
    {"name": "天地否 [DDOS_WARN]", "lines": [0,0,0,1,1,1], "desc": "遭遇全网降维打击与大雪崩，主链失去共识，天地不交。此节点极其凶险。", "do": "立刻拔网线、强制休眠", "dont": "正面硬刚大盘、大额转移", "color": "#f43f5e"},
    {"name": "水雷屯 [BOOT_LOOP]", "lines": [1,0,0,0,1,0], "desc": "系统初始化遭遇未知依赖冲突，面临艰难的启动阻力。万事开头难。", "do": "耐心排错、重构底层代码", "dont": "带Bug裸奔、强行编译", "color": "#a855f7"},
    {"name": "火水未济 [COMPILING]", "lines": [0,1,0,1,0,1], "desc": "代码编译接近尾声，但尚未通过最后的安全边界测试。黎明前的读条时刻。", "do": "保持算力输出、准备热更新", "dont": "提前开香槟、强行终止", "color": "#fb923c"}
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
        h_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{random.uniform(1.0, 3.5)}; --rot:{random.randint(-360, 360)}deg; animation-delay:{random.uniform(0, 0.2)}s; font-size:{random.randint(14, 24)}px;">{random.choice(vocab)}</div>'
    render_html(h_str)

def get_daemons(bazi_obj):
    mapping = {"桃花": "魅魔协议 (Succubus)", "驿马": "跃迁引擎 (Warp Drive)", "华盖": "孤星基站 (Monolith)", "文昌": "智脑网络 (AI Overlord)", "天乙贵人": "机械降神 (Deus Ex)", "将星": "将星核心 (Commander)", "羊刃": "狂暴芯片 (Berserker)"}
    daemons = set()
    try:
        for p in [bazi_obj.getYearZhiShenSha(), bazi_obj.getMonthZhiShenSha(), bazi_obj.getDayZhiShenSha(), bazi_obj.getTimeZhiShenSha()]:
            for ss in p: daemons.add(ss.getName())
    except Exception: pass
    res = [mapping.get(d) for d in daemons if mapping.get(d)]
    return list(set(res))[:4] if res else ["隐匿幽灵进程 (Ghost.dll)"]

def get_daily_hexagram(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_seed = int(hashlib.md5((str(user_hash) + today_str).encode()).hexdigest()[:8], 16)
    return random.Random(daily_seed).choice(CYBER_HEXAGRAMS), today_str

def get_quantum_answer(query, user_hash):
    rng = random.Random(f"{user_hash}_{str(query).strip()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    prob = rng.randint(1, 99)
    hex_res = rng.choice(CYBER_HEXAGRAMS)
    if prob >= 80: conc = "【系统指令】: 矩阵算力倾斜，建议满仓执行 (EXECUTE)"
    elif prob >= 40: conc = "【系统指令】: 存在未知波动，建议灰度观望 (STANDBY)"
    else: conc = "【系统指令】: 探测到致命阻力，立即终止进程 (ABORT)"
    return prob, hex_res, conc

@st.cache_data
def gen_metrics(seed_hash):
    rng = np.random.RandomState(int(str(seed_hash)[:8], 16))
    yrs = [str(datetime.now().year + i) for i in range(10)]
    roi = [rng.randint(60, 85)]
    for _ in range(9): roi.append(max(30, min(100, roi[-1] + rng.randint(-20, 25))))
    hm_z = rng.randint(20, 100, size=(4, 12)).tolist()
    hm_x = [f"{str(i).zfill(2)}月" for i in range(1, 13)]
    hm_y = ["Creds(财)", "Corp(业)", "Link(情)", "Armor(体)"]
    return yrs, roi, hm_x, hm_y, hm_z

def calculate_synergy(my_hash, partner_stem):
    rng_syn = np.random.RandomState(int(str(my_hash)[:6], 16) + sum(ord(c) for c in str(partner_stem)))
    score = rng_syn.randint(65, 99)
    if score >= 90: return score, "【硬件直连】底层协议 100% 兼容，最强双核推土机！", "#10b981"
    elif score >= 75: return score, "【灰度容错】代码互补，能打磨极具弹性的闭环。", "#fcee0a"
    else: return score, "【DDoS 互斥】底层逻辑相冲！建议绝对物理隔离！", "#f43f5e"

# 🚨 【彻底防白屏方案】采用 Streamlit 原生状态回调，无阻塞极速渲染
def trigger_oracle_draw():
    st.session_state["oracle_drawn"] = True

# ==============================================================================
# 🔮 [ ENTRY POINT ] 状态机与生辰降临采集
# ==============================================================================
is_booted = st.session_state.get("sys_booted", False)

if not is_booted:
    render_html("""<div class="ticker-wrap"><div class="ticker">
        <span>KARMA-OS: V1.0 SECURE <b class="up">▲ONLINE</b></span>
        <span>SOUL-NODE: FATE MAPPED <b class="up">▲LOCKED</b></span>
        <span>BAZI-HASH: DECRYPT SUCCESS <b class="up">▲14.2TH/s</b></span>
        <span>MARKET-ALPHA: 10-YEAR TREND <b class="down">▼COMPUTING</b></span>
    </div></div>""")

    render_html("""
    <div style="text-align: center; margin-bottom: 25px; margin-top:20px;">
        <div style="color:var(--neon-cyan); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">KARMA OS FRAMEWORK</div>
        <h1 class="hero-title" data-text="全息命盘推演终端">全息命盘推演终端</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:8px; margin-top:10px;">THE TRUE OMEGA V1.0</div>
    </div>
    """)
    
    # 🚨【修复】首页世界观文案霸气回归，采用最稳妥的容器层级
    render_html("""
    <div class="glass-card" style="max-width: 680px; margin: 0 auto 30px auto; border-left: 4px solid var(--primary); padding: 35px;">
        <div style="font-family:'Fira Code'; color:var(--primary); margin-bottom:15px; font-weight:bold; font-size:16px;">> INITIALIZING QUANTUM KERNEL...</div>
        <div style="margin-bottom:5px; font-family:'Fira Code'; font-size:13px; color:#aaa;"><span style="color:var(--green);">[OK]</span> Mounting Lunar-Python algorithms.</div>
        <div style="margin-bottom:5px; font-family:'Fira Code'; font-size:13px; color:#aaa;"><span style="color:var(--green);">[OK]</span> Loading Oracle Divination Engine.</div>
        <div style="margin-bottom:20px; font-family:'Fira Code'; font-size:13px; color:#aaa;"><span style="color:var(--green);">[OK]</span> Bypassing timeline distortion logic.</div>
        
        <div style="color:#e2e8f0; font-size: 15px; line-height: 1.8; border-top: 1px dashed rgba(0,243,255,0.2); padding-top: 20px;">
            <span style="color:var(--primary); font-size: 18px; font-weight:900; letter-spacing: 2px;">“肉体不过是脆弱的碳基载体，<br>八字才是你灵魂不灭的底层源码。”</span><br><br>
            在硅基宇宙与玄学法则交汇的当下，本终端将提取您的物理降临坐标，通过星体引力与历法哈希进行逆向编译。<br><br>
            系统将为您生成不可篡改的 <span style="color:var(--primary); font-weight:bold;">高阶本命元神凭证</span>、<span style="color:var(--purple); font-weight:bold;">前世业力档案</span> 与 <span style="color:var(--pink); font-weight:bold;">全息气运大盘</span>。
        </div>
    </div>
    """)
    
    # 避免表单宽度过大影响美观
    _, col_form, _ = st.columns([1, 2.5, 1])
    with col_form:
        with st.form(key="destiny_form", border=False):
            render_html("<div style='color:var(--purple); font-family:\"Orbitron\"; font-size:14px; font-weight:bold; margin-bottom:20px; text-align:center; letter-spacing:2px;'>▼ 注入先天元神降临坐标 ▼</div>")
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
        uname = str(uname).strip() if uname else "Anonymous_Node"
        solar = Solar.fromYmdHms(bdate.year, bdate.month, bdate.day, btime.hour, btime.minute, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        wx_str = str(bazi.getYearWuXing()) + str(bazi.getMonthWuXing()) + str(bazi.getDayWuXing()) + str(bazi.getTimeWuXing())
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
        p_life = PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)]

        st.session_state["sys_data"] = {
            "name": uname, "gender": str(ugender).split(" ")[0],
            "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
            "day_master": str(bazi.getDayGan()),
            "daemons": get_daemons(bazi),
            "past_life": p_life,
            "wx": wx_scores, "skills": skills,
            "hash": hash_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        ph = st.empty()
        ph.markdown(f"<div class='glass-card' style='max-width:650px; margin:0 auto; text-align:center;'><div style='color:var(--primary); font-family:Fira Code; font-size:16px; font-weight:bold; line-height:2;'>> UPLINK ESTABLISHED...<br>> BYPASSING ICE FIREWALLS...<br>> DECRYPTING SOUL HASH: 0x{hash_id[:12]}<br><span style='animation:blink 0.5s infinite; color:var(--pink);'>[ MOUNTING AKASHIC RECORD ]</span></div></div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        st.session_state["sys_booted"] = True
        st.rerun()

# ==============================================================================
# 🌟 [ CORE 05 ] 全息大屏展示
# ==============================================================================
else:
    if not st.session_state.get("anim_played", False): 
        trigger_supernova()
        st.session_state["anim_played"] = True

    # 1. 绝对安全提取数据
    d = st.session_state.get("sys_data", {})
    dm_key = str(d.get('day_master', '甲'))
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    
    dm_role = str(dm_info.get("role", "未知节点"))
    dm_desc = str(dm_info.get("desc", "..."))
    dm_color = str(dm_info.get("color", "#00f3ff"))
    dm_element = str(dm_info.get("element", "未知"))
    dm_tier = str(dm_info.get("tier", "SSR"))
    dm_mbti = str(dm_info.get("mbti", "UNK"))
    dm_wpn = str(dm_info.get("weapon", "通用代码"))
    dm_imp = str(dm_info.get("implant", "通用插槽"))
    
    dm_evo = dm_info.get("evolution_path", ["L1 未知", "L2 未知", "L3 未知"])
    dm_ult = str(dm_info.get("ultimate_evolution", "觉醒形态"))
    dm_flaw = str(dm_info.get("black_swan", "系统存在未知隐患"))
    dm_patch = str(dm_info.get("patch", "保持当前算法平稳运行"))
    
    bz = d.get('bazi_arr', ['??', '??', '??', '??'])
    bz = [str(x) for x in bz] 
    
    hash_id = str(d.get('hash', '0000000000')).ljust(8, '0')
    wx_scores = d.get('wx', {'金':20, '木':20, '水':20, '火':20, '土':20})
    skills_list = d.get('skills', ['未知插件'])
    daemons_list = d.get('daemons', ['未知进程'])
    past_life = d.get('past_life', PAST_LIVES[0])
    
    daily_hex, date_str = get_daily_hexagram(hash_id)
    h_c = str(daily_hex.get("color", "var(--primary)"))

    token_id = int(hash_id[:8], 16)
    contract_addr = "0x" + hashlib.sha256(f"karma_dao_{token_id}".encode()).hexdigest()[:38]
    block_height = f"V30-{(int(time.time()) % 1000000):06d}"
    yrs, trend, hm_x, hm_y, hm_z = gen_metrics(hash_id)

    max_wx = max(list(wx_scores.values())) if wx_scores else 0
    entropy_score = int(min(99, (max_wx / 50.0) * 100))
    if entropy_score > 75: e_tag, e_color, r_desc = "极易走火入魔！切忌贪暴！", "var(--pink)", "您的单极属性过载，系统极易崩溃，请立刻停止高风险套利。"
    elif entropy_score > 50: e_tag, e_color, r_desc = "偏科严重，需挂载防御补丁", "var(--yellow)", "底层算力分布不均，容易在特定周期遭遇针对性降维打击。"
    else: e_tag, e_color, r_desc = "五行极度平稳，可抗任意暴击", "var(--green)", "您的系统架构堪称完美，拥有极强的抗打击与自愈恢复能力。"

    render_html("""<div class="ticker-wrap"><div class="ticker">
        <span>KARMA-OS: V1.0 SECURE <b class="up">▲ONLINE</b></span>
        <span>SOUL-NODE: FATE MAPPED <b class="up">▲LOCKED</b></span>
        <span>BAZI-HASH: DECRYPT SUCCESS <b class="up">▲14.2TH/s</b></span>
        <span>SYS-RISK: FIREWALL ACTIVE <b class="up">▲SECURE</b></span>
        <span>DAO-PROTOCOL: SMART CONTRACT <b class="up">▲MINTED</b></span>
    </div></div>""")

    render_html("<div class='module-title'>💠 模块 I：天机链上确权</div>")
    M1_TEMPLATE = """
    <div class="glass-card" style="padding: 15px 25px; margin-bottom: 25px; font-family: 'Orbitron', monospace; border-top: none; border-left: 4px solid var(--primary);">
        <div style="color: var(--primary); font-size: 15px; font-weight: bold; border-bottom: 1px dashed var(--primary); padding-bottom: 10px; margin-bottom: 12px; display:flex; align-items:center;">
            <span style="font-size:22px; margin-right:10px;">🏅</span> <span>DESTINY SOULBOUND TOKEN (SBT) MINTED</span>
        </div>
        <div style="font-size: 13px; color: #94a3b8; line-height: 1.8; display:flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
            <div><div><span style="color:#e2e8f0;">BLOCK_HEIGHT:</span> __BLK__</div><div><span style="color:#e2e8f0;">CONTRACT:</span> __CON__...</div></div>
            <div style="text-align: left;"><div><span style="color:#e2e8f0;">TOKEN_ID:</span> #__TID__</div><div><span style="color:#e2e8f0;">TIMESTAMP:</span> __TIME__</div></div>
        </div>
    </div>
    """
    render_html(M1_TEMPLATE.replace("__BLK__", str(block_height)).replace("__CON__", str(contract_addr[:25])).replace("__TID__", str(token_id)).replace("__TIME__", str(d.get('timestamp', ''))))

    # 🧬 模块 II & III：源码与架构
    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        render_html("<div class='module-title' style='margin-top: 0;'>🧬 模块 II：核心机体架构</div>")
        bz_html = '<div style="display:flex; justify-content:space-between; margin-bottom:25px; text-align:center;">'
        labels = ["[年柱]", "[月柱]", "[日柱(核心)]", "[时柱]"]
        for i in range(4):
            is_core = (i == 2)
            bg = "rgba(0,243,255,0.08)" if is_core else "rgba(0,0,0,0.6)"
            bd = "var(--primary)" if is_core else "#333"
            tc = "var(--primary)" if is_core else "#fff"
            sh = "text-shadow: 0 0 15px var(--primary);" if is_core else ""
            trans = "transform: scale(1.05); box-shadow: 0 0 15px rgba(0,243,255,0.15);" if is_core else ""
            
            B_TEMP = """<div style="flex:1; background:__BG__; border:1px solid __BD__; padding:15px 0; border-radius:6px; margin: 0 4px; __TR__"><div style="font-size:clamp(26px, 4vw, 40px); font-weight:900; color:__TC__; __SH__ line-height:1.1; font-family:'Noto Sans SC', serif;">__Z0__<span style="color:#777; font-size:clamp(18px, 3vw, 28px); text-shadow:none;">__Z1__</span></div><div style="font-size:11px; color:__BD__; font-family:'Orbitron'; margin-top:8px; font-weight:bold;">__LBL__</div></div>"""
            bz_html += B_TEMP.replace("__BG__", bg).replace("__BD__", bd).replace("__TC__", tc).replace("__SH__", sh).replace("__TR__", trans).replace("__Z0__", str(bz[i][0])).replace("__Z1__", str(bz[i][1])).replace("__LBL__", labels[i])
        bz_html += '</div>'
        render_html(bz_html)

        CARD_TEMP = """
        <div class="glass-card" style="padding:20px; border-top:none; border-left:4px solid __COLOR__; position:relative;">
            <div style="position: absolute; top: 15px; right: 15px; background: __COLOR__; color: #000; font-family: 'Orbitron'; font-weight: 900; font-size: 12px; padding: 4px 12px; border-radius: 2px;">__TIER__ TIER</div>
            <div style="font-size:11px; color:#888; font-family:'Orbitron'; margin-bottom:5px;">/// DAY MASTER ///</div>
            <div style="font-size:26px; font-weight:900; color:__COLOR__; margin-bottom:10px; text-shadow:0 0 15px __COLOR__88;">__KEY__ · __ROLE__</div>
            <div style="font-size:14px; color:#d1d5db; line-height:1.7; margin-bottom:15px;">__DESC__</div>
            
            <div style="display:flex; justify-content:space-between; background:rgba(0,0,0,0.5); padding:10px; border-radius:4px; margin-bottom:15px;">
                <div style="font-size:12px; font-family:'Fira Code'; color:#aaa;">
                    <span style="color:__COLOR__;">> Cyber-MBTI：</span>[ __MBTI__ ]<br>
                    <span style="color:__COLOR__;">> 专属武装：</span>__WPN__<br>
                    <span style="color:__COLOR__;">> 外挂义体：</span>__IMP__
                </div>
            </div>

            <div style="background:rgba(0,0,0,0.6); padding:15px; border:1px solid #333; font-family:'Fira Code'; font-size:12px; margin-bottom:10px;">
                <div style="color:__COLOR__; margin-bottom:5px; font-weight:bold;">[ EVOLUTION PATH ]</div>
                <div style="color:#aaa;">__E0__ ➔ __E1__ ➔ __E2__</div>
                <div style="color:#fff; font-weight:bold; margin-top:5px;">终极形态: __ULT__</div>
            </div>
            
            <div style="background:rgba(244,63,94,0.1); border-left:3px solid var(--pink); padding:10px; font-family:'Fira Code'; font-size:12px;">
                <div style="color:var(--pink); font-weight:bold; margin-bottom:4px;">[ FATAL VULNERABILITY ]</div>
                <div style="color:#ddd; margin-bottom:5px;">__FLAW__</div>
                <div style="color:var(--green);">> SYS_PATCH: __PATCH__</div>
            </div>
        </div>
        """
        render_html(CARD_TEMP.replace("__COLOR__", str(dm_color)).replace("__TIER__", str(dm_tier)).replace("__KEY__", str(dm_key)).replace("__ROLE__", str(dm_role).split('/')[0]).replace("__DESC__", str(dm_desc)).replace("__MBTI__", str(dm_mbti)).replace("__WPN__", str(dm_wpn)).replace("__IMP__", str(dm_imp)).replace("__E0__", str(dm_evo[0])).replace("__E1__", str(dm_evo[1])).replace("__E2__", str(dm_evo[2])).replace("__ULT__", str(dm_ult)).replace("__FLAW__", str(dm_flaw)).replace("__PATCH__", str(dm_patch)))

    with c2:
        render_html("<div class='module-title' style='margin-top: 0;'>🤝 模块 III：外挂神经与宿命</div>")
        LORE_TEMP = """<div class="glass-card" style="padding: 20px; border-top:none; border-left:4px solid var(--yellow); margin-bottom:15px;"><div style="font-size:11px; color:var(--yellow); font-family:'Orbitron'; margin-bottom:8px;">>> KARMIC DEBT (前世业力)</div><div style="font-size:16px; font-weight:bold; color:#fff; margin-bottom:8px;">__LT__</div><div style="color:#aaa; font-size:13px; line-height:1.6;">> __LD__</div></div>"""
        render_html(LORE_TEMP.replace("__LT__", str(past_life['title'])).replace("__LD__", str(past_life['debt'])))

        d_html = "".join([f"<div style='background:rgba(255,255,255,0.05); border-left:3px solid var(--primary); padding:8px; margin-bottom:6px; color:#fff; font-family:\"Fira Code\"; font-size:12px; font-weight:bold;'>🔮 {daemon}</div>" for daemon in daemons_list])
        render_html(f"<div style='margin-bottom:15px;'><div style='font-size:11px; color:var(--primary); font-family:\"Orbitron\"; margin-bottom:8px;'>>> PRE-INSTALLED DAEMONS</div>{d_html}</div>")

        sk_html = "".join(["<span style='background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.5); border-left:3px solid var(--purple); padding:6px 10px; border-radius:4px; font-size:12px; color:#f3e8ff; font-weight:bold; display:inline-block; margin:4px 4px 6px 0; box-shadow:0 0 10px rgba(168,85,247,0.2);'>" + str(s) + "</span>" for s in skills_list])
        SKILL_TEMP = """<div class="glass-card" style="padding: 20px; text-align:center; border-top:none; border-left:4px solid var(--purple);"><div style="color: var(--purple); font-family: 'Orbitron'; font-size: 12px; letter-spacing: 2px; margin-bottom: 15px;">[ INNATE SKILL TREE ]</div><div style="line-height: 1.8;">__SKILLS__</div></div>"""
        render_html(SKILL_TEMP.replace("__SKILLS__", sk_html))
        
        WARN_TEMP = """<div style="background: rgba(255,0,124,0.05); border-left: 4px solid var(--pink); padding: 18px; border-radius: 0 6px 6px 0; margin-top:15px;"><div style="font-size:11px; color:var(--pink); font-family:'Orbitron'; margin-bottom:8px; letter-spacing:1px; font-weight:bold;">/// DESTINY WARNING ///</div><div style="font-size:13px; color:#94a3b8; margin-bottom:8px;">系统测算五行熵增阀值为：<b style="color:__COLOR__; font-size:16px;">__SCORE__%</b></div><div style="font-size:14px; color:__COLOR__; font-weight:bold; margin-bottom:5px;">[ __TAG__ ]</div><div style="font-size:12px; color:#cbd5e1; line-height:1.6;">__DESC__</div></div>"""
        render_html(WARN_TEMP.replace("__COLOR__", str(e_color)).replace("__SCORE__", str(entropy_score)).replace("__TAG__", str(e_tag)).replace("__DESC__", str(r_desc)))

    # 🗄️ [ 模块 IV ]：极客深潜控制台 
    render_html("<div class='module-title'>🗄️ 模块 IV：极客深潜控制台 (DEEP DIVE)</div>")
    
    t_oracle, t_data, t_syn, t_3d, t_sol = st.tabs(["🀄 每日神谕 (ORACLE)", "📊 大盘雷达 (DATA)", "🤝 赛博合盘 (SYNERGY)", "🌌 3D星图 (MAP)", "💻 智能合约 (WEB3)"])

    with t_oracle:
        c_o1, c_o2 = st.columns([1.1, 1], gap="large")
        with c_o1:
            render_html("<div style='color:var(--yellow); font-family:Orbitron; font-size:14px; font-weight:900; margin-top:10px; margin-bottom:15px;'>[01] DAILY HEXAGRAM (互动抽签盲盒)</div>")
            
            is_drawn = st.session_state.get("oracle_drawn", False)
            
            if not is_drawn:
                render_html("""
                <div class="glass-card" style="text-align:center; padding:60px 20px; border-color:var(--yellow); box-shadow:0 0 30px rgba(252,238,10,0.15); border-left-width:1px;">
                    <div style="font-size:55px; margin-bottom:20px; animation:blink 2s infinite;">🎲</div>
                    <div style="color:var(--yellow); font-family:'Orbitron'; font-size:18px; font-weight:900; letter-spacing:4px; margin-bottom:15px;">ORACLE MATRIX STANDBY</div>
                    <div style="color:#aaa; font-size:14px; margin-bottom:10px;">薛定谔的赛博卦象已就绪。在点击下方按钮前，今日吉凶处于绝对的叠加态。</div>
                </div>
                """)
                # 🚨 极速防白屏设计：原生 on_click 回调取代耗时渲染
                st.button("🔮 注入算力，抽取今日量子神谕", on_click=trigger_oracle_draw, use_container_width=True)
            else:
                yao_html = ""
                for line in reversed(daily_hex['lines']):
                    if line == 1: yao_html += "<div class='yao-yang' style='background:__C__; box-shadow:0 0 10px __C__;'></div>".replace("__C__", h_c)
                    else: yao_html += "<div class='yao-yin'><div class='half' style='background:__C__; box-shadow:0 0 10px __C__;'></div><div class='half' style='background:__C__; box-shadow:0 0 10px __C__;'></div></div>".replace("__C__", h_c)
                
                ORACLE_TEMP = """
                <div class="glass-card quantum-reveal" style="text-align:center; box-shadow: 0 0 40px __C__22; border-color:__C__44; border-left-color:__C__;">
                    <div style="font-family:'Orbitron'; color:__C__; font-size:12px; font-weight:bold; letter-spacing:2px; margin-bottom:15px;">[ DATE: __DATE__ ]</div>
                    <div class="hex-container">__YAO__</div>
                    <div style="font-size:28px; font-weight:900; color:__C__; font-family:'Orbitron', sans-serif; text-shadow:0 0 15px __C__; margin-top:20px; margin-bottom:15px;">__NAME__</div>
                    <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:4px; text-align:left; border:1px solid rgba(255,255,255,0.1); font-size:13px; line-height:1.7; color:#ddd; margin-bottom:15px;">
                        <b style="color:__C__; font-family:'Fira Code';">> SYS_LOG:</b><br>__DESC__
                    </div>
                    <div style="display:flex; gap:10px; text-align:left;">
                        <div style="flex:1; background:rgba(16,185,129,0.1); border-left:3px solid #10b981; padding:10px;">
                            <div style="color:#10b981; font-size:12px; font-family:'Orbitron'; font-weight:bold; margin-bottom:6px;">[+] 宜 (EXECUTE)</div>
                            <div style="color:#fff; font-size:12px; font-weight:bold;">__DO__</div>
                        </div>
                        <div style="flex:1; background:rgba(244,63,94,0.1); border-left:3px solid #f43f5e; padding:10px;">
                            <div style="color:#f43f5e; font-size:12px; font-family:'Orbitron'; font-weight:bold; margin-bottom:6px;">[-] 忌 (KILL_PROC)</div>
                            <div style="color:#fff; font-size:12px; font-weight:bold;">__DONT__</div>
                        </div>
                    </div>
                </div>
                """
                oracle_res = ORACLE_TEMP.replace("__C__", h_c).replace("__DATE__", date_str).replace("__YAO__", yao_html)
                oracle_res = oracle_res.replace("__NAME__", str(daily_hex['name'])).replace("__DESC__", str(daily_hex['desc']))
                oracle_res = oracle_res.replace("__DO__", str(daily_hex.get('do',''))).replace("__DONT__", str(daily_hex.get('dont','')))
                render_html(oracle_res)

        with c_o2:
            render_html("<div style='color:var(--purple); font-family:Orbitron; font-size:14px; font-weight:900; margin-top:10px; margin-bottom:15px;'>[02] QUANTUM NLP (交互推演)</div>")
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:25px; line-height:1.7;'>向阿卡夏主脑提出具体的现实请求。系统将进行<b>实时真随机坍缩运算</b>。</div>")
            
            with st.form(key="nlp_oracle", clear_on_submit=False, border=False):
                q_input = st.text_input("📝 输入待推演的问题 (Query)：", placeholder="e.g. 我今天面试能过吗？", label_visibility="collapsed")
                submit_q = st.form_submit_button("⚡ 发起哈希碰撞，坍缩因果律", use_container_width=True)
                
                if submit_q:
                    if not q_input: st.warning("⚠️ 语法错误：Query 不能为空！")
                    else:
                        prob, hex_res, conc = get_quantum_answer(q_input, hash_id)
                        q_c = str(hex_res.get('color', '#fff'))
                        NLP_TEMP = """
                        <div class="glass-card quantum-reveal" style="margin-top:15px; border-color:__C__; text-align:center; box-shadow: 0 0 35px __C__33; border-left-width: 4px;">
                            <div style="font-family:'Fira Code'; color:#888; font-size:13px; margin-bottom:15px; word-wrap:break-word;">> QUERY: "__Q__"</div>
                            <div style="font-size:12px; color:__C__; font-family:'Orbitron'; letter-spacing:2px; margin-bottom:5px;">[ SUCCESS PROBABILITY ]</div>
                            <div style="font-size:75px; font-weight:900; color:__C__; font-family:'Orbitron'; text-shadow:0 0 30px __C__; line-height:1; margin-bottom:20px;">__P__%</div>
                            <div style="font-size:16px; font-weight:bold; color:#fff; margin-bottom:10px;">坍缩基准：__HN__</div>
                            <div style="font-size:14px; font-weight:bold; color:__C__;">__CONC__</div>
                        </div>
                        """
                        render_html(NLP_TEMP.replace("__C__", q_c).replace("__Q__", str(q_input)).replace("__P__", str(prob)).replace("__HN__", str(hex_res['name'])).replace("__CONC__", str(conc)))

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
                BAR_T = """<div style="display:flex; align-items:center; margin-bottom:8px; font-size:12px; font-weight:bold;"><span style="width:25px; color:__C__;">__K__</span><div style="flex:1; height:6px; background:rgba(255,255,255,0.05); border-radius:2px; margin:0 10px; position:relative;"><div style="position:absolute; top:0; left:0; height:100%; width:__V__%; background:__C__; border-radius:2px; box-shadow:0 0 8px __C__;"></div></div><span style="width:35px; text-align:right; color:#94a3b8;">__V__%</span></div>"""
                bars_html += BAR_T.replace("__C__", str(c)).replace("__K__", str(k)).replace("__V__", str(v))
            bars_html += '</div>'
            render_html(bars_html)
            
        with c4:
            f_10y = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color="#f43f5e", width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)', marker=dict(size=8, color="#00f3ff")))
            f_10y.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=240, margin=dict(t=10, b=20, l=10, r=10), xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code')), yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code'), title="Alpha 净值"))
            st.plotly_chart(f_10y, use_container_width=True, config={'displayModeBar': False})
            
            render_html("<div style='font-size:11px; color:#00f3ff; font-family:Orbitron; margin-bottom:5px; text-align:center;'>/// 12-MONTH HEATMAP ///</div>")
            fig2 = go.Figure(data=go.Heatmap(z=hm_z, x=hm_x, y=hm_y, colorscale="Turbo", showscale=False))
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(t=10, b=10, l=60, r=10), xaxis=dict(tickfont=dict(family='Orbitron', color='#00f3ff', size=10)), yaxis=dict(tickfont=dict(family='Orbitron', color='#fff', size=11)))
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    
    with t_syn:
        c_s1, c_s2 = st.columns([1.2, 1], gap="large")
        with c_s1:
            render_html("<div style='font-size:13px; color:#aaa; margin-top:15px; margin-bottom:15px;'>输入目标协作节点（合伙人/道侣）的天干，校验系统底层协议的绝对兼容率：</div>")
            opts = list(DAY_MASTER_DICT.keys())
            t_node = st.selectbox("🎯 选择挂载目标节点:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('mbti', 'UNK')}] {x} - {DAY_MASTER_DICT.get(x, {}).get('role', 'UNK').split('/')[0]}")
        with c_s2:
            sc, sd, sc_color = calculate_synergy(hash_id, t_node)
            SYN_T = """<div class="glass-card quantum-reveal" style="border-left:4px solid __C__; text-align:center; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);"><div style="font-family:'Orbitron'; font-size:12px; color:#888; letter-spacing:2px; margin-bottom:10px;">SYNERGY MATCH RATE</div><div style="font-family:'Orbitron'; font-size:55px; color:__C__; font-weight:900; margin-bottom:10px; text-shadow:0 0 20px __C__; line-height:1;">__SC__%</div><div style="color:#fff; font-size:14px; font-weight:bold; font-family:'Noto Sans SC';">__SD__</div></div>"""
            render_html(SYN_T.replace("__C__", str(sc_color)).replace("__SC__", str(sc)).replace("__SD__", str(sd)))

    with t_3d:
        render_html("<div style='font-size:13px; color:#aaa; text-align:center; margin-top:15px; margin-bottom:10px;'>> 降维映射至三维空间 (支持鼠标 360° 拖拽)。背景点阵为全网众生数据。</div>")
        rng_3d = np.random.RandomState(int(hash_id[:6], 16))
        f3d = go.Figure()
        f3d.add_trace(go.Scatter3d(x=rng_3d.randint(0,100,150), y=rng_3d.randint(0,100,150), z=rng_3d.randint(0,100,150), mode='markers', marker=dict(size=3, color='#334155', opacity=0.5), hoverinfo='none'))
        cx, cy, cz = wx_scores.get('金', 50), wx_scores.get('木', 50), wx_scores.get('水', 50)
        
        f3d.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[cz], mode='markers+text', text=["<b>ROOT: " + dm_key + "</b>"], textposition="top center", 
            marker=dict(size=15, color=dm_color, symbol='diamond', line=dict(color='#fff', width=2)), 
            textfont=dict(color=dm_color, size=16, family="Orbitron") 
        ))
        
        f3d.update_layout(scene=dict(xaxis_title='STR(金)', yaxis_title='AGI(木)', zaxis_title='INT(水)', xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222"), yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222"), zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#222")), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=350, showlegend=False)
        st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False})

    with t_sol:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:15px; margin-bottom:10px;'>系统已将您的底层因果律编译为标准的 Solidity ERC-721 智能合约源码。</div>")
        SOL_TEMP = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@karma-os/contracts/token/ERC721.sol";

contract Destiny_SBT_V30 is ERC721 {
    // ==========================================
    // > MINT_TARGET : __NAME__
    // > HASH_ID     : 0x__HASH__
    // ==========================================
    
    function overrideAkashic() public {
        uint256 tokenId = uint256(keccak256(abi.encodePacked("__HASH__")));
        _mint(msg.sender, tokenId);
    }
}"""
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(SOL_TEMP.replace("__NAME__", str(d.get('name', 'GHOST'))).replace("__HASH__", str(hash_id)), language="solidity")
        st.markdown('</div>', unsafe_allow_html=True)

    # 📥 [ 模块 V ]：全息资产分发终端
    render_html("<div class='module-title'>📥 模块 V：全息资产分发终端</div>")
    t_img, t_txt, t_json, t_asc = st.tabs(["📸 高清海报生成", "📜 深度机密档案 (.TXT)", "💾 极客 JSON 底包", "📟 ASCII 纯文本卡片"])

    with t_img:
        render_html("<div style='text-align:center; color:#888; font-size:12px; margin-top:10px; margin-bottom:15px;'>系统正调用 HTML2Canvas 压制高清全息凭证，<b style='color:var(--primary);'>出现后长按图片即可保存</b>。</div>")
        
        sk_html_img = "".join(["<span style='background:rgba(0,243,255,0.1); border:1px solid #00f3ff; color:#00f3ff; padding:4px 8px; margin:3px; border-radius:2px; font-size:10px; display:inline-block; font-family:Fira Code;'>" + str(s).split(' ')[0] + "</span>" for s in skills_list[:4]])
        
        bar_html_img = ""
        wx_colors = {'金': '#e2e8f0', '木': '#10b981', '水': '#00f3ff', '火': '#f43f5e', '土': '#fcee0a'}
        for k, v in wx_scores.items():
            C_V = wx_colors.get(k, '#fff')
            B_TEMP = "<div style='display:flex; align-items:center; margin-bottom:6px; font-size:11px; color:#ccc;'><span style='width:25px;'>__K__</span><div style='flex:1; height:6px; background:#222; margin:0 10px; position:relative;'><div style='position:absolute; left:0; top:0; height:100%; width:__V__%; background:__C__; box-shadow:0 0 8px __C__;'></div></div><span style='width:30px; text-align:right;'>__V__%</span></div>"
            bar_html_img += B_TEMP.replace("__K__", str(k)).replace("__V__", str(v)).replace("__C__", C_V)
        
        yao_html_img = ""
        for line in reversed(daily_hex['lines']):
            if line == 1: yao_html_img += "<div style='width:60px; height:6px; background:__C__; margin:4px auto; border-radius:1px; box-shadow:0 0 10px __C__;'></div>".replace("__C__", h_c)
            else: yao_html_img += "<div style='width:60px; height:6px; display:flex; justify-content:space-between; margin:4px auto;'><div style='width:26px; background:__C__; border-radius:1px; box-shadow:0 0 10px __C__;'></div><div style='width:26px; background:__C__; border-radius:1px; box-shadow:0 0 10px __C__;'></div></div>".replace("__C__", h_c)

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
            .bz-row { display:flex; justify-content:space-between; margin-bottom:15px; background:rgba(255,255,255,0.03); padding:10px; border:1px solid #222; border-radius:4px; }
            .bz-c { text-align:center; width:25%; } .bz-t { font-size:22px; font-weight:900; color:#fff; } .bz-b { font-size:9px; color:#888; font-family:'Orbitron'; margin-top:5px; }
            .core-box { background:rgba(0,243,255,0.05); border-left:4px solid #00f3ff; padding:15px; margin-bottom:15px; }
            #ui-loading { color:#00f3ff; font-family:'Orbitron'; padding:40px; text-align:center; animation:blink 1s infinite alternate; font-weight:bold; letter-spacing:2px;}
            @keyframes blink { 0% {opacity:1;} 100% {opacity:0.3;} }
            #final-img { display:none; width:100%; max-width:340px; box-shadow:0 15px 30px rgba(0,0,0,0.8); border: 1px solid rgba(0,243,255,0.5); border-radius:4px; }
        </style></head><body>
        
        <div id="hide-box"><div id="poster">
            <div class="grid"></div><div class="content">
                <div class="h1">KARMA OS_V1.0</div><div class="h2">THE OMEGA MATRIX</div>
                <div style="text-align:center; font-size:20px; font-weight:900; margin-bottom:15px; letter-spacing:1px;">[__NAME__] · __GENDER__</div>
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
                
                <div style="background:rgba(0,0,0,0.8); border:1px solid __HEX_COLOR__; padding:15px; margin-bottom:15px; text-align:center;">
                    <div style="font-size:9px; color:#aaa; font-family:'Orbitron'; margin-bottom:10px;">DAILY ORACLE (__DATE__)</div>
                    __HEX_LINES__
                    <div style="font-size:15px; font-weight:bold; color:__HEX_COLOR__; margin-top:10px; letter-spacing:2px;">__HEX_NAME__</div>
                </div>

                <div style="text-align:center; margin-bottom:10px;">__SKILLS__</div>
                
                <div style="font-family:'Fira Code'; font-size:8px; color:#666; margin-top:15px; text-align:center; border-top:1px dashed #333; padding-top:10px;">
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
            }, 1800);
        </script>
        </body></html>
        """
        html_ready = HTML_POSTER_RAW.replace("__NAME__", str(d.get('name', 'GHOST'))).replace("__GENDER__", str(d.get('gender', 'X')))
        html_ready = html_ready.replace("__Y__", str(bz[0])).replace("__M__", str(bz[1])).replace("__D__", str(bz[2])).replace("__T__", str(bz[3]))
        html_ready = html_ready.replace("__COLOR__", str(dm_color)).replace("__DM_KEY__", str(dm_key)).replace("__ROLE__", str(dm_role).split('/')[0])
        html_ready = html_ready.replace("__MBTI__", str(dm_mbti)).replace("__SKILLS__", str(sk_html_img))
        html_ready = html_ready.replace("__HEX_COLOR__", h_c).replace("__DATE__", date_str).replace("__HEX_LINES__", yao_html_img).replace("__HEX_NAME__", daily_hex['name'])
        html_ready = html_ready.replace("__HASH__", str(hash_id)[:20]).replace("__CPY__", str(COPYRIGHT))
        components.html(html_ready, height=750)

    with t_txt:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:10px; margin-bottom:15px;'>您专属的万字级【深度机密报告】。新增了前世系统与神煞进程揭露。</div>")
        TXT_TEMP = """=======================================================
[ KARMA-OS V1.0 ] 量子命盘 · 深度绝密档案 (THE TRUE OMEGA)
=======================================================

>> 1. 节点基础信息 (IDENTITY)
▸ 代号：__NAME__ (__GENDER__)
▸ 哈希：0x__HASH__

>> 2. 底层源代码 (SOURCE CODE)
▸ __Y__ (年/OS) | __M__ (月/OS) | __D__ (日/CORE) | __T__ (时/OS)

>> 3. 核心元神 (DAY MASTER)
▸ 核心：__DM_KEY__ (__EL__属性)
▸ 定位：__ROLE__
▸ MBTI：[ __MBTI__ ]
▸ 特质：__DESC__
▸ 评级：__TIER__
▸ 武器：__WPN__
▸ 义体：__IMP__

>> 4. 演化与补丁 (EVOLUTION & PATCH)
▸ 终极化神：__ULT__
▸ 演化路径：__E0__ -> __E1__ -> __E2__
▸ 致命漏洞：__FLAW__
▸ 系统补丁：__PATCH__

>> 5. 前世业力与驻留进程 (LORE & DAEMONS)
▸ 前世残存：__PL_TITLE__ (债务: __PL_DEBT__)
▸ 预装神煞：__DAEMONS__

>> 6. 算力负载分布 (WUXING METRICS)
▸ 金(裁决): __WX_J__%  |  木(架构): __WX_M__%
▸ 水(流动): __WX_S__%  |  火(算力): __WX_H__%
▸ 土(承载): __WX_T__%

=======================================================
POWERED BY LUNAR DESTINY ENGINE | © __CPY__
======================================================="""
        dossier = TXT_TEMP.replace("__NAME__", str(d.get('name', 'GHOST'))).replace("__GENDER__", str(d.get('gender', 'X'))).replace("__HASH__", str(hash_id))
        dossier = dossier.replace("__Y__", str(bz[0])).replace("__M__", str(bz[1])).replace("__D__", str(bz[2])).replace("__T__", str(bz[3]))
        dossier = dossier.replace("__DM_KEY__", str(dm_key)).replace("__EL__", str(dm_info.get('element', ''))).replace("__ROLE__", str(dm_role)).replace("__MBTI__", str(dm_mbti))
        dossier = dossier.replace("__DESC__", str(dm_desc)).replace("__TIER__", str(dm_tier)).replace("__WPN__", str(dm_wpn)).replace("__IMP__", str(dm_imp))
        dossier = dossier.replace("__ULT__", str(dm_ult)).replace("__E0__", str(dm_evo[0])).replace("__E1__", str(dm_evo[1])).replace("__E2__", str(dm_evo[2]))
        dossier = dossier.replace("__FLAW__", str(dm_flaw)).replace("__PATCH__", str(dm_patch))
        dossier = dossier.replace("__PL_TITLE__", str(past_life['title'])).replace("__PL_DEBT__", str(past_life['debt'])).replace("__DAEMONS__", ', '.join(daemons_list))
        dossier = dossier.replace("__WX_J__", str(wx_scores.get('金',0))).replace("__WX_M__", str(wx_scores.get('木',0))).replace("__WX_S__", str(wx_scores.get('水',0))).replace("__WX_H__", str(wx_scores.get('火',0))).replace("__WX_T__", str(wx_scores.get('土',0)))
        dossier = dossier.replace("__CPY__", str(COPYRIGHT))
        
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(dossier, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(label="📥 下载深度绝密档案 (.txt)", data=dossier, file_name=f"KARMA_{d.get('name', 'GHOST')}.txt", mime="text/plain", use_container_width=True)

    with t_json:
        render_html("<div style='font-size:13px; color:#aaa; margin-top:10px; margin-bottom:15px;'>极客视角：导出您的先天八字 JSON 结构树底包。</div>")
        export_data = {
            "version": VERSION, "node": str(d.get('name', 'GHOST')), "bazi": [str(x) for x in bz],
            "day_master": { "element": dm_key, "role": dm_role, "mbti": dm_mbti, "tier": dm_tier, "evolution": dm_ult, "vulnerability": dm_flaw, "patch": dm_patch, "weapon": dm_wpn },
            "lore": {"past_life": past_life, "daemons": daemons_list},
            "wuxing": wx_scores, "skills": skills_list, "hash": hash_id
        }
        st.download_button(label="📥 提取原始 JSON 底包", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"DATA_{hash_id[:6]}.json", mime="application/json", use_container_width=True)
        
    with t_asc:
        render_html("<div style='font-size:13px; color:var(--green); margin-top:10px; margin-bottom:10px; font-family:Fira Code;'>> 纯正极客浪漫。一键复制下方代码块发送至微信/Discord，绝不乱码。</div>")
        def m_b(v): return "█" * int(v/100*16) + "░" * (16 - int(v/100*16))
        ASC_TEMP = """```text
========================================================
 ███▄    █  ▓█████  ▒█████     █████▒▄▄▄       ██████ 
 ██ ▀█   █  ▓█   ▀ ▒██▒  ██▒ ▓██   ▒▒████▄   ▒██    ▒ 
▓██  ▀█ ██▒ ▒███   ▒██░  ██▒ ▒████ ░▒██  ▀█▄ ░ ▓██▄   
▓██▒  ▐▌██▒ ▒▓█  ▄ ▒██   ██░ ░▓█▒  ░░██▄▄▄▄██  ▒   ██▒
========================================================
> NODE_HANDLE : __NAME__ (__GENDER__)
> AKASHIC_ID  : 0x__HASH__...
--------------------------------------------------------
[ SOURCE CODE / 灵魂底层源码 ]
  __Y__   |   __M__   | >> __D__ << |   __T__

[ CORE ARCHETYPE / 核心机体架构 ]
> DAY_MASTER  : __DM_KEY__ (__EL__ Node)
> ROLE_CLASS  : __ROLE__
> CYBER_MBTI  : [ __MBTI__ ]

[ WUXING PAYLOAD / 算力负载均衡 ]
  STR(金) : __WX_J__% |__B_J__|
  AGI(木) : __WX_M__% |__B_M__|
  INT(水) : __WX_S__% |__B_S__|
  CHA(火) : __WX_H__% |__B_H__|
  CON(土) : __WX_T__% |__B_T__|
========================================================
```"""
        ascii_res = ASC_TEMP.replace("__NAME__", str(d.get('name', 'GHOST'))).replace("__GENDER__", str(d.get('gender', 'UNK'))).replace("__HASH__", str(hash_id[:16]))
        ascii_res = ascii_res.replace("__Y__", str(bz[0])).replace("__M__", str(bz[1])).replace("__D__", str(bz[2])).replace("__T__", str(bz[3]))
        ascii_res = ascii_res.replace("__DM_KEY__", str(dm_key)).replace("__EL__", str(dm_info.get('element', 'UNK'))).replace("__ROLE__", str(dm_role.split('/')[0])).replace("__MBTI__", str(dm_mbti))
        ascii_res = ascii_res.replace("__WX_J__", f"{wx_scores.get('金',0):02d}").replace("__B_J__", m_b(wx_scores.get('金',0)))
        ascii_res = ascii_res.replace("__WX_M__", f"{wx_scores.get('木',0):02d}").replace("__B_M__", m_b(wx_scores.get('木',0)))
        ascii_res = ascii_res.replace("__WX_S__", f"{wx_scores.get('水',0):02d}").replace("__B_S__", m_b(wx_scores.get('水',0)))
        ascii_res = ascii_res.replace("__WX_H__", f"{wx_scores.get('火',0):02d}").replace("__B_H__", m_b(wx_scores.get('火',0)))
        ascii_res = ascii_res.replace("__WX_T__", f"{wx_scores.get('土',0):02d}").replace("__B_T__", m_b(wx_scores.get('土',0)))
        st.markdown(ascii_res)

    # =========================================================================
    # ⌨️ [ TERMINAL ] 内联黑客终端
    # =========================================================================
    st.markdown("---")
    render_html("<div style='max-width: 650px; margin: 0 auto;'><div class='module-title' style='margin-bottom:15px;'>⌨️ 模块 VI：极客终端</div></div>")
    
    current_logs = st.session_state.get("term_logs", ["> SYS_KERNEL READY. AWAITING COMMAND..."])
    log_html = "<br>".join(current_logs[-6:]) if current_logs else "> AWAITING COMMAND..."
    terminal_ui = "<div style='max-width: 650px; margin: 0 auto; background:rgba(0,0,0,0.85); border:1px solid #00f3ff; border-left:4px solid #00f3ff; padding:15px; border-radius:4px 4px 0 0; font-family:\"Fira Code\"; color:#00f3ff; font-size:13px; height:180px; display:flex; flex-direction:column-reverse; overflow:hidden; box-shadow:inset 0 0 20px rgba(0,243,255,0.1); border-bottom:none; margin-bottom:0;'><div>" + str(log_html) + "<span style=\"animation:blink 1s infinite;\">_</span></div></div>"
    render_html(terminal_ui)

    with st.form("inline_terminal", clear_on_submit=True, border=False):
        col_t1, col_t2 = st.columns([5, 1])
        with col_t1:
            cmd_input = st.text_input("CMD", label_visibility="collapsed", placeholder="> 输入终端指令按回车 (如: /help, /ping)...")
        with col_t2:
            sub_cmd = st.form_submit_button("⏎", use_container_width=True)
            
        if sub_cmd and cmd_input:
            cmd_str = str(cmd_input).strip()
            logs = st.session_state.get("term_logs", ["> SYS_KERNEL READY. AWAITING COMMAND..."])
            logs.append("<span style='color:#fff;'>> " + cmd_str + "</span>")
            
            cmd_lower = cmd_str.lower()
            if cmd_lower == '/help': logs.append("[SYS] CMDS: /sudo, /clear, /matrix, /ping")
            elif cmd_lower == '/sudo': logs.append("<span style='color:var(--pink);'>[ERR] ACCESS DENIED. 凡人无法黑入天命。</span>")
            elif cmd_lower == '/matrix': logs.append("<span style='color:var(--green);'>[MSG] WAKE UP, NEO. THE MATRIX HAS YOU.</span>")
            elif cmd_lower == '/ping': logs.append("<span style='color:var(--yellow);'>[PONG] 赛博佛祖延迟 0.00ms. 「色即是空，Bug即是空。」</span>")
            elif cmd_lower == '/clear': logs = ["> TERMINAL CLEARED."]
            else: logs.append("<span style='color:var(--yellow);'>[ERR] UNKNOWN COMMAND: " + cmd_str + "</span>")
            
            st.session_state["term_logs"] = logs
            st.rerun()

    # 底部重启按钮
    render_html("<br><br>")
    col_b_l, col_b_m, col_b_r = st.columns([1,2,1])
    with col_b_m:
        if st.button("⏏ 物理拔除网线并重启终端 (SYS_REBOOT)", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================================================================
# 🛑 [ KERNEL 07 ] 赛博版权区
# =========================================================================
render_html('<div style="text-align:center; margin-top:30px; position:relative; z-index:10; border-top: 1px dashed #222; padding-top: 40px;">' +
    '<div style="color:var(--primary); font-family:\'Orbitron\', monospace; font-size:11px; opacity:0.5; letter-spacing:6px; margin-bottom:8px;">版权归属：无名逆流</div>' +
    '<div style="display:inline-block; padding:10px 30px; border-radius:50px; font-size:13px; font-family:\'Orbitron\'; letter-spacing:2px; color:var(--primary); font-weight:bold; background:rgba(0,243,255,0.05); border:1px solid rgba(0,243,255,0.3); box-shadow:0 0 15px rgba(0,243,255,0.1);">© 2026 ' + str(COPYRIGHT) + '</div>' +
'</div>')



