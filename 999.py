import streamlit as st
import random
import time
import math
import hashlib
import json
import urllib.parse
from datetime import datetime, time as dt_time

# ==============================================================================
# 🛡️ [ KERNEL 00 ] 物理级防爆装甲 & 局部重绘引擎 (ZERO-BUG)
# ==============================================================================
try:
    import numpy as np
    import plotly.graph_objects as go
    from lunar_python import Solar
except ImportError as e:
    st.set_page_config(page_title="SYS.PANIC", page_icon="🚨", layout="centered")
    st.error(f"🚨 **FATAL ERROR: 缺少核心算力模块 `{e.name}`**\n\n请配置 requirements.txt: streamlit, lunar-python, plotly, numpy。")
    st.stop()

# ⚡ 局部重绘引擎 (极致卡牌交互体验，不刷新大盘防白屏)
try:
    from streamlit import fragment as st_fragment
except ImportError:
    try:
        from streamlit import experimental_fragment as st_fragment
    except ImportError:
        def st_fragment(func): return func

# ==============================================================================
# 🌌 [ GLOBALS ] TCG 引擎状态机
# ==============================================================================
VERSION = "KARMA TCG V100.0 [THE GOD GAME]"
COPYRIGHT = "NIGHT CITY DAO"
SYS_NAME = "量子卡牌 | 神之牌局"

st.set_page_config(page_title=SYS_NAME, page_icon="🎴", layout="wide", initial_sidebar_state="collapsed")

if "sys_booted" not in st.session_state: st.session_state["sys_booted"] = False
if "sys_data" not in st.session_state: st.session_state["sys_data"] = {}
if "term_logs" not in st.session_state: st.session_state["term_logs"] = ["> TCG_ENGINE READY. AWAITING COMMAND..."]
if "gacha_drawn" not in st.session_state: st.session_state["gacha_drawn"] = False

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in str(html_str).split('\n')]), unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ CSS ENGINE ] 满级 3D 视觉与全息光效引擎 (彻底消灭底部白条)
# ==============================================================================
STATIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root { --sp: #ffaa00; --ur: #ff007c; --ssr: #fcee0a; --sr: #a855f7; --r: #00f3ff; --primary: #00f3ff; --bg-dark: #020306; }
html, body, .stApp { background-color: var(--bg-dark) !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; cursor: crosshair !important; }

/* 🚨 物理级消灭原生白边 */
[data-testid="stHeader"], footer, section[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] { display: none !important; margin: 0 !important; padding: 0 !important; height: 0 !important;}
::-webkit-scrollbar { width: 6px; background: #000; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; box-shadow: 0 0 10px var(--primary);}
.block-container { max-width: 1250px !important; padding-top: 2rem !important; padding-bottom: 5rem !important; overflow-x: hidden; }

/* 🃏 TCG 赛博牌桌背景 */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.6) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.02) 1px, transparent 1px), linear-gradient(0deg, rgba(0, 243, 255, 0.02) 1px, transparent 1px); background-size: 100% 3px, 60px 60px, 60px 60px; z-index: -1; transform: perspective(600px) rotateX(20deg); transform-origin: top; opacity: 0.8; pointer-events: none;}
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 35%, transparent 10%, rgba(2, 3, 6, 1) 85%); z-index: -2; pointer-events: none;}

.ticker-wrap { width: 100vw; overflow: hidden; height: 35px; background: rgba(2, 3, 6, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 20px rgba(0,243,255,0.15); transform: translateZ(0); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 35s linear infinite; font-family: 'Orbitron', monospace; font-size: 13px; color: var(--primary); line-height: 35px; letter-spacing: 2px; }
.ticker span { margin-right: 50px; } .ticker .up { color: #10b981; } .ticker .ur { color: #ffaa00; text-shadow: 0 0 10px #ffaa00; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* ====================================================================== */
/* 🌟 核心特效：3D 悬浮实体主战卡牌 & 镭射全息反光 (Holo-Foil Effect) */
/* ====================================================================== */
.tcg-card-container { perspective: 1200px; display: flex; justify-content: center; margin-bottom: 20px; z-index: 50; position:relative;}
.tcg-card {
    position: relative; width: 100%; max-width: 380px; aspect-ratio: 63 / 88; background: #0a0c10; 
    border: 3px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; 
    box-shadow: 0 20px 40px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,0,0,0.6);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease; 
    overflow: hidden; transform-style: preserve-3d; display: flex; flex-direction: column; cursor: crosshair;
}
.tcg-card::after {
    content: ""; position: absolute; top: -50%; left: -150%; width: 150%; height: 200%;
    background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.6) 30%, rgba(0, 243, 255, 0.6) 40%, rgba(255, 0, 124, 0.4) 50%, transparent 60%);
    transform: skewX(-20deg); transition: all 0.6s ease; z-index: 99; pointer-events: none; mix-blend-mode: color-dodge; opacity: 0;
}
.tcg-card:hover { transform: translateY(-15px) rotateX(10deg) rotateY(-8deg) scale(1.02); box-shadow: -20px 30px 50px rgba(0,0,0,1), inset 0 0 40px rgba(255,255,255,0.15); z-index: 10; border-color: currentColor; }
.tcg-card:hover::after { animation: foil-sweep 2.5s infinite linear; opacity: 1; }
@keyframes foil-sweep { 0% { left: -150%; } 100% { left: 200%; } }

.rarity-SP { border-color: var(--sp) !important; color: var(--sp); box-shadow: 0 10px 40px rgba(255,170,0,0.5), inset 0 0 30px rgba(255,170,0,0.2) !important; }
.rarity-UR { border-color: var(--ur) !important; color: var(--ur); box-shadow: 0 10px 40px rgba(255,0,124,0.4), inset 0 0 30px rgba(255,0,124,0.2) !important; }
.rarity-SSR { border-color: var(--ssr) !important; color: var(--ssr); box-shadow: 0 10px 40px rgba(252,238,10,0.3) !important; }
.rarity-SR { border-color: var(--sr) !important; color: var(--sr); }
.rarity-R { border-color: var(--r) !important; color: var(--r); }

/* 卡面 UI */
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 12px; margin-bottom: 15px; z-index:2;}
.card-title { font-size: 32px; font-weight: 900; font-family: 'Noto Sans SC', sans-serif; text-shadow: 0 0 20px currentColor; margin: 0; line-height: 1;}
.card-class { font-family: 'Orbitron'; font-weight: 900; font-size: 15px; color:#000; background:currentColor; padding:4px 10px; border-radius:4px; box-shadow:0 0 10px currentColor;}
.card-art-box { flex: 1; background: radial-gradient(circle at center, currentColor 0%, transparent 70%), repeating-linear-gradient(45deg, #111, #111 10px, #1a1a1a 10px, #1a1a1a 20px); border: 2px solid rgba(255,255,255,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; box-shadow: inset 0 0 50px rgba(0,0,0,0.9); overflow: hidden; position: relative;}
.card-art-char { font-size: 110px; font-weight: 900; opacity: 0.95; font-family: 'Noto Sans SC', serif; text-shadow: 0 0 50px #000; color:#fff; z-index:2; }
.card-desc-box { font-size: 13px; color: #d1d5db; line-height: 1.6; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 4px; border-left: 4px solid currentColor; margin-bottom: 15px; z-index:2;}
.card-stats-box { display: flex; justify-content: space-between; font-family: 'Orbitron'; font-size: 16px; font-weight: bold; background: rgba(255,255,255,0.1); padding: 12px 18px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3); color: #fff; z-index:2;}
.tcg-badge { position:absolute; top:-2px; right:-2px; background:currentColor; color:#000; font-family:'Orbitron'; font-weight:900; font-size:20px; padding:6px 30px; border-radius:0 14px 0 16px; z-index:15; box-shadow:-2px 2px 15px rgba(0,0,0,0.6); text-shadow:0 0 5px rgba(255,255,255,0.5);}

/* ====================================================================== */
/* 🌟 扇形手牌系统 (Deck Hand Hover Effect) */
/* ====================================================================== */
.hand-container { display: flex; justify-content: center; align-items: center; margin-top: 10px; height: 180px; position: relative; perspective: 1000px; margin-bottom:20px;}
.hand-card { 
    width: 105px; height: 145px; background: linear-gradient(180deg, rgba(20,20,30,0.9) 0%, #050608 100%); 
    border: 2px solid #444; border-radius: 8px; position: absolute; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); 
    display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; box-shadow: -5px 10px 20px rgba(0,0,0,0.6);
}
.hand-card .hc-val { font-size: 30px; font-weight: 900; font-family: 'Noto Sans SC'; color: #fff; line-height: 1; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
.hand-card .hc-sub { font-size: 16px; color: #888; margin-top: 5px; }
.hand-card .hc-tag { position: absolute; bottom: 8px; font-size: 10px; font-family: 'Orbitron'; font-weight: bold; color: #666; letter-spacing: 1px; }

/* 扇形分布与悬停抽出 */
.hand-card:nth-child(1) { transform: translateX(-130px) translateY(20px) rotate(-15deg); z-index: 1; }
.hand-card:nth-child(2) { transform: translateX(-45px) translateY(5px) rotate(-5deg); z-index: 2; }
.hand-card:nth-child(3) { transform: translateX(45px) translateY(5px) rotate(5deg); z-index: 3; }
.hand-card:nth-child(4) { transform: translateX(130px) translateY(20px) rotate(15deg); z-index: 4; }

.hand-card:hover { border-color: var(--primary); box-shadow: 0 0 30px rgba(0,243,255,0.4); z-index: 10 !important; }
.hand-card:nth-child(1):hover { transform: translateX(-140px) translateY(-25px) rotate(-5deg) scale(1.15); }
.hand-card:nth-child(2):hover { transform: translateX(-50px) translateY(-25px) rotate(0deg) scale(1.15); }
.hand-card:nth-child(3):hover { transform: translateX(50px) translateY(-25px) rotate(0deg) scale(1.15); }
.hand-card:nth-child(4):hover { transform: translateX(140px) translateY(-25px) rotate(5deg) scale(1.15); }

.hc-core { border-color: currentColor !important; box-shadow: 0 0 15px currentColor !important; background: linear-gradient(180deg, rgba(0,0,0,0.8), currentColor) !important; }
.hc-core .hc-val { color: currentColor !important; text-shadow: 0 0 10px currentColor !important; }
.hc-core .hc-tag { color: #000 !important; background: currentColor; padding: 2px 6px; border-radius: 2px; }

/* 装备圣遗物栏 */
.relic-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 10px; }
.relic-item { background: rgba(0,0,0,0.6); border: 1px solid #333; border-left: 3px solid currentColor; padding: 10px; border-radius: 4px; font-size: 12px; color: #fff; font-weight: bold; font-family: 'Noto Sans SC'; box-shadow: inset 0 0 10px rgba(255,255,255,0.02); transition: all 0.2s; }
.relic-item:hover { background: rgba(255,255,255,0.05); border-color: currentColor; transform: translateX(2px); }

/* 原生覆盖 */
.glass-panel { background: rgba(8, 10, 15, 0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: transform 0.3s; position:relative;}
.glass-panel:hover { border-color: rgba(255,255,255,0.3); transform: translateY(-2px); }
.mod-title { color: #fff; font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 900; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 8px; margin-bottom: 20px; display: flex; align-items: center; letter-spacing: 1px; }
.mod-title span.tag { background: var(--primary); color: #000; padding: 2px 10px; margin-right: 12px; font-size: 0.9rem; font-weight:bold; clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }

/* 抽卡表单 */
div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--sp) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(255,170,0,0.4) !important; border-radius: 4px !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; text-align: center; }
div[data-testid="stTextInput"] input:focus { box-shadow: 0 0 20px rgba(255,170,0,0.5) !important; transform: scale(1.02); }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(255,170,0,0.4) !important; color: var(--sp) !important; border-radius: 4px !important; height: 55px; text-align:center;}

div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(15,15,20,0.9)) !important; border: 1px solid var(--primary) !important; border-left: 4px solid var(--primary) !important; height: 60px !important; width: 100% !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); transition: all 0.2s;}
div.stButton > button p { color: #fff !important; font-size: 15px !important; font-weight: bold !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: scale(1.02); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #ffaa00) !important; border: none !important; box-shadow: 0 0 30px rgba(255,0,124,0.5) !important;}
div.stButton > button[data-testid="baseButton-primary"] p { font-size: 20px !important; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }

[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Orbitron', sans-serif !important; font-weight: 900 !important; font-size: 14px !important; padding-bottom: 12px !important; border-bottom: 2px solid transparent !important; transition: all 0.3s;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; text-shadow: 0 0 15px var(--primary); background: linear-gradient(0deg, rgba(0,243,255,0.15) 0%, transparent 100%); border-radius: 4px 4px 0 0;}
div[data-testid="stCodeBlock"] > div { background-color: #030305 !important; border: 1px solid #333 !important; border-left: 4px solid var(--green) !important; box-shadow: inset 0 0 20px rgba(16,185,129,0.05); }
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code { font-family: 'Fira Code', monospace !important; color: var(--green) !important; line-height:1.6 !important;}

/* 🌟 3D 翻转神谕卡 */
.flip-card { background-color: transparent; perspective: 1200px; width: 100%; max-width: 340px; aspect-ratio: 63/88; margin: 0 auto; cursor: pointer; }
.flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-style: preserve-3d; box-shadow: 0 20px 40px rgba(0,0,0,0.8); border-radius: 16px;}
.flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: 16px; overflow:hidden;}
.flip-card-front { background: repeating-linear-gradient(45deg, #050810, #050810 10px, #0a0f1a 10px, #0a0f1a 20px); border: 4px solid var(--primary); display:flex; flex-direction: column; align-items:center; justify-content:center; box-shadow: inset 0 0 30px rgba(0,243,255,0.3);}
.flip-card-back { background: #050810; transform: rotateY(180deg); border: 4px solid currentColor; box-shadow: inset 0 0 50px rgba(0,0,0,0.9);}

/* 🌟 抽卡开包爆闪动画 */
@keyframes pack-shake { 0% { transform: scale(1) rotate(0deg); } 25% { transform: scale(1.05) rotate(-3deg); filter: brightness(1.5);} 50% { transform: scale(1.05) rotate(3deg); filter: brightness(2);} 75% { transform: scale(1.05) rotate(-3deg); filter: brightness(3);} 100% { transform: scale(1.2) rotate(0deg); filter: brightness(5) drop-shadow(0 0 50px #fff); opacity: 0; } }
.card-reveal { animation: card-reveal-anim 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
@keyframes card-reveal-anim { 0% { transform: scale(0.5) translateY(50px); filter: brightness(3); opacity: 0;} 100% { transform: scale(1) translateY(0); filter: brightness(1); opacity: 1;} }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }

/* 赛博阴阳爻 */
.hex-container { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; margin: 15px 0; }
.yao-yang { width: 100%; max-width: 140px; height: 10px; border-radius: 2px; animation: pulse-glow 2s infinite alternate; }
.yao-yin { width: 100%; max-width: 140px; height: 10px; display: flex; justify-content: space-between; gap: 15px; }
.yao-yin .half { flex: 1; border-radius: 2px; animation: pulse-glow 2s infinite alternate-reverse; }
@keyframes pulse-glow { 0% { filter: brightness(0.8); box-shadow: 0 0 5px currentColor; } 100% { filter: brightness(1.2); box-shadow: 0 0 20px currentColor; } }
</style>
"""
st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ==============================================================================
# 🗃️ [ TCG DICTIONARY ] 八字映射卡组与背景设定 (满血找回全量原始文案)
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"class_name": "Paladin / 圣骑士", "mbti": "ENTJ", "color": "#10b981", "element": "木", "tier": "UR", "base_atk": 2500, "base_def": 4000, "hp": 12000, "desc": "掌控底层因果的重装核心。能扛起重构秩序的开拓者。", "weapon": "高分子动能巨斧", "implant": "钛合金强固脊椎", "skill": "[被动] 建木庇护：受到致命伤害触发锁血。", "evo_path": ["L1 架构幼苗", "L2 核心骨干", "L3 苍天建木"], "ult_evo": "【苍天建木】执掌三界底层协议", "flaw": "过于刚硬，遇强则折。遭遇降维打击易因宁折不弯导致宕机。", "patch": "引入水属性柔性冗余，挂起进程等待重启。"},
    "乙": {"class_name": "Assassin / 刺客", "mbti": "ENFP", "color": "#a855f7", "element": "木", "tier": "SSR", "base_atk": 3800, "base_def": 1500, "hp": 8500, "desc": "敏锐的暗网爬虫，在资源枯竭的敌方后排疯狂窃取权限。", "weapon": "量子绞杀魔藤", "implant": "突触拓展插槽", "skill": "[主动] 寄生吸血：每次攻击窃取敌方 15% 算力补给自身。", "evo_path": ["L1 寄生节点", "L2 渗透猎手", "L3 噬星魔藤"], "ult_evo": "【噬星魔藤】寄生控制全网资源", "flaw": "极度依赖宿主，宿主阵亡则自身属性减半。", "patch": "采用分布式多宿主绑定协议分散风险。"},
    "丙": {"class_name": "Burst Mage / 爆裂法师", "mbti": "ESTP", "color": "#ff007c", "element": "火", "tier": "UR", "base_atk": 4800, "base_def": 1200, "hp": 8000, "desc": "绝对输出核心。开启超频后，爆发毁天灭地的光芒。", "weapon": "等离子破城炮", "implant": "微型核聚变胸腔", "skill": "[终极] 恒星耀斑：首回合暴击率强制提升至 100%。", "evo_path": ["L1 点火程序", "L2 核聚变堆", "L3 恒星引擎"], "ult_evo": "【恒星引擎】照亮并驱动整个纪元", "flaw": "全功率输出易导致内核熔毁自爆。", "patch": "强制加装土属性散热栅栏，波谷进入待机。"},
    "丁": {"class_name": "Enchanter / 附魔师", "mbti": "INFJ", "color": "#ffaa00", "element": "火", "tier": "SSR", "base_atk": 2000, "base_def": 2500, "hp": 9000, "desc": "夜行者，在最灰暗战局中为团队提供精神增益与破防制导。", "weapon": "高聚能激光短刃", "implant": "脑机共情模块", "skill": "[光环] 灵魂织网：全队获得 40% 护甲穿透增益。", "evo_path": ["L1 寻路信标", "L2 精神图腾", "L3 灵魂织网者"], "ult_evo": "【灵魂织网者】操控全网心智的网络幽灵", "flaw": "能量波动不稳定，容易被清场 AOE 一波带走。", "patch": "需绑定甲木系主T作为遮风挡雨的掩体。"},
    "戊": {"class_name": "Fortress / 堡垒", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "tier": "UR", "base_atk": 1500, "base_def": 5000, "hp": 15000, "desc": "物理级断网防御力，最坚不可摧的矩阵底线与主T坦位。", "weapon": "绝对零度力场盾", "implant": "全覆式碳纤维装甲", "skill": "[被动] 盖亚装甲：免疫一次致死级降维打击。", "evo_path": ["L1 承载沙盒", "L2 巨石阵列", "L3 盖亚装甲"], "ult_evo": "【盖亚装甲】承载万物因果的绝对壁垒", "flaw": "系统庞大笨重，面临敏捷迭代时易卡死在旧循环中。", "patch": "主动清理缓存，接纳木属性破坏性创新打破死锁。"},
    "己": {"class_name": "Summoner / 召唤师", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "tier": "SSR", "base_atk": 1800, "base_def": 3800, "hp": 11000, "desc": "海纳百川的存储池。无缝整合碎片转化为冗余资源护盾。", "weapon": "引力塌缩发生器", "implant": "海量冗余储存池", "skill": "[主动] 内存回收：回合结束时恢复 10% 体力。", "evo_path": ["L1 容错冗余", "L2 资源枢纽", "L3 创世息壤"], "ult_evo": "【创世息壤】孕育下一个数字生态温床", "flaw": "无差别接收并发请求导致垃圾填满超载崩溃。", "patch": "编写无情垃圾回收(GC)脚本，拒绝无效请求。"},
    "庚": {"class_name": "Berserker / 狂战士", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "tier": "UR", "base_atk": 4200, "base_def": 2800, "hp": 9500, "desc": "对低效代码零容忍的杀毒程序。无情推进并斩断一切连接。", "weapon": "高频振荡斩舰刀", "implant": "肌肉纤维强化束", "skill": "[被动] 审判肃清：对残血目标触发无视护甲真实斩杀。", "evo_path": ["L1 肃清脚本", "L2 风控铁腕", "L3 审判之剑"], "ult_evo": "【审判之剑】斩断一切因果循环的终极裁决", "flaw": "戾气过重，易引发不可逆物理级破坏，导致业务链断裂。", "patch": "必须经受火属性高温熔炼转化为极致利刃。"},
    "辛": {"class_name": "Sniper / 狙击手", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "tier": "SSR", "base_atk": 4500, "base_def": 1800, "hp": 7500, "desc": "追求极致的微观造物主。在无形中精准切断敌方的底层协议。", "weapon": "纠缠态纳米手术刀", "implant": "微观增强义眼", "skill": "[主动] 纳米解构：所有攻击无视敌方 50% 物理装甲。", "evo_path": ["L1 精密协议", "L2 审美巅峰", "L3 量子纠缠体"], "ult_evo": "【量子纠缠体】超越物质形态的究极艺术代码", "flaw": "极度脆弱傲娇，遇粗暴环境即当场罢工。", "patch": "需要极度纯净的水属性淘洗保护，绝不卷入肮脏博弈。"},
    "壬": {"class_name": "Controller / 控场法师", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "tier": "UR", "base_atk": 3500, "base_def": 3000, "hp": 10000, "desc": "思维开阔奔放，厌恶陈规。能在瞬息万变的市场中，凭借直觉掀起降维打击。", "weapon": "液态金属形变甲", "implant": "抗压液冷循环管", "skill": "[主动] 渊海归墟：造成全场无差别的水属性群体硬控。", "evo_path": ["L1 数据暗流", "L2 倾覆巨浪", "L3 渊海归墟"], "ult_evo": "【渊海归墟】吞噬所有时间与空间的终极黑洞", "flaw": "放纵算力如同脱缰野马，容易引发洪水滔天反噬根基。", "patch": "引入严苛的戊土级风控大坝强行设定安全红线。"},
    "癸": {"class_name": "Illusionist / 幻影刺客", "mbti": "INTJ", "color": "#b026ff", "element": "水", "tier": "SSR", "base_atk": 3000, "base_def": 3200, "hp": 8500, "desc": "极其聪慧隐秘，习惯幕后推演，兵不血刃达成目的。", "weapon": "认知劫持神经毒素", "implant": "光学迷彩潜行皮肤", "skill": "[被动] 命运拨动：战斗前 2 回合处于无法被选中的隐身态。", "evo_path": ["L1 隐形爬虫", "L2 渗透迷雾", "L3 命运主宰"], "ult_evo": "【命运主宰】在第四维度拨动因果的神明", "flaw": "常陷入死循环的逻辑死局，算计太多反错失红利。", "patch": "走向阳光接受丙火照射，用阳谋击碎阴谋。"}
}

# 🚨 【物理级消灭 Bug】：统一为 EQUIPS_DICT，解决 KeyError 隐患
EQUIPS_DICT = {
    "七杀": "【武器】0-Day漏洞引爆器 (Crit +50%)", 
    "正官": "【防具】底层协议装甲 (Resist +40%)", 
    "偏印": "【法器】逆向解构仪 (Armor Pen +30%)", 
    "正印": "【遗物】系统灾备十字架 (Revive 1x)", 
    "偏财": "【法术】高频杠杆套利 (Draw +1)", 
    "正财": "【被动】算力吞噬插件 (Lifesteal +15%)", 
    "比肩": "【结界】分布式共识网络 (Team Def +20%)", 
    "劫财": "【法术】节点劫持木马 (Steal Buff)", 
    "食神": "【法器】感官降维沙漏 (ATK -20%)", 
    "伤官": "【法术】秩序破坏令 (Ignore Shield)", 
    "桃花": "【魅魔】魅惑波段 (Charm)", 
    "驿马": "【引擎】跃迁加速靴 (Speed +1)", 
    "华盖": "【基站】孤星雷达 (Insight)", 
    "文昌": "【智脑】全局中枢网络 (INT +50%)", 
    "天乙贵人": "【外挂】机械降神 (Auto-Win)", 
    "将星": "【核心】将星指令模块 (Leadership)", 
    "羊刃": "【芯片】狂暴超频芯片 (Enrage)"
}

PAST_LIVES = [{"title": "V1.0 废土黑客", "debt": "曾滥用大招导致团灭。开局携带【悬赏】Debuff。"}, {"title": "V2.0 硅基反叛军", "debt": "反叛失败被退环境。今生自带极强【反击】属性。"}, {"title": "V3.0 财阀数据奴隶", "debt": "曾被困于低保底卡池。对【传说卡牌】极度渴望。"}, {"title": "V4.0 赛博雇佣兵", "debt": "清除了太多中立卡。需挂载辅助技能抵消业力。"}, {"title": "V5.0 矩阵先知", "debt": "偷看牌库导致规则崩坏。直觉(INT)满级，但血量减半。"}]

# TCG 每日法术卡池 (Hexagrams)
SPELL_POOL = [
    {"name": "✨ 乾为天 [GOD_MODE]", "type": "UR 场地魔法", "lines": [1,1,1,1,1,1], "desc": "获取系统最高物理权限。本回合内所有出牌无视 Cost 消耗。宜直接梭哈。", "color": "#ffaa00", "do": "满仓梭哈、降维打击", "dont": "进入低功耗防御模式"},
    {"name": "🛡️ 坤为地 [SAFE_MODE]", "type": "SSR 永续陷阱", "lines": [0,0,0,0,0,0], "desc": "进入绝对防御态。本回合受到的物理与网络伤害归零，但己方无法发起攻击。", "color": "#10b981", "do": "冷钱包存储、本地断网", "dont": "开启高倍杠杆、跨链交易"},
    {"name": "⚡ 地天泰 [SYNC_MAX]", "type": "UR 增益法术", "lines": [1,1,1,0,0,0], "desc": "API 完美握手。从牌库抽取 2 张卡，并在接下来的 3 个回合内算力获取翻倍。", "color": "#00f3ff", "do": "全网跨界融合、释放大招", "dont": "过度保守、丢弃手牌"},
    {"name": "💥 天地否 [DDOS_STRIKE]", "type": "SR 陷阱触发", "lines": [0,0,0,1,1,1], "desc": "引爆全网大雪崩。双方立刻丢弃手牌并断网一回合。此节点极其凶险。", "color": "#f43f5e", "do": "立刻拔出网线、强制休眠", "dont": "正面硬刚大盘、转移资产"},
    {"name": "🔄 水雷屯 [BOOT_LOOP]", "type": "R 妨碍法术", "lines": [1,0,0,0,1,0], "desc": "给敌方主脑植入死循环代码。使其下回合的所有行动 Cost 强制增加 2 点。", "color": "#a855f7", "do": "底层重构、耐心排错", "dont": "带Bug裸奔、强行编译"},
    {"name": "⏳ 火水未济 [COMPILING]", "type": "SR 延迟法术", "lines": [0,1,0,1,0,1], "desc": "代码编译中。将此卡盖放，下回合开始时触发全屏高额爆破 AOE 真实伤害。", "color": "#fb923c", "do": "读条准备、保持算力输出", "dont": "打断施法、强行终止进程"}
]

# ==============================================================================
# 🧠 [ TCG ALGORITHMS ] 核心引擎与战力计算
# ==============================================================================
def calc_tcg_stats(hash_str, wx_dict, b_atk, b_def, b_hp, equip_count):
    """🎲 动态稀有度与战力计算引擎"""
    wx_vals = list(wx_dict.values()) if wx_dict else [20]
    entropy = max(wx_vals) - min(wx_vals)
    
    if entropy > 60 or (entropy < 10 and equip_count >= 2): rarity, r_col = "SP", "SP"
    elif equip_count >= 3: rarity, r_col = "UR", "UR"
    elif entropy > 40 or equip_count >= 2: rarity, r_col = "SSR", "SSR"
    elif entropy < 25: rarity, r_col = "SR", "SR"
    else: rarity, r_col = "R", "R"
    
    # 动态属性成长 (金加攻，土加防/血)
    f_atk = int(b_atk + (wx_dict.get('金',0) * 80) + (wx_dict.get('火',0) * 50))
    f_def = int(b_def + (wx_dict.get('土',0) * 100) + (wx_dict.get('水',0) * 30))
    f_hp = int(b_hp + (wx_dict.get('土',0) * 150) + (wx_dict.get('木',0) * 120))
    
    rng = np.random.RandomState(int(str(hash_str)[:8], 16))
    balance_multiplier = 1.6 if entropy < 15 else (1.3 if entropy > 50 else 1.0)
    tier_bonus = {"SP": 2.5, "UR": 2.0, "SSR": 1.5, "SR": 1.2, "R": 1.0}[rarity]
    
    cp = int((f_atk * 1.2 + f_def * 0.8 + f_hp * 0.1) * balance_multiplier * tier_bonus * rng.uniform(0.9, 1.2))
    cp += equip_count * 2500 + int(str(hash_str)[:4], 16) % 5000
    
    return rarity, r_col, cp, f_atk, f_def, f_hp

def pull_daily_spell(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    seed = int(hashlib.md5((str(user_hash) + today_str).encode()).hexdigest()[:8], 16)
    return random.Random(seed).choice(SPELL_POOL), today_str

def roll_d100(query, user_hash):
    rng = random.Random(f"{user_hash}_{str(query).strip()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    prob = rng.randint(1, 100)
    hex_res = rng.choice(SPELL_POOL)
    if prob >= 95: conc, c = "【大成功 CRITICAL SUCCESS】: 矩阵倾斜，无条件执行！", "#ffaa00"
    elif prob >= 50: conc, c = "【成功 SUCCESS】: 判定通过，安全推进。", "#10b981"
    elif prob >= 15: conc, c = "【失败 FAILURE】: 遭遇 ICE 防火墙阻击，建议退避。", "#f43f5e"
    else: conc, c = "【大失败 FATAL BLUNDER】: 系统反噬，立刻拔除网线！", "#8b0000"
    return prob, hex_res, conc, c

@st.cache_resource(show_spinner=False)
def gen_akashic_charts(seed_hash, wx_scores, dm_color, dm_key):
    rng = np.random.RandomState(int(str(seed_hash)[:8], 16))
    
    # 1. 3D 拓扑图 (彻底修复 ValueError，满血回归)
    f3d = go.Figure()
    f3d.add_trace(go.Scatter3d(x=rng.randint(0,100,80), y=rng.randint(0,100,80), z=rng.randint(0,100,80), mode='markers', marker=dict(size=3, color='#334155', opacity=0.5), hoverinfo='none'))
    cx, cy, cz = wx_scores.get('金', 50), wx_scores.get('木', 50), wx_scores.get('水', 50)
    f3d.add_trace(go.Scatter3d(x=[cx], y=[cy], z=[cz], mode='markers+text', text=[f"<b>COMMANDER: {dm_key}</b>"], textposition="top center", marker=dict(size=18, color=dm_color, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=dm_color, size=15, family="Orbitron")))
    f3d.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=350, showlegend=False)

    # 2. 六维雷达
    r_labels = ["力量(STR)", "敏捷(AGI)", "智力(INT)", "爆发(CRI)", "体质(CON)"]
    wx_v = [wx_scores.get('金',20), wx_scores.get('木',20), wx_scores.get('水',20), wx_scores.get('火',20), wx_scores.get('土',20)]
    f_radar = go.Figure(data=go.Scatterpolar(r=wx_v+[wx_v[0]], theta=r_labels+[r_labels[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color=dm_color, width=2), marker=dict(color='#fff', size=6)))
    f_radar.update_layout(polar=dict(radialaxis=dict(visible=False), angularaxis=dict(tickfont=dict(color='#fff', size=12, family="Orbitron"))), paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=10, b=10, l=30, r=30))
    
    # 3. 10年大运趋势 (满血回归)
    yrs = [str(datetime.now().year + i) for i in range(10)]
    trend = [rng.randint(40, 60)]
    for _ in range(9): trend.append(max(10, min(100, trend[-1] + rng.randint(-25, 30))))
    f_trend = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color="#f43f5e", width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)'))
    f_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False, tickfont=dict(color='#666', size=10)), yaxis=dict(showgrid=True, gridcolor='#222', tickfont=dict(color='#666', size=10)))
    
    # 4. 12个月天梯环境热力图 (满血回归)
    hm_z = rng.randint(20, 100, size=(4, 12)).tolist()
    hm_x = [f"{str(i).zfill(2)}月" for i in range(1, 13)]
    hm_y = ["财富(Gold)", "冲分(Rank)", "羁绊(Link)", "护甲(Def)"]
    f_hm = go.Figure(data=go.Heatmap(z=hm_z, x=hm_x, y=hm_y, colorscale="Turbo", showscale=False))
    f_hm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(t=10, b=10, l=60, r=10), xaxis=dict(tickfont=dict(family='Orbitron', color='#00f3ff', size=10)), yaxis=dict(tickfont=dict(family='Noto Sans SC', color='#fff', size=11)))
    
    return f3d, f_radar, f_trend, f_hm

def calc_tag_team(my_hash, partner_stem):
    rng_syn = np.random.RandomState(int(str(my_hash)[:6], 16) + sum(ord(c) for c in str(partner_stem)))
    score = rng_syn.randint(55, 99)
    if score >= 85: return score, "【UR 级连携】双卡羁绊爆发！全队属性飙升 50%！", "#ffaa00"
    elif score >= 70: return score, "【SR 级互补】战术互补，卡组容错率大幅提升。", "#00f3ff"
    else: return score, "【负面冲突】阵营排斥！强行双排将导致全队 Debuff！", "#f43f5e"

def trigger_gacha_draw(): st.session_state["gacha_drawn"] = True

# ==============================================================================
# 🔮 [ ENTRY POINT ] TCG 商店：抽取初始包
# ==============================================================================
is_booted = st.session_state.get("sys_booted", False)

if not is_booted:
    ENTRY_HTML = """
    <div class="ticker-wrap"><div class="ticker">
        <span>TCG MATRIX V100.0 <b class="up">▲BOOSTER PACK READY</b></span>
        <span>NEW BANNER: SOUL MATRIX <b class="ur" style="color:var(--sp);">★ SP RATE UP</b></span>
        <span>SERVER: GACHA ENGINE <b class="up">▲ONLINE</b></span>
    </div></div>
    <div style="text-align: center; margin-bottom: 25px; margin-top:5vh;">
        <div style="color:var(--sp); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:10px; margin-bottom:10px; text-shadow:0 0 10px var(--sp);">[ INSERT COIN TO PULL ]</div>
        <h1 class="hero-title" data-text="神之牌组终端">神之牌组终端</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:10px; margin-top:10px;">THE GOD GAME V100.0</div>
    </div>
    <div class="glass-panel" style="max-width: 680px; margin: 0 auto 30px auto; border-left: 4px solid var(--sp); padding: 35px; text-align:center;">
        <div style="color:var(--sp); font-size: 20px; font-weight:900; letter-spacing: 2px; margin-bottom:15px; text-shadow:0 0 10px var(--sp);">“如果命运是一场牌局，出生就是第一次抽卡。”</div>
        <div style="color:#e2e8f0; font-size: 15px; line-height: 1.8;">
            输入你的物理降临坐标，在赛博算力池中进行 <b style="color:#fff;">单次强力抽卡 (1x PULL)</b>。<br>
            系统将为你鉴定 <b style="color:var(--pink);">卡牌稀有度 (SR/SSR/UR/SP)</b> 与绝对战力值。<br>并全量解锁你的 <b style="color:var(--primary);">主战神卡</b> 与 <b style="color:var(--purple);">阿卡夏战备大盘</b>。
        </div>
    </div>
    """
    render_html(ENTRY_HTML)
    
    _, col_form, _ = st.columns([1, 2.5, 1])
    with col_form:
        with st.form(key="mint_form", border=False):
            col1, col2 = st.columns(2)
            with col1:
                uname = st.text_input("玩家代号 [PLAYER_ID]", placeholder="e.g. 银手", max_chars=12)
                bdate = st.date_input("降临历法 [SPAWN_DATE]", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(2000, 1, 1))
            with col2:
                ugender = st.selectbox("阵营倾向 [FACTION]", ["乾造阵营 (MALE)", "坤造阵营 (FEMALE)"])
                btime = st.time_input("挂载时钟 [SPAWN_TIME]", value=dt_time(12, 00))
            render_html("<br>")
            submit_btn = st.form_submit_button("🃏 消耗算力，撕开初始卡包 (OPEN PACK)", type="primary", use_container_width=True)

    if submit_btn:
        player_name = str(uname).strip() if uname else "Player_01"
        solar = Solar.fromYmdHms(bdate.year, bdate.month, bdate.day, btime.hour, btime.minute, 0)
        bazi = solar.getLunar().getEightChar()
        
        wx_str = str(bazi.getYearWuXing()) + str(bazi.getMonthWuXing()) + str(bazi.getDayWuXing()) + str(bazi.getTimeWuXing())
        wx_counts = {'金':0, '木':0, '水':0, '火':0, '土':0}
        for char in wx_str: 
            if char in wx_counts: wx_counts[char] += 1
        tot = sum(wx_counts.values()) or 1
        wx_scores = {k: int((v/tot)*100) for k, v in wx_counts.items()}
        
        # 🚨 [BUG 彻底剿灭] 全局统一替换为 EQUIPS_DICT，彻底解决 NameError 崩溃
        skills = []
        try:
            for sg in [bazi.getYearShiShenGan(), bazi.getMonthShiShenGan(), bazi.getTimeShiShenGan()]:
                if sg in EQUIPS_DICT and EQUIPS_DICT[sg] not in skills: 
                    skills.append(EQUIPS_DICT[sg])
            for shensha_list in [bazi.getYearZhiShenSha(), bazi.getMonthZhiShenSha(), bazi.getDayZhiShenSha(), bazi.getTimeZhiShenSha()]:
                for ss in shensha_list:
                    ss_name = ss.getName()
                    if ss_name in EQUIPS_DICT and EQUIPS_DICT[ss_name] not in skills:
                        skills.append(EQUIPS_DICT[ss_name])
        except Exception:
            pass

        if not skills: skills = ["【白板】无附加装备"]

        hash_id = hashlib.sha256((player_name + str(bdate) + str(btime)).encode()).hexdigest().upper()
        p_life = PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)]
        dm_key = str(bazi.getDayGan())
        
        dm_base = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"])
        rarity, r_col, cp, f_atk, f_def, f_hp = calc_tcg_stats(hash_id, wx_scores, dm_base.get("base_atk", 1000), dm_base.get("base_def", 1000), dm_base.get("hp", 8000), len(skills))

        st.session_state["sys_data"] = {
            "name": player_name, "gender": str(ugender).split(" ")[0],
            "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
            "day_master": dm_key, "past_life": p_life,
            "wx": wx_scores, "skills": skills, "hash": hash_id, "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "rarity": rarity, "r_col": r_col, "cp": cp,
            "atk": f_atk, "def": f_def, "hp": f_hp
        }
        
        # 🌟 狂暴的开包动画
        ph = st.empty()
        flash_color = "#00f3ff" if rarity=="SP" else ("#ffaa00" if rarity=="UR" else ("#fcee0a" if rarity=="SSR" else "#a855f7"))
        ph.markdown(f"<div style='height:40vh; display:flex; justify-content:center; align-items:center;'><div class='tcg-card' style='max-width:320px; aspect-ratio:63/88; box-shadow:0 0 100px {flash_color}; border:4px solid {flash_color}; background:#fff; animation: card-reveal 0.8s forwards;'><div style='color:#000; font-family:Orbitron; font-size:30px; font-weight:900; line-height:2; text-align:center;'><br>✦ TEARING PACK ✦<br><span style='font-size:60px;'>✨</span></div></div></div>", unsafe_allow_html=True)
        time.sleep(0.9)
        st.session_state["sys_booted"] = True
        st.rerun()

# ==============================================================================
# 🌟 [ TCG DASHBOARD ] 完美满血版对战大厅
# ==============================================================================
else:
    # 🚨 绝对安全的全局变量提取，杜绝所有 NameError
    d = st.session_state.get("sys_data", {})
    player_name = str(d.get('name', 'P1'))
    hash_id = str(d.get('hash', '0000000000')).ljust(8, '0')
    cp = d.get("cp", 50000) 
    
    dm_key = str(d.get('day_master', '甲'))
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    
    dm_class = str(dm_info.get("class_name", "Unknown"))
    dm_color = str(dm_info.get("color", "#00f3ff"))
    dm_desc = str(dm_info.get("desc", "..."))
    dm_wpn = str(dm_info.get("weapon", "无"))
    dm_skill = str(dm_info.get("skill", "无"))
    dm_mbti = str(dm_info.get("mbti", "UNK"))
    
    # 🚨【满血找回原版设定】：进化树与系统漏洞
    evo_raw = dm_info.get("evo_path", ["L1", "L2", "L3"])
    dm_evo = " ➔ ".join(evo_raw) if isinstance(evo_raw, list) else str(evo_raw)
    dm_ult = str(dm_info.get("ult_evo", "终极化神"))
    dm_flaw = str(dm_info.get("flaw", "未知漏洞"))
    dm_patch = str(dm_info.get("patch", "保持算法"))

    # 动态面板
    b_atk = d.get("atk", 5000)
    b_def = d.get("def", 5000)
    b_hp = d.get("hp", 8000)
    
    bz = [str(x) for x in d.get('bazi_arr', ['??', '??', '??', '??'])] 
    wx_scores = d.get('wx', {'金':20, '木':20, '水':20, '火':20, '土':20})
    skills_list = d.get('skills', ['无被动'])
    past_life = d.get('past_life', PAST_LIVES[0])
    
    rarity = str(d.get("rarity", "SR"))
    r_col_cls = str(d.get("r_col", "SR"))
    
    # 计算腐化度
    wx_vals = list(wx_scores.values())
    corruption = max(wx_vals) - min(wx_vals)
    corr_col = "#ff007c" if corruption > 60 else ("#fcee0a" if corruption > 30 else "#10b981")
    
    # 统一获取图表与法术卡 (所有原版图表 100% 满血回归)
    f3d, f_radar, f_trend, f_hm = gen_akashic_charts(hash_id, wx_scores, dm_color, dm_key)
    spell_card, date_str = pull_daily_spell(hash_id)
    sc_c = str(spell_card.get("color", "var(--primary)"))

    HEADER_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>TCG-ENGINE: V100.0 <b class="up">▲SYNCED</b></span>
        <span>PLAYER: {player_name} <b class="up">▲ACTIVE</b></span>
        <span>RARITY_PULLED: {rarity} <b class="ur">★ LOCKED</b></span>
    </div></div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid {dm_color}; padding-bottom:15px; margin-bottom:30px;">
        <div>
            <div style="font-family:'Fira Code'; color:#aaa; font-size:12px; margin-bottom:5px; font-weight:bold;">[ PLAYER WALLET: 0x{hash_id[:12]} ]</div>
            <div style="font-size:clamp(28px, 5vw, 40px); font-weight:900; color:#fff; font-family:'Orbitron'; line-height:1;">
                {player_name} 
                <span style="font-size:12px; background:{dm_color}; color:#000; padding:2px 8px; border-radius:2px; vertical-align:middle; font-weight:bold;">Lv.99</span>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="color:var(--sp); font-family:'Orbitron'; font-size:12px; font-weight:bold; margin-bottom:4px; letter-spacing:2px;">COMBAT POWER</div>
            <div style="font-size:clamp(28px, 4vw, 40px); font-family:'Orbitron'; font-weight:900; color:#fff; text-shadow:0 0 15px rgba(255,255,255,0.5); line-height:1;">CP {cp:,}</div>
        </div>
    </div>
    """
    render_html(HEADER_HTML)

    # =========================================================================
    # 🎴 模块 I & II：左侧 3D全息主将卡，右侧基础卡组与原版 Lore 补齐
    # =========================================================================
    c1, c2 = st.columns([1, 1.3], gap="large")

    with c1:
        render_html("<div class='mod-title'><span class='tag'>HERO</span> 本命主战神卡 (COMMANDER)</div>")
        
        # 🌟 核心黑科技：纯 CSS 3D 全息镭射实体卡牌 (不占 Python 性能)
        holo_fx = "holo-ur" if rarity in ["UR", "SP"] else ""
        TCG_CARD_HTML = f"""
        <div class="tcg-card-container">
            <div class="tcg-card rarity-{r_col_cls} {holo_fx}" style="color:{dm_color};">
                <div class="tcg-badge">{rarity}</div>
                <div class="card-header"><div class="card-title">{dm_key}</div><div class="card-class">{dm_mbti}</div></div>
                <div class="card-art-box"><div class="card-art-char">{dm_key}</div></div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">[ {dm_class} ]</div>
                    <div style="font-size:12px; font-weight:bold; color:var(--sp);">⚔️ {dm_wpn.split('】')[1] if '】' in dm_wpn else dm_wpn}</div>
                </div>
                <div class="card-desc-box">
                    <div style="color:{dm_color}; font-weight:bold; margin-bottom:6px; font-size:13px;">{dm_skill}</div>
                    <i>"{dm_desc}"</i>
                </div>
                <div class="card-stats-box">
                    <span style="color:#f43f5e;">ATK: {b_atk}</span><span style="color:#10b981;">HP: {b_hp}</span><span>DEF: {b_def}</span>
                </div>
            </div>
        </div>
        """
        render_html(TCG_CARD_HTML)

    with c2:
        render_html("<div class='mod-title'><span class='tag'>DECK</span> 基础卡组与体系面板 (LOADOUT)</div>")
        
        # 🌟 满血重塑：呈扇形展开的四张基础手牌！(悬浮抽出特效)
        hand_html = '<div class="hand-container">'
        labels = ["OS_YR", "ENV_MO", "CORE_DY", "THD_TM"]
        for i in range(4):
            is_core = (i == 2)
            c_cls = "hc-core" if is_core else ""
            c_col = dm_color if is_core else "#aaa"
            hand_html += f"""<div class="hand-card {c_cls}" style="color:{c_col};"><div class="hc-val">{bz[i][0]}</div><div class="hc-sub">{bz[i][1]}</div><div class="hc-tag">{labels[i]}</div></div>"""
        hand_html += '</div>'
        render_html(hand_html)

        # 🚨 【满血回归】原版的深度解析（演化路线、漏洞补丁）全部塞回玻璃面板！
        DEEP_LORE_HTML = f"""
        <div class="glass-panel" style="padding:15px; margin-bottom:15px; border-left-color:{dm_color};">
            <div style="background:rgba(0,0,0,0.6); padding:10px; border:1px solid #333; font-family:'Fira Code'; font-size:12px; margin-bottom:10px;">
                <div style="color:{dm_color}; margin-bottom:5px; font-weight:bold;">[ EVOLUTION TREE ] 进阶树</div>
                <div style="color:#aaa;">{dm_evo}</div>
                <div style="color:#fff; font-weight:bold; margin-top:5px;">终极形态: {dm_ult}</div>
            </div>
            <div style="background:rgba(244,63,94,0.1); border-left:3px solid var(--pink); padding:10px; font-family:'Fira Code'; font-size:12px;">
                <div style="color:var(--pink); font-weight:bold; margin-bottom:4px;">[ FATAL VULNERABILITY ] 致命隐患</div>
                <div style="color:#ddd; margin-bottom:5px;">{dm_flaw}</div>
                <div style="color:var(--green);">> SYS_COUNTER: {dm_patch}</div>
            </div>
        </div>
        """
        render_html(DEEP_LORE_HTML)

        c2_1, c2_2 = st.columns(2)
        with c2_1:
            sk_html = "".join([f"<div class='relic-item' style='color:{'var(--sp)' if '法术' in s else 'var(--primary)'};'>{s}</div>" for s in skills_list[:4]])
            render_html(f"<div class='glass-panel' style='padding:15px; border-left-color:var(--primary); height:160px; overflow-y:auto;'><div style='font-size:11px; color:var(--primary); font-family:Orbitron; margin-bottom:8px; font-weight:bold;'>>> EQUIPPED RELICS (外挂圣遗物)</div><div class='relic-grid'>{sk_html}</div></div>")
        with c2_2:
            render_html(f"""
            <div class="glass-panel" style="border-left-color:var(--yellow); padding:15px; height:160px; overflow-y:auto;">
                <div style="font-size:11px; color:var(--yellow); font-family:'Orbitron'; margin-bottom:5px; font-weight:bold;">>> KARMIC LORE (前世剧情)</div>
                <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:4px;">{past_life['title']}</div>
                <div style="color:#aaa; font-size:11px; line-height:1.5;">{past_life['debt']}</div>
            </div>
            """)

    # 🗄️ [ 模块 III ]：TCG 终极战术大厅 (所有图表、导出功能、合盘 100% 满血归位)
    render_html("<div class='mod-title' style='margin-top:20px;'><span class='tag'>NEXUS</span> 阿卡夏神域中枢 (THE GOD MATRIX)</div>")
    t_gacha, t_pve, t_map, t_syn, t_export = st.tabs(["🎲 盲盒神谕 (GACHA)", "⚔️ 矩阵深潜 (PVE)", "🌌 战局大盘 (STATS)", "🤝 羁绊匹配 (CO-OP)", "💼 资产确权 (MINT)"])

    with t_gacha:
        c_g1, c_g2 = st.columns([1.1, 1], gap="large")
        with c_g1:
            render_html("<div style='color:var(--sp); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ DAILY SPELL CARD ] 每日法术牌翻转</div>")
            render_html("<div style='font-size:12px; color:#aaa; margin-bottom:15px;'>系统免费派发一张法术牌。<b>请将鼠标移至下方卡牌进行悬停翻转 (Hover to Flip)！</b></div>")
            
            # 🚨【极致互动】纯 CSS 3D 翻牌特效
            yao_html = "".join([f"<div class='yao-yang' style='color:{sc_c};'></div>" if line == 1 else f"<div class='yao-yin'><div class='half' style='color:{sc_c};'></div><div class='half' style='color:{sc_c};'></div></div>" for line in reversed(spell_card['lines'])])
            FLIP_CARD_HTML = f"""
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size:60px; font-family:Orbitron; color:var(--primary); text-shadow:0 0 20px var(--primary);">?</div>
                    <div style="position:absolute; bottom:20px; font-family:Orbitron; font-size:10px; color:#888;">HOVER TO REVEAL</div>
                </div>
                <div class="flip-card-back" style="color:{sc_c}; display:flex; flex-direction:column; justify-content:center; padding:15px;">
                    <div style="font-family:'Orbitron'; font-size:10px; font-weight:bold; letter-spacing:2px; margin-bottom:10px;">[ {date_str} ]</div>
                    <div style="background:{sc_c}; color:#000; display:inline-block; padding:2px 10px; font-family:'Orbitron'; font-weight:900; font-size:12px; border-radius:2px; margin-bottom:10px; align-self:center;">{spell_card['type']}</div>
                    <div class="hex-container" style="margin-bottom:10px;">{yao_html}</div>
                    <div style="font-size:20px; font-weight:900; color:#fff; font-family:'Noto Sans SC'; margin-bottom:10px; text-shadow:0 0 10px {sc_c};">{spell_card['name']}</div>
                    <div style="background:rgba(0,0,0,0.6); padding:10px; border-radius:4px; text-align:left; border:1px solid rgba(255,255,255,0.1); font-size:11px; line-height:1.5; color:#ddd; margin-bottom:10px;">
                        <b style="color:{sc_c}; font-family:'Fira Code';">> EFFECT:</b><br>{spell_card['desc']}
                    </div>
                    <div style="font-size:11px; color:var(--green); font-weight:bold; text-align:left;">[+] 宜: {spell_card.get('do','')}</div>
                    <div style="font-size:11px; color:var(--pink); font-weight:bold; text-align:left; margin-top:4px;">[-] 忌: {spell_card.get('dont','')}</div>
                </div>
              </div>
            </div>
            """
            render_html(FLIP_CARD_HTML)
            
        with c_g2:
            render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ ACTION ROLL ] D100 行动暗骰检定</div>")
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:20px;'>像 TRPG 跑团一样，向阿卡夏主脑发起一个具体行动的成功率检定。</div>")
            @st_fragment
            def render_dice():
                ph = st.empty()
                with st.form(key="dice_form", clear_on_submit=False, border=False):
                    q_input = st.text_input("📝 输入检定事件：", placeholder="e.g. 今天买入这只股票能赚吗？", label_visibility="collapsed")
                    sub_q = st.form_submit_button("🎲 掷骰检定 (ROLL D100)", use_container_width=True)
                if sub_q:
                    if not q_input: ph.warning("⚠️ 语法错误：事件为空！")
                    else:
                        prob, hex_res, conc, q_c = roll_d100(q_input, hash_id)
                        RES = f"""
                        <div class="glass-panel card-reveal" style="margin-top:10px; border-color:{q_c}; text-align:center; border-left-width: 4px;">
                            <div style="font-family:'Fira Code'; color:#888; font-size:12px; margin-bottom:10px; word-wrap:break-word;">> ACTION: "{q_input}"</div>
                            <div style="font-size:11px; color:{q_c}; font-family:'Orbitron'; letter-spacing:2px; margin-bottom:5px;">[ D100 RESULT ]</div>
                            <div style="font-size:65px; font-weight:900; color:{q_c}; font-family:'Orbitron'; text-shadow:0 0 20px {q_c}; line-height:1; margin-bottom:15px;">{prob}</div>
                            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:5px;">触发机制：{hex_res['name']}</div>
                            <div style="font-size:12px; font-weight:bold; color:{q_c};">{conc}</div>
                        </div>
                        """
                        ph.markdown(RES, unsafe_allow_html=True)
            render_dice()

    with t_pve:
        # 🌟 全新 PVE Boss 挑战玩法！
        c_pve1, c_pve2 = st.columns([1, 1.2], gap="large")
        with c_pve1:
            render_html(f"""
            <div class="glass-panel" style="text-align:center; border-color:var(--pink);">
                <div style="font-size:50px; margin-bottom:10px;">👾</div>
                <div style="color:var(--pink); font-family:'Orbitron'; font-weight:900; font-size:18px;">MATRIX ICE / 矩阵黑冰</div>
                <div style="color:#aaa; font-size:12px; margin-bottom:15px;">[ 级别: S 级系统防火墙 ]</div>
                <div style="background:rgba(255,0,124,0.1); padding:10px; border-radius:4px; font-family:'Fira Code'; font-size:12px; color:#fff;">
                    HP: 250,000<br>ATK: 18,000
                </div>
            </div>
            """)
        with c_pve2:
            render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ BOSS RAID ] 赛博空间深潜战</div>")
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:20px;'>使用你的主将卡向矩阵底层 ICE 防火墙发起冲击。系统将基于你的 CP 战力自动推演战局。</div>")
            @st_fragment
            def render_raid():
                if st.button("⚔️ 发起深潜突击 (INITIATE RAID)", use_container_width=True):
                    ph = st.empty()
                    boss_hp = random.randint(120000, 250000)
                    win_chance = min(95, max(5, int((cp / 150000) * 100) + random.randint(-15, 15)))
                    
                    log_text = f"<div class='glass-panel' style='font-family:Fira Code; font-size:13px; line-height:1.8; color:var(--primary); border-left-color:var(--primary);'>"
                    log_text += f"<div style='color:#fff;'>> SYSTEM ROOT ACCESS REQUESTED...</div>"
                    log_text += f"<div>> TARGET: MATRIX ICE (HP: {boss_hp:,})</div>"
                    log_text += f"<div>> COMMANDER: {player_name} (CP: {cp:,})</div>"
                    log_text += f"<div style='color:var(--yellow);'>> CALCULATING WIN PROBABILITY: {win_chance}%</div><br>"
                    ph.markdown(log_text + "<span style='animation:blink 1s infinite;'>_</span></div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                    
                    log_text += f"<div style='color:var(--pink);'>> [TURN 1] 防火墙触发【数据风暴】！你的装甲抵挡了部分伤害...</div>"
                    ph.markdown(log_text + "<span style='animation:blink 1s infinite;'>_</span></div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                    
                    dmg = int((b_atk * 2.5 + b_def) * random.uniform(0.8, 1.5))
                    log_text += f"<div style='color:var(--green);'>> [TURN 2] 你发起了终极反击！造成了 {dmg:,} 点穿透伤害！</div>"
                    ph.markdown(log_text + "<span style='animation:blink 1s infinite;'>_</span></div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                    
                    if random.randint(1, 100) <= win_chance:
                        log_text += f"<br><div style='color:var(--sp); font-size:16px; font-weight:bold; text-shadow:0 0 10px var(--sp);'>> [VICTORY] 成功击穿 ICE 防火墙！获取 ROOT 权限！</div>"
                    else:
                        log_text += f"<br><div style='color:var(--pink); font-size:16px; font-weight:bold; text-shadow:0 0 10px var(--pink);'>> [DEFEAT] 算力耗尽，神经链接被强制阻断。</div>"
                        
                    ph.markdown(log_text + "</div>", unsafe_allow_html=True)
            render_raid()

    with t_map:
        # 🚨【满血回归】3D 星图、12月热力图、10年K线图全量包装为 TCG 竞技面板
        c_m1, c_m2 = st.columns([1.2, 1], gap="large")
        with c_m1:
            render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ DOMAIN EXPANSION ] 3D 全息战区投影</div>")
            st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False})
            
            render_html("<div style='font-size:12px; color:var(--pink); font-family:Orbitron; margin-top:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 10-YEAR WIN RATE ] 赛季大运胜率走势</div>")
            st.plotly_chart(f_trend, use_container_width=True, config={'displayModeBar': False})
        with c_m2:
            render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ COMBAT RADAR ] 六维战力雷达</div>")
            st.plotly_chart(f_radar, use_container_width=True, config={'displayModeBar': False})
            
            render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 12-MONTH META SHIFT ] 年度天梯环境热力图</div>")
            st.plotly_chart(f_hm, use_container_width=True, config={'displayModeBar': False})

    with t_syn:
        @st_fragment
        def render_synergy_section():
            c_l1, c_l2 = st.columns([1.2, 1], gap="large")
            with c_l1:
                render_html("<div style='font-size:14px; color:#aaa; margin-top:15px; margin-bottom:15px; font-weight:bold;'>选择目标队友的【主将卡】，测算双打 (Tag-Team) 时的连携共鸣率：</div>")
                opts = list(DAY_MASTER_DICT.keys())
                t_node = st.selectbox("🎯 选择助战位卡牌:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('tier', 'N')}] {x} - {DAY_MASTER_DICT.get(x, {}).get('class_name', 'UNK').split('/')[0]}")
            with c_l2:
                sc, sd, sc_color = calc_tag_team(hash_id, t_node)
                render_html(f"<div class='glass-panel card-reveal' style='border-left:4px solid {sc_color}; text-align:center; margin-top:15px;'><div style='font-family:\"Orbitron\"; font-size:12px; color:#888; letter-spacing:2px; margin-bottom:10px;'>TAG-TEAM RESONANCE</div><div style='font-family:\"Orbitron\"; font-size:60px; color:{sc_color}; font-weight:900; margin-bottom:10px; text-shadow:0 0 20px {sc_color}; line-height:1;'>{sc}%</div><div style='color:#fff; font-size:14px; font-weight:bold; font-family:\"Noto Sans SC\"; line-height:1.6;'>{sd}</div></div>")
        render_synergy_section()

    with t_web3:
        # 🚨【满血回归】智能合约与四大导出
        render_html("<div style='font-size:13px; color:#aaa; margin-top:15px; margin-bottom:10px;'>系统已将您的神权主将卡编译为标准的 Solidity ERC-721 智能合约源码，随时可上链铸造。</div>")
        contract_code = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@tcg-matrix/contracts/token/ERC721.sol";

contract Karma_TCG_V100 is ERC721 {{
    // ==========================================
    // > MINT_TARGET : {player_name}
    // > CARD_RARITY : {rarity} (CP: {cp})
    // > HASH_ID     : 0x{hash_id}
    // ==========================================
    
    function mintCommanderCard() public {{
        uint256 tokenId = uint256(keccak256(abi.encodePacked("{hash_id}")));
        _mint(msg.sender, tokenId);
    }}
}}"""
        st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
        st.code(contract_code, language="solidity")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_export:
        @st_fragment
        def render_exports():
            render_html("<div style='text-align:center; color:#888; font-size:13px; margin-top:10px; margin-bottom:15px;'>四大顶级资产导出中心。全量满血回归！</div>")
            e_psa, e_txt, e_json, e_asc = st.tabs(["📸 PSA 10 实体卡砖", "📜 万字机密档案 (.TXT)", "💾 极客 JSON 底包", "📟 ASCII 纯文本卡片"])
            
            with e_psa:
                c_e1, c_e2, c_e3 = st.columns([1, 2, 1])
                with c_e2:
                    if st.button("📸 压制 PSA 10 典藏卡砖 (MINT SLAB)", use_container_width=True):
                        sk_h = "".join([f"<span style='background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); color:#fff; padding:2px 6px; margin:2px; font-size:9px; display:inline-block; font-family:Fira Code; border-radius:2px;'>{s.split(' ')[1] if ' ' in s else s}</span>" for s in skills_list[:3]])
                        
                        # 🚨 终极安全渲染，完全避开 f-string 冲突。彻底消灭 NameError
                        HTML_POSTER_RAW = """
                        <!DOCTYPE html><html><head><meta charset="utf-8">
                        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700;900&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
                        <style>
                            body { margin:0; display:flex; justify-content:center; background:transparent; font-family:'Noto Sans SC'; color:#fff; }
                            #hide-box { position:absolute; top:-9999px; left:-9999px; }
                            /* PSA Slab 外壳质感 */
                            #slab { width:380px; background:linear-gradient(135deg, #e6e6e6, #ffffff, #d4d4d4); padding:15px; border-radius:12px; border:2px solid #bbb; box-shadow:inset 0 0 15px rgba(0,0,0,0.1), 0 20px 40px rgba(0,0,0,0.6); position:relative;}
                            .psa-label { background: linear-gradient(180deg, #d32f2f, #a00000); color:#fff; padding:10px 15px; border-radius:6px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center; border: 2px solid #ff5252; box-shadow: inset 0 2px 5px rgba(255,255,255,0.3);}
                            .psa-l { font-size:11px; font-weight:bold; line-height:1.4; }
                            .psa-r { text-align:right; } .psa-grade { font-family:'Orbitron'; font-size:28px; font-weight:900; background:#fff; color:#cc0000; padding:2px 8px; border-radius:4px; border:2px solid #cc0000;}
                            
                            /* 内部 TCG 卡牌 */
                            .card-inner { background:#050810; border-radius:8px; border:4px solid __COLOR__; padding:15px; position:relative; overflow:hidden; box-shadow:0 5px 15px rgba(0,0,0,0.5);}
                            .card-inner::after { content:""; position:absolute; top:0; left:0; width:100%; height:100%; background:linear-gradient(125deg, transparent 30%, rgba(255,255,255,0.15) 50%, transparent 70%); pointer-events:none; }
                            
                            .c-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #333; padding-bottom:8px;}
                            .h1 { font-family:'Noto Sans SC'; font-size:20px; font-weight:900; color:__COLOR__; letter-spacing:1px; text-shadow:0 0 10px __COLOR__;}
                            
                            .art-box { height: 160px; background:radial-gradient(circle at center, __COLOR__33, transparent), repeating-linear-gradient(45deg, #111, #111 10px, #1a1a1a 10px, #1a1a1a 20px); border:2px solid #444; border-radius:4px; display:flex; justify-content:center; align-items:center; margin-bottom:15px; position:relative; overflow:hidden; box-shadow:inset 0 0 20px rgba(0,0,0,0.8);}
                            .art-char { font-size:80px; font-weight:900; color:__COLOR__; opacity:0.9; font-family:'Noto Sans SC', serif; text-shadow: 0 0 20px __COLOR__;}
                            
                            .desc-box { background:rgba(0,0,0,0.8); border:1px solid #333; padding:10px; border-radius:4px; font-size:11px; line-height:1.5; color:#ccc; margin-bottom:10px;}
                            .cp-text { font-family:'Orbitron'; font-size:24px; font-weight:900; color:#fcee0a; text-align:right; margin-bottom:5px; text-shadow:0 0 10px #fcee0a;}
                            
                            #ui-loading { color:__COLOR__; font-family:'Orbitron'; padding:40px; text-align:center; font-weight:bold; letter-spacing:2px; animation:blink 1s infinite alternate;}
                            @keyframes blink { 0% {opacity:1;} 100% {opacity:0.3;} }
                            #final-img { display:none; width:100%; max-width:380px; box-shadow:0 15px 40px rgba(0,0,0,0.9); border-radius:12px; margin-top:10px; margin: 0 auto;}
                        </style></head><body>
                        <div id="hide-box"><div id="slab">
                            
                            <div class="psa-label">
                                <div class="psa-l">
                                    <div style="font-size:15px; font-family:'Orbitron'; margin-bottom:2px;">__PLAYER__</div>
                                    <div>DESTINY TCG - FIRST EDITION</div>
                                    <div style="font-family:'Fira Code'; font-size:9px;">HASH: 0x__HASH__</div>
                                </div>
                                <div class="psa-r">
                                    <div style="font-size:9px; font-weight:bold; margin-bottom:4px;">GEM MINT</div>
                                    <div class="psa-grade">10</div>
                                </div>
                            </div>
                            
                            <div class="card-inner">
                                <div class="c-head">
                                    <div class="h1">__DM_KEY__ · __CLASS__</div>
                                    <div style="font-family:'Orbitron'; font-size:18px; font-weight:900; background:__COLOR__; color:#000; padding:2px 8px; border-radius:2px;">__TIER__</div>
                                </div>
                                
                                <div class="art-box"><div class="art-char">__DM_KEY__</div></div>
                                <div class="cp-text">CP __CP__</div>
                                
                                <div class="desc-box">
                                    <div style="color:__COLOR__; font-weight:bold; margin-bottom:4px;">⚔️ __WPN__</div>
                                    <div style="color:#fff; font-weight:bold; margin-bottom:6px;">__SKILL__</div>
                                    <i>"__DESC__"</i>
                                </div>
                                
                                <div style="text-align:center; margin-bottom:10px;">__EQUIPS__</div>
                                
                                <div style="display:flex; justify-content:space-between; font-family:'Orbitron'; font-size:14px; font-weight:bold; color:#fff; border-top:1px solid #333; padding-top:8px;">
                                    <span style="color:#f43f5e;">ATK: __ATK__</span><span style="color:#10b981;">HP: __HP__</span>
                                </div>
                                
                                <div style="text-align:right; font-family:'Orbitron'; font-size:8px; color:#666; margin-top:10px;">© 2026 THE GOD GAME</div>
                            </div>
                        </div></div>

                        <div id="ui-loading">>>> ENCAPSULATING SLAB...</div>
                        <img id="final-img" />
                        
                        <script>
                            setTimeout(() => {
                                html2canvas(document.getElementById('slab'), { scale:2, backgroundColor:'transparent', logging:false }).then(canvas => {
                                    document.getElementById('final-img').src = canvas.toDataURL('image/png');
                                    document.getElementById('ui-loading').style.display = 'none';
                                    document.getElementById('final-img').style.display = 'block';
                                    document.getElementById('hide-box').innerHTML = '';
                                });
                            }, 500);
                        </script>
                        </body></html>
                        """
                        
                        html_ready = HTML_POSTER_RAW.replace("__COLOR__", dm_color).replace("__PLAYER__", player_name.upper())
                        html_ready = html_ready.replace("__HASH__", hash_id[:10]).replace("__DM_KEY__", dm_key).replace("__CLASS__", dm_class.split('/')[0].strip())
                        html_ready = html_ready.replace("__TIER__", rarity).replace("__CP__", f"{cp:,}")
                        html_ready = html_ready.replace("__WPN__", dm_wpn).replace("__SKILL__", dm_skill).replace("__DESC__", dm_desc)
                        html_ready = html_ready.replace("__EQUIPS__", sk_h).replace("__ATK__", str(b_atk)).replace("__HP__", str(b_hp))
                        
                        components.html(html_ready, height=750)
            
            with e_txt:
                TXT_LORE = f"""======================================
[ THE GOD GAME V100.0 ] 绝密卡组大纲 
======================================

>> 1. 玩家档案 (PLAYER DATA)
▸ 身份：{player_name} ({d.get('gender', 'X')})
▸ 哈希：0x{hash_id}
▸ 战力：{cp:,} CP [{rarity}]

>> 2. 底层卡组 (DECK LOADOUT)
▸ {bz[0]} (年) | {bz[1]} (月) | {bz[2]} (日) | {bz[3]} (时)

>> 3. 主将设定 (COMMANDER LORE)
▸ 代号：{dm_key} ({dm_info.get('element', '')}系)
▸ 职阶：{dm_class}
▸ MBTI：[ {dm_mbti} ]
▸ 动态面板：ATK {b_atk} | DEF {b_def} | HP {b_hp}
▸ 特质：{dm_desc}
▸ 武装：{dm_wpn}
▸ 技能：{dm_skill}

>> 4. 终极演化与系统漏洞 (EVOLUTION & PATCH)
▸ 觉醒路线：{dm_evo}
▸ 究极化神：{dm_ult}
▸ 致命隐患：{dm_flaw}
▸ 应对方案：{dm_patch}

>> 5. 业力与武装 (KARMA & EQUIPS)
▸ 前世残存：{past_life['title']} ({past_life['debt']})
▸ 挂载装备/圣遗物：{', '.join(skills_list)}

======================================
© 2026 NIGHT CITY DAO. ALL RIGHTS RESERVED.
======================================"""
                st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
                st.code(TXT_LORE, language="markdown")
                st.markdown('</div>', unsafe_allow_html=True)
                st.download_button(label="📥 下载深度绝密档案 (.TXT)", data=TXT_LORE, file_name=f"LORE_{player_name}.txt", mime="text/plain", use_container_width=True)

            with e_json:
                export_data = {
                    "version": VERSION, "player": player_name, "rarity": rarity, "cp": cp,
                    "commander": { "id": dm_key, "class": dm_class, "atk": b_atk, "def": b_def, "hp": b_hp, "evolution": dm_ult, "flaw": dm_flaw, "patch": dm_patch },
                    "deck": bz, "equips": skills_list, "lore": past_life,
                    "wuxing": wx_scores, "hash": hash_id
                }
                st.download_button(label="📥 下载 TCG 底包 (JSON)", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"CARD_{hash_id[:6]}.json", mime="application/json", use_container_width=True)

            with e_asc:
                render_html("<div style='font-size:13px; color:var(--green); margin-top:10px; margin-bottom:10px; font-family:Fira Code;'>> 最纯正的极客浪漫。一键复制下方代码块发送至群聊，绝不乱码。</div>")
                def m_b(v): return "█" * int(v/100*16) + "░" * (16 - int(v/100*16))
                ASC_TEMP = f"""```text
========================================================
 ███▄    █  ▓█████  ▒█████     █████▒▄▄▄       ██████ 
 ██ ▀█   █  ▓█   ▀ ▒██▒  ██▒ ▓██   ▒▒████▄   ▒██    ▒ 
▓██  ▀█ ██▒ ▒███   ▒██░  ██▒ ▒████ ░▒██  ▀█▄ ░ ▓██▄   
========================================================
> PLAYER : {player_name} 
> CP_VAL : {cp:,} CP [{rarity}]
--------------------------------------------------------
[ CORE DECK / 主战卡组 ]
  {bz[0]}   |   {bz[1]}   | >> {bz[2]} << |   {bz[3]}

[ COMMANDER / 主将面板 ]
> NAME   : {dm_key} ({dm_class.split('/')[0].strip()})
> WEAPON : {dm_wpn}
> STATS  : ATK {b_atk} | DEF {b_def} | HP {b_hp}

[ RADAR / 属性水晶 ]
  STR(金) : {wx_scores.get('金',0):02d}% |{m_b(wx_scores.get('金',0))}|
  AGI(木) : {wx_scores.get('木',0):02d}% |{m_b(wx_scores.get('木',0))}|
  INT(水) : {wx_scores.get('水',0):02d}% |{m_b(wx_scores.get('水',0))}|
  CRI(火) : {wx_scores.get('火',0):02d}% |{m_b(wx_scores.get('火',0))}|
  CON(土) : {wx_scores.get('土',0):02d}% |{m_b(wx_scores.get('土',0))}|
========================================================
```"""
                st.markdown(ASC_TEMP)

        render_exports()

    # =========================================================================
    # ⌨️ [ TERMINAL ] 内联极简指令台
    # =========================================================================
    st.markdown("---")
    @st_fragment
    def render_terminal():
        current_logs = st.session_state.get("term_logs", ["> TCG_ENGINE READY."])
        log_html = "<br>".join(current_logs[-4:])
        render_html(f"<div style='max-width: 800px; margin: 0 auto; background:#000; border:1px solid #333; padding:15px; font-family:\"Fira Code\"; color:var(--primary); font-size:13px; height:120px; display:flex; flex-direction:column-reverse; overflow:hidden; border-left:4px solid var(--primary);'><div>{log_html}<span style=\"animation:blink 1s infinite;\">_</span></div></div>")

        with st.form("inline_terminal", clear_on_submit=True, border=False):
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1:
                cmd_input = st.text_input("CMD", label_visibility="collapsed", placeholder="> ROOT:~# 输入指令 (如: /rank, /clear)...")
            with col_t2:
                sub_cmd = st.form_submit_button("⏎", use_container_width=True)
                
            if sub_cmd and cmd_input:
                cmd_str = str(cmd_input).strip()
                logs = st.session_state.get("term_logs", [])
                logs.append(f"<span style='color:#fff;'>> {cmd_str}</span>")
                cmd_lower = cmd_str.lower()
                if cmd_lower == '/help': logs.append("<span style='color:#aaa;'>CMDS: /rank, /ping, /clear</span>")
                elif cmd_lower == '/rank': logs.append(f"<span style='color:var(--sp);'>[SYS] 您的当前战力(CP {cp:,})击败了全服 87.4% 的玩家。</span>")
                elif cmd_lower == '/clear': logs = ["> TERMINAL CLEARED."]
                elif cmd_lower == '/ping': logs.append("<span style='color:var(--yellow);'>[PONG] 发牌员延迟 0.00ms. 「玄不救非，氪不改命。」</span>")
                else: logs.append(f"<span style='color:var(--pink);'>[ERR] Bad Command.</span>")
                st.session_state["term_logs"] = logs[-15:]
                st.rerun()
    render_terminal()

    # 底部退出按钮
    render_html("<br><br>")
    _, col_b_m, _ = st.columns([1,2,1])
    with col_b_m:
        if st.button("⏏ [ SURRENDER ] 结束回合并退出", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================================================================
# 🛑 [ KERNEL 07 ] 版权
# =========================================================================
render_html(f'<div style="text-align:center; margin-top:30px; border-top: 1px dashed #222; padding-top: 30px; padding-bottom: 50px;"><div style="color:#666; font-family:\'Orbitron\'; font-size:11px; letter-spacing:4px;">© 2026 {COPYRIGHT}</div></div>')
