# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS — formatting, interpolation, color, track geometry
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import fastf1
import fastf1.plotting
from _utils.constants import DRIVER_COLORS


def fmt_laptime(seconds) -> str:
    """Convert raw seconds to 'M:SS.mmm' string."""
    try:
        s = float(seconds)
        if s != s:           # NaN check
            return "N/A"
        return f"{int(s // 60)}:{s % 60:06.3f}"
    except Exception:
        return "N/A"


def hex_to_rgba(h: str, a: float = 0.85) -> str:
    """'#RRGGBB' → 'rgba(r,g,b,a)'."""
    h = h.lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{a})"
    return h


def get_driver_color(driver: str, session=None) -> str:
    """Return FastF1 colour with fallback to our DRIVER_COLORS dict."""
    try:
        return fastf1.plotting.get_driver_color(driver, session=session)
    except Exception:
        return DRIVER_COLORS.get(driver, "#ffffff")


def build_track_outline(tel_ref: pd.DataFrame) -> tuple:
    """Smooth GPS X/Y columns into a clean track outline."""
    x = (
        pd.Series(tel_ref["X"].values.astype(float))
        .rolling(8, center=True, min_periods=1)
        .mean()
        .values
    )
    y = (
        pd.Series(tel_ref["Y"].values.astype(float))
        .rolling(8, center=True, min_periods=1)
        .mean()
        .values
    )
    return x, y


def interpolate_position(tel: pd.DataFrame, t_sec: float) -> tuple:
    """
    Linearly interpolate (X, Y, Speed, Gear, Throttle, Brake, DRS)
    at time t_sec (seconds from lap start).
    Requires a pre-computed 'T' column (tel['Time'].dt.total_seconds()).
    """
    ts = tel["T"].values

    if t_sec <= ts[0]:
        r = tel.iloc[0]
        return (
            float(r["X"]), float(r["Y"]), float(r["Speed"]),
            int(r["nGear"]), float(r["Throttle"]), bool(r["Brake"]), int(r["DRS"]),
        )
    if t_sec >= ts[-1]:
        r = tel.iloc[-1]
        return (
            float(r["X"]), float(r["Y"]), float(r["Speed"]),
            int(r["nGear"]), float(r["Throttle"]), bool(r["Brake"]), int(r["DRS"]),
        )

    idx = int(np.searchsorted(ts, t_sec))
    idx = min(max(idx, 1), len(ts) - 1)
    t0, t1 = ts[idx - 1], ts[idx]
    a = (t_sec - t0) / (t1 - t0) if t1 > t0 else 0.0

    def lerp(col):
        return tel[col].iloc[idx - 1] * (1 - a) + tel[col].iloc[idx] * a

    return (
        lerp("X"),
        lerp("Y"),
        lerp("Speed"),
        int(round(lerp("nGear"))),
        lerp("Throttle"),
        bool(tel["Brake"].iloc[idx]),
        int(tel["DRS"].iloc[idx]),
    )
