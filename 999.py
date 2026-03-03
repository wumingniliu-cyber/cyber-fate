import streamlit as st
import random
import time
import hashlib
from datetime import datetime, time as dt_time

# ==============================================================================
# 🛡️ [ KERNEL 00 ] 智能自检防爆装甲 (物理级环境守卫)
# ==============================================================================
try:
    import numpy as np
    import plotly.graph_objects as go
    from lunar_python import Solar
except ImportError as e:
    st.set_page_config(page_title="SYSTEM KERNEL PANIC", page_icon="🚨", layout="centered")
    st.error(f"🚨 **FATAL ERROR: 赛博神谕终端缺少核心算力模块！**\n\n系统找不到模块: `{e.name}`")
    st.warning("请在同级目录的 requirements.txt 中添加：\n`streamlit`\n`lunar-python`\n`plotly`\n`numpy`\n然后重启服务器。")
    st.stop()

# ==============================================================================
# 🌌 [ KERNEL 01 ] 宇宙物理引擎与全局配置
# ==============================================================================
VERSION = "NEO-FATE_OS_V4.0"
COPYRIGHT = "NIGHT CITY DAO"
SYS_NAME = "量子命理 | NEO-FATE"

st.set_page_config(page_title=SYS_NAME, page_icon="🧿", layout="wide", initial_sidebar_state="collapsed")

def render_html(html_str):
    cleaned = '\n'.join([line.lstrip() for line in html_str.split('\n')])
    st.markdown(cleaned, unsafe_allow_html=True)

# ==============================================================================
# 🎨 [ KERNEL 02 ] 赛博朋克 2077 级 UI 底座 (玻璃拟态 + 故障艺术)
# ==============================================================================
render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&family=Orbitron:wght@500;700;900&family=Fira+Code:wght@400;700&display=swap');

:root {
    --bg-dark: #050508;
    --neon-cyan: #00f3ff;
    --neon-pink: #ff007c;
    --neon-yellow: #fcee0a;
    --neon-green: #00ff9d;
    --glass-bg: rgba(12, 12, 18, 0.75);
}

/* 强制全站黑客字体与深渊背景 */
html, body, .stApp { background-color: var(--bg-dark) !important; font-family: 'Noto Sans SC', sans-serif !important; color: #e0e0e0 !important; }
[data-testid="stHeader"], footer { display: none !important; }
.block-container { max-width: 1100px !important; padding-top: 2rem !important; overflow-x: hidden; }

/* CRT 扫描线特效 */
.stApp::before {
    content: " "; display: block; position: fixed; top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 999; background-size: 100% 2px, 3px 100%; pointer-events: none;
}

/* Glitch 故障标题 */
.glitch-title {
    font-family: 'Orbitron', sans-serif; font-size: clamp(2.5rem, 6vw, 4.5rem); font-weight: 900;
    text-transform: uppercase; text-align: center; color: var(--neon-cyan); text-shadow: 0 0 10px var(--neon-cyan);
    position: relative; margin-bottom: 0.5rem; letter-spacing: 6px;
}
.glitch-title::before, .glitch-title::after {
    content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.8;
}
.glitch-title::before { left: 3px; text-shadow: -2px 0 var(--neon-pink); animation: glitch 2.5s infinite linear alternate-reverse; }
.glitch-title::after { left: -3px; text-shadow: 2px 0 var(--neon-yellow); animation: glitch 3s infinite linear alternate-reverse; }
@keyframes glitch {
    0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); }
    40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); }
    80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); }
}

/* 赛博毛玻璃面板 */
.cyber-panel {
    background: var(--glass-bg); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 243, 255, 0.3); box-shadow: 0 0 20px rgba(0, 243, 255, 0.05), inset 0 0 20px rgba(0, 0, 0, 0.8);
    padding: 25px; border-radius: 6px; position: relative; margin-bottom: 25px; border-left: 4px solid var(--neon-pink);
}
.cyber-panel::before {
    content: "SYS.NODE.ACTIVE"; position: absolute; top: -12px; right: 15px;
    background: var(--bg-dark); color: var(--neon-pink); font-size: 10px; padding: 0 8px; font-family: 'Orbitron'; font-weight: bold; border: 1px solid var(--neon-pink);
}
.cyber-panel.yellow { border-left-color: var(--neon-yellow); border-color: rgba(252,238,10,0.3); box-shadow: 0 0 20px rgba(252,238,10,0.05), inset 0 0 20px rgba(0,0,0,0.8); }

/* 按钮重构：异形切角与发光 */
div.stButton > button {
    background: rgba(0, 0, 0, 0.5) !important; border: 1px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important; font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important; letter-spacing: 2px !important; text-transform: uppercase;
    transition: all 0.3s ease; border-radius: 0 !important; clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
    height: 55px; box-shadow: 0 0 10px rgba(0,243,255,0.1) !important;
}
div.stButton > button:hover {
    background: var(--neon-cyan) !important; color: #000 !important; box-shadow: 0 0 25px var(--neon-cyan) !important; transform: scale(1.02);
}
div.stButton > button[data-testid="baseButton-primary"] {
    background: var(--neon-pink) !important; color: #fff !important; border: none !important; box-shadow: 0 0 20px rgba(255,0,124,0.4) !important;
}
div.stButton > button[data-testid="baseButton-primary"]:hover { background: #ff3399 !important; box-shadow: 0 0 35px var(--neon-pink) !important; color: #fff !important;}
div.stButton > button[data-testid="baseButton-primary"] p { color: #fff !important; }

/* 黑客风输入框 */
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input {
    background: rgba(0,0,0,0.8) !important; color: var(--neon-green) !important;
    border: 1px solid rgba(0, 255, 157, 0.4) !important; font-family: 'Fira Code', monospace !important;
    text-align: center; border-radius: 0; font-size: 16px; font-weight: bold; height: 50px;
}
div[data-testid="stTextInput"] input:focus { border-color: var(--neon-green) !important; box-shadow: 0 0 15px rgba(0,255,157,0.4) !important; }
div[data-baseweb="select"] > div { background: rgba(0,0,0,0.8) !important; color: var(--neon-green) !important; border: 1px solid rgba(0, 255, 157, 0.4) !important; border-radius: 0 !important; font-family: 'Fira Code', monospace !important; }

/* 炫酷模块标题 */
.mod-title {
    color: #fff; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: 900;
    text-transform: uppercase; border-bottom: 1px dashed rgba(255,255,255,0.2);
    padding-bottom: 8px; margin-bottom: 20px; display: flex; align-items: center; letter-spacing: 1px;
}
.mod-title span { background: var(--neon-cyan); color: #000; padding: 2px 8px; margin-right: 12px; font-size: 0.9rem; }

/* ASCII 代码块保护 */
div[data-testid="stCodeBlock"] pre { background: #030305 !important; border: 1px solid #333 !important; border-left: 4px solid var(--neon-cyan) !important; border-radius: 4px; font-family: 'Fira Code', monospace !important; color: var(--neon-green) !important; }

/* Tabs 改造 */
[data-testid="stTabs"] button { color: #666 !important; font-family: 'Orbitron', sans-serif !important; font-weight: 700 !important; font-size: 15px !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--neon-pink) !important; border-bottom-color: var(--neon-pink) !important; text-shadow: 0 0 10px var(--neon-pink); }
</style>
""")

# ==============================================================================
# 🗃️ [ KERNEL 03 ] 极客黑话字典库 (MBTI + 义体与赛博阶级映射)
# ==============================================================================
DAY_MASTER_DICT = {
    "甲": {"mbti": "ENTJ", "role": "Root Node / 根服务器", "desc": "绝对的架构师。拥有宏大的底层构建能力，能在系统崩坏时扛起重构秩序的重任。", "color": "#00ff9d", "element": "木", "implant": "钛合金强固脊椎 (强化绝对承载力)"},
    "乙": {"mbti": "ENFP", "role": "P2P Network / 渗透网", "desc": "极其敏锐的嗅觉与恐怖的适应力。能在毫无资源的夹缝中疯狂攫取数据权限。", "color": "#34d399", "element": "木", "implant": "突触拓展插槽 (增加暗网抓取雷达)"},
    "丙": {"mbti": "ESTP", "role": "Overclock GPU / 超频核心", "desc": "充满爆裂输出的核聚变爆发力。只要你在线，就是全队输出最高绝对算力的发光体。", "color": "#ff007c", "element": "火", "implant": "微型核聚变胸腔堆 (提供无限动能)"},
    "丁": {"mbti": "INFJ", "role": "Optical Fiber / 幽网信标", "desc": "洞察人心的夜行者。擅长在最灰暗的地带，为系统提供精准的情绪价值与破局方向。", "color": "#ffaa00", "element": "火", "implant": "脑机共情模块 (读取并同频他人情绪)"},
    "戊": {"mbti": "ISTJ", "role": "Hardware Firewall / 防火墙", "desc": "稳如泰山，拥有物理级断网的防御力。最坚不可摧的安全底线与全网信用节点。", "color": "#fcee0a", "element": "土", "implant": "全覆式碳纤维装甲 (无视物理降维打击)"},
    "己": {"mbti": "ISFJ", "role": "Cloud Storage / 云端母体", "desc": "海纳百川的包容力，擅长无缝整合一切碎片数据。将天马行空的狂想转化为落地进程。", "color": "#d4af37", "element": "土", "implant": "海量冗余储存矩阵 (吞噬一切碎片资源)"},
    "庚": {"mbti": "ESTJ", "role": "Execution Thread / 杀毒进程", "desc": "杀伐果断，对低效与冗余代码零容忍。无情推进业务进度、斩断无效连接的风控大闸。", "color": "#ffffff", "element": "金", "implant": "高频螳螂臂刃 (物理超度低效节点)"},
    "辛": {"mbti": "INTP", "role": "Quantum Chip / 纳米精工", "desc": "永远追求完美的极致极客。能在粗糙的草台中，打磨出顶尖跨时代产品的核心大脑。", "color": "#e0e0e0", "element": "金", "implant": "纠缠态纳米手术刀 (代码级微观刺绣)"},
    "壬": {"mbti": "ENTP", "role": "Data Flood / 深网狂潮", "desc": "思维极其奔放，厌恶陈规。在瞬息万变的市场中，凭借直觉掀起降维打击的巨浪。", "color": "#00f3ff", "element": "水", "implant": "抗压液冷循环管 (防止超频脑机熔毁)"},
    "癸": {"mbti": "INTJ", "role": "Back Service / 幽灵算法", "desc": "极其隐秘，习惯幕后推演全局。擅长通过博弈和信息差，兵不血刃地窃取最高权限。", "color": "#3b82f6", "element": "水", "implant": "光学迷彩潜行皮肤 (从全网监控中隐身)"}
}

SHEN_SKILLS = {
    "七杀": "0-Day漏洞爆破 [Max]", "正官": "底层协议锚定 [Max]", 
    "偏印": "逆向工程解构 [Max]", "正印": "系统灾备兜底 [Max]",
    "偏财": "高频杠杆套利 [Max]", "正财": "算力资产控制 [Max]",
    "比肩": "P2P分布式共识 [Max]", "劫财": "网络节点劫持 [Max]",
    "食神": "UI感官体验降维 [Max]", "伤官": "范式秩序破坏 [Max]"
}

HEXAGRAMS = [
    ("乾为天 (THE CREATIVE)", "系统获得ROOT权限，算力如日中天，宜大举并发执行高能耗进程，抢占风口。"),
    ("坤为地 (THE RECEPTIVE)", "进入休眠与深层存储模式，积累缓存，避免盲目开辟新线程，宜猥琐发育。"),
    ("水雷屯 (SYSTEM BOOTING)", "初始化阶段配置异常，系统正在艰难 Boot，需耐心 Debug，切勿梭哈。"),
    ("火水未济 (UPDATING PATCH)", "代码编译接近尾声但尚未跑通，保持火力全开，随时准备热更新上线。"),
    ("地天泰 (PEACE / SYNCED)", "内外网 API 接口完美握手，数据流通极其顺畅，进入十年一遇黄金红利期。"),
    ("天地否 (DDOS ATTACKED)", "遭遇物理级断网或高频降维打击，服务器无响应，建议立刻拔网线停止操作。")
]

def gen_alpha_curve(seed_hash):
    rng = np.random.RandomState(int(seed_hash[:8], 16))
    years = [str(datetime.now().year + i) for i in range(10)]
    roi = [rng.randint(40, 70)]
    for _ in range(9): roi.append(max(10, min(100, roi[-1] + rng.randint(-25, 30))))
    return years, roi

# ==============================================================================
# 🔮 [ KERNEL 04 ] 状态机与终端采集口
# ==============================================================================
if 'booted' not in st.session_state:
    st.session_state.booted = False
    st.session_state.data = {}

if not st.session_state.booted:
    render_html(f"""
    <div style="text-align: center; margin-top: 8vh; margin-bottom: 40px;">
        <div style="color:var(--neon-pink); font-family:'Fira Code'; font-size:14px; letter-spacing:6px; margin-bottom:10px;">> /SYS/BOOT SEQUENCE INITIATED...</div>
        <h1 class="glitch-title" data-text="NEO-FATE OS">NEO-FATE OS</h1>
        <div style="color:var(--neon-cyan); font-family:'Orbitron'; font-size:12px; font-weight:700; letter-spacing:4px;">[ WEB3 SOUL-CODE DECRYPTOR V4.0 ]</div>
    </div>
    <div class="cyber-panel" style="max-width: 650px; margin: 0 auto; text-align:center;">
        <p style="color:#a0a0a0; font-size:14px; line-height:1.8;">肉体不过是碳基的载体，八字才是灵魂的底层代码。<br>输入降临坐标，提取你的高阶元神确权凭证。</p>
    </div>
    """)
    
    with st.form(key="login_form", border=False):
        col1, col2 = st.columns(2)
        with col1:
            user_name = st.text_input("赛博代号 [HANDLE]", placeholder="e.g. Neo / 银手", max_chars=16)
            birth_date = st.date_input("出厂历法 [COMPILE_DATE]", min_value=datetime(1900, 1, 1), max_value=datetime(2030, 12, 31), value=datetime(2000, 1, 1))
        with col2:
            gender = st.selectbox("机体型号 [CHASSIS]", ["乾造 (MALE)", "坤造 (FEMALE)"])
            birth_time = st.time_input("挂载时钟 [BOOT_TIME]", value=dt_time(12, 00))
        
        render_html("<br>")
        submit_btn = st.form_submit_button("▶ UPLINK TO THE MATRIX (接入矩阵)", type="primary", use_container_width=True)

        if submit_btn:
            user_name = user_name.strip() if user_name else f"Ghost_Node_{random.randint(100,999)}"
            
            # --- 历法核心计算 ---
            solar = Solar.fromYmdHms(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            # 五行与算力映射
            wx_str = bazi.getYearWuXing() + bazi.getMonthWuXing() + bazi.getDayWuXing() + bazi.getTimeWuXing()
            wx_counts = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
            for char in wx_str:
                if char in wx_counts: wx_counts[char] += 1
            
            # 找到最弱的五行推荐义体
            min_wx = min(wx_counts, key=wx_counts.get)
            total = sum(wx_counts.values()) or 1
            wx_scores_dict = {k: int((v/total)*100) for k, v in wx_counts.items()}
            
            # 抓取外挂技能库
            raw_skills = [SHEN_SKILLS.get(bazi.getYearShiShenGan(), ""), SHEN_SKILLS.get(bazi.getMonthShiShenGan(), ""), SHEN_SKILLS.get(bazi.getTimeShiShenGan(), "")]
            skills = list(set([s for s in raw_skills if s]))
            if not skills: skills = ["未定义幽灵进程 [Lv.?]"]

            # 赛博哈希与每日卦象锁定
            hash_id = hashlib.sha256(f"{user_name}{birth_date}{birth_time}".encode()).hexdigest().upper()
            rng = random.Random(f"{hash_id}{datetime.now().date()}")
            daily_hex = rng.choice(HEXAGRAMS)

            st.session_state.data = {
                "name": user_name, "gender": gender.split(" ")[0],
                "bazi_arr": [bazi.getYearGan() + bazi.getYearZhi(), bazi.getMonthGan() + bazi.getMonthZhi(), bazi.getDayGan() + bazi.getDayZhi(), bazi.getTimeGan() + bazi.getTimeZhi()],
                "day_master": bazi.getDayGan(),
                "wx_scores": wx_scores_dict,
                "missing_wx": min_wx,
                "skills": skills,
                "hash": hash_id,
                "hexagram": daily_hex
            }
            
            # 模拟黑客注入终端
            ph = st.empty()
            logs = ["[OK] BYPASSING ICE FIREWALL...", "[+] DECRYPTING SOUL HASH...", "[-] MAPPING WUXING NEURAL NET...", "[!] MINTING DESTINY SBT..."]
            log_text = ""
            for l in logs:
                log_text += f"<span style='color:var(--neon-green); font-family:Fira Code;'>{l}</span><br>"
                ph.markdown(f"<div class='cyber-panel' style='max-width: 650px; margin: 0 auto; height:150px;'>{log_text}</div>", unsafe_allow_html=True)
                time.sleep(0.35)
            
            st.session_state.booted = True
            st.rerun()

# ==============================================================================
# 📊 [ KERNEL 05 ] 全息算力大屏 (Holographic Dashboard)
# ==============================================================================
else:
    data = st.session_state.data
    dm = DAY_MASTER_DICT.get(data['day_master'], DAY_MASTER_DICT["甲"])
    bz = data['bazi_arr']
    
    # 顶部全局状态
    render_html(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:1px solid var(--neon-cyan); padding-bottom:10px; margin-bottom:25px;">
        <div>
            <div style="font-size:32px; font-weight:900; color:#fff; text-transform:uppercase; font-family:'Orbitron';">{data['name']} <span style="font-size:12px; color:var(--neon-pink); border:1px solid var(--neon-pink); padding:2px 6px; border-radius:2px; vertical-align:middle; font-weight:bold;">ROOT</span></div>
            <div style="font-family:'Fira Code'; color:#888; font-size:13px; margin-top:5px;">SBT_HASH: 0x{data['hash'][:24]}...</div>
        </div>
        <div style="text-align:right; font-family:'Fira Code'; color:var(--neon-green); font-size:14px; line-height: 1.5;">
            > SYS.OP: ONLINE<br>> SYNC_RATE: 100%
        </div>
    </div>
    """)

    # 🟢 [ 模块 1 & 2 ]: 源码解密 & 义体植入
    col1, col2 = st.columns([1.3, 1], gap="large")
    
    with col1:
        render_html("<div class='mod-title'><span>01</span>SOURCE CODE (因果底层源码)</div>")
        
        # 八字阵列 UI
        bz_html = '<div style="display:flex; justify-content:space-between; margin-bottom:20px; text-align:center;">'
        labels = ["YEAR_OS", "MONTH_OS", "CORE_DAY", "TIME_OS"]
        for i in range(4):
            is_core = (i == 2)
            bg = "rgba(255,0,124,0.15)" if is_core else "rgba(255,255,255,0.05)"
            bd = "var(--neon-pink)" if is_core else "#333"
            sh = "text-shadow: 0 0 15px var(--neon-pink);" if is_core else ""
            tc = "var(--neon-pink)" if is_core else "#fff"
            trans = "transform: scale(1.05); z-index: 2; box-shadow: 0 0 15px rgba(255,0,124,0.2);" if is_core else ""
            
            bz_html += f'''
            <div style="flex:1; background:{bg}; border:1px solid {bd}; padding:15px 0; border-radius:4px; margin: 0 5px; {trans}">
                <div style="font-size:clamp(24px, 4vw, 36px); font-weight:900; color:{tc}; {sh} line-height:1.1;">{bz[i][0]}<span style="color:#888; font-size:clamp(20px, 3vw, 28px);">{bz[i][1]}</span></div>
                <div style="font-size:10px; color:{bd}; font-family:'Orbitron'; margin-top:8px;">{labels[i]}</div>
            </div>'''
        bz_html += '</div>'
        render_html(bz_html)
        
        # 核心解析与 MBTI
        render_html(f"""
        <div class="cyber-panel" style="padding: 18px;">
            <div style="font-size:12px; color:var(--neon-cyan); font-family:'Orbitron'; margin-bottom:8px;">>> ARCHETYPE IDENTIFIER</div>
            <div style="font-size:24px; font-weight:900; color:{dm['color']}; text-shadow:0 0 10px {dm['color']}; display:flex; justify-content:space-between; align-items: center;">
                <span>{data['day_master']} · {dm['role']}</span>
                <span style="border:2px solid {dm['color']}; padding:2px 10px; border-radius:2px; font-size: 16px;">{dm['mbti']}</span>
            </div>
            <p style="color:#ccc; font-size:14px; line-height:1.6; margin-top:15px;">{dm['desc']}</p>
            <div style="margin-top:15px;">
                <span style="background:rgba(255,255,255,0.1); padding:4px 8px; font-size:12px; border-radius:2px; color:#fff; font-family:'Fira Code';">SIGNATURE WPN: {dm['weapon']}</span>
            </div>
        </div>
        """)

    with col2:
        render_html("<div class='mod-title'><span>02</span>CYBERWARE (外挂神经与义体)</div>")
        
        # 极客义体推荐 (取最弱五行)
        rec_implant = next(v['implant'] for k, v in DAY_MASTER_DICT.items() if v['element'] == data['missing_wx'])
        
        render_html(f"""
        <div class="cyber-panel yellow" style="padding: 18px;">
            <div style="font-size:12px; color:#aaa; margin-bottom:8px; font-family:'Fira Code';">⚠️ SYS.WARN: 系统算力池严重缺乏 <b style="color:var(--neon-yellow); font-size:16px;">{data['missing_wx']}</b> 属性基质。</div>
            <div style="font-size:14px; font-weight:bold; color:var(--neon-yellow); margin-bottom:5px;">[+] 强烈建议前往黑市植入义体：</div>
            <div style="font-size:16px; color:#fff; font-weight:900; letter-spacing:1px;">{rec_implant}</div>
        </div>
        """)
        
        # 十神技能云
        render_html("<div style='font-size:12px; color:#888; font-family:Orbitron; margin-bottom:10px;'>/// PRE-INSTALLED PLUGINS ///</div>")
        skills_html = "".join([f"<div style='border-left:3px solid var(--neon-cyan); background:rgba(0,243,255,0.05); padding:10px 15px; margin-bottom:8px; font-weight:bold; color:var(--neon-cyan); font-size:14px; font-family:\"Fira Code\"; box-shadow: 0 0 10px rgba(0,243,255,0.1);'>{s}</div>" for s in data['skills']])
        render_html(skills_html)

    # 🟡 [ 模块 3 & 4 ]: RPG 算力雷达 & 趋势预测
    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1.2], gap="large")
    
    with col3:
        render_html("<div class='mod-title'><span>03</span>PAYLOAD RADAR (RPG 面板)</div>")
        # 将五行包装成游戏六边形战士：金=力量，木=敏捷，水=智力，火=魅力，土=体质
        rpg_labels = ["STR(金/执行)", "AGI(木/拓展)", "INT(水/直觉)", "CHA(火/爆发)", "CON(土/承载)"]
        wx_vals = [data['wx_scores']['金'], data['wx_scores']['木'], data['wx_scores']['水'], data['wx_scores']['火'], data['wx_scores']['土']]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=wx_vals + [wx_vals[0]], theta=rpg_labels + [rpg_labels[0]],
            fill='toself', fillcolor='rgba(0, 243, 255, 0.2)', line=dict(color='#00f3ff', width=2), marker=dict(color='#ff007c', size=8)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=False, range=[0, max(wx_vals)+10]), angularaxis=dict(tickfont=dict(color='#fff', size=13), gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.2)')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=280, margin=dict(t=20, b=20, l=30, r=30)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col4:
        render_html("<div class='mod-title'><span>04</span>10-YEAR ALPHA (算力趋势曲线)</div>")
        years, trend = gen_alpha_curve(data['hash'])
        
        fig2 = go.Figure(data=go.Scatter(
            x=years, y=trend, mode='lines+markers', line=dict(color="#ff007c", width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(255, 0, 124, 0.15)', marker=dict(size=8, color="#00f3ff")
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#888', family='Fira Code'), title="Alpha 净值")
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # 🔴 [ 模块 5 ]: 裂变出图 & 高频互动模块
    st.markdown("---")
    
    t_card, t_oracle, t_premium = st.tabs(["📋 提取全息终端凭证 (SHARE)", "🎲 今日量子预言 (DAILY PING)", "💰 解锁阿卡夏深潜 (PREMIUM)"])
    
    with t_card:
        render_html("<div style='font-size:13px; color:var(--neon-green); margin-bottom:15px; font-family:Fira Code;'>[SUCCESS] 你的高阶本命档案已编译完毕。👇 点击代码框右上角『复制』按钮，无损发送至朋友圈或小红书。</div>")
        
        # ASCII 生成进度条
        def make_ascii_bar(val):
            filled = int(val / 100 * 12)
            return "█" * filled + "░" * (12 - filled)

        ascii_card = f"""```text
===================================================
 █▄░█ █▀▀ █▀█ ▄▄ █▀▀ ▄▀█ ▀█▀ █▀▀
 █░▀█ ██▄ █▄█ ░░ █▀░ █▀█ ░█░ ██▄
      [ NEO-FATE OS · DESTINY PROFILE ]
===================================================
> NODE_ID    : {data['name']} ({data['gender']})
> SOUL_HASH  : 0x{data['hash'][:16]}...
---------------------------------------------------
[ SOURCE CODE / 灵魂底层源码 ]
  {bz[0]}  |  {bz[1]}  | >> {bz[2]} << |  {bz[3]}
  (YR)    (MO)      (DY)      (TM)

[ CORE ARCHETYPE / 核心机体架构 ]
> DAY_MASTER : {data['day_master']} ({dm['element']} Node)
> ROLE_CLASS : {dm['role']}
> CYBER_MBTI : [ {dm['mbti']} ]
> SIGNATURE  : {dm['weapon']}

[ CYBER IMPLANTS / 预装外挂神经 ]
{chr(10).join(['  [+] ' + s for s in data['skills']])}

[ WUXING PAYLOAD / 算力负载均衡 ]
  STR(金) : {data['wx_scores']['金']:02d}% |{make_ascii_bar(data['wx_scores']['金'])}|
  AGI(木) : {data['wx_scores']['木']:02d}% |{make_ascii_bar(data['wx_scores']['木'])}|
  INT(水) : {data['wx_scores']['水']:02d}% |{make_ascii_bar(data['wx_scores']['水'])}|
  CHA(火) : {data['wx_scores']['火']:02d}% |{make_ascii_bar(data['wx_scores']['火'])}|
  CON(土) : {data['wx_scores']['土']:02d}% |{make_ascii_bar(data['wx_scores']['土'])}|
---------------------------------------------------
         POWERED BY LUNAR DESTINY ENGINE
         © 2026 NEO-FATE DAO.
===================================================
```"""
        st.markdown(ascii_card)

    with t_oracle:
        h_title, h_desc = data['hexagram']
        render_html(f"""
        <div style="text-align:center; padding: 30px 0;">
            <div style="font-size:14px; color:var(--neon-cyan); font-family:Orbitron; margin-bottom:10px;">/// DAILY QUANTUM HEXAGRAM ///</div>
            <div style="font-size:38px; color:var(--neon-yellow); font-weight:900; margin-bottom:20px; text-shadow: 0 0 15px rgba(252,238,10,0.5);">{h_title}</div>
            <div style="background:rgba(255,255,255,0.05); border-left:4px solid var(--neon-yellow); padding:20px; display:inline-block; max-width:600px; color:#ccc; text-align:left; font-size:15px; line-height: 1.6;">
                <b>[ SYSTEM LOG ] :</b> <br>{h_desc}
            </div>
        </div>
        """)

    with t_premium:
        render_html("""
        <div class="cyber-panel" style="text-align:center; border-color:var(--neon-pink); background:rgba(255, 0, 124, 0.05); margin-top:20px; border-left: 4px solid var(--neon-pink);">
            <div style="font-size:40px; margin-bottom:10px;">🔒</div>
            <div style="font-family:'Orbitron'; font-size:22px; color:var(--neon-pink); font-weight:bold; letter-spacing:2px; margin-bottom:10px;">UNLOCK AKASHIC DEEP DIVE</div>
            <div style="color:#aaa; font-size:14px; margin-bottom:25px; line-height:1.6;">接入量子 AI 算力池，立即解密：<br>【未来 12 个月搞钱精准爆点】/【赛博桃花双修合盘测试】/【前世底层源码追溯】</div>
            <div style="display:inline-block; padding:15px 35px; border:1px solid var(--neon-pink); background:rgba(255,0,124,0.1); color:var(--neon-pink); font-family:'Fira Code'; font-weight:bold; cursor:not-allowed; box-shadow: 0 0 15px rgba(255,0,124,0.2);">
                > PING PAYMENT GATEWAY ( 0.005 ETH / ¥ 9.9 )
            </div>
        </div>
        """)

    # 底部断开连接按钮
    render_html("<br><br>")
    if st.button("⏏ 物理断网并清除内存 (DISCONNECT & REBOOT)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # 页脚版权声明
    render_html(f"""
    <div style='text-align:center; color:#555; font-size:12px; margin-top:60px; font-family:Orbitron; border-top: 1px dashed #222; padding-top:20px;'>
        © 2026 {COPYRIGHT}. ALL RIGHTS RESERVED.<br>
        WAKE UP, NEO. THE MATRIX HAS YOU.
    </div>
    """)
