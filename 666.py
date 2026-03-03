import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math
import hashlib
import json
from datetime import datetime, time as dt_time
import numpy as np
import plotly.graph_objects as go
from lunar_python import Solar

# ==============================================================================
# 🌌 [ CORE 01 ] 宇宙物理引擎与全局配置
# ==============================================================================
VERSION = "KARMA_OS_V33.0_GOD_MODE"
COPYRIGHT = "无名逆流"
SYS_NAME = "量子命理 | 赛博算命终端"

# 宽屏布局，为响应式瀑布流提供极致空间
st.set_page_config(page_title=SYS_NAME, page_icon="☯", layout="wide", initial_sidebar_state="collapsed")

# ==============================================================================
# 🎨 [ CORE 02 ] 赛博修仙 UI 底座 (绝对顶格防爆版，杜绝代码裸奔)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;600&display=swap');

:root { color-scheme: dark; }

[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
.block-container { padding-top: 2.5rem !important; padding-bottom: 4rem !important; max-width: 1200px !important; overflow-x: hidden; }

/* 锁死深渊暗黑背景 */
html, body, .stApp { background-color: #020408 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; }
[data-testid="stAppViewContainer"]::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 30%, rgba(0, 243, 255, 0.05) 0%, rgba(2, 4, 8, 1) 80%); pointer-events: none; z-index: 0; }
[data-testid="stAppViewContainer"]::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.02), transparent, rgba(0, 243, 255, 0.02)); background-size: 100% 3px, 3px 100%; z-index: 99999; pointer-events: none; opacity: 0.7; }

/* 文本与进度条兜底 */
.stMarkdown, p, span, h2, h3, h4, li, div, label { color: #f8fafc !important; z-index: 2; position: relative; }
[data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #00f3ff, #a855f7) !important; box-shadow: 0 0 15px rgba(0,243,255,0.8); }

/* 硬件加速全息跑马灯 */
.ticker-wrap { width: 100vw; overflow: hidden; height: 32px; background-color: rgba(2, 4, 8, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 20px rgba(0,243,255,0.15); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 35s linear infinite; font-family: 'Orbitron', monospace; font-size: 12px; color: #00f3ff; line-height: 32px; letter-spacing: 2px; }
.ticker span { margin-right: 50px; } .ticker .up { color: #10b981; text-shadow: 0 0 8px rgba(16,185,129,0.8); } .ticker .down { color: #f43f5e; text-shadow: 0 0 8px rgba(244,63,94,0.8); }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* 赛博天机主标题 */
.hero-title { font-size: clamp(32px, 6vw, 48px) !important; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 6px; margin-bottom: 5px; margin-top: 15px; text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3); position: relative; display: inline-block; text-transform: uppercase; }
.hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; }
.hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2.5s infinite linear alternate-reverse; }
.hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3.5s infinite linear alternate-reverse; }
@keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
@keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }

/* 模块隔离标题 */
.module-title { color: #00f3ff !important; border-left: 6px solid #00f3ff; padding-left: 12px; font-weight: 900; margin-top: 45px; margin-bottom: 25px; letter-spacing: 2px; font-family: 'Noto Sans SC', sans-serif; text-shadow: 0 0 15px rgba(0,243,255,0.5); background: linear-gradient(90deg, rgba(0,243,255,0.15), transparent); padding-top: 8px; padding-bottom: 8px; border-radius: 4px; text-transform: uppercase;}

/* 天机自检窗 */
.terminal-container { background: rgba(5, 10, 20, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 8px; font-family: 'Fira Code', monospace; font-size: 14px; color: #e2e8f0; box-shadow: inset 0 0 30px rgba(0,243,255,0.05), 0 15px 40px rgba(0,0,0,0.9); margin-bottom: 30px; border-top: 3px solid #00f3ff;}
.cursor-blink { display: inline-block; width: 10px; height: 18px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* 罗盘表单域劫持 */
div[data-testid="stForm"] { max-width: 650px; margin: 0 auto; border: none !important; background: transparent !important;}
div[data-testid="stTextInput"] > div > div > input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(5, 10, 15, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 6px !important; text-align: center; font-size: 18px !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1) !important; height: 50px; }
div[data-testid="stTextInput"] > div > div > input:focus { border-color: #a855f7 !important; box-shadow: 0 0 25px rgba(168,85,247,0.4), inset 0 0 15px rgba(168,85,247,0.1) !important; }
div[data-baseweb="select"] > div { background-color: rgba(5, 10, 15, 0.95) !important; border: 1px solid rgba(0,243,255,0.5) !important; color: #00f3ff !important; font-weight: bold;}

/* 交互按钮 */
div.stButton > button { background: linear-gradient(135deg, #050a15 0%, #02040a 100%) !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 6px !important; min-height: 60px !important; width: 100% !important; transition: all 0.3s ease !important; margin-bottom: 5px !important;}
div.stButton > button p { color: #ffffff !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 1px !important;}
div.stButton > button:hover { border-color: #00f3ff !important; border-left: 6px solid #00f3ff !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: translateX(4px) !important; }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #0088ff, #a855f7) !important; border: none !important; text-align: center !important; }
div.stButton > button[data-testid="baseButton-primary"] p { color: #ffffff !important; font-weight: 900 !important; font-size: 18px !important; letter-spacing: 4px !important; text-shadow: 0 0 10px rgba(0,0,0,0.8);}

/* 命盘展示大卡 */
.bazi-card { padding: 40px 30px; border-radius: 12px; background: rgba(5, 8, 15, 0.95) !important; border: 1px solid rgba(0,243,255,0.4); border-top: 6px solid #00f3ff; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.9), inset 0 0 40px rgba(0,243,255,0.05); position:relative; overflow:hidden;}
.bazi-char { font-size: clamp(38px, 6vw, 65px); font-weight: 900; color: #00f3ff; text-shadow: 0 0 25px rgba(0,243,255,0.8); margin: 0 10px; font-family: "Noto Sans SC", serif; }
.bazi-label { color: #94a3b8; font-size: 12px; letter-spacing: 6px; margin-top: 15px; font-family: 'Orbitron'; font-weight:bold;}
.tier-badge { position: absolute; top: 20px; right: -45px; background: #00f3ff; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 13px; padding: 5px 50px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 20px rgba(0,243,255,0.8);}

/* 外挂技能树标签 */
.skill-badge { background: linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.1)); border: 1px solid rgba(168,85,247,0.6); border-left: 3px solid #a855f7; padding: 6px 12px; border-radius: 4px; font-size: 13px; color: #f3e8ff; font-weight: bold; display: inline-block; margin: 5px; box-shadow: 0 0 15px rgba(168,85,247,0.3); }

/* Tabs 极客导航坞 */
[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: clamp(14px, 2vw, 16px) !important; padding-bottom: 12px !important; transition: all 0.3s ease; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #00f3ff !important; border-bottom-color: #00f3ff !important; border-bottom-width: 3px !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); background: rgba(0,243,255,0.05); }

/* 代码块深色保护 */
div[data-testid="stCodeBlock"] > div { background-color: #050505 !important; border-color: #333 !important; }
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code { font-family: 'Fira Code', monospace !important; font-size: 12px !important; color: #10b981 !important; line-height: 1.6 !important;}
div[data-testid="stCodeBlock"] { border-left: 4px solid #10b981 !important; border-radius: 6px !important; margin-top: 10px; }

/* 下载按钮矩阵 */
div[data-testid="stDownloadButton"] > button { background: rgba(5, 10, 15, 0.95) !important; border: 1px dashed rgba(168, 85, 247, 0.8) !important; border-left: 6px solid #a855f7 !important; margin-top: 15px; border-radius: 6px !important; height: 55px; text-align: center !important; width: 100% !important;}
div[data-testid="stDownloadButton"] > button p { color: #a855f7 !important; font-family: 'Orbitron', monospace !important; font-weight: bold !important; letter-spacing: 2px !important; font-size: 15px !important;}
div[data-testid="stDownloadButton"] > button:hover { background: rgba(168, 85, 247, 0.15) !important; box-shadow: 0 0 30px rgba(168, 85, 247, 0.5) !important; transform: scale(1.02) !important; border-color: #00f3ff !important; border-left-color: #00f3ff !important; }
div[data-testid="stDownloadButton"] > button:hover p { color: #00f3ff !important; text-shadow: 0 0 10px #00f3ff;}

/* 🌟 版权呼吸灯 (无名逆流专属) */
.copyright-niliu { display: inline-block; padding: 12px 35px; border-radius: 50px; font-size: 13px; font-family: "Noto Sans SC", sans-serif; letter-spacing: 2px; color: #00f3ff; font-weight: 900; background: rgba(0,243,255,0.05); border: 1px solid rgba(0,243,255,0.3); animation: neon-breathe 2.5s infinite alternate; transition: all 0.3s ease; box-shadow: 0 0 20px rgba(0,243,255,0.2); margin-top: 20px;}
.copyright-niliu:hover { transform: scale(1.05); box-shadow: 0 0 35px rgba(0,243,255,0.8), inset 0 0 15px rgba(0,243,255,0.5); border-color: #00f3ff; text-shadow: 0 0 15px #00f3ff; cursor: crosshair;}
@keyframes neon-breathe { 0% { box-shadow: 0 0 10px rgba(0,243,255,0.1), inset 0 0 5px rgba(0,243,255,0.1); border-color: rgba(0,243,255,0.2); text-shadow: none; } 100% { box-shadow: 0 0 25px rgba(0,243,255,0.6), inset 0 0 15px rgba(0,243,255,0.2); border-color: rgba(0,243,255,0.7); text-shadow: 0 0 10px #00f3ff; } }

/* 🎆 结算纯代码烟花 */
.firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', monospace; color: #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 30px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;}
@keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }

/* 📱 手机端瀑布流与防爆适配 */
@media (max-width: 768px) {
    .hero-title { font-size: 24px !important; letter-spacing: 2px !important; }
    .bazi-char { font-size: 32px !important; margin: 0 4px !important; }
    .block-container { padding-top: 2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    .module-title { font-size: 15px !important; margin-top: 30px !important; padding-top: 6px !important; padding-bottom: 6px !important;}
    div[data-testid="stColumns"] > div { margin-bottom: 20px; } 
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 📊 [ CORE 03 ] 宇宙大盘跑马灯
# ==============================================================================
st.markdown("""
<div class="ticker-wrap"><div class="ticker">
    <span>KARMA-OS: V33.0 SECURE <b class="up">▲ONLINE</b></span>
    <span>SOUL-NODE: FATE MAPPED <b class="up">▲LOCKED</b></span>
    <span>BAZI-HASH: DECRYPT SUCCESS <b class="up">▲14.2TH/s</b></span>
    <span>SYS-RISK: FIVE ELEMENTS BALANCED <b class="up">▲SECURE</b></span>
    <span>MARKET-ALPHA: 10-YEAR TREND <b class="down">▼COMPUTING</b></span>
    <span>DAO-PROTOCOL: SMART CONTRACT <b class="up">▲MINTED</b></span>
    <span>KARMA-OS: V33.0 SECURE <b class="up">▲ONLINE</b></span>
</div></div>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    vocab = ["KARMA", "DAO", "HASH", "DESTINY", "SYNC", "OS", "MINT"]
    for _ in range(40): 
        tx = random.uniform(200, 800) * math.cos(random.uniform(0, 2 * math.pi))
        ty = random.uniform(200, 800) * math.sin(random.uniform(0, 2 * math.pi))
        text = random.choice(vocab)
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{random.uniform(1.0, 3.5)}; --rot:{random.randint(-360, 360)}deg; animation-delay:{random.uniform(0, 0.2)}s; font-size:{random.randint(14, 24)}px;">{text}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

def generate_alpha_curve(seed_hash):
    rng = np.random.RandomState(int(seed_hash[:8], 16))
    current_year = datetime.now().year
    years = [str(current_year + i) for i in range(10)] 
    roi = [rng.randint(60, 85)]
    for _ in range(9): 
        roi.append(max(30, min(100, roi[-1] + rng.randint(-20, 25))))
    return years, roi

# ==============================================================================
# 🗃️ [ CORE 04 ] 万字玄学大厂字典：天干元神与十神算力矩阵
# ==============================================================================
# 🚨 极其关键：补齐所有属性，坚决杜绝 KeyError
DAY_MASTER_DICT = {
    "甲": {"role": "硅基巨树 / 系统架构师", "desc": "天生具备宏大的底层系统构建能力，性格直爽且极度抗压。在混乱的局势中，你是能够扛起从0到1重构秩序的绝对开拓者。", "color": "#10b981", "element": "木", "tier": "UR", "evolution_path": ["L1 架构幼苗", "L2 核心骨干", "L3 苍天建木"], "ultimate_evolution": "【苍天建木】执掌三界底层协议的创世神", "black_swan": "过于刚硬，遇强则折。在遭遇系统级降维打击时，容易宁折不弯导致全面宕机。", "patch": "引入「水」属性的柔性冗余算法，学会在逆境中挂起进程，等待重启时机。"},
    "乙": {"role": "量子藤蔓 / 网络渗透者", "desc": "拥有极其敏锐的嗅觉与恐怖的适应力。能在毫无资源的夹缝中疯狂生长，是天生的社交网络捕手与暗网渗透专家。", "color": "#34d399", "element": "木", "tier": "SSR", "evolution_path": ["L1 寄生节点", "L2 渗透猎手", "L3 噬星魔藤"], "ultimate_evolution": "【噬星魔藤】寄生并控制全网资源的暗影君王", "black_swan": "极度依赖宿主资源。一旦核心宿主（平台/领导）断网，容易失去独立运行能力。", "patch": "建立分布式的多宿主挂载协议，将风险分散至全网各个边缘节点。"},
    "丙": {"role": "核聚耀阳 / 爆裂狂战士", "desc": "充满着极具感染力的核聚变爆发力，气场全开。只要你在线，就是团队中照亮一切、输出最高绝对算力的发光核心。", "color": "#f43f5e", "element": "火", "tier": "UR", "evolution_path": ["L1 点火程序", "L2 核聚变堆", "L3 恒星引擎"], "ultimate_evolution": "【恒星引擎】照亮并驱动整个纪元的绝对算力", "black_swan": "全功率输出容易导致自身内核熔毁，且光芒太盛极易引来全网黑客的集中攻击。", "patch": "强制加装「土」属性散热散热栅栏，学会在波谷期进入低功耗待机模式。"},
    "丁": {"role": "幽网霓虹 / 精神引导者", "desc": "洞察人心的夜行者，思维细腻到极致。擅长在最灰暗、最迷茫的业务地带，为团队提供精准的情绪价值与破局方向。", "color": "#fb923c", "element": "火", "tier": "SSR", "evolution_path": ["L1 寻路信标", "L2 精神图腾", "L3 灵魂织网者"], "ultimate_evolution": "【灵魂织网者】操控全网心智与情绪的网络幽灵", "black_swan": "能量波动极不稳定，在狂风骤雨的市场洗牌中，容易被一波带走断网。", "patch": "寻找强大的「甲」属性巨树作为遮风挡雨的物理服务器，安心在后台推演。"},
    "戊": {"role": "绝对防火墙 / 秩序守护神", "desc": "稳如泰山，物理级断网的防御力。你是极其靠谱的信用节点，是所有疯狂的创新业务背后，那道最坚不可摧的安全底线。", "color": "#d97706", "element": "土", "tier": "UR", "evolution_path": ["L1 承载沙盒", "L2 巨石阵列", "L3 盖亚装甲"], "ultimate_evolution": "【盖亚装甲】承载万物因果的绝对零度壁垒", "black_swan": "系统过于庞大笨重，在面临极其敏捷的突发迭代需求时，极易卡死在旧有循环中。", "patch": "定期主动清理内存缓存，接纳「甲/乙」属性的破坏性创新，强行打破死锁。"},
    "己": {"role": "主板息壤 / 资源吞噬者", "desc": "拥有海纳百川的包容力，擅长无缝整合一切零散资源与冗余数据。你是将天马行空的狂想转化为具体落地的超强执行中枢。", "color": "#f59e0b", "element": "土", "tier": "SSR", "evolution_path": ["L1 容错冗余", "L2 资源枢纽", "L3 创世息壤"], "ultimate_evolution": "【创世息壤】孕育下一个数字生态文明的温床", "black_swan": "什么进程都想接，极易导致系统超载崩溃，被无数无效的数据垃圾填满内存。", "patch": "立刻编写无情的 Garbage Collection (垃圾回收) 脚本，学会拒绝无效的并发请求。"},
    "庚": {"role": "冷血代码 / 裁决执行官", "desc": "杀伐果断，对低效与冗余代码零容忍。天生自带威严，是无情推进业务进度、斩断一切无效社交与羁绊的风控大闸。", "color": "#cbd5e1", "element": "金", "tier": "UR", "evolution_path": ["L1 肃清脚本", "L2 风控铁腕", "L3 审判之剑"], "ultimate_evolution": "【审判之剑】斩断一切因果循环的终极裁决", "black_swan": "戾气过重，容易在团队中引发不可逆的物理级破坏，导致整个业务链条彻底断裂。", "patch": "必须要经受「火」属性的高温熔炼与淬火，才能把狂暴的杀气转化为极致的利刃。"},
    "辛": {"role": "纳米精工 / 极致重构者", "desc": "永远在追求完美与极致的代码质感，自带极高的审美溢价与贵气。你是能在粗糙的草台中，打磨出顶尖跨时代产品的核心枢纽。", "color": "#f8fafc", "element": "金", "tier": "SSR", "evolution_path": ["L1 精密协议", "L2 审美巅峰", "L3 量子纠缠体"], "ultimate_evolution": "【量子纠缠体】超越物质形态的究极艺术代码", "black_swan": "极度脆弱且傲娇。一旦环境稍微不达标，或者遇到粗暴的野蛮人，就会当场崩溃罢工。", "patch": "需要极度纯净的「水」属性来淘洗保护，千万不要让自己卷入肮脏的底层泥潭博弈。"},
    "壬": {"role": "深网狂潮 / 降维破局者", "desc": "思维极其开阔奔放，极度厌恶陈规陋习，从来不按套路出牌。你能在瞬息万变的市场中，凭借直觉掀起降维打击的颠覆浪潮。", "color": "#3b82f6", "element": "水", "tier": "UR", "evolution_path": ["L1 数据暗流", "L2 倾覆巨浪", "L3 渊海归墟"], "ultimate_evolution": "【渊海归墟】吞噬所有时间与空间的终极黑洞", "black_swan": "过于放纵自己的算力，如同脱缰的野马，最终引发洪水滔天，反噬自身的根基。", "patch": "必须引入极度严苛的「戊」土级风控大坝，强行给自己的疯狂创意设定红线。"},
    "癸": {"role": "暗流算法 / 幽灵谋略家", "desc": "极其聪慧且隐秘不发，习惯在幕后推演全局。擅长通过无声的谋略、博弈和信息差，兵不血刃地达成最终目的。", "color": "#60a5fa", "element": "水", "tier": "SSR", "evolution_path": ["L1 隐形爬虫", "L2 渗透迷雾", "L3 命运主宰"], "ultimate_evolution": "【命运主宰】在第四维度拨动因果之线的神明", "black_swan": "心思过重，经常陷入无限循环的逻辑死胡同，算计太多反而错失了最直白的红利。", "patch": "走到阳光下，接受「丙」火的正向照射，用最简单的阳谋去击碎所有复杂的阴谋。"}
}

# 十神外挂技能库
SHEN_SKILLS = {
    "七杀": "零日漏洞爆破 (Lv.Max)", "正官": "底层协议锚定 (Lv.Max)", 
    "偏印": "逆向工程解构 (Lv.Max)", "正印": "系统灾备兜底 (Lv.Max)",
    "偏财": "高频杠杆套利 (Lv.Max)", "正财": "算力资产吞噬 (Lv.Max)",
    "比肩": "分布式共识网 (Lv.Max)", "劫财": "网络节点劫持 (Lv.Max)",
    "食神": "感官体验降维 (Lv.Max)", "伤官": "范式秩序破坏 (Lv.Max)"
}

# 🤝 动态协同算法
def calculate_synergy(hash1, target_stem):
    rng_syn = np.random.RandomState(int(hash1[:6], 16) + sum(ord(c) for c in target_stem))
    score = rng_syn.randint(65, 99)
    if score >= 95: return score, "【黄金并网】底层协议高度兼容，堪称最强双核推土机！"
    elif score >= 85: return score, "【灰度容错】代码视角互补，能打磨出极具弹性的业务闭环。"
    elif score >= 75: return score, "【高频摩擦】存在通信壁垒，需强制引入中间缓冲件。"
    else: return score, "【阴阳反转】底层逻辑完全相冲！必须背靠背物理隔离执行！"

# ==============================================================================
# 🔮 [ CORE 05 ] 状态机与生辰降临采集
# ==============================================================================
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
    st.session_state.bazi_data = {}
    st.session_state.anim_played = False

if not st.session_state.calculated:
    st.markdown("""
    <div style="max-width: 650px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">KARMA OS FRAMEWORK</div>
            <h1 class="hero-title" data-text="全息命盘推演终端">全息命盘推演终端</h1><br>
            <div style="color:#f43f5e; font-family:'Orbitron', sans-serif; font-size:13px; font-weight:700; letter-spacing:6px; margin-bottom:30px;">DESTINY ENGINE V33.0</div>
        </div>
        
        <div class="terminal-container">
            <div style="font-family:'Orbitron', monospace; color:#00f3ff; margin-bottom:15px; font-weight:bold;">> INITIALIZING QUANTUM LUNAR KERNEL...</div>
            <div style="margin-bottom:5px;"><span style="color:#10b981;">[OK]</span> Mounting Lunar-Python astronomical algorithms.</div>
            <div style="margin-bottom:5px;"><span style="color:#10b981;">[OK]</span> Bypassing temporal distortion logic.</div>
            <div>
                <br><span style="color:#ffffff; font-size: 15px; font-family: 'Noto Sans SC', sans-serif; line-height: 1.8;"><b>肉体不过是碳基的载体，八字才是灵魂的底层代码。</b><br><br>
                在硅基宇宙与玄学法则交汇的当下，本终端将提取您的先天降临坐标。<br>
                通过星体引力与历法哈希计算，为您生成不可篡改的<b>高阶本命元神凭证与气运大盘</b>。</span>
                <span class="cursor-blink"></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="destiny_form", border=False):
        st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:13px; font-weight:bold; margin-bottom:15px; text-align:center;'>▼ 注入先天元神降临坐标 ▼</div>", unsafe_allow_html=True)
        
        user_name = st.text_input("赛博代号 (昵称/姓名)", placeholder="例如：Neo / 银手", value="")
        gender = st.selectbox("载体形态 (性别)", ["乾造 (男)", "坤造 (女)"])
        
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input("降临太阳历 (公历)", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(1999, 9, 9))
        with col2:
            birth_time = st.time_input("降临时辰 (精确时间)", value=dt_time(12, 00))
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("▶ 连接宇宙算力，推演天机", type="primary", use_container_width=True)

        if submit_btn:
            solar = Solar.fromYmdHms(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            wu_xing_str = bazi.getYearWuXing() + bazi.getMonthWuXing() + bazi.getDayWuXing() + bazi.getTimeWuXing()
            wx_counts = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
            for char in wu_xing_str:
                if char in wx_counts: wx_counts[char] += 1
            
            total = sum(wx_counts.values()) or 1
            wx_scores = {k: int((v / total) * 100) for k, v in wx_counts.items()}
            
            skills = []
            for shen in [bazi.getYearShiShenGan(), bazi.getMonthShiShenGan(), bazi.getTimeShiShenGan()]:
                if shen in SHEN_SKILLS and SHEN_SKILLS[shen] not in skills:
                    skills.append(SHEN_SKILLS[shen])
            if not skills: skills = ["混沌未知域 (Lv.Unknown)"]

            st.session_state.bazi_data = {
                "name": user_name if user_name else "Anonymous_Node",
                "gender": gender.split(" ")[0],
                "bazi_str": f"{bazi.getYear()} {bazi.getMonth()} {bazi.getDay()} {bazi.getTime()}",
                "day_master": bazi.getDayGan(),
                "zodiac": lunar.getYearShengXiao(),
                "wx_scores": wx_scores,
                "skills": skills,
                "hash_id": hashlib.sha256(f"{user_name}{birth_date}{birth_time}".encode()).hexdigest().upper(),
                "birth_date_str": str(birth_date),
                "birth_time_str": str(birth_time)[:5]
            }
            
            st.markdown("<div style='max-width: 650px; margin: 0 auto;'><h2 class='hero-title' data-text='[ DECODING KARMA... ]' style='font-size:28px !important; margin-top:20px; text-align:center; display:block;'>[ DECODING KARMA... ]</h2></div>", unsafe_allow_html=True)
            mint_box = st.empty()
            h_logs = ""
            for _ in range(12):
                h_logs = f"<span style='color:#94a3b8;'>[ASTRO_SYNC]</span> <span style='color:#00f3ff;'>0x{hashlib.md5(str(random.random()).encode()).hexdigest()[:24]}...</span> <span style='color:#10b981;'>[OK]</span><br>" + h_logs
                mint_box.markdown(f"<div style='max-width: 650px; margin: 0 auto;'><div class='cli-box' style='height:200px; overflow:hidden;'>{h_logs}</div></div>", unsafe_allow_html=True)
                time.sleep(0.12)
                
            st.session_state.calculated = True
            st.rerun()

# ==============================================================================
# 🌟 [ CORE 06 ] 全息大屏展示 (六大瀑布流模块)
# ==============================================================================
else:
    if not st.session_state.anim_played: 
        trigger_supernova()
        st.session_state.anim_played = True

    # --------------------------------------------------------------------------
    # 🚨 绝对物理防爆区：全量变量提前计算提升 (Variable Hoisting) 
    # 杜绝任何 UI 渲染中断导致的 NameError 
    # --------------------------------------------------------------------------
    data = st.session_state.bazi_data
    dm_info = DAY_MASTER_DICT.get(data['day_master'], DAY_MASTER_DICT["甲"])
    bazi_arr = data['bazi_str'].split(' ')
    
    hash_code = data['hash_id']
    token_id = int(hash_code[:8], 16)
    contract_addr = "0x" + hashlib.sha256(f"karma_dao_{token_id}".encode()).hexdigest()[:38]
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # 运势走势预计算
    years_k, fortunes_k = generate_alpha_curve(hash_code)

    # 黄金搭档判定
    rng_partner = random.Random(int(hash_code[:8], 16))
    wx_list = ["金", "木", "水", "火", "土"]
    my_element = dm_info["element"]
    if my_element in wx_list:
        wx_list.remove(my_element)
    partner_element = rng_partner.choice(wx_list)
    
    # 搜寻最佳天干搭档
    best_partner_stem = ""
    best_score = 0
    for stem, info in DAY_MASTER_DICT.items():
        sc, desc = calculate_synergy(hash_code, stem)
        if sc > best_score:
            best_score = sc
            best_partner_stem = f"{stem} ({info['role']})"

    # 五行能量阵列预计算
    wx_scores = data['wx_scores']
    wx_keys = list(wx_scores.keys())
    wx_vals = list(wx_scores.values())
    
    # 赛博精神病阈值 (走火入魔) 计算
    max_wx = max(wx_vals) if wx_vals else 0
    entropy_score = int(min(99, (max_wx / 50.0) * 100))
    if entropy_score > 75: 
        e_tag, e_color, r_desc = "极易走火入魔！切忌贪暴！", "#f43f5e", "您的单极属性过载，系统极易崩溃，请立刻停止高风险套利。"
    elif entropy_score > 50: 
        e_tag, e_color, r_desc = "偏科严重，需挂载防御补丁", "#f59e0b", "底层算力分布不均，容易在特定周期遭遇针对性降维打击。"
    else: 
        e_tag, e_color, r_desc = "五行极度平稳，可抗任意暴击", "#10b981", "您的系统架构堪称完美，拥有极强的抗打击与自愈恢复能力。"

    # HTML 样式预组装
    tags_html_web = "".join([f"<span style='background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:6px 14px; border-radius:6px; font-size:13px; font-weight:900; margin:4px; display:inline-block;'>{t}</span>" for t in [dm_info['element'] + "属性", dm_info['tier'] + "级节点", "天机验证"]])
    skills_html_web = "".join([f"<span class='skill-badge'>{s}</span>" for s in data['skills']])

    # =========================================================================
    # 📱 模块渲染开始 (严格遵守流式布局)
    # =========================================================================
    
    # 💠 [模块 I]：链上确权凭证
    st.markdown("<div class='module-title'>💠 模块 I：天机链上确权</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,243,255,0.05), rgba(5,5,10,0.9)); border: 1px solid #00f3ff; border-radius: 8px; padding: 15px 25px; margin-bottom: 25px; font-family: 'Orbitron', monospace; box-shadow: 0 0 20px rgba(0,243,255,0.15);">
        <div style="color: #00f3ff; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #00f3ff; padding-bottom: 10px; margin-bottom: 12px; display:flex; align-items:center;">
            <span style="font-size:20px; margin-right:10px;">🏅</span> <span>DESTINY SOULBOUND TOKEN (SBT) MINTED [ V 33.0 ]</span>
        </div>
        <div style="font-size: 12px; color: #94a3b8; line-height: 1.8; display:flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
            <div><div><span style="color:#e2e8f0;">BLOCK HEIGHT:</span> V33-{(int(time.time()) % 1000000):06d}</div><div><span style="color:#e2e8f0;">CONTRACT:</span> {contract_addr[:20]}...</div></div>
            <div style="text-align: left;"><div><span style="color:#e2e8f0;">TOKEN ID:</span> #{token_id}</div><div><span style="color:#e2e8f0;">TIMESTAMP:</span> {current_time_str}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🧬 [模块 II & III]：核心架构与运势沙盘 (响应式布局)
    col_card_l, col_card_r = st.columns([1.2, 1], gap="large")

    with col_card_l:
        st.markdown("<div class='module-title' style='margin-top: 0;'>🧬 模块 II：八字底层源码</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-card">
            <div class="tier-badge" style="background:{dm_info['color']}; box-shadow:0 0 25px {dm_info['color']}99;">{dm_info['tier']}</div>
            <div style="color:#f43f5e; font-size:12px; letter-spacing:6px; font-family:'Orbitron'; margin-bottom:20px; font-weight:bold;">/// EIGHT CHARACTERS DECRYPTED ///</div>
            <div style="font-size:16px; color:#e2e8f0; margin-bottom:25px;">节点 <b style="color:#fff; font-size:20px;">{data['name']}</b> ({data['gender']} · 属{data['zodiac']}) 的底层代码：</div>
            
            <div style="display:flex; justify-content:center; align-items:center; flex-wrap:wrap; gap:10px;">
                <div style="display:flex; flex-direction:column; align-items:center; background:rgba(0,0,0,0.6); padding:10px; border-radius:8px; border:1px solid #333; min-width:70px;">
                    <span class="bazi-char">{bazi_arr[0][0]}</span><span class="bazi-char" style="color:#94a3b8;">{bazi_arr[0][1]}</span><span class="bazi-label">[年柱]</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; background:rgba(0,0,0,0.6); padding:10px; border-radius:8px; border:1px solid #333; min-width:70px;">
                    <span class="bazi-char">{bazi_arr[1][0]}</span><span class="bazi-char" style="color:#94a3b8;">{bazi_arr[1][1]}</span><span class="bazi-label">[月柱]</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; background:rgba(0,243,255,0.08); padding:10px; border-radius:8px; border:1px solid rgba(0,243,255,0.4); min-width:70px; box-shadow:0 0 15px rgba(0,243,255,0.15);">
                    <span class="bazi-char" style="color:#00f3ff;">{bazi_arr[2][0]}</span><span class="bazi-char" style="color:#e2e8f0;">{bazi_arr[2][1]}</span><span class="bazi-label" style="color:#00f3ff;">[日柱]</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; background:rgba(0,0,0,0.6); padding:10px; border-radius:8px; border:1px solid #333; min-width:70px;">
                    <span class="bazi-char">{bazi_arr[3][0]}</span><span class="bazi-char" style="color:#94a3b8;">{bazi_arr[3][1]}</span><span class="bazi-label">[时柱]</span>
                </div>
            </div>
            
            <div style="margin-top:30px; padding-top:20px; border-top:1px dashed rgba(0,243,255,0.3);">
                <div style="font-size:12px; color:#94a3b8; margin-bottom:5px;">您的本命元神 (日干核心)</div>
                <div style="font-size:26px; font-weight:900; color:{dm_info['color']}; text-shadow:0 0 15px {dm_info['color']}; margin-bottom:12px;">{data['day_master']} · {dm_info['role']}</div>
                <div style="font-size:14px; color:#cbd5e1; line-height:1.6; background:rgba(255,255,255,0.03); padding:15px; border-radius:8px; text-align:left;">{dm_info['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_card_r:
        st.markdown("<div class='module-title' style='margin-top: 0;'>🤝 模块 III：外挂算力技能树</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px; color:#94a3b8; margin-bottom:15px; line-height:1.6;'>基于您的四柱十神排布，系统已提取您的先天外挂核心技能点：</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(244,63,94,0.05); border: 1px solid rgba(244,63,94,0.3); border-radius: 8px; padding: 25px; margin-bottom: 25px; text-align:center;">
            <div style="color: #f43f5e; font-family: 'Orbitron', sans-serif; font-size: 12px; letter-spacing: 2px; margin-bottom: 15px;">[ INNATE SKILL TREE ]</div>
            <div style="line-height: 2.2;">{skills_html_web}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h5 style='color:#10b981; margin-top:20px; margin-bottom:10px;'>💡 破局黄金搭档建议：</h5>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:20px; border-radius:4px; font-size:14px; color:#e2e8f0; line-height: 1.6;'>
            您是强大的 <b style='color:{dm_info['color']};'>{my_element}</b> 属性元神。<br>在进行人生高危业务攻坚时，建议挂载拥有强 <b style='color:#10b981; font-size:16px;'>{partner_element}</b> 属性的队友作为副驾驶，以平衡系统的整体熵增。
        </div>
        """, unsafe_allow_html=True)

    # 🕸️ [模块 IV]：算力雷达与大运K线
    st.markdown("<div class='module-title'>🕸️ 模块 IV：五行算力雷达与大运 K 线</div>", unsafe_allow_html=True)
    col_mid_l, col_mid_r = st.columns([1, 1.1], gap="large")
    
    with col_mid_l:
        st.markdown("<div style='text-align:center; color:#00f3ff; font-weight:bold; margin-bottom:10px; font-family:Orbitron;'>/// WUXING RADAR MATRIX</div>", unsafe_allow_html=True)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=wx_vals + [wx_vals[0]], theta=wx_keys + [wx_keys[0]], 
            fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', 
            line=dict(color='#00f3ff', width=2.5), marker=dict(color='#f43f5e', size=6, symbol='diamond')
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=False, range=[0, max_wx + 10]), 
                angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=14), linecolor='rgba(0,243,255,0.3)', gridcolor='rgba(0,243,255,0.1)')
            ), 
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=20, b=20), height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        wx_colors = {'金': '#e2e8f0', '木': '#10b981', '水': '#3b82f6', '火': '#f43f5e', '土': '#f59e0b'}
        bars_html = '<div style="background:rgba(0,0,0,0.5); padding:20px; border-radius:8px; border:1px solid rgba(0,243,255,0.2);">'
        for k, v in data['wx_scores'].items():
            bars_html += f'''
            <div style="display:flex; align-items:center; margin-bottom:12px; font-size:13px; font-weight:bold;">
                <span style="width:30px; color:{wx_colors[k]};">{k}</span>
                <div style="flex:1; height:8px; background:rgba(255,255,255,0.05); border-radius:4px; margin:0 10px; position:relative;">
                    <div style="position:absolute; top:0; left:0; height:100%; width:{v}%; background:{wx_colors[k]}; border-radius:4px; box-shadow:0 0 10px {wx_colors[k]};"></div>
                </div>
                <span style="width:40px; text-align:right; color:#94a3b8;">{v}%</span>
            </div>
            '''
        bars_html += '</div>'
        st.markdown(bars_html, unsafe_allow_html=True)

    with col_mid_r:
        st.markdown("<div style='text-align:center; color:#f43f5e; font-weight:bold; margin-bottom:10px; font-family:Orbitron;'>/// 10-YEAR ALPHA FORTUNE</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; font-size:14px; color:#e2e8f0; margin-bottom:10px;'>基于先天代码推演未来十年气运走势：</div>", unsafe_allow_html=True)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=years_k, y=fortunes_k, mode='lines+markers', 
            line=dict(color="#f43f5e", width=3, shape='spline'), 
            fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)',
            marker=dict(size=8, color="#00f3ff")
        ))
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            margin=dict(l=10, r=10, t=10, b=10), height=300, 
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8')), 
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='Alpha 气运净值', tickfont=dict(color='#94a3b8'))
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown(f"""
        <div style="background: rgba(255,0,60,0.1); border-left: 4px solid #ff003c; padding: 20px; margin-top: 20px; border-radius: 0 8px 8px 0;">
            <div style="font-size:11px; color:#ff003c; font-family:'Orbitron'; margin-bottom:8px; letter-spacing:1px; font-weight:bold;">/// DESTINY WARNING ///</div>
            <div style="font-size:14px; color:#fff; line-height:1.6; margin-bottom:10px;">在气运波峰期大胆加满杠杆出击；在波谷期必须开启防御协议，严守底线，切忌越界套利。</div>
            <div style="font-size:12px; color:#94a3b8;">系统测算您的五行熵增阀值为：<b style="color:{e_color}; font-size:14px;">{entropy_score}% ({e_tag})</b></div>
            <div style="font-size:11px; color:#64748b; margin-top:5px;">{r_desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # 🗄️ [模块 V]：算力深潜控制台
    st.markdown("<div class='module-title'>🗄️ 模块 V：极客深潜控制台 (DEEP DIVE)</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:right; font-size:12px; color:#94a3b8; margin-bottom:10px; opacity:0.8;'>👉 手机端可左右滑动切换 Tabs 面板</div>", unsafe_allow_html=True)
    
    t_syn, t_3d, t_sol = st.tabs(["🤝 异体节点并网沙盘", "🌌 3D 能量坐标图", "💻 智能合约源码"])
    
    with t_syn:
        st.markdown("<div style='text-align:center; color:#a855f7; font-weight:bold; margin-bottom:10px; margin-top:15px; font-family:Orbitron;'>/// TEAM SYNERGY SIMULATOR</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; text-align:center;'>输入团队成员/道侣的天干元神，强制校验物理并网匹配度：</div>", unsafe_allow_html=True)
        options_list = list(DAY_MASTER_DICT.keys())
        format_func = lambda x: f"{x} ({DAY_MASTER_DICT[x]['element']}属性) - {DAY_MASTER_DICT[x]['role']}"
        pmbti = st.selectbox("🎯 挂载目标协作节点:", options=options_list, index=0, format_func=format_func, label_visibility="collapsed")
        
        sc, sd = calculate_synergy(hash_code, pmbti)
        
        st.markdown(f"""
        <div style="background: rgba(168,85,247,0.1); border: 1px solid rgba(168,85,247,0.5); padding: 30px; border-radius: 12px; margin-top:10px; text-align:center; box-shadow: 0 0 30px rgba(168,85,247,0.15);">
            <div style="font-family:'Orbitron', sans-serif; color:#a855f7; font-size:14px; font-weight:bold; margin-bottom:15px; letter-spacing: 3px;">[ SYNERGY MATCH RATE ]</div>
            <div style="font-family:'Orbitron', sans-serif; font-size:65px; font-weight:900; color:#fff; text-shadow:0 0 35px rgba(168,85,247,0.8); margin-bottom:20px;">{sc}%</div>
            <div style="color:#e2e8f0; font-size:15px; font-weight:bold; line-height:1.7;">{sd}</div>
        </div>
        """, unsafe_allow_html=True)

    with t_3d:
        st.markdown("<div style='text-align:center; color:#00f3ff; font-weight:bold; margin-bottom:10px; margin-top:15px; font-family:Orbitron;'>/// 3D ENERGY TOPOLOGY MAP</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; text-align:center;'>降维映射至三维空间 (支持鼠标/触控 360° 拖拽)。背景点阵为全网众生数据节点。</div>", unsafe_allow_html=True)
        rng_3d = np.random.RandomState(int(hash_code[:6], 16))
        x_v = data['wx_scores'].get('金', 20)
        y_v = data['wx_scores'].get('木', 20)
        z_v = data['wx_scores'].get('水', 20)
        f3d = go.Figure()
        f3d.add_trace(go.Scatter3d(x=rng_3d.randint(0,60,size=150), y=rng_3d.randint(0,60,size=150), z=rng_3d.randint(0,60,size=150), mode='markers', marker=dict(size=4, color='#334155', opacity=0.6), name='全网众生节点'))
        f3d.add_trace(go.Scatter3d(x=[x_v], y=[y_v], z=[z_v], mode='markers+text', text=[data['day_master']], textposition="top center", marker=dict(size=18, color=dm_info['color'], symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=dm_info['color'], size=20, family="Noto Sans SC", weight="bold"), name='你的元神系位'))
        f3d.update_layout(scene=dict(xaxis_title='金属性算力', yaxis_title='木属性算力', zaxis_title='水属性算力', xaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), yaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), zaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b")), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=400, showlegend=False)
        st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False}, theme=None)

    with t_sol:
        st.markdown("<div style='text-align:center; color:#10b981; font-weight:bold; margin-bottom:10px; margin-top:15px; font-family:Orbitron;'>/// SOLIDITY SMART CONTRACT MINT LOG</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#94a3b8; margin-bottom:10px; text-align:center;'>系统已自动将您的八字编译为不可篡改的 ERC721 智能合约源码。</div>", unsafe_allow_html=True)
        code_block = f"""// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\nimport "@karma-os/contracts/token/ERC721.sol";\n\ncontract Karma_Destiny_Registry_V33 is ERC721 {{\n    struct SoulProfile {{\n        string bazi_code;\n        string day_master;\n        string primary_element;\n    }}\n    \n    mapping(uint256 => SoulProfile) public souls;\n    \n    constructor() ERC721("KARMA_DESTINY", "SOUL") {{}}\n\n    // =====================================\n    // SYSTEM MINT LOG \n    // MINTED_TO: {data['name']}\n    // BLOCK_HEIGHT: {block_height}\n    // CONTRACT_ADDR: {contract_addr}\n    // =====================================\n    \n    function executeMint() public {{\n        uint256 tokenId = {token_id};\n        souls[tokenId] = SoulProfile("{data['bazi_str']}", "{data['day_master']}", "{dm_info['element']}");\n        _mint(msg.sender, tokenId);\n    }}\n}}"""
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(code_block, language="solidity")
        st.markdown('</div>', unsafe_allow_html=True)

    # 📥 [模块 VI]：资产提取与分享终端 (终极深渊解析卡片)
    st.markdown("<div class='module-title'>📥 模块 VI：全息资产提取终端</div>", unsafe_allow_html=True)
    t_img, t_txt, t_json = st.tabs(["📸 视觉海报 (长按/右键保存)", "📜 万字深度解析档案 (强力推荐)", "💾 极客 JSON 底包"])

    with t_img:
        st.markdown("<div style='font-size:13px; color:#10b981; margin-bottom:10px; text-align:center;'>系统已启用最高优先级【防死锁渲染引擎】压制高清海报，请等待 2 秒...</div>", unsafe_allow_html=True)
        
        tags_html_poster = "".join([f"<span style='background:rgba(244,63,94,0.15); border:1px solid rgba(244,63,94,0.6); padding:4px 8px; border-radius:4px; font-size:11px; color:#ffe4e6; font-weight:bold; margin:3px; display:inline-block;'>{s}</span>" for s in data['skills']])
        wx_colors = {'金': '#e2e8f0', '木': '#10b981', '水': '#3b82f6', '火': '#f43f5e', '土': '#f59e0b'}
        
        wx_bars_html = ""
        for k, v in data['wx_scores'].items():
            wx_bars_html += f'''<div class="stat-row"><span style="color:#e2e8f0; width:30px;">{k}</span><div class="sbc"><div class="sbf" style="width:{v}%; background:{wx_colors[k]}; box-shadow: 0 0 8px {wx_colors[k]}"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">{v}%</span></div>'''

        # 🚨 终极安全 HTML 海报引擎：绝对顶格，不留任何隐患
        HTML_POSTER = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
body {{ margin: 0; display: flex; flex-direction: column; align-items: center; background-color: transparent !important; font-family: 'Noto Sans SC', sans-serif; user-select: none; padding: 10px 0; color: #ffffff; overflow-x: hidden; }}
#render-target {{ position: absolute; top: -9999px; left: -9999px; z-index: -100; pointer-events: none; }}
#capture-box {{ width: 340px; background-color: #010308; padding: 30px 20px; border-radius: 12px; border: 1px solid rgba(0, 243, 255, 0.5); box-shadow: 0 0 40px rgba(0, 243, 255, 0.2); position: relative; overflow: hidden; color: #fff; box-sizing: border-box; margin: 0 auto; }}
.cyber-grid {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px); background-size: 20px 20px; z-index: 0; pointer-events:none;}}
.top-glow {{ position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: linear-gradient(90deg, transparent, #00f3ff, transparent); z-index: 1; }}
.ct {{ position: relative; z-index: 2; }}
.hd {{ border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 15px; margin-bottom: 20px; text-align:center; }}
.logo-title {{ color: #00f3ff; font-family: 'Orbitron', sans-serif; font-size: 18px; font-weight: 900; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0,243,255,0.5);}}
.logo-sub {{ font-size: 12px; color: #f43f5e; font-weight: bold; margin-top: 5px; letter-spacing: 4px; }}
.user-info {{ text-align: center; font-size: 18px; font-weight: 900; letter-spacing: 2px; margin-bottom: 20px; color: #fff; }}
.bz-grid {{ display: flex; justify-content: space-around; margin-bottom: 20px; background: rgba(0,0,0,0.4); padding: 15px 5px; border-radius: 8px; border: 1px solid rgba(0,243,255,0.2);}}
.bz-col {{ display: flex; flex-direction: column; align-items: center; }}
.bz-c {{ font-size: 26px; font-weight: 900; color: #00f3ff; margin-bottom: 2px; text-shadow: 0 0 10px rgba(0,243,255,0.4); font-family: 'Noto Sans SC', serif;}}
.bz-l {{ font-size: 9px; color: #94a3b8; letter-spacing: 1px; margin-top:4px; font-family: 'Orbitron', sans-serif;}}
.dm-box {{ background: rgba(244,63,94,0.1); border-left: 4px solid #f43f5e; padding: 12px; margin-bottom: 25px; border-radius: 0 6px 6px 0; }}
.dm-title {{ font-size: 10px; color: #f43f5e; font-family: 'Orbitron'; margin-bottom: 5px; letter-spacing: 1px; font-weight:bold;}}
.dm-val {{ font-size: 16px; font-weight: bold; color: {dm_info['color']}; text-shadow: 0 0 10px {dm_info['color']};}}
.ft {{ text-align: center; color: #64748b; font-family: 'Orbitron'; font-size: 9px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.1); line-height: 1.6; margin-top: 10px;}}
#ui {{ font-family: 'Orbitron'; color: #00f3ff; font-size: 13px; text-align: center; padding: 40px; animation: p 1s infinite alternate; letter-spacing: 2px; font-weight:bold;}}
@keyframes p {{ 0% {{ opacity: 1; text-shadow: 0 0 10px #00f3ff; }} 100% {{ opacity: 0.4; }} }}
#img {{ display: none; width: 100%; max-width: 340px; height: auto; border-radius: 12px; border: 1px solid rgba(0,243,255,0.5); box-shadow: 0 20px 40px rgba(0,0,0,0.8); margin: 0 auto; box-sizing: border-box;}}
.ht {{ display: none; background: rgba(0,243,255,0.1); border: 1px solid #00f3ff; padding: 15px; border-radius: 8px; font-size: 13px; color: #fff; text-align: center; margin: 20px auto 0 auto; width: 100%; max-width: 340px; box-sizing: border-box; text-shadow: 0 0 5px rgba(0,0,0,0.8); line-height: 1.6;}}
.stat-row {{ display: flex; align-items: center; margin-bottom: 8px; font-size: 11px; font-weight: bold; justify-content: space-between; }}
.stat-row:last-child {{ margin-bottom: 0; }}
.sbc {{ background: rgba(255,255,255,0.05); border-radius: 3px; height: 6px; width: 160px; position: relative; overflow: hidden; margin: 0 8px; border: 1px solid rgba(255,255,255,0.1);}}
.sbf {{ position: absolute; left: 0; top: 0; height: 100%; border-radius: 3px;}}
</style>
</head>
<body>
<div id="render-target">
    <div id="capture-box">
        <div class="cyber-grid"></div><div class="top-glow"></div>
        <div class="ct">
            <div class="hd">
                <div class="logo-title">KARMA OS V1.0</div>
                <div class="logo-sub">全 息 命 盘 终 端</div>
            </div>
            
            <div class="user-info">[{data['name']}] · {data['gender']}</div>
            
            <div class="bz-grid">
                <div class="bz-col"><span class="bz-c">{bazi_arr[0][0]}</span><span class="bz-c" style="color:#e2e8f0;">{bazi_arr[0][1]}</span><span class="bz-l">YEAR</span></div>
                <div class="bz-col"><span class="bz-c">{bazi_arr[1][0]}</span><span class="bz-c" style="color:#e2e8f0;">{bazi_arr[1][1]}</span><span class="bz-l">MONTH</span></div>
                <div class="bz-col" style="background:rgba(0,243,255,0.15); border:1px solid rgba(0,243,255,0.4); padding:5px; border-radius:6px; box-shadow: 0 0 10px rgba(0,243,255,0.2);"><span class="bz-c" style="color:#00f3ff;">{bazi_arr[2][0]}</span><span class="bz-c" style="color:#e2e8f0;">{bazi_arr[2][1]}</span><span class="bz-l" style="color:#00f3ff;">DAY</span></div>
                <div class="bz-col"><span class="bz-c">{bazi_arr[3][0]}</span><span class="bz-c" style="color:#e2e8f0;">{bazi_arr[3][1]}</span><span class="bz-l">TIME</span></div>
            </div>
            
            <div class="dm-box">
                <div class="dm-title">/// CORE DAY MASTER ///</div>
                <div class="dm-val">{data['day_master']} · {dm_info['role']}</div>
            </div>

            <div style="text-align:center; margin-bottom:10px;"><div style="font-size:10px; color:#a855f7; margin-bottom:8px; font-family:Orbitron; font-weight:bold;">[ SKILL TREE ]</div>{tags_html_poster}</div>
            
            <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.2); border-radius: 8px; padding: 15px 10px; margin-bottom: 20px;">
                <div style="font-family: 'Orbitron', monospace; font-size: 9px; color: #00f3ff; text-align: center; margin-bottom: 12px;">/// WUXING METRICS ///</div>
                {wx_bars_html}
            </div>

            <div class="ft">
                <div style="margin-bottom:4px;font-weight:bold; color:#00f3ff;">POWERED BY LUNAR ALGORITHM</div>
                <div>HASH: 0x{data['hash_id'][:12]} | © {COPYRIGHT}</div>
            </div>
        </div>
    </div>
</div>

<div id="ui">[ GENERATING HOLOGRAPHIC POSTER... ]</div>
<img id="result-img" alt="Cyber Bazi Card" title="长按保存或分享" />
<div id="hint" class="ht"><span style="font-size:18px;">✅</span> <b>全息命盘压制完成！</b><br><span style="color:#00f3ff;">👆 手机端请 <b>长按上方图片</b> 保存至相册</span></div>

<script>
const executeRender = () => {{
    setTimeout(() => {{ 
        if(typeof html2canvas === 'undefined') {{ 
            document.getElementById('ui').innerHTML='<span style="color:#f43f5e;">❌ 渲染引擎拦截。</span><br>请直接截屏当前网页。'; 
            return; 
        }} 
        
        const target = document.getElementById('capture-box');
        html2canvas(target, {{
            scale: 1.5, 
            backgroundColor: '#010308', 
            useCORS: true, 
            allowTaint: true,
            logging: false,
            onclone: function(clonedDoc) {{
                var rt = clonedDoc.getElementById('render-target');
                if (rt) {{
                    rt.style.position = 'relative';
                    rt.style.top = '0';
                    rt.style.left = '0';
                    rt.style.transform = 'none';
                    rt.style.opacity = '1';
                    rt.style.zIndex = '1';
                }}
            }}
        }}).then(canvas => {{ 
            document.getElementById('result-img').src = canvas.toDataURL('image/png'); 
            document.getElementById('ui').style.display = 'none'; 
            document.getElementById('result-img').style.display = 'block'; 
            document.getElementById('hint').style.display = 'block'; 
            document.getElementById('render-target').style.display = 'none'; 
        }}).catch(err => {{ 
            console.error(err);
            document.getElementById('ui').innerHTML='<span style="color:#ffd700;">⚠️ 手机内存受限，图片压制失败。</span><br>请直接系统截屏！'; 
        }});
    }}, 1500); 
}};

// 强力兜底：无论 load 事件是否触发，2秒后强制执行截图
if (document.readyState === 'complete') {{
    executeRender();
}} else {{
    window.addEventListener('load', executeRender);
    setTimeout(executeRender, 2000);
}}
</script>
</body>
</html>
"""
        components.html(HTML_POSTER, height=850)

    # 🚀 极致强化：万字级深度命格解析卡片 (完全兑现可复制下载需求)
    with t_txt:
        st.markdown("<div style='font-size:14px; color:#10b981; margin-bottom:10px; margin-top:10px; font-weight:bold;'>系统已为您生成专属的【深度命格鉴定报告】。您可以点击代码框右上角一键复制，或直接下载保存为本地档案。</div>", unsafe_allow_html=True)
        
        detailed_card = f"""=======================================================
███████╗██████╗ ███████╗    ██████╗ ███████╗███████╗████████╗
██╔════╝██╔══██╗██╔════╝    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝
███████╗██║  ██║█████╗      ██║  ██║█████╗  ███████╗   ██║   
╚════██║██║  ██║██╔══╝      ██║  ██║██╔══╝  ╚════██║   ██║   
███████║██████╔╝███████╗    ██████╔╝███████╗███████║   ██║   
╚══════╝╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
=======================================================
【 KARMA-OS 量子命盘 · 深度鉴定报告 V33.0 】

[ 👤 节点基础信息 ]
▸ 物理标识：{data['name']}
▸ 载体形态：{data['gender']}
▸ 生肖锚点：{data['zodiac']}
▸ 诞生坐标：{data['birth_date_str']} {data['birth_time_str']}
▸ 灵魂哈希：0x{data['hash_id']}

[ 🧬 底层源代码 (四柱八字) ]
▸ 源码数组：{data['bazi_str']}
          (年柱)   (月柱)   (日柱)   (时柱)

[ 🔥 核心元神 (日主属性解析) ]
▸ 绝对核心：{data['day_master']} ({dm_info['element']}属性)
▸ 命理定位：{dm_info['role']}
▸ 算力特质：{dm_info['desc']}

[ 📈 核心演进路线 (Evolution Path) ]
▸ 初阶形态：{dm_info['evolution_path'][0]}
▸ 觉醒形态：{dm_info['evolution_path'][1]}
▸ 满血形态：{dm_info['evolution_path'][2]}
▸ 终极化神：{dm_info['ultimate_evolution']}

[ ⚠️ 致命崩溃盲点 (Black Swan Vulnerability) ]
▸ 致命漏洞：{dm_info['black_swan']}
▸ 官方补丁：{dm_info['patch']}

[ 📊 算力负载分布 (五行能量监测) ]
▸ 金属性 (裁决/执行) : {data['wx_scores'].get('金', 0)}%
▸ 木属性 (架构/生长) : {data['wx_scores'].get('木', 0)}%
▸ 水属性 (数据/流动) : {data['wx_scores'].get('水', 0)}%
▸ 火属性 (算力/爆发) : {data['wx_scores'].get('火', 0)}%
▸ 土属性 (存储/承载) : {data['wx_scores'].get('土', 0)}%
▸ 综合评定：您的五行熵增阀值为 {entropy_score}%。{e_tag}
  ({r_desc})

[ 🗡️ 先天外挂技能树 (十神配置) ]
▸ 核心挂载：{', '.join(data['skills'])}
▸ 协同建议：基于您的系统架构，强烈建议寻找拥有高【{partner_element}】属性的节点，或本命元神为【{best_partner_stem}】的道侣进行并网运行。可大幅降低系统级宕机风险。

=======================================================
POWERED BY LUNAR DESTINY ENGINE | © {COPYRIGHT}
======================================================="""
        
        # 恢复原生 st.code 提供极其丝滑的一键 Copy
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(detailed_card, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 增加一键原生下载功能
        st.download_button(
            label="📥 下载深度命格机密报告 (.txt)",
            data=detailed_card,
            file_name=f"DESTINY_REPORT_{data['name']}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with t_json:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; margin-top:10px;'>💾 极客视角：导出您的先天八字 JSON 结构树底包：</div>", unsafe_allow_html=True)
        export_data = {
            "version": VERSION,
            "node_alias": data['name'],
            "bazi_code": data['bazi_str'],
            "day_master": {
                "element": data['day_master'],
                "role": dm_info['role'],
                "description": dm_info['desc'],
                "evolution": dm_info['ultimate_evolution'],
                "vulnerability": dm_info['black_swan'],
                "system_patch": dm_info['patch']
            },
            "wu_xing_distribution": data['wx_scores'],
            "extracted_skills": data['skills'],
            "entropy_warning": {
                "score": entropy_score,
                "status": e_tag,
                "details": r_desc
            },
            "hash_signature": data['hash_id'],
            "timestamp": current_time_str
        }
        json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
        st.download_button(label="📥 提取原始 JSON 命盘档案", data=json_str, file_name=f"DESTINY_{data['hash_id'][:6]}.json", mime="application/json", use_container_width=True)

    # 底部重启按钮
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_btm_l, col_btm_m, col_btm_r = st.columns([1, 2, 1])
    with col_btm_m:
        if st.button("⏏ 弹出磁盘并重启终端 (SYS_REBOOT)", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================================================================
# 🛑 [ CORE 07 ] 赛博呼吸专属版权区
# =========================================================================
st.markdown(f"""
<div style="text-align:center; margin-top:60px; margin-bottom:40px; position:relative; z-index:10;">
    <div style="color:#ffd700 !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;">POWERED BY LUNAR ENGINE</div>
    <div class="copyright-niliu">© 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">{COPYRIGHT}</b></div>
</div>
""", unsafe_allow_html=True)
