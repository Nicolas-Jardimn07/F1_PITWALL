# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: English Study Room
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from _data.content import (
    RADIO_PHRASES,
    INTERVIEW_PHRASES,
    BROADCAST_VOCAB,
    PODIUM_INTERVIEW_SCRIPT,
)


def render():
    st.markdown("## 🎓 F1 English Study Room")
    st.caption("Team radio phrases · Broadcast vocabulary · Podium interviews · Race day language")
    st.divider()

    etab1, etab2, etab3, etab4 = st.tabs([
        "📻 Team Radio Phrases",
        "🎙️ Interview Expressions",
        "📡 Broadcast Vocabulary",
        "🏆 Podium Interview Script",
    ])

    with etab1:
        _render_radio()

    with etab2:
        _render_interviews()

    with etab3:
        _render_broadcast()

    with etab4:
        _render_script()


# ─────────────────────────────────────────────────────────────────────────────
#  Sub-sections
# ─────────────────────────────────────────────────────────────────────────────

def _render_radio():
    st.markdown("### 📻 Most Common Team Radio Phrases")
    st.caption("Phrases you'll hear in every race broadcast — with context, translation and who says them.")
    st.divider()

    search  = st.text_input("🔍 Search phrase or keyword", placeholder="e.g. tyre, push, delta...", key="radio_search")
    phrases = RADIO_PHRASES
    if search:
        phrases = [
            p for p in phrases
            if search.lower() in p[0].lower()
            or search.lower() in p[1].lower()
            or search.lower() in p[3].lower()
        ]

    for phrase, context, pt, who in phrases:
        who_color = (
            "#3671C6" if "Engineer" in who and "→ Driver" in who
            else "#FF8000" if "Driver" in who and "→ Engineer" in who
            else "#6a6a8a"
        )
        st.markdown(f"""
        <div style="background:#12121a;border:1px solid #2a2a3a;border-left:4px solid #e10600;
                    border-radius:6px;padding:.9rem 1.1rem;margin-bottom:.8rem">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap">
                <div style="font-family:Share Tech Mono,monospace;font-size:1rem;color:#fff;font-weight:700">
                    🎙️ "{phrase}"
                </div>
                <div style="background:rgba(255,255,255,.06);border-radius:3px;padding:2px 8px;
                            font-size:.65rem;color:{who_color};letter-spacing:1px;white-space:nowrap">{who}</div>
            </div>
            <div style="font-size:.82rem;color:#9a9ab0;margin:.4rem 0;line-height:1.5">{context}</div>
            <div style="font-size:.78rem;color:#6a6a8a;border-top:1px solid #1e1e2e;padding-top:.35rem;margin-top:.35rem">
                🇧🇷 <em>{pt}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not phrases:
        st.info("No phrases match your search. Try a different keyword.")


def _render_interviews():
    st.markdown("### 🎙️ F1 Interview Expressions")
    st.caption("Phrases drivers and team bosses use in every post-race press conference and trackside interview.")
    st.divider()

    for phrase, context, pt in INTERVIEW_PHRASES:
        st.markdown(f"""
        <div style="background:#12121a;border:1px solid #2a2a3a;border-left:4px solid #FF8000;
                    border-radius:6px;padding:.9rem 1.1rem;margin-bottom:.8rem">
            <div style="font-family:Share Tech Mono,monospace;font-size:.95rem;color:#FF8000;font-weight:700;margin-bottom:.35rem">
                💬 "{phrase}"
            </div>
            <div style="font-size:.82rem;color:#c8c8d8;margin-bottom:.35rem;line-height:1.5">{context}</div>
            <div style="font-size:.78rem;color:#6a6a8a;border-top:1px solid #1e1e2e;padding-top:.35rem">
                🇧🇷 <em>{pt}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_broadcast():
    st.markdown("### 📡 Broadcast Vocabulary")
    st.caption("Technical terms used by commentators (Sky Sports F1, F1 TV) during live races.")
    st.divider()

    cols = st.columns(2)
    for i, (term, definition, pt) in enumerate(BROADCAST_VOCAB):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:#12121a;border:1px solid #2a2a3a;border-top:2px solid #27F4D2;
                        border-radius:6px;padding:.8rem 1rem;margin-bottom:.7rem">
                <div style="font-weight:700;color:#27F4D2;font-size:.95rem;font-family:Share Tech Mono,monospace">{term}</div>
                <div style="font-size:.8rem;color:#c8c8d8;margin:.3rem 0;line-height:1.4">{definition}</div>
                <div style="font-size:.72rem;color:#6a6a8a">🇧🇷 {pt}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_script():
    st.markdown("### 🏆 Podium Interview — Full Script")
    st.caption("A real podium interview follows this structure almost every time. Learn the pattern.")
    st.divider()

    st.markdown(f"""
    <div style="background:#0d0d16;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem 2rem;
                font-size:.9rem;line-height:1.8;color:#c8c8d8;font-family:Rajdhani,sans-serif">
        <pre style="white-space:pre-wrap;font-family:Rajdhani,sans-serif;font-size:.9rem;
                    line-height:1.8;color:#c8c8d8;background:transparent;border:none;padding:0">{PODIUM_INTERVIEW_SCRIPT}</pre>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🔑 Key Phrases")
    key_phrases = [
        ("massive thanks to the whole team", "Standard winner opener",             "#ffd700"),
        ("manage the race / tyres",           "Controlled driving, not flat-out",   "#00e676"),
        ("the gap was closing",               "Leader feeling pressure from behind", "#ff8000"),
        ("to be honest",                      "Discourse filler before direct answer","#FF8000"),
        ("maximised our points",              "Got everything possible today",       "#00e676"),
        ("go through the data",               "Post-race analysis in factory",       "#3671C6"),
        ("long season",                       "Downplaying importance of one race",  "#ff8000"),
        ("safety car window",                 "Strategic pit opportunity under SC",  "#ff8000"),
        ("race pace",                         "Sustained lap time over many laps",   "#3671C6"),
    ]
    kp_cols = st.columns(3)
    for i, (kp, meaning, col) in enumerate(key_phrases):
        with kp_cols[i % 3]:
            st.markdown(f"""
            <div style="background:#1a1a26;border-left:3px solid {col};border-radius:4px;
                        padding:.5rem .75rem;margin-bottom:.5rem">
                <div style="font-family:Share Tech Mono,monospace;font-size:.8rem;color:{col}">{kp}</div>
                <div style="font-size:.72rem;color:#9a9ab0;margin-top:.2rem">{meaning}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 💡 Study Tips")
    st.info("""
**How to use this section to improve your F1 English:**

1. **Watch with subtitles first** — Sky Sports F1 has English CC. Read while listening.
2. **Radio focus** — During live races, listen for the exact phrases listed in the Radio tab above.
3. **Pattern recognition** — Notice how drivers answer: opener → explanation → team credit.
4. **Repeat out loud** — "Box, box, box" / "Copy that" / "The gap is closing".
5. **Telemetry connection** — When you see a speed drop on the Speed Trace, the radio phrase is *"we had a lock-up into Turn 3"*.
    """)
