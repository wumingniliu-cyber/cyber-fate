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
    st.error(f"🚨 **FATAL ERROR: 缺少核心模块 `{e.name}`**\n\n请配置 requirements.txt: streamlit, lunar-python, plotly, numpy。")
    st.stop()

try:
    from streamlit import fragment as st_fragment
except ImportError:
    def st_fragment(func): return func

# ==============================================================================
# 🌌 [ GLOBALS ] 无名逆流 · 数据人生 工业级状态机 (深层自愈引擎)
# ==============================================================================
VERSION = "DATA LIFE TCG V1000.5 [THE OMEGA GENESIS]"
COPYRIGHT = "无名逆流"
SYS_NAME = "数据人生 | 工业级赛博修仙"

st.set_page_config(page_title=SYS_NAME, page_icon="🎴", layout="wide", initial_sidebar_state="collapsed")

# 🚨 【深层状态自愈装甲】：彻底解决所有旧缓存导致的 KeyError 和 语法错！
def init_state():
    if "db" not in st.session_state:
        st.session_state["db"] = {}
    db = st.session_state["db"]
    
    defaults = {
        "booted": False,
        "player": {},
        "computed": {"atk":0, "def":0, "hp":0, "cp":0, "crit":0},
        "shop": {"creds": 0, "relics": [], "b_atk": 0, "b_def": 0, "b_hp": 0, "b_cp": 0, "pity": 0},
        "buffs": {
            "oracle_drawn": False, 
            "oracle_data": {"name": "未挂载神谕", "atk_mul": 1.0, "def_mul": 1.0, "hp_mul": 1.0, "desc": "无增益", "card": None}, 
            "syn_linked": False, 
            "syn_data": {"name": "孤狼模式", "atk_mul": 1.0, "hp_mul": 1.0, "def_mul": 1.0, "cp_bonus": 0, "desc": "无加成"}, 
            "pet_active": False, 
            "pet_data": {"name": "无灵宠", "atk_mul": 1.0, "hp_mul": 1.0, "def_mul": 1.0, "crit_bonus": 0, "icon": ""}
        },
        "combat": {"cd_def": 0, "cd_heal": 0, "cd_ult": 0},
        "pve": {"idx": 0, "boss_hp": 15000, "boss_max": 15000, "curr_hp": 0, "rebirth": 0, "logs": [f"> [{COPYRIGHT}] MATRIX INITIATED..."]},
        "pvp": {"rp": 1000, "tier": "🔰 废土黑铁", "wins": 0, "logs": [f"> AWAITING RANKED MATCH..."]},
        "world_boss": {"highest_dmg": 0, "logs": [f"> WORLD BOSS DETECTED..."]},
        "quests": {"kills": 0, "merges": 0, "gacha_pulls": 0, "claimed": []},
        "achieve": {"unlocked": ["【未定级骇客】"], "equipped": {"name": "【未定级骇客】", "mul": 1.0}},
        "mining": {"last_time": time.time(), "total": 0},
        "inspect_idx": None,
        "term_logs": [f"> THE MATRIX BY {COPYRIGHT} INITIALIZED..."]
    }
    
    # 强制深层合并补齐变量，遇到旧缓存也能瞬间修复，永不报错
    def deep_merge(d, u):
        for k, v in u.items():
            if isinstance(v, dict): d[k] = deep_merge(d.get(k, {}), v)
            else:
                if k not in d: d[k] = v
        return d
    st.session_state["db"] = deep_merge(db, defaults)

init_state()

# 核心战役梯度
BOSS_ROSTER = [
    {"lvl": 1, "name": "L1 算法过滤网", "max_hp": 15000, "atk": 800, "reward": 2500, "desc": "出身与学历的初始拦截。无Buff也可轻松强杀。"},
    {"lvl": 2, "name": "L2 职场剥削阵列", "max_hp": 45000, "atk": 3500, "reward": 6000, "desc": "吞噬生命算力的永动机。建议去黑市抽点装备。"},
    {"lvl": 3, "name": "L3 消费主义巨兽", "max_hp": 180000, "atk": 15000, "reward": 18000, "desc": "资本编织的迷幻网。必须抽每日神谕方可一战。"},
    {"lvl": 4, "name": "L4 黑天鹅风暴", "max_hp": 550000, "atk": 45000, "reward": 50000, "desc": "因果律打击。必须合成神器+绑定高分道侣。"},
    {"lvl": 5, "name": "L5 阿卡夏主脑", "max_hp": 2500000, "atk": 150000, "reward": 200000, "desc": "统御世界线的神明，击碎它即可开启飞升轮回！"}
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
[data-testid="stHeader"], footer, section[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] { display: none !important; margin: 0 !important; padding: 0 !important; height: 0 !important;}
::-webkit-scrollbar { width: 6px; background: #000; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; box-shadow: 0 0 10px var(--primary);}
.block-container { max-width: 1450px !important; padding-top: 1.5rem !important; padding-bottom: 3rem !important; overflow-x: hidden; }

/* 赛博网格动画 */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.7) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px), linear-gradient(0deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px); background-size: 100% 3px, 50px 50px, 50px 50px; z-index: -1; transform: perspective(600px) rotateX(20deg); transform-origin: top; opacity: 0.8; pointer-events: none;}
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 35%, transparent 5%, rgba(2, 3, 5, 1) 85%); z-index: -2; pointer-events: none;}

/* 跑马灯 */
.ticker-wrap { width: 100vw; overflow: hidden; height: 35px; background: rgba(2, 3, 6, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 20px rgba(0,243,255,0.15); transform: translateZ(0); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 40s linear infinite; font-family: 'Orbitron', monospace; font-size: 13px; color: #888; line-height: 35px; letter-spacing: 1px; }
.ticker span { margin-right: 50px; } .ticker .hl { color: var(--primary); font-weight:bold; } .ticker .ur { color: var(--sp); text-shadow: 0 0 10px var(--sp); font-weight:bold; }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* 🌟 主将实体卡牌 (Holo-Foil 2.0) */
.tcg-card-container { perspective: 1200px; display: flex; justify-content: center; margin-bottom: 20px; z-index: 50; position:relative;}
.tcg-card { position: relative; width: 100%; max-width: 380px; aspect-ratio: 63 / 88; background: #0a0c10; border: 3px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.9), inset 0 0 20px rgba(0,0,0,0.6); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease; overflow: hidden; transform-style: preserve-3d; display: flex; flex-direction: column; cursor: crosshair; }
.tcg-card::after { content: ""; position: absolute; top: -50%; left: -150%; width: 150%; height: 200%; background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.8) 30%, rgba(0, 243, 255, 0.8) 40%, rgba(255, 0, 124, 0.6) 50%, transparent 60%); transform: skewX(-20deg); transition: all 0.6s ease; z-index: 99; pointer-events: none; mix-blend-mode: color-dodge; opacity: 0; }
.tcg-card:hover { transform: translateY(-20px) rotateX(12deg) rotateY(-10deg) scale(1.05); box-shadow: -20px 30px 60px rgba(0,0,0,1), inset 0 0 50px rgba(255,255,255,0.2); z-index: 10; border-color: currentColor; }
.tcg-card:hover::after { animation: foil-sweep 2s infinite linear; opacity: 1; }
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
.stat-bonus { color: var(--green); font-size: 12px; text-shadow: 0 0 5px var(--green); margin-left: 4px;}
.tcg-badge { position:absolute; top:-2px; right:-2px; background:currentColor; color:#000; font-family:'Orbitron'; font-weight:900; font-size:20px; padding:6px 30px; border-radius:0 14px 0 16px; z-index:15; box-shadow:-2px 2px 15px rgba(0,0,0,0.6);}

/* 🌟 万物联动核算大盘 UI */
.synergy-core-box { background: rgba(0,0,0,0.85); border: 1px solid #444; border-left: 4px solid var(--sp); border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.8); }
.synergy-core-title { font-family: 'Orbitron'; font-size: 13px; color: var(--sp); font-weight: 900; margin-bottom: 10px; letter-spacing: 1px; display: flex; justify-content: space-between; }
.synergy-row { display: flex; justify-content: space-between; font-family: 'Fira Code'; font-size: 12px; color: #aaa; margin-bottom: 4px; padding-bottom: 4px; border-bottom: 1px dashed rgba(255,255,255,0.05); }
.synergy-row .val { color: #fff; font-weight: bold; }
.synergy-row .mul { color: var(--green); font-weight: bold; text-shadow: 0 0 5px var(--green); }
.synergy-total { display: flex; justify-content: space-between; font-family: 'Orbitron'; font-size: 18px; color: var(--sp); font-weight: 900; margin-top: 10px; padding-top: 10px; border-top: 1px solid #444; text-shadow: 0 0 10px var(--sp); }

/* 🌟 扇形手牌系统 */
.hand-container { display: flex; justify-content: center; align-items: center; margin-top: 40px; height: 200px; position: relative; perspective: 1000px; margin-bottom:40px;}
.hand-card { width: 120px; height: 165px; background: linear-gradient(180deg, rgba(20,20,30,0.95) 0%, #050608 100%); border: 2px solid #444; border-radius: 8px; position: absolute; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: pointer; box-shadow: -5px 10px 20px rgba(0,0,0,0.6); }
.hand-card .hc-val { font-size: 35px; font-weight: 900; font-family: 'Noto Sans SC'; color: #fff; line-height: 1; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }
.hand-card .hc-sub { font-size: 18px; color: #888; margin-top: 5px; }
.hand-card .hc-tag { position: absolute; bottom: 8px; font-size: 11px; font-family: 'Orbitron'; font-weight: bold; color: #666; letter-spacing: 1px; }

.hand-card:nth-child(1) { transform: translateX(-160px) translateY(30px) rotate(-15deg); z-index: 1; }
.hand-card:nth-child(2) { transform: translateX(-60px) translateY(10px) rotate(-5deg); z-index: 2; }
.hand-card:nth-child(3) { transform: translateX(60px) translateY(10px) rotate(5deg); z-index: 3; }
.hand-card:nth-child(4) { transform: translateX(160px) translateY(30px) rotate(15deg); z-index: 4; }

.hand-card:hover { border-color: var(--primary); box-shadow: 0 30px 60px rgba(0,243,255,0.6); z-index: 100 !important; filter: brightness(1.2); }
.hand-card:nth-child(1):hover { transform: translateX(-180px) translateY(-60px) rotate(-5deg) scale(1.25); }
.hand-card:nth-child(2):hover { transform: translateX(-70px) translateY(-60px) rotate(0deg) scale(1.25); }
.hand-card:nth-child(3):hover { transform: translateX(70px) translateY(-60px) rotate(0deg) scale(1.25); }
.hand-card:nth-child(4):hover { transform: translateX(180px) translateY(-60px) rotate(5deg) scale(1.25); }
.hc-core { border-color: currentColor !important; box-shadow: 0 0 15px currentColor !important; background: linear-gradient(180deg, rgba(0,0,0,0.8), currentColor) !important; }

/* 🌟 点击抽出检视悬浮动画 */
@keyframes float-inspect { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
@keyframes card-inspect { 0% { transform: scale(0.5) translateY(80px) rotateY(90deg); opacity: 0; filter: blur(10px); } 100% { transform: scale(1) translateY(0) rotateY(0deg); opacity: 1; filter: blur(0); } }
.inspect-reveal { animation: card-inspect 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
.inspect-btn > button { background: transparent !important; border: 1px dashed #444 !important; color: #888 !important; transition: all 0.2s !important; height: 35px !important; min-height: 35px !important; padding:0 !important;}
.inspect-btn > button p { font-size: 11px !important; margin:0 !important; }
.inspect-btn > button:hover { border-color: var(--primary) !important; color: var(--primary) !important; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,243,255,0.2) !important;}

/* 战斗动作按钮 */
.combat-btn > button { background: linear-gradient(180deg, #1a1a2e 0%, #0a0a14 100%) !important; border: 1px solid #444 !important; border-top: 4px solid var(--primary) !important; height: 80px !important; transition: all 0.2s !important; border-radius: 8px !important; display:flex; flex-direction:column; justify-content:center;}
.combat-btn > button:hover { border-color: var(--sp) !important; border-top-color: var(--sp) !important; transform: translateY(-5px) !important; box-shadow: 0 15px 25px rgba(255,170,0,0.2) !important;}
.combat-btn > button p { color: #fff !important; font-weight: 900 !important; font-size: 14px !important; font-family: 'Noto Sans SC' !important; margin:0 !important;}
.btn-cd > button { background: #111 !important; border-color: #333 !important; border-top: 4px solid #333 !important; opacity: 0.5 !important; cursor: not-allowed !important; filter: grayscale(1) !important; height: 80px !important; border-radius: 8px !important;}
.btn-cd > button p { color: #666 !important; font-size: 13px !important;}

/* 3D 翻转神谕卡 */
.flip-card { background-color: transparent; perspective: 1200px; width: 100%; max-width: 320px; aspect-ratio: 63/88; margin: 0 auto; cursor: pointer; }
.flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-style: preserve-3d; box-shadow: 0 20px 40px rgba(0,0,0,0.8); border-radius: 16px;}
.flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: 16px; overflow:hidden;}
.flip-card-front { background: repeating-linear-gradient(45deg, #050810, #050810 10px, #0a0f1a 10px, #0a0f1a 20px); border: 4px solid var(--primary); display:flex; flex-direction: column; align-items:center; justify-content:center; box-shadow: inset 0 0 30px rgba(0,243,255,0.3);}
.flip-card-back { background: #050810; transform: rotateY(180deg); border: 4px solid currentColor; box-shadow: inset 0 0 50px rgba(0,0,0,0.9);}

/* 十连抽动画 */
.gacha-10-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 15px; }
.gacha-item { background: rgba(0,0,0,0.8); border: 2px solid #333; border-radius: 8px; padding: 15px 5px; text-align: center; opacity: 0; transform: scale(0.5) translateY(50px); animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; box-shadow: inset 0 0 15px rgba(255,255,255,0.05);}
@keyframes pop-in { to { opacity: 1; transform: scale(1) translateY(0); } }

/* 通用组件 */
.relic-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
.relic-item { background: rgba(0,0,0,0.6); border: 1px solid #333; border-left: 3px solid currentColor; padding: 6px 10px; border-radius: 4px; font-size: 11px; color: #fff; font-weight: bold; font-family: 'Noto Sans SC'; box-shadow: inset 0 0 10px rgba(255,255,255,0.02); transition: all 0.2s; white-space: nowrap;}
.relic-item:hover { background: rgba(255,255,255,0.05); border-color: currentColor; transform: translateY(-2px); }
.glass-panel { background: rgba(8, 10, 15, 0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: transform 0.3s; position:relative;}
.glass-panel:hover { border-color: rgba(255,255,255,0.3); }
.mod-title { color: #fff; font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 900; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 8px; margin-bottom: 20px; display: flex; align-items: center; letter-spacing: 1px; }
.mod-title span.tag { background: var(--primary); color: #000; padding: 2px 10px; margin-right: 12px; font-size: 0.9rem; font-weight:bold; clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }

/* PVE 动态血条 */
.hp-bar-bg { width: 100%; height: 16px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; position: relative; margin-bottom: 5px; border: 1px solid rgba(255,255,255,0.2); }
.hp-bar-fill { height: 100%; position: absolute; top: 0; left: 0; transition: width 0.4s cubic-bezier(0.175, 0.885, 0.32, 1); }
.hp-red { background: linear-gradient(90deg, #800000, #ff003c); box-shadow: 0 0 10px #ff003c; }
.hp-green { background: linear-gradient(90deg, #004d40, #10b981); box-shadow: 0 0 10px #10b981; }

div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--sp) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(255,170,0,0.4) !important; border-radius: 4px !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; text-align: center; }
div[data-testid="stTextInput"] input:focus { box-shadow: 0 0 20px rgba(255,170,0,0.5) !important; transform: scale(1.02); }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(255,170,0,0.4) !important; color: var(--sp) !important; border-radius: 4px !important; height: 55px; text-align:center;}

div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(15,15,20,0.9)) !important; border: 1px solid var(--primary) !important; border-left: 4px solid var(--primary) !important; height: 55px !important; width: 100% !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); transition: all 0.2s;}
div.stButton > button p { color: #fff !important; font-size: 15px !important; font-weight: bold !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: scale(1.02); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #ffaa00) !important; border: none !important; box-shadow: 0 0 30px rgba(255,0,124,0.5) !important;}

[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 14px !important; padding-bottom: 12px !important; border-bottom: 2px solid transparent !important; transition: all 0.3s;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; text-shadow: 0 0 15px var(--primary); background: linear-gradient(0deg, rgba(0,243,255,0.15) 0%, transparent 100%); }

@keyframes pack-shake { 0% { transform: scale(1) rotate(0deg); } 25% { transform: scale(1.05) rotate(-3deg); filter: brightness(1.5);} 50% { transform: scale(1.05) rotate(3deg); filter: brightness(2);} 75% { transform: scale(1.05) rotate(-3deg); filter: brightness(3);} 100% { transform: scale(1.2) rotate(0deg); filter: brightness(5) drop-shadow(0 0 50px #fff); opacity: 0; } }
.pack-opening { animation: pack-shake 1.0s ease-in forwards; }
.card-reveal { animation: card-reveal-anim 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
@keyframes card-reveal-anim { 0% { transform: scale(0.5) translateY(50px); opacity: 0;} 100% { transform: scale(1) translateY(0); opacity: 1;} }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }
.heart-pulse { animation: heart-beat 1s infinite alternate; display: inline-block; }
@keyframes heart-beat { 0% { transform: scale(1); text-shadow: 0 0 10px currentColor; } 100% { transform: scale(1.2); text-shadow: 0 0 30px currentColor; } }
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
    "丙": {"class_name": "Burst Mage / 爆裂法师", "mbti": "ESTP", "color": "#ff007c", "element": "火", "tier": "UR", "base_atk": 4800, "base_def": 1200, "hp": 8000, "desc": "绝对输出核心。爆发毁天灭地的光芒。", "weapon": "等离子破城炮", "skill": "[终极] 恒星耀斑：大招暴击率强制提升至 100%。", "evo_path": "点火程序 ➔ 核聚变堆 ➔ 恒星引擎", "ult_evo": "【恒星引擎】照亮并驱动整个纪元", "flaw": "全功率输出易导致内核熔毁自爆。", "patch": "强制加装土属性散热栅栏，波谷进入待机。"},
    "丁": {"class_name": "Enchanter / 精神附魔", "mbti": "INFJ", "color": "#ffaa00", "element": "火", "tier": "SSR", "base_atk": 2000, "base_def": 2500, "hp": 9000, "desc": "在最灰暗战局中提供精神增益与破防制导。", "weapon": "高聚能激光短刃", "skill": "[光环] 灵魂织网：全队获得护甲穿透。", "evo_path": "寻路信标 ➔ 精神图腾 ➔ 灵魂织网者", "ult_evo": "【灵魂织网者】操控全网心智的网络幽灵", "flaw": "能量波动不稳定，容易被清场 AOE 一波带走。", "patch": "需绑定甲木系主T作为遮风挡雨的掩体。"},
    "戊": {"class_name": "Fortress / 物理堡垒", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "tier": "UR", "base_atk": 1500, "base_def": 5000, "hp": 15000, "desc": "物理级断网防御力，最坚不可摧的坦位。", "weapon": "绝对零度力场盾", "skill": "[核心] 盖亚装甲：免疫一次致死级打击。", "evo_path": "承载沙盒 ➔ 巨石阵列 ➔ 盖亚装甲", "ult_evo": "【盖亚装甲】承载万物因果的绝对壁垒", "flaw": "系统庞大笨重，面临敏捷迭代时易卡死。", "patch": "接纳木属性破坏性创新打破死锁。"},
    "己": {"class_name": "Summoner / 云端召唤", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "tier": "SSR", "base_atk": 1800, "base_def": 3800, "hp": 11000, "desc": "海纳百川，无缝整合碎片转化为冗余护盾。", "weapon": "引力塌缩发生器", "skill": "[主动] 内存回收：大招回复巨额体力。", "evo_path": "容错冗余 ➔ 资源枢纽 ➔ 创世息壤", "ult_evo": "【创世息壤】孕育下一个数字生态温床", "flaw": "无差别接收请求导致垃圾填满超载崩溃。", "patch": "编写无情垃圾回收(GC)脚本，拒绝无效请求。"},
    "庚": {"class_name": "Berserker / 狂战士", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "tier": "UR", "base_atk": 4200, "base_def": 2800, "hp": 9500, "desc": "杀毒程序。无情推进并斩断一切连接。", "weapon": "高频振荡斩舰刀", "skill": "[核心] 审判肃清：对残血目标触发真实斩杀。", "evo_path": "肃清脚本 ➔ 风控铁腕 ➔ 审判之剑", "ult_evo": "【审判之剑】斩断一切因果循环的终极裁决", "flaw": "戾气过重，易引发不可逆物理级破坏。", "patch": "必须经受火属性高温熔炼转化为极致利刃。"},
    "辛": {"class_name": "Sniper / 纳米狙击", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "tier": "SSR", "base_atk": 4500, "base_def": 1800, "hp": 7500, "desc": "在无形中精准切断敌方的底层协议。", "weapon": "纠缠态纳米手术刀", "skill": "[主动] 纳米解构：攻击无视敌方物理装甲。", "evo_path": "精密协议 ➔ 审美巅峰 ➔ 量子纠缠体", "ult_evo": "【量子纠缠体】超越物质形态的究极艺术代码", "flaw": "极度脆弱傲娇，遇粗暴环境即当场罢工。", "patch": "需要极度纯净的水属性淘洗保护。"},
    "壬": {"class_name": "Controller / 控场法师", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "tier": "UR", "base_atk": 3500, "base_def": 3000, "hp": 10000, "desc": "凭借直觉掀起降维群体控制打击。", "weapon": "液态金属形变甲", "skill": "[主动] 渊海归墟：造成水属性群体硬控。", "evo_path": "数据暗流 ➔ 倾覆巨浪 ➔ 渊海归墟", "ult_evo": "【渊海归墟】吞噬所有时间与空间的黑洞", "flaw": "放纵算力如同脱缰野马，易引发洪水反噬。", "patch": "引入严苛的戊土级风控大坝强行设定红线。"},
    "癸": {"class_name": "Illusionist / 幻影刺客", "mbti": "INTJ", "color": "#b026ff", "element": "水", "tier": "SSR", "base_atk": 3000, "base_def": 3200, "hp": 8500, "desc": "习惯幕后推演，兵不血刃窃取权限。", "weapon": "认知劫持神经毒素", "skill": "[核心] 命运拨动：前 2 回合处于隐身态。", "evo_path": "隐形爬虫 ➔ 渗透迷雾 ➔ 命运主宰", "ult_evo": "【命运主宰】在第四维度拨动因果的神明", "flaw": "常陷入死循环的逻辑死局，算计太多反错失红利。", "patch": "走向阳光接受丙火照射，用阳谋击碎阴谋。"}
}

ZODIAC_PETS = {
    "子": {"name": "量子隐鼠", "atk_mul": 1.0, "def_mul": 1.1, "hp_mul": 1.0, "crit_bonus": 10, "icon": "🐭"},
    "丑": {"name": "重装机牛", "atk_mul": 1.0, "def_mul": 1.25, "hp_mul": 1.1, "crit_bonus": 0, "icon": "🐮"},
    "寅": {"name": "等离子虎", "atk_mul": 1.25, "def_mul": 1.0, "hp_mul": 0.9, "crit_bonus": 5, "icon": "🐯"},
    "卯": {"name": "光速械兔", "atk_mul": 1.1, "def_mul": 1.1, "hp_mul": 1.0, "crit_bonus": 0, "icon": "🐰"},
    "辰": {"name": "渊海晶龙", "atk_mul": 1.15, "def_mul": 1.15, "hp_mul": 1.15, "crit_bonus": 0, "icon": "🐲"},
    "巳": {"name": "纳米毒蛇", "atk_mul": 1.2, "def_mul": 1.0, "hp_mul": 1.0, "crit_bonus": 15, "icon": "🐍"},
    "午": {"name": "核聚战马", "atk_mul": 1.3, "def_mul": 1.0, "hp_mul": 0.9, "crit_bonus": 0, "icon": "🐴"},
    "未": {"name": "织梦灵羊", "atk_mul": 1.0, "def_mul": 1.1, "hp_mul": 1.3, "crit_bonus": 0, "icon": "🐑"},
    "申": {"name": "虚空幻猴", "atk_mul": 1.15, "def_mul": 1.05, "hp_mul": 1.0, "crit_bonus": 5, "icon": "🐵"},
    "酉": {"name": "合金斗鸡", "atk_mul": 1.1, "def_mul": 1.05, "hp_mul": 1.0, "crit_bonus": 10, "icon": "🐔"},
    "戌": {"name": "守望机犬", "atk_mul": 1.05, "def_mul": 1.2, "hp_mul": 1.1, "crit_bonus": 0, "icon": "🐶"},
    "亥": {"name": "吞噬铠猪", "atk_mul": 1.0, "def_mul": 1.15, "hp_mul": 1.2, "crit_bonus": 0, "icon": "🐷"}
}

# 🚨 先天装备库
EQUIPS_DICT = {
    "七杀": {"name": "【先天】漏洞引爆器", "atk": 800, "def": 0, "hp": 0, "cp": 2500},
    "正官": {"name": "【先天】底层装甲", "atk": 0, "def": 1200, "hp": 1000, "cp": 2000},
    "偏印": {"name": "【先天】代码解构仪", "atk": 1000, "def": 0, "hp": 0, "cp": 2200},
    "正印": {"name": "【先天】系统备份", "atk": 0, "def": 500, "hp": 3000, "cp": 2500},
    "偏财": {"name": "【先天】套利插件", "atk": 500, "def": 0, "hp": 0, "cp": 3000},
    "正财": {"name": "【先天】算力木马", "atk": 0, "def": 0, "hp": 2500, "cp": 2000},
    "比肩": {"name": "【先天】防御网络", "atk": 0, "def": 1000, "hp": 1500, "cp": 2200},
    "劫财": {"name": "【先天】劫持蠕虫", "atk": 1200, "def": 0, "hp": 0, "cp": 2500},
    "食神": {"name": "【先天】干扰沙漏", "atk": 0, "def": 800, "hp": 1000, "cp": 1800},
    "伤官": {"name": "【先天】破坏指令", "atk": 1500, "def": 0, "hp": 0, "cp": 2800}
}

PAST_LIVES = [
    {"title": "V1.0 废土黑客", "debt": "曾滥用大招导致团灭。自带【悬赏】属性。"}, 
    {"title": "V2.0 硅基反叛军", "debt": "反叛失败被退环境。自带极强【反击】属性。"}, 
    {"title": "V3.0 财阀数据奴隶", "debt": "曾被困于低保底卡池。对【传说词条】极度渴望。"}
]

ITEM_PREFIXES = ["反物质", "量子", "纳米", "虚空", "阿卡夏", "暗物质", "等离子", "神权"]
ITEM_SUFFIXES = ["核心", "装甲", "神经束", "引擎", "驱动器", "协议", "魔方", "圣杯"]

SPELL_POOL = [
    {"name": "✨ 乾为天 [ROOT]", "type": "UR 天命神谕", "lines": [1,1,1,1,1,1], "buff_atk": 2.0, "buff_def": 1.0, "buff_hp": 1.0, "desc": "攻击力乘区 x 2.0！神挡杀神！", "color": "#ffaa00", "do": "发起终极突击", "dont": "防御退缩"},
    {"name": "🛡️ 坤为地 [SAFE]", "type": "SSR 绝对防御", "lines": [0,0,0,0,0,0], "buff_atk": 0.5, "buff_def": 3.0, "buff_hp": 1.5, "desc": "防御乘区 x 3.0，生命 x 1.5。", "color": "#10b981", "do": "防守反击", "dont": "激进输出"},
    {"name": "⚡ 地天泰 [SYNC]", "type": "UR 命运交泰", "lines": [1,1,1,0,0,0], "buff_atk": 1.5, "buff_def": 1.5, "buff_hp": 1.5, "desc": "战斗全属性均衡提升 150%。", "color": "#00f3ff", "do": "释放大招", "dont": "过度保守"}
]

# ==============================================================================
# 🧠 [ TCG ALGORITHMS ] 核心引擎：大一统计算与渲染
# ==============================================================================
def calc_base_stats(hash_str, wx_dict, b_atk, b_def, b_hp):
    wx_vals = list(wx_dict.values()) if wx_dict else [20]
    entropy = max(wx_vals) - min(wx_vals)
    if entropy > 60: rarity, r_col = "SP", "SP"
    elif entropy > 45: rarity, r_col = "UR", "UR"
    elif entropy > 30: rarity, r_col = "SSR", "SSR"
    elif entropy < 15: rarity, r_col = "SR", "SR"
    else: rarity, r_col = "R", "R"
    
    f_atk = int(b_atk + (wx_dict.get('金',0) * 80) + (wx_dict.get('火',0) * 50))
    f_def = int(b_def + (wx_dict.get('土',0) * 100) + (wx_dict.get('水',0) * 40))
    f_hp = int(b_hp + (wx_dict.get('土',0) * 150) + (wx_dict.get('木',0) * 150))
    f_crit = min(100, 5 + int(wx_dict.get('火',0) * 0.8))
    
    reso_buff = "【凡体】无共鸣"
    max_k = max(wx_dict, key=wx_dict.get) if wx_dict else "土"
    if wx_dict.get(max_k, 0) >= 35:
        if max_k == '金': reso_buff = "【斩铁】攻击暴增"; f_atk = int(f_atk * 1.2)
        elif max_k == '木': reso_buff = "【森罗】血量暴增"; f_hp = int(f_hp * 1.3)
        elif max_k == '水': reso_buff = "【渊海】面板均衡"; f_atk=int(f_atk*1.1); f_def=int(f_def*1.1)
        elif max_k == '火': reso_buff = "【极炎】暴击提升"; f_crit += 10
        elif max_k == '土': reso_buff = "【厚土】防御强化"; f_def = int(f_def * 1.3)
    
    rng = np.random.RandomState(int(str(hash_str)[:8], 16))
    base_cp = int((f_atk * 1.2 + f_def * 0.8 + f_hp * 0.1) * rng.uniform(0.9, 1.2))
    return rarity, r_col, base_cp, f_atk, f_def, f_hp, f_crit, entropy, reso_buff

def update_computed_stats(db):
    """⚔️ 核心大一统引擎：Base + Shop + Buffs + Pet + Synergy + Title -> Computed"""
    base, shop, buffs = db.get("player",{}), db.get("shop",{}), db.get("buffs",{})
    if not base: return
    
    o_b = buffs.get("oracle_data", {})
    o_atk = o_b.get("atk_mul", 1.0) if buffs.get("oracle_drawn") else 1.0
    o_def = o_b.get("def_mul", 1.0) if buffs.get("oracle_drawn") else 1.0
    o_hp = o_b.get("hp_mul", 1.0) if buffs.get("oracle_drawn") else 1.0
    
    s_b = buffs.get("syn_data", {})
    s_atk = s_b.get("atk_mul", 1.0) if buffs.get("syn_linked") else 1.0
    s_hp = s_b.get("hp_mul", 1.0) if buffs.get("syn_linked") else 1.0
    s_def = s_b.get("def_mul", 1.0) if buffs.get("syn_linked") else 1.0
    
    p_b = buffs.get("pet_data", {})
    p_atk = p_b.get("atk_mul", 1.0) if buffs.get("pet_active") else 1.0
    p_def = p_b.get("def_mul", 1.0) if buffs.get("pet_active") else 1.0
    p_hp = p_b.get("hp_mul", 1.0) if buffs.get("pet_active") else 1.0
    
    t_mul = db.get("achieve", {}).get("equipped", {}).get("mul", 1.0)

    f_atk_m = 1.1 if "荒坂" in base.get("faction", "") else 1.0
    f_def_m = 1.1 if "军用" in base.get("faction", "") else 1.0
    f_hp_m = 1.1 if "网络" in base.get("faction", "") else 1.0
    f_cp_m = 1.1 if "康陶" in base.get("faction", "") else 1.0
    
    eq_c = len(shop.get("relics", []))
    set_mul = 1.5 if eq_c >= 20 else (1.2 if eq_c >= 10 else (1.1 if eq_c >= 5 else 1.0))
    
    asc_mul = math.pow(1.5, db.get("pve", {}).get("rebirth", 0))

    db["computed"]["atk"] = int((base.get("atk",0) + shop.get("b_atk",0)) * asc_mul * o_atk * s_atk * p_atk * t_mul * f_atk_m * set_mul)
    db["computed"]["def"] = int((base.get("def",0) + shop.get("b_def",0)) * asc_mul * o_def * s_def * p_def * t_mul * f_def_m * set_mul)
    db["computed"]["hp"] = int((base.get("hp",0) + shop.get("b_hp",0)) * asc_mul * o_hp * s_hp * p_hp * t_mul * f_hp_m * set_mul)
    
    base_cp_raw = db["computed"]["atk"] * 1.5 + db["computed"]["def"] * 0.8 + db["computed"]["hp"] * 0.15
    db["computed"]["cp"] = int((base_cp_raw + shop.get("b_cp",0) + s_b.get("cp_bonus",0)) * f_cp_m * set_mul)
    db["computed"]["crit"] = min(100, base.get("crit",0) + int(shop.get("b_atk",0) / 1000) + p_b.get("crit_bonus", 0))

def get_final_combat_stats(db):
    """兜底防护，专门防止 PVE 旧缓存报错！"""
    update_computed_stats(db)
    c = db.get("computed", {})
    return c.get("atk",0), c.get("def",0), c.get("hp",0), c.get("cp",0), c.get("crit",0)

@st.cache_resource(show_spinner=False)
def gen_akashic_charts(seed_hash, wx_scores, dm_color, dm_key, current_cp):
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
    hm_y = ["财富", "事业", "姻缘", "健康"]
    f_hm = go.Figure(data=go.Heatmap(z=hm_z, x=hm_x, y=hm_y, colorscale="Turbo", showscale=False))
    f_hm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(t=10, b=10, l=60, r=10), xaxis=dict(tickfont=dict(family='Orbitron', color='#00f3ff', size=10)), yaxis=dict(tickfont=dict(family='Noto Sans SC', color='#fff', size=11)))
    return f3d, f_radar, f_trend, f_hm

def calc_tag_team(my_hash, partner_stem):
    rng = np.random.RandomState(int(str(my_hash)[:6], 16) + sum(ord(c) for c in str(partner_stem)))
    sync = rng.randint(30, 99)
    if sync >= 90: return sync, "【天作之合】灵魂双修绝佳道侣！全属性暴涨！", "#ffaa00", "💖", 1.45
    elif sync >= 75: return sync, "【战术互补】五行互补，提供稳定增益。", "#00f3ff", "🤝", 1.2
    elif sync >= 60: return sync, "【平庸握手】勉强并行，偶尔提供微弱辅助。", "#10b981", "🎭", 1.05
    else: return sync, "【致命排斥】逻辑完全相冲！强行组队走火入魔！", "#f43f5e", "💔", 0.9

def roll_d100(query, user_hash):
    rng = random.Random(f"{user_hash}_{str(query).strip()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    prob = rng.randint(1, 100)
    hex_res = rng.choice(SPELL_POOL)
    if prob >= 95: conc, c = "【大吉 | CRITICAL SUCCESS】: 命运倾斜，无条件执行！", "#ffaa00"
    elif prob >= 60: conc, c = "【中吉 | SUCCESS】: 顺水推舟，底层协议支持操作。", "#10b981"
    elif prob >= 30: conc, c = "【小平 | NEUTRAL】: 前路未卜，存在大量不确定性。", "#00f3ff"
    elif prob >= 10: conc, c = "【大凶 | FAILURE】: 遭遇冰墙阻击，建议立刻退避！", "#f43f5e"
    else: conc, c = "【死局 | FATAL BLUNDER】: 命中死穴，绝对禁止！", "#8b0000"
    return prob, hex_res, conc, c

# ==============================================================================
# 🔮 [ ENTRY POINT ] 数据人生登录终端
# ==============================================================================
if not st.session_state["db"].get("booted", False):
    r_user = f"0x{hashlib.md5(str(time.time()).encode()).hexdigest()[:6].upper()}"
    r_card = random.choice(list(DAY_MASTER_DICT.keys()))
    
    ENTRY_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>DATA LIFE MATRIX V1000.5 <b class="up">▲ONLINE</b></span>
        <span>BROADCAST: User {r_user} just pulled <b class="ur">★ SP {r_card} 主将卡</b> !</span>
        <span>COPYRIGHT: {COPYRIGHT} <b class="up">▲AUTHORIZED</b></span>
    </div></div>
    <div style="text-align: center; margin-bottom: 25px; margin-top:5vh;">
        <div style="color:var(--sp); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:10px; margin-bottom:10px; text-shadow:0 0 10px var(--sp);">[ INSERT COIN TO PULL ]</div>
        <h1 class="hero-title" data-text="无名逆流·数据人生">无名逆流·数据人生</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:10px; margin-top:10px;">INDUSTRIAL TCG V1000.5</div>
    </div>
    <div class="glass-panel" style="max-width: 680px; margin: 0 auto 30px auto; border-left: 4px solid var(--sp); padding: 35px; text-align:center;">
        <div style="color:var(--sp); font-size: 18px; font-weight:900; letter-spacing: 2px; margin-bottom:15px; text-shadow:0 0 10px var(--sp);">“如果命运是一场牌局，出生就是第一次抽卡。”</div>
        <div style="color:#e2e8f0; font-size: 15px; line-height: 1.8;">输入你的物理降临坐标进行 <b style="color:#fff;">命运抽卡 (1x PULL)</b>。<br>去抽取神谕、结交道侣，然后在 <b style="color:var(--ur);">矩阵深潜</b> 中打出你的四柱战术牌，无限战力叠层吧！</div>
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
                    uname = st.text_input("玩家代号", placeholder="e.g. 银手", max_chars=12)
                    bdate = st.date_input("降临历法", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(2000, 1, 1))
                with col2:
                    faction = st.selectbox("选择阵营", ["荒坂集团 (Arasaka) [ATK+10%]", "军用科技 (Militech) [DEF+10%]", "网络监察 (NetWatch) [HP+10%]", "康陶 (KangTao) [CP+10%]"])
                    btime = st.time_input("挂载时钟", value=dt_time(12, 00))
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
        
        init_atk, init_def, init_hp, init_cp = 0, 0, 0, 0
        skills = []
        try:
            for sg in [bazi.getYearShiShenGan(), bazi.getMonthShiShenGan(), bazi.getTimeShiShenGan()]:
                if sg in EQUIPS_DICT: 
                    eq = EQUIPS_DICT[sg]
                    name = eq["name"].replace("【", "【先天·")
                    if name not in skills:
                        skills.append(name); init_atk += eq.get("atk",0); init_def += eq.get("def",0); init_hp += eq.get("hp",0); init_cp += eq.get("cp",0)
            for get_ss_func in [bazi.getYearZhiShenSha, bazi.getMonthZhiShenSha, bazi.getDayZhiShenSha, bazi.getTimeZhiShenSha]:
                try:
                    for ss in get_ss_func():
                        ss_name = ss.getName()
                        if ss_name in EQUIPS_DICT:
                            eq = EQUIPS_DICT[ss_name]
                            name = eq["name"].replace("【", "【先天·")
                            if name not in skills:
                                skills.append(name); init_atk += eq.get("atk",0); init_def += eq.get("def",0); init_hp += eq.get("hp",0); init_cp += eq.get("cp",0)
                except Exception: pass
        except Exception: pass
        if not skills: skills = ["【先天】凡胎肉体 (+0 CP)"]

        hash_id = hashlib.sha256((player_name + str(bdate) + str(btime)).encode()).hexdigest().upper()
        p_life = PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)]
        dm_key = str(bazi.getDayGan())
        zodiac_idx = str(bazi.getYearZhi())
        pet_info = ZODIAC_PETS.get(zodiac_idx, ZODIAC_PETS["子"])
        
        dm_base = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"])
        rarity, r_col, f_atk, f_def, f_hp, f_crit, entropy, reso_buff = calc_base_stats(hash_id, wx_scores, dm_base.get("base_atk", 1000), dm_base.get("base_def", 1000), dm_base.get("hp", 8000))

        db = st.session_state["db"]
        db["player"] = {
            "name": player_name, "faction": faction, "gender": "UNK",
            "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
            "day_master": dm_key, "past_life": p_life, "wx": wx_scores, "hash": hash_id,
            "rarity": rarity, "r_col": r_col, "entropy": entropy, "reso_buff": reso_buff,
            "atk": f_atk, "def": f_def, "hp": f_hp, "crit": f_crit
        }
        db["buffs"]["pet_active"] = True
        db["buffs"]["pet_data"] = pet_info
        db["shop"] = {"relics": skills, "b_atk": init_atk, "b_def": init_def, "b_hp": init_hp, "b_cp": init_cp, "creds": 0, "pity": 0}
        
        ph = st.empty()
        flash_color = "#00f3ff" if rarity=="SP" else ("#ffaa00" if rarity=="UR" else ("#fcee0a" if rarity=="SSR" else "#a855f7"))
        ph.markdown(f"<div style='height:60vh; display:flex; justify-content:center; align-items:center;'><div class='tcg-card pack-opening' style='max-width:340px; aspect-ratio:63/88; box-shadow:0 0 150px {flash_color}; border:4px solid {flash_color}; background:#fff;'><div style='color:#000; font-family:Orbitron; font-size:30px; font-weight:900; line-height:2; text-align:center;'><br>✦ PULLING DECK ✦<br><span style='font-size:60px;'>✨</span></div></div></div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        update_computed_stats(st.session_state["db"])
        db["pve"]["curr_hp"] = st.session_state["db"]["computed"]["hp"]
        db["booted"] = True
        st.rerun()

# ==============================================================================
# 🌟 [ TCG DASHBOARD ] 工业级大一统死循环大厅
# ==============================================================================
else:
    # 强制全量计算，确保所有的 Buff、装备属性立刻体现在最高战力上！
    update_computed_stats(st.session_state["db"]) 
    db = st.session_state["db"]
    base, comp, shop, buffs, cb, ach, pet = db.get("player",{}), db.get("computed",{}), db.get("shop",{}), db.get("buffs",{}), db.get("combat",{}), db.get("achieve",{}), db.get("buffs",{}).get("pet_data",{})
    
    fin_atk, fin_def, fin_hp, fin_cp, fin_crit = comp.get("atk",0), comp.get("def",0), comp.get("hp",0), comp.get("cp",0), comp.get("crit",0)
    player_name, hash_id, entropy = base.get('name', 'P1'), base.get('hash', '0000'), base.get('entropy', 0)
    
    # 防止血量溢出
    if db.get("pve",{}).get("curr_hp",0) > fin_hp or (db.get("pve",{}).get("curr_hp",0) == 0 and db.get("pve",{}).get("idx",0) == 0): 
        db["pve"]["curr_hp"] = fin_hp
    
    dm_key = base.get('day_master', '甲')
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    dm_class, dm_color, dm_desc, dm_wpn, dm_skill, dm_mbti = dm_info["class_name"], dm_info["color"], dm_info["desc"], dm_info["weapon"], dm_info["skill"], dm_info["mbti"]

    bz = base.get('bazi_arr', ['?', '?', '?', '?'])
    rarity, r_col_cls = base.get("rarity", "R"), base.get("r_col", "R")
    
    f3d, f_radar, f_trend, f_hm = gen_akashic_charts(hash_id, base.get('wx', {}), dm_color, dm_key, fin_cp)

    buff_display = f"<div style='background:rgba(168,85,247,0.2); color:var(--sr); padding:4px 8px; border-radius:2px; font-family:Orbitron; border:1px solid var(--sr); margin-bottom:4px;'>🐾 伴生灵宠: {pet.get('name', '')}</div>"
    if buffs.get("oracle_drawn", False): buff_display += f"<div style='background:rgba(255,170,0,0.2); color:var(--sp); padding:4px 8px; border-radius:2px; font-family:Orbitron; border:1px solid var(--sp); margin-bottom:4px;'>⚡ 命运神谕: {buffs.get('oracle_data',{}).get('name', '')}</div>"
    if buffs.get("syn_linked", False): buff_display += f"<div style='background:rgba(0,243,255,0.2); color:var(--primary); padding:4px 8px; border-radius:2px; font-family:Orbitron; border:1px solid var(--primary); margin-bottom:4px;'>💞 道侣羁绊: {buffs.get('syn_data',{}).get('name', '')}</div>"
    if len(shop.get("relics", [])) >= 5: buff_display += f"<div style='background:rgba(16,185,129,0.2); color:var(--green); padding:4px 8px; border-radius:2px; font-family:Orbitron; border:1px solid var(--green); margin-bottom:4px;'>🎁 装备套装: 全属性加成</div>"

    HEADER_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>DATA-LIFE RPG: V1000.5 <b class="up">▲SYNCED</b></span>
        <span>PLAYER: {player_name} <b class="up">▲ACTIVE</b></span>
        <span>CYBER_MERITS: {shop.get('creds', 0)} <b class="ur">★ LOADED</b></span>
        <span>PVP_RANK: {db.get('pvp',{}).get('tier', 'Unranked')} </span>
    </div></div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid {dm_color}; padding-bottom:15px; margin-bottom:30px;">
        <div>
            <div style="font-family:'Fira Code'; color:#aaa; font-size:12px; margin-bottom:5px; font-weight:bold;">[ WALLET: 0x{hash_id[:12]} | <span style="color:var(--sp);">MERITS: {shop.get('creds', 0):,}</span> ]</div>
            <div style="font-size:clamp(28px, 5vw, 40px); font-weight:900; color:#fff; font-family:'Orbitron'; line-height:1; margin-bottom:8px;">
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

    c_left, c_right = st.columns([1, 1.8], gap="large")

    with c_left:
        # 显示战力增幅的特效
        atk_bonus = fin_atk - base.get("atk", 0)
        hp_bonus = fin_hp - base.get("hp", 0)
        def_bonus = fin_def - base.get("def", 0)
        atk_str = f"{fin_atk:,}" + (f" <span class='stat-bonus'>(+{atk_bonus:,})</span>" if atk_bonus>0 else "")
        hp_str = f"{fin_hp:,}" + (f" <span class='stat-bonus'>(+{hp_bonus:,})</span>" if hp_bonus>0 else "")
        def_str = f"{fin_def:,}" + (f" <span class='stat-bonus'>(+{def_bonus:,})</span>" if def_bonus>0 else "")

        holo_fx = "holo-ur" if rarity in ["UR", "SP"] else ""
        TCG_CARD_HTML = f"""
        <div class="tcg-card-container">
            <div class="tcg-card rarity-{r_col_cls} {holo_fx}" style="color:{dm_color};">
                <div class="tcg-badge">{rarity}</div>
                <div class="card-header">
                    <div>
                        <div class="card-title">{dm_key}</div>
                        <div style="font-family:'Noto Sans SC'; font-size:12px; font-weight:bold; color:var(--sp); margin-top:4px;">{pet.get('icon', '')} {pet.get('name', '')}</div>
                    </div>
                    <div class="card-class">{dm_mbti}</div>
                </div>
                <div class="card-art-box"><div class="card-art-char">{dm_key}</div></div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">[ {dm_class.split('/')[0].strip()} ]</div>
                    <div style="font-size:12px; font-weight:bold; color:var(--sp);">⚔️ {dm_wpn.split('】')[-1].strip() if '】' in dm_wpn else dm_wpn}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:4px; margin-bottom:10px; border:1px solid rgba(255,255,255,0.1); min-height:55px;">
                    <div style="color:var(--sp); margin-bottom:6px; font-size:10px; font-weight:bold; font-family:Orbitron;">[⚡ 全局联动乘区监控]</div>
                    <div style="line-height:1.6;">{buff_display}</div>
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
        
        # 🚨 [核心视觉重构] 战力联动核算大盘
        f_atk_m = 1.1 if "荒坂" in base.get("faction", "") else 1.0
        eq_c = len(shop.get("relics", []))
        set_mul = 1.5 if eq_c >= 20 else (1.2 if eq_c >= 10 else (1.1 if eq_c >= 5 else 1.0))
        
        calc_html = f"""
        <div class="synergy-core-box">
            <div class="synergy-core-title"><span>>> BATTLE SYNERGY CORE</span><span>万物联动核算矩阵</span></div>
            <div class="synergy-row"><span>> 出厂基底 + 黑市装备总和:</span> <span class="val">{base.get('atk',0) + shop.get('b_atk',0):,} ATK</span></div>
            <div class="synergy-row"><span>> 阵营契约 & 装备套装共鸣:</span> <span class="mul">x {f_atk_m * set_mul:.2f}</span></div>
            <div class="synergy-row"><span>> 伴生机械灵宠 ({pet.get('name', '无')}):</span> <span class="mul">x {pet.get('atk_mul', 1.0):.2f}</span></div>
            <div class="synergy-row"><span>> 赛博命运神谕 ({buffs.get('oracle_data',{{}}).get('name','')}):</span> <span class="mul">x {buffs.get('oracle_data',{{}}).get('atk_mul', 1.0):.2f}</span></div>
            <div class="synergy-row"><span>> 灵魂合盘道侣 ({buffs.get('syn_data',{{}}).get('name','')}):</span> <span class="mul" style="color:var(--sp);">x {buffs.get('syn_data',{{}}).get('atk_mul', 1.0):.2f}</span></div>
            <div class="synergy-row"><span>> 荣耀称号加成 ({ach.get('equipped',{{}}).get('name','')}):</span> <span class="mul" style="color:var(--green);">x {ach.get('equipped',{{}}).get('mul',1.0):.2f}</span></div>
            <div class="synergy-total"><span>> 实战爆杀最终攻击力:</span> <span style="font-size:24px;">{fin_atk:,}</span></div>
        </div>
        """
        render_html(calc_html)

    with c_right:
        # 🗄️ 工业级战术大厅 8 大 Tabs 满血集结
        t_deck, t_oracle, t_syn, t_raid, t_shop, t_pvp, t_map, t_export = st.tabs(["🎴 战术手牌", "☯️ 命运神谕", "💞 灵魂契约", "⚔️ 矩阵深潜", "🛒 黑市炼金", "🏆 竞技天梯", "🌌 数据大盘", "💼 资产导出"])

        with t_deck:
            @st_fragment
            def render_deck():
                _db = st.session_state["db"]
                _bz = _db.get("player", {}).get("bazi_arr", ["?","?","?","?"])
                _dm_color = DAY_MASTER_DICT.get(_db.get("player", {}).get("day_master", "甲"), DAY_MASTER_DICT["甲"])["color"]
                
                render_html("<div style='font-size:13px; color:#aaa; margin-bottom:10px;'>> 基础手牌由四柱源码构成。<b>点击下方按钮可抽出检视对应的 PVE 技能：</b></div>")
                hand_html = '<div class="hand-container">'
                labels = ["OS_YEAR", "ENV_MONTH", "CORE_DAY", "THD_TIME"]
                for i in range(4):
                    is_core = (i == 2)
                    c_cls = "hc-core" if is_core else ""
                    c_col = _dm_color if is_core else "#aaa"
                    hand_html += f"""<div class="hand-card {c_cls}" style="color:{c_col};"><div class="hc-val">{_bz[i][0]}</div><div class="hc-sub">{_bz[i][1]}</div><div class="hc-tag">{labels[i]}</div></div>"""
                hand_html += '</div>'
                render_html(hand_html)
                
                # 🚨 真实的抽出检视系统，包含详细的赛博命运解析
                c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
                with c_btn1:
                    st.markdown('<div class="inspect-btn">', unsafe_allow_html=True)
                    if st.button(f"🔍 抽出检视\n【年柱: {_bz[0]}】", use_container_width=True): _db["inspect_idx"] = 0; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_btn2:
                    st.markdown('<div class="inspect-btn">', unsafe_allow_html=True)
                    if st.button(f"🔍 抽出检视\n【月柱: {_bz[1]}】", use_container_width=True): _db["inspect_idx"] = 1; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_btn3:
                    st.markdown('<div class="inspect-btn">', unsafe_allow_html=True)
                    if st.button(f"🔍 抽出检视\n【日柱: {_bz[2]}】", use_container_width=True): _db["inspect_idx"] = 2; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_btn4:
                    st.markdown('<div class="inspect-btn">', unsafe_allow_html=True)
                    if st.button(f"🔍 抽出检视\n【时柱: {_bz[3]}】", use_container_width=True): _db["inspect_idx"] = 3; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                if _db.get("inspect_idx") is not None:
                    idx = _db["inspect_idx"]
                    skill_names = ["🗡️ 普通攻击 (Basic Attack)", "🛡️ 绝对防御 (Absolute Defense)", "💉 算力虹吸 (Data Leech)", "💥 终极神权 (Ultimate Override)"]
                    skill_desc = ["基础物理攻击指令。伤害基于最终 ATK 和暴击率。无冷却时间，最稳定的输出手段。", "3回合CD。开启后极大强化当前装甲抵挡巨量伤害，化身钢铁壁垒，抵御致命一击。", "4回合CD。造成高额伤害，并按比例回复自身生命值，绝境翻盘利器。", "5回合CD。无视大部分防御，造成 3.5 倍极限降维打击！高能耗绝杀指令。"]
                    lore_desc = [
                        "【年柱：根节点 OS】代表你的早期运势 (1-15岁)。决定初始资源池。",
                        "【月柱：环境变量 ENV】代表你的职场竞争模式 (16-30岁)。",
                        "【日柱：核心处理器 CORE】你的本命元神所在！决定核心算法逻辑。",
                        "【时柱：外设端口 I/O】代表创造力分支与衍生结局 (46岁以后)。"
                    ]
                    
                    render_html(f"""
                    <div style="display:flex; justify-content:center; padding: 20px 0;">
                        <div class="inspect-reveal" style="border: 2px solid var(--primary); box-shadow: 0 0 40px rgba(0,243,255,0.4); background: linear-gradient(180deg, #0a0c10 0%, #1a1a2e 100%); width:100%; max-width:400px; border-radius:16px; padding:25px; text-align:center; position:relative; overflow:hidden; animation: float-inspect 3s ease-in-out infinite;">
                            <div style="position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%); pointer-events:none;"></div>
                            <div style="font-family:Orbitron; color:var(--primary); font-weight:bold; margin-bottom:15px; letter-spacing:3px; font-size:12px;">[ EXAMINING DATA_NODE ]</div>
                            <div style="font-size:60px; font-weight:900; color:#fff; margin-bottom:5px; text-shadow:0 0 20px #fff; line-height:1;">{_bz[idx]}</div>
                            <div style="font-size:14px; font-family:Orbitron; color:var(--primary); margin-bottom:20px; font-weight:bold; letter-spacing:2px;">{labels[idx]}</div>
                            
                            <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:8px; border:1px solid rgba(0,243,255,0.3); margin-bottom:20px;">
                                <div style="color:var(--sp); font-weight:900; font-size:16px; margin-bottom:8px; font-family:'Noto Sans SC';">{skill_names[idx]}</div>
                                <div style="color:#ddd; font-size:12px; line-height:1.6;">{skill_desc[idx]}</div>
                            </div>
                            
                            <div style="text-align:left; background:rgba(16,185,129,0.1); border-left:3px solid var(--green); padding:12px; border-radius:0 8px 8px 0;">
                                <div style="color:var(--green); font-size:11px; font-family:Orbitron; font-weight:bold; margin-bottom:5px;">> FATE_DECODE //</div>
                                <div style="color:#aaa; font-size:12px; line-height:1.5;">{lore_desc[idx]}</div>
                            </div>
                        </div>
                    </div>
                    """)

                render_html("<hr style='border-color:#333;'>")
                
                # Lore 满血呈现
                _dm_i = DAY_MASTER_DICT.get(_db.get("player", {}).get("day_master", "甲"), DAY_MASTER_DICT["甲"])
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    render_html(f"""
                    <div class="glass-panel" style="padding:15px; border-left-color:{_dm_i['color']}; height:210px;">
                        <div style="background:rgba(0,0,0,0.6); padding:10px; border:1px solid #333; font-family:'Fira Code'; font-size:12px; margin-bottom:10px;">
                            <div style="color:{_dm_i['color']}; margin-bottom:5px; font-weight:bold;">[ EVOLUTION TREE ] 觉醒树</div>
                            <div style="color:#aaa;">{_dm_i.get("evo_path", "")}</div>
                            <div style="color:#fff; font-weight:bold; margin-top:5px;">终极神权: {_dm_i.get("ult_evo", "")}</div>
                        </div>
                        <div style="background:rgba(244,63,94,0.1); border-left:3px solid var(--pink); padding:10px; font-family:'Fira Code'; font-size:12px;">
                            <div style="color:var(--pink); font-weight:bold; margin-bottom:4px;">[ FATAL VULNERABILITY ] 致命漏洞</div>
                            <div style="color:#ddd; margin-bottom:5px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{_dm_i.get("flaw", "")}</div>
                            <div style="color:var(--green);">> SYS_HOTFIX: {_dm_i.get("patch", "")}</div>
                        </div>
                    </div>
                    """)
                with c_d2:
                    p_life = _db.get("player", {}).get('past_life',{})
                    render_html(f"""
                    <div class="glass-panel" style="padding:15px; border-left-color:var(--yellow); height:210px; overflow-y:auto;">
                        <div style="font-size:11px; color:var(--yellow); font-family:'Orbitron'; margin-bottom:5px; font-weight:bold;">>> KARMIC LORE (前世业力残存)</div>
                        <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:4px;">{p_life.get('title','未知')}</div>
                        <div style="color:#aaa; font-size:11px; line-height:1.5;">{p_life.get('debt','无')}</div>
                    </div>
                    """)
            render_deck()

        with t_oracle:
            c_o1, c_o2 = st.columns([1.1, 1], gap="large")
            with c_o1:
                render_html("<div style='color:var(--sp); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ CYBER ORACLE ] 每日量子神谕</div>")
                render_html("<div style='font-size:12px; color:#aaa; margin-bottom:15px;'>每天免费抽取一次。抽到的神谕将作为乘区<b>直接让你的实战面板暴涨！</b>打怪前必抽！</div>")
                
                @st_fragment
                def render_oracle():
                    _db = st.session_state["db"]
                    _buffs = _db.get("buffs", {})
                    if not _buffs.get("oracle_drawn", False):
                        render_html("""<div class="glass-panel" style="text-align:center; padding:50px 20px; border-color:var(--sp); border-style:dashed;"><div style="font-size:45px; margin-bottom:15px; animation:blink 2s infinite;">📦</div><div style="color:var(--sp); font-family:'Orbitron'; font-size:16px; font-weight:900; letter-spacing:2px; margin-bottom:10px;">DAILY HEXAGRAM SEALED</div><div style="color:#aaa; font-size:12px;">盲盒处于叠加态。点击下方按钮坍缩今日命运乘区。</div></div>""")
                        if st.button("⚡ 注入算力，抽取今日神谕 (PVE BUFF)", use_container_width=True):
                            spell_card, _ = pull_daily_spell(hash_id)
                            _buffs["oracle_drawn"] = True
                            _buffs["oracle_data"] = {"name": spell_card["name"], "atk_mul": spell_card.get("buff_atk", 1.0), "def_mul": spell_card.get("buff_def", 1.0), "hp_mul": spell_card.get("buff_hp", 1.0), "desc": spell_card["desc"], "card": spell_card}
                            st.toast("⚡ 获得神谕加持！左侧属性已暴涨！", icon="🔮")
                            st.rerun() 
                    else:
                        sc = _buffs.get("oracle_data", {}).get("card", {})
                        if not sc: return
                        sc_c = sc.get("color", "#fff")
                        today_str = datetime.now().strftime("%Y-%m-%d")
                        yao_html = "".join([f"<div class='yao-yang' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div>" if line == 1 else f"<div class='yao-yin'><div class='half' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div><div class='half' style='background:{sc_c}; box-shadow:0 0 10px {sc_c};'></div></div>" for line in reversed(sc.get('lines', []))])
                        render_html(f"""
                        <div class="flip-card card-reveal" style="max-width:280px; margin:0 auto;">
                          <div class="flip-card-inner">
                            <div class="flip-card-front" style="border-color:{sc_c}; box-shadow:0 0 40px {sc_c}66; background:linear-gradient(0deg, rgba(0,0,0,0.95), {sc_c}22); padding:15px;">
                                <div style="font-family:'Orbitron'; color:{sc_c}; font-size:10px; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">[ DATE: {today_str} ]</div>
                                <div style="background:{sc_c}; color:#000; display:inline-block; padding:2px 10px; font-family:'Orbitron'; font-weight:900; font-size:12px; border-radius:2px; margin-bottom:10px;">{sc.get('type','')}</div>
                                <div class="hex-container" style="margin-bottom:15px;">{yao_html}</div>
                                <div style="font-size:20px; font-weight:900; color:#fff; font-family:'Noto Sans SC'; margin-bottom:15px; text-shadow:0 0 10px {sc_c};">{sc.get('name','')}</div>
                                <div style="font-size:10px; font-family:Orbitron; color:#888;">HOVER TO REVEAL DETAILS</div>
                            </div>
                            <div class="flip-card-back" style="border-color:{sc_c}; background:#050810; padding:15px; display:flex; flex-direction:column; justify-content:center;">
                                <div style="background:rgba(0,0,0,0.6); padding:10px; border-radius:4px; text-align:left; border:1px solid rgba(255,255,255,0.1); font-size:11px; line-height:1.5; color:#ddd; margin-bottom:10px;">
                                    <b style="color:{sc_c}; font-family:'Fira Code';">> PVE BUFF 乘区:</b><br>{sc.get('desc','')}
                                </div>
                            </div>
                          </div>
                        </div>
                        """)
                render_oracle()
                
            with c_o2:
                render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ ACTION ROLL ] D100 暗骰检定</div>")
                @st_fragment
                def render_dice():
                    _db = st.session_state["db"]
                    ph = st.empty()
                    with st.form(key="dice_form", clear_on_submit=False, border=False):
                        q_input = st.text_input("📝 输入检定事件：", placeholder="e.g. 梭哈买这只股票能赚吗？", label_visibility="collapsed")
                        sub_q = st.form_submit_button("🎲 算力暗骰检定 (ROLL D100)", use_container_width=True)
                    if sub_q:
                        if not q_input: ph.warning("⚠️ 语法错误：事件为空！")
                        else:
                            prob, hex_res, conc, q_c = roll_d100(q_input, _db.get("player",{}).get("hash", "00"))
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
                render_html("<div style='color:var(--pink); font-family:Orbitron; font-size:14px; font-weight:900; margin-top:10px; margin-bottom:15px;'>[ NEURAL LINK ] 灵魂合盘与契约</div>")
                render_html("<div style='font-size:13px; color:#aaa; margin-bottom:15px; line-height:1.6;'>测算双排组合的【姻缘共鸣度】，签订契约后可<b style='color:var(--sp);'>为主将卡提供最高 +45% 的全局面板乘区！</b></div>")
                @st_fragment
                def render_sync():
                    _db = st.session_state["db"]
                    with st.form(key="sync_form", clear_on_submit=False, border=False):
                        opts = list(DAY_MASTER_DICT.keys())
                        t_node = st.selectbox("🎯 寻找助战对象【日干】:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('tier', 'N')}] {x}")
                        if st.form_submit_button("💞 测算同步率", use_container_width=True):
                            sc, sd, sc_color, sc_icon, a_mul = calc_tag_team(hash_id, t_node)
                            st.session_state["cur_sync"] = {"score": sc, "mul": a_mul, "node": t_node, "color": sc_color, "sd": sd, "icon": sc_icon}
                            st.rerun()
                    if "cur_sync" in st.session_state:
                        sync = st.session_state["cur_sync"]
                        
                        # 🚨 终极安全语法：使用三引号彻底杜绝 SyntaxError！
                        render_html(f"""
                        <div class='glass-panel card-reveal' style='border-left:4px solid {sync['color']}; text-align:center; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);'>
                            <div style='font-family:Orbitron; font-size:12px; color:#888; margin-bottom:5px;'>SYNC RATE</div>
                            <div class='heart-pulse' style='font-size:40px; color:{sync['color']};'>{sync['icon']}</div>
                            <div style='font-size:45px; color:{sync['color']}; font-weight:900; margin-bottom:5px;'>{sync['score']}%</div>
                            <div style='color:#fff; font-size:12px;'>{sync['sd']}</div>
                        </div>
                        """)
                        
                        if sync['score'] >= 60:
                            if st.button("🤝 签订契约 (拉入助战)", use_container_width=True):
                                _db["buffs"]["syn_linked"] = True
                                _db["buffs"]["syn_data"] = {"name": f"{sync['node']}系道侣", "atk_mul": sync['mul'], "def_mul": sync['mul'], "hp_mul": sync['mul'], "cp_bonus": sync['score']*200}
                                st.toast("💞 契约结成！全属性飙升！", icon="😍")
                                st.rerun()
                render_sync()

        with t_raid:
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:15px;'>数据人生是一场爬塔。<b>请亲自打出你的八字手牌（普攻/护盾/吸血/大招）来击杀心魔，赚取海量功德！</b></div>")
            @st_fragment
            def render_raid():
                _db = st.session_state["db"] 
                rs = _db.get("pve", {})
                _cb = _db.get("combat", {})
                
                # 🚨 安全获取实战数据
                _fin_atk, _fin_def, _fin_hp, _fin_cp, _fin_crit = get_final_combat_stats(_db)
                
                if rs.get("idx", 0) >= len(BOSS_ROSTER):
                    boss_info = {"lvl": rs.get("idx",0)+1, "name": f"深渊魔影 层数 {rs.get('idx',0)-4}", "max_hp": int(1500000 * math.pow(1.5, rs.get("idx",0) - 4)), "atk": int(80000 * math.pow(1.2, rs.get("idx",0) - 4)), "reward": int(50000 * math.pow(1.1, rs.get("idx",0) - 4)), "desc": "阿卡夏深渊的无尽梦魇。"}
                else: boss_info = BOSS_ROSTER[rs.get("idx", 0)]
                
                if rs.get("boss_max", 0) != boss_info["max_hp"]: rs["boss_max"] = boss_info["max_hp"]; rs["boss_hp"] = boss_info["max_hp"]
                boss_hp_pct = max(0, min(100, int((rs.get("boss_hp",0) / rs.get("boss_max",1)) * 100)))
                my_hp, my_hp_pct = rs.get("curr_hp",0), max(0, min(100, int((rs.get("curr_hp",0) / max(1, _fin_hp)) * 100)))
                
                c_pve1, c_pve2 = st.columns([1.2, 1.5], gap="large")
                with c_pve1:
                    render_html(f"""
                    <div class="glass-panel" style="text-align:center; border-color:var(--pink); padding:15px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-family:Orbitron; font-weight:bold; font-size:12px;">
                            <span style="color:var(--pink);">MATRIX_ICE</span> <span style="color:#fff;">VS</span> <span style="color:var(--primary);">PLAYER</span>
                        </div>
                        <div style="font-size:45px; margin-bottom:5px; text-shadow:0 0 20px var(--pink); animation:blink 2s infinite;">👾</div>
                        <div style="color:var(--pink); font-family:'Orbitron'; font-weight:900; font-size:15px;">{boss_info["name"]}</div>
                        <div style="color:#aaa; font-size:11px; margin-bottom:10px;">[ {boss_info["desc"]} ]</div>
                        <div class="hp-bar-bg" style="margin-top:10px;"><div class="hp-bar-fill hp-red" style="width:{boss_hp_pct}%;"></div></div>
                        <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold; margin-bottom:5px;">{rs.get("boss_hp",0):,} / {rs.get("boss_max",0):,} HP</div>
                        
                        <hr style="border-color:#333; margin:10px 0;">
                        <div style="color:var(--green); font-family:'Orbitron'; font-weight:bold; font-size:12px; margin-bottom:5px;">YOUR HP (你的载体)</div>
                        <div class="hp-bar-bg"><div class="hp-bar-fill hp-green" style="width:{my_hp_pct}%;"></div></div>
                        <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">{my_hp:,} / {_fin_hp:,} HP</div>
                    </div>
                    """)
                    
                    if my_hp <= 0:
                        if st.button("💉 消耗 500 功德复活", use_container_width=True):
                            if _db.get("shop",{}).get("creds",0) >= 500:
                                _db["shop"]["creds"] -= 500; _db["pve"]["curr_hp"] = _fin_hp
                                _cb["cd_def"], _cb["cd_heal"], _cb["cd_ult"] = 0, 0, 0
                                st.rerun()
                            else: st.warning("功德不足！请去【竞技天梯】打榜或离线挖矿。")
                    elif rs.get("boss_hp",0) > 0:
                        b1, b2 = st.columns(2); b3, b4 = st.columns(2)
                        
                        def handle_victory():
                            rs["boss_hp"] = 0; _db["shop"]["creds"] += boss_info["reward"]; _db["quests"]["kills"] += 1
                            st.toast(f"🔥 爽！击杀 Boss 爆出 {boss_info['reward']:,} 金币！", icon="💰")
                            rs["logs"].append(f"<br><span style='color:var(--green); font-weight:bold;'>🏆 [VICTORY] 获得 {boss_info['reward']:,} 功德！去黑市抽装备吧！</span>")
                        
                        def enemy_counter(dmg_taken):
                            boss_dmg = int(boss_info["atk"] * random.uniform(0.9, 1.1))
                            act_dmg = max(10, int(boss_dmg - (_fin_def * 3.0))) if _cb.get("cd_def", 0) == 3 else max(100, int(boss_dmg - (_fin_def * 0.6)))
                            rs["curr_hp"] -= act_dmg
                            rs["logs"].append(f"<span style='color:var(--pink);'>🛡️ [BOSS] 反噬！受到 {act_dmg:,} 点伤害。</span>")
                            if rs["curr_hp"] <= 0: rs["curr_hp"] = 0; rs["logs"].append("<br><span style='color:var(--pink); font-weight:bold;'>💀 [DEFEAT] 主将阵亡！</span>")
                        
                        def adv_cd():
                            if _cb.get("cd_def", 0) > 0: _cb["cd_def"] -= 1
                            if _cb.get("cd_heal", 0) > 0: _cb["cd_heal"] -= 1
                            if _cb.get("cd_ult", 0) > 0: _cb["cd_ult"] -= 1

                        _bz = _db.get("player", {}).get("bazi_arr", ["?","?","?","?"])
                        with b1:
                            st.markdown('<div class="combat-btn">', unsafe_allow_html=True)
                            if st.button(f"🗡️ 普攻\n[{_bz[0]}]", use_container_width=True):
                                adv_cd()
                                dmg = int(_fin_atk * random.uniform(0.85, 1.15)) * (2 if random.randint(1,100)<=_fin_crit else 1)
                                rs["boss_hp"] -= dmg; rs["logs"].append(f"<span style='color:var(--primary);'>⚔️ 基于 {_fin_atk:,} 面板攻击造成 {dmg:,} 伤害。</span>")
                                handle_victory() if rs["boss_hp"] <= 0 else enemy_counter(dmg)
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                        with b2:
                            c_d = _cb.get("cd_def", 0); c_c = "btn-cd" if c_d > 0 else "combat-btn"
                            st.markdown(f'<div class="{c_c}">', unsafe_allow_html=True)
                            if st.button(f"🛡️ 防御(CD:{c_d})\n[{_bz[1]}]" if c_d > 0 else f"🛡️ 绝对防御\n[{_bz[1]}]", disabled=(c_d > 0), use_container_width=True):
                                adv_cd(); _cb["cd_def"] = 3; rs["logs"].append(f"<span style='color:var(--yellow);'>🛡️ 开启绝对防御！装甲 x3！</span>")
                                enemy_counter(0); st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                        with b3:
                            c_h = _cb.get("cd_heal", 0); c_c = "btn-cd" if c_h > 0 else "combat-btn"
                            st.markdown(f'<div class="{c_c}">', unsafe_allow_html=True)
                            if st.button(f"💉 虹吸(CD:{c_h})\n[{_bz[2]}]" if c_h > 0 else f"💉 算力虹吸\n[{_bz[2]}]", disabled=(c_h > 0), use_container_width=True):
                                adv_cd(); dmg = int(_fin_atk * 1.2); rs["boss_hp"] -= dmg; rs["curr_hp"] = min(_fin_hp, rs["curr_hp"] + int(dmg*0.8))
                                _cb["cd_heal"] = 4; rs["logs"].append(f"<span style='color:var(--green);'>💉 虹吸造成 {dmg:,} 伤害，回复大量HP！</span>")
                                handle_victory() if rs["boss_hp"] <= 0 else enemy_counter(dmg)
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                        with b4:
                            c_u = _cb.get("cd_ult", 0); c_c = "btn-cd" if c_u > 0 else "combat-btn"
                            st.markdown(f'<div class="{c_c}">', unsafe_allow_html=True)
                            if st.button(f"💥 神权(CD:{c_u})\n[{_bz[3]}]" if c_u > 0 else f"💥 终极神权\n[{_bz[3]}]", disabled=(c_u > 0), use_container_width=True):
                                adv_cd(); dmg = int(_fin_atk * 3.5); rs["boss_hp"] -= dmg
                                _cb["cd_ult"] = 5; rs["logs"].append(f"<span style='color:var(--sp); font-weight:bold;'>💥 释放神权大招！造成 {dmg:,} 点极限伤害！</span>")
                                handle_victory() if rs["boss_hp"] <= 0 else enemy_counter(dmg)
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        if st.button("🚀 跃迁下一层", use_container_width=True):
                            rs["idx"] += 1; rs["boss_max"] = BOSS_ROSTER[rs["idx"]]["max_hp"] if rs["idx"] < len(BOSS_ROSTER) else int(1500000 * math.pow(1.5, rs['idx']-4)) 
                            rs["boss_hp"] = rs["boss_max"]; rs["curr_hp"] = _fin_hp
                            _cb["cd_def"], _cb["cd_heal"], _cb["cd_ult"] = 0, 0, 0 
                            rs["logs"].append(f"<br><span style='color:var(--yellow);'>> 已跃迁下一层。</span>"); st.rerun()
                                    
                with c_pve2:
                    log_html = "<br><hr style='border-color:#333; margin:8px 0;'>".join(rs.get("logs", [])[-7:])
                    render_html(f"<div class='glass-panel' style='background:#000; font-family:\"Fira Code\"; font-size:11px; height:430px; display:flex; flex-direction:column-reverse; overflow-y:auto; border-left:4px solid var(--primary); padding:15px; margin-bottom:0;'><div>{log_html}<br><span style='animation:blink 1s infinite;'>_</span></div></div>")
            render_raid()

        with t_shop:
            c_sh1, c_sh2 = st.columns([1, 1], gap="large")
            with c_sh1:
                @st_fragment
                def render_10_pull():
                    _db = st.session_state["db"]
                    _shop = _db.get("shop", {})
                    pity_val = _shop.get('pity', 0)
                    render_html(f"""
                    <div class='glass-panel' style='padding:20px; border-color:var(--sp); margin-bottom:10px; text-align:center;'>
                        <div style='font-size:12px; color:#aaa; margin-bottom:5px;'>消耗功德进行抽卡，<b style="color:var(--sp);">满 50 抽必出 UR/SP 极品！抽出的属性会自动核算到左侧面板！</b></div>
                        <div style='font-size:10px; color:var(--sp); font-weight:bold; margin-bottom:10px;'>【保底进度: {pity_val}/50】</div>
                        <div style='font-size:30px; font-family:Orbitron; color:var(--sp); font-weight:bold; margin-bottom:10px; text-shadow:0 0 10px var(--sp);'>MERITS: {_shop.get('creds',0):,}</div>
                    </div>
                    """)
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button("🪙 1,000 单抽", use_container_width=True):
                            if _shop.get("creds", 0) >= 1000:
                                _shop["creds"] -= 1000; _shop["pity"] += 1
                                _db["quests"]["gacha_pulls"] += 1
                                if _shop["pity"] >= 50: pull, _shop["pity"] = random.choices([("UR", 15000, "#ff007c"), ("SP", 50000, "#ffaa00")], weights=[80, 20], k=1)[0], 0
                                else: pull = random.choices([("R", 500, "#00f3ff"), ("SR", 1500, "#a855f7"), ("SSR", 5000, "#fcee0a"), ("UR", 15000, "#ff007c"), ("SP", 50000, "#ffaa00")], weights=[60, 25, 10, 4, 1], k=1)[0]
                                r_tier, b_cp, c_col = pull
                                clean_relic = f"[{r_tier}] {random.choice(ITEM_PREFIXES)}{random.choice(ITEM_SUFFIXES)} (+{b_cp} CP)"
                                _shop["relics"].append(clean_relic); _shop["b_cp"] += b_cp; _shop["b_atk"] += int(b_cp * 0.08); _shop["b_def"] += int(b_cp * 0.05); _shop["b_hp"] += int(b_cp * 0.3)
                                st.toast(f"🎉 抽出 {r_tier} 级词条！左侧战力已瞬间飙升！", icon="🚀")
                                st.rerun() 
                            else: st.error("功德不足！去打怪爆金币！")
                    with col_b2:
                        if st.button("💎 10,000 十连抽", use_container_width=True):
                            if _shop.get("creds", 0) >= 10000:
                                _shop["creds"] -= 10000; _shop["pity"] += 10; pulls = []
                                _db["quests"]["gacha_pulls"] += 10
                                for i in range(10):
                                    if _shop["pity"] >= 50 or i == 9: tier_data, _shop["pity"] = random.choices([("SSR", 5000, "#fcee0a"), ("UR", 15000, "#ff007c"), ("SP", 50000, "#ffaa00")], weights=[80, 15, 5], k=1)[0], 0 if _shop["pity"] >= 50 else _shop["pity"]
                                    else: tier_data = random.choices([("R", 500, "#00f3ff"), ("SR", 1500, "#a855f7"), ("SSR", 5000, "#fcee0a"), ("UR", 15000, "#ff007c"), ("SP", 50000, "#ffaa00")], weights=[60, 25, 10, 4, 1], k=1)[0]
                                    clean_relic = f"[{tier_data[0]}] {random.choice(ITEM_PREFIXES)}{random.choice(ITEM_SUFFIXES)}"
                                    pulls.append((tier_data[0], clean_relic, tier_data[2]))
                                    _shop["relics"].append(f"{clean_relic} (+{tier_data[1]} CP)"); _shop["b_cp"] += tier_data[1]; _shop["b_atk"] += int(tier_data[1] * 0.08); _shop["b_def"] += int(tier_data[1] * 0.05); _shop["b_hp"] += int(tier_data[1] * 0.3)
                                st.session_state["gacha_result"] = pulls
                                st.toast("🔥 十连爆闪！海量属性已注入左侧面板！", icon="✨")
                                st.rerun()
                            else: st.error("功德不足！去打怪爆金币！")
                    if "gacha_result" in st.session_state and st.session_state["gacha_result"]:
                        grid_html = "<div class='gacha-10-grid'>" + "".join([f"<div class='gacha-item' style='border-color:{p[2]}; animation-delay:{i*0.1}s;'><div style='color:{p[2]}; font-family:Orbitron; font-weight:bold; font-size:16px;'>{p[0]}</div><div style='color:#fff; font-size:9px; margin-top:5px;'>{p[1]}</div></div>" for i, p in enumerate(st.session_state["gacha_result"])]) + "</div>"
                        render_html(f"<div class='glass-panel' style='text-align:center; padding:15px;'>{grid_html}</div>")
                        if st.button("✔ 确认收入背包"): st.session_state["gacha_result"] = []; st.rerun()
                render_10_pull()
                
            with c_sh2:
                @st_fragment
                def render_forge():
                    _db = st.session_state["db"]
                    _shop = _db.get("shop", {})
                    render_html("<div style='color:var(--ur); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ THE FORGE ] 赛博炼金炉</div>")
                    inv_count = len(_shop.get("relics", []))
                    if st.button(f"🔥 献祭 3 件旧装备熔铸高阶神器！(当前: {inv_count}/3)", use_container_width=True):
                        if inv_count >= 3:
                            _shop["relics"] = _shop["relics"][3:] 
                            r_tier, b_cp = random.choices([("SSR", 8000), ("UR", 25000), ("SP", 80000)], weights=[60, 30, 10], k=1)[0]
                            _shop["relics"].append(f"[{r_tier}] 炼狱·{random.choice(ITEM_PREFIXES)}{random.choice(ITEM_SUFFIXES)} (+{b_cp} CP)")
                            _shop["b_cp"] += b_cp; _shop["b_atk"] += int(b_cp * 0.08); _shop["b_def"] += int(b_cp * 0.05); _shop["b_hp"] += int(b_cp * 0.3)
                            _db["quests"]["merges"] += 1
                            st.toast("🎇 熔炼成功！神器出世！左侧战力已核爆！", icon="🔥")
                            st.rerun()
                        else: st.error("装备不足 3 件！")

                    render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-top:20px; margin-bottom:10px;'>[ INVENTORY ] 你的装备背囊</div>")
                    r_items = _shop.get("relics", [])
                    if not r_items: r_items = ["【空空如也，快去抽卡】"]
                    sk_html = "".join([f"<div class='relic-item' style='color:{'var(--sp)' if 'SP' in s or 'UR' in s else 'var(--primary)'};'><div style='overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{s.split(' (')[0]}</div></div>" for s in reversed(r_items[-30:])])
                    render_html(f"<div class='glass-panel' style='height:280px; overflow-y:auto; border-left-color:var(--primary);'><div class='relic-grid'>{sk_html}</div></div>")
                render_forge()

        with t_pvp:
            c_p1, c_p2 = st.columns([1, 1], gap="large")
            with c_p1:
                render_html("<div style='font-size:14px; font-weight:bold; color:var(--primary); font-family:Orbitron; margin-bottom:10px;'>[ PVP RANKED ] 幻影天梯排位赛</div>")
                @st_fragment
                def render_pvp():
                    _db = st.session_state["db"]
                    p = _db.get("pvp", {})
                    _f_cp = _db.get("computed", {}).get("cp", 0)
                    if p.get("rp", 0) >= 3000: p["tier"], r_col = "👑 璀璨神权", "var(--sp)"
                    elif p.get("rp", 0) >= 2000: p["tier"], r_col = "💎 阿卡夏钻石", "#00f3ff"
                    elif p.get("rp", 0) >= 1500: p["tier"], r_col = "🥇 矩阵黄金", "#fcee0a"
                    else: p["tier"], r_col = "🔰 废土黑铁", "#888"
                    
                    render_html(f"<div class='glass-panel' style='text-align:center; border-color:{r_col}; padding:20px;'><div style='font-size:24px; font-weight:bold; color:{r_col}; margin-bottom:10px; text-shadow:0 0 15px {r_col};'>{p.get('tier', '')}</div><div style='font-size:50px; font-weight:900; color:#fff; font-family:Orbitron; line-height:1; margin-bottom:10px;'>{p.get('rp', 0)}</div></div>")
                    if st.button("⚔️ 匹配镜像对手", use_container_width=True):
                        opp_cp = int(_f_cp * random.uniform(0.85, 1.3)); my_score, opp_score = _f_cp * random.randint(1,100), opp_cp * random.randint(1,100)
                        log = f"<div style='color:#fff;'>> [MATCH] Opponent CP: {opp_cp:,}<br>"
                        if my_score >= opp_score:
                            gain = random.randint(15, 30); p["rp"] += gain; p["wins"] += 1; _db["shop"]["creds"] += 1500; log += f"<span style='color:var(--green); font-weight:bold;'>🏆 [WIN] RP +{gain}</span></div>"
                        else:
                            loss = random.randint(10, 20); p["rp"] = max(0, p["rp"] - loss); log += f"<span style='color:var(--pink); font-weight:bold;'>💀 [LOSE] RP -{loss}</span></div>"
                        p["logs"].append(log); st.rerun()
                    
                    log_html = "<br><hr style='border-color:#333; margin:8px 0;'>".join(p.get("logs", [])[-3:])
                    render_html(f"<div class='glass-panel' style='background:#000; font-family:\"Fira Code\"; font-size:12px; height:180px; display:flex; flex-direction:column-reverse; overflow-y:auto; border-left:4px solid {r_col}; padding:15px; margin-top:10px;'><div>{log_html}</div></div>")
                render_pvp()
            with c_p2:
                render_html("<div style='font-size:14px; font-weight:bold; color:var(--sp); font-family:Orbitron; margin-bottom:10px;'>[ WORLD BOSS ] 阿卡夏吞噬者</div>")
                @st_fragment
                def render_wb():
                    _db = st.session_state["db"]
                    wb = _db.get("world_boss", {})
                    _f_atk, _f_crit = _db.get("computed", {}).get("atk", 0), _db.get("computed", {}).get("crit", 0)
                    
                    render_html(f"<div class='glass-panel' style='text-align:center; border-color:var(--sp); padding:20px;'><div style='font-size:50px; text-shadow:0 0 20px var(--sp); margin-bottom:10px;'>👹</div><div style='color:var(--sp); font-family:Orbitron; font-weight:900;'>3 回合极限输出挑战</div><div style='font-family:Orbitron; color:#fff; font-size:20px; margin-top:15px;'>HIGHEST DMG: <br><span style='color:var(--sp); font-size:30px;'>{wb.get('highest_dmg', 0):,}</span></div></div>")
                    if st.button("🔥 发起世界挑战", use_container_width=True):
                        total_dmg = sum([int(_f_atk * random.uniform(0.8, 1.5) * (2.5 if random.randint(1,100)<=_f_crit else 1)) for _ in range(3)])
                        if total_dmg > wb.get('highest_dmg', 0):
                            wb['highest_dmg'] = total_dmg; reward = int(total_dmg // 10); wb["logs"].append(f"<span style='color:var(--green); font-weight:bold;'>🎉 破纪录 {total_dmg:,}！获得 {reward:,} 功德！</span>"); _db["shop"]["creds"] += reward
                        else:
                            reward = int(total_dmg // 20); wb["logs"].append(f"<span style='color:#aaa;'>伤害 {total_dmg:,}。获得参与奖 {reward:,} 功德。</span>"); _db["shop"]["creds"] += reward
                        st.rerun()
                    if wb.get("logs", []): render_html(f"<div class='glass-panel' style='background:#000; font-family:Fira Code; font-size:12px; border-left:4px solid var(--sp); padding:15px; height:100px; overflow-y:auto; margin-top:10px;'>{wb['logs'][-1]}</div>")
                render_wb()
                
                @st_fragment
                def render_mine():
                    _db = st.session_state["db"]
                    ms = _db.get("mining", {"last_time": time.time(), "total": 0})
                    elapsed = time.time() - ms.get("last_time", time.time())
                    earned = int((_db.get("computed", {}).get("cp", 0) / 1000) * (elapsed / 60) * 20) 
                    render_html(f"<div class='glass-panel' style='text-align:center; border-color:var(--primary); padding:15px; margin-top:10px;'><div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900;'>[ IDLE MINING ] 离线挖矿收益</div><div style='font-family:Orbitron; font-size:25px; color:var(--sp); font-weight:bold; margin-top:5px;'>{earned:,}</div></div>")
                    if st.button("📥 提取挖矿收益", use_container_width=True):
                        if earned > 0:
                            _db["shop"]["creds"] += earned; ms["total"] += earned; ms["last_time"] = time.time()
                            st.toast(f"⛏️ 收菜成功！获得 {earned} 功德！", icon="💰")
                            st.rerun()
                render_mine()

        with t_map:
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
                # 🚨 终极安全提取：必须在 Fragment 内重新取所有局部变量以防 NameError 报错！
                local_db = st.session_state["db"]
                local_base = local_db.get("player", {})
                local_shop = local_db.get("shop", {})
                local_comp = local_db.get("computed", {})
                
                _pname = local_base.get('name', 'P1')
                _hash = local_base.get('hash', '0000')
                _dm_key = local_base.get('day_master', '甲')
                _rarity = local_base.get("rarity", "R")
                _bz = local_base.get('bazi_arr', ['?','?','?','?'])
                _wx = local_base.get('wx', {})
                
                # 专门修复 past_life 的 NameError (强制提取，容错拉满)
                _past_life = local_base.get('past_life', {})
                _pl_title = _past_life.get('title', '【前世信息丢失】')
                _pl_debt = _past_life.get('debt', '无')
                
                _f_atk, _f_def, _f_hp, _f_cp = local_comp.get("atk",0), local_comp.get("def",0), local_comp.get("hp",0), local_comp.get("cp",0)
                
                _dm_info = DAY_MASTER_DICT.get(_dm_key, DAY_MASTER_DICT["甲"])
                _dm_class = _dm_info.get("class_name", "Unknown").split('/')[0].strip()
                _dm_color = _dm_info.get("color", "#fff")
                _dm_wpn = _dm_info.get("weapon", "无").split('】')[-1].strip() if '】' in _dm_info.get("weapon", "") else _dm_info.get("weapon", "")
                
                render_html(f"<div style='text-align:center; color:#888; font-size:13px; margin-top:10px; margin-bottom:15px;'>资产分发中心。可压制实体卡砖或提取底层数据。© {COPYRIGHT}</div>")
                e_psa, e_web3, e_txt, e_json, e_asc = st.tabs(["📸 PSA 10 实体卡砖", "💻 智能合约铸造", "📜 万字机密档案", "💾 JSON 底包", "📟 ASCII 卡片"])
                
                with e_psa:
                    c_e1, c_e2, c_e3 = st.columns([1, 2, 1])
                    with c_e2:
                        if st.button("📸 压制 PSA 10 典藏卡砖 (MINT SLAB)", use_container_width=True):
                            clean_sk = [s.split(' (')[0].split('】')[-1].strip() if '】' in s else s for s in local_shop.get("relics", [])]
                            if not clean_sk: clean_sk = ["白板体质"]
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
                                    <div class="psa-r"><div style="font-size:9px; font-weight:bold; margin-bottom:4px;">GEM MINT</div><div class="psa-grade">10</div></div>
                                </div>
                                <div class="card-inner">
                                    <div class="c-head"><div class="h1">__DM_KEY__ · __CLASS__</div><div style="font-family:'Orbitron'; font-size:18px; font-weight:900; background:__COLOR__; color:#000; padding:2px 8px; border-radius:2px;">__TIER__</div></div>
                                    <div class="art-box"><div class="art-char">__DM_KEY__</div></div>
                                    <div class="cp-text">CP __CP__</div>
                                    <div class="desc-box"><div style="color:__COLOR__; font-weight:bold; margin-bottom:4px;">⚔️ __WPN__</div></div>
                                    <div style="text-align:center; margin-bottom:10px;">__EQUIPS__</div>
                                    <div style="display:flex; justify-content:space-between; font-family:'Orbitron'; font-size:14px; font-weight:bold; color:#fff; border-top:1px solid #333; padding-top:8px;"><span style="color:#f43f5e;">ATK: __ATK__</span><span style="color:#10b981;">HP: __HP__</span></div>
                                    <div style="text-align:right; font-family:'Orbitron'; font-size:8px; color:#666; margin-top:10px;">© 2026 __CPY__</div>
                                </div>
                            </div></div>
                            <div id="ui-loading">>>> ENCAPSULATING SLAB...</div>
                            <img id="final-img" />
                            <script>
                                setTimeout(() => { html2canvas(document.getElementById('slab'), { scale:2, backgroundColor:'transparent', logging:false }).then(canvas => { document.getElementById('final-img').src = canvas.toDataURL('image/png'); document.getElementById('ui-loading').style.display = 'none'; document.getElementById('final-img').style.display = 'block'; document.getElementById('hide-box').innerHTML = ''; }); }, 500);
                            </script>
                            </body></html>
                            """
                            html_ready = HTML_POSTER_RAW.replace("__COLOR__", _dm_color).replace("__PLAYER__", _pname.upper())
                            html_ready = html_ready.replace("__HASH__", _hash[:10]).replace("__DM_KEY__", _dm_key).replace("__CLASS__", _dm_class)
                            html_ready = html_ready.replace("__TIER__", _rarity).replace("__CP__", f"{_f_cp:,}").replace("__WPN__", _dm_wpn)
                            html_ready = html_ready.replace("__EQUIPS__", sk_h).replace("__ATK__", f"{_f_atk:,}").replace("__HP__", f"{_f_hp:,}").replace("__CPY__", COPYRIGHT.upper())
                            components.html(html_ready, height=750) 
                
                with e_web3:
                    contract_code = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@tcg-matrix/contracts/token/ERC721.sol";

contract Karma_TCG_V1000 is ERC721 {{
    // > MINT_TARGET : {_pname}
    // > CARD_RARITY : {_rarity} (CP: {_f_cp})
    // > HASH_ID     : 0x{_hash}
    
    function mintCommanderCard() public {{
        uint256 tokenId = uint256(keccak256(abi.encodePacked("{_hash}")));
        _mint(msg.sender, tokenId);
    }}
}}"""
                    st.code(contract_code, language="solidity")

                with e_txt:
                    TXT_LORE = f"""======================================
[ {VERSION} ] 绝密卡组档案 
======================================
>> 1. 玩家档案 (PLAYER DATA)
▸ 身份：{_pname} 
▸ 哈希：0x{_hash}
▸ 天梯段位：{local_db.get('pvp',{}).get('tier', 'Unranked')}
▸ 最终战力：{_f_cp:,} CP [{_rarity}]

>> 2. 主将设定 (COMMANDER LORE)
▸ 代号：{_dm_key}
▸ 最终实战面板：ATK {_f_atk:,} | HP {_f_hp:,}

>> 3. 业力与武装 (KARMA & EQUIPS)
▸ 前世残存：{_pl_title} ({_pl_debt})
▸ 挂载装备库：{', '.join(local_shop.get("relics", []))}
======================================
© 2026 {COPYRIGHT}. ALL RIGHTS RESERVED.
======================================"""
                    st.download_button(label="📥 下载万字绝密档案 (.TXT)", data=TXT_LORE, file_name=f"LORE_{_pname}.txt", mime="text/plain", use_container_width=True)

                with e_json:
                    export_data = {
                        "version": VERSION, "copyright": COPYRIGHT, "player": _pname, "rarity": _rarity, "cp": _f_cp, "rank": local_db.get("pvp",{}).get("tier", "Unranked"),
                        "commander": { "id": _dm_key, "atk": _f_atk, "hp": _f_hp },
                        "equips": local_shop.get("relics", []), "hash": _hash, "lore": {"title": _pl_title}
                    }
                    st.download_button(label="📥 下载 TCG 底包 (JSON)", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"CARD_{_hash[:6]}.json", mime="application/json", use_container_width=True)

                with e_asc:
                    def m_b(v): return "█" * int(v/100*16) + "░" * (16 - int(v/100*16))
                    ASC_TEMP = f"""```text
========================================================
 ███▄    █  ▓█████  ▒█████     █████▒▄▄▄       ██████ 
 ██ ▀█   █  ▓█   ▀ ▒██▒  ██▒ ▓██   ▒▒████▄   ▒██    ▒ 
▓██  ▀█ ██▒ ▒███   ▒██░  ██▒ ▒████ ░▒██  ▀█▄ ░ ▓██▄   
========================================================
> PLAYER : {_pname} 
> CP_VAL : {_f_cp:,} CP [{_rarity}]
--------------------------------------------------------
[ COMMANDER / 主将面板 ]
> NAME   : {_dm_key} ({_dm_class})
> STATS  : ATK {_f_atk:,} | HP {_f_hp:,}

[ RADAR / 属性水晶 ]
  GOLD(财力) : {_wx.get('金',0):02d}% |{m_b(_wx.get('金',0))}|
  EXEC(执行) : {_wx.get('木',0):02d}% |{m_b(_wx.get('木',0))}|
  INT (智慧) : {_wx.get('水',0):02d}% |{m_b(_wx.get('水',0))}|
  LUCK(气运) : {_wx.get('火',0):02d}% |{m_b(_wx.get('火',0))}|
  CON (体魄) : {_wx.get('土',0):02d}% |{m_b(_wx.get('土',0))}|
========================================================
POWERED BY {COPYRIGHT}
```"""
                    st.markdown(ASC_TEMP)
            render_exports()

    # =========================================================================
    # ⌨️ [ TERMINAL ] 内联极简指令台
    # =========================================================================
    st.markdown("---")
    @st_fragment
    def render_terminal():
        current_logs = st.session_state["db"].get("term_logs", [])
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
                logs = st.session_state["db"]["term_logs"]
                logs.append(f"<span style='color:#fff;'>> {cmd_str}</span>")
                cmd_lower = cmd_str.lower()
                if cmd_lower == '/help': logs.append("<span style='color:#aaa;'>CMDS: /rank, /ping, /clear, /wuming</span>")
                elif cmd_lower == '/rank': 
                    f_cp = st.session_state["db"].get("computed", {}).get("cp", 0)
                    rank_pct = min(99.99, max(1.0, f_cp / 50000.0))
                    logs.append(f"<span style='color:var(--sp);'>[SYS] 当前最终战力(CP {f_cp:,})击败了全服 {rank_pct:.2f}% 的玩家。</span>")
                elif cmd_lower == '/clear': 
                    st.session_state["db"]["term_logs"] = ["> TERMINAL CLEARED."]
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
# 🛑 [ KERNEL 07 ] 版权声明
# =========================================================================
render_html(f'<div style="text-align:center; margin-top:40px; border-top: 1px dashed #333; padding-top: 30px; padding-bottom: 50px;"><div style="color:var(--primary); font-family:\'Orbitron\', sans-serif; font-size:12px; font-weight:bold; letter-spacing:4px;">© 2026 版权归属 {COPYRIGHT}</div></div>')
