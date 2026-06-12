# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTS — drivers, teams, tyres, track status, Plotly layout
# ─────────────────────────────────────────────────────────────────────────────

DRIVER_COLORS = {
    "VER": "#3671C6", "PER": "#3671C6",
    "NOR": "#FF8000", "PIA": "#FF8000",
    "LEC": "#E8002D", "SAI": "#E8002D", "HAM": "#E8002D",
    "RUS": "#27F4D2", "ANT": "#27F4D2",
    "ALO": "#358C75", "STR": "#358C75",
    "GAS": "#2293D1", "DOO": "#2293D1",
    "ALB": "#64C4FF", "SAR": "#64C4FF", "COL": "#64C4FF",
    "TSU": "#6692FF", "HAD": "#6692FF", "LAW": "#6692FF",
    "HUL": "#B6BABD", "BEA": "#B6BABD",
    "BOT": "#C92D4B", "BOR": "#C92D4B",
}

DRIVER_TEAMS = {
    "VER": "Red Bull",     "PER": "Red Bull",
    "NOR": "McLaren",      "PIA": "McLaren",
    "LEC": "Ferrari",      "SAI": "Ferrari",      "HAM": "Ferrari",
    "RUS": "Mercedes",     "ANT": "Mercedes",
    "ALO": "Aston Martin", "STR": "Aston Martin",
    "GAS": "Alpine",       "DOO": "Alpine",
    "ALB": "Williams",     "SAR": "Williams",     "COL": "Williams",
    "TSU": "RB",           "HAD": "RB",           "LAW": "RB",
    "HUL": "Haas",         "BEA": "Haas",
    "BOT": "Kick Sauber",  "BOR": "Kick Sauber",
    "LIN": "Racing Bulls", "HAD": "Red Bull",
}

DRIVER_NUMBER_MAP = {
    1:  "VER",  4:  "NOR",  16: "LEC",  44: "HAM",  63: "RUS",
    11: "PER",  81: "PIA",  55: "SAI",  14: "ALO",  18: "STR",
    10: "GAS",  31: "OCO",  23: "ALB",   2: "SAR",  22: "TSU",
     3: "RIC",  27: "HUL",  20: "MAG",  77: "BOT",  24: "ZHO",
    87: "BEA",   7: "DOO",  43: "COL",   6: "HAD",  30: "LAW",
    12: "ANT",  50: "BOR",
}

TYRE_EMOJI = {
    "SOFT":         "🔴",
    "MEDIUM":       "🟡",
    "HARD":         "⚪",
    "INTERMEDIATE": "🟢",
    "WET":          "🔵",
}

TRACK_STATUS_MAP = {
    "1": ("Track Clear",        "#00e676"),
    "2": ("Yellow Flag",        "#ffd700"),
    "4": ("Safety Car",         "#ff8000"),
    "5": ("Red Flag",           "#ff0000"),
    "6": ("Virtual Safety Car", "#ff8000"),
}

TEAM_COLOR_MAP = {
    "mercedes":      "#27F4D2",
    "ferrari":       "#E8002D",
    "mclaren":       "#FF8000",
    "red bull":      "#3671C6",
    "alpine":        "#2293D1",
    "racing bulls":  "#6692FF",
    "rb":            "#6692FF",
    "haas":          "#B6BABD",
    "williams":      "#64C4FF",
    "audi":          "#D4AF37",
    "aston martin":  "#358C75",
    "cadillac":      "#CC0000",
    "kick sauber":   "#C92D4B",
}

SPRINT_ROUNDS_2026 = {2, 4, 5, 9, 12, 16}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0d0d16",
    font=dict(family="Rajdhani, sans-serif", color="#e8e8f0"),
    margin=dict(l=50, r=20, t=30, b=40),
    legend=dict(
        bgcolor="rgba(26,26,38,0.9)",
        bordercolor="#2a2a3a",
        borderwidth=1,
        font=dict(size=12),
    ),
    xaxis=dict(
        gridcolor="#1e1e2e",
        zerolinecolor="#2a2a3a",
        title_font=dict(size=11, color="#6a6a8a"),
        tickfont=dict(size=10, color="#6a6a8a"),
        showspikes=True,
        spikecolor="#ffffff",
        spikethickness=1,
        spikedash="dot",
    ),
    yaxis=dict(
        gridcolor="#1e1e2e",
        zerolinecolor="#2a2a3a",
        title_font=dict(size=11, color="#6a6a8a"),
        tickfont=dict(size=10, color="#6a6a8a"),
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#1a1a26",
        bordercolor="#2a2a3a",
        font=dict(family="Share Tech Mono", size=12, color="#e8e8f0"),
    ),
)
