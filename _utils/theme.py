# ─────────────────────────────────────────────────────────────────────────────
#  CSS — Dark Pit Wall Theme
#  Call inject_css() once at the top of app.py
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st


def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #12121a;
    border-right: 1px solid #2a2a3a;
}
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: #1a1a26 !important;
    border: 1px solid #2a2a3a !important;
    color: #e8e8f0 !important;
}

/* ── Primary Button ── */
[data-testid="stButton"] > button {
    background: #e10600;
    color: #fff;
    border: none;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    width: 100%;
    padding: .6rem;
    border-radius: 3px;
    transition: background .2s;
}
[data-testid="stButton"] > button:hover { background: #ff1a0e; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #1a1a26;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: .75rem 1rem;
    border-top: 2px solid #e10600;
}
[data-testid="metric-container"] label {
    font-size: .7rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6a6a8a !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.4rem !important;
    color: #fff !important;
}

/* ── Headings ── */
h1 { color: #e10600 !important; font-weight: 700 !important; letter-spacing: 3px; }
h2, h3 { color: #e8e8f0 !important; letter-spacing: 1px; }
hr { border-color: #2a2a3a; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: .85rem;
    color: #6a6a8a;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #e10600 !important;
    border-bottom-color: #e10600 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #1a1a26;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
}

/* ── Plotly transparent bg ── */
.js-plotly-plot { background: transparent !important; }

/* ── Live badge ── */
.live-badge {
    display: inline-block;
    background: #e10600;
    color: white;
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 2px;
    animation: livepulse 1.2s infinite;
    vertical-align: middle;
    margin-left: .5rem;
}
@keyframes livepulse { 0%,100%{ opacity:1 } 50%{ opacity:.4 } }

/* ── Timing tower table ── */
.pos-table { width: 100%; border-collapse: collapse; font-size: .85rem; }
.pos-table th {
    background: #1a1a26;
    color: #6a6a8a;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: .7rem;
    padding: .4rem .6rem;
    border-bottom: 1px solid #2a2a3a;
    text-align: left;
}
.pos-table td {
    padding: .35rem .6rem;
    border-bottom: 1px solid #1a1a26;
    font-family: 'Share Tech Mono', monospace;
    font-size: .82rem;
}
.pos-table tr:hover td { background: #1a1a26; }
.pos-1 { color: #ffd700; font-weight: 700; }
.pos-2 { color: #c0c0c0; }
.pos-3 { color: #cd7f32; }

/* ── Radio message card ── */
.radio-card {
    background: #12121a;
    border: 1px solid #2a2a3a;
    border-left: 3px solid var(--rc, #e10600);
    border-radius: 4px;
    padding: .5rem .9rem;
    margin: .3rem 0;
    font-size: .85rem;
}
.radio-time   { font-family: 'Share Tech Mono', monospace; font-size: .7rem; color: #6a6a8a; }
.radio-driver { font-weight: 700; font-size: .9rem; }
.radio-msg    { color: #c8c8d8; font-size: .82rem; margin-top: .15rem; font-style: italic; }

/* ── News Feed — Social Style ── */
.news-card {
    background: #0a0a14;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    margin-bottom: 1.8rem;
    overflow: hidden;
    transition: border-color .25s, box-shadow .25s, transform .2s;
    cursor: pointer;
    box-shadow: 0 4px 24px rgba(0,0,0,.5);
}
.news-card:hover {
    border-color: #e10600;
    box-shadow: 0 6px 36px rgba(225,6,0,.2);
    transform: translateY(-3px);
}
.news-img { width: 100%; height: 230px; object-fit: cover; display: block; }
.news-img-placeholder {
    width: 100%; height: 180px;
    background: linear-gradient(135deg, #1a0808 0%, #080814 50%, #0a1a08 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 3rem; letter-spacing: 6px;
}
.news-body { padding: 1.1rem 1.3rem 1.2rem; }
.news-source-badge {
    display: inline-block;
    background: rgba(225,6,0,.13);
    color: #e10600;
    border: 1px solid rgba(225,6,0,.3);
    font-size: .58rem; font-weight: 700; letter-spacing: 1.8px;
    text-transform: uppercase; padding: 2px 9px; border-radius: 20px;
}
.news-date  { font-size: .6rem; color: #3a3a58; font-family: 'Share Tech Mono', monospace; }
.news-title { font-size: 1.12rem; font-weight: 700; color: #f0f0ff; margin: .4rem 0 .5rem; line-height: 1.4; }
.news-desc  { font-size: .84rem; color: #7a7a9a; line-height: 1.6; }
.news-footer {
    display: flex; justify-content: flex-end;
    margin-top: .8rem; padding-top: .65rem; border-top: 1px solid #1a1a2c;
}
.news-read-more {
    font-size: .7rem; color: #e10600; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
}

/* ── Engineering card ── */
.eng-card {
    background: #1a1a26;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: .75rem 1rem;
    margin-bottom: .6rem;
    border-left: 3px solid var(--ac, #e10600);
}
.eng-title { color: #e10600; font-weight: 700; font-size: .95rem; text-transform: uppercase; letter-spacing: .5px; }
.eng-sub   { color: #6a6a8a; font-size: .72rem; margin: .15rem 0; }
.eng-body  { color: #c8c8d8; font-size: .82rem; line-height: 1.5; }
</style>
    """, unsafe_allow_html=True)
