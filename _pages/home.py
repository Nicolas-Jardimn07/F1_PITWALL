# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: Home — season overview, standings, calendar, last race
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from datetime import datetime as _dt
from _utils.constants import DRIVER_COLORS, DRIVER_TEAMS
from _data.season_data import get_season_data


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
            <div style="font-size:.62rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:.5rem">
                ✓ LAST RACE
            </div>
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
            <div style="font-size:.78rem;color:#7a7a9a;margin-top:.7rem;line-height:1.5;
                        border-top:1px solid #1a1a2a;padding-top:.6rem">{lr["highlight"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Standings side by side
    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("### 🏆 Driver Standings")
        rows = ""
        for pos, drv, team, pts, wins in _drv_st:
            dclr  = DRIVER_COLORS.get(drv, "#ffffff")
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"{pos}."
            w_txt = (
                f"<span style='color:#ffd700;font-size:.7rem'>{wins}W</span>"
                if wins > 0 else ""
            )
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

    # ── Calendar
    st.markdown("### 📅 2026 Season Calendar")
    cal_cols = st.columns(4)
    for i, (rnd, name, circuit, date_str, status, is_sprint) in enumerate(_cal):
        border = "#e10600" if status == "next" else "#2a2a3a" if status == "done" else "#1e1e30"
        bg     = "#0d0d18" if status == "next" else "#08080e" if status == "done" else "#0a0a14"
        txt_op = "opacity:.45" if status == "done" else ""
        next_badge = (
            '<span style="background:#e10600;color:#fff;font-size:.52rem;font-weight:700;'
            'letter-spacing:1px;padding:1px 6px;border-radius:10px;margin-left:.3rem">NEXT</span>'
            if status == "next" else
            '<span style="color:#6a6a8a;font-size:.62rem"> ✓</span>'
            if status == "done" else ""
        )
        sprint_badge = (
            '<span style="background:rgba(255,215,0,.15);color:#ffd700;font-size:.48rem;'
            'font-weight:700;letter-spacing:1px;padding:1px 5px;border-radius:8px;margin-left:.3rem">★ SPRINT</span>'
            if is_sprint else ""
        )
        with cal_cols[i % 4]:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:8px;
                        padding:.6rem .75rem;margin-bottom:.6rem;{txt_op}">
                <div style="font-size:.58rem;color:#6a6a8a;font-family:Share Tech Mono,monospace">R{rnd:02d} · {date_str}</div>
                <div style="font-size:.82rem;font-weight:700;color:#e8e8f0;line-height:1.25;margin:.2rem 0">
                    {name}{next_badge}{sprint_badge}
                </div>
                <div style="font-size:.66rem;color:#5a5a7a">{circuit}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Quick nav
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Quick Access")
    nav_cols  = st.columns(4)
    nav_items = [
        ("📊", "Historical Analysis", "Telemetry · Speed · Delta · Mini-Sectors", "#e10600"),
        ("🔴", "Live Mode",           "Timing · Car data · Race control",          "#ff4444"),
        ("📰", "F1 News 2026",        "Latest headlines from the paddock",          "#ffd700"),
        ("🎓", "English Study",       "Radio · Interviews · Broadcast vocab",       "#00e676"),
    ]
    for i, (icon, title, desc, color) in enumerate(nav_items):
        with nav_cols[i]:
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #1e1e30;border-top:3px solid {color};
                        border-radius:10px;padding:1rem;text-align:center">
                <div style="font-size:2rem;margin-bottom:.4rem">{icon}</div>
                <div style="font-weight:700;color:#fff;font-size:.95rem">{title}</div>
                <div style="font-size:.72rem;color:#6a6a8a;margin-top:.25rem;line-height:1.4">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
