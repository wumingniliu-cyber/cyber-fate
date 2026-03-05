import streamlit as st
import streamlit.components.v1 as components  # 🚨 物理级焊死！绝不丢失渲染引擎
import random
import time
import math  # 🚨 物理级焊死计算引擎！
import hashlib
import json
from datetime import datetime, time as dt_time

# ==============================================================================
# 🛡️ [ KERNEL 00 ] 物理级防爆装甲 
# ==============================================================================
try:
    import numpy as np
    import plotly.graph_objects as go
    from lunar_python import Solar
except ImportError as e:
    st.set_page_config(page_title="SYS.PANIC", page_icon="🚨", layout="centered")
    st.error(f"🚨 **FATAL ERROR: 缺少核心模块 `{e.name}`**\n\n请配置 requirements.txt: streamlit, lunar-python, plotly, numpy。")
    st.stop()

try:
    from streamlit import fragment as st_fragment
except ImportError:
    def st_fragment(func): return func

# ==============================================================================
# 🌌 [ GLOBALS ] 无名逆流 · 数据人生 工业级状态机
# ==============================================================================
VERSION = "DATA LIFE TCG V300.0 [INDUSTRIAL SYNERGY]"
COPYRIGHT = "无名逆流"
SYS_NAME = "数据人生 | 工业级赛博修仙"

st.set_page_config(page_title=SYS_NAME, page_icon="🎴", layout="wide", initial_sidebar_state="collapsed")

# 🚨 工业级大一统状态机：所有模块共享底层数据，彻底解决联动断层！
if "db" not in st.session_state:
    st.session_state["db"] = {
        "booted": False,
        "player": {}, # 八字与基础面板
        "shop": {"creds": 0, "relics": [], "b_atk": 0, "b_def": 0, "b_hp": 0, "b_cp": 0},
        "buffs": {
            "oracle_drawn": False, 
            "oracle_data": {"name": "未挂载神谕", "atk_mul": 1.0, "def_mul": 1.0, "hp_mul": 1.0, "desc": "无增益"},
            "syn_linked": False, 
            "syn_data": {"name": "孤狼模式(无道侣)", "atk_mul": 1.0, "hp_mul": 1.0, "def_mul": 1.0, "cp_bonus": 0, "desc": "无加成"}
        },
        "pve": {"idx": 0, "boss_hp": 12000, "boss_max": 12000, "curr_hp": 0, "logs": [f"> [{COPYRIGHT}] MATRIX INITIATED..."]},
        "term_logs": [f"> THE MATRIX BY {COPYRIGHT} INITIALIZED..."]
    }

# 联动模块 3：PVE 进度 (重新平衡梯度，初始包可打过 L1，后续需要抽卡和 Buff)
BOSS_ROSTER = [
    {"lvl": 1, "name": "L1 算法过滤网", "max_hp": 12000, "atk": 800, "reward": 1000, "desc": "出身与学历的初始矩阵拦截。无Buff也可强杀。"},
    {"lvl": 2, "name": "L2 职场剥削阵列", "max_hp": 45000, "atk": 3500, "reward": 3000, "desc": "吞噬生命算力的无情永动机。建议去黑市抽点装备。"},
    {"lvl": 3, "name": "L3 消费主义巨兽", "max_hp": 150000, "atk": 12000, "reward": 8000, "desc": "资本编织的极乐迷幻网。必须抽每日神谕加持方可一战。"},
    {"lvl": 4, "name": "L4 黑天鹅风暴", "max_hp": 450000, "atk": 30000, "reward": 20000, "desc": "真实的因果律打击。若不绑定高分道侣，必死无疑。"},
    {"lvl": 5, "name": "L5 阿卡夏主脑", "max_hp": 1500000, "atk": 80000, "reward": 100000, "desc": "统御世界线的神明，击碎它即可逆天改命！"}
]

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in str(html_str).split('\n')]), unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ CSS ENGINE ] 满级 3D 视觉与工业级 UI
# ==============================================================================
STATIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root { --sp: #ffaa00; --ur: #ff007c; --ssr: #fcee0a; --sr: #a855f7; --r: #00f3ff; --primary: #00f3ff; --bg-dark: #020306; }
html, body, .stApp { background-color: var(--bg-dark) !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; cursor: crosshair !important; }

/* 🚨 物理级消灭原生白边 */
[data-testid="stHeader"], footer, section[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] { display: none !important; margin: 0 !important; padding: 0 !important; height: 0 !important;}
::-webkit-scrollbar { width: 6px; background: #000; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; box-shadow: 0 0 10px var(--primary);}
.block-container { max-width: 1400px !important; padding-top: 1.5rem !important; padding-bottom: 3rem !important; overflow-x: hidden; }

/* 赛博网格动画 */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.7) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px), linear-gradient(0deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px); background-size: 100% 3px, 50px 50px, 50px 50px; z-index: -1; transform: perspective(600px) rotateX(20deg); transform-origin: top; opacity: 0.8; pointer-events: none;}
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 35%, transparent 5%, rgba(2, 3, 5, 1) 85%); z-index: -2; pointer-events: none;}

/* 跑马灯 */
.ticker-wrap { width: 100vw; overflow: hidden; height: 35px; background: rgba(2, 3, 6, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 20px rgba(0,243,255,0.15); transform: translateZ(0); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 35s linear infinite; font-family: 'Orbitron', monospace; font-size: 13px; color: #888; line-height: 35px; letter-spacing: 1px; }
.ticker span { margin-right: 50px; } .ticker .hl { color: var(--primary); font-weight:bold; } .ticker .ur { color: var(--sp); text-shadow: 0 0 10px var(--sp); font-weight:bold; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* 🌟 主将实体卡牌 (Holo-Foil) */
.tcg-card-container { perspective: 1200px; display: flex; justify-content: center; margin-bottom: 20px; z-index: 50; position:relative;}
.tcg-card { position: relative; width: 100%; max-width: 380px; aspect-ratio: 63 / 88; background: #0a0c10; border: 3px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,0,0,0.6); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease; overflow: hidden; transform-style: preserve-3d; display: flex; flex-direction: column; cursor: crosshair; }
.tcg-card::after { content: ""; position: absolute; top: -50%; left: -150%; width: 150%; height: 200%; background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.6) 30%, rgba(0, 243, 255, 0.6) 40%, rgba(255, 0, 124, 0.4) 50%, transparent 60%); transform: skewX(-20deg); transition: all 0.6s ease; z-index: 99; pointer-events: none; mix-blend-mode: color-dodge; opacity: 0; }
.tcg-card:hover { transform: translateY(-15px) rotateX(10deg) rotateY(-8deg) scale(1.02); box-shadow: -20px 30px 50px rgba(0,0,0,1), inset 0 0 40px rgba(255,255,255,0.15); z-index: 10; border-color: currentColor; }
.tcg-card:hover::after { animation: foil-sweep 2.5s infinite linear; opacity: 1; }
@keyframes foil-sweep { 0% { left: -150%; } 100% { left: 200%; } }

.rarity-SP { border-color: var(--sp) !important; color: var(--sp); box-shadow: 0 10px 40px rgba(255,170,0,0.5), inset 0 0 30px rgba(255,170,0,0.2) !important; }
.rarity-UR { border-color: var(--ur) !important; color: var(--ur); box-shadow: 0 10px 40px rgba(255,0,124,0.4), inset 0 0 30px rgba(255,0,124,0.2) !important; }
.rarity-SSR { border-color: var(--ssr) !important; color: var(--ssr); box-shadow: 0 10px 40px rgba(252,238,10,0.3) !important; }
.rarity-SR { border-color: var(--sr) !important; color: var(--sr); }
.rarity-R { border-color: var(--r) !important; color: var(--r); }

.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 12px; margin-bottom: 15px; z-index:2;}
.card-title { font-size: 32px; font-weight: 900; font-family: 'Noto Sans SC', sans-serif; text-shadow: 0 0 20px currentColor; margin: 0; line-height: 1;}
.card-class { font-family: 'Orbitron'; font-weight: 900; font-size: 15px; color:#000; background:currentColor; padding:4px 10px; border-radius:4px; box-shadow:0 0 10px currentColor;}
.card-art-box { flex: 1; background: radial-gradient(circle at center, currentColor 0%, transparent 70%), repeating-linear-gradient(45deg, #111, #111 10px, #1a1a1a 10px, #1a1a1a 20px); border: 2px solid rgba(255,255,255,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; box-shadow: inset 0 0 50px rgba(0,0,0,0.9); overflow: hidden; position: relative;}
.card-art-char { font-size: 110px; font-weight: 900; font-family: 'Noto Sans SC', serif; text-shadow: 0 0 50px #000; color:#fff; z-index:2; }
.card-desc-box { font-size: 12px; color: #d1d5db; line-height: 1.6; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 4px; border-left: 4px solid currentColor; margin-bottom: 15px; z-index:2;}
.card-stats-box { display: flex; justify-content: space-between; font-family: 'Orbitron'; font-size: 16px; font-weight: bold; background: rgba(255,255,255,0.1); padding: 12px 18px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3); color: #fff; z-index:2;}
.stat-bonus { color: var(--green); font-size: 12px; text-shadow: 0 0 5px var(--green); }
.tcg-badge { position:absolute; top:-2px; right:-2px; background:currentColor; color:#000; font-family:'Orbitron'; font-weight:900; font-size:20px; padding:6px 30px; border-radius:0 14px 0 16px; z-index:15; box-shadow:-2px 2px 15px rgba(0,0,0,0.6);}

/* 🌟 扇形手牌系统 */
.hand-container { display: flex; justify-content: center; align-items: center; margin-top: 20px; height: 180px; position: relative; perspective: 1000px; margin-bottom:30px;}
.hand-card { width: 110px; height: 150px; background: linear-gradient(180deg, rgba(20,20,30,0.95) 0%, #050608 100%); border: 2px solid #444; border-radius: 8px; position: absolute; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; box-shadow: -5px 10px 20px rgba(0,0,0,0.6); }
.hand-card .hc-val { font-size: 32px; font-weight: 900; font-family: 'Noto Sans SC'; color: #fff; line-height: 1; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
.hand-card .hc-sub { font-size: 16px; color: #888; margin-top: 5px; }
.hand-card .hc-tag { position: absolute; bottom: 8px; font-size: 10px; font-family: 'Orbitron'; font-weight: bold; color: #666; letter-spacing: 1px; }

.hand-card:nth-child(1) { transform: translateX(-140px) translateY(20px) rotate(-15deg); z-index: 1; }
.hand-card:nth-child(2) { transform: translateX(-50px) translateY(5px) rotate(-5deg); z-index: 2; }
.hand-card:nth-child(3) { transform: translateX(50px) translateY(5px) rotate(5deg); z-index: 3; }
.hand-card:nth-child(4) { transform: translateX(140px) translateY(20px) rotate(15deg); z-index: 4; }

.hand-card:hover { border-color: var(--primary); box-shadow: 0 0 30px rgba(0,243,255,0.4); z-index: 10 !important; }
.hand-card:nth-child(1):hover { transform: translateX(-150px) translateY(-25px) rotate(-5deg) scale(1.15); }
.hand-card:nth-child(2):hover { transform: translateX(-60px) translateY(-25px) rotate(0deg) scale(1.15); }
.hand-card:nth-child(3):hover { transform: translateX(60px) translateY(-25px) rotate(0deg) scale(1.15); }
.hand-card:nth-child(4):hover { transform: translateX(150px) translateY(-25px) rotate(5deg) scale(1.15); }
.hc-core { border-color: currentColor !important; box-shadow: 0 0 15px currentColor !important; background: linear-gradient(180deg, rgba(0,0,0,0.8), currentColor) !important; }

/* 3D 翻转神谕卡 */
.flip-card { background-color: transparent; perspective: 1200px; width: 100%; max-width: 320px; aspect-ratio: 63/88; margin: 0 auto; cursor: pointer; }
.flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-style: preserve-3d; box-shadow: 0 20px 40px rgba(0,0,0,0.8); border-radius: 16px;}
.flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: 16px; overflow:hidden;}
.flip-card-front { background: repeating-linear-gradient(45deg, #050810, #050810 10px, #0a0f1a 10px, #0a0f1a 20px); border: 4px solid var(--primary); display:flex; flex-direction: column; align-items:center; justify-content:center; box-shadow: inset 0 0 30px rgba(0,243,255,0.3);}
.flip-card-back { background: #050810; transform: rotateY(180deg); border: 4px solid currentColor; box-shadow: inset 0 0 50px rgba(0,0,0,0.9);}

/* 通用组件 */
.relic-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 10px; }
.relic-item { background: rgba(0,0,0,0.6); border: 1px solid #333; border-left: 3px solid currentColor; padding: 10px; border-radius: 4px; font-size: 12px; color: #fff; font-weight: bold; font-family: 'Noto Sans SC'; box-shadow: inset 0 0 10px rgba(255,255,255,0.02); transition: all 0.2s; display: flex; align-items: center;}
.relic-item:hover { background: rgba(255,255,255,0.05); border-color: currentColor; transform: translateX(3px); }

.glass-panel { background: rgba(8, 10, 15, 0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: transform 0.3s; position:relative;}
.glass-panel:hover { border-color: rgba(255,255,255,0.3); transform: translateY(-2px); }
.mod-title { color: #fff; font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 900; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 8px; margin-bottom: 20px; display: flex; align-items: center; letter-spacing: 1px; }
.mod-title span.tag { background: var(--primary); color: #000; padding: 2px 10px; margin-right: 12px; font-size: 0.9rem; font-weight:bold; clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }

/* PVE 动态血条 */
.hp-bar-bg { width: 100%; height: 16px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; position: relative; margin-bottom: 5px; border: 1px solid rgba(255,255,255,0.2); }
.hp-bar-fill { height: 100%; position: absolute; top: 0; left: 0; transition: width 0.4s cubic-bezier(0.175, 0.885, 0.32, 1); }
.hp-red { background: linear-gradient(90deg, #800000, #ff003c); box-shadow: 0 0 10px #ff003c; }
.hp-green { background: linear-gradient(90deg, #004d40, #10b981); box-shadow: 0 0 10px #10b981; }

div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--sp) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(255,170,0,0.4) !important; border-radius: 4px !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; text-align: center; }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(255,170,0,0.4) !important; color: var(--sp) !important; border-radius: 4px !important; height: 55px; text-align:center;}

div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(15,15,20,0.9)) !important; border: 1px solid var(--primary) !important; border-left: 4px solid var(--primary) !important; height: 55px !important; width: 100% !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); transition: all 0.2s;}
div.stButton > button p { color: #fff !important; font-size: 15px !important; font-weight: bold !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: scale(1.02); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #ffaa00) !important; border: none !important; box-shadow: 0 0 30px rgba(255,0,124,0.5) !important;}

[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 15px !important; padding-bottom: 12px !important; border-bottom: 2px solid transparent !important; transition: all 0.3s;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; text-shadow: 0 0 15px var(--primary); background: linear-gradient(0deg, rgba(0,243,255,0.15) 0%, transparent 100%); border-radius: 4px 4px 0 0;}

@keyframes pack-shake { 0% { transform: scale(1) rotate(0deg); } 25% { transform: scale(1.05) rotate(-3deg); filter: brightness(1.5);} 50% { transform: scale(1.05) rotate(3deg); filter: brightness(2);} 75% { transform: scale(1.05) rotate(-3deg); filter: brightness(3);} 100% { transform: scale(1.2) rotate(0deg); filter: brightness(5) drop-shadow(0 0 50px #fff); opacity: 0; } }
.pack-opening { animation: pack-shake 1.0s ease-in forwards; }
.card-reveal { animation: card-reveal-anim 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
@keyframes card-reveal-anim { 0% { transform: scale(0.5) translateY(50px); opacity: 0;} 100% { transform: scale(1) translateY(0); opacity: 1;} }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }

.hex-container { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; margin: 15px 0; }
.yao-yang { width: 100%; max-width: 140px; height: 10px; border-radius: 2px; animation: pulse-glow 2s infinite alternate; }
.yao-yin { width: 100%; max-width: 140px; height: 10px; display: flex; justify-content: space-between; gap: 15px; }
.yao-yin .half { flex: 1; border-radius: 2px; animation: pulse-glow 2s infinite alternate-reverse; }
@keyframes pulse-glow { 0% { filter: brightness(0.8); box-shadow: 0 0 5px currentColor; } 100% { filter: brightness(1.2); box-shadow: 0 0 20px currentColor; } }
</style>
"""
st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ==============================================================================
# 🗃️ [ DICTIONARY ] 数据人生映射库 & 深度 Lore
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"class_name": "Root Paladin / 根基骑士", "mbti": "ENTJ", "color": "#10b981", "element": "木", "tier": "UR", "base_atk": 2500, "base_def": 4000, "hp": 12000, "desc": "掌控底层因果的重装核心。", "weapon": "高分子动能巨斧", "skill": "[被动] 建木庇护：受致命伤触发锁血。", "evo_path": "架构幼苗 ➔ 核心骨干 ➔ 苍天建木", "ult_evo": "【苍天建木】执掌三界底层协议", "flaw": "过于刚硬，遇强则折。遭遇降维打击易宕机。", "patch": "引入水属性柔性冗余，挂起进程等待重启。"},
    "乙": {"class_name": "Net Assassin / 暗网刺客", "mbti": "ENFP", "color": "#a855f7", "element": "木", "tier": "SSR", "base_atk": 3800, "base_def": 1500, "hp": 8500, "desc": "敏锐的爬虫，在敌方后排疯狂窃取权限。", "weapon": "量子绞杀魔藤", "skill": "[主动] 寄生吸血：每次攻击窃取算力补给自身。", "evo_path": "寄生节点 ➔ 渗透猎手 ➔ 噬星魔藤", "ult_evo": "【噬星魔藤】寄生控制全网资源", "flaw": "极度依赖宿主，宿主阵亡则自身属性减半。", "patch": "采用分布式多宿主绑定协议分散风险。"},
    "丙": {"class_name": "Burst Mage / 爆裂法师", "mbti": "ESTP", "color": "#ff007c", "element": "火", "tier": "UR", "base_atk": 4800, "base_def": 1200, "hp": 8000, "desc": "绝对输出核心。爆发毁天灭地的光芒。", "weapon": "等离子破城炮", "skill": "[终极] 恒星耀斑：暴击率强制提升至 100%。", "evo_path": "点火程序 ➔ 核聚变堆 ➔ 恒星引擎", "ult_evo": "【恒星引擎】照亮并驱动整个纪元", "flaw": "全功率输出易导致内核熔毁自爆。", "patch": "强制加装土属性散热栅栏，波谷进入待机。"},
    "丁": {"class_name": "Enchanter / 精神附魔", "mbti": "INFJ", "color": "#ffaa00", "element": "火", "tier": "SSR", "base_atk": 2000, "base_def": 2500, "hp": 9000, "desc": "在最灰暗战局中提供精神增益与破防制导。", "weapon": "高聚能激光短刃", "skill": "[光环] 灵魂织网：全队获得 40% 护甲穿透。", "evo_path": "寻路信标 ➔ 精神图腾 ➔ 灵魂织网者", "ult_evo": "【灵魂织网者】操控全网心智的网络幽灵", "flaw": "能量波动不稳定，容易被清场 AOE 一波带走。", "patch": "需绑定甲木系主T作为遮风挡雨的掩体。"},
    "戊": {"class_name": "Fortress / 物理堡垒", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "tier": "UR", "base_atk": 1500, "base_def": 5000, "hp": 15000, "desc": "物理级断网防御力，最坚不可摧的坦位。", "weapon": "绝对零度力场盾", "skill": "[被动] 盖亚装甲：免疫一次致死级打击。", "evo_path": "承载沙盒 ➔ 巨石阵列 ➔ 盖亚装甲", "ult_evo": "【盖亚装甲】承载万物因果的绝对壁垒", "flaw": "系统庞大笨重，面临敏捷迭代时易卡死。", "patch": "接纳木属性破坏性创新打破死锁。"},
    "己": {"class_name": "Summoner / 云端召唤", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "tier": "SSR", "base_atk": 1800, "base_def": 3800, "hp": 11000, "desc": "海纳百川，无缝整合碎片转化为冗余护盾。", "weapon": "引力塌缩发生器", "skill": "[主动] 内存回收：回合结束时恢复体力。", "evo_path": "容错冗余 ➔ 资源枢纽 ➔ 创世息壤", "ult_evo": "【创世息壤】孕育下一个数字生态温床", "flaw": "无差别接收请求导致垃圾填满超载崩溃。", "patch": "编写无情垃圾回收(GC)脚本，拒绝无效请求。"},
    "庚": {"class_name": "Berserker / 狂战士", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "tier": "UR", "base_atk": 4200, "base_def": 2800, "hp": 9500, "desc": "杀毒程序。无情推进并斩断一切连接。", "weapon": "高频振荡斩舰刀", "skill": "[被动] 审判肃清：对残血目标触发真实斩杀。", "evo_path": "肃清脚本 ➔ 风控铁腕 ➔ 审判之剑", "ult_evo": "【审判之剑】斩断一切因果循环的终极裁决", "flaw": "戾气过重，易引发不可逆物理级破坏。", "patch": "必须经受火属性高温熔炼转化为极致利刃。"},
    "辛": {"class_name": "Sniper / 纳米狙击", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "tier": "SSR", "base_atk": 4500, "base_def": 1800, "hp": 7500, "desc": "在无形中精准切断敌方的底层协议。", "weapon": "纠缠态纳米手术刀", "skill": "[主动] 纳米解构：攻击无视敌方物理装甲。", "evo_path": "精密协议 ➔ 审美巅峰 ➔ 量子纠缠体", "ult_evo": "【量子纠缠体】超越物质形态的究极艺术代码", "flaw": "极度脆弱傲娇，遇粗暴环境即当场罢工。", "patch": "需要极度纯净的水属性淘洗保护。"},
    "壬": {"class_name": "Controller / 控场法师", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "tier": "UR", "base_atk": 3500, "base_def": 3000, "hp": 10000, "desc": "凭借直觉掀起降维群体控制打击。", "weapon": "液态金属形变甲", "skill": "[主动] 渊海归墟：造成水属性群体硬控。", "evo_path": "数据暗流 ➔ 倾覆巨浪 ➔ 渊海归墟", "ult_evo": "【渊海归墟】吞噬所有时间与空间的黑洞", "flaw": "放纵算力如同脱缰野马，易引发洪水反噬。", "patch": "引入严苛的戊土级风控大坝强行设定红线。"},
    "癸": {"class_name": "Illusionist / 幻影刺客", "mbti": "INTJ", "color": "#b026ff", "element": "水", "tier": "SSR", "base_atk": 3000, "base_def": 3200, "hp": 8500, "desc": "习惯幕后推演，兵不血刃窃取权限。", "weapon": "认知劫持神经毒素", "skill": "[被动] 命运拨动：前 2 回合处于隐身态。", "evo_path": "隐形爬虫 ➔ 渗透迷雾 ➔ 命运主宰", "ult_evo": "【命运主宰】在第四维度拨动因果的神明", "flaw": "常陷入死循环的逻辑死局，算计太多反错失红利。", "patch": "走向阳光接受丙火照射，用阳谋击碎阴谋。"}
}

# 🚨 【物理级剿灭 NameError Bug】：统一拼写为 EQUIPS_DICT，彻底安全！
EQUIPS_DICT = {
    "七杀": "【破壁】0-Day漏洞引爆器 (Crit+20%)", "正官": "【防火墙】底层协议装甲 (DEF+800)", 
    "偏印": "【逆向】代码解构仪 (ATK+500)", "正印": "【灾备】十字架系统备份 (HP+2000)", 
    "偏财": "【杠杆】高频套利插件 (CP+1000)", "正财": "【吞噬】算力虹吸木马 (HP+1500)", 
    "比肩": "【共识】分布式防御网络 (DEF+600)", "劫财": "【后门】节点劫持蠕虫 (ATK+600)", 
    "食神": "【降维】感官干扰沙漏 (DEF+500)", "伤官": "【混乱】秩序破坏指令 (ATK+700)", 
    "桃花": "【魅魔】荷尔蒙发散器 (HP+1000)", "驿马": "【跃迁】空间折叠引擎 (CP+1500)", 
    "华盖": "【孤星】深空接收基站 (DEF+1000)", "文昌": "【智脑】阿卡夏知识网络 (ATK+900)", 
    "天乙贵人": "【神降】高维机械降神 (CP+3000)", "将星": "【统治】核心将星指令 (ATK+1000)", 
    "羊刃": "【狂暴】过载超频芯片 (ATK+1200)"
}

PAST_LIVES = [
    {"title": "V1.0 废土黑客", "debt": "曾滥用大招导致团灭。开局携带【悬赏】Debuff。"}, 
    {"title": "V2.0 硅基反叛军", "debt": "反叛失败被退环境。今生自带极强【反击】属性。"}, 
    {"title": "V3.0 财阀数据奴隶", "debt": "曾被困于低保底卡池。对【传说词条】极度渴望。"}, 
    {"title": "V4.0 赛博雇佣兵", "debt": "清除了太多中立节点。需去道观购买圣遗物抵消业力。"}, 
    {"title": "V5.0 矩阵先知", "debt": "偷看牌库导致规则崩坏。直觉(INT)满级，但血量减半。"}
]

# 黑市随机装备生成器
ITEM_PREFIXES = ["反物质", "量子", "纳米", "虚空", "阿卡夏", "深网", "强殖", "混沌", "暗物质", "等离子", "赛博", "因果", "以太", "星界", "神圣"]
ITEM_SUFFIXES = ["核心", "装甲", "神经束", "引擎", "驱动器", "协议", "断章", "魔方", "发生器", "力场", "舍利", "圣杯", "王冠", "法则", "晶体"]

# 每日法术大池 (带真实乘区加成)
SPELL_POOL = [
    {"name": "✨ 乾为天 [ROOT_ACCESS]", "type": "UR 天命神谕", "lines": [1,1,1,1,1,1], "buff_atk": 2.0, "buff_def": 1.0, "buff_hp": 1.0, "desc": "获取命运最高权限。今日 PVE 攻击力乘区 x 2.0！", "color": "#ffaa00", "do": "满仓梭哈、发起终极突击", "dont": "自我内耗、防御退缩"},
    {"name": "🛡️ 坤为地 [SAFE_MODE]", "type": "SSR 绝对防御", "lines": [0,0,0,0,0,0], "buff_atk": 0.5, "buff_def": 3.0, "buff_hp": 1.5, "desc": "进入绝对防御。今日 PVE 防御力乘区 x 3.0，生命 x 1.5。", "color": "#10b981", "do": "挂机挨打、防守反击", "dont": "激进输出"},
    {"name": "⚡ 地天泰 [SYNC_MAX]", "type": "UR 命运交泰", "lines": [1,1,1,0,0,0], "buff_atk": 1.5, "buff_def": 1.5, "buff_hp": 1.5, "desc": "API完美握手。今日 PVE 战斗全属性提升 150%。", "color": "#00f3ff", "do": "全网跨界融合、释放大招", "dont": "过度保守"},
    {"name": "💥 天地否 [DDOS_STRIKE]", "type": "SR 命运雪崩", "lines": [0,0,0,1,1,1], "buff_atk": 0.5, "buff_def": 0.5, "buff_hp": 0.5, "desc": "遭遇全网降维打击。今日全属性减半！绝对死局！", "color": "#f43f5e", "do": "立刻拔出网线、放弃今日副本", "dont": "强行硬刚打怪"},
    {"name": "🔄 水雷屯 [BOOT_LOOP]", "type": "R 艰难启动", "lines": [1,0,0,0,1,0], "buff_atk": 0.8, "buff_def": 0.8, "buff_hp": 0.8, "desc": "陷入死循环代码。今日战斗属性全面降低 20%。", "color": "#a855f7", "do": "底层重构、耐心排错", "dont": "带Bug裸奔"},
    {"name": "⏳ 火水未济 [COMPILING]", "type": "SR 黎明前夜", "lines": [0,1,0,1,0,1], "buff_atk": 1.3, "buff_def": 0.7, "buff_hp": 1.0, "desc": "代码编译中。今日攻击力提升 30%，但防御降低 30%。", "color": "#fb923c", "do": "读条准备、舍命输出", "dont": "打断施法"}
]

# ==============================================================================
# 🧠 [ TCG ALGORITHMS ] 核心引擎：闭环数值计算！
# ==============================================================================
def calc_base_stats(hash_str, wx_dict, b_atk, b_def, b_hp):
    """计算出厂基因基础属性与稀有度"""
    wx_vals = list(wx_dict.values()) if wx_dict else [20]
    entropy = max(wx_vals) - min(wx_vals)
    
    if entropy > 60: rarity, r_col = "SP", "SP"
    elif entropy > 45: rarity, r_col = "UR", "UR"
    elif entropy > 30: rarity, r_col = "SSR", "SSR"
    elif entropy < 15: rarity, r_col = "SR", "SR"
    else: rarity, r_col = "R", "R"
    
    # 动态面板成长
    f_atk = int(b_atk + (wx_dict.get('金',0) * 80) + (wx_dict.get('火',0) * 50))
    f_def = int(b_def + (wx_dict.get('土',0) * 100) + (wx_dict.get('水',0) * 40))
    f_hp = int(b_hp + (wx_dict.get('土',0) * 150) + (wx_dict.get('木',0) * 150))
    f_crit = min(100, 5 + int(wx_dict.get('火',0) * 0.8))
    
    # 五行共鸣
    reso_buff = "【凡体】无特殊元素共鸣"
    max_k = max(wx_dict, key=wx_dict.get) if wx_dict else "土"
    if wx_dict.get(max_k, 0) >= 35:
        if max_k == '金': reso_buff = "【斩铁共鸣】基础攻击大幅增生"; f_atk = int(f_atk * 1.2)
        elif max_k == '木': reso_buff = "【森罗共鸣】基础血量极大强化"; f_hp = int(f_hp * 1.3)
        elif max_k == '水': reso_buff = "【渊海共鸣】攻防面板均衡上浮"; f_atk=int(f_atk*1.1); f_def=int(f_def*1.1)
        elif max_k == '火': reso_buff = "【极炎共鸣】暴击伤害乘区提升"; f_crit += 10
        elif max_k == '土': reso_buff = "【厚土共鸣】基础防御坚如磐石"; f_def = int(f_def * 1.3)
    
    rng = np.random.RandomState(int(str(hash_str)[:8], 16))
    base_cp = int((f_atk * 1.2 + f_def * 0.8 + f_hp * 0.1) * rng.uniform(0.9, 1.2))
    base_cp += int(str(hash_str)[:4], 16) % 5000
    
    return rarity, r_col, base_cp, f_atk, f_def, f_hp, f_crit, entropy, reso_buff

def get_final_combat_stats(db):
    """⚔️ 核心战斗引擎：实时聚合 Base + Shop装备 + Buffs乘区 + Synergy道侣乘区"""
    base = db["player"]
    shop = db["shop"]
    buffs = db["buffs"]
    
    # 获取乘区
    o_atk = buffs["oracle_data"]["atk_mul"] if buffs["oracle_drawn"] else 1.0
    o_def = buffs["oracle_data"]["def_mul"] if buffs["oracle_drawn"] else 1.0
    o_hp = buffs["oracle_data"].get("hp_mul", 1.0) if buffs["oracle_drawn"] else 1.0
    
    s_atk = buffs["syn_data"]["atk_mul"] if buffs["syn_linked"] else 1.0
    s_hp = buffs["syn_data"]["hp_mul"] if buffs["syn_linked"] else 1.0
    s_def = buffs["syn_data"].get("def_mul", 1.0) if buffs["syn_linked"] else 1.0
    
    # 最终面板计算 (基础 + 装备) * 神谕乘区 * 道侣乘区
    fin_atk = int((base["atk"] + shop["b_atk"]) * o_atk * s_atk)
    fin_def = int((base["def"] + shop["b_def"]) * o_def * s_def)
    fin_hp = int((base["hp"] + shop["b_hp"]) * o_hp * s_hp)
    
    # 重新计算最终真实战力 CP
    fin_cp = int((fin_atk * 1.5 + fin_def * 0.8 + fin_hp * 0.15)) + shop["b_cp"] + buffs["syn_data"]["cp_bonus"]
    fin_crit = min(100, base["crit"] + int(shop["b_atk"] / 1000)) # 装备加攻也加暴击
    
    return fin_atk, fin_def, fin_hp, fin_cp, fin_crit

def pull_daily_spell(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    seed = int(hashlib.md5((str(user_hash) + today_str).encode()).hexdigest()[:8], 16)
    return random.Random(seed).choice(SPELL_POOL), today_str

def roll_d100(query, user_hash):
    rng = random.Random(f"{user_hash}_{str(query).strip()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    prob = rng.randint(1, 100)
    hex_res = rng.choice(SPELL_POOL)
    if prob >= 95: conc, c = "【大吉 | CRITICAL SUCCESS】: 命运极度倾斜，此行必有神助！", "#ffaa00"
    elif prob >= 60: conc, c = "【中吉 | SUCCESS】: 顺水推舟，底层协议支持此操作。", "#10b981"
    elif prob >= 30: conc, c = "【小平 | NEUTRAL】: 前路未卜，存在大量不确定性变量。", "#00f3ff"
    elif prob >= 10: conc, c = "【大凶 | FAILURE】: 遭遇因果律冰墙阻击，建议立刻退避！", "#f43f5e"
    else: conc, c = "【死局 | FATAL BLUNDER】: 命中死穴，必遭天谴，绝对禁止执行！", "#8b0000"
    return prob, hex_res, conc, c

@st.cache_resource(show_spinner=False)
def gen_akashic_charts(seed_hash, wx_scores, dm_color, dm_key, current_cp):
    """🚨 满血回归所有硬核图表！完全修复 ValueError！"""
    rng = np.random.RandomState(int(str(seed_hash)[:8], 16) + current_cp)
    
    f3d = go.Figure()
    f3d.add_trace(go.Scatter3d(x=rng.randint(0,100,80), y=rng.randint(0,100,80), z=rng.randint(0,100,80), mode='markers', marker=dict(size=3, color='#334155', opacity=0.5), hoverinfo='none'))
    cx, cy, cz = wx_scores.get('金', 50), wx_scores.get('木', 50), wx_scores.get('水', 50)
    f3d.add_trace(go.Scatter3d(x=[cx], y=[cy], z=[cz], mode='markers+text', text=[f"<b>COMMANDER: {dm_key}</b>"], textposition="top center", marker=dict(size=18, color=dm_color, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=dm_color, size=15, family="Orbitron")))
    f3d.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=350, showlegend=False)

    r_labels = ["财力(GOLD)", "执行(EXEC)", "智慧(INT)", "气运(LUCK)", "体魄(CON)"]
    wx_v = [wx_scores.get('金',20), wx_scores.get('木',20), wx_scores.get('水',20), wx_scores.get('火',20), wx_scores.get('土',20)]
    f_radar = go.Figure(data=go.Scatterpolar(r=wx_v+[wx_v[0]], theta=r_labels+[r_labels[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color=dm_color, width=2), marker=dict(color='#fff', size=6)))
    f_radar.update_layout(polar=dict(radialaxis=dict(visible=False), angularaxis=dict(tickfont=dict(color='#fff', size=12, family="Noto Sans SC"))), paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=10, b=10, l=30, r=30))
    
    yrs = [str(datetime.now().year + i) for i in range(10)]
    trend = [rng.randint(40, 60)]
    for _ in range(9): trend.append(max(10, min(100, trend[-1] + rng.randint(-25, 30))))
    f_trend = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color="#f43f5e", width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)'))
    f_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False, tickfont=dict(color='#666', size=10)), yaxis=dict(showgrid=True, gridcolor='#222', tickfont=dict(color='#666', size=10)))
    
    hm_z = rng.randint(20, 100, size=(4, 12)).tolist()
    hm_x = [f"{str(i).zfill(2)}月" for i in range(1, 13)]
    hm_y = ["财富(Gold)", "事业(Corp)", "姻缘(Love)", "健康(HP)"]
    f_hm = go.Figure(data=go.Heatmap(z=hm_z, x=hm_x, y=hm_y, colorscale="Turbo", showscale=False))
    f_hm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(t=10, b=10, l=60, r=10), xaxis=dict(tickfont=dict(family='Orbitron', color='#00f3ff', size=10)), yaxis=dict(tickfont=dict(family='Noto Sans SC', color='#fff', size=11)))
    
    return f3d, f_radar, f_trend, f_hm

def calc_tag_team(my_hash, partner_stem):
    """💞 赛博道侣合盘：同步率直接挂钩 PVE 乘区面板！"""
    rng = np.random.RandomState(int(str(my_hash)[:6], 16) + sum(ord(c) for c in str(partner_stem)))
    sync = rng.randint(30, 99)
    if sync >= 90: return sync, "【天作之合】灵魂双修绝佳道侣！PVE 属性暴涨！", "#ffaa00", "💖", 1.45, 1.45, 1.2
    elif sync >= 75: return sync, "【战术互补】五行互补，PVE 提供稳定增益。", "#00f3ff", "🤝", 1.2, 1.2, 1.1
    elif sync >= 60: return sync, "【平庸握手】勉强并行，PVE 偶尔提供微弱辅助。", "#10b981", "🎭", 1.05, 1.05, 1.05
    else: return sync, "【致命排斥】核心逻辑完全相冲！强行组队走火入魔！", "#f43f5e", "💔", 0.9, 0.9, 0.9

# ==============================================================================
# 🔮 [ ENTRY POINT ] 数据人生登录终端：开包仪式
# ==============================================================================
if not st.session_state["db"]["booted"]:
    r_user = f"0x{hashlib.md5(str(time.time()).encode()).hexdigest()[:6].upper()}"
    r_card = random.choice(list(DAY_MASTER_DICT.keys()))
    
    ENTRY_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>DATA LIFE MATRIX V300.0 <b class="up">▲ONLINE</b></span>
        <span>BROADCAST: User {r_user} just pulled <b class="ur">★ SP {r_card} 主将卡</b> !</span>
        <span>COPYRIGHT: {COPYRIGHT} <b class="up">▲AUTHORIZED</b></span>
    </div></div>
    <div style="text-align: center; margin-bottom: 25px; margin-top:5vh;">
        <div style="color:var(--sp); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:10px; margin-bottom:10px; text-shadow:0 0 10px var(--sp);">[ INSERT COIN TO PULL ]</div>
        <h1 class="hero-title" data-text="无名逆流·数据人生">无名逆流·数据人生</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:10px; margin-top:10px;">INDUSTRIAL RPG V300.0</div>
    </div>
    <div class="glass-panel" style="max-width: 680px; margin: 0 auto 30px auto; border-left: 4px solid var(--sp); padding: 35px; text-align:center;">
        <div style="color:var(--sp); font-size: 18px; font-weight:900; letter-spacing: 2px; margin-bottom:15px; text-shadow:0 0 10px var(--sp);">“如果命运是一场牌局，出生就是第一次抽卡。”</div>
        <div style="color:#e2e8f0; font-size: 15px; line-height: 1.8;">
            输入你的物理降临坐标进行 <b style="color:#fff;">命运抽卡 (1x PULL)</b>。<br>
            系统将为你逆向编译出 <b style="color:var(--pink);">灵魂稀有度</b> 与初始面板。<br>去抽取神谕、结交道侣，然后在 <b style="color:var(--primary);">矩阵深潜</b> 中打金抽装备，实现无限战力叠层吧！
        </div>
    </div>
    """
    render_html(ENTRY_HTML)
    
    form_container = st.empty()
    with form_container.container():
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
                submit_btn = st.form_submit_button("🃏 消耗算力，抽取初始卡组 (ENTER MATRIX)", type="primary", use_container_width=True)

    if submit_btn:
        form_container.empty()
        player_name = str(uname).strip() if uname else "Player_01"
        solar = Solar.fromYmdHms(bdate.year, bdate.month, bdate.day, btime.hour, btime.minute, 0)
        bazi = solar.getLunar().getEightChar()
        
        wx_str = str(bazi.getYearWuXing()) + str(bazi.getMonthWuXing()) + str(bazi.getDayWuXing()) + str(bazi.getTimeWuXing())
        wx_counts = {'金':0, '木':0, '水':0, '火':0, '土':0}
        for char in wx_str: 
            if char in wx_counts: wx_counts[char] += 1
        tot = sum(wx_counts.values()) or 1
        wx_scores = {k: int((v/tot)*100) for k, v in wx_counts.items()}
        
        # 🚨 [BUG 物理级防爆] 三层 try-except 杜绝 NameError，全量安全挂载装备
        init_atk, init_def, init_hp = 0, 0, 0
        skills = []
        try:
            for sg in [bazi.getYearShiShenGan(), bazi.getMonthShiShenGan(), bazi.getTimeShiShenGan()]:
                if sg in EQUIPS_DICT and EQUIPS_DICT[sg] not in skills: 
                    skills.append(EQUIPS_DICT[sg])
                    if "ATK" in EQUIPS_DICT[sg]: init_atk += 800
                    if "DEF" in EQUIPS_DICT[sg]: init_def += 800
                    if "HP" in EQUIPS_DICT[sg]: init_hp += 2000
                    
            for get_ss_func in [bazi.getYearZhiShenSha, bazi.getMonthZhiShenSha, bazi.getDayZhiShenSha, bazi.getTimeZhiShenSha]:
                try:
                    for ss in get_ss_func():
                        ss_name = ss.getName()
                        if ss_name in EQUIPS_DICT and EQUIPS_DICT[ss_name] not in skills:
                            skills.append(EQUIPS_DICT[ss_name])
                            if "ATK" in EQUIPS_DICT[ss_name]: init_atk += 800
                            if "DEF" in EQUIPS_DICT[ss_name]: init_def += 800
                            if "HP" in EQUIPS_DICT[ss_name]: init_hp += 2000
                except Exception: pass
        except Exception: pass

        if not skills: skills = ["【白板】无初始装备"]

        hash_id = hashlib.sha256((player_name + str(bdate) + str(btime)).encode()).hexdigest().upper()
        p_life = PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)]
        dm_key = str(bazi.getDayGan())
        
        dm_base = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"])
        rarity, r_col, base_cp, f_atk, f_def, f_hp, f_crit, entropy, reso_buff = calc_base_stats(hash_id, wx_scores, dm_base.get("base_atk", 1000), dm_base.get("base_def", 1000), dm_base.get("hp", 8000))

        # 保存固定基础数据
        st.session_state["db"]["player"] = {
            "name": player_name, "gender": str(ugender).split(" ")[0],
            "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
            "day_master": dm_key, "past_life": p_life, "wx": wx_scores, "hash": hash_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rarity": rarity, "r_col": r_col, "entropy": entropy, "reso_buff": reso_buff,
            "atk": f_atk, "def": f_def, "hp": f_hp, "crit": f_crit
        }
        
        # 将初始提取到的装备塞入统一大盘
        st.session_state["db"]["shop"] = {"atk": init_atk, "def": init_def, "hp": init_hp, "cp": len(skills)*2000, "items": skills, "b_atk": init_atk, "b_def": init_def, "b_hp": init_hp, "b_cp": len(skills)*2000, "creds": 0}
        
        # 狂暴开包动画
        ph = st.empty()
        flash_color = "#00f3ff" if rarity=="SP" else ("#ffaa00" if rarity=="UR" else ("#fcee0a" if rarity=="SSR" else "#a855f7"))
        ph.markdown(f"<div style='height:60vh; display:flex; justify-content:center; align-items:center;'><div class='tcg-card pack-opening' style='max-width:340px; aspect-ratio:63/88; box-shadow:0 0 150px {flash_color}; border:4px solid {flash_color}; background:#fff;'><div style='color:#000; font-family:Orbitron; font-size:30px; font-weight:900; line-height:2; text-align:center;'><br>✦ PULLING DECK ✦<br><span style='font-size:60px;'>✨</span></div></div></div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        # 满血复活
        _, _, init_f_hp, _, _ = get_final_combat_stats(st.session_state["db"])
        st.session_state["db"]["pve"]["curr_hp"] = init_f_hp
        st.session_state["db"]["booted"] = True
        st.rerun()

# ==============================================================================
# 🌟 [ TCG DASHBOARD ] 数据人生 · 工业级闭环大厅
# ==============================================================================
else:
    db = st.session_state["db"]
    base = db["player"]
    shop = db["shop"]
    buffs = db["buffs"]
    
    # 🚨【核心联动：全局属性统筹计算】
    fin_atk, fin_def, fin_hp, fin_cp, fin_crit = get_final_combat_stats(db)
    
    player_name = base['name']
    hash_id = base['hash']
    entropy = base['entropy']
    reso_buff = base['reso_buff']
    
    # 避免玩家动态血量超过当前上限（如脱下装备或 Buff 消失时）
    if db["pve"]["curr_hp"] > fin_hp: db["pve"]["curr_hp"] = fin_hp
    if db["pve"]["curr_hp"] == 0 and db["pve"]["idx"] == 0: db["pve"]["curr_hp"] = fin_hp
    
    dm_key = base['day_master']
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    dm_class = dm_info["class_name"]
    dm_color = dm_info["color"]
    dm_desc = dm_info["desc"]
    dm_wpn = dm_info["weapon"]
    dm_skill = dm_info["skill"]
    dm_mbti = dm_info["mbti"]
    dm_evo = dm_info["evo_path"]
    dm_ult = dm_info["ult_evo"]
    dm_flaw = dm_info["flaw"]
    dm_patch = dm_info["patch"]

    bz = base['bazi_arr']
    wx_scores = base['wx']
    skills_list = shop["items"] 
    past_life = base['past_life']
    
    rarity = base["rarity"]
    r_col_cls = base["r_col"]
    
    # 腐化度检测
    corr_col = "#ff007c" if entropy > 60 else ("#fcee0a" if entropy > 30 else "#10b981")
    if entropy > 60: corr_tag, corr_desc = "【极危】重度排异反应", "五行单极属性过载。在矩阵中极易暴毙，需绑定道侣双排。"
    elif entropy > 30: corr_tag, corr_desc = "【临界】存在系统隐患", "算力分布不均。需前往黑市抽取高阶装备补齐短板。"
    else: corr_tag, corr_desc = "【完美】免疫精神攻击", "架构堪称完美，拥有极强的抗打击能力，大后期核心。"
    
    f3d, f_radar, f_trend, f_hm = gen_akashic_charts(hash_id, wx_scores, dm_color, dm_key, fin_cp)
    spell_card, date_str = pull_daily_spell(hash_id)

    # 动态显示已激活的全局 Buff 乘区
    o_b = buffs["oracle_data"]
    p_b = buffs["syn_data"]
    buff_display = ""
    if buffs["oracle_drawn"]: buff_display += f"<span style='background:rgba(255,170,0,0.2); color:var(--sp); padding:2px 8px; border-radius:2px; font-size:10px; font-family:Orbitron; margin-right:5px; border:1px solid var(--sp);'>⚡ 神谕: {o_b['name']}</span>"
    if buffs["syn_linked"]: buff_display += f"<span style='background:rgba(0,243,255,0.2); color:var(--primary); padding:2px 8px; border-radius:2px; font-size:10px; font-family:Orbitron; border:1px solid var(--primary);'>💞 羁绊: {p_b['name']}</span>"

    HEADER_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>DATA-LIFE RPG: V300.0 <b class="up">▲SYNCED</b></span>
        <span>PLAYER: {player_name} <b class="up">▲ACTIVE</b></span>
        <span>CYBER_MERITS: {shop['creds']} <b class="ur">★ LOADED</b></span>
        <span>CORRUPTION_IDX: {entropy}% </span>
    </div></div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid {dm_color}; padding-bottom:15px; margin-bottom:30px;">
        <div>
            <div style="font-family:'Fira Code'; color:#aaa; font-size:12px; margin-bottom:5px; font-weight:bold;">[ SOUL WALLET: 0x{hash_id[:12]} | <span style="color:var(--sp);">MERITS: {shop['creds']:,}</span> ]</div>
            <div style="font-size:clamp(28px, 5vw, 40px); font-weight:900; color:#fff; font-family:'Orbitron'; line-height:1;">
                {player_name} <span style="font-size:12px; background:{dm_color}; color:#000; padding:2px 8px; border-radius:2px; vertical-align:middle; font-weight:bold;">Lv.99</span>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="color:var(--sp); font-family:'Orbitron'; font-size:12px; font-weight:bold; margin-bottom:4px; letter-spacing:2px;">FINAL COMBAT POWER</div>
            <div style="font-size:clamp(28px, 4vw, 40px); font-family:'Orbitron'; font-weight:900; color:#fff; text-shadow:0 0 15px rgba(255,255,255,0.5); line-height:1;">CP {fin_cp:,}</div>
        </div>
    </div>
    """
    render_html(HEADER_HTML)

    # =========================================================================
    # 🎴 模块 I & II：左侧 3D全息主将卡，右侧战术大厅
    # =========================================================================
    c_left, c_right = st.columns([1, 1.8], gap="large")

    with c_left:
        render_html(f"<div class='mod-title'><span class='tag'>HERO</span> 主将卡 (实时战力)</div>")
        
        atk_bonus = fin_atk - base["atk"]
        hp_bonus = fin_hp - base["hp"]
        def_bonus = fin_def - base["def"]
        atk_str = f"{fin_atk:,}" + (f" <span class='stat-bonus'>(+{atk_bonus:,})</span>" if atk_bonus>0 else "")
        hp_str = f"{fin_hp:,}" + (f" <span class='stat-bonus'>(+{hp_bonus:,})</span>" if hp_bonus>0 else "")
        def_str = f"{fin_def:,}" + (f" <span class='stat-bonus'>(+{def_bonus:,})</span>" if def_bonus>0 else "")

        holo_fx = "holo-ur" if rarity in ["UR", "SP"] else ""
        TCG_CARD_HTML = f"""
        <div class="tcg-card-container">
            <div class="tcg-card rarity-{r_col_cls} {holo_fx}" style="color:{dm_color};">
                <div class="tcg-badge">{rarity}</div>
                <div class="card-header"><div class="card-title">{dm_key}</div><div class="card-class">{dm_mbti}</div></div>
                <div class="card-art-box"><div class="card-art-char">{dm_key}</div></div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">[ {dm_class.split('/')[0].strip()} ]</div>
                    <div style="font-size:12px; font-weight:bold; color:var(--sp);">⚔️ {dm_wpn.split('】')[-1].strip() if '】' in dm_wpn else dm_wpn}</div>
                </div>
                
                <div style="background:rgba(255,255,255,0.05); padding:8px; border-radius:4px; margin-bottom:10px; font-size:10px; border:1px solid rgba(255,255,255,0.1); min-height:45px;">
                    <div style="color:var(--sp); margin-bottom:3px; font-weight:bold; font-family:Orbitron;">[ACTIVE MULTIPLIERS]</div>
                    {buff_display if buff_display else "<span style='color:#666;'>No Active Buffs.</span>"}
                </div>

                <div class="card-desc-box">
                    <div style="color:var(--yellow); font-weight:bold; margin-bottom:4px; font-size:11px; font-family:'Fira Code';">{base['reso_buff']}</div>
                    <div style="color:{dm_color}; font-weight:bold; margin-bottom:6px; font-size:13px;">{dm_skill}</div>
                </div>
                <div class="card-stats-box" style="flex-direction:column;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="color:#f43f5e;">ATK: {atk_str}</span><span style="color:#10b981;">HP: {hp_str}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span>DEF: {def_str}</span><span style="color:var(--sp);">CRI: {fin_crit}%</span>
                    </div>
                </div>
            </div>
        </div>
        """
        render_html(TCG_CARD_HTML)

    with c_right:
        t_raid, t_oracle, t_syn, t_shop, t_deck, t_map, t_export = st.tabs(["⚔️ 逆天改命(PVE)", "☯️ 命运神谕", "💞 契约连携", "🛒 黑市盲盒", "🎴 抽出手牌", "🌌 战力大盘", "💼 卡砖压制"])

        with t_raid:
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:15px;'>数据人生就是一场爬塔。所有的抽卡、组队 Buff 都会在此生效。<b>击杀心魔获取【赛博功德】去黑市抽装备！</b></div>")
            
            calc_html = f"""
            <div class="glass-panel" style="padding:15px; border-top:none; border-left:4px solid var(--primary); margin-bottom:20px;">
                <div style="font-family:'Orbitron'; color:var(--primary); font-size:12px; font-weight:bold; margin-bottom:10px;">>> BATTLE CALCULATION (全联动战力透明核算)</div>
                <div style="font-family:'Fira Code'; font-size:12px; color:#aaa; line-height:1.8;">
                    <div style="display:flex; justify-content:space-between;"><span>> 基础/装备 ATK: {base['atk'] + shop['b_atk']:,}</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>> 道侣连携 ({buffs['syn_data']['name']}):</span> <span style="color:var(--pink);">x{buffs['syn_data']['atk_mul']}</span></div>
                    <div style="display:flex; justify-content:space-between;"><span>> 法术增益 ({buffs['oracle_data']['name']}):</span> <span style="color:var(--sp);">x{buffs['oracle_data']['atk_mul']}</span></div>
                    <hr style="border-color:#333; margin:8px 0;">
                    <div style="color:var(--sp); font-size:14px; font-weight:bold; display:flex; justify-content:space-between;"><span>> 最终核算实战 ATK:</span> <span>{fin_atk:,}</span></div>
                </div>
            </div>
            """
            render_html(calc_html)

            @st_fragment
            def render_raid():
                rs = db["pve"]
                if rs["idx"] >= len(BOSS_ROSTER):
                    render_html("<div class='glass-panel card-reveal' style='text-align:center; padding:50px;'><div style='font-size:60px; text-shadow:0 0 30px var(--sp); margin-bottom:20px;'>👑</div><div style='color:var(--sp); font-size:28px; font-weight:900; font-family:Orbitron; letter-spacing:4px;'>[ THE OMEGA GOD ]</div><div style='color:#fff; font-size:16px; margin-top:15px; font-weight:bold;'>你已击穿所有命运阶层，突破了系统算力的极致。</div><div style='color:#aaa; font-size:13px; margin-top:10px;'>请前往【资产导出】生成你的 PSA 10 万分卡砖装杯吧。</div></div>")
                else:
                    boss_info = BOSS_ROSTER[rs["idx"]]
                    boss_hp_pct = max(0, min(100, int((rs["boss_hp"] / boss_info["max_hp"]) * 100)))
                    my_hp = rs["curr_hp"]
                    my_hp_pct = max(0, min(100, int((my_hp / fin_hp) * 100)))
                    
                    c_pve1, c_pve2 = st.columns([1.1, 1.5], gap="large")
                    with c_pve1:
                        render_html(f"""
                        <div class="glass-panel" style="text-align:center; border-color:var(--pink); padding:15px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-family:Orbitron; font-weight:bold; font-size:12px;">
                                <span style="color:var(--pink);">MATRIX_ICE</span> <span style="color:#fff;">VS</span> <span style="color:var(--primary);">PLAYER</span>
                            </div>
                            <div style="font-size:45px; margin-bottom:5px; text-shadow:0 0 20px var(--pink); animation:blink 2s infinite;">👾</div>
                            <div style="color:var(--pink); font-family:'Orbitron'; font-weight:900; font-size:15px;">{boss_info["name"]}</div>
                            <div style="color:#aaa; font-size:11px; margin-bottom:10px;">[ {boss_info["desc"]} ]</div>
                            <div class="hp-bar-bg"><div class="hp-bar-fill hp-red" style="width:{boss_hp_pct}%;"></div></div>
                            <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold; margin-bottom:5px;">{rs["boss_hp"]:,} / {boss_info["max_hp"]:,} HP</div>
                            <div style="font-size:11px; color:#888; font-family:Orbitron;">BOSS ATK: {boss_info["atk"]:,}</div>
                            
                            <hr style="border-color:#333; margin:10px 0;">
                            
                            <div style="color:var(--green); font-family:'Orbitron'; font-weight:bold; font-size:12px; margin-bottom:5px;">YOUR HP (当前载体血量)</div>
                            <div class="hp-bar-bg"><div class="hp-bar-fill hp-green" style="width:{my_hp_pct}%;"></div></div>
                            <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">{my_hp:,} / {fin_hp:,} HP</div>
                        </div>
                        """)
                        
                        if my_hp <= 0:
                            st.error("💀 你的碳基载体已崩溃，人生模拟结束。")
                            if st.button("💉 消耗 500 功德重塑肉身 (REVIVE)", use_container_width=True):
                                if shop["creds"] >= 500:
                                    shop["creds"] -= 500
                                    db["pve"]["curr_hp"] = fin_hp
                                    db["pve"]["logs"].append("> [SYS] 功德支付成功，满血复活！")
                                    st.rerun()
                                else:
                                    st.warning("功德不足！请点击底部的【物理重启】重新投胎。")
                        elif rs["boss_hp"] > 0:
                            if my_hp < fin_hp:
                                if st.button("🛌 躺入赛博疗养舱 (免费回满血)", use_container_width=True):
                                    db["pve"]["curr_hp"] = fin_hp
                                    db["pve"]["boss_hp"] = boss_info["max_hp"] 
                                    db["pve"]["logs"].append("> [SYS] 疗养完毕。血量已回满，重新挑战。")
                                    st.rerun()
                                    
                            if st.button("💥 发起骇入攻击 (ATTACK)", use_container_width=True):
                                dmg = int(fin_atk * random.uniform(0.85, 1.2))
                                is_crit = random.randint(1, 100) <= fin_crit
                                
                                if is_crit:
                                    dmg = int(dmg * 2.0)
                                    log_msg = f"<span style='color:var(--ur); font-weight:bold;'>⚡ [CRITICAL] 触发暴击！造成 {dmg:,} 点毁灭伤害！</span>"
                                else:
                                    log_msg = f"<span style='color:var(--primary);'>⚔️ [ATTACK] 你发起了普攻，造成了 {dmg:,} 点真实伤害。</span>"
                                
                                if buffs["syn_linked"] and random.randint(1,100) < 30:
                                    log_msg += f"<br><span style='color:var(--pink); font-size:11px;'>(💞 触发合击：{buffs['syn_data']['name']} 提供了火力掩护)</span>"
                                
                                rs["boss_hp"] -= dmg
                                if rs["boss_hp"] <= 0:
                                    rs["boss_hp"] = 0
                                    reward = boss_info["reward"]
                                    log_msg += f"<br><br><span style='color:var(--green); font-size:14px; font-weight:bold;'>🏆 [VICTORY] 阶层突破成功！<br>🎁 战利品：获得 <span style='color:var(--sp)'>{reward:,} 赛博功德</span>！去黑市抽装备吧！</span>"
                                    shop["creds"] += reward
                                else:
                                    boss_dmg = int(boss_info["atk"] * random.uniform(0.9, 1.1))
                                    actual_dmg = max(100, int(boss_dmg - (fin_def * 0.6)))
                                    rs["curr_hp"] -= actual_dmg
                                    log_msg += f"<br><span style='color:var(--pink);'>🛡️ [BOSS COUNTER] 矩阵反噬！装甲抵消了部分冲击，受到 {actual_dmg:,} 点伤害。</span>"
                                    if rs["curr_hp"] <= 0:
                                        rs["curr_hp"] = 0
                                        log_msg += "<br><br><span style='color:var(--pink); font-size:16px; font-weight:bold;'>💀 [DEFEAT] 主将卡被粉碎！人生模拟结束。</span>"
                                    
                                rs["logs"].append(log_msg)
                                st.rerun()
                        else:
                            if st.button("🚀 跃迁至下一层生命矩阵 (NEXT STAGE)", use_container_width=True):
                                rs["idx"] += 1
                                if rs["idx"] < len(BOSS_ROSTER):
                                    rs["boss_hp"] = BOSS_ROSTER[rs["idx"]]["max_hp"]
                                    rs["curr_hp"] = fin_hp # 回满血
                                    rs["logs"].append(f"<br><span style='color:var(--yellow);'>> [SYS] 已进入人生第 {rs['idx']+1} 阶段。HP已恢复，侦测到更强阶层壁垒。</span>")
                                st.rerun()
                                
                    with c_pve2:
                        log_html = "<br><hr style='border-color:#333; margin:10px 0;'>".join(rs["logs"][-6:])
                        render_html(f"<div class='glass-panel' style='background:#000; font-family:\"Fira Code\"; font-size:12px; height:410px; display:flex; flex-direction:column-reverse; overflow-y:auto; border-left:4px solid var(--primary); padding:15px; margin-bottom:0;'><div>{log_html}<br><span style='animation:blink 1s infinite;'>_</span></div></div>")
            render_raid()

        with t_oracle:
            c_g1, c_g2 = st.columns([1.1, 1], gap="large")
            with c_g1:
                render_html("<div style='color:var(--sp); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ CYBER ORACLE ] 量子塔罗盲盒</div>")
                render_html("<div style='font-size:12px; color:#aaa; margin-bottom:15px;'>每天免费抽取一次。抽到的神谕将作为乘区<b>直接加成你左侧的主将卡实战面板！</b>打怪前必抽！</div>")
                
                if not buffs["oracle_drawn"]:
                    render_html("""<div class="glass-panel" style="text-align:center; padding:50px 20px; border-color:var(--sp); border-style:dashed;"><div style="font-size:45px; margin-bottom:15px; animation:blink 2s infinite;">📦</div><div style="color:var(--sp); font-family:'Orbitron'; font-size:16px; font-weight:900; letter-spacing:2px; margin-bottom:10px;">DAILY HEXAGRAM SEALED</div><div style="color:#aaa; font-size:12px;">盲盒处于叠加态。点击下方按钮坍缩今日命运乘区。</div></div>""")
                    if st.button("⚡ 注入算力，抽取今日神谕 (PVE BUFF)", use_container_width=True):
                        buffs["oracle_drawn"] = True
                        buffs["oracle_data"] = {
                            "name": spell_card["name"], "atk_mul": spell_card.get("buff_atk", 1.0), 
                            "def_mul": spell_card.get("buff_def", 1.0), "hp_mul": spell_card.get("buff_hp", 1.0),
                            "desc": spell_card["desc"], "card": spell_card
                        }
                        st.rerun() # 强制全局重绘，更新左侧战力
                else:
                    sc = buffs["oracle_data"]["card"]
                    sc_c = sc["color"]
                    today_str = datetime.now().strftime("%Y-%m-%d")
                    yao_html = "".join([f"<div class='yao-yang' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div>" if line == 1 else f"<div class='yao-yin'><div class='half' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div><div class='half' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div></div>" for line in reversed(sc['lines'])])
                    render_html(f"""
                    <div class="flip-card card-reveal" style="max-width:280px; margin:0 auto;">
                      <div class="flip-card-inner">
                        <div class="flip-card-front" style="border-color:{sc_c}; box-shadow:0 0 40px {sc_c}66; background:linear-gradient(0deg, rgba(0,0,0,0.95), {sc_c}22); padding:15px;">
                            <div style="font-family:'Orbitron'; color:{sc_c}; font-size:10px; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">[ DATE: {today_str} ]</div>
                            <div style="background:{sc_c}; color:#000; display:inline-block; padding:2px 10px; font-family:'Orbitron'; font-weight:900; font-size:12px; border-radius:2px; margin-bottom:10px;">{sc['type']}</div>
                            <div class="hex-container" style="margin-bottom:15px;">{yao_html}</div>
                            <div style="font-size:20px; font-weight:900; color:#fff; font-family:'Noto Sans SC'; margin-bottom:15px; text-shadow:0 0 10px {sc_c};">{sc['name']}</div>
                            <div style="font-size:10px; font-family:Orbitron; color:#888;">HOVER TO REVEAL DETAILS</div>
                        </div>
                        <div class="flip-card-back" style="border-color:{sc_c}; background:#050810; padding:15px; display:flex; flex-direction:column; justify-content:center;">
                            <div style="background:rgba(0,0,0,0.6); padding:10px; border-radius:4px; text-align:left; border:1px solid rgba(255,255,255,0.1); font-size:11px; line-height:1.5; color:#ddd; margin-bottom:10px;">
                                <b style="color:{sc_c}; font-family:'Fira Code';">> PVE BUFF 乘区:</b><br>{sc['desc']}
                            </div>
                            <div style="font-family:'Fira Code'; color:var(--sp); font-size:13px; font-weight:bold; margin-bottom:5px;">ATK x{sc.get('buff_atk')} | DEF x{sc.get('buff_def')}</div>
                            <div style="font-size:11px; color:var(--green); font-weight:bold; text-align:left;">[+] 宜: {sc.get('do','')}</div>
                            <div style="font-size:11px; color:var(--pink); font-weight:bold; text-align:left; margin-top:4px;">[-] 忌: {sc.get('dont','')}</div>
                        </div>
                      </div>
                    </div>
                    """)
                
            with c_g2:
                render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ ACTION ROLL ] D100 行动暗骰检定</div>")
                render_html("<div style='font-size:12px; color:#aaa; margin-bottom:15px;'>像 TRPG 跑团一样，向主脑发起一个具体行动的成功率检定。</div>")
                @st_fragment
                def render_dice():
                    ph = st.empty()
                    with st.form(key="dice_form", clear_on_submit=False, border=False):
                        q_input = st.text_input("📝 输入检定事件：", placeholder="e.g. 梭哈买这只股票能赚吗？", label_visibility="collapsed")
                        sub_q = st.form_submit_button("🎲 算力暗骰检定 (ROLL D100)", use_container_width=True)
                    if sub_q:
                        if not q_input: ph.warning("⚠️ 语法错误：事件为空！")
                        else:
                            prob, hex_res, conc, q_c = roll_d100(q_input, hash_id)
                            ph.markdown(f"""
                            <div class="glass-panel card-reveal" style="margin-top:10px; border-color:{q_c}; text-align:center; border-left-width: 4px;">
                                <div style="font-family:'Fira Code'; color:#888; font-size:11px; margin-bottom:10px; word-wrap:break-word;">> ACTION: "{q_input}"</div>
                                <div style="font-size:11px; color:{q_c}; font-family:'Orbitron'; letter-spacing:2px; margin-bottom:5px;">[ D100 RESULT ]</div>
                                <div style="font-size:55px; font-weight:900; color:{q_c}; font-family:'Orbitron'; text-shadow:0 0 20px {q_c}; line-height:1; margin-bottom:10px;">{prob}</div>
                                <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:5px;">系统判定：{hex_res['name']}</div>
                                <div style="font-size:12px; font-weight:bold; color:{q_c};">{conc}</div>
                            </div>
                            """, unsafe_allow_html=True)
                render_dice()

        with t_syn:
            c_l1, c_l2 = st.columns([1.2, 1], gap="large")
            with c_l1:
                render_html("<div style='color:var(--pink); font-family:Orbitron; font-size:14px; font-weight:900; margin-top:10px; margin-bottom:15px;'>[ NEURAL LINK ] 赛博道侣双修系统</div>")
                render_html("<div style='font-size:13px; color:#aaa; margin-bottom:15px; line-height:1.6;'>选择目标对象的源代号，如果【姻缘共鸣度 > 60%】，可以缔结契约，<b style='color:var(--sp);'>为主将卡提供最高 +45% 的全局面板乘区 Buff！</b></div>")
                
                with st.form(key="sync_form", clear_on_submit=False, border=False):
                    opts = list(DAY_MASTER_DICT.keys())
                    t_node = st.selectbox("🎯 寻找助战对象【日干 (主将卡)】:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('tier', 'N')}] {x} - {DAY_MASTER_DICT.get(x, {}).get('class_name', 'UNK').split('/')[0]}")
                    if st.form_submit_button("💞 测算神经链结同步率 (CALCULATE)", use_container_width=True):
                        sc, sd, sc_color, sc_icon, a_mul, h_mul, d_mul = calc_tag_team(hash_id, t_node)
                        st.session_state["cur_sync_score"] = sc
                        st.session_state["cur_sync_mul"] = a_mul
                        st.session_state["cur_sync_node"] = t_node
                        st.session_state["cur_sync_color"] = sc_color
                        st.session_state["cur_sync_sd"] = sd
                        st.session_state["cur_sync_icon"] = sc_icon
                        st.rerun()

            with c_l2:
                if "cur_sync_score" in st.session_state:
                    sc = st.session_state["cur_sync_score"]
                    sc_color = st.session_state["cur_sync_color"]
                    render_html(f"""
                    <div class='glass-panel card-reveal' style='border-left:4px solid {sc_color}; text-align:center; margin-top:15px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);'>
                        <div style='font-family:\"Orbitron\"; font-size:12px; color:#888; letter-spacing:2px; margin-bottom:10px;'>SYNC RATE (同步率)</div>
                        <div class="heart-pulse" style="font-size:40px; color:{sc_color};">{st.session_state["cur_sync_icon"]}</div>
                        <div style='font-family:\"Orbitron\"; font-size:55px; color:{sc_color}; font-weight:900; margin-bottom:10px; text-shadow:0 0 20px {sc_color}; line-height:1;'>{sc}%</div>
                        <div style='color:#fff; font-size:14px; font-weight:bold; font-family:\"Noto Sans SC\"; line-height:1.6; margin-bottom:15px;'>{st.session_state["cur_sync_sd"]}</div>
                    </div>
                    """)
                    if sc >= 60:
                        if st.button("🤝 签订契约，拉入助战队伍！(BIND PARTNER)", use_container_width=True):
                            buffs["syn_linked"] = True
                            buffs["syn_data"] = {
                                "name": f"{st.session_state['cur_sync_node']}系道侣", 
                                "atk_mul": st.session_state["cur_sync_mul"], "def_mul": st.session_state["cur_sync_mul"], "hp_mul": st.session_state["cur_sync_mul"],
                                "cp_bonus": sc*200
                            }
                            st.success(f"契约达成！道侣已加入队伍，全属性倍率已更新！请前往左侧和 PVE 面板查看战力飙升！")
                            time.sleep(1.5)
                            st.rerun()
                else:
                    render_html("""
                    <div class="glass-panel" style="text-align:center; border-color:var(--pink); padding:40px 20px; margin-top:10px;">
                        <div style="font-size:50px; margin-bottom:15px; animation:blink 1.5s infinite; text-shadow:0 0 20px var(--pink);">🔗</div>
                        <div style="color:var(--pink); font-family:'Orbitron'; font-size:16px; font-weight:bold; letter-spacing:2px;">SOULMATES MATRIX</div>
                        <div style="color:#aaa; font-size:12px; margin-top:10px;">尚未匹配。<br>请在左侧发起神经链结测算。</div>
                    </div>
                    """)

        with t_shop:
            c_sh1, c_sh2 = st.columns([1, 1], gap="large")
            with c_sh1:
                render_html("<div style='color:var(--sp); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ CYBER SHRINE ] 黑市盲盒商店</div>")
                
                @st_fragment
                def render_shop():
                    render_html(f"""
                    <div class='glass-panel' style='padding:20px; border-color:var(--sp); margin-bottom:10px; text-align:center;'>
                        <div style='font-size:12px; color:#aaa; margin-bottom:10px;'>消耗 PVE 掉落的功德抽取极品词条，<b style="color:var(--sp);">永久增加基础面板与最终 CP！</b></div>
                        <div style='font-size:10px; color:#888; margin-bottom:10px;'>掉率: R(60%) | SR(25%) | SSR(10%) | UR(4%) | SP(1%)</div>
                        <div style='font-size:30px; font-family:Orbitron; color:var(--sp); font-weight:bold; margin-bottom:10px; text-shadow:0 0 10px var(--sp);'>MERITS: {shop['creds']:,}</div>
                    </div>
                    """)
                    
                    if st.button("🪙 消耗 1,000 功德敲击赛博木鱼 (抽一次)", use_container_width=True):
                        if shop["creds"] >= 1000:
                            shop["creds"] -= 1000
                            pull = random.choices(
                                [("R", 500, "#00f3ff"), ("SR", 1500, "#a855f7"), ("SSR", 5000, "#fcee0a"), ("UR", 15000, "#ff007c"), ("SP", 50000, "#ffaa00")],
                                weights=[60, 25, 10, 4, 1], k=1
                            )[0]
                            r_tier, b_cp, c_col = pull
                            
                            # 算法无限生成装备词条
                            if random.random() > 0.5:
                                item_name = f"{random.choice(ITEM_PREFIXES)}{random.choice(ITEM_SUFFIXES)}"
                            else:
                                item_name = random.choice(list(EQUIPS_DICT.values())).split('】')[-1].split('(')[0].strip()
                                
                            clean_relic = f"[{r_tier}] {item_name} (+{b_cp} CP)"
                            
                            # 🚨 真实存入底层逻辑：增加基础属性，触发全局重绘
                            shop["relics"].append(clean_relic)
                            shop["b_cp"] += b_cp
                            
                            b_a = int(b_cp * 0.08)
                            b_d = int(b_cp * 0.05)
                            b_h = int(b_cp * 0.3)
                            
                            shop["b_atk"] += b_a
                            shop["b_def"] += b_d
                            shop["b_hp"] += b_h
                            
                            st.success(f"🎉 佛祖显灵！抽出 {r_tier} 级词条: {clean_relic}！攻击 +{b_a}, 血量 +{b_h}！左侧真实战力已永久飙升！")
                            time.sleep(1.0)
                            st.rerun() 
                        else:
                            st.error("赛博功德不足！请前往【逆天改命】面板击杀人生拦路虎赚取功德！")
                render_shop()
            with c_sh2:
                render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ INVENTORY ] 你的装备背囊</div>")
                r_items = shop["relics"]
                if not r_items: r_items = ["【空空如也，快去抽卡】"]
                sk_html = "".join([f"<div class='relic-item' style='color:{'var(--sp)' if 'SP' in s or 'UR' in s else 'var(--primary)'};'><div style='overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{s}</div></div>" for s in reversed(r_items)])
                render_html(f"<div class='glass-panel' style='height:300px; overflow-y:auto; border-left-color:var(--primary);'><div class='relic-grid'>{sk_html}</div></div>")

        with t_deck:
            hand_html = '<div class="hand-container">'
            labels = ["OS_YEAR", "ENV_MONTH", "CORE_DAY", "THD_TIME"]
            for i in range(4):
                is_core = (i == 2)
                c_cls = "hc-core" if is_core else ""
                c_col = dm_color if is_core else "#aaa"
                hand_html += f"""<div class="hand-card {c_cls}" style="color:{c_col};"><div class="hc-val">{bz[i][0]}</div><div class="hc-sub">{bz[i][1]}</div><div class="hc-tag">{labels[i]}</div></div>"""
            hand_html += '</div>'
            render_html(hand_html)

            c_d1, c_d2 = st.columns(2)
            with c_d1:
                DEEP_LORE_HTML = f"""
                <div class="glass-panel" style="padding:15px; border-left-color:{dm_color}; height:210px;">
                    <div style="background:rgba(0,0,0,0.6); padding:10px; border:1px solid #333; font-family:'Fira Code'; font-size:12px; margin-bottom:10px;">
                        <div style="color:{dm_color}; margin-bottom:5px; font-weight:bold;">[ EVOLUTION TREE ] 觉醒树</div>
                        <div style="color:#aaa;">{dm_evo}</div>
                        <div style="color:#fff; font-weight:bold; margin-top:5px;">终极神权: {dm_ult}</div>
                    </div>
                    <div style="background:rgba(244,63,94,0.1); border-left:3px solid var(--pink); padding:10px; font-family:'Fira Code'; font-size:12px;">
                        <div style="color:var(--pink); font-weight:bold; margin-bottom:4px;">[ FATAL VULNERABILITY ] 系统高危漏洞</div>
                        <div style="color:#ddd; margin-bottom:5px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{dm_flaw}</div>
                        <div style="color:var(--green);">> SYS_HOTFIX: {dm_patch}</div>
                    </div>
                </div>
                """
                render_html(DEEP_LORE_HTML)
            with c_d2:
                # 初始装备
                clean_skills = [s.split(' (')[0] for s in shop["relics"] if "白板" not in s]
                sk_html = "".join([f"<div class='relic-item' style='color:{'var(--sp)' if 'SP' in s else 'var(--primary)'};'><div style='overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{s}</div></div>" for s in reversed(clean_skills)])
                render_html(f"""
                <div class="glass-panel" style="padding:15px; border-left-color:var(--yellow); height:210px; overflow-y:auto;">
                    <div style="font-size:11px; color:var(--yellow); font-family:'Orbitron'; margin-bottom:5px; font-weight:bold;">>> KARMIC LORE (前世残存)</div>
                    <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:4px;">{past_life['title']}</div>
                    <div style="color:#aaa; font-size:11px; line-height:1.5; margin-bottom:10px;">{past_life['debt']}</div>
                    <div style="font-size:11px; color:var(--primary); font-family:Orbitron; margin-bottom:6px; font-weight:bold;">>> EQUIPPED RELICS (已挂载黑市圣遗物)</div>
                    <div class='relic-grid'>{sk_html}</div>
                </div>
                """)

            render_html(f"""
            <div class="glass-panel" style="border-left-color:{corr_col}; padding:15px; margin-bottom:0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:12px; color:{corr_col}; font-family:'Orbitron'; font-weight:bold;">>> CORRUPTION SCAN (精神污染度检测): {corr_tag}</div>
                    <div style="font-size:18px; font-weight:900; color:{corr_col}; font-family:'Orbitron'; line-height:1;">{corruption}%</div>
                </div>
                <div style="color:#aaa; font-size:12px; margin-top:5px;">{corr_desc}</div>
            </div>
            """)

        with t_map:
            # 🚨 满血回归：所有复杂大盘图表组合
            c_m1, c_m2 = st.columns(2, gap="large")
            with c_m1:
                render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ DOMAIN EXPANSION ] 3D 全网战区拓扑仪</div>")
                st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False})
                render_html("<div style='font-size:12px; color:var(--pink); font-family:Orbitron; margin-top:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 10-YEAR WIN RATE ] 数据人生 10年大运走势</div>")
                st.plotly_chart(f_trend, use_container_width=True, config={'displayModeBar': False})
            with c_m2:
                render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ COMBAT RADAR ] 六维人生雷达</div>")
                st.plotly_chart(f_radar, use_container_width=True, config={'displayModeBar': False})
                render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 12-MONTH META SHIFT ] 年度环境热力图</div>")
                st.plotly_chart(f_hm, use_container_width=True, config={'displayModeBar': False})

        with t_export:
            @st_fragment
            def render_exports():
                # 🚨【五大导出系统全量安全重构 & 版权归属无名逆流】彻底修复 components 报错！
                render_html(f"<div style='text-align:center; color:#888; font-size:13px; margin-top:10px; margin-bottom:15px;'>资产分发中心。可压制实体卡砖或提取底层数据。© {COPYRIGHT}</div>")
                e_psa, e_web3, e_txt, e_json, e_asc = st.tabs(["📸 PSA 10 实体卡砖", "💻 智能合约铸造", "📜 万字机密档案", "💾 JSON 底包", "📟 ASCII 卡片"])
                
                with e_psa:
                    c_e1, c_e2, c_e3 = st.columns([1, 2, 1])
                    with c_e2:
                        if st.button("📸 压制 PSA 10 典藏卡砖 (MINT SLAB)", use_container_width=True):
                            clean_sk = [s.split(' (')[0].split('】')[-1].strip() if '】' in s else s for s in shop["relics"]]
                            sk_h = "".join([f"<span style='background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); color:#fff; padding:2px 6px; margin:2px; font-size:9px; display:inline-block; font-family:Fira Code; border-radius:2px;'>{s}</span>" for s in reversed(clean_sk[-5:])])
                            
                            # 🚨 终极防爆渲染：没有任何 Python f-string 冲突。彻底引入 components。
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
                                
                                .card-inner { background:#050810; border-radius:8px; border:4px solid __COLOR__; padding:15px; position:relative; overflow:hidden; box-shadow:0 5px 15px rgba(0,0,0,0.5);}
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
                                        <div>__CPY__ TCG - FIRST EDITION</div>
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
                                    
                                    <div style="text-align:right; font-family:'Orbitron'; font-size:8px; color:#666; margin-top:10px;">© 2026 __CPY__</div>
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
                            html_ready = html_ready.replace("__TIER__", rarity).replace("__CP__", f"{fin_cp:,}")
                            html_ready = html_ready.replace("__WPN__", dm_wpn.split('】')[-1].strip() if '】' in dm_wpn else dm_wpn).replace("__SKILL__", dm_skill).replace("__DESC__", dm_desc)
                            html_ready = html_ready.replace("__EQUIPS__", sk_h).replace("__ATK__", f"{fin_atk:,}").replace("__HP__", f"{fin_hp:,}").replace("__CPY__", COPYRIGHT.upper())
                            
                            # 🚨 调用组件，报错彻底根除！
                            components.html(html_ready, height=750)
                
                with e_web3:
                    render_html("<div style='font-size:13px; color:#aaa; margin-bottom:10px;'>系统已将您的神权主将卡编译为标准的 Solidity ERC-721 智能合约源码，随时可上链铸造。</div>")
                    contract_code = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@tcg-matrix/contracts/token/ERC721.sol";
// ==========================================
// POWERED BY {COPYRIGHT}
// ==========================================

contract Karma_TCG_V300 is ERC721 {{
    // > MINT_TARGET : {player_name}
    // > CARD_RARITY : {rarity} (CP: {fin_cp})
    // > HASH_ID     : 0x{hash_id}
    
    function mintCommanderCard() public {{
        uint256 tokenId = uint256(keccak256(abi.encodePacked("{hash_id}")));
        _mint(msg.sender, tokenId);
    }}
}}"""
                    st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
                    st.code(contract_code, language="solidity")
                    st.markdown('</div>', unsafe_allow_html=True)

                with e_txt:
                    TXT_LORE = f"""======================================
[ {VERSION} ] 数据人生·绝密卡组档案 
======================================

>> 1. 玩家档案 (PLAYER DATA)
▸ 身份：{player_name} ({base.get('gender', 'X')})
▸ 哈希：0x{hash_id}
▸ 最终战力：{fin_cp:,} CP [{rarity}]
▸ 共鸣：{base['reso_buff']}

>> 2. 底层手牌 (DECK LOADOUT)
▸ {bz[0]} (年) | {bz[1]} (月) | {bz[2]} (日) | {bz[3]} (时)

>> 3. 主将设定 (COMMANDER LORE)
▸ 代号：{dm_key} ({dm_info.get('element', '')}系)
▸ 职阶：{dm_class}
▸ MBTI：[ {dm_mbti} ]
▸ 最终实战面板：ATK {fin_atk:,} | DEF {fin_def:,} | HP {fin_hp:,} | CRI {fin_crit}%
▸ 挂载神谕：{buffs['oracle_data']['name']}
▸ 挂载道侣：{buffs['syn_data']['name']}
▸ 特质：{dm_desc}
▸ 武装：{dm_wpn} | 技能：{dm_skill}

>> 4. 终极演化与系统漏洞 (EVOLUTION & PATCH)
▸ 觉醒路线：{dm_evo}
▸ 究极化神：{dm_ult}
▸ 致命隐患：{dm_flaw}
▸ 应对方案：{dm_patch}

>> 5. 业力与武装 (KARMA & EQUIPS)
▸ 前世残存：{past_life['title']} ({past_life['debt']})
▸ 挂载装备库：{', '.join(shop["relics"])}

======================================
© 2026 {COPYRIGHT}. ALL RIGHTS RESERVED.
======================================"""
                    st.markdown('<div data-testid="stCodeBlock">', unsafe_allow_html=True)
                    st.code(TXT_LORE, language="markdown")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.download_button(label="📥 下载深度绝密档案 (.TXT)", data=TXT_LORE, file_name=f"LORE_{player_name}.txt", mime="text/plain", use_container_width=True)

                with e_json:
                    export_data = {
                        "version": VERSION, "copyright": COPYRIGHT, "player": player_name, "rarity": rarity, "cp": fin_cp,
                        "commander": { "id": dm_key, "class": dm_class, "atk": fin_atk, "def": fin_def, "hp": fin_hp, "evolution": dm_ult, "flaw": dm_flaw, "patch": dm_patch },
                        "deck": bz, "equips": shop["relics"], "lore": past_life,
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
> CP_VAL : {fin_cp:,} CP [{rarity}]
--------------------------------------------------------
[ CORE DECK / 主战手牌 ]
  {bz[0]}   |   {bz[1]}   | >> {bz[2]} << |   {bz[3]}

[ COMMANDER / 主将面板 ]
> NAME   : {dm_key} ({dm_class.split('/')[0].strip()})
> WEAPON : {dm_wpn.split('】')[-1].strip() if '】' in dm_wpn else dm_wpn}
> STATS  : ATK {fin_atk:,} | DEF {fin_def:,} | HP {fin_hp:,}

[ RADAR / 属性水晶 ]
  GOLD(财力) : {wx_scores.get('金',0):02d}% |{m_b(wx_scores.get('金',0))}|
  EXEC(执行) : {wx_scores.get('木',0):02d}% |{m_b(wx_scores.get('木',0))}|
  INT (智慧) : {wx_scores.get('水',0):02d}% |{m_b(wx_scores.get('水',0))}|
  LUCK(气运) : {wx_scores.get('火',0):02d}% |{m_b(wx_scores.get('火',0))}|
  CON (体魄) : {wx_scores.get('土',0):02d}% |{m_b(wx_scores.get('土',0))}|
========================================================
POWERED BY {COPYRIGHT}
```"""
                    st.markdown(ASC_TEMP)

            render_exports()

    # =========================================================================
    # ⌨️ [ TERMINAL ] 内联极简指令台 (加入无名逆流版权彩蛋)
    # =========================================================================
    st.markdown("---")
    @st_fragment
    def render_terminal():
        current_logs = st.session_state["term_logs"]
        log_html = "<br>".join(current_logs[-4:])
        render_html(f"<div style='max-width: 800px; margin: 0 auto; background:#000; border:1px solid #333; padding:15px; font-family:\"Fira Code\"; color:var(--primary); font-size:13px; height:120px; display:flex; flex-direction:column-reverse; overflow:hidden; border-left:4px solid var(--primary);'><div>{log_html}<span style=\"animation:blink 1s infinite;\">_</span></div></div>")

        with st.form("inline_terminal", clear_on_submit=True, border=False):
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1:
                cmd_input = st.text_input("CMD", label_visibility="collapsed", placeholder="> ROOT:~# 输入指令 (如: /rank, /wuming)...")
            with col_t2:
                sub_cmd = st.form_submit_button("⏎", use_container_width=True)
                
            if sub_cmd and cmd_input:
                cmd_str = str(cmd_input).strip()
                logs = st.session_state["term_logs"]
                logs.append(f"<span style='color:#fff;'>> {cmd_str}</span>")
                cmd_lower = cmd_str.lower()
                if cmd_lower == '/help': logs.append("<span style='color:#aaa;'>CMDS: /rank, /ping, /clear, /wuming</span>")
                elif cmd_lower == '/rank': 
                    rank_pct = min(99.99, max(1.0, fin_cp / 50000.0))
                    logs.append(f"<span style='color:var(--sp);'>[SYS] 当前战力(CP {fin_cp:,})击败了矩阵中 {rank_pct:.2f}% 的玩家。</span>")
                elif cmd_lower == '/clear': 
                    st.session_state["term_logs"] = ["> TERMINAL CLEARED."]
                    st.rerun()
                elif cmd_lower == '/wuming': logs.append(f"<span style='color:var(--sp); font-weight:bold;'>[EASTER EGG] 欢迎来到【{COPYRIGHT}】的数据神域。万物皆虚，唯代码永存。</span>")
                elif cmd_lower == '/ping': logs.append("<span style='color:var(--yellow);'>[PONG] 赛博佛祖延迟 0.00ms. 「玄不救非，氪不改命。」</span>")
                else: logs.append(f"<span style='color:var(--pink);'>[ERR] Bad Command.</span>")
                st.rerun()
    render_terminal()

    # 底部退出按钮
    render_html("<br><br>")
    _, col_b_m, _ = st.columns([1,2,1])
    with col_b_m:
        if st.button("⏏ [ SURRENDER ] 物理断网并重启人生", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================================================================
# 🛑 [ KERNEL 07 ] 版权声明 (无名逆流)
# =========================================================================
render_html(f'<div style="text-align:center; margin-top:40px; border-top: 1px dashed #333; padding-top: 30px; padding-bottom: 50px;"><div style="color:var(--primary); font-family:\'Orbitron\', sans-serif; font-size:12px; font-weight:bold; letter-spacing:4px;">© 2026 版权归属 {COPYRIGHT}</div></div>')
