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
            ("FP1",        "Fri 14 Mar", "11:30"),
            ("FP2",        "Fri 14 Mar", "15:00"),
            ("FP3",        "Sat 15 Mar", "11:30"),
            ("Qualifying", "Sat 15 Mar", "15:00"),
            ("Race",       "Sun 16 Mar", "15:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "NOR", "fl": "ANT", "fl_time": "1:17.456"},
    },
    "Chinese GP": {
        "sessions": [
            ("FP1",          "Fri 21 Mar", "11:30"),
            ("Sprint Quali", "Fri 21 Mar", "15:30"),
            ("Sprint",       "Sat 22 Mar", "11:00"),
            ("Qualifying",   "Sat 22 Mar", "15:00"),
            ("Race",         "Sun 23 Mar", "15:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "NOR", "fl": "ANT", "fl_time": "1:32.145"},
    },
    "Japanese GP": {
        "sessions": [
            ("FP1",        "Fri 04 Apr", "11:30"),
            ("FP2",        "Fri 04 Apr", "15:00"),
            ("FP3",        "Sat 05 Apr", "11:30"),
            ("Qualifying", "Sat 05 Apr", "15:00"),
            ("Race",       "Sun 06 Apr", "14:00"),
        ],
        "result": {"winner": "ANT", "p2": "HAM", "p3": "LEC", "fl": "HAM", "fl_time": "1:30.983"},
    },
    "Miami GP": {
        "sessions": [
            ("FP1",          "Fri 02 May", "12:30"),
            ("Sprint Quali", "Fri 02 May", "16:30"),
            ("Sprint",       "Sat 03 May", "12:00"),
            ("Qualifying",   "Sat 03 May", "16:00"),
            ("Race",         "Sun 04 May", "16:00"),
        ],
        "result": {"winner": "ANT", "p2": "PIA", "p3": "NOR", "fl": "RUS", "fl_time": "1:27.341"},
    },
    "Canadian GP": {
        "sessions": [
            ("FP1",          "Fri 06 Jun", "13:30"),
            ("Sprint Quali", "Fri 06 Jun", "17:30"),
            ("Sprint",       "Sat 07 Jun", "13:00"),
            ("Qualifying",   "Sat 07 Jun", "17:00"),
            ("Race",         "Sun 08 Jun", "14:00"),
        ],
        "result": {"winner": "ANT", "p2": "RUS", "p3": "HAM", "fl": "ANT", "fl_time": "1:13.702"},
    },
    "Monaco GP": {
        "sessions": [
            ("FP1",        "Thu 22 May", "11:30"),
            ("FP2",        "Thu 22 May", "15:00"),
            ("FP3",        "Sat 24 May", "11:30"),
            ("Qualifying", "Sat 24 May", "15:00"),
            ("Race",       "Sun 25 May", "15:00"),
        ],
        "result": {"winner": "ANT", "p2": "HAM", "p3": "HAD", "fl": "ANT", "fl_time": "1:12.803"},
    },
    "Barcelona GP": {
        "sessions": [
            ("FP1",        "Fri 12 Jun", "13:30"),
            ("FP2",        "Fri 12 Jun", "17:00"),
            ("FP3",        "Sat 13 Jun", "12:30"),
            ("Qualifying", "Sat 13 Jun", "16:00"),
            ("Race",       "Sun 14 Jun", "15:00"),
        ],
        "result": None,
    },
    "Austrian GP": {
        "sessions": [
            ("FP1",        "Fri 26 Jun", "13:30"),
            ("FP2",        "Fri 26 Jun", "17:00"),
            ("FP3",        "Sat 27 Jun", "12:30"),
            ("Qualifying", "Sat 27 Jun", "16:00"),
            ("Race",       "Sun 28 Jun", "15:00"),
        ],
        "result": None,
    },
    "British GP": {
        "sessions": [
            ("FP1",          "Fri 03 Jul", "13:30"),
            ("Sprint Quali", "Fri 03 Jul", "17:30"),
            ("Sprint",       "Sat 04 Jul", "12:30"),
            ("Qualifying",   "Sat 04 Jul", "16:00"),
            ("Race",         "Sun 05 Jul", "15:00"),
        ],
        "result": None,
    },
    "Belgian GP": {
        "sessions": [
            ("FP1",        "Fri 17 Jul", "13:30"),
            ("FP2",        "Fri 17 Jul", "17:00"),
            ("FP3",        "Sat 18 Jul", "12:30"),
            ("Qualifying", "Sat 18 Jul", "16:00"),
            ("Race",       "Sun 19 Jul", "15:00"),
        ],
        "result": None,
    },
    "Hungarian GP": {
        "sessions": [
            ("FP1",        "Fri 24 Jul", "13:30"),
            ("FP2",        "Fri 24 Jul", "17:00"),
            ("FP3",        "Sat 25 Jul", "12:30"),
            ("Qualifying", "Sat 25 Jul", "16:00"),
            ("Race",       "Sun 26 Jul", "15:00"),
        ],
        "result": None,
    },
    "Dutch GP": {
        "sessions": [
            ("FP1",          "Fri 21 Aug", "12:30"),
            ("Sprint Quali", "Fri 21 Aug", "16:30"),
            ("Sprint",       "Sat 22 Aug", "12:00"),
            ("Qualifying",   "Sat 22 Aug", "16:00"),
            ("Race",         "Sun 23 Aug", "15:00"),
        ],
        "result": None,
    },
    "Italian GP": {
        "sessions": [
            ("FP1",        "Fri 04 Sep", "13:30"),
            ("FP2",        "Fri 04 Sep", "17:00"),
            ("FP3",        "Sat 05 Sep", "12:30"),
            ("Qualifying", "Sat 05 Sep", "16:00"),
            ("Race",       "Sun 06 Sep", "15:00"),
        ],
        "result": None,
    },
    "Madrid GP": {
        "sessions": [
            ("FP1",        "Fri 11 Sep", "13:30"),
            ("FP2",        "Fri 11 Sep", "17:00"),
            ("FP3",        "Sat 12 Sep", "12:30"),
            ("Qualifying", "Sat 12 Sep", "16:00"),
            ("Race",       "Sun 13 Sep", "15:00"),
        ],
        "result": None,
    },
    "Azerbaijan GP": {
        "sessions": [
            ("FP1",        "Fri 25 Sep", "13:30"),
            ("FP2",        "Fri 25 Sep", "17:00"),
            ("FP3",        "Sat 26 Sep", "12:30"),
            ("Qualifying", "Sat 26 Sep", "16:00"),
            ("Race",       "Sun 27 Sep", "14:00"),
        ],
        "result": None,
    },
    "Singapore GP": {
        "sessions": [
            ("FP1",          "Fri 09 Oct", "17:30"),
            ("Sprint Quali", "Fri 09 Oct", "21:30"),
            ("Sprint",       "Sat 10 Oct", "17:00"),
            ("Qualifying",   "Sat 10 Oct", "21:00"),
            ("Race",         "Sun 11 Oct", "20:00"),
        ],
        "result": None,
    },
    "United States GP": {
        "sessions": [
            ("FP1",        "Fri 23 Oct", "19:30"),
            ("FP2",        "Fri 23 Oct", "23:00"),
            ("FP3",        "Sat 24 Oct", "19:30"),
            ("Qualifying", "Sat 24 Oct", "23:00"),
            ("Race",       "Sun 25 Oct", "21:00"),
        ],
        "result": None,
    },
    "Mexico City GP": {
        "sessions": [
            ("FP1",        "Fri 30 Oct", "19:30"),
            ("FP2",        "Fri 30 Oct", "23:00"),
            ("FP3",        "Sat 31 Oct", "18:30"),
            ("Qualifying", "Sat 31 Oct", "22:00"),
            ("Race",       "Sun 01 Nov", "21:00"),
        ],
        "result": None,
    },
    "São Paulo GP": {
        "sessions": [
            ("FP1",        "Fri 06 Nov", "15:30"),
            ("FP2",        "Fri 06 Nov", "19:00"),
            ("FP3",        "Sat 07 Nov", "14:30"),
            ("Qualifying", "Sat 07 Nov", "18:00"),
            ("Race",       "Sun 08 Nov", "17:00"),
        ],
        "result": None,
    },
    "Las Vegas GP": {
        "sessions": [
            ("FP1",        "Thu 19 Nov", "04:30"),
            ("FP2",        "Thu 19 Nov", "08:00"),
            ("FP3",        "Fri 20 Nov", "04:30"),
            ("Qualifying", "Fri 20 Nov", "08:00"),
            ("Race",       "Sat 21 Nov", "06:00"),
        ],
        "result": None,
    },
    "Qatar GP": {
        "sessions": [
            ("FP1",        "Fri 27 Nov", "17:30"),
            ("FP2",        "Fri 27 Nov", "21:00"),
            ("FP3",        "Sat 28 Nov", "17:30"),
            ("Qualifying", "Sat 28 Nov", "21:00"),
            ("Race",       "Sun 29 Nov", "18:00"),
        ],
        "result": None,
    },
    "Abu Dhabi GP": {
        "sessions": [
            ("FP1",        "Fri 04 Dec", "13:30"),
            ("FP2",        "Fri 04 Dec", "17:00"),
            ("FP3",        "Sat 05 Dec", "13:30"),
            ("Qualifying", "Sat 05 Dec", "17:00"),
            ("Race",       "Sun 06 Dec", "17:00"),
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

    # ── Calendário clicável
    st.markdown("### 📅 2026 Season Calendar")
    st.caption("Clique em qualquer GP para ver os horários das sessões e o resultado")

    # Estado do GP selecionado
    if "selected_gp" not in st.session_state:
        st.session_state.selected_gp = None

    cal_cols = st.columns(4)
    for i, (rnd, name, circuit, date_str, status, is_sprint) in enumerate(_cal):
        border = "#e10600" if status == "next" else "#2a2a3a" if status == "done" else "#1e1e30"
        bg     = "#0d0d18" if status == "next" else "#08080e" if status == "done" else "#0a0a14"
        txt_op = "opacity:.5" if status == "done" else ""
        next_badge = (
            '<span style="background:#e10600;color:#fff;font-size:.48rem;font-weight:700;'
            'padding:1px 5px;border-radius:8px;margin-left:.3rem">NEXT</span>'
            if status == "next" else
            '<span style="color:#3a3a5a;font-size:.6rem"> ✓</span>'
            if status == "done" else ""
        )
        sprint_badge = (
            '<span style="background:rgba(255,215,0,.15);color:#ffd700;font-size:.44rem;'
            'font-weight:700;padding:1px 4px;border-radius:6px;margin-left:.2rem">★ S</span>'
            if is_sprint else ""
        )
        selected = st.session_state.selected_gp == name
        sel_border = "2px solid #e10600" if selected else f"1px solid {border}"

        with cal_cols[i % 4]:
            st.markdown(f"""
            <div style="background:{bg};border:{sel_border};border-radius:8px;
                        padding:.55rem .7rem;margin-bottom:.5rem;{txt_op}">
                <div style="font-size:.55rem;color:#6a6a8a;font-family:Share Tech Mono,monospace">R{rnd:02d} · {date_str}</div>
                <div style="font-size:.8rem;font-weight:700;color:#e8e8f0;line-height:1.25;margin:.15rem 0">
                    {name}{next_badge}{sprint_badge}
                </div>
                <div style="font-size:.62rem;color:#4a4a6a">{circuit}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📋", key=f"gp_{rnd}", help=f"Ver sessões de {name}", use_container_width=True):
                if st.session_state.selected_gp == name:
                    st.session_state.selected_gp = None
                else:
                    st.session_state.selected_gp = name
                st.rerun()

    # ── Painel de detalhes do GP selecionado
    if st.session_state.selected_gp:
        _render_gp_detail(st.session_state.selected_gp, _cal)


def _render_gp_detail(gp_name: str, cal: list):
    """Mostra horários e resultado do GP selecionado."""
    details = GP_DETAILS.get(gp_name)

    # Encontra info do GP no calendário
    gp_info = next((r for r in cal if r[1] == gp_name), None)
    if not gp_info:
        return

    rnd, name, circuit, date_str, status, is_sprint = gp_info

    st.markdown("---")
    st.markdown(f"### 📋 {name} — Round {rnd}")
    st.caption(f"{circuit} · {date_str}")

    if not details:
        st.info("Detalhes das sessões não disponíveis ainda.")
        return

    col_sess, col_result = st.columns([3, 2])

    with col_sess:
        st.markdown("#### 🕐 Horários das Sessões")
        st.caption("Horário local do circuito")

        for session_name, day, time_local in details["sessions"]:
            icon  = SESSION_ICONS.get(session_name, "⚪")
            color = SESSION_COLORS.get(session_name, "#ffffff")
            is_race = session_name == "Race"
            bg = "rgba(225,6,0,.08)" if is_race else "rgba(255,255,255,.03)"
            border_left = f"3px solid {color}"

            st.markdown(f"""
            <div style="background:{bg};border:1px solid #1e1e2e;border-left:{border_left};
                        border-radius:6px;padding:.55rem .9rem;margin-bottom:.4rem;
                        display:flex;justify-content:space-between;align-items:center">
                <div>
                    <span style="font-size:.85rem">{icon}</span>
                    <span style="font-weight:700;color:{color};font-size:.9rem;margin-left:.4rem">{session_name}</span>
                    <span style="color:#5a5a7a;font-size:.75rem;margin-left:.5rem">{day}</span>
                </div>
                <div style="font-family:Share Tech Mono,monospace;font-size:.95rem;color:#fff">{time_local}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_result:
        result = details.get("result")
        if status == "done" and result:
            st.markdown("#### 🏆 Resultado")
            podium = [
                (result["winner"], "🥇 P1", DRIVER_COLORS.get(result["winner"], "#ffd700")),
                (result["p2"],     "🥈 P2", DRIVER_COLORS.get(result["p2"],     "#c0c0c0")),
                (result["p3"],     "🥉 P3", DRIVER_COLORS.get(result["p3"],     "#cd7f32")),
            ]
            for drv, label, dclr in podium:
                team = DRIVER_TEAMS.get(drv, "")
                st.markdown(f"""
                <div style="background:#0d0d18;border:1px solid #1e1e30;border-left:3px solid {dclr};
                            border-radius:8px;padding:.6rem .9rem;margin-bottom:.4rem;
                            display:flex;align-items:center;gap:.75rem">
                    <div style="font-size:1.1rem">{label}</div>
                    <div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1rem;font-weight:700;color:{dclr}">{drv}</div>
                        <div style="font-size:.68rem;color:#5a5a7a">{team}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#0a0a14;border:1px solid #1e1e30;border-radius:6px;
                        padding:.55rem .9rem;margin-top:.2rem">
                <span style="color:#a020f0;font-size:.7rem;font-weight:700">⚡ FASTEST LAP</span>
                <span style="font-family:Share Tech Mono,monospace;font-size:.85rem;color:#fff;margin-left:.5rem">
                    {result["fl"]} {result["fl_time"]}
                </span>
            </div>
            """, unsafe_allow_html=True)

        elif status in ("next", "upcoming"):
            st.markdown("#### ⏳ Aguardando")
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #1e1e30;border-radius:10px;
                        padding:1.5rem;text-align:center;margin-top:.5rem">
                <div style="font-size:2rem">🏎️</div>
                <div style="color:#6a6a8a;font-size:.85rem;margin-top:.5rem">
                    Resultado disponível<br>após a corrida
                </div>
                {"<div style='margin-top:.75rem'><span style=\"background:#e10600;color:#fff;font-size:.65rem;font-weight:700;padding:3px 10px;border-radius:10px;letter-spacing:1px\">NEXT RACE</span></div>" if status == "next" else ""}
            </div>
            """, unsafe_allow_html=True)

    if st.button("✕ Fechar", key="close_detail"):
        st.session_state.selected_gp = None
        st.rerun()
