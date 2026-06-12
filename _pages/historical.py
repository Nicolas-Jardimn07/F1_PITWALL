# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: Historical Analysis — via OpenF1 API (sem FastF1)
#  Funciona no Streamlit Cloud com Python 3.14
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

from _utils.constants import DRIVER_TEAMS, DRIVER_COLORS, TRACK_STATUS_MAP, PLOTLY_LAYOUT
from _utils.helpers import fmt_laptime, hex_to_rgba
from _data.content import ENGINEERING_SECTIONS, GLOSSARY

OPENF1 = "https://api.openf1.org/v1"

# Mapa de nomes do sidebar → nome da sessão na OpenF1
SESSION_NAME_MAP = {
    "Q":   "Qualifying",
    "R":   "Race",
    "S":   "Sprint",
    "FP1": "Practice 1",
    "FP2": "Practice 2",
    "FP3": "Practice 3",
}

COUNTRY_MAP = {
    "Australia": "Australia", "China": "China", "Japan": "Japan",
    "Bahrain": "Bahrain", "Saudi Arabia": "Saudi Arabia", "Miami": "United States",
    "Emilia Romagna": "Italy", "Monaco": "Monaco", "Spain": "Spain",
    "Canada": "Canada", "Austria": "Austria", "Great Britain": "Great Britain",
    "Belgium": "Belgium", "Hungary": "Hungary", "Netherlands": "Netherlands",
    "Italy": "Italy", "Azerbaijan": "Azerbaijan", "Singapore": "Singapore",
    "United States": "United States", "Mexico City": "Mexico", "São Paulo": "Brazil",
    "Las Vegas": "United States", "Qatar": "Qatar", "Abu Dhabi": "United Arab Emirates",
}


def _get(endpoint, params, timeout=15):
    try:
        r = requests.get(f"{OPENF1}/{endpoint}", params=params, timeout=timeout)
        r.raise_for_status()
        return r.json() or []
    except Exception:
        return []


@st.cache_data(ttl=3600, show_spinner=False)
def find_session_key(year: int, gp: str, stype: str) -> int | None:
    """Busca o session_key na OpenF1 para o GP e tipo de sessão."""
    country = COUNTRY_MAP.get(gp, gp)
    sess_name = SESSION_NAME_MAP.get(stype, stype)
    data = _get("sessions", {"year": year, "country_name": country, "session_name": sess_name})
    if not data:
        # Tenta pelo nome do circuito
        data = _get("sessions", {"year": year, "session_name": sess_name})
        data = [s for s in data if gp.lower() in s.get("circuit_short_name", "").lower()
                or gp.lower() in s.get("meeting_name", "").lower()]
    return data[0]["session_key"] if data else None


@st.cache_data(ttl=3600, show_spinner=False)
def get_drivers_openf1(session_key: int) -> list:
    """Retorna lista de drivers da sessão."""
    data = _get("drivers", {"session_key": session_key})
    return sorted([d["name_acronym"] for d in data if d.get("name_acronym")])


@st.cache_data(ttl=3600, show_spinner=False)
def get_fastest_lap_telemetry(session_key: int, driver: str) -> pd.DataFrame | None:
    """
    Busca a telemetria da volta mais rápida de um driver via OpenF1.
    Retorna DataFrame com Speed, Throttle, Brake, nGear, DRS, Distance.
    """
    # 1. Acha o número do driver
    drivers = _get("drivers", {"session_key": session_key})
    drv_num = next((d["driver_number"] for d in drivers
                    if d.get("name_acronym") == driver), None)
    if not drv_num:
        return None

    # 2. Acha a volta mais rápida
    laps = _get("laps", {"session_key": session_key, "driver_number": drv_num})
    if not laps:
        return None

    laps_df = pd.DataFrame(laps)
    laps_df = laps_df[laps_df["lap_duration"].notna()]
    if laps_df.empty:
        return None

    fastest = laps_df.loc[laps_df["lap_duration"].idxmin()]
    lap_num = int(fastest["lap_number"])
    lap_time = float(fastest["lap_duration"])

    # 3. Busca telemetria desta volta
    car_data = _get("car_data", {
        "session_key": session_key,
        "driver_number": drv_num,
        "lap_number": lap_num,
    })
    if not car_data:
        return None

    df = pd.DataFrame(car_data)
    if df.empty:
        return None

    # Renomeia colunas para compatibilidade com os gráficos existentes
    df = df.rename(columns={
        "speed":    "Speed",
        "throttle": "Throttle",
        "brake":    "Brake",
        "n_gear":   "nGear",
        "drs":      "DRS",
        "rpm":      "RPM",
    })

    # Calcula distância a partir do índice (aprox.)
    df = df.sort_values("date").reset_index(drop=True)
    df["Throttle"] = pd.to_numeric(df["Throttle"], errors="coerce").fillna(0)
    df["Brake"]    = pd.to_numeric(df["Brake"],    errors="coerce").fillna(0).astype(bool)
    df["nGear"]    = pd.to_numeric(df["nGear"],    errors="coerce").fillna(1)
    df["Speed"]    = pd.to_numeric(df["Speed"],    errors="coerce").fillna(0)
    df["DRS"]      = pd.to_numeric(df["DRS"],      errors="coerce").fillna(0)

    # Estima distância pela velocidade e intervalo de tempo
    df["Time"] = pd.to_datetime(df["date"])
    df["dt"]   = df["Time"].diff().dt.total_seconds().fillna(0.27)
    df["Distance"] = (df["Speed"] / 3.6 * df["dt"]).cumsum()

    # Guarda lap_time para métricas
    df.attrs["lap_time"]  = lap_time
    df.attrs["lap_number"] = lap_num

    return df


def get_driver_color(driver: str) -> str:
    return DRIVER_COLORS.get(driver, "#ffffff")


# ─────────────────────────────────────────────────────────────────────────────
#  Gráficos (idênticos ao código anterior)
# ─────────────────────────────────────────────────────────────────────────────

def make_speed_chart(tels: dict, colors: dict) -> go.Figure:
    fig = go.Figure()
    for drv, tel in tels.items():
        fig.add_trace(go.Scatter(
            x=tel["Distance"], y=tel["Speed"], mode="lines", name=drv,
            line=dict(color=colors[drv], width=2),
            hovertemplate=f"<b>{drv}</b><br>Dist: %{{x:.0f}} m<br>Speed: %{{y:.0f}} km/h<extra></extra>",
        ))
    fig.update_layout(**{**PLOTLY_LAYOUT,
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "Speed (km/h)"},
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Distance (m)"},
        "title": dict(text="SPEED TRACE — FASTEST LAP", font=dict(size=13, color="#6a6a8a"), x=0),
    })
    return fig


def make_inputs_chart(tels: dict, colors: dict) -> go.Figure:
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.4, 0.3, 0.3], vertical_spacing=0.06,
        subplot_titles=("THROTTLE (%)", "BRAKE (%)", "GEAR"))
    for drv, tel in tels.items():
        c = colors[drv]
        fig.add_trace(go.Scatter(x=tel["Distance"], y=tel["Throttle"],
            mode="lines", name=drv, line=dict(color=c, width=1.5), legendgroup=drv,
            hovertemplate=f"<b>{drv}</b> Throttle: %{{y:.0f}}%<extra></extra>"), row=1, col=1)
        fig.add_trace(go.Scatter(x=tel["Distance"], y=tel["Brake"].astype(int) * 100,
            mode="lines", name=drv, line=dict(color=c, width=1.5), legendgroup=drv, showlegend=False,
            hovertemplate=f"<b>{drv}</b> Brake: %{{y:.0f}}%<extra></extra>"), row=2, col=1)
        fig.add_trace(go.Scatter(x=tel["Distance"], y=tel["nGear"],
            mode="lines", name=drv, line=dict(color=c, width=1.5), legendgroup=drv, showlegend=False,
            hovertemplate=f"<b>{drv}</b> Gear: %{{y}}<extra></extra>"), row=3, col=1)
    B = PLOTLY_LAYOUT
    fig.update_layout(paper_bgcolor=B["paper_bgcolor"], plot_bgcolor=B["plot_bgcolor"],
        font=B["font"], margin=dict(l=50,r=20,t=40,b=40),
        legend=B["legend"], hovermode=B["hovermode"], hoverlabel=B["hoverlabel"], height=520)
    for ax in ["xaxis","xaxis2","xaxis3"]:
        fig.update_layout(**{ax: dict(gridcolor="#1e1e2e", tickfont=dict(color="#6a6a8a", size=10))})
    for ax in ["yaxis","yaxis2","yaxis3"]:
        fig.update_layout(**{ax: dict(gridcolor="#1e1e2e", tickfont=dict(color="#6a6a8a", size=10))})
    fig.update_xaxes(title_text="Distance (m)", row=3, col=1)
    fig.update_yaxes(range=[0, 102], row=1, col=1)
    fig.update_yaxes(range=[0, 105], row=2, col=1)
    fig.update_yaxes(range=[0.5, 8.5], dtick=1, row=3, col=1)
    return fig


def make_delta_chart(tels: dict, drivers: list, colors: dict) -> go.Figure:
    if len(drivers) < 2:
        return go.Figure()
    d1, d2 = drivers[0], drivers[1]
    t1, t2 = tels[d1], tels[d2]
    dist = np.linspace(max(t1["Distance"].min(), t2["Distance"].min()),
                       min(t1["Distance"].max(), t2["Distance"].max()), 500)
    s1 = np.interp(dist, t1["Distance"], t1["Speed"])
    s2 = np.interp(dist, t2["Distance"], t2["Speed"])
    dt = np.diff(dist)
    tt1 = np.cumsum(np.append(0, dt / (s1[:-1] / 3.6)))
    tt2 = np.cumsum(np.append(0, dt / (s2[:-1] / 3.6)))
    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color="#ffffff", width=1, dash="dot"))
    fig.add_trace(go.Scatter(x=dist, y=tt1-tt2, mode="lines", name=f"{d1} vs {d2}",
        line=dict(color="#ffd700", width=2), fill="tozeroy", fillcolor="rgba(255,215,0,0.08)",
        hovertemplate="Dist: %{x:.0f} m<br>Delta: %{y:.3f} s<extra></extra>"))
    fig.update_layout(**{**PLOTLY_LAYOUT,
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "Delta (s)"},
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Distance (m)"},
        "title": dict(text=f"DELTA TIME — {d1} vs {d2}", font=dict(size=13, color="#6a6a8a"), x=0),
    })
    return fig


def make_minisectors_chart(tels: dict, drivers: list, colors: dict, n: int = 25) -> go.Figure:
    if len(drivers) < 2:
        return go.Figure()
    d1, d2 = drivers[0], drivers[1]
    t1, t2 = tels[d1], tels[d2]
    dmax = min(t1["Distance"].max(), t2["Distance"].max())
    bins = np.linspace(0, dmax, n + 1)
    winners = []
    for i in range(n):
        m1 = (t1["Distance"] >= bins[i]) & (t1["Distance"] < bins[i+1])
        m2 = (t2["Distance"] >= bins[i]) & (t2["Distance"] < bins[i+1])
        a1 = t1.loc[m1, "Speed"].mean() if m1.any() else 0
        a2 = t2.loc[m2, "Speed"].mean() if m2.any() else 0
        winners.append(d1 if a1 >= a2 else d2)
    fig = go.Figure()
    for i, w in enumerate(winners):
        fig.add_shape(type="rect", x0=bins[i], x1=bins[i+1], y0=0, y1=1,
                      fillcolor=hex_to_rgba(colors[w], 0.85), line=dict(width=0))
        fig.add_shape(type="rect", x0=bins[i], x1=bins[i+1], y0=0, y1=1,
                      fillcolor="rgba(0,0,0,0)", line=dict(color="#0a0a0f", width=1))
    for drv in [d1, d2]:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            marker=dict(size=12, color=colors[drv], symbol="square"), name=f"{drv} fastest"))
    fig.update_layout(**{**PLOTLY_LAYOUT,
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Distance (m)"},
        "yaxis": dict(visible=False, range=[0, 1]),
        "title": dict(text="MINI-SECTOR ADVANTAGE", font=dict(size=13, color="#6a6a8a"), x=0),
        "height": 100, "margin": dict(l=50, r=20, t=30, b=40),
    })
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def render(year: int, gp_name: str, session_type: str, session_code: str, analyze: bool):

    # Reset ao mudar seleção
    cur_sel = (year, gp_name, session_code)
    if st.session_state.last_selection != cur_sel:
        st.session_state.session        = None
        st.session_state.drivers        = []
        st.session_state.last_selection = cur_sel

    if analyze:
        with st.spinner(f"⏳ Buscando {gp_name} {year} — {session_type} na OpenF1..."):
            sk = find_session_key(year, gp_name, session_code)
            if not sk:
                st.error(f"❌ Sessão não encontrada na OpenF1. "
                         f"A OpenF1 cobre apenas 2023 em diante. "
                         f"Tente: 2023, 2024 ou 2025.")
                return
            drivers = get_drivers_openf1(sk)
            if not drivers:
                st.error("❌ Nenhum piloto encontrado para esta sessão.")
                return
            st.session_state.session = sk
            st.session_state.drivers = drivers
            st.success(f"✅ Sessão encontrada (key: {sk}) — {len(drivers)} pilotos disponíveis.")

    if st.session_state.session is None:
        _splash()
        return

    session_key = st.session_state.session
    available   = st.session_state.drivers

    # Seleção de pilotos
    def safe_idx(lst, val, fb=0):
        return lst.index(val) if val in lst else fb

    c1, c2 = st.columns(2)
    with c1:
        d1 = st.selectbox("🔵 Driver A", available,
                          index=safe_idx(available, "VER", 0), key="d1")
    with c2:
        d2 = st.selectbox("🟠 Driver B", available,
                          index=safe_idx(available, "NOR", min(1, len(available)-1)), key="d2")

    drivers = [d1, d2] if d1 != d2 else [d1]
    colors  = {drv: get_driver_color(drv) for drv in drivers}

    # Carrega telemetria
    tels = {}
    with st.spinner("📡 Buscando telemetria da volta mais rápida..."):
        for drv in drivers:
            tel = get_fastest_lap_telemetry(session_key, drv)
            if tel is not None and not tel.empty:
                tels[drv] = tel
            else:
                st.warning(f"⚠️ Sem telemetria para {drv}")

    if not tels:
        st.error("Sem dados de telemetria. Tente outra sessão ou pilotos.")
        return

    # Métricas
    st.markdown("### Lap Metrics")
    mc = st.columns(len(drivers) * 3 + (1 if len(drivers) == 2 else 0))
    ci = 0
    for drv in drivers:
        tel = tels[drv]
        lt  = tel.attrs.get("lap_time")
        mc[ci].metric(f"⏱️ {drv} · {DRIVER_TEAMS.get(drv,'')}", fmt_laptime(lt)); ci += 1
        mc[ci].metric(f"🚀 Top Speed {drv}", f"{int(tel['Speed'].max())} km/h");   ci += 1
        mc[ci].metric(f"🎮 Avg Throttle {drv}", f"{int(tel['Throttle'].mean())}%"); ci += 1

    if len(drivers) == 2 and all(tels[d].attrs.get("lap_time") for d in drivers):
        gap = tels[drivers[1]].attrs["lap_time"] - tels[drivers[0]].attrs["lap_time"]
        mc[ci].metric("⚡ Gap", f"{gap:+.3f}s",
                      delta=f"{drivers[1]} {'behind' if gap > 0 else 'ahead'}",
                      delta_color="inverse")
    st.divider()

    # Abas de análise
    (tab_speed, tab_inputs, tab_delta, tab_mini,
     tab_stats, tab_eng, tab_gloss) = st.tabs([
        "📈 Speed Trace", "🎮 Driver Inputs", "⏱️ Delta Time",
        "🗺️ Mini-Sectors", "📊 Lap Stats", "⚙️ Engineering", "📖 F1 Glossary",
    ])

    with tab_speed:
        st.plotly_chart(make_speed_chart(tels, colors), use_container_width=True)
        with st.expander("💡 Como ler — Speed Trace"):
            st.markdown("- **Picos** = retas em aceleração máxima\n"
                        "- **Vales** = zonas de frenagem\n"
                        "- **Diferença entre as linhas** = quem freia mais tarde ou acelera antes")

    with tab_inputs:
        st.plotly_chart(make_inputs_chart(tels, colors), use_container_width=True)

    with tab_delta:
        if len(drivers) == 2:
            st.plotly_chart(make_delta_chart(tels, drivers, colors), use_container_width=True)
        else:
            st.info("Selecione dois pilotos diferentes para ver o Delta Time.")

    with tab_mini:
        if len(drivers) == 2:
            st.plotly_chart(make_minisectors_chart(tels, drivers, colors), use_container_width=True)
        else:
            st.info("Selecione dois pilotos diferentes.")

    with tab_stats:
        _lap_stats_tab(tels, drivers, colors)

    with tab_eng:
        _engineering_tab()

    with tab_gloss:
        _glossary_tab()


# ─────────────────────────────────────────────────────────────────────────────
#  Sub-funções
# ─────────────────────────────────────────────────────────────────────────────

def _splash():
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem">
        <div style="font-size:4rem">🏎️</div>
        <h2 style="color:#e10600;letter-spacing:3px;margin:.5rem 0">READY FOR ANALYSIS</h2>
        <p style="color:#6a6a8a;font-size:1rem">
            Selecione temporada, GP e sessão na barra lateral.<br>
            Clique <strong style="color:#e10600">▶ ANALYZE</strong> para buscar os dados.<br><br>
            <span style="color:#4a4a6a;font-size:.85rem">⚠️ Dados disponíveis apenas a partir de 2023 (OpenF1 API)</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def _lap_stats(tel) -> dict:
    ft_pct    = round((tel["Throttle"] >= 98).mean() * 100, 1)
    brk_pct   = round(tel["Brake"].astype(bool).mean() * 100, 1)
    coast_pct = round(float(((tel["Throttle"] < 5) & (~tel["Brake"].astype(bool))).mean()) * 100, 1)
    drs_pct   = round((tel["DRS"] >= 8).mean() * 100, 1)
    gear_cnt  = tel["nGear"].value_counts().sort_index().to_dict()
    gear_tot  = max(sum(gear_cnt.values()), 1)
    return dict(
        laptime   = tel.attrs.get("lap_time"),
        dist      = float(tel["Distance"].max()),
        ft_pct    = ft_pct, brk_pct=brk_pct,
        coast_pct = coast_pct, drs_pct=drs_pct,
        top_spd   = int(tel["Speed"].max()),
        min_spd   = int(tel["Speed"].min()),
        avg_spd   = round(float(tel["Speed"].mean()), 1),
        avg_thr   = round(float(tel.loc[tel["Throttle"] > 0, "Throttle"].mean()), 1),
        brk_ev    = int(((tel["Brake"].astype(int).diff() > 0)).sum()),
        gear_ch   = int((tel["nGear"].diff().abs() > 0).sum()),
        gear_dist = {g: round(gear_cnt.get(g, 0) / gear_tot * 100, 1) for g in range(1, 9)},
    )


def _lap_stats_tab(tels, drivers, colors):
    st.markdown("### 📊 Lap Statistics")
    st.divider()
    stats = {drv: _lap_stats(tels[drv]) for drv in drivers}

    ov = st.columns(len(drivers))
    for i, drv in enumerate(drivers):
        s    = stats[drv]
        dclr = colors.get(drv, "#fff")
        lt_s = fmt_laptime(s["laptime"]) if s["laptime"] else "N/A"
        with ov[i]:
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #1e1e32;border-top:4px solid {dclr};
                        border-radius:10px;padding:1rem;text-align:center">
                <div style="color:{dclr};font-weight:700;font-size:1.4rem;letter-spacing:3px">{drv}</div>
                <div style="font-size:.68rem;color:#6a6a8a;margin:.2rem 0">{DRIVER_TEAMS.get(drv,'')}</div>
                <div style="font-family:Share Tech Mono,monospace;font-size:2rem;color:#fff;margin:.4rem 0">{lt_s}</div>
                <div style="font-size:.7rem;color:#6a6a8a">{s['dist']:.0f} m</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    if len(drivers) == 2:
        d1_, d2_ = drivers[0], drivers[1]
        s1,  s2  = stats[d1_], stats[d2_]
        c1_, c2_ = colors.get(d1_, "#fff"), colors.get(d2_, "#fff")
        st.markdown("#### 📋 Head-to-Head")
        rows = [
            ("Top Speed",       f"{s1['top_spd']} km/h", f"{s2['top_spd']} km/h", s1['top_spd'],   s2['top_spd'],   True),
            ("Avg Speed",       f"{s1['avg_spd']} km/h", f"{s2['avg_spd']} km/h", s1['avg_spd'],   s2['avg_spd'],   True),
            ("Full Throttle %", f"{s1['ft_pct']}%",      f"{s2['ft_pct']}%",      s1['ft_pct'],    s2['ft_pct'],    True),
            ("Avg Throttle",    f"{s1['avg_thr']}%",     f"{s2['avg_thr']}%",     s1['avg_thr'],   s2['avg_thr'],   True),
            ("Time Braking",    f"{s1['brk_pct']}%",     f"{s2['brk_pct']}%",     s2['brk_pct'],   s1['brk_pct'],   False),
            ("Coasting",        f"{s1['coast_pct']}%",   f"{s2['coast_pct']}%",   s2['coast_pct'], s1['coast_pct'], False),
            ("DRS Active",      f"{s1['drs_pct']}%",     f"{s2['drs_pct']}%",     s1['drs_pct'],   s2['drs_pct'],   True),
            ("Gear Changes",    str(s1['gear_ch']),       str(s2['gear_ch']),       0,               0,               False),
        ]
        h2h = (f"<div style='background:#0d0d18;border:1px solid #1e1e32;border-radius:10px;overflow:hidden'>"
               f"<table style='width:100%;border-collapse:collapse;font-size:.88rem'>"
               f"<thead><tr>"
               f"<th style='background:#1a1a28;color:{c1_};font-family:Share Tech Mono,monospace;"
               f"padding:.6rem 1rem;text-align:right;border-bottom:2px solid {c1_};width:28%'>{d1_}</th>"
               f"<th style='background:#1a1a28;color:#6a6a8a;font-size:.65rem;text-transform:uppercase;"
               f"padding:.6rem;text-align:center;border-bottom:1px solid #2a2a3a;width:34%'>STAT</th>"
               f"<th style='background:#1a1a28;color:{c2_};font-family:Share Tech Mono,monospace;"
               f"padding:.6rem 1rem;text-align:left;border-bottom:2px solid {c2_};width:28%'>{d2_}</th>"
               f"</tr></thead><tbody>")
        for stat_n, v1, v2, n1, n2, hw in rows:
            w1  = (n1 > n2) if hw else (n1 < n2)
            hl1 = f"color:{c1_};font-weight:700" if w1 else "color:#6a6a8a"
            hl2 = f"color:{c2_};font-weight:700" if not w1 else "color:#6a6a8a"
            h2h += (f"<tr style='border-bottom:1px solid #12121a'>"
                    f"<td style='padding:.45rem 1rem;text-align:right;font-family:Share Tech Mono,monospace;{hl1}'>{v1}</td>"
                    f"<td style='padding:.45rem;text-align:center;color:#5a5a7a;font-size:.72rem;"
                    f"text-transform:uppercase;letter-spacing:.8px'>{stat_n}</td>"
                    f"<td style='padding:.45rem 1rem;text-align:left;font-family:Share Tech Mono,monospace;{hl2}'>{v2}</td>"
                    f"</tr>")
        h2h += "</tbody></table></div>"
        st.markdown(h2h, unsafe_allow_html=True)
        st.divider()

    # Gear chart
    st.markdown("#### ⚙️ Gear Usage")
    fig_gear = go.Figure()
    for drv in drivers:
        pcts = [stats[drv]["gear_dist"].get(g, 0) for g in range(1, 9)]
        fig_gear.add_trace(go.Bar(
            x=[f"G{g}" for g in range(1, 9)], y=pcts, name=drv,
            marker_color=colors.get(drv, "#fff"),
            text=[f"{v:.0f}%" for v in pcts], textposition="outside",
        ))
    fig_gear.update_layout(**{**PLOTLY_LAYOUT,
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "% of lap"},
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Gear"},
        "title": dict(text="TIME IN EACH GEAR", font=dict(size=13, color="#6a6a8a"), x=0),
        "barmode": "group", "height": 300,
    })
    st.plotly_chart(fig_gear, use_container_width=True)


def _engineering_tab():
    st.markdown("### ⚙️ Engineering & Mechanics")
    st.caption("Referência técnica dos sistemas visíveis na telemetria.")
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


def _glossary_tab():
    st.markdown("### 📖 F1 Technical Glossary")
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
