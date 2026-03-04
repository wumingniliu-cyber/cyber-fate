import streamlit as st
import random
import time
import math
import hashlib
import json
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

# ⚡ 局部重绘引擎 (极致卡牌交互体验，不刷新大盘)
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
VERSION = "KARMA TCG V50.0 [HOLO-FOIL EDITION]"
COPYRIGHT = "NIGHT CITY DAO"
SYS_NAME = "量子卡牌 | TCG 神之座"

st.set_page_config(page_title=SYS_NAME, page_icon="🎴", layout="wide", initial_sidebar_state="collapsed")

if "sys_booted" not in st.session_state: st.session_state["sys_booted"] = False
if "sys_data" not in st.session_state: st.session_state["sys_data"] = {}
if "term_logs" not in st.session_state: st.session_state["term_logs"] = ["> TCG_ENGINE READY. AWAITING DRAW..."]
if "gacha_drawn" not in st.session_state: st.session_state["gacha_drawn"] = False

def render_html(html_str):
    st.markdown('\n'.join([line.lstrip() for line in str(html_str).split('\n')]), unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ CSS ENGINE ] TCG 3D 卡牌渲染引擎与全息反光特效
# ==============================================================================
STATIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root { --ur: #ff007c; --sp: #ffaa00; --ssr: #fcee0a; --sr: #a855f7; --r: #00f3ff; --primary: #00f3ff; --bg-dark: #020306; }
html, body, .stApp { background-color: var(--bg-dark) !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e2e8f0 !important; cursor: crosshair !important; }
[data-testid="stHeader"], footer, section[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] { display: none !important; margin: 0 !important; padding: 0 !important; height: 0 !important;}
::-webkit-scrollbar { width: 6px; background: #000; } ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; }
.block-container { max-width: 1250px !important; padding-top: 2rem !important; padding-bottom: 5rem !important; overflow-x: hidden; }

/* 🃏 TCG 赛博牌桌背景 */
.stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.5) 50%), linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px), linear-gradient(0deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px); background-size: 100% 3px, 60px 60px, 60px 60px; z-index: -1; transform: perspective(600px) rotateX(20deg); transform-origin: top; opacity: 0.8; pointer-events: none;}
.stApp::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 35%, transparent 10%, rgba(2, 3, 6, 1) 85%); z-index: -2; pointer-events: none;}

/* ====================================================================== */
/* 🌟 核心引擎：3D 悬浮实体卡牌 & 镭射全息反光 (Holo-Foil Effect) */
/* ====================================================================== */
.tcg-card-container { perspective: 1200px; display: flex; justify-content: center; margin-bottom: 20px; }
.tcg-card {
    position: relative; width: 100%; max-width: 360px; aspect-ratio: 63 / 88; background: #0a0c10; 
    border: 3px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; 
    box-shadow: 0 15px 35px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,0,0,0.6);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease; 
    overflow: hidden; transform-style: preserve-3d; cursor: crosshair; display: flex; flex-direction: column;
}
.tcg-card::before { /* 镭射涂层 */
    content: ""; position: absolute; top: -50%; left: -150%; width: 150%; height: 200%;
    background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.5) 30%, rgba(0, 243, 255, 0.5) 40%, rgba(255, 0, 124, 0.3) 50%, transparent 60%);
    transform: skewX(-20deg); transition: all 0.6s ease; z-index: 10; pointer-events: none; mix-blend-mode: overlay;
}
.tcg-card:hover { transform: translateY(-15px) rotateX(8deg) rotateY(-6deg); box-shadow: -15px 30px 50px rgba(0,0,0,1), inset 0 0 40px rgba(0,243,255,0.1); z-index: 10; border-color: currentColor; }
.tcg-card:hover::before { animation: foil-sweep 2s infinite linear; }
@keyframes foil-sweep { 0% { left: -150%; } 100% { left: 200%; } }

/* 稀有度边框光效发散 */
.rarity-SP { border-color: var(--sp) !important; color: var(--sp); box-shadow: 0 10px 40px rgba(255,170,0,0.5), inset 0 0 30px rgba(255,170,0,0.2) !important; }
.rarity-UR { border-color: var(--ur) !important; color: var(--ur); box-shadow: 0 10px 40px rgba(255,0,124,0.4), inset 0 0 30px rgba(255,0,124,0.2) !important; }
.rarity-SSR { border-color: var(--ssr) !important; color: var(--ssr); box-shadow: 0 10px 40px rgba(252,238,10,0.3), inset 0 0 20px rgba(252,238,10,0.1) !important; }
.rarity-SR { border-color: var(--sr) !important; color: var(--sr); }
.rarity-R { border-color: var(--r) !important; color: var(--r); }

/* 卡面 UI 排版 */
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 10px; margin-bottom: 12px; }
.card-title { font-size: 28px; font-weight: 900; font-family: 'Noto Sans SC', sans-serif; text-shadow: 0 0 15px currentColor; margin: 0; line-height: 1;}
.card-class { font-family: 'Orbitron'; font-weight: 900; font-size: 14px; color:#fff; background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px;}
.card-art-box { flex: 1; background: repeating-linear-gradient(45deg, #111, #111 10px, #1a1a1a 10px, #1a1a1a 20px); border: 2px solid rgba(255,255,255,0.2); border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px; box-shadow: inset 0 0 40px rgba(0,0,0,0.9); overflow: hidden; position: relative;}
.card-art-char { font-size: 90px; font-weight: 900; opacity: 0.9; font-family: 'Noto Sans SC', serif; text-shadow: 0 0 40px currentColor; z-index:2; }
.card-desc-box { font-size: 12px; color: #cbd5e1; line-height: 1.6; background: rgba(0,0,0,0.6); padding: 12px; border-radius: 4px; border-left: 3px solid currentColor; margin-bottom: 12px; }
.card-stats-box { display: flex; justify-content: space-between; font-family: 'Orbitron'; font-size: 15px; font-weight: bold; background: rgba(255,255,255,0.1); padding: 10px 15px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); color: #fff;}
.tcg-badge { position:absolute; top:-2px; right:-2px; background:currentColor; color:#000; font-family:'Orbitron'; font-weight:900; font-size:18px; padding:5px 25px; border-radius:0 12px 0 12px; z-index:15; box-shadow:-2px 2px 10px rgba(0,0,0,0.5); text-shadow:0 0 5px rgba(255,255,255,0.5);}

/* 原生覆盖 */
.glass-panel { background: rgba(8, 10, 15, 0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: transform 0.3s; }
.glass-panel:hover { border-color: rgba(255,255,255,0.3); transform: translateY(-2px); }
.mod-title { color: #fff; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: 900; text-transform: uppercase; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 8px; margin-bottom: 20px; display: flex; align-items: center; letter-spacing: 1px; }
.mod-title span.tag { background: var(--primary); color: #000; padding: 2px 10px; margin-right: 12px; font-size: 0.9rem; font-weight:bold; clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%); }

/* 抽卡表单 */
div[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input { background-color: rgba(0, 0, 0, 0.8) !important; color: var(--sp) !important; font-family: 'Fira Code', monospace !important; border: 1px solid rgba(255,170,0,0.4) !important; border-radius: 4px !important; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; height: 55px; text-align: center; }
div[data-testid="stTextInput"] input:focus { box-shadow: 0 0 20px rgba(255,170,0,0.5) !important; transform: scale(1.02); }
div[data-baseweb="select"] > div { background-color: rgba(0,0,0,0.8) !important; border: 1px solid rgba(255,170,0,0.4) !important; color: var(--sp) !important; border-radius: 4px !important; height: 55px; text-align:center;}

div.stButton > button { background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(15,15,20,0.9)) !important; border: 1px solid var(--primary) !important; border-left: 4px solid var(--primary) !important; height: 55px !important; width: 100% !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); transition: all 0.2s;}
div.stButton > button p { color: #fff !important; font-size: 15px !important; font-weight: bold !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important; }
div.stButton > button:hover { border-color: var(--primary) !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: scale(1.02); }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #ff007c, #ffaa00) !important; border: none !important; box-shadow: 0 0 25px rgba(255,0,124,0.5) !important;}
div.stButton > button[data-testid="baseButton-primary"] p { font-size: 18px !important; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }

[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Orbitron', sans-serif !important; font-weight: 900 !important; font-size: 14px !important; padding-bottom: 12px !important; border-bottom: 2px solid transparent !important; transition: all 0.3s;}
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; text-shadow: 0 0 15px var(--primary); background: linear-gradient(0deg, rgba(0,243,255,0.1) 0%, transparent 100%); }

/* 🌟 抽卡开包爆闪动画 */
@keyframes pack-open { 0% { transform: scale(0.5) rotate(10deg); filter: brightness(5) blur(10px); opacity: 0;} 50% { transform: scale(1.05) rotate(-2deg); filter: brightness(2) blur(0px); opacity: 1;} 100% { transform: scale(1) rotate(0deg); filter: brightness(1); opacity: 1;} }
.card-reveal { animation: pack-open 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
@keyframes blink { 0%, 100% {opacity: 1;} 50% {opacity: 0.3;} }
</style>
"""
st.markdown(STATIC_CSS, unsafe_allow_html=True)

# ==============================================================================
# 🗃️ [ TCG DICTIONARY ] TCG 卡牌属性库 (带 ATK/DEF 面板)
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"class": "Paladin / 圣骑士", "mbti": "ENTJ", "color": "#10b981", "element": "木", "base_atk": 2500, "base_def": 4000, "hp": 12000, "desc": "掌控底层因果律的重装核心。宁折不弯，能扛起从0到1重构秩序的重任。", "weapon": "【神器】动能巨斧", "skill": "[被动] 建木庇护：队伍受到致命伤害时触发锁血。"},
    "乙": {"class": "Assassin / 刺客", "mbti": "ENFP", "color": "#a855f7", "element": "木", "base_atk": 3800, "base_def": 1500, "hp": 8500, "desc": "敏锐的暗网爬虫，能在资源枯竭的敌方后排疯狂生长，窃取权限。", "weapon": "【暗器】量子绞杀藤", "skill": "[主动] 寄生吸血：每次攻击窃取敌方 15% 算力补给自身。"},
    "丙": {"class": "Burst Mage / 爆裂法师", "mbti": "ESTP", "color": "#ff007c", "element": "火", "base_atk": 4800, "base_def": 1200, "hp": 8000, "desc": "全队绝对的输出核心。开启核聚变超频后，爆发毁天灭地的光芒。", "weapon": "【法器】等离子破城炮", "skill": "[终极] 恒星耀斑：首回合暴击率强制提升至 100%。"},
    "丁": {"class": "Enchanter / 附魔师", "mbti": "INFJ", "color": "#ffaa00", "element": "火", "base_atk": 2000, "base_def": 2500, "hp": 9000, "desc": "洞察人心的夜行者，在最灰暗战局中为团队提供精神增益与破防制导。", "weapon": "【法器】激光短刃", "skill": "[光环] 灵魂织网：全队获得 40% 护甲穿透增益。"},
    "戊": {"class": "Fortress / 堡垒", "mbti": "ISTJ", "color": "#fcee0a", "element": "土", "base_atk": 1500, "base_def": 5000, "hp": 15000, "desc": "拥有物理级断网防御力，最坚不可摧的矩阵底线与主T坦位。", "weapon": "【防具】绝对力场盾", "skill": "[被动] 盖亚装甲：免疫一次致死级降维打击。"},
    "己": {"class": "Summoner / 召唤师", "mbti": "ISFJ", "color": "#d4af37", "element": "土", "base_atk": 1800, "base_def": 3800, "hp": 11000, "desc": "海纳百川的云端存储池。无缝整合全场碎片转化为冗余资源护盾。", "weapon": "【法器】塌缩发生器", "skill": "[主动] 内存回收：回合结束时自动恢复 10% 体力。"},
    "庚": {"class": "Berserker / 狂战士", "mbti": "ESTJ", "color": "#ffffff", "element": "金", "base_atk": 4200, "base_def": 2800, "hp": 9500, "desc": "对低效代码零容忍的杀毒程序。无情推进并斩断一切无效连接。", "weapon": "【神器】振荡斩舰刀", "skill": "[被动] 审判肃清：对残血目标触发无视护甲的真实斩杀。"},
    "辛": {"class": "Sniper / 狙击手", "mbti": "INTP", "color": "#e0e0e0", "element": "金", "base_atk": 4500, "base_def": 1800, "hp": 7500, "desc": "追求极致的微观造物主。在无形中精准切断敌方的底层协议。", "weapon": "【暗器】纳米手术刀", "skill": "[主动] 纳米解构：所有攻击无视敌方 50% 物理装甲。"},
    "壬": {"class": "Controller / 控场法师", "mbti": "ENTP", "color": "#00f3ff", "element": "水", "base_atk": 3500, "base_def": 3000, "hp": 10000, "desc": "思维开阔奔放，极度厌恶陈规，凭借直觉掀起水淹七军的降维控制。", "weapon": "【防具】液态形变甲", "skill": "[主动] 渊海归墟：造成全场无差别的水属性群体硬控。"},
    "癸": {"class": "Illusionist / 幻影刺客", "mbti": "INTJ", "color": "#b026ff", "element": "水", "base_atk": 3000, "base_def": 3200, "hp": 8500, "desc": "习惯幕后推演全局。擅长通过博弈和信息差，兵不血刃窃取最终权限。", "weapon": "【法器】认知毒素", "skill": "[被动] 命运拨动：战斗前 2 回合处于无法被选中的隐身态。"}
}

# 圣遗物与装备池 (Shensha)
EQUIPS_DICT = {"七杀": "【装备】漏洞引爆器 (Crit Dmg +50%)", "正官": "【防具】协议装甲 (Resist +40%)", "偏印": "【法器】逆向解构仪 (Armor Pen +30%)", "正印": "【圣遗物】灾备十字架 (Revive 1x)", "偏财": "【法术】高频杠杆 (Draw +1)", "正财": "【装备】嗜血插件 (Lifesteal +15%)", "比肩": "【结界】共识网络 (Team Def +20%)", "劫财": "【法术】节点劫持木马 (Steal Buff)", "食神": "【法器】感官降维沙漏 (Enemy ATK -20%)", "伤官": "【法术】秩序破坏令 (Ignore Shield)"}

PAST_LIVES = [{"title": "V1.0 废土黑客", "debt": "曾滥用大招导致团灭。开局携带【悬赏】Debuff。"}, {"title": "V2.0 硅基反叛军", "debt": "反叛失败被退环境。今生自带极强【反击】属性。"}, {"title": "V3.0 财阀卡牌奴隶", "debt": "曾被困于低保底卡池。对【传说稀有度】极度渴望。"}, {"title": "V4.0 赛博雇佣兵", "debt": "清除了太多中立卡。需挂载辅助技能抵消业力。"}, {"title": "V5.0 矩阵先知", "debt": "偷看牌库导致规则崩坏。直觉(INT)满级，但血量减半。"}]

# TCG 每日法术卡池 (Hexagrams)
SPELL_POOL = [
    {"name": "✨ 乾为天 [GOD_MODE]", "type": "UR 场地魔法", "desc": "获取系统最高物理权限。本回合内，所有出牌无视 Cost 消耗。宜直接梭哈。", "color": "#ffaa00"},
    {"name": "🛡️ 坤为地 [SAFE_MODE]", "type": "SSR 永续陷阱", "desc": "进入绝对防御态。本回合受到的物理与网络伤害归零，但己方无法发起攻击。", "color": "#10b981"},
    {"name": "⚡ 地天泰 [SYNC_MAX]", "type": "UR 增益法术", "desc": "API 完美握手。抽取 2 张卡，并在接下来的 3 个回合内算力获取翻倍。", "color": "#00f3ff"},
    {"name": "💥 天地否 [DDOS_STRIKE]", "type": "SR 陷阱触发", "desc": "引爆全网大雪崩。双方立刻丢弃手牌并断网一回合。此节点极其凶险。", "color": "#f43f5e"},
    {"name": "🔄 水雷屯 [BOOT_LOOP]", "type": "R 妨碍法术", "desc": "给敌方主脑植入死循环代码。使其下回合的所有行动 Cost 增加 2 点。", "color": "#a855f7"},
    {"name": "⏳ 火水未济 [COMPILING]", "type": "SR 延迟法术", "desc": "代码编译中。将此卡盖放，下回合开始时触发全屏高额爆破 AOE 伤害。", "color": "#fb923c"}
]

# ==============================================================================
# 🧠 [ TCG ALGORITHMS ] 核心引擎与战力计算
# ==============================================================================
def calc_tcg_stats(hash_str, wx_dict, b_atk, b_def, equip_count):
    """🎲 动态稀有度与战力计算引擎"""
    wx_vals = list(wx_dict.values()) if wx_dict else [20]
    entropy = max(wx_vals) - min(wx_vals)
    
    # 稀有度判定：属性越极端（偏枯）或越平均，越稀有；带的装备词条越多越稀有
    if entropy > 60 or (entropy < 10 and equip_count >= 2): rarity, r_col = "SP", "SP"
    elif equip_count >= 3: rarity, r_col = "UR", "UR"
    elif entropy > 40 or equip_count >= 2: rarity, r_col = "SSR", "SSR"
    elif entropy < 25: rarity, r_col = "SR", "SR"
    else: rarity, r_col = "R", "R"
    
    # 战斗力(CP)计算
    rng = np.random.RandomState(int(hash_str[:8], 16))
    balance_multiplier = 1.6 if entropy < 15 else (1.3 if entropy > 50 else 1.0)
    tier_bonus = {"SP": 2.5, "UR": 2.0, "SSR": 1.5, "SR": 1.2, "R": 1.0}[rarity]
    
    cp = int((b_atk * 1.2 + b_def * 0.8) * balance_multiplier * tier_bonus * rng.uniform(0.9, 1.2) * 5)
    cp += equip_count * 2500 + int(hash_str[:4], 16) % 5000
    
    return rarity, r_col, cp

def pull_daily_spell(user_hash):
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_seed = int(hashlib.md5((str(user_hash) + today_str).encode()).hexdigest()[:8], 16)
    return random.Random(daily_seed).choice(SPELL_POOL), today_str

@st.cache_resource(show_spinner=False)
def gen_tcg_charts(seed_hash, wx_scores, dm_color):
    rng = np.random.RandomState(int(str(seed_hash)[:8], 16))
    
    # 6维战斗雷达
    wx_v = [wx_scores.get('金',20), wx_scores.get('木',20), wx_scores.get('水',20), wx_scores.get('火',20), wx_scores.get('土',20)]
    r_labels = ["力量(STR)", "敏捷(AGI)", "智力(INT)", "爆发(CRI)", "体质(CON)"]
    f_radar = go.Figure(data=go.Scatterpolar(r=wx_v+[wx_v[0]], theta=r_labels+[r_labels[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color=dm_color, width=2), marker=dict(color='#fff', size=6)))
    f_radar.update_layout(polar=dict(radialaxis=dict(visible=False), angularaxis=dict(tickfont=dict(color='#fff', size=12, family="Orbitron"))), paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=10, b=10, l=30, r=30))
    
    # 赛季大运推演
    yrs = [str(datetime.now().year + i) for i in range(10)]
    trend = [rng.randint(40, 60)]
    for _ in range(9): trend.append(max(10, min(100, trend[-1] + rng.randint(-25, 30))))
    f_trend = go.Figure(go.Scatter(x=yrs, y=trend, mode='lines+markers', line=dict(color="#f43f5e", width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.15)'))
    f_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(showgrid=False, tickfont=dict(color='#666', size=10)), yaxis=dict(showgrid=True, gridcolor='#222', tickfont=dict(color='#666', size=10)))
    
    # 12个月天梯环境热力图
    hm_z = rng.randint(20, 100, size=(4, 12)).tolist()
    hm_x = [f"{str(i).zfill(2)}月" for i in range(1, 13)]
    hm_y = ["财富(Gold)", "冲分(Rank)", "羁绊(Link)", "护甲(Def)"]
    f_hm = go.Figure(data=go.Heatmap(z=hm_z, x=hm_x, y=hm_y, colorscale="Turbo", showscale=False))
    f_hm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(t=10, b=10, l=60, r=10), xaxis=dict(tickfont=dict(family='Orbitron', color='#00f3ff', size=10)), yaxis=dict(tickfont=dict(family='Noto Sans SC', color='#fff', size=11)))
    
    return f_radar, f_trend, f_hm

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
        <span>TCG MATRIX V50.0 <b class="up">▲BOOSTER PACK READY</b></span>
        <span>NEW BANNER: SOUL MATRIX <b class="ur" style="color:var(--sp);">★ SP RATE UP</b></span>
        <span>SERVER: GACHA ENGINE <b class="up">▲ONLINE</b></span>
    </div></div>
    <div style="text-align: center; margin-bottom: 25px; margin-top:5vh;">
        <div style="color:var(--sp); font-family:'Orbitron', monospace; font-size:14px; letter-spacing:10px; margin-bottom:10px; animation:blink 2s infinite; text-shadow:0 0 10px var(--sp);">[ INSERT COIN TO PULL ]</div>
        <h1 class="hero-title" data-text="神之牌组终端">神之牌组终端</h1><br>
        <div style="color:var(--pink); font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; letter-spacing:10px; margin-top:10px;">DESTINY TCG V50.0</div>
    </div>
    <div class="glass-panel" style="max-width: 680px; margin: 0 auto 30px auto; border-left: 4px solid var(--sp); padding: 35px; text-align:center;">
        <div style="color:var(--sp); font-size: 20px; font-weight:900; letter-spacing: 2px; margin-bottom:15px; text-shadow:0 0 10px var(--sp);">“如果命运是一场牌局，出生就是第一次抽卡。”</div>
        <div style="color:#e2e8f0; font-size: 15px; line-height: 1.8;">
            输入你的物理降临坐标，在赛博算力池中进行 <b style="color:#fff;">单次强力抽卡 (1x PULL)</b>。<br>
            系统将为你鉴定 <b style="color:var(--pink);">卡牌稀有度 (SR/SSR/UR/SP)</b>。<br>并开启属于你的 <b style="color:var(--primary);">赛博主战者卡</b> 与 <b style="color:var(--purple);">初始配套卡组</b>。
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
            submit_btn = st.form_submit_button("🃏 消耗算力，抽取初始卡包 (OPEN PACK)", type="primary", use_container_width=True)

    if submit_btn:
        uname = str(uname).strip() if uname else "Player_01"
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
            if sg in EQUIP_DICT and EQUIP_DICT[sg] not in skills: skills.append(EQUIP_DICT[sg])
        if not skills: skills = ["【白板】无装备加成"]

        hash_id = hashlib.sha256((uname + str(bdate) + str(btime)).encode()).hexdigest().upper()
        p_life = PAST_LIVES[int(hash_id[:8], 16) % len(PAST_LIVES)]
        dm_key = str(bazi.getDayGan())
        
        dm_base = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"])
        rarity, r_col, cp = calc_tcg_stats(hash_id, wx_scores, dm_base["base_atk"], dm_base["base_def"], len(skills))

        st.session_state["sys_data"] = {
            "name": uname, "gender": str(ugender).split(" ")[0],
            "bazi_arr": [bazi.getYearGan()+bazi.getYearZhi(), bazi.getMonthGan()+bazi.getMonthZhi(), bazi.getDayGan()+bazi.getDayZhi(), bazi.getTimeGan()+bazi.getTimeZhi()],
            "day_master": dm_key, "past_life": p_life,
            "wx": wx_scores, "skills": skills, "hash": hash_id, "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "rarity": rarity, "r_col": r_col, "cp": cp
        }
        
        # ⚡ 抽卡金光闪烁动画 (0.6s)
        ph = st.empty()
        flash_color = "#00f3ff" if rarity=="SP" else ("#ffaa00" if rarity=="UR" else ("#fcee0a" if rarity=="SSR" else "#a855f7"))
        ph.markdown(f"<div class='tcg-card' style='max-width:320px; margin:0 auto; display:flex; justify-content:center; align-items:center; aspect-ratio:63/88; box-shadow:0 0 100px {flash_color}; border:4px solid {flash_color};'><div style='color:{flash_color}; font-family:Orbitron; font-size:25px; font-weight:900; line-height:2; text-align:center; animation: card-reveal 0.6s forwards;'><br>✦ TEARING PACK ✦<br><span style='font-size:50px;'>✨</span><br><br></div></div>", unsafe_allow_html=True)
        time.sleep(0.7)
        st.session_state["sys_booted"] = True
        st.rerun()

# ==============================================================================
# 🌟 [ TCG DASHBOARD ] 玩家对战大厅
# ==============================================================================
else:
    d = st.session_state.get("sys_data", {})
    dm_key = str(d.get('day_master', '甲'))
    dm_info = DAY_MASTER_DICT.get(dm_key, DAY_MASTER_DICT["甲"]) 
    
    dm_class = str(dm_info.get("class", "Unknown"))
    dm_color = str(dm_info.get("color", "#00f3ff"))
    dm_desc = str(dm_info.get("desc", "..."))
    dm_wpn = str(dm_info.get("weapon", "无"))
    dm_skill = str(dm_info.get("skill", "无"))
    dm_mbti = str(dm_info.get("mbti", "UNK"))
    b_atk = dm_info.get("base_atk", 5000)
    b_def = dm_info.get("base_def", 5000)
    b_hp = dm_info.get("hp", 8000)
    
    bz = [str(x) for x in d.get('bazi_arr', ['??', '??', '??', '??'])] 
    hash_id = str(d.get('hash', '0000000000')).ljust(8, '0')
    wx_scores = d.get('wx', {'金':20, '木':20, '水':20, '火':20, '土':20})
    skills_list = d.get('skills', ['无被动'])
    past_life = d.get('past_life', PAST_LIVES[0])
    
    rarity = d.get("rarity", "SR")
    r_col_cls = d.get("r_col", "SR")
    cp = d.get("cp", 50000)
    
    f_radar, f_trend, f_hm = gen_tcg_charts(hash_id, wx_scores, dm_color)
    spell_card, date_str = pull_daily_spell(hash_id)
    sc_c = str(spell_card.get("color", "var(--primary)"))

    HEADER_HTML = f"""
    <div class="ticker-wrap"><div class="ticker">
        <span>TCG-ENGINE: V50.0 <b class="up">▲SYNCED</b></span>
        <span>PLAYER: {d.get('name', 'GHOST')} <b class="up">▲ACTIVE</b></span>
        <span>RARITY_PULLED: {rarity} <b class="up">▲LOCKED</b></span>
    </div></div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid {dm_color}; padding-bottom:15px; margin-bottom:30px;">
        <div>
            <div style="font-family:'Fira Code'; color:#aaa; font-size:12px; margin-bottom:5px; font-weight:bold;">[ PLAYER WALLET: 0x{hash_id[:12]} ]</div>
            <div style="font-size:clamp(28px, 5vw, 40px); font-weight:900; color:#fff; font-family:'Orbitron'; line-height:1;">
                {d.get('name', 'P1')} 
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
    # 🎴 模块 I：左侧全息主战卡，右侧卡组装备
    # =========================================================================
    c1, c2 = st.columns([1, 1.2], gap="large")

    with c1:
        render_html("<div class='mod-title'><span class='tag'>HERO</span> 本命主战神卡 (COMMANDER)</div>")
        
        # 🌟 核心黑科技：纯 CSS 3D 全息镭射实体卡牌 (不占 Python 性能)
        holo_fx = "holo-ur" if rarity in ["UR", "SP"] else ""
        TCG_CARD_HTML = f"""
        <div class="tcg-card-container">
            <div class="tcg-card rarity-{r_col_cls} {holo_fx}" style="color:{dm_color};">
                <div class="tcg-badge">{rarity}</div>
                
                <div class="card-header">
                    <div class="card-title">{dm_key}</div>
                    <div class="card-class">{dm_mbti}</div>
                </div>
                
                <div class="card-art-box">
                    <div class="card-art-char">{dm_key}</div>
                </div>
                
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-family:'Orbitron'; font-size:13px; color:#fff; font-weight:bold;">[ {dm_class} ]</div>
                    <div style="font-size:12px; font-weight:bold; color:var(--sp);">⚔️ {dm_wpn.split(' ')[0]}</div>
                </div>
                
                <div class="card-desc-box">
                    <div style="color:{dm_color}; font-weight:bold; margin-bottom:6px; font-size:13px;">{dm_skill}</div>
                    <i>"{dm_desc}"</i>
                </div>
                
                <div class="card-stats-box">
                    <span style="color:#f43f5e;">ATK: {b_atk}</span>
                    <span style="color:#10b981;">HP: {b_hp}</span>
                    <span>DEF: {b_def}</span>
                </div>
            </div>
        </div>
        """
        render_html(TCG_CARD_HTML)

    with c2:
        render_html("<div class='mod-title'><span class='tag'>DECK</span> 基础卡组与装备栏 (LOADOUT)</div>")
        
        bz_html = '<div style="display:flex; justify-content:space-between; margin-bottom:20px; text-align:center;">'
        labels = ["OS_YEAR", "ENV_MONTH", "CORE_DAY", "THD_TIME"]
        for i in range(4):
            is_core = (i == 2)
            bg = f"linear-gradient(180deg, {dm_color}33 0%, transparent 100%)" if is_core else "rgba(255,255,255,0.03)"
            bd = dm_color if is_core else "#333"
            tc = dm_color if is_core else "#fff"
            trans = f"transform: scale(1.05); box-shadow: 0 0 15px {dm_color}44; border-width:2px;" if is_core else "border:1px solid rgba(255,255,255,0.1);"
            bz_html += f"""<div style="flex:1; background:{bg}; border:1px solid {bd}; padding:15px 0; border-radius:4px; margin:0 4px; {trans}"><div style="font-size:clamp(22px, 3.5vw, 32px); font-weight:900; color:{tc}; line-height:1.1; font-family:'Noto Sans SC';">{bz[i][0]}<span style="color:#777; font-size:clamp(16px, 2.5vw, 24px);">{bz[i][1]}</span></div><div style="font-size:10px; color:{bd}; font-family:'Orbitron'; margin-top:8px; font-weight:bold;">{labels[i]}</div></div>"""
        bz_html += '</div>'
        render_html(bz_html)

        render_html("<div style='font-size:13px; color:var(--purple); font-family:\"Orbitron\"; margin-bottom:10px; font-weight:bold;'>>> EQUIPPED TRAITS (挂载装备与被动)</div>")
        sk_html = "<div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px;'>"
        for s in skills_list[:4]:
            t_col = "var(--ur)" if "被动" in s else "var(--primary)"
            sk_html += f"<div style='background:rgba(0,0,0,0.6); border:1px solid #333; border-left:3px solid {t_col}; padding:10px; border-radius:4px; box-shadow:inset 0 0 10px {t_col}22;'><div style='font-size:12px; font-weight:bold; color:#fff; font-family:\"Noto Sans SC\";'>{s}</div></div>"
        sk_html += "</div>"
        
        render_html(f"""
        <div class="glass-panel" style="padding:15px; margin-bottom:15px;">{sk_html}</div>
        <div class="glass-panel" style="border-left-color:var(--yellow); padding:15px;">
            <div style="font-size:11px; color:var(--yellow); font-family:'Orbitron'; margin-bottom:5px; font-weight:bold;">>> KARMIC LORE (前世剧情)</div>
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">{past_life['title']}</div>
            <div style="color:#aaa; font-size:12px;">{past_life['debt']}</div>
        </div>
        """)

    # 🗄️ [ 模块 III ]：TCG 玩法大厅
    render_html("<div class='mod-title' style='margin-top:20px;'><span class='tag'>LOBBY</span> TCG 战术指挥室 (BATTLE CONSOLE)</div>")
    t_gacha, t_data, t_syn, t_export = st.tabs(["🎰 每日法术单抽 (GACHA)", "📊 战力大盘推演 (STATS)", "🤝 双排羁绊测试 (TAG-TEAM)", "📸 封装实体卡砖 (PSA 10)"])

    with t_gacha:
        c_g1, c_g2 = st.columns([1.1, 1], gap="large")
        with c_g1:
            render_html("<div style='color:var(--sp); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ DAILY SPELL PULL ] 每日盲盒</div>")
            
            @st_fragment
            def render_gacha_1pull():
                is_drawn = st.session_state.get("gacha_drawn", False)
                if not is_drawn:
                    render_html("""
                    <div class="glass-panel" style="text-align:center; padding:60px 20px; border-color:var(--sp); border-style:dashed;">
                        <div style="font-size:55px; margin-bottom:15px; animation:blink 2s infinite;">📦</div>
                        <div style="color:var(--sp); font-family:'Orbitron'; font-size:18px; font-weight:900; letter-spacing:4px; margin-bottom:10px;">DAILY PACK SEALED</div>
                        <div style="color:#aaa; font-size:13px;">每日一次免费单抽。点击下方按钮拆开今日的法术卡盲盒。</div>
                    </div>
                    """)
                    st.button("⚡ 消耗 0 算力开启盲盒 (OPEN PACK)", on_click=trigger_gacha_draw, use_container_width=True)
                else:
                    GACHA_HTML = f"""
                    <div class="tcg-card-container card-reveal" style="max-width:320px; margin:0 auto;">
                        <div class="tcg-card" style="border-color:{sc_c}; box-shadow:0 0 40px {sc_c}66; aspect-ratio: 63/88; background:linear-gradient(0deg, rgba(0,0,0,0.95), {sc_c}22);">
                            <div style="padding:15px; text-align:center;">
                                <div style="font-family:'Orbitron'; color:{sc_c}; font-size:11px; font-weight:bold; letter-spacing:2px; margin-bottom:15px;">[ DATE: {date_str} ]</div>
                                <div style="background:{sc_c}; color:#000; display:inline-block; padding:4px 15px; font-family:'Orbitron'; font-weight:900; font-size:14px; border-radius:2px; margin-bottom:15px;">{spell_card['type']}</div>
                                <div style="font-size:24px; font-weight:900; color:#fff; font-family:'Noto Sans SC'; margin-bottom:20px; text-shadow:0 0 10px {sc_c};">{spell_card['name']}</div>
                                <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:4px; text-align:left; border:1px solid rgba(255,255,255,0.1); font-size:13px; line-height:1.6; color:#ddd; margin-bottom:15px;">
                                    <b style="color:{sc_c}; font-family:'Fira Code';">> EFFECT:</b><br>{spell_card['desc']}
                                </div>
                                <div style="font-size:12px; color:var(--green); font-weight:bold; text-align:left;">[+] 连招: {spell_card.get('do','')}</div>
                                <div style="font-size:12px; color:var(--pink); font-weight:bold; text-align:left; margin-top:5px;">[-] 规避: {spell_card.get('dont','')}</div>
                            </div>
                        </div>
                    </div>
                    """
                    render_html(GACHA_HTML)
            render_gacha_1pull()
            
        with c_g2:
            render_html("<div style='color:var(--primary); font-family:Orbitron; font-size:14px; font-weight:900; margin-bottom:15px;'>[ ACTION ROLL ] 行动暗骰检定</div>")
            render_html("<div style='font-size:13px; color:#aaa; margin-bottom:20px;'>向系统发起一个具体行动的成功率检定（D100）。</div>")
            @st_fragment
            def render_dice():
                ph = st.empty()
                with st.form(key="dice_form", clear_on_submit=False, border=False):
                    q_input = st.text_input("📝 输入检定事件：", placeholder="e.g. 攻击这个Boss有胜算吗？", label_visibility="collapsed")
                    sub_q = st.form_submit_button("🎲 掷骰检定 (ROLL D100)", use_container_width=True)
                if sub_q:
                    if not q_input: ph.warning("⚠️ 语法错误：事件为空！")
                    else:
                        prob, hex_res, conc = get_quantum_answer(q_input, hash_id)
                        q_c = hex_res['color']
                        RES = f"""
                        <div class="glass-panel card-reveal" style="margin-top:10px; border-color:{q_c}; text-align:center; border-left-width: 4px;">
                            <div style="font-family:'Fira Code'; color:#888; font-size:12px; margin-bottom:10px;">> ACTION: "{q_input}"</div>
                            <div style="font-size:11px; color:{q_c}; font-family:'Orbitron'; letter-spacing:2px; margin-bottom:5px;">[ D100 RESULT ]</div>
                            <div style="font-size:65px; font-weight:900; color:{q_c}; font-family:'Orbitron'; text-shadow:0 0 20px {q_c}; line-height:1; margin-bottom:15px;">{prob}</div>
                            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:5px;">触发机制：{hex_res['name']}</div>
                            <div style="font-size:12px; font-weight:bold; color:{q_c};">{conc}</div>
                        </div>
                        """
                        ph.markdown(RES, unsafe_allow_html=True)
            render_dice()

    with t_data:
        c_st1, c_st2 = st.columns([1, 1.2], gap="large")
        with c_st1:
            render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ COMBAT RADAR ] 六维战斗面板</div>")
            st.plotly_chart(f_radar, use_container_width=True, config={'displayModeBar': False})
            
            bar_html = "<div class='glass-panel' style='padding:15px; border-top:none;'>"
            wx_colors = {'金': '#e2e8f0', '木': '#10b981', '水': '#00f3ff', '火': '#f43f5e', '土': '#fcee0a'}
            for k, v in wx_scores.items():
                col = wx_colors.get(k, '#fff')
                bar_html += f"<div style='display:flex; align-items:center; margin-bottom:8px; font-size:12px; font-weight:bold;'><span style='width:25px; color:{col};'>{k}</span><div style='flex:1; height:8px; background:rgba(255,255,255,0.05); border-radius:4px; margin:0 10px; position:relative;'><div style='position:absolute; top:0; left:0; height:100%; width:{v}%; background:{col}; border-radius:4px; box-shadow:0 0 10px {col};'></div></div><span style='width:35px; text-align:right; color:#888;'>{v}%</span></div>"
            bar_html += "</div>"
            render_html(bar_html)
            
        with c_st2:
            render_html("<div style='font-size:12px; color:var(--primary); font-family:Orbitron; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 12-MONTH META SHIFT ] 年度天梯环境热力图</div>")
            st.plotly_chart(f_hm, use_container_width=True, config={'displayModeBar': False})
            
            render_html("<div style='font-size:12px; color:var(--pink); font-family:Orbitron; margin-top:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>[ 10-YEAR WIN RATE ] 胜率推演大盘</div>")
            st.plotly_chart(f_trend, use_container_width=True, config={'displayModeBar': False})

    with t_syn:
        @st_fragment
        def render_synergy_section():
            c_l1, c_l2 = st.columns([1.2, 1], gap="large")
            with c_l1:
                render_html("<div style='font-size:14px; color:#aaa; margin-top:15px; margin-bottom:15px; font-weight:bold;'>选择目标队友的【主将卡】，测算双打 (Tag-Team) 时的连携共鸣率：</div>")
                opts = list(DAY_MASTER_DICT.keys())
                t_node = st.selectbox("🎯 选择助战位卡牌:", options=opts, format_func=lambda x: f"[{DAY_MASTER_DICT.get(x, {}).get('tier', 'N')}] {x} - {DAY_MASTER_DICT.get(x, {}).get('class', 'UNK').split('/')[0]}")
            with c_l2:
                sc, sd, sc_color = calc_tag_team(hash_id, t_node)
                render_html(f"<div class='glass-panel card-reveal' style='border-left:4px solid {sc_color}; text-align:center; margin-top:15px;'><div style='font-family:\"Orbitron\"; font-size:12px; color:#888; letter-spacing:2px; margin-bottom:10px;'>TAG-TEAM RESONANCE</div><div style='font-family:\"Orbitron\"; font-size:60px; color:{sc_color}; font-weight:900; margin-bottom:10px; text-shadow:0 0 20px {sc_color}; line-height:1;'>{sc}%</div><div style='color:#fff; font-size:14px; font-weight:bold; font-family:\"Noto Sans SC\"; line-height:1.6;'>{sd}</div></div>")
        render_synergy_section()

    with t_export:
        @st_fragment
        def render_psa_export():
            render_html("<div style='text-align:center; color:#888; font-size:13px; margin-top:10px; margin-bottom:15px;'>将你的主战卡压制为一张 <b style='color:var(--sp);'>PSA 10分 实体评级卡砖</b>。出图后长按即可保存至相册发圈。</div>")
            
            c_e1, c_e2 = st.columns(2, gap="large")
            with c_e1:
                if st.button("📸 压制 PSA 典藏卡砖 (MINT SLAB)", use_container_width=True):
                    sk_h = "".join([f"<span style='background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); color:#fff; padding:2px 6px; margin:2px; font-size:9px; display:inline-block; font-family:Fira Code; border-radius:2px;'>{s.split(' ')[1] if ' ' in s else s}</span>" for s in skills_list[:3]])
                    
                    # 🚨 终极安全渲染，杜绝 f-string 花括号冲突
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
                        #final-img { display:none; width:100%; max-width:380px; box-shadow:0 15px 40px rgba(0,0,0,0.9); border-radius:12px; margin-top:10px; }
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
                            
                            <div style="text-align:right; font-family:'Orbitron'; font-size:8px; color:#666; margin-top:10px;">© 2026 TCG MATRIX</div>
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
                    
                    html_ready = HTML_POSTER_RAW.replace("__COLOR__", dm_color).replace("__PLAYER__", d.get('name', 'P1').upper())
                    html_ready = html_ready.replace("__HASH__", hash_id[:10]).replace("__DM_KEY__", dm_key).replace("__CLASS__", dm_class.split('/')[0].strip())
                    html_ready = html_ready.replace("__TIER__", rarity).replace("__CP__", f"{cp_val:,}")
                    html_ready = html_ready.replace("__WPN__", dm_wpn).replace("__SKILL__", dm_skill).replace("__DESC__", dm_desc)
                    html_ready = html_ready.replace("__EQUIPS__", sk_html_img).replace("__ATK__", str(b_atk)).replace("__HP__", str(b_hp))
                    
                    components.html(html_ready, height=750)
            
            with c_e2:
                TXT_CARD = f"""```text
======================================
  [ TCG COMMANDER DECK PROFILE ]
======================================
> PLAYER  : {d.get('name','')}
> CP_VAL  : {cp_val:,} CP
--------------------------------------
> CARD_ID : {bz[2]} [{rarity}]
> CLASS   : {dm_key} · {dm_class}
--------------------------------------
[ STATS ]
  ATK: {b_atk} | DEF: {b_def} | HP: {b_hp}
[ EQUIPS ]
{chr(10).join(['  + ' + s for s in skills_list[:4]])}
[ RESOURCES ]
  STR: {wx_scores.get('金',0):02d}%  |  AGI: {wx_scores.get('木',0):02d}%
  INT: {wx_scores.get('水',0):02d}%  |  CRI: {wx_scores.get('火',0):02d}%
  CON: {wx_scores.get('土',0):02d}% 
======================================
```"""
                st.markdown(TXT_CARD)
        render_psa_export()

    # =========================================================================
    # ⌨️ [ TERMINAL ] 内联极简指令台
    # =========================================================================
    st.markdown("---")
    @st_fragment
    def render_terminal():
        current_logs = st.session_state.get("term_logs", ["> TCG_ENGINE READY."])
        log_html = "<br>".join(current_logs[-4:])
        render_html(f"<div style='max-width: 800px; margin: 0 auto; background:#000; border:1px solid #333; padding:15px; font-family:\"Fira Code\"; color:var(--primary); font-size:13px; height:120px; display:flex; flex-direction:column-reverse; overflow:hidden;'><div>{log_html}<span style=\"animation:blink 1s infinite;\">_</span></div></div>")

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
                elif cmd_lower == '/rank': logs.append(f"<span style='color:var(--sp);'>[SYS] 您的当前战力(CP {cp_val})击败了全服 87.4% 的玩家。</span>")
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
render_html(f'<div style="text-align:center; margin-top:30px; border-top: 1px dashed #222; padding-top: 30px;"><div style="color:#666; font-family:\'Orbitron\'; font-size:11px; letter-spacing:4px;">© 2026 {COPYRIGHT}</div></div>')
