# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: News — RSS feed + standings, podium, calendar, storylines
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from _utils.constants import DRIVER_COLORS, DRIVER_TEAMS
from _data.news_fetcher import fetch_f1_news, filter_f1_articles
from _data.season_data import get_season_data


def render():
    st.markdown("### 📰 F1 2026 — Latest News")
    st.caption("Aggregated from Autosport, Motorsport.com and Racer · Refreshed every 30 minutes")

    with st.spinner("📡 Fetching latest F1 news..."):
        articles = fetch_f1_news()

    if not articles:
        st.warning("""
⚠️ Could not reach the news feeds right now.

Try these sources directly:
- [Autosport F1](https://www.autosport.com/f1/)
- [Motorsport.com F1](https://www.motorsport.com/f1/)
- [The Race](https://www.therace.com/)
- [Racefans.net](https://www.racefans.net/)
        """)
    else:
        display = filter_f1_articles(articles)
        st.markdown(f"**{len(display)} articles found** · scroll down for more")
        st.divider()

        _, feed_col, _ = st.columns([1, 4, 1])
        with feed_col:
            for art in display:
                href     = art["link"] if art["link"] else "#"
                img      = art.get("image", "")
                img_html = (
                    f'<img class="news-img" src="{img}" alt="">'
                    if img else
                    '<div class="news-img-placeholder">🏎️</div>'
                )
                st.markdown(f"""
                <a href="{href}" target="_blank" style="text-decoration:none">
                <div class="news-card">
                    {img_html}
                    <div class="news-body">
                        <div class="news-source-badge">{art["source"]}</div>
                        <div class="news-title">{art["title"]}</div>
                        <div class="news-desc">{art["desc"]}</div>
                        <div class="news-footer">
                            <div class="news-date">{art["date"]}</div>
                            <div class="news-read-more">Read more →</div>
                        </div>
                    </div>
                </div>
                </a>
                """, unsafe_allow_html=True)

    _render_extras()


def _render_extras():
    _drv_st, _con_st, _cal, _lr = get_season_data()

    # ── Standings
    st.markdown("---")
    st.markdown("## 🏆 Championship Standings — 2026")
    st.caption(f"After Round 6: Monaco GP · {_lr['date']}")
    sc1, sc2 = st.columns(2)

    with sc1:
        st.markdown("#### Drivers")
        max_pts = _drv_st[0][3]
        for pos, drv, team, pts, wins in _drv_st:
            dclr  = DRIVER_COLORS.get(drv, "#ffffff")
            bar_w = round(pts / max_pts * 100)
            w_txt = f'<span style="color:#ffd700;font-size:.65rem;margin-left:.3rem">{wins}W</span>' if wins else ""
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f'<span style="color:#4a4a6a">{pos}</span>'
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.35rem">
                <div style="width:22px;text-align:center;font-size:.78rem">{medal}</div>
                <div style="font-weight:700;color:{dclr};font-family:Share Tech Mono,monospace;font-size:.82rem;width:38px">{drv}</div>
                <div style="font-size:.68rem;color:#5a5a7a;width:88px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{team}</div>
                <div style="flex:1;background:#12121e;border-radius:3px;height:5px;overflow:hidden">
                    <div style="background:{dclr};height:100%;width:{bar_w}%;border-radius:3px"></div>
                </div>
                <div style="font-family:Share Tech Mono,monospace;font-size:.82rem;color:#fff;width:44px;text-align:right">{pts}{w_txt}</div>
            </div>
            """, unsafe_allow_html=True)

    with sc2:
        st.markdown("#### Constructors")
        max_c = _con_st[0][2]
        for pos, team, pts, color in _con_st:
            bar_w = round(pts / max_c * 100)
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f'<span style="color:#4a4a6a">{pos}</span>'
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.35rem">
                <div style="width:22px;text-align:center;font-size:.78rem">{medal}</div>
                <div style="font-weight:700;color:{color};font-size:.82rem;width:100px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{team}</div>
                <div style="flex:1;background:#12121e;border-radius:3px;height:5px;overflow:hidden">
                    <div style="background:{color};height:100%;width:{bar_w}%;border-radius:3px"></div>
                </div>
                <div style="font-family:Share Tech Mono,monospace;font-size:.82rem;color:#fff;width:40px;text-align:right">{pts}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Last race podium
    st.markdown("---")
    st.markdown("## 🏁 Last Race — Monaco GP")
    lr     = _lr
    podium = [
        (lr["winner"], "🥇 P1", DRIVER_COLORS.get(lr["winner"], "#ffd700")),
        (lr["p2"],     "🥈 P2", DRIVER_COLORS.get(lr["p2"],     "#c0c0c0")),
        (lr["p3"],     "🥉 P3", DRIVER_COLORS.get(lr["p3"],     "#cd7f32")),
    ]
    for col, (drv, label, dclr) in zip(st.columns(3), podium):
        with col:
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #1e1e30;border-top:4px solid {dclr};
                        border-radius:10px;padding:1rem;text-align:center">
                <div style="font-size:1.5rem">{label}</div>
                <div style="font-family:Share Tech Mono,monospace;font-size:1.6rem;font-weight:700;color:{dclr};margin:.3rem 0">{drv}</div>
                <div style="font-size:.75rem;color:#6a6a8a">{DRIVER_TEAMS.get(drv, "")}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#0a0a14;border:1px solid #1e1e30;border-radius:8px;
                padding:.8rem 1.1rem;margin-top:.75rem;font-size:.82rem;color:#8a8aaa;line-height:1.6">
        <span style="color:#ffd700;font-size:.65rem;font-weight:700;letter-spacing:1px">⚡ FASTEST LAP</span>
        &nbsp; {lr["fl"]} — {lr["fl_time"]}
        &nbsp;&nbsp;|&nbsp;&nbsp; {lr["highlight"]}
    </div>
    """, unsafe_allow_html=True)

    # ── Season stats
    st.markdown("---")
    st.markdown("## 📊 Season at a Glance")
    done  = [r for r in _cal if r[4] == "done"]
    total = len(_cal)
    pct   = round(len(done) / total * 100)

    for col, label, val in zip(
        st.columns(5),
        ["Races Done", "Championship Ldr", "Ldr Wins", "Ldr Points", "Gap to P2"],
        [f"{len(done)} / {total}", "ANT", "5", "156", "+66 pts"],
    ):
        col.metric(label, val)

    st.markdown(f"""
    <div style="background:#12121e;border-radius:6px;height:8px;overflow:hidden;margin:.5rem 0 1.5rem">
        <div style="background:linear-gradient(90deg,#e10600,#ff6600);height:100%;width:{pct}%;border-radius:6px"></div>
    </div>
    <div style="text-align:center;font-size:.7rem;color:#4a4a6a;margin-bottom:1rem">
        {pct}% of the 2026 season complete
    </div>
    """, unsafe_allow_html=True)

    # ── Upcoming races
    st.markdown("## 📅 Upcoming Races")
    upcoming = [r for r in _cal if r[4] in ("next", "upcoming")][:6]
    ur_cols  = st.columns(3)
    for i, (rnd, name, circuit, date_str, status, is_sprint) in enumerate(upcoming):
        border = "#e10600" if status == "next" else "#1e1e30"
        bg     = "#0d0d18" if status == "next" else "#0a0a14"
        next_badge = (
            '<span style="background:#e10600;color:#fff;font-size:.5rem;font-weight:700;'
            'padding:1px 6px;border-radius:10px;margin-left:.3rem">NEXT</span>'
            if status == "next" else ""
        )
        sprint_badge = (
            '<span style="background:rgba(255,215,0,.12);color:#ffd700;font-size:.5rem;'
            'font-weight:700;padding:1px 5px;border-radius:8px;margin-left:.3rem">★ SPRINT</span>'
            if is_sprint else ""
        )
        with ur_cols[i % 3]:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:8px;padding:.75rem .9rem;margin-bottom:.6rem">
                <div style="font-size:.58rem;color:#6a6a8a;font-family:Share Tech Mono,monospace;margin-bottom:.2rem">
                    R{rnd:02d} · {date_str}
                </div>
                <div style="font-size:.9rem;font-weight:700;color:#e8e8f0;line-height:1.3">
                    {name}{next_badge}{sprint_badge}
                </div>
                <div style="font-size:.68rem;color:#5a5a7a;margin-top:.2rem">{circuit}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Key storylines
    st.markdown("---")
    st.markdown("## 🔑 Key Storylines — 2026")
    stories = [
        ("🟦 Antonelli's Dominance",               "#27F4D2",
         "Kimi Antonelli, 19, has won every race from pole. 5 wins in 6 races — the most dominant "
         "start by a rookie in F1 history. Mercedes' new 2026 power unit appears significantly ahead of rivals."),
        ("🔴 Ferrari's Hamilton Gamble Paying Off", "#E8002D",
         "Lewis Hamilton, in his first Ferrari season at 41, is P2 in the championship. Two podiums "
         "in Monaco and consistent points haul vindicating Ferrari's controversial signing."),
        ("🟠 McLaren's Regulation Struggle",        "#FF8000",
         "Defending champions McLaren sit P3 in constructors after a difficult transition to the 2026 regs. "
         "Norris had two DNFs in back-to-back races. Piastri carrying the team's points."),
        ("🔵 Verstappen's Horror Start",            "#3671C6",
         "Verstappen P7 in the championship after 6 rounds. Three DNFs including a lap-1 retirement in Monaco. "
         "Red Bull's Ford power unit described as 'not competitive enough yet'."),
        ("⭐ Madrid Grand Prix Debut",               "#ffd700",
         "A brand new street circuit in the Spanish capital makes its F1 debut in September (R14). "
         "The Madring circuit replaces Imola. Subject to final FIA approval."),
        ("🇺🇸 Cadillac's First F1 Season",          "#64C4FF",
         "General Motors' Cadillac team joins as the 11th constructor. Perez was set to score their "
         "first point in Monaco before a post-race penalty. Bottas is their second driver."),
    ]
    st_cols = st.columns(2)
    for i, (title, color, body) in enumerate(stories):
        with st_cols[i % 2]:
            st.markdown(f"""
            <div style="background:#0a0a14;border:1px solid #1e1e30;border-left:4px solid {color};
                        border-radius:8px;padding:.85rem 1rem;margin-bottom:.75rem">
                <div style="font-weight:700;color:#e8e8f0;font-size:.92rem;margin-bottom:.35rem">{title}</div>
                <div style="font-size:.8rem;color:#7a7a9a;line-height:1.55">{body}</div>
            </div>
            """, unsafe_allow_html=True)
