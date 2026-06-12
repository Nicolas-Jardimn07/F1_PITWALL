# ─────────────────────────────────────────────────────────────────────────────
#  DATA — FastF1 loaders + OpenF1 live API
# ─────────────────────────────────────────────────────────────────────────────
import os
import asyncio
import fastf1
import requests
import streamlit as st

# Fix para Python 3.14+ onde o event loop do asyncio mudou
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

# Workaround adicional para Python 3.14 asyncio
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

CACHE_DIR   = "./f1_cache_local"
OPENF1_BASE = "https://api.openf1.org/v1"

os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)


# ─────────────────────────────────────────────────────────────────────────────
#  FastF1 — Historical
# ─────────────────────────────────────────────────────────────────────────────

def load_session_f1(year: int, gp: str, stype: str):
    """Carrega e retorna uma Session FastF1 completa."""
    cache_key = f"f1sess_{year}_{gp}_{stype}"

    if cache_key in st.session_state:
        sess = st.session_state[cache_key]
        try:
            _ = sess.laps
            return sess
        except Exception:
            del st.session_state[cache_key]

    sess = fastf1.get_session(year, gp, stype)
    sess.load(telemetry=True, weather=True, messages=False)
    st.session_state[cache_key] = sess
    return sess


def get_driver_list(sess) -> list:
    return sorted(sess.laps["Driver"].unique().tolist())


def get_telemetry(sess, driver: str):
    lap = sess.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry().add_distance()
    return tel, lap


def get_all_telemetry(sess, drivers: tuple) -> dict:
    result = {}
    for drv in drivers:
        try:
            lap = sess.laps.pick_drivers(drv).pick_fastest()
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
