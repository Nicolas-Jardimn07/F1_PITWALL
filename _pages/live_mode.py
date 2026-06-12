# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: Live Mode — OpenF1 real-time data (~3-5s delay)
# ─────────────────────────────────────────────────────────────────────────────
import time
import streamlit as st
from datetime import datetime, timezone

from _utils.constants import DRIVER_COLORS, DRIVER_NUMBER_MAP, TYRE_EMOJI
from _utils.helpers import fmt_laptime
from _data.f1_data import (
    of1_session, of1_positions, of1_intervals, of1_drivers,
    of1_laps, of1_pits, of1_rc, of1_stints, of1_car,
    of1_weather, of1_team_radio,
)


def render(live_filter: list, refresh_interval: str):
    live_sess = of1_session()

    if not live_sess:
        st.warning("⚠️ No active F1 session detected via OpenF1.")
        st.info("""
**Live Mode works during:**
- Practice, Qualifying or Race on an active GP weekend
- OpenF1 streams data with ~3–5 seconds of delay

**Outside race weekends:** use 📊 Historical Analysis mode.

Check status: https://api.openf1.org
        """)
        return

    sk          = live_sess.get("session_key")
    sess_name   = live_sess.get("session_name",  "?")
    gp_live     = live_sess.get("meeting_name",  "?")
    year_live   = live_sess.get("year",          "")
    sess_status = str(live_sess.get("session_status") or "unknown")
    sc_color    = (
        "#00e676" if sess_status == "started"
        else "#ff8000" if sess_status == "finished"
        else "#6a6a8a"
    )
    now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S")

    st.markdown(f"""
    <div style="background:#1a1a26;border:1px solid #2a2a3a;border-radius:4px;
                padding:.8rem 1.2rem;display:flex;gap:2.5rem;align-items:center;
                margin-bottom:1rem;flex-wrap:wrap">
        <div>
            <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px">Session</div>
            <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#fff">{gp_live} — {sess_name} {year_live}</div>
        </div>
        <div>
            <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px">Status</div>
            <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:{sc_color};text-transform:uppercase">{sess_status}</div>
        </div>
        <div style="margin-left:auto;font-size:.75rem;color:#6a6a8a;font-family:Share Tech Mono,monospace">
            Updated: {now_utc} UTC
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch all live data
    with st.spinner("📡 Fetching live data from OpenF1..."):
        positions   = of1_positions(sk)  or []
        intervals   = of1_intervals(sk)  or []
        drivers_raw = of1_drivers(sk)    or []
        laps_raw    = of1_laps(sk)       or []
        pits_raw    = of1_pits(sk)       or []
        rc_msgs     = of1_rc(sk)         or []
        weather     = of1_weather(sk)
        stints_raw  = of1_stints(sk)     or []
        radio_raw   = of1_team_radio(sk) or []

    # ── Driver lookup dict
    drv_lkp = {}
    for d in drivers_raw:
        num  = d.get("driver_number")
        abbr = d.get("name_acronym") or DRIVER_NUMBER_MAP.get(num, str(num))
        drv_lkp[num] = {
            "abbr":  abbr,
            "name":  d.get("full_name", abbr),
            "team":  d.get("team_name", ""),
            "color": f"#{d.get('team_colour') or 'ffffff'}",
        }

    iv_map  = {iv.get("driver_number"): iv for iv in intervals}
    lp_map  = {lp.get("driver_number"): lp for lp in laps_raw}
    st_map  = {s.get("driver_number"):  s  for s  in stints_raw}
    pit_map = {}
    for p in pits_raw:
        pit_map.setdefault(p.get("driver_number"), []).append(p)

    ltab1, ltab2, ltab3, ltab4 = st.tabs([
        "🏁 Timing Tower",
        "📡 Car Telemetry",
        "📻 Race Control & Radio",
        "🌤️ Weather",
    ])

    with ltab1:
        _timing_tower(positions, drv_lkp, iv_map, lp_map, st_map, pit_map, live_filter)

    with ltab2:
        _car_telemetry(sk, drv_lkp, live_filter)

    with ltab3:
        _race_control(rc_msgs, radio_raw, drv_lkp)

    with ltab4:
        _weather(weather)

    # ── Auto-refresh footer
    st.divider()
    rf1, rf2 = st.columns([4, 1])
    with rf1:
        cycle = st.session_state.get("live_refresh_count", 0) + 1
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} · Cycle #{cycle}")
    with rf2:
        if st.button("🔄 Refresh Now"):
            st.session_state.live_refresh_count = cycle
            st.rerun()

    refresh_sec = int(refresh_interval.replace("s", ""))
    time.sleep(refresh_sec)
    st.session_state.live_refresh_count = cycle
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  Sub-sections
# ─────────────────────────────────────────────────────────────────────────────

def _timing_tower(positions, drv_lkp, iv_map, lp_map, st_map, pit_map, live_filter):
    st.markdown("### 🏁 Live Timing Tower")
    pos_sorted = sorted(positions, key=lambda x: x.get("position", 99))
    filter_set = set(live_filter) if live_filter else set()
    rows_html  = ""

    for p in pos_sorted:
        num  = p.get("driver_number")
        pos  = p.get("position", "—")
        info = drv_lkp.get(num, {"abbr": str(num), "team": "", "color": "#ffffff"})
        abbr = info["abbr"]
        if filter_set and abbr not in filter_set:
            continue

        color   = info.get("color") or DRIVER_COLORS.get(abbr, "#ffffff")
        iv      = iv_map.get(num, {})
        gap_raw = iv.get("gap_to_leader")
        gap_str = (
            "LEADER" if gap_raw == 0 or (gap_raw is None and pos == 1)
            else f"+{gap_raw:.3f}s" if isinstance(gap_raw, float)
            else str(gap_raw) if gap_raw else "—"
        )
        ivl_raw = iv.get("interval")
        ivl_str = (
            f"+{ivl_raw:.3f}s" if isinstance(ivl_raw, float)
            else str(ivl_raw) if ivl_raw else "—"
        )
        lp     = lp_map.get(num, {})
        stint  = st_map.get(num, {})
        comp   = str(stint.get("compound") or "—")
        t_icon = TYRE_EMOJI.get(comp, "⬜")
        pits   = len(pit_map.get(num, []))
        lt     = lp.get("lap_duration")
        s1     = lp.get("duration_sector_1")
        s2     = lp.get("duration_sector_2")
        s3     = lp.get("duration_sector_3")
        pc     = f"pos-{pos}" if pos in [1, 2, 3] else ""

        rows_html += f"""
        <tr>
            <td class="{pc}">{pos}</td>
            <td style="color:{color};font-weight:700">{abbr}</td>
            <td style="color:#9a9ab0;font-size:.75rem">{info.get('team', '')}</td>
            <td>{gap_str}</td>
            <td>{ivl_str}</td>
            <td>{lp.get('lap_number', '—')}</td>
            <td>{fmt_laptime(lt) if lt else '—'}</td>
            <td>{f'{s1:.3f}' if s1 else '—'}</td>
            <td>{f'{s2:.3f}' if s2 else '—'}</td>
            <td>{f'{s3:.3f}' if s3 else '—'}</td>
            <td>{t_icon} {comp}</td>
            <td>{pits}</td>
        </tr>"""

    if rows_html:
        st.markdown(f"""
        <table class="pos-table"><thead><tr>
        <th>POS</th><th>DRIVER</th><th>TEAM</th><th>GAP</th><th>INT</th>
        <th>LAP</th><th>LAP TIME</th><th>S1</th><th>S2</th><th>S3</th>
        <th>TYRE</th><th>STOPS</th>
        </tr></thead><tbody>{rows_html}</tbody></table>
        """, unsafe_allow_html=True)
    else:
        st.info("No position data available yet for this session.")


def _car_telemetry(sk, drv_lkp, live_filter):
    st.markdown("### 📡 Live Car Telemetry")
    num_rev = {v: k for k, v in DRIVER_NUMBER_MAP.items()}
    tracked = live_filter if live_filter else list(DRIVER_NUMBER_MAP.values())[:4]
    tel_cols = st.columns(min(len(tracked), 4))
    any_data = False

    for i, abbr in enumerate(tracked[:4]):
        dnum = num_rev.get(abbr)
        if not dnum:
            continue
        td_list = of1_car(sk, dnum)
        if not td_list:
            continue
        td       = td_list[-1]
        any_data = True
        dclr     = drv_lkp.get(dnum, {}).get("color") or DRIVER_COLORS.get(abbr, "#fff")

        with tel_cols[i]:
            spd  = td.get("speed",    "—")
            gear = td.get("n_gear",   "—")
            thr  = td.get("throttle", "—")
            brk  = td.get("brake",    0)
            drs  = td.get("drs",      0)
            rpm  = td.get("rpm",      "—")
            st.markdown(f"""
            <div style="background:#1a1a26;border:1px solid #2a2a3a;
                        border-top:3px solid {dclr};border-radius:4px;padding:.9rem 1rem">
                <div style="color:{dclr};font-weight:700;font-size:1.15rem;letter-spacing:2px;margin-bottom:.6rem">{abbr}</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem">
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Speed</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1.4rem;color:#fff">{spd} <span style="font-size:.7rem;color:#6a6a8a">km/h</span></div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Gear</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1.4rem;color:#fff">{gear}</div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Throttle</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1.2rem;color:#00e676">{thr}%</div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">Brake</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1.2rem;color:{'#ff4444' if brk else '#6a6a8a'}">{'ON' if brk else 'OFF'}</div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">DRS</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:{'#00e676' if drs and drs > 8 else '#6a6a8a'}">{'OPEN' if drs and drs > 8 else 'CLOSED'}</div>
                    </div>
                    <div>
                        <div style="font-size:.6rem;color:#6a6a8a;text-transform:uppercase">RPM</div>
                        <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#fff">{rpm}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if not any_data:
        st.info("No live car telemetry available. Data is only streamed during an active session.")


def _race_control(rc_msgs, radio_raw, drv_lkp):
    rc1, rc2 = st.columns(2)

    with rc1:
        st.markdown("### 📻 Race Control Messages")
        if rc_msgs:
            for msg in reversed(rc_msgs[-10:]):
                flag = str(msg.get("flag")     or "")
                cat  = str(msg.get("category") or "")
                txt  = str(msg.get("message")  or "")
                col  = (
                    "#ff0000" if "RED"    in flag
                    else "#ffd700" if "YELLOW" in flag or "SAFETY" in cat
                    else "#00e676" if "GREEN"  in flag or "DRS"    in cat
                    else "#6a6a8a"
                )
                st.markdown(
                    f'<div class="radio-card" style="--rc:{col}"><div style="color:{col};font-size:.8rem">{txt}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No race control messages yet.")

    with rc2:
        st.markdown("### 🎙️ Team Radio")
        if radio_raw:
            for r in reversed(radio_raw[-10:]):
                drv_num   = r.get("driver_number")
                abbr      = drv_lkp.get(drv_num, {}).get("abbr", str(drv_num))
                dclr      = drv_lkp.get(drv_num, {}).get("color") or DRIVER_COLORS.get(abbr, "#ffffff")
                date_str  = str(r.get("date") or "")[:19].replace("T", " ")
                audio_url = r.get("recording_url", "")
                st.markdown(f"""
                <div class="radio-card" style="--rc:{dclr}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div class="radio-driver" style="color:{dclr}">{abbr}</div>
                        <div class="radio-time">{date_str}</div>
                    </div>
                    <div class="radio-msg">🎙️ Radio transmission recorded</div>
                </div>
                """, unsafe_allow_html=True)
                if audio_url:
                    st.audio(audio_url)
        else:
            st.info("No team radio data available yet.\nAudio clips appear here during/after active sessions.")


def _weather(weather):
    st.markdown("### 🌤️ Track Conditions")
    if weather:
        wc = st.columns(6)
        wc[0].metric("🌡️ Air Temp",   f"{weather.get('air_temperature',   '—')}°C")
        wc[1].metric("🛣️ Track Temp", f"{weather.get('track_temperature', '—')}°C")
        wc[2].metric("💧 Humidity",   f"{weather.get('humidity',           '—')}%")
        wc[3].metric("🌬️ Wind Speed", f"{weather.get('wind_speed',         '—')} m/s")
        wc[4].metric("🌧️ Rainfall",   "YES" if weather.get("rainfall") else "NO")
        wc[5].metric("💨 Pressure",   f"{weather.get('pressure',           '—')} mbar")
    else:
        st.info("No weather data available yet.")
