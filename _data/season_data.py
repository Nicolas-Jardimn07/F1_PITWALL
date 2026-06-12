# ─────────────────────────────────────────────────────────────────────────────
#  SEASON DATA — Ergast API (standings, calendar, last race)
#  Cached 1 hour. Falls back to hardcoded 2026 data if API is unreachable.
# ─────────────────────────────────────────────────────────────────────────────
import requests
import streamlit as st
from datetime import datetime, timezone
from _utils.constants import TEAM_COLOR_MAP, SPRINT_ROUNDS_2026

ERGAST_BASE  = "https://ergast.com/api/f1"
CURRENT_YEAR = 2026


def _ergast_get(path: str, timeout: int = 8) -> dict:
    try:
        r = requests.get(
            f"{ERGAST_BASE}/{path}.json",
            params={"limit": 100},
            timeout=timeout,
            headers={"Accept": "application/json"},
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


# ─────────────────────────────────────────────────────────────────────────────
#  Public fetchers (each cached independently)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_driver_standings(year: int = CURRENT_YEAR) -> list:
    """Returns list of (pos, code, team, points, wins)."""
    data = _ergast_get(f"{year}/driverStandings")
    try:
        table = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
        result = []
        for entry in table:
            drv_id = entry["Driver"]["driverId"]
            code   = entry["Driver"].get("code", drv_id[:3].upper())
            team   = entry["Constructors"][0]["name"] if entry["Constructors"] else "—"
            pts    = int(float(entry["points"]))
            wins   = int(entry["wins"])
            pos    = int(entry["position"])
            result.append((pos, code, team, pts, wins))
        return result
    except (KeyError, IndexError, TypeError):
        return _fallback_driver_standings()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_constructor_standings(year: int = CURRENT_YEAR) -> list:
    """Returns list of (pos, team, points, color)."""
    data = _ergast_get(f"{year}/constructorStandings")
    try:
        table = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
        result = []
        for entry in table:
            team  = entry["Constructor"]["name"]
            pts   = int(float(entry["points"]))
            pos   = int(entry["position"])
            color = TEAM_COLOR_MAP.get(team.lower(), "#ffffff")
            result.append((pos, team, pts, color))
        return result
    except (KeyError, IndexError, TypeError):
        return _fallback_constructor_standings()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_calendar(year: int = CURRENT_YEAR) -> list:
    """Returns list of (round, name, circuit, date, status, is_sprint).
    status: 'done' | 'next' | 'upcoming'
    """
    data  = _ergast_get(f"{year}")
    today = datetime.now(timezone.utc).date()
    try:
        races    = data["MRData"]["RaceTable"]["Races"]
        result   = []
        next_set = False
        for race in races:
            rnd      = int(race["round"])
            name     = race["raceName"].replace(" Grand Prix", " GP")
            circuit  = race["Circuit"]["circuitName"]
            date_str = race["date"]
            try:
                race_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                race_date = today
            is_sprint = rnd in SPRINT_ROUNDS_2026
            if race_date < today:
                status = "done"
            elif not next_set:
                status   = "next"
                next_set = True
            else:
                status = "upcoming"
            result.append((rnd, name, circuit, date_str, status, is_sprint))
        return result if result else _fallback_calendar()
    except (KeyError, IndexError, TypeError):
        return _fallback_calendar()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_last_race(year: int = CURRENT_YEAR) -> dict:
    """Returns dict with winner, p2, p3, fastest lap, circuit, date."""
    data = _ergast_get(f"{year}/last/results")
    try:
        race    = data["MRData"]["RaceTable"]["Races"][0]
        results = race["Results"]

        def get_code(r):
            return r["Driver"].get("code", r["Driver"]["driverId"][:3].upper())

        p1 = get_code(results[0])
        p2 = get_code(results[1])
        p3 = get_code(results[2])

        fl_drv, fl_time = "—", "—"
        for r in results:
            if r.get("FastestLap", {}).get("rank") == "1":
                fl_drv  = get_code(r)
                fl_time = r["FastestLap"]["Time"]["time"]
                break

        return {
            "name":      race["raceName"],
            "circuit":   race["Circuit"]["circuitName"],
            "date":      race["date"],
            "winner":    p1,
            "p2":        p2,
            "p3":        p3,
            "fl":        fl_drv,
            "fl_time":   fl_time,
            "highlight": f"Round {race['round']} · {race['Circuit']['Location']['country']}",
        }
    except (KeyError, IndexError, TypeError):
        return _fallback_last_race()


def get_season_data() -> tuple:
    """Single call → (driver_standings, constructor_standings, calendar, last_race)."""
    return (
        fetch_driver_standings(),
        fetch_constructor_standings(),
        fetch_calendar(),
        fetch_last_race(),
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Fallback data (hardcoded 2026, used when Ergast is unreachable)
# ─────────────────────────────────────────────────────────────────────────────

def _fallback_driver_standings() -> list:
    return [
        (1,  "ANT", "Mercedes",      156, 5),
        (2,  "HAM", "Ferrari",        90, 0),
        (3,  "RUS", "Mercedes",       88, 0),
        (4,  "LEC", "Ferrari",        75, 0),
        (5,  "PIA", "McLaren",        60, 0),
        (6,  "NOR", "McLaren",        58, 0),
        (7,  "VER", "Red Bull",       43, 0),
        (8,  "HAD", "Red Bull",       29, 0),
        (9,  "LAW", "Racing Bulls",   26, 0),
        (10, "GAS", "Alpine",         26, 0),
        (11, "BEA", "Haas",           18, 0),
        (12, "COL", "Alpine",         15, 0),
        (13, "LIN", "Racing Bulls",   13, 0),
        (14, "SAI", "Williams",        6, 0),
        (15, "ALB", "Williams",        5, 0),
        (16, "OCO", "Haas",            3, 0),
        (17, "BOR", "Audi",            2, 0),
        (18, "ALO", "Aston Martin",    1, 0),
    ]


def _fallback_constructor_standings() -> list:
    return [
        (1,  "Mercedes",      244, "#27F4D2"),
        (2,  "Ferrari",       165, "#E8002D"),
        (3,  "McLaren",       118, "#FF8000"),
        (4,  "Red Bull",       72, "#3671C6"),
        (5,  "Alpine",         41, "#2293D1"),
        (6,  "Racing Bulls",   39, "#6692FF"),
        (7,  "Haas",           21, "#B6BABD"),
        (8,  "Williams",       11, "#64C4FF"),
        (9,  "Audi",            2, "#D4AF37"),
        (10, "Aston Martin",    1, "#358C75"),
    ]


def _fallback_calendar() -> list:
    return [
        (1,  "Australian GP",    "Albert Park",                   "2026-03-08", "done",     False),
        (2,  "Chinese GP",       "Shanghai International",        "2026-03-15", "done",     True),
        (3,  "Japanese GP",      "Suzuka",                        "2026-03-29", "done",     False),
        (4,  "Miami GP",         "Miami International Autodrome", "2026-05-03", "done",     True),
        (5,  "Canadian GP",      "Circuit Gilles-Villeneuve",     "2026-05-24", "done",     True),
        (6,  "Monaco GP",        "Circuit de Monaco",             "2026-06-07", "done",     False),
        (7,  "Barcelona GP",     "Circuit de Barcelona-Catalunya","2026-06-14", "next",     False),
        (8,  "Austrian GP",      "Red Bull Ring",                 "2026-06-28", "upcoming", False),
        (9,  "British GP",       "Silverstone",                   "2026-07-05", "upcoming", True),
        (10, "Belgian GP",       "Spa-Francorchamps",             "2026-07-19", "upcoming", False),
        (11, "Hungarian GP",     "Hungaroring",                   "2026-07-26", "upcoming", False),
        (12, "Dutch GP",         "Circuit Zandvoort",             "2026-08-23", "upcoming", True),
        (13, "Italian GP",       "Autodromo Nazionale Monza",     "2026-09-06", "upcoming", False),
        (14, "Madrid GP",        "Madring Circuit",               "2026-09-13", "upcoming", False),
        (15, "Azerbaijan GP",    "Baku City Circuit",             "2026-09-27", "upcoming", False),
        (16, "Singapore GP",     "Marina Bay Street Circuit",     "2026-10-11", "upcoming", True),
        (17, "United States GP", "Circuit of The Americas",       "2026-10-25", "upcoming", False),
        (18, "Mexico City GP",   "Autodromo Hermanos Rodriguez",  "2026-11-01", "upcoming", False),
        (19, "São Paulo GP",     "Autodromo Jose Carlos Pace",    "2026-11-08", "upcoming", False),
        (20, "Las Vegas GP",     "Las Vegas Strip Circuit",       "2026-11-21", "upcoming", False),
        (21, "Qatar GP",         "Lusail International Circuit",  "2026-11-29", "upcoming", False),
        (22, "Abu Dhabi GP",     "Yas Marina Circuit",            "2026-12-06", "upcoming", False),
    ]


def _fallback_last_race() -> dict:
    return {
        "name":      "Monaco Grand Prix",
        "circuit":   "Circuit de Monaco",
        "date":      "2026-06-07",
        "winner":    "ANT",
        "p2":        "HAM",
        "p3":        "HAD",
        "fl":        "ANT",
        "fl_time":   "1:12.803",
        "highlight": "Antonelli 5th consecutive win. Hamilton P2. Hadjar P3 after Gasly penalty.",
    }
