# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: Historical Analysis — FastF1 telemetry comparison
# ─────────────────────────────────────────────────────────────────────────────
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from _utils.constants import DRIVER_TEAMS, TRACK_STATUS_MAP, PLOTLY_LAYOUT
from _utils.helpers import fmt_laptime, hex_to_rgba, get_driver_color
from _data.f1_data import load_session_f1, get_driver_list, get_telemetry
from _data.content import ENGINEERING_SECTIONS, GLOSSARY
from _components.charts import (
    make_speed_chart, make_inputs_chart,
    make_delta_chart, make_minisectors_chart,
)


def render(year: int, gp_name: str, session_type: str, session_code: str, analyze: bool):
    # ── Reset drivers list when selection changes
    cur_sel = (year, gp_name, session_code)
    if st.session_state.last_selection != cur_sel:
        st.session_state.drivers        = []
        st.session_state.last_selection = cur_sel
        st.session_state.replay_playing = False
        st.session_state.replay_t       = 0.0

    # ── Load session on button click
    if analyze:
        with st.spinner(f"⏳ Carregando {gp_name} {year} — {session_type}... (pode levar alguns minutos)"):
            try:
                sess = load_session_f1(year, gp_name, session_code)
                drivers_list = get_driver_list(sess)
                st.session_state.drivers = drivers_list
                st.success(f"✅ Sessão carregada — {len(drivers_list)} pilotos disponíveis.")
            except Exception as e:
                import traceback
                st.error(f"❌ Falha ao carregar sessão:")
                st.code(str(e), language="text")
                st.expander("🔍 Traceback completo").code(traceback.format_exc(), language="text")
                return

    # ── Verifica se a sessão está disponível (via session_state interno do f1_data)
    cache_key = f"f1sess_{year}_{gp_name}_{session_code}"
    if cache_key not in st.session_state or not st.session_state.drivers:
        _splash()
        return

    session   = st.session_state[cache_key]
    available = st.session_state.drivers
    if not available:
        st.error("No drivers found in this session.")
        return

    # ── Driver selectors
    def safe_idx(lst, val, fb=0):
        return lst.index(val) if val in lst else fb

    c1, c2 = st.columns(2)
    with c1:
        d1 = st.selectbox("🔵 Driver A", available, index=safe_idx(available, "VER", 0), key="d1")
    with c2:
        d2 = st.selectbox("🟠 Driver B", available, index=safe_idx(available, "NOR", min(1, len(available) - 1)), key="d2")

    if not d1 or not d2:
        st.info("Select both drivers to load telemetry.")
        return

    drivers = [d1, d2] if d1 != d2 else [d1]

    # ── Load telemetry
    tels, laps_data, colors = {}, {}, {}
    with st.spinner("📡 Extracting telemetry..."):
        for drv in drivers:
            try:
                tel, lap       = get_telemetry(session, drv)
                tels[drv]      = tel
                laps_data[drv] = lap
                colors[drv]    = get_driver_color(drv, session)
            except Exception as e:
                st.warning(f"⚠️ No data for {drv}: {e}")

    if not tels:
        st.error("No telemetry data available. Try a different session or driver.")
        return

    # ── Metrics row
    st.markdown("### Lap Metrics")
    mc = st.columns(len(drivers) * 3 + (1 if len(drivers) == 2 else 0))
    ci = 0
    for drv in drivers:
        lap = laps_data[drv]
        tel = tels[drv]
        lt  = lap["LapTime"].total_seconds() if not pd.isna(lap["LapTime"]) else None
        mc[ci].metric(f"⏱️ {drv} · {DRIVER_TEAMS.get(drv, '')}", fmt_laptime(lt)); ci += 1
        mc[ci].metric(f"🚀 Top Speed {drv}", f"{int(tel['Speed'].max())} km/h");   ci += 1
        mc[ci].metric(f"🎮 Avg Throttle {drv}", f"{int(tel['Throttle'].mean())}%"); ci += 1

    if len(drivers) == 2:
        lt1 = laps_data[drivers[0]]["LapTime"].total_seconds()
        lt2 = laps_data[drivers[1]]["LapTime"].total_seconds()
        if not pd.isna(lt1) and not pd.isna(lt2):
            gap = lt2 - lt1
            mc[ci].metric("⚡ Gap", f"{gap:+.3f}s",
                          delta=f"{drivers[1]} {'behind' if gap > 0 else 'ahead'}",
                          delta_color="inverse")
    st.divider()

    # ── Analysis tabs
    (tab_speed, tab_inputs, tab_delta, tab_mini,
     tab_stats, tab_eng, tab_radio, tab_gloss) = st.tabs([
        "📈 Speed Trace", "🎮 Driver Inputs", "⏱️ Delta Time",
        "🗺️ Mini-Sectors", "📊 Lap Stats", "⚙️ Engineering",
        "🎙️ Team Radio", "📖 F1 Glossary",
    ])

    with tab_speed:
        st.plotly_chart(make_speed_chart(tels, colors), use_container_width=True)
        with st.expander("💡 How to read — Speed Trace"):
            st.markdown("""
- **Peaks** = full throttle straights
- **Valleys** = braking zones — depth shows minimum corner speed
- **Gap between lines** = who brakes later or accelerates earlier
            """)

    with tab_inputs:
        st.plotly_chart(make_inputs_chart(tels, colors), use_container_width=True)
        with st.expander("💡 How to read — Driver Inputs"):
            st.markdown("""
- **Throttle 100% longer** = more confidence on corner exit
- **High brake spike** = more aggressive / later braking point
- Overlapping brake + throttle = **trail braking** technique
            """)

    with tab_delta:
        if len(drivers) == 2:
            st.plotly_chart(make_delta_chart(tels, drivers, colors), use_container_width=True)
            with st.expander("💡 How to read — Delta Time"):
                st.markdown(f"""
- **Above zero** = **{drivers[0]}** losing time to **{drivers[1]}**
- **Below zero** = **{drivers[0]}** gaining time
                """)
        else:
            st.info("Select two different drivers to see the Delta Time chart.")

    with tab_mini:
        if len(drivers) == 2:
            st.markdown("##### Each mini-sector coloured by the faster driver in that segment")
            st.plotly_chart(make_minisectors_chart(tels, drivers, colors), use_container_width=True)
        else:
            st.info("Select two different drivers to see the Mini-Sector advantage chart.")

    with tab_stats:
        _lap_stats_tab(tels, laps_data, drivers, colors)

    with tab_eng:
        _engineering_tab()

    with tab_radio:
        _radio_tab(session, drivers, colors)

    with tab_gloss:
        _glossary_tab()

    # ── Replay auto-advance
    if st.session_state.get("_replay_need_rerun"):
        _dur  = st.session_state.get("_replay_duration", 999)
        _next = st.session_state.replay_t + 0.5
        if _next >= _dur:
            st.session_state.replay_playing = False
            st.session_state.replay_t       = 0.0
        else:
            st.session_state.replay_t = _next
        time.sleep(0.12)
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  Sub-tabs
# ─────────────────────────────────────────────────────────────────────────────

def _splash():
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem">
        <div style="font-size:4rem">🏎️</div>
        <h2 style="color:#e10600;letter-spacing:3px;margin:.5rem 0">READY FOR ANALYSIS</h2>
        <p style="color:#6a6a8a;font-size:1rem">
            Select the season, Grand Prix and session in the sidebar.<br>
            Click <strong style="color:#e10600">▶ ANALYZE</strong> to load data from the official F1 API.
        </p>
        <div style="margin-top:2rem;font-size:.8rem;color:#3a3a5a;font-family:Share Tech Mono,monospace">
            Local cache active · Data downloaded once · Subsequent runs are instant
        </div>
    </div>
    """, unsafe_allow_html=True)


def _lap_stats(tel, lap) -> dict:
    t         = tel.copy()
    dur       = lap["LapTime"].total_seconds() if not pd.isna(lap["LapTime"]) else None
    ft_pct    = round((t["Throttle"] >= 98).mean() * 100, 1)
    brk_pct   = round(t["Brake"].astype(bool).mean() * 100, 1)
    coast_pct = round(float(((t["Throttle"] < 5) & (~t["Brake"].astype(bool))).mean()) * 100, 1)
    drs_pct   = round((t["DRS"] >= 8).mean() * 100, 1)
    gear_cnt  = t["nGear"].value_counts().sort_index().to_dict()
    gear_tot  = max(sum(gear_cnt.values()), 1)
    return dict(
        laptime   = dur,
        dist      = float(t["Distance"].max()),
        ft_pct    = ft_pct,
        brk_pct   = brk_pct,
        coast_pct = coast_pct,
        drs_pct   = drs_pct,
        top_spd   = int(t["Speed"].max()),
        min_spd   = int(t["Speed"].min()),
        avg_spd   = round(float(t["Speed"].mean()), 1),
        avg_thr   = round(float(t.loc[t["Throttle"] > 0, "Throttle"].mean()), 1),
        brk_ev    = int(((t["Brake"].astype(int).diff() > 0)).sum()),
        gear_ch   = int((t["nGear"].diff().abs() > 0).sum()),
        gear_dist = {g: round(gear_cnt.get(g, 0) / gear_tot * 100, 1) for g in range(1, 9)},
    )


def _lap_stats_tab(tels, laps_data, drivers, colors):
    st.markdown("### 📊 Lap Statistics Dashboard")
    st.caption("Deep statistical comparison — all metrics computed from raw telemetry")
    st.divider()

    stats = {drv: _lap_stats(tels[drv], laps_data[drv]) for drv in drivers}

    # Overview cards
    st.markdown("#### ⏱️ Lap Overview")
    ov_cols = st.columns(len(drivers))
    for i, drv in enumerate(drivers):
        s    = stats[drv]
        dclr = colors.get(drv, "#ffffff")
        lt_s = fmt_laptime(s["laptime"]) if s["laptime"] else "N/A"
        with ov_cols[i]:
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #1e1e32;border-top:4px solid {dclr};
                        border-radius:10px;padding:1.1rem 1.2rem;text-align:center">
                <div style="color:{dclr};font-weight:700;font-size:1.4rem;letter-spacing:3px">{drv}</div>
                <div style="font-size:.68rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px;margin:.2rem 0">{DRIVER_TEAMS.get(drv,'')}</div>
                <div style="font-family:Share Tech Mono,monospace;font-size:2.2rem;color:#fff;margin:.5rem 0">{lt_s}</div>
                <div style="font-size:.72rem;color:#6a6a8a">fastest lap · {s['dist']:.0f} m</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Pedal stacked bars
    st.markdown("#### 🎮 Pedal Input Distribution (% of lap)")
    for drv in drivers:
        s    = stats[drv]
        dclr = colors.get(drv, "#ffffff")
        ft   = s["ft_pct"]
        brk  = s["brk_pct"]
        cst  = s["coast_pct"]
        mid  = round(max(100 - ft - brk - cst, 0), 1)
        fig_b = go.Figure()
        for val, label, col in [
            (ft,  f"{ft}% Full Throttle", "#00e676"),
            (mid, f"{mid}% Partial",       "#ffd700"),
            (cst, f"{cst}% Coasting",      "#6a6a8a"),
            (brk, f"{brk}% Braking",       "#ff4444"),
        ]:
            fig_b.add_trace(go.Bar(
                x=[val], y=[drv], orientation="h", name=label,
                marker_color=col,
                text=[label] if val > 3 else [""],
                textposition="inside", insidetextanchor="middle",
            ))
        fig_b.update_layout(
            barmode="stack", height=80,
            margin=dict(l=70, r=10, t=4, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis=dict(visible=False, range=[0, 100]),
            yaxis=dict(tickfont=dict(color=dclr, size=13, family="Share Tech Mono"),
                       gridcolor="#1e1e2e"),
            font=dict(family="Rajdhani, sans-serif"),
        )
        st.plotly_chart(fig_b, use_container_width=True)

    st.divider()

    # Head-to-head table
    if len(drivers) == 2:
        d1_, d2_ = drivers[0], drivers[1]
        s1,  s2  = stats[d1_], stats[d2_]
        c1_, c2_ = colors.get(d1_, "#fff"), colors.get(d2_, "#fff")
        st.markdown("#### 📋 Head-to-Head Statistics")

        rows = [
            ("Top Speed",        f"{s1['top_spd']} km/h", f"{s2['top_spd']} km/h", s1['top_spd'],   s2['top_spd'],   True),
            ("Min Corner Speed", f"{s1['min_spd']} km/h", f"{s2['min_spd']} km/h", s1['min_spd'],   s2['min_spd'],   True),
            ("Avg Speed",        f"{s1['avg_spd']} km/h", f"{s2['avg_spd']} km/h", s1['avg_spd'],   s2['avg_spd'],   True),
            ("Full Throttle %",  f"{s1['ft_pct']}%",      f"{s2['ft_pct']}%",      s1['ft_pct'],    s2['ft_pct'],    True),
            ("Avg Throttle",     f"{s1['avg_thr']}%",     f"{s2['avg_thr']}%",     s1['avg_thr'],   s2['avg_thr'],   True),
            ("Time Braking",     f"{s1['brk_pct']}%",     f"{s2['brk_pct']}%",     s2['brk_pct'],   s1['brk_pct'],   False),
            ("Coasting",         f"{s1['coast_pct']}%",   f"{s2['coast_pct']}%",   s2['coast_pct'], s1['coast_pct'], False),
            ("DRS Active",       f"{s1['drs_pct']}%",     f"{s2['drs_pct']}%",     s1['drs_pct'],   s2['drs_pct'],   True),
            ("Braking Events",   str(s1['brk_ev']),       str(s2['brk_ev']),        s2['brk_ev'],    s1['brk_ev'],    False),
            ("Gear Changes",     str(s1['gear_ch']),      str(s2['gear_ch']),        0,               0,               False),
        ]

        h2h = f"""
        <div style="background:#0d0d18;border:1px solid #1e1e32;border-radius:10px;overflow:hidden">
        <table style="width:100%;border-collapse:collapse;font-size:.88rem">
        <thead><tr>
          <th style="background:#1a1a28;color:{c1_};font-family:Share Tech Mono,monospace;
                     padding:.6rem 1rem;text-align:right;border-bottom:2px solid {c1_};width:28%">{d1_}</th>
          <th style="background:#1a1a28;color:#6a6a8a;font-size:.65rem;text-transform:uppercase;
                     letter-spacing:1.5px;padding:.6rem;text-align:center;
                     border-bottom:1px solid #2a2a3a;width:34%">STAT</th>
          <th style="background:#1a1a28;color:{c2_};font-family:Share Tech Mono,monospace;
                     padding:.6rem 1rem;text-align:left;border-bottom:2px solid {c2_};width:28%">{d2_}</th>
        </tr></thead><tbody>"""
        for stat_n, v1, v2, n1, n2, higher_wins in rows:
            w1  = (n1 > n2) if higher_wins else (n1 < n2)
            hl1 = f"color:{c1_};font-weight:700" if w1 else "color:#6a6a8a"
            hl2 = f"color:{c2_};font-weight:700" if not w1 else "color:#6a6a8a"
            h2h += f"""
            <tr style="border-bottom:1px solid #12121a">
              <td style="padding:.45rem 1rem;text-align:right;font-family:Share Tech Mono,monospace;{hl1}">{v1}</td>
              <td style="padding:.45rem;text-align:center;color:#5a5a7a;font-size:.72rem;
                         text-transform:uppercase;letter-spacing:.8px">{stat_n}</td>
              <td style="padding:.45rem 1rem;text-align:left;font-family:Share Tech Mono,monospace;{hl2}">{v2}</td>
            </tr>"""
        h2h += "</tbody></table></div>"
        st.markdown(h2h, unsafe_allow_html=True)
        st.divider()

    # Gear usage
    st.markdown("#### ⚙️ Gear Usage Distribution")
    fig_gear = go.Figure()
    for drv in drivers:
        pcts = [stats[drv]["gear_dist"].get(g, 0) for g in range(1, 9)]
        fig_gear.add_trace(go.Bar(
            x=[f"G{g}" for g in range(1, 9)], y=pcts, name=drv,
            marker_color=colors.get(drv, "#ffffff"),
            text=[f"{v:.0f}%" for v in pcts], textposition="outside",
        ))
    fig_gear.update_layout(**{
        **PLOTLY_LAYOUT,
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "% of lap"},
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Gear"},
        "title": dict(text="TIME IN EACH GEAR (% of lap samples)", font=dict(size=13, color="#6a6a8a"), x=0),
        "barmode": "group", "height": 320,
    })
    st.plotly_chart(fig_gear, use_container_width=True)
    st.divider()

    # Speed histogram
    st.markdown("#### 🚀 Speed Distribution")
    fig_hist = go.Figure()
    for drv in drivers:
        fig_hist.add_trace(go.Histogram(
            x=tels[drv]["Speed"], name=drv, nbinsx=40,
            marker_color=hex_to_rgba(colors.get(drv, "#ffffff"), 0.65), opacity=0.85,
        ))
    fig_hist.update_layout(**{
        **PLOTLY_LAYOUT,
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Speed (km/h)"},
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "Frequency"},
        "title": dict(text="SPEED DISTRIBUTION — FASTEST LAP", font=dict(size=13, color="#6a6a8a"), x=0),
        "barmode": "overlay", "height": 300, "hovermode": "x",
    })
    st.plotly_chart(fig_hist, use_container_width=True)


def _engineering_tab():
    st.markdown("### ⚙️ Engineering & Mechanics")
    st.caption("Technical reference for the systems visible in the telemetry data above.")
    st.divider()

    for section_title, entries in ENGINEERING_SECTIONS.items():
        st.markdown(f"#### {section_title}")
        eng_cols = st.columns(2)
        for j, (title, accent, body) in enumerate(entries):
            with eng_cols[j % 2]:
                st.markdown(f"""
                <div class="eng-card" style="--ac:{accent}">
                    <div class="eng-title">{title}</div>
                    <div class="eng-body">{body}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")

    st.divider()
    st.markdown("#### 📊 Track Status Codes")
    sc_cols = st.columns(len(TRACK_STATUS_MAP))
    for i, (code, (label, color)) in enumerate(TRACK_STATUS_MAP.items()):
        sc_cols[i].markdown(f"""
        <div style="background:#1a1a26;border:1px solid #2a2a3a;border-top:3px solid {color};
                    border-radius:4px;padding:.6rem .8rem;text-align:center">
            <div style="font-family:Share Tech Mono,monospace;font-size:1.5rem;color:{color}">{code}</div>
            <div style="font-size:.75rem;color:#c8c8d8;margin-top:.2rem">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def _radio_tab(session, drivers, colors):
    st.markdown("### 🎙️ Team Radio Messages")
    st.caption("Radio transcripts from the FastF1 historical data feed.")
    try:
        radio_df = session.race_control_messages
        if radio_df is None or len(radio_df) == 0:
            raise ValueError("empty")
        if "Category" in radio_df.columns:
            radio_df = radio_df[radio_df["Category"] != "Flag"].copy()

        st.markdown(f"**{len(radio_df)} messages found in this session**")
        st.divider()

        driver_filter = st.multiselect("Filter by driver", options=drivers + ["All"], default=["All"], key="radio_filter")
        radio_cols    = st.columns(2)
        shown = 0
        for _, row in radio_df.iterrows():
            if shown >= 40:
                break
            drv_abbr = str(row.get("Driver", ""))
            if "All" not in driver_filter and drv_abbr not in driver_filter:
                continue
            msg   = str(row.get("Message", ""))
            t     = row.get("Time", "")
            t_str = str(t)[:8] if t else ""
            dclr  = colors.get(drv_abbr, "#6a6a8a")
            with radio_cols[shown % 2]:
                st.markdown(f"""
                <div class="radio-card" style="--rc:{dclr}">
                    <div style="display:flex;justify-content:space-between">
                        <div class="radio-driver" style="color:{dclr}">{drv_abbr or 'RACE CTRL'}</div>
                        <div class="radio-time">{t_str}</div>
                    </div>
                    <div class="radio-msg">{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            shown += 1

        if shown == 0:
            st.info("No messages match the current filter.")
    except Exception:
        st.info("""
No radio messages available in this session's data.

FastF1 provides transcripts mainly for Race sessions.
For live audio, switch to **🔴 Live Mode**.
        """)


def _glossary_tab():
    st.markdown("### 📖 F1 Technical Glossary")
    st.markdown("Terms used in **team radio**, international broadcasts, and trackside engineering.")
    st.divider()
    gcols = st.columns(3)
    for i, (en, pt, desc) in enumerate(GLOSSARY):
        with gcols[i % 3]:
            st.markdown(f"""
            <div class="eng-card" style="--ac:#e10600">
                <div class="eng-title">{en}</div>
                <div class="eng-sub">{pt}</div>
                <div class="eng-body">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
