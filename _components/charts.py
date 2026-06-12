# ─────────────────────────────────────────────────────────────────────────────
#  COMPONENTS: Plotly chart builders — speed, inputs, delta, mini-sectors
# ─────────────────────────────────────────────────────────────────────────────
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from _utils.constants import PLOTLY_LAYOUT
from _utils.helpers import hex_to_rgba, build_track_outline, interpolate_position


def make_speed_chart(tels: dict, colors: dict) -> go.Figure:
    fig = go.Figure()
    for drv, tel in tels.items():
        fig.add_trace(go.Scatter(
            x=tel["Distance"],
            y=tel["Speed"],
            mode="lines",
            name=drv,
            line=dict(color=colors[drv], width=2),
            hovertemplate=f"<b>{drv}</b><br>Dist: %{{x:.0f}} m<br>Speed: %{{y:.0f}} km/h<extra></extra>",
        ))
    fig.update_layout(**{
        **PLOTLY_LAYOUT,
        "yaxis": {**PLOTLY_LAYOUT["yaxis"], "title": "Speed (km/h)"},
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Distance (m)"},
        "title": dict(text="SPEED TRACE — FASTEST LAP", font=dict(size=13, color="#6a6a8a"), x=0),
    })
    return fig


def make_inputs_chart(tels: dict, colors: dict) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.4, 0.3, 0.3], vertical_spacing=0.06,
        subplot_titles=("THROTTLE (%)", "BRAKE (%)", "GEAR"),
    )
    for drv, tel in tels.items():
        c = colors[drv]
        fig.add_trace(go.Scatter(
            x=tel["Distance"], y=tel["Throttle"], mode="lines", name=drv,
            line=dict(color=c, width=1.5), legendgroup=drv,
            hovertemplate=f"<b>{drv}</b> Throttle: %{{y:.0f}}%<extra></extra>",
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=tel["Distance"], y=tel["Brake"].astype(int) * 100, mode="lines", name=drv,
            line=dict(color=c, width=1.5), legendgroup=drv, showlegend=False,
            hovertemplate=f"<b>{drv}</b> Brake: %{{y:.0f}}%<extra></extra>",
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=tel["Distance"], y=tel["nGear"], mode="lines", name=drv,
            line=dict(color=c, width=1.5), legendgroup=drv, showlegend=False,
            hovertemplate=f"<b>{drv}</b> Gear: %{{y}}<extra></extra>",
        ), row=3, col=1)

    B = PLOTLY_LAYOUT
    fig.update_layout(
        paper_bgcolor=B["paper_bgcolor"], plot_bgcolor=B["plot_bgcolor"],
        font=B["font"], margin=dict(l=50, r=20, t=40, b=40),
        legend=B["legend"], hovermode=B["hovermode"], hoverlabel=B["hoverlabel"], height=520,
    )
    for ax in ["xaxis", "xaxis2", "xaxis3"]:
        fig.update_layout(**{ax: dict(gridcolor="#1e1e2e", tickfont=dict(color="#6a6a8a", size=10))})
    for ax in ["yaxis", "yaxis2", "yaxis3"]:
        fig.update_layout(**{ax: dict(gridcolor="#1e1e2e", tickfont=dict(color="#6a6a8a", size=10))})
    fig.update_xaxes(title_text="Distance (m)", row=3, col=1)
    fig.update_yaxes(range=[0, 102],   row=1, col=1)
    fig.update_yaxes(range=[0, 105],   row=2, col=1)
    fig.update_yaxes(range=[0.5, 8.5], dtick=1, row=3, col=1)
    return fig


def make_delta_chart(tels: dict, drivers: list, colors: dict) -> go.Figure:
    if len(drivers) < 2:
        return go.Figure()

    d1, d2 = drivers[0], drivers[1]
    t1, t2 = tels[d1], tels[d2]
    dist = np.linspace(
        max(t1["Distance"].min(), t2["Distance"].min()),
        min(t1["Distance"].max(), t2["Distance"].max()),
        500,
    )
    s1  = np.interp(dist, t1["Distance"], t1["Speed"])
    s2  = np.interp(dist, t2["Distance"], t2["Speed"])
    dt  = np.diff(dist)
    tt1 = np.cumsum(np.append(0, dt / (s1[:-1] / 3.6)))
    tt2 = np.cumsum(np.append(0, dt / (s2[:-1] / 3.6)))

    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color="#ffffff", width=1, dash="dot"))
    fig.add_trace(go.Scatter(
        x=dist, y=tt1 - tt2, mode="lines",
        name=f"{d1} vs {d2}",
        line=dict(color="#ffd700", width=2),
        fill="tozeroy", fillcolor="rgba(255,215,0,0.08)",
        hovertemplate="Dist: %{x:.0f} m<br>Delta: %{y:.3f} s<extra></extra>",
    ))
    fig.update_layout(**{
        **PLOTLY_LAYOUT,
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
    dmax   = min(t1["Distance"].max(), t2["Distance"].max())
    bins   = np.linspace(0, dmax, n + 1)

    winners = []
    for i in range(n):
        m1 = (t1["Distance"] >= bins[i]) & (t1["Distance"] < bins[i + 1])
        m2 = (t2["Distance"] >= bins[i]) & (t2["Distance"] < bins[i + 1])
        a1 = t1.loc[m1, "Speed"].mean() if m1.any() else 0
        a2 = t2.loc[m2, "Speed"].mean() if m2.any() else 0
        winners.append(d1 if a1 >= a2 else d2)

    fig = go.Figure()
    for i, w in enumerate(winners):
        fig.add_shape(type="rect", x0=bins[i], x1=bins[i + 1], y0=0, y1=1,
                      fillcolor=hex_to_rgba(colors[w], 0.85), line=dict(width=0))
        fig.add_shape(type="rect", x0=bins[i], x1=bins[i + 1], y0=0, y1=1,
                      fillcolor="rgba(0,0,0,0)", line=dict(color="#0a0a0f", width=1))
    for drv in [d1, d2]:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
            marker=dict(size=12, color=colors[drv], symbol="square"), name=f"{drv} fastest"))

    fig.update_layout(**{
        **PLOTLY_LAYOUT,
        "xaxis": {**PLOTLY_LAYOUT["xaxis"], "title": "Distance (m)"},
        "yaxis": dict(visible=False, range=[0, 1]),
        "title": dict(text="MINI-SECTOR ADVANTAGE", font=dict(size=13, color="#6a6a8a"), x=0),
        "height": 100, "margin": dict(l=50, r=20, t=30, b=40),
    })
    return fig


def make_replay_frame(
    all_tels: dict,
    t_now: float,
    drivers_render: list,
    show_trail: bool,
    colors: dict,
) -> go.Figure:
    """One Plotly frame for the track map replay at time t_now."""
    ref_drv = drivers_render[0]
    tx, ty  = build_track_outline(all_tels[ref_drv])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tx, y=ty, mode="lines",
        line=dict(color="#2a2a3a", width=14), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=tx, y=ty, mode="lines",
        line=dict(color="#0f0f1a", width=9), showlegend=False, hoverinfo="skip"))

    for drv in drivers_render:
        tel  = all_tels[drv]
        dclr = colors.get(drv, "#ffffff")

        if show_trail:
            mask  = (tel["T"] >= t_now - 4.0) & (tel["T"] <= t_now)
            trail = tel[mask]
            if len(trail) > 1:
                for k in range(len(trail) - 1):
                    seg  = trail.iloc[k:k + 2]
                    spd  = float(seg["Speed"].mean())
                    norm = min(max(spd / 320.0, 0), 1)
                    r_c  = int(norm * 255)
                    g_c  = int((1 - abs(norm - 0.5) * 2) * 255)
                    b_c  = int((1 - norm) * 120)
                    fig.add_trace(go.Scatter(
                        x=seg["X"].tolist(), y=seg["Y"].tolist(), mode="lines",
                        line=dict(color=f"rgb({r_c},{g_c},{b_c})", width=4),
                        showlegend=False, hoverinfo="skip",
                    ))

        px, py, spd, gear, thr, brk, drs = interpolate_position(tel, t_now)
        fig.add_trace(go.Scatter(
            x=[px], y=[py], mode="markers+text", name=drv,
            marker=dict(size=16, color=dclr, line=dict(color="#ffffff", width=2), symbol="circle"),
            text=[drv], textposition="top center",
            textfont=dict(size=10, color=dclr, family="Share Tech Mono"),
            hovertemplate=(
                f"<b>{drv}</b><br>Speed: {spd:.0f} km/h · Gear: {gear}<br>"
                f"Throttle: {thr:.0f}% · Brake: {'ON' if brk else 'OFF'}<br>"
                f"DRS: {'OPEN' if drs >= 8 else 'CLOSED'}<extra></extra>"
            ),
        ))

    fig.add_trace(go.Scatter(
        x=[tx[0]], y=[ty[0]], mode="markers", name="S/F Line",
        marker=dict(size=14, color="#ffffff", symbol="line-ew", line=dict(width=3, color="#ffffff")),
        showlegend=True, hoverinfo="skip",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0a0a0f",
        font=dict(family="Rajdhani, sans-serif", color="#e8e8f0"),
        margin=dict(l=10, r=10, t=40, b=10), height=620,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        legend=dict(bgcolor="rgba(26,26,38,0.92)", bordercolor="#2a2a3a",
                    borderwidth=1, font=dict(size=11), x=1.01, y=1),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#1a1a26", bordercolor="#2a2a3a",
                        font=dict(family="Share Tech Mono", size=12, color="#e8e8f0")),
    )
    return fig
