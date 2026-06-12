# ─────────────────────────────────────────────────────────────────────────────
#  DATA — FastF1 loaders + OpenF1 live API
# ─────────────────────────────────────────────────────────────────────────────
import os
import fastf1
import pandas as pd
import requests
import streamlit as st

CACHE_DIR   = "./f1_cache_local"
OPENF1_BASE = "https://api.openf1.org/v1"

os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)


# ─────────────────────────────────────────────────────────────────────────────
#  FastF1 — Historical
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_session_f1(year: int, gp: str, stype: str):
    sess = fastf1.get_session(year, gp, stype)
    sess.load(telemetry=True, weather=True, messages=False)
    return sess


@st.cache_data(show_spinner=False)
def get_driver_list(_sess) -> list:
    return sorted(_sess.laps["Driver"].unique().tolist())


@st.cache_data(show_spinner=False)
def get_telemetry(_sess, driver: str):
    lap = _sess.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry().add_distance()
    return tel, lap


@st.cache_data(show_spinner=False)
def get_all_telemetry(_sess, drivers: tuple) -> dict:
    """Load GPS + sensor telemetry for all drivers. Adds 'T' column (seconds)."""
    result = {}
    for drv in drivers:
        try:
            lap = _sess.laps.pick_drivers(drv).pick_fastest()
            tel = lap.get_telemetry().add_distance()
            tel["T"] = tel["Time"].dt.total_seconds()
            result[drv] = tel
        except Exception:
            pass
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  OpenF1 — Live
# ─────────────────────────────────────────────────────────────────────────────

def openf1_get(endpoint: str, params: dict = None, timeout: int = 8) -> list:
    """Generic OpenF1 GET — returns list, empty list on any error."""
    try:
        r = requests.get(
            f"{OPENF1_BASE}/{endpoint}",
            params=params,
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json() or []
    except Exception:
        return []


def of1_session() -> dict | None:
    d = openf1_get("sessions", {"session_key": "latest"})
    return d[0] if d else None

def of1_positions(sk)  -> list: return openf1_get("position",     {"session_key": sk, "date": "latest"})
def of1_intervals(sk)  -> list: return openf1_get("intervals",    {"session_key": sk, "date": "latest"})
def of1_drivers(sk)    -> list: return openf1_get("drivers",      {"session_key": sk})
def of1_laps(sk)       -> list: return openf1_get("laps",         {"session_key": sk})
def of1_pits(sk)       -> list: return openf1_get("pit",          {"session_key": sk})
def of1_rc(sk)         -> list: return openf1_get("race_control", {"session_key": sk})
def of1_stints(sk)     -> list: return openf1_get("stints",       {"session_key": sk})
def of1_team_radio(sk) -> list: return openf1_get("team_radio",   {"session_key": sk})

def of1_car(sk, num) -> list:
    return openf1_get("car_data", {"session_key": sk, "driver_number": num, "date": "latest"})

def of1_weather(sk) -> dict | None:
    d = openf1_get("weather", {"session_key": sk, "date": "latest"})
    return d[0] if d else None
