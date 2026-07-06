"""
╔══════════════════════════════════════════════════════════════════╗
║  F1 PIT WALL  —  Telemetry & Race Intelligence Dashboard         ║
║  FastF1 (historical) + OpenF1 API (live, ~3-5s delay)           ║
║                                                                  ║
║  Run:  streamlit run app.py                                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
#  PATH BOOTSTRAP — executado antes de qualquer import do projeto
# ─────────────────────────────────────────────────────────────────────────────
import sys
import os

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))

# Garante que a raiz do projeto está no sys.path
sys.path = [p for p in sys.path if p != _THIS_DIR]
sys.path.insert(0, _THIS_DIR)

# Detecta automaticamente se as pastas usam prefixo "_" ou não
# (compatível antes e depois de rodar corrigir_menu.py)
def _resolve_pkg(name):
    """Retorna '_name' se existir, senão 'name'. Cria __init__.py se faltar."""
    for candidate in (f"_{name}", name):
        pkg_dir = os.path.join(_THIS_DIR, candidate)
        if os.path.isdir(pkg_dir):
            init = os.path.join(pkg_dir, "__init__.py")
            if not os.path.exists(init):
                open(init, "w").close()
            return candidate
    # Nenhum encontrado: cria a pasta sem prefixo
    pkg_dir = os.path.join(_THIS_DIR, name)
    os.makedirs(pkg_dir, exist_ok=True)
    open(os.path.join(pkg_dir, "__init__.py"), "w").close()
    return name

UTILS      = _resolve_pkg("utils")
DATA       = _resolve_pkg("data")
PAGES      = _resolve_pkg("pages")
COMPONENTS = _resolve_pkg("components")

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS DO PROJETO
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import importlib

def _import(pkg_var, module, symbol=None):
    """Import dinâmico: usa o nome de pasta resolvido acima."""
    mod = importlib.import_module(f"{pkg_var}.{module}")
    return getattr(mod, symbol) if symbol else mod

inject_css      = _import(UTILS, "theme",     "inject_css")
DRIVER_NUMBER_MAP = _import(UTILS, "constants", "DRIVER_NUMBER_MAP")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="F1 Pit Wall",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_defaults = {
    "session":            None,
    "drivers":            [],
    "last_selection":     None,
    "live_refresh_count": 0,
    "replay_playing":     False,
    "replay_t":           0.0,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🏎️ F1 PIT WALL")
    st.markdown("---")

    mode = st.radio(
        "Mode",
        ["🏠 Home", "📊 Historical Analysis", "🔴 Live Mode", "📰 F1 News 2026", "🎓 English Study"],
        label_visibility="collapsed",
    )

    is_home  = mode == "🏠 Home"
    is_hist  = mode == "📊 Historical Analysis"
    is_live  = mode == "🔴 Live Mode"
    is_news  = mode == "📰 F1 News 2026"
    is_study = mode == "🎓 English Study"

    st.markdown("---")

    if is_hist:
        year    = st.selectbox("📅 Season", [2025, 2024, 2023, 2022], index=0)
        gp_name = st.selectbox("🏁 Grand Prix", [
            "Australia", "China", "Japan", "Bahrain", "Saudi Arabia",
            "Miami", "Emilia Romagna", "Monaco", "Spain", "Canada",
            "Austria", "Great Britain", "Belgium", "Hungary",
            "Netherlands", "Italy", "Azerbaijan", "Singapore",
            "United States", "Mexico City", "São Paulo", "Las Vegas",
            "Qatar", "Abu Dhabi",
        ], index=0)
        session_type = st.selectbox("⏱️ Session", [
            "Qualifying", "Race", "Sprint", "Practice 1", "Practice 2", "Practice 3",
        ])
        session_code = {
            "Qualifying": "Q", "Race": "R", "Sprint": "S",
            "Practice 1": "FP1", "Practice 2": "FP2", "Practice 3": "FP3",
        }[session_type]
        analyze = st.button("▶  ANALYZE")

    elif is_live:
        st.markdown("### 🔴 Live Mode")
        st.markdown("Powered by **OpenF1 API** · ~3–5s delay")
        refresh_interval = st.selectbox("Auto-refresh every", ["5s", "10s", "20s", "30s"], index=1)
        live_filter      = st.multiselect(
            "Track drivers (empty = all)",
            list(DRIVER_NUMBER_MAP.values()),
            default=["VER", "NOR"],
        )

    elif is_study:
        st.markdown("### 🎓 English Study")
        st.markdown("Team radio · Interviews · Race phrases")
    elif is_home:
        st.markdown("### 🏠 Dashboard")
        st.markdown("F1 Pit Wall — Race Intelligence")
    else:
        st.markdown("### 📰 F1 News 2026")

    st.markdown("---")
    st.markdown("**FastF1** historical · **OpenF1** live · **RSS** news")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
hc1, hc2 = st.columns([3, 1])
with hc1:
    if is_live:
        st.markdown('# F1 PIT WALL <span class="live-badge">LIVE</span>', unsafe_allow_html=True)
        st.markdown("##### `OpenF1 · Real-Time Feed`")
    elif is_news:
        st.markdown("# F1 PIT WALL")
        st.markdown("##### `📰 F1 2026 · Latest News`")
    elif is_study:
        st.markdown("# F1 PIT WALL")
        st.markdown("##### `🎓 English Study — Radio & Interviews`")
    elif is_home:
        st.markdown(
            '# F1 PIT WALL <span style="font-size:.9rem;color:#6a6a8a;letter-spacing:2px"> · DASHBOARD</span>',
            unsafe_allow_html=True,
        )
        st.markdown("##### `Race Intelligence · Season 2026`")
    else:
        st.markdown("# F1 PIT WALL")
        st.markdown(f"##### `{year} · {gp_name} · {session_type}`")

with hc2:
    src = (
        "OpenF1 · Streamlit"          if is_live
        else "RSS Feeds · Streamlit"  if is_news
        else "English Study · F1"     if is_study
        else "Home · F1 2026"         if is_home
        else "FastF1 · Plotly · Streamlit"
    )
    st.markdown(
        f'<div style="text-align:right;font-family:Share Tech Mono,monospace;'
        f'font-size:.8rem;color:#6a6a8a;margin-top:1.5rem">{src}</div>',
        unsafe_allow_html=True,
    )
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  ROUTING — import dinâmico usando o nome de pasta resolvido
# ─────────────────────────────────────────────────────────────────────────────
if is_home:
    render = _import(PAGES, "home", "render")
    render()

elif is_news:
    render = _import(PAGES, "news", "render")
    render()

elif is_study:
    render = _import(PAGES, "english_study", "render")
    render()

elif is_live:
    render = _import(PAGES, "live_mode", "render")
    render(live_filter=live_filter, refresh_interval=refresh_interval)

else:
    render = _import(PAGES, "historical", "render")
    render(
        year         = year,
        gp_name      = gp_name,
        session_type = session_type,
        session_code = session_code,
        analyze      = analyze,
    )
# updated seg 06 jul 2026 20:18:57 -03
