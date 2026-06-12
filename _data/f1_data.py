
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
#
#  IMPORTANTE: usar @st.cache_resource (não @st.cache_data) para objetos
#  FastF1 Session — o cache_data tenta serializar o objeto e perde os dados
#  carregados. O cache_resource mantém o objeto vivo em memória.
# ─────────────────────────────────────────────────────────────────────────────
 
@st.cache_resource(show_spinner=False)
def load_session_f1(year: int, gp: str, stype: str):
    """Carrega e retorna uma Session FastF1 completa com telemetria."""
    sess = fastf1.get_session(year, gp, stype)
    sess.load(telemetry=True, weather=True, messages=False)
    return sess
 
 
def get_driver_list(sess) -> list:
    """Retorna lista ordenada de drivers na sessão."""
    return sorted(sess.laps["Driver"].unique().tolist())
 
 
def get_telemetry(sess, driver: str):
    """Retorna telemetria da volta mais rápida do driver."""
    lap = sess.laps.pick_drivers(driver).pick_fastest()
    tel = lap.get_telemetry().add_distance()
    return tel, lap
 
 
def get_all_telemetry(sess, drivers: tuple) -> dict:
    """Carrega telemetria GPS para todos os drivers. Adiciona coluna 'T' (segundos)."""
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
 
