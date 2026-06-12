# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: Home — season overview, standings, calendar com detalhes por GP
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from datetime import datetime as _dt
from _utils.constants import DRIVER_COLORS, DRIVER_TEAMS
from _data.season_data import get_season_data

# ─────────────────────────────────────────────────────────────────────────────
#  DADOS DOS GPs — horários locais (CEST/fuso do circuito) e resultados
# ─────────────────────────────────────────────────────────────────────────────
GP_DETAILS = {
    "Australian GP": {
        "sessions": [
            ("FP1",        "Sex 14 Mar", "01:30"),
            ("FP2",        "Sex 14 Mar", "05:00"),
            ("FP3",        "Sáb 15 Mar", "01:30"),
            ("Qualifying", "Sáb 15 Mar", "05:00"),
            ("Race",       "Dom 16 Mar", "01:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "NOR", "fl": "ANT", "fl_time": "1:17.456"},
    },
    "Chinese GP": {
        "sessions": [
            ("FP1",          "Sex 21 Mar", "00:30"),
            ("Sprint Quali", "Sex 21 Mar", "04:30"),
            ("Sprint",       "Sáb 22 Mar", "00:00"),
            ("Qualifying",   "Sáb 22 Mar", "04:00"),
            ("Race",         "Dom 23 Mar", "04:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "NOR", "fl": "ANT", "fl_time": "1:32.145"},
    },
    "Japanese GP": {
        "sessions": [
            ("FP1",        "Sex 04 Abr", "23:30"),
            ("FP2",        "Sex 04 Abr", "03:00"),
            ("FP3",        "Sáb 05 Abr", "23:30"),
            ("Qualifying", "Dom 06 Abr", "03:00"),
            ("Race",       "Dom 06 Abr", "02:00"),
        ],
        "result": {"winner": "ANT", "p2": "HAM", "p3": "LEC", "fl": "HAM", "fl_time": "1:30.983"},
    },
    "Miami GP": {
        "sessions": [
            ("FP1",          "Sex 02 Mai", "13:30"),
            ("Sprint Quali", "Sex 02 Mai", "17:30"),
            ("Sprint",       "Sáb 03 Mai", "13:00"),
            ("Qualifying",   "Sáb 03 Mai", "17:00"),
            ("Race",         "Dom 04 Mai", "17:00"),
        ],
        "result": {"winner": "ANT", "p2": "PIA", "p3": "NOR", "fl": "RUS", "fl_time": "1:27.341"},
    },
    "Canadian GP": {
        "sessions": [
            ("FP1",          "Sex 06 Jun", "14:30"),
            ("Sprint Quali", "Sex 06 Jun", "18:30"),
            ("Sprint",       "Sáb 07 Jun", "14:00"),
            ("Qualifying",   "Sáb 07 Jun", "18:00"),
            ("Race",         "Dom 08 Jun", "15:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "HAM", "fl": "ANT", "fl_time": "1:13.702"},
    },
    "Monaco GP": {
        "sessions": [
            ("FP1",        "Qui 22 Mai", "06:30"),
            ("FP2",        "Qui 22 Mai", "10:00"),
            ("FP3",        "Sáb 24 Mai", "06:30"),
            ("Qualifying", "Sáb 24 Mai", "10:00"),
            ("Race",       "Dom 25 Mai", "10:00"),
        ],
        "result": {"winner": "ANT", "p2": "HAM", "p3": "HAD", "fl": "ANT", "fl_time": "1:12.803"},
    },
    "Barcelona GP": {
        "sessions": [
            ("FP1",        "Sex 12 Jun", "08:30"),
            ("FP2",        "Sex 12 Jun", "12:00"),
            ("FP3",        "Sáb 13 Jun", "07:30"),
            ("Qualifying", "Sáb 13 Jun", "11:00"),
            ("Race",       "Dom 14 Jun", "10:00"),
        ],
        "result": None,
    },
    "Austrian GP": {
        "sessions": [
            ("FP1",        "Sex 26 Jun", "08:30"),
            ("FP2",        "Sex 26 Jun", "12:00"),
            ("FP3",        "Sáb 27 Jun", "07:30"),
            ("Qualifying", "Sáb 27 Jun", "11:00"),
            ("Race",       "Dom 28 Jun", "10:00"),
        ],
        "result": None,
    },
    "British GP": {
        "sessions": [
            ("FP1",          "Sex 03 Jul", "09:30"),
            ("Sprint Quali", "Sex 03 Jul", "13:30"),
            ("Sprint",       "Sáb 04 Jul", "08:30"),
            ("Qualifying",   "Sáb 04 Jul", "12:00"),
            ("Race",         "Dom 05 Jul", "11:00"),
        ],
        "result": None,
    },
    "Belgian GP": {
        "sessions": [
            ("FP1",        "Sex 17 Jul", "08:30"),
            ("FP2",        "Sex 17 Jul", "12:00"),
            ("FP3",        "Sáb 18 Jul", "07:30"),
            ("Qualifying", "Sáb 18 Jul", "11:00"),
            ("Race",       "Dom 19 Jul", "10:00"),
        ],
        "result": None,
    },
    "Hungarian GP": {
        "sessions": [
            ("FP1",        "Sex 24 Jul", "08:30"),
            ("FP2",        "Sex 24 Jul", "12:00"),
            ("FP3",        "Sáb 25 Jul", "07:30"),
            ("Qualifying", "Sáb 25 Jul", "11:00"),
            ("Race",       "Dom 26 Jul", "10:00"),
        ],
        "result": None,
    },
    "Dutch GP": {
        "sessions": [
            ("FP1",          "Sex 21 Ago", "07:30"),
            ("Sprint Quali", "Sex 21 Ago", "11:30"),
            ("Sprint",       "Sáb 22 Ago", "07:00"),
            ("Qualifying",   "Sáb 22 Ago", "11:00"),
            ("Race",         "Dom 23 Ago", "10:00"),
        ],
        "result": None,
    },
    "Italian GP": {
        "sessions": [
            ("FP1",        "Sex 04 Set", "08:30"),
            ("FP2",        "Sex 04 Set", "12:00"),
            ("FP3",        "Sáb 05 Set", "07:30"),
            ("Qualifying", "Sáb 05 Set", "11:00"),
            ("Race",       "Dom 06 Set", "10:00"),
        ],
        "result": None,
    },
    "Madrid GP": {
        "sessions": [
            ("FP1",        "Sex 11 Set", "08:30"),
            ("FP2",        "Sex 11 Set", "12:00"),
            ("FP3",        "Sáb 12 Set", "07:30"),
            ("Qualifying", "Sáb 12 Set", "11:00"),
            ("Race",       "Dom 13 Set", "10:00"),
        ],
        "result": None,
    },
    "Azerbaijan GP": {
        "sessions": [
            ("FP1",        "Sex 25 Set", "06:30"),
            ("FP2",        "Sex 25 Set", "10:00"),
            ("FP3",        "Sáb 26 Set", "05:30"),
            ("Qualifying", "Sáb 26 Set", "09:00"),
            ("Race",       "Dom 27 Set", "07:00"),
        ],
        "result": None,
    },
    "Singapore GP": {
        "sessions": [
            ("FP1",          "Sex 09 Out", "06:30"),
            ("Sprint Quali", "Sex 09 Out", "10:30"),
            ("Sprint",       "Sáb 10 Out", "06:00"),
            ("Qualifying",   "Sáb 10 Out", "10:00"),
            ("Race",         "Dom 11 Out", "09:00"),
        ],
        "result": None,
    },
    "United States GP": {
        "sessions": [
            ("FP1",        "Sex 23 Out", "21:30"),
            ("FP2",        "Sex 23 Out", "01:00"),
            ("FP3",        "Sáb 24 Out", "21:30"),
            ("Qualifying", "Dom 25 Out", "01:00"),
            ("Race",       "Dom 25 Out", "23:00"),
        ],
        "result": None,
    },
    "Mexico City GP": {
        "sessions": [
            ("FP1",        "Sex 30 Out", "21:30"),
            ("FP2",        "Sex 30 Out", "01:00"),
            ("FP3",        "Sáb 31 Out", "20:30"),
            ("Qualifying", "Dom 01 Nov", "00:00"),
            ("Race",       "Dom 01 Nov", "23:00"),
        ],
        "result": None,
    },
    "São Paulo GP": {
        "sessions": [
            ("FP1",        "Sex 06 Nov", "15:30"),
            ("FP2",        "Sex 06 Nov", "19:00"),
            ("FP3",        "Sáb 07 Nov", "14:30"),
            ("Qualifying", "Sáb 07 Nov", "18:00"),
            ("Race",       "Dom 08 Nov", "17:00"),
        ],
        "result": None,
    },
    "Las Vegas GP": {
        "sessions": [
            ("FP1",        "Qui 19 Nov", "09:30"),
            ("FP2",        "Qui 19 Nov", "13:00"),
            ("FP3",        "Sex 20 Nov", "09:30"),
            ("Qualifying", "Sex 20 Nov", "13:00"),
            ("Race",       "Sáb 21 Nov", "11:00"),
        ],
        "result": None,
    },
    "Qatar GP": {
        "sessions": [
            ("FP1",        "Sex 27 Nov", "11:30"),
            ("FP2",        "Sex 27 Nov", "15:00"),
            ("FP3",        "Sáb 28 Nov", "11:30"),
            ("Qualifying", "Sáb 28 Nov", "15:00"),
            ("Race",       "Dom 29 Nov", "12:00"),
        ],
        "result": None,
    },
    "Abu Dhabi GP": {
        "sessions": [
            ("FP1",        "Sex 04 Dez", "06:30"),
            ("FP2",        "Sex 04 Dez", "10:00"),
            ("FP3",        "Sáb 05 Dez", "06:30"),
            ("Qualifying", "Sáb 05 Dez", "10:00"),
            ("Race",       "Dom 06 Dez", "10:00"),
        ],
        "result": None,
    },
}

SESSION_ICONS = {
    "FP1": "🔵", "FP2": "🔵", "FP3": "🔵",
    "Sprint Quali": "🟡", "Sprint": "🟠",
    "Qualifying": "🟣", "Race": "🔴",
}

SESSION_COLORS = {
    "FP1": "#2293D1", "FP2": "#2293D1", "FP3": "#2293D1",
    "Sprint Quali": "#ffd700", "Sprint": "#ff8000",
    "Qualifying": "#a020f0", "Race": "#e10600",
}


def render():
    _drv_st, _con_st, _cal, _lr = get_season_data()

    next_gp    = next((r for r in _cal if r[4] == "next"), None)
    done_count = sum(1 for r in _cal if r[4] == "done")
    total      = len(_cal)

    # ── Hero banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a0a0f 0%,#1a0808 50%,#0a0a14 100%);
                border:1px solid #2a2a3a;border-radius:14px;padding:2.5rem 2.5rem 2rem;
                margin-bottom:1.5rem;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#e10600,#ff8000,#e10600)"></div>
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem">
            <div>
                <div style="font-size:.7rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:3px;margin-bottom:.4rem">
                    Formula 1 · Season 2026
                </div>
                <div style="font-size:2.8rem;font-weight:700;color:#fff;letter-spacing:2px;line-height:1">
                    F1 PIT WALL
                </div>
                <div style="font-size:1rem;color:#9a9ab0;margin-top:.5rem">
                    Race Intelligence Dashboard · FastF1 + OpenF1
                </div>
            </div>
            <div style="text-align:right">
                <div style="font-size:.65rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:2px">Season Progress</div>
                <div style="font-family:Share Tech Mono,monospace;font-size:2rem;color:#e10600;font-weight:700">
                    {done_count} / {total}
                </div>
                <div style="font-size:.75rem;color:#6a6a8a">races completed</div>
                <div style="background:#1a1a26;border-radius:4px;height:6px;width:200px;margin:.4rem 0 0 auto;overflow:hidden">
                    <div style="background:linear-gradient(90deg,#e10600,#ff4400);height:100%;
                                width:{round(done_count / total * 100)}%;border-radius:4px"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Next GP + Last race
    col_next, col_last = st.columns(2)
    with col_next:
        if next_gp:
            rnd, name, circuit, date_str, _, _sprint = next_gp
            try:
                race_date = _dt.strptime(date_str, "%Y-%m-%d")
                days_left = (race_date - _dt.now()).days
                days_txt  = f"{days_left} days away" if days_left > 0 else "This weekend!"
            except Exception:
                days_txt = date_str
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #e10600;border-radius:12px;padding:1.3rem 1.4rem;height:100%">
                <div style="font-size:.62rem;color:#e10600;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:.5rem">
                    ▶ NEXT RACE — Round {rnd}
                </div>
                <div style="font-size:1.5rem;font-weight:700;color:#fff;line-height:1.2">{name}</div>
                <div style="font-size:.85rem;color:#9a9ab0;margin:.3rem 0">{circuit}</div>
                <div style="display:flex;gap:1rem;margin-top:.8rem;flex-wrap:wrap">
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px">Date</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:.95rem;color:#fff">{date_str}</div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px">Countdown</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:.95rem;color:#ffd700">{days_txt}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_last:
        lr      = _lr
        w_color = DRIVER_COLORS.get(lr["winner"], "#ffffff")
        st.markdown(f"""
        <div style="background:#0d0d18;border:1px solid #2a2a3a;border-radius:12px;padding:1.3rem 1.4rem;height:100%">
            <div style="font-size:.62rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:.5rem">✓ LAST RACE</div>
            <div style="font-size:1.3rem;font-weight:700;color:#fff;line-height:1.2">{lr["name"]}</div>
            <div style="font-size:.82rem;color:#9a9ab0;margin:.25rem 0">{lr["circuit"]} · {lr["date"]}</div>
            <div style="display:flex;gap:1.2rem;margin-top:.8rem;flex-wrap:wrap">
                <div>
                    <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Winner</div>
                    <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:{w_color};font-weight:700">{lr["winner"]}</div>
                </div>
                <div>
                    <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">P2 / P3</div>
                    <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#c0c0c0">{lr["p2"]} / {lr["p3"]}</div>
                </div>
                <div>
                    <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Fastest Lap</div>
                    <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#a020f0">{lr["fl"]} {lr["fl_time"]}</div>
                </div>
            </div>
            <div style="font-size:.78rem;color:#7a7a9a;margin-top:.7rem;line-height:1.5;border-top:1px solid #1a1a2a;padding-top:.6rem">{lr["highlight"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Standings
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("### 🏆 Driver Standings")
        rows = ""
        for pos, drv, team, pts, wins in _drv_st:
            dclr  = DRIVER_COLORS.get(drv, "#ffffff")
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"{pos}."
            w_txt = f"<span style='color:#ffd700;font-size:.7rem'>{wins}W</span>" if wins > 0 else ""
            rows += f"""
            <tr>
              <td style="padding:.32rem .6rem;color:#6a6a8a;font-size:.75rem;width:36px">{medal}</td>
              <td style="padding:.32rem .4rem;color:{dclr};font-weight:700;font-family:Share Tech Mono,monospace">{drv}</td>
              <td style="padding:.32rem .4rem;color:#7a7a9a;font-size:.78rem">{team}</td>
              <td style="padding:.32rem .6rem;text-align:right;font-family:Share Tech Mono,monospace;color:#fff;font-weight:600">{pts} {w_txt}</td>
            </tr>"""
        st.markdown(f"""
        <div style="background:#0a0a14;border:1px solid #1e1e30;border-radius:10px;overflow:hidden">
        <table style="width:100%;border-collapse:collapse;font-size:.88rem">
        <thead><tr style="background:#14141e">
          <th style="padding:.4rem .6rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">POS</th>
          <th style="padding:.4rem .4rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">DRIVER</th>
          <th style="padding:.4rem .4rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">TEAM</th>
          <th style="padding:.4rem .6rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:right">PTS</th>
        </tr></thead><tbody>{rows}</tbody></table></div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown("### 🏗️ Constructor Standings")
        c_rows = ""
        for pos, team, pts, color in _con_st:
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"{pos}."
            bar_w = round(pts / _con_st[0][2] * 100)
            c_rows += f"""
            <tr>
              <td style="padding:.32rem .6rem;color:#6a6a8a;font-size:.75rem;width:36px">{medal}</td>
              <td style="padding:.32rem .5rem;color:{color};font-weight:700;font-size:.88rem;width:130px">{team}</td>
              <td style="padding:.32rem .5rem">
                <div style="background:#1a1a2a;border-radius:3px;height:5px;overflow:hidden">
                  <div style="background:{color};height:100%;width:{bar_w}%;border-radius:3px"></div>
                </div>
              </td>
              <td style="padding:.32rem .6rem;text-align:right;font-family:Share Tech Mono,monospace;color:#fff;font-weight:600;font-size:.88rem">{pts}</td>
            </tr>"""
        st.markdown(f"""
        <div style="background:#0a0a14;border:1px solid #1e1e30;border-radius:10px;overflow:hidden">
        <table style="width:100%;border-collapse:collapse;font-size:.88rem">
        <thead><tr style="background:#14141e">
          <th style="padding:.4rem .6rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">POS</th>
          <th style="padding:.4rem .5rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">TEAM</th>
          <th style="padding:.4rem .5rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:left">BAR</th>
          <th style="padding:.4rem .6rem;color:#6a6a8a;font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;text-align:right">PTS</th>
        </tr></thead><tbody>{c_rows}</tbody></table></div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CSS: esconde os botões invisíveis que ficam sobre os cards
    st.markdown("""
    <style>
    div[data-testid="stButton"] button p { font-size:0 !important; }
    div[data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin-top: -72px !important;
        height: 72px !important;
        opacity: 0 !important;
        position: relative !important;
        z-index: 10 !important;
        cursor: pointer !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Calendário clicável
    st.markdown("### 📅 2026 Season Calendar")
    st.caption("Clique em qualquer GP para ver os horários (🇧🇷 BRT) e resultado")

    if "selected_gp" not in st.session_state:
        st.session_state.selected_gp = None

    cal_cols = st.columns(4)
    for i, (rnd, name, circuit, date_str, status, is_sprint) in enumerate(_cal):
        border   = "#e10600" if status == "next" else "#2a2a3a" if status == "done" else "#1e1e30"
        bg       = "#0d0d18" if status == "next" else "#08080e" if status == "done" else "#0a0a14"
        faded    = "opacity:.45;" if status == "done" else ""
        selected = st.session_state.selected_gp == name
        sel_style = "border:2px solid #e10600;" if selected else f"border:1px solid {border};"
        next_badge = (
            ' <span style="background:#e10600;color:#fff;font-size:.44rem;font-weight:700;'
            'padding:1px 5px;border-radius:6px;">NEXT</span>'
            if status == "next" else
            ' <span style="color:#3a3a5a;font-size:.6rem">✓</span>'
            if status == "done" else ""
        )
        sprint_badge = (
            ' <span style="background:rgba(255,215,0,.12);color:#ffd700;font-size:.42rem;'
            'font-weight:700;padding:1px 4px;border-radius:5px;">★ S</span>'
            if is_sprint else ""
        )
        with cal_cols[i % 4]:
            st.markdown(f"""
            <div style="background:{bg};{sel_style}border-radius:8px;
                        padding:.6rem .75rem;margin-bottom:.2rem;{faded}cursor:pointer;">
                <div style="font-size:.58rem;color:#6a6a8a;font-family:Share Tech Mono,monospace">R{rnd:02d} · {date_str}</div>
                <div style="font-size:.82rem;font-weight:700;color:#e8e8f0;line-height:1.25;margin:.2rem 0">
                    {name}{next_badge}{sprint_badge}
                </div>
                <div style="font-size:.66rem;color:#5a5a7a">{circuit}</div>
            </div>
            """, unsafe_allow_html=True)
            # Botão invisível sobre o card
            if st.button("​", key=f"gp_{rnd}", use_container_width=True,
                         help=f"Ver sessões de {name}"):
                st.session_state.selected_gp = None if selected else name
                st.rerun()

    # ── Painel de detalhes abaixo do calendário
    if st.session_state.selected_gp:
        st.markdown("---")
        gp_info = next((r for r in _cal if r[1] == st.session_state.selected_gp), None)
        if gp_info:
            rnd, name, circuit, date_str, status, is_sprint = gp_info
            col_title, col_close = st.columns([10, 1])
            with col_title:
                st.markdown(f"### 📋 {name} — Round {rnd}")
                st.caption(f"📍 {circuit} · 📅 {date_str} · 🇧🇷 Horário de Brasília")
            with col_close:
                if st.button("✕", key="close_gp"):
                    st.session_state.selected_gp = None
                    st.rerun()
            _render_gp_detail_inline(name, status, date_str, circuit)



def _render_gp_detail_inline(gp_name: str, status: str, date_str: str, circuit: str):
    """Conteúdo do expander: horários + resultado."""
    details = GP_DETAILS.get(gp_name)

    st.markdown(f"""
    <div style="font-size:.72rem;color:#6a6a8a;margin-bottom:.6rem">
        📍 {circuit} &nbsp;·&nbsp; 📅 {date_str}
    </div>
    """, unsafe_allow_html=True)

    if not details:
        st.info("Detalhes ainda não disponíveis.")
        return

    # ── Sessões
    for session_name, day, time_local in details["sessions"]:
        icon  = SESSION_ICONS.get(session_name, "⚪")
        color = SESSION_COLORS.get(session_name, "#ffffff")
        is_race = session_name == "Race"
        bg = "rgba(225,6,0,.08)" if is_race else "rgba(255,255,255,.02)"
        st.markdown(f"""
        <div style="background:{bg};border-left:3px solid {color};border-radius:0 5px 5px 0;
                    padding:.4rem .75rem;margin-bottom:.3rem;
                    display:flex;justify-content:space-between;align-items:center">
            <div>
                <span>{icon}</span>
                <span style="font-weight:700;color:{color};font-size:.85rem;margin-left:.35rem">{session_name}</span>
                <span style="color:#4a4a6a;font-size:.72rem;margin-left:.4rem">{day}</span>
            </div>
            <div style="font-family:Share Tech Mono,monospace;font-size:.9rem;color:#fff">{time_local}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Resultado (só GPs passados)
    result = details.get("result")
    if status == "done" and result:
        st.markdown("<div style='margin-top:.8rem'></div>", unsafe_allow_html=True)
        st.markdown("**🏆 Resultado**")

        w   = result["winner"];  wc = DRIVER_COLORS.get(w,  "#ffd700"); wt = DRIVER_TEAMS.get(w,  "")
        p2  = result["p2"];      p2c= DRIVER_COLORS.get(p2, "#c0c0c0"); p2t= DRIVER_TEAMS.get(p2, "")
        p3  = result["p3"];      p3c= DRIVER_COLORS.get(p3, "#cd7f32"); p3t= DRIVER_TEAMS.get(p3, "")
        fl  = result["fl"];      flt= result["fl_time"]

        html = (
            "<div style='background:#0d0d18;border:1px solid #1e1e2e;border-radius:8px;"
            "padding:.7rem .9rem;margin-bottom:.4rem'>"
            "<div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.3rem'>"
            "<span style='font-size:.9rem'>🥇</span>"
            f"<span style='font-family:Share Tech Mono,monospace;font-weight:700;color:{wc};font-size:.95rem'>{w}</span>"
            f"<span style='font-size:.68rem;color:#5a5a7a'>{wt}</span></div>"
            "<div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.3rem'>"
            "<span style='font-size:.9rem'>🥈</span>"
            f"<span style='font-family:Share Tech Mono,monospace;font-weight:700;color:{p2c};font-size:.95rem'>{p2}</span>"
            f"<span style='font-size:.68rem;color:#5a5a7a'>{p2t}</span></div>"
            "<div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.3rem'>"
            "<span style='font-size:.9rem'>🥉</span>"
            f"<span style='font-family:Share Tech Mono,monospace;font-weight:700;color:{p3c};font-size:.95rem'>{p3}</span>"
            f"<span style='font-size:.68rem;color:#5a5a7a'>{p3t}</span></div>"
            "<div style='border-top:1px solid #1e1e2e;margin-top:.4rem;padding-top:.4rem;"
            "font-size:.78rem;color:#7a7a9a'>"
            "⚡ <span style='color:#a020f0;font-weight:700'>FL</span>"
            f"&nbsp;{fl}"
            f"<span style='font-family:Share Tech Mono,monospace;color:#fff;margin-left:.3rem'>{flt}</span>"
            "</div></div>"
        )
        st.markdown(html, unsafe_allow_html=True)

    elif status in ("next", "upcoming"):
        next_badge = ("<br><br><span style='background:#e10600;color:#fff;font-size:.65rem;"
                      "font-weight:700;padding:2px 10px;border-radius:8px'>NEXT RACE</span>"
                      if status == "next" else "")
        st.markdown(
            f"<div style='text-align:center;padding:.8rem;color:#4a4a6a;font-size:.8rem;margin-top:.5rem'>"
            f"🏎️ &nbsp; Resultado disponível após a corrida{next_badge}</div>",
            unsafe_allow_html=True,
        )
