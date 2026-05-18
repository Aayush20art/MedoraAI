"""
MediMind — Premium CSS Theme Block
===================================
Replace the entire st.markdown(\"\"\"<style>...</style>\"\"\") block in your app.py
with this constant. Call it once at the top after set_page_config():

    from medimind_premium_css import PREMIUM_CSS
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

Font stack  : Syne (display) + DM Sans (body) + JetBrains Mono (mono)
Palette     : Deep ink bg · Electric cyan primary · Violet secondary · Rose accent
Animations  : Infinite gradient bar, scan line, card lifts, button pulses,
              gauge glow, chat bubble reveals, scrollbar style, hover shimmers
"""

CSS = """
<style>
/* ══════════════════════════════════════════════════════
   FONTS
══════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;1,14..32,400&family=Fira+Code:wght@400;500;600&display=swap');

/* ══════════════════════════════════════════════════════
   TOKENS
══════════════════════════════════════════════════════ */
:root {
    /* Backgrounds */
    --ink:         #06090f;
    --surface:     #0c1120;
    --panel:       #111827;
    --card:        #141c2e;
    --lift:        #1a2440;

    /* Brand */
    --cyan:        #00e5ff;
    --cyan2:       #00b4d8;
    --violet:      #a78bfa;
    --violet2:     #7c3aed;
    --rose:        #fb7185;
    --emerald:     #34d399;
    --amber:       #fbbf24;

    /* Text */
    --white:       #eef4ff;
    --dim:         rgba(238,244,255,.62);
    --muted:       rgba(238,244,255,.35);

    /* Borders / glows */
    --line:        rgba(0,229,255,.1);
    --line-h:      rgba(0,229,255,.28);
    --glow-c:      rgba(0,229,255,.22);
    --glow-v:      rgba(167,139,250,.22);
    --glow-r:      rgba(251,113,133,.22);
    --glow-e:      rgba(52,211,153,.22);

    /* Fonts */
    --ff-display:  'Orbitron', sans-serif;
    --ff-body:     'Inter', sans-serif;
    --ff-mono:     'Fira Code', monospace;
}

/* ══════════════════════════════════════════════════════
   GLOBAL RESET
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: var(--ff-body) !important;
    background:  var(--ink) !important;
    color:       var(--dim) !important;
    scroll-behavior: smooth;
}

/* ══════════════════════════════════════════════════════
   APP SHELL — animated grid + scan line + aura
══════════════════════════════════════════════════════ */
.stApp {
    background: var(--ink) !important;
    background-image:
        linear-gradient(rgba(0,229,255,.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,.045) 1px, transparent 1px),
        radial-gradient(ellipse 80% 60% at 15% 25%, rgba(0,229,255,.04), transparent),
        radial-gradient(ellipse 70% 70% at 85% 75%, rgba(167,139,250,.035), transparent) !important;
    background-size: 52px 52px, 52px 52px, 100% 100%, 100% 100% !important;
    animation: gridpulse 12s ease-in-out infinite;
}
@keyframes gridpulse {
    0%,100% { background-size: 52px 52px, 52px 52px, 100% 100%, 100% 100%; }
    50%      { background-size: 54px 54px, 54px 54px, 100% 100%, 100% 100%; }
}

# /* Scan line */
# .stApp::after {
#     content: '';
#     position: fixed;
#     top: -2px; left: 0; right: 0; height: 2px;
#     background: linear-gradient(90deg, transparent, var(--cyan), transparent);
#     animation: scanline 6s linear infinite;
#     pointer-events: none;
#     z-index: 9999;
#     opacity: .5;
# }
# @keyframes scanline { 0% { top: -2px; } 100% { top: 100vh; } }

/* ══════════════════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════════════════ */
::-webkit-scrollbar              { width: 5px; height: 5px; }
::-webkit-scrollbar-track        { background: var(--ink); }
::-webkit-scrollbar-thumb        { background: rgba(0,229,255,.3); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover  { background: rgba(0,229,255,.55); }

/* ══════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090e1a 0%, #06090f 100%) !important;
    border-right: 1px solid var(--line) !important;
    position: relative;
}

/* Sidebar animated left accent bar */
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute; top: 0; left: 0; bottom: 0; width: 2px;
    background: linear-gradient(180deg, var(--violet), var(--cyan), var(--emerald), var(--violet));
    background-size: 100% 300%;
    animation: sidebarbar 5s linear infinite;
    border-radius: 0 2px 2px 0;
}
@keyframes sidebarbar {
    0%   { background-position: 0%   0%; }
    100% { background-position: 0% 300%; }
}

[data-testid="stSidebar"] * { color: var(--dim) !important; }

/* ── Brand block ── */
.brand-wrap {
    padding: 28px 20px 22px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 14px;
}
.brand-logo-row {
    display: flex; align-items: center; gap: 14px;
}
.brand-icon {
    width: 50px; height: 50px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--cyan), var(--violet));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    box-shadow: 0 4px 20px var(--glow-c), 0 0 0 1px rgba(0,229,255,.2);
    animation: iconpulse 3s ease-in-out infinite;
}
@keyframes iconpulse {
    0%,100% { box-shadow: 0 4px 20px var(--glow-c), 0 0 0 1px rgba(0,229,255,.2); }
    50%      { box-shadow: 0 6px 32px var(--glow-c), 0 0 0 2px rgba(0,229,255,.35); }
}
.brand-title {
    font-family: var(--ff-display);
    font-size: 2rem; font-weight: 800; letter-spacing: -.5px;
    background: linear-gradient(135deg, #fff, var(--dim));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.brand-title span {
    background: linear-gradient(135deg, var(--cyan), var(--violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.brand-tagline {
    font-family: var(--ff-mono);
    font-size: .58rem; letter-spacing: 2px;
    text-transform: uppercase; color: var(--muted) !important;
    margin-top: 5px;
}
.brand-badges { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
.brand-badge {
    font-family: var(--ff-mono);
    font-size: .55rem; letter-spacing: 1.5px;
    padding: 4px 10px; border-radius: 20px;
    border: 1px solid var(--line);
    color: var(--cyan) !important;
    text-transform: uppercase;
    transition: all .3s ease;
}
.brand-badge:hover {
    border-color: var(--cyan);
    background: rgba(0,229,255,.08);
    transform: translateY(-2px);
}

/* ── Nav section label ── */
.nav-section {
    font-family: var(--ff-mono);
    font-size: .58rem; letter-spacing: 3px; text-transform: uppercase;
    color: var(--muted) !important;
    padding: 0 20px 8px;
}

/* ── Radio nav pills ── */
[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: transparent !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    padding: 11px 16px !important;
    font-size: .82rem !important;
    transition: all .3s cubic-bezier(.34,1.56,.64,1) !important;
    position: relative; overflow: hidden;
}
[data-testid="stSidebar"] .stRadio label::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(0,229,255,.06), rgba(167,139,250,.04));
    transform: scaleX(0); transform-origin: left;
    transition: transform .3s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
    border-color: var(--line-h) !important;
    transform: translateX(6px) !important;
    box-shadow: 4px 0 16px var(--glow-c) !important;
}
[data-testid="stSidebar"] .stRadio label:hover::before { transform: scaleX(1); }

/* ── System status ── */
.sys-status {
    margin: 16px 12px 8px;
    background: rgba(0,0,0,.3);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 14px 16px;
}
.sys-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 5px 0; border-bottom: 1px solid rgba(0,229,255,.05);
}
.sys-row:last-child { border-bottom: none; }
.sys-key {
    font-family: var(--ff-mono);
    font-size: .6rem; letter-spacing: 1px; color: var(--muted) !important;
}
.sys-val {
    font-family: var(--ff-mono);
    font-size: .6rem; padding: 2px 8px;
    border-radius: 20px; border: 1px solid;
}
.sys-val.ok    { color: var(--emerald) !important; border-color: rgba(52,211,153,.3); background: rgba(52,211,153,.07); }
.sys-val.warn  { color: var(--amber)   !important; border-color: rgba(251,191,36,.3);  background: rgba(251,191,36,.07); }

/* ══════════════════════════════════════════════════════
   MASTER HEADER
══════════════════════════════════════════════════════ */
.master-header {
    position: relative;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    overflow: hidden;
    background: linear-gradient(135deg,
        rgba(0,229,255,.04) 0%,
        rgba(6,9,15,.97) 50%,
        rgba(167,139,250,.03) 100%);
    border: 1px solid var(--line);
    animation: headerreveal .8s ease forwards;
}
@keyframes headerreveal {
    0%   { opacity:0; transform: translateY(-10px); }
    100% { opacity:1; transform: translateY(0); }
}

/* Animated top rainbow bar */
.master-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        var(--violet), var(--cyan), var(--emerald), var(--amber), var(--rose), var(--violet));
    background-size: 300% 100%;
    animation: rainbowbar 5s linear infinite;
}
@keyframes rainbowbar { 0% { background-position: 0% 50%; } 100% { background-position: 300% 50%; } }

/* Bottom shimmer line */
.master-header::after {
    content: '';
    position: absolute; bottom: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--line-h), transparent);
}

.header-eyebrow {
    font-family: var(--ff-mono);
    font-size: .6rem; letter-spacing: 3px; text-transform: uppercase;
    color: var(--cyan); margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}
.header-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
    animation: dotblink 1.5s ease-in-out infinite;
}
@keyframes dotblink { 0%,100%{opacity:1} 50%{opacity:.2} }

.master-header h1 {
    font-family: var(--ff-display) !important;
    font-size: clamp(2.2rem, 4vw, 3.4rem) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -1px !important;
    color: var(--white) !important;
}
.master-header h1 span { color: var(--cyan) !important; }

.header-sub {
    font-size: .88rem; color: var(--dim); margin-top: 10px; line-height: 1.5;
}
.header-sub strong { color: var(--cyan); font-weight: 600; }

.header-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.header-tag {
    font-family: var(--ff-mono);
    font-size: .58rem; letter-spacing: 1.5px; text-transform: uppercase;
    padding: 5px 12px; border-radius: 20px; border: 1px solid;
    transition: all .3s ease;
    cursor: default;
}
.tag-cyan   { color: var(--cyan)    !important; border-color: rgba(0,229,255,.25);   background: rgba(0,229,255,.06); }
.tag-violet { color: var(--violet)  !important; border-color: rgba(167,139,250,.25); background: rgba(167,139,250,.06); }
.tag-rose   { color: var(--rose)    !important; border-color: rgba(251,113,133,.25); background: rgba(251,113,133,.06); }
.tag-emerald{ color: var(--emerald) !important; border-color: rgba(52,211,153,.25);  background: rgba(52,211,153,.06); }
/* Legacy aliases from original code */
.tag-red   { color: var(--cyan)    !important; border-color: rgba(0,229,255,.25);   background: rgba(0,229,255,.06); }
.tag-white { color: var(--violet)  !important; border-color: rgba(167,139,250,.25); background: rgba(167,139,250,.06); }

.header-tag:hover { transform: translateY(-3px) scale(1.06); }
.tag-cyan:hover   { box-shadow: 0 4px 16px var(--glow-c); }
.tag-violet:hover { box-shadow: 0 4px 16px var(--glow-v); }
.tag-rose:hover   { box-shadow: 0 4px 16px var(--glow-r); }
.tag-emerald:hover{ box-shadow: 0 4px 16px var(--glow-e); }
.tag-red:hover    { box-shadow: 0 4px 16px var(--glow-c); }
.tag-white:hover  { box-shadow: 0 4px 16px var(--glow-v); }

.header-time {
    font-family: var(--ff-mono);
    font-size: .7rem; color: var(--muted);
    text-align: right;
}

/* ══════════════════════════════════════════════════════
   MODEL BAR
══════════════════════════════════════════════════════ */
.model-bar {
    font-family: var(--ff-mono);
    font-size: .65rem; letter-spacing: 1px;
    padding: 10px 20px;
    background: rgba(0,229,255,.04);
    border: 1px solid var(--line);
    border-radius: 10px;
    margin-bottom: 20px;
    color: var(--dim) !important;
    position: relative; overflow: hidden;
}
.model-bar::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,.06), transparent);
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer { 0%{ left:-100%; } 100%{ left:200%; } }
.model-bar strong { color: var(--cyan) !important; }
.mbar-sep { color: var(--line-h) !important; margin: 0 8px; }

/* ══════════════════════════════════════════════════════
   CARDS
══════════════════════════════════════════════════════ */
.sec-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative; overflow: hidden;
    transition: border-color .4s ease, transform .4s cubic-bezier(.34,1.56,.64,1), box-shadow .4s ease;
    animation: cardappear .5s ease forwards;
}
@keyframes cardappear {
    0%   { opacity:0; transform: translateY(12px); }
    100% { opacity:1; transform: translateY(0); }
}
.sec-card:hover {
    border-color: var(--line-h);
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,.4), 0 0 0 1px var(--line-h);
}
/* Corner accent glow on hover */
.sec-card::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0; transition: opacity .4s;
}
.sec-card:hover::after { opacity: .7; }

.sec-title {
    font-family: var(--ff-mono) !important;
    font-size: .65rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--cyan) !important;
    margin-bottom: 20px !important;
}

/* ══════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,229,255,.12), rgba(167,139,250,.1)) !important;
    border: 1px solid rgba(0,229,255,.3) !important;
    color: var(--cyan) !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-family: var(--ff-mono) !important;
    font-size: .75rem !important;
    letter-spacing: 1.5px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    position: relative; overflow: hidden !important;
    transition: all .3s cubic-bezier(.34,1.56,.64,1) !important;
}
.stButton > button::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, var(--cyan), var(--violet));
    opacity: 0; transition: opacity .3s;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    color: var(--ink) !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 28px var(--glow-c), 0 0 0 1px var(--cyan) !important;
}
.stButton > button:hover::before { opacity: 1; }
.stButton > button:hover span { position: relative; z-index: 1; color: var(--ink) !important; }
.stButton > button:active {
    transform: translateY(0) scale(.98) !important;
}

/* ══════════════════════════════════════════════════════
   INPUTS / SELECTS / TEXTAREA
══════════════════════════════════════════════════════ */
.stTextInput input,
.stTextArea textarea {
    background: rgba(255,255,255,.03) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    color: var(--white) !important;
    font-family: var(--ff-body) !important;
    transition: border-color .3s, box-shadow .3s !important;
    caret-color: var(--cyan) !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,.1), 0 4px 20px rgba(0,0,0,.3) !important;
    background: rgba(0,229,255,.02) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,.03) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    color: var(--white) !important;
    transition: border-color .3s, box-shadow .3s !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--line-h) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,.3) !important;
}

/* Dropdown menu */
[data-baseweb="popover"] div,
[data-baseweb="menu"] {
    background: var(--panel) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
}
[data-baseweb="menu"] li:hover { background: rgba(0,229,255,.07) !important; }

/* ══════════════════════════════════════════════════════
   SLIDERS
══════════════════════════════════════════════════════ */
[data-testid="stSlider"] > div > div > div {
    background: rgba(0,229,255,.12) !important;
    border-radius: 4px !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--cyan), var(--violet)) !important;
    border-radius: 4px !important;
}
/* Thumb */
[data-testid="stSlider"] > div > div > div > div > div {
    background: var(--white) !important;
    border: 2px solid var(--cyan) !important;
    box-shadow: 0 0 12px var(--glow-c) !important;
    transition: transform .2s, box-shadow .2s !important;
}
[data-testid="stSlider"] > div > div > div > div > div:hover {
    transform: scale(1.2) !important;
    box-shadow: 0 0 20px var(--glow-c), 0 0 0 4px rgba(0,229,255,.15) !important;
}

/* ══════════════════════════════════════════════════════
   METRICS
══════════════════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all .4s cubic-bezier(.34,1.56,.64,1) !important;
    position: relative; overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    transform: scaleX(0); transition: transform .4s ease;
}
[data-testid="metric-container"]:hover {
    border-color: var(--line-h) !important;
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 32px rgba(0,0,0,.4) !important;
}
[data-testid="metric-container"]:hover::before { transform: scaleX(1); }

[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .72rem !important; letter-spacing: 1px !important; }
[data-testid="stMetricValue"] {
    color: var(--white) !important;
    font-family: var(--ff-display) !important;
    font-size: 1.9rem !important; font-weight: 800 !important;
}
[data-testid="stMetricDelta"] { font-family: var(--ff-mono) !important; font-size: .7rem !important; }

/* ══════════════════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: rgba(0,229,255,.025) !important;
    border: 1.5px dashed rgba(0,229,255,.25) !important;
    border-radius: 14px !important;
    transition: all .3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    background: rgba(0,229,255,.04) !important;
    border-color: rgba(0,229,255,.5) !important;
    box-shadow: 0 0 24px var(--glow-c) !important;
}

/* ══════════════════════════════════════════════════════
   FORMS
══════════════════════════════════════════════════════ */
[data-testid="stForm"] {
    background: rgba(0,229,255,.02) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}

/* ══════════════════════════════════════════════════════
   RESULT BANNERS
══════════════════════════════════════════════════════ */
.result-banner {
    border-radius: 14px;
    padding: 20px 24px;
    margin: 16px 0;
    display: flex; align-items: flex-start; gap: 16px;
    animation: bannerslide .5s cubic-bezier(.34,1.56,.64,1) forwards;
    position: relative; overflow: hidden;
}
@keyframes bannerslide {
    0%   { opacity:0; transform: translateX(-16px); }
    100% { opacity:1; transform: translateX(0); }
}
.result-banner::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.015), transparent);
    animation: shimmer 3s linear infinite;
}
.banner-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.banner-body h3 {
    font-family: var(--ff-display) !important;
    font-size: 1rem !important; font-weight: 700 !important;
    margin-bottom: 4px !important;
}
.banner-body p { font-size: .83rem !important; line-height: 1.5 !important; }

.banner-danger {
    background: rgba(0,229,255,.05);
    border: 1px solid rgba(0,229,255,.25);
    border-left: 3px solid var(--cyan);
}
.banner-danger .banner-body h3 { color: var(--cyan) !important; }

.banner-ok {
    background: rgba(52,211,153,.06);
    border: 1px solid rgba(52,211,153,.25);
    border-left: 3px solid var(--emerald);
}
.banner-ok .banner-body h3 { color: var(--emerald) !important; }

.banner-warn {
    background: rgba(251,191,36,.05);
    border: 1px solid rgba(251,191,36,.25);
    border-left: 3px solid var(--amber);
}
.banner-warn .banner-body h3 { color: var(--amber) !important; }

/* ══════════════════════════════════════════════════════
   GAUGE WRAPPER (centering + glow)
══════════════════════════════════════════════════════ */
.gauge-wrap {
    display: flex; justify-content: center; align-items: center;
    padding: 10px 0;
    filter: drop-shadow(0 0 18px var(--glow-c));
    animation: gaugein .7s cubic-bezier(.34,1.56,.64,1) forwards;
}
@keyframes gaugein {
    0%   { opacity:0; transform: scale(.8); }
    100% { opacity:1; transform: scale(1); }
}

/* ══════════════════════════════════════════════════════
   HISTORY ITEMS
══════════════════════════════════════════════════════ */
.hist-item {
    display: flex; align-items: center; gap: 14px;
    padding: 13px 16px;
    border-radius: 12px;
    background: rgba(255,255,255,.018);
    border: 1px solid var(--line);
    margin-bottom: 8px;
    transition: all .35s cubic-bezier(.34,1.56,.64,1);
    cursor: default;
    position: relative; overflow: hidden;
}
.hist-item::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0; width: 2px;
    background: linear-gradient(180deg, var(--cyan), var(--violet));
    transform: scaleY(0); transition: transform .35s ease;
}
.hist-item:hover {
    background: rgba(0,229,255,.04);
    border-color: var(--line-h);
    transform: translateX(6px);
    box-shadow: 4px 0 20px var(--glow-c);
}
.hist-item:hover::before { transform: scaleY(1); }

.hist-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,229,255,.07);
    border: 1px solid rgba(0,229,255,.18);
    font-size: 1.1rem;
    transition: transform .3s;
}
.hist-item:hover .hist-icon { transform: scale(1.12) rotate(-6deg); }

.hist-label {
    font-weight: 600; font-size: .82rem;
    color: var(--white) !important;
}
.hist-detail {
    font-family: var(--ff-mono);
    font-size: .6rem; color: var(--muted) !important;
    margin-top: 2px;
}
.hist-prob {
    font-family: var(--ff-display);
    font-size: 1.1rem; font-weight: 800;
}
.hist-badge {
    font-family: var(--ff-mono);
    font-size: .55rem; letter-spacing: 1px; text-transform: uppercase;
    padding: 3px 9px; border-radius: 20px; border: 1px solid;
}
.badge-hi   { color: var(--cyan)    !important; border-color: rgba(0,229,255,.3); }
.badge-mod  { color: var(--amber)   !important; border-color: rgba(251,191,36,.3); }
.badge-lo   { color: var(--emerald) !important; border-color: rgba(52,211,153,.3); }
.hist-time {
    font-family: var(--ff-mono);
    font-size: .58rem; color: var(--muted) !important;
    margin-left: 4px;
}

/* ══════════════════════════════════════════════════════
   CHAT BUBBLES
══════════════════════════════════════════════════════ */
.chat-user, .chat-ai {
    display: flex; margin-bottom: 16px;
    animation: bubblein .4s ease forwards;
}
@keyframes bubblein {
    0%   { opacity:0; transform: translateY(10px); }
    100% { opacity:1; transform: translateY(0); }
}
.chat-user { justify-content: flex-end; }
.chat-ai   { justify-content: flex-start; }

.bubble-label {
    font-family: var(--ff-mono);
    font-size: .58rem; letter-spacing: 1.5px;
    text-transform: uppercase;
    display: block; margin-bottom: 5px;
}
.label-user { color: var(--cyan)   !important; text-align: right; }
.label-ai   { color: var(--violet) !important; }

.bubble-user {
    background: rgba(0,229,255,.08);
    border: 1px solid rgba(0,229,255,.25);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px; max-width: 75%;
    font-size: .87rem; line-height: 1.55;
    color: var(--white) !important;
    transition: box-shadow .3s;
}
.bubble-user:hover { box-shadow: 0 4px 20px var(--glow-c); }

.bubble-ai {
    background: rgba(167,139,250,.06);
    border: 1px solid rgba(167,139,250,.2);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px; max-width: 80%;
    font-size: .87rem; line-height: 1.55;
    color: var(--white) !important;
    transition: box-shadow .3s;
}
.bubble-ai:hover { box-shadow: 0 4px 20px var(--glow-v); }

.chat-empty {
    text-align: center;
    padding: 56px 24px;
    color: var(--muted) !important;
    font-size: .88rem; line-height: 1.7;
    border: 1px dashed var(--line);
    border-radius: 16px;
    animation: fadein 1s ease;
}
.chat-empty span { font-size: 2.5rem; display: block; margin-bottom: 12px; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

/* ══════════════════════════════════════════════════════
   SOURCE CHIPS
══════════════════════════════════════════════════════ */
.source-chip {
    display: inline-block;
    font-family: var(--ff-mono);
    font-size: .58rem; letter-spacing: .5px;
    padding: 4px 10px; margin: 3px 4px 3px 0;
    border-radius: 20px;
    background: rgba(0,229,255,.06);
    border: 1px solid rgba(0,229,255,.2);
    color: var(--cyan) !important;
    transition: all .25s ease;
}
.source-chip:hover {
    background: rgba(0,229,255,.12);
    transform: translateY(-2px);
}

/* ══════════════════════════════════════════════════════
   NLP ENTITIES
══════════════════════════════════════════════════════ */
.entity-group { margin-bottom: 14px; }
.entity-label {
    font-family: var(--ff-mono);
    font-size: .6rem; letter-spacing: 2px; text-transform: uppercase;
    color: var(--muted) !important;
    margin-bottom: 8px;
}
.entity-tag {
    display: inline-block;
    padding: 5px 13px; border-radius: 20px;
    font-size: .72rem; font-weight: 500;
    margin: 4px 5px 4px 0;
    cursor: default;
    transition: all .25s cubic-bezier(.34,1.56,.64,1);
}
.entity-tag:hover { transform: translateY(-3px) scale(1.06); }

.tag-DISEASE  { background:rgba(0,229,255,.09); color: var(--cyan)    !important; border:1px solid rgba(0,229,255,.25); }
.tag-SYMPTOM  { background:rgba(251,191,36,.07); color: var(--amber)   !important; border:1px solid rgba(251,191,36,.25); }
.tag-MEDICATION{ background:rgba(52,211,153,.08); color: var(--emerald) !important; border:1px solid rgba(52,211,153,.25); }
.tag-ANATOMY  { background:rgba(167,139,250,.08);color: var(--violet)  !important; border:1px solid rgba(167,139,250,.25); }
.tag-VITAL    { background:rgba(251,113,133,.08); color: var(--rose)    !important; border:1px solid rgba(251,113,133,.25); }

.tag-DISEASE:hover   { box-shadow: 0 4px 14px var(--glow-c); }
.tag-SYMPTOM:hover   { box-shadow: 0 4px 14px rgba(251,191,36,.2); }
.tag-MEDICATION:hover{ box-shadow: 0 4px 14px var(--glow-e); }
.tag-ANATOMY:hover   { box-shadow: 0 4px 14px var(--glow-v); }
.tag-VITAL:hover     { box-shadow: 0 4px 14px var(--glow-r); }

/* ══════════════════════════════════════════════════════
   ANNOTATED TEXT
══════════════════════════════════════════════════════ */
.annotated-text {
    font-family: var(--ff-body) !important;
    font-size: .88rem; line-height: 1.8;
    color: var(--dim) !important;
    background: rgba(0,0,0,.2);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px;
}

/* ══════════════════════════════════════════════════════
   EXPANDERS
══════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.018) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    transition: border-color .3s !important;
}
[data-testid="stExpander"]:hover { border-color: var(--line-h) !important; }

/* ══════════════════════════════════════════════════════
   SPINNER
══════════════════════════════════════════════════════ */
.stSpinner > div {
    border-color: var(--cyan) transparent transparent transparent !important;
    animation-duration: .7s !important;
}

/* ══════════════════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--cyan), var(--violet)) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 10px var(--glow-c) !important;
}

/* ══════════════════════════════════════════════════════
   ALERTS / INFO / WARNING / ERROR
══════════════════════════════════════════════════════ */
.stAlert { border-radius: 12px !important; }
[data-testid="stNotification"] { border-radius: 12px !important; }

/* ══════════════════════════════════════════════════════
   MATPLOTLIB / PYPLOT CHARTS (dark canvas)
══════════════════════════════════════════════════════ */
[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid var(--line);
    transition: all .4s ease;
}
[data-testid="stImage"] img:hover {
    border-color: var(--line-h);
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
}

/* ══════════════════════════════════════════════════════
   COLUMNS DIVIDER FIX
══════════════════════════════════════════════════════ */
[data-testid="column"] { animation: colreveal .6s ease forwards; }
@keyframes colreveal {
    0%   { opacity:0; transform: translateY(8px); }
    100% { opacity:1; transform: translateY(0); }
}

/* ══════════════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════════════ */
.footer {
    text-align: center;
    font-family: var(--ff-mono) !important;
    font-size: .58rem !important;
    letter-spacing: 2px !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    padding: 28px 0 16px;
    border-top: 1px solid var(--line);
    margin-top: 40px;
    position: relative;
}
.footer::before {
    content: '';
    position: absolute; top: 0; left: 20%; right: 20%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    animation: footerbar 6s ease-in-out infinite;
}
@keyframes footerbar {
    0%,100% { opacity:.3; left:20%; right:20%; }
    50%      { opacity:.9; left:10%; right:10%; }
}

/* ══════════════════════════════════════════════════════
   UTILITY ANIMATIONS
══════════════════════════════════════════════════════ */
@keyframes fadein { 0%{opacity:0} 100%{opacity:1} }


/* ══════════════════════════════════════════════════════
   SIDEBAR VISIBILITY FIXES
══════════════════════════════════════════════════════ */

/* Ensure sidebar itself is always visible */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Fix the sidebar toggle/collapse button that header:hidden kills */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[kind="header"] {
    visibility: visible !important;
    display: flex !important;
}

/* Make sure sidebar children are visible */
[data-testid="stSidebar"] > div {
    visibility: visible !important;
    opacity: 1 !important;
}
</style>
"""
