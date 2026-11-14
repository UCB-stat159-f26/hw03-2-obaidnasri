
import json
import re
import urllib.request
import urllib.error

import pandas as pd
import matplotlib.pyplot as plt


def _extract_matches(raw_text):
    """Extract match records from Tennis Abstract JavaScript."""
    match = re.search(
        r"var\s+morematchmx\s*=\s*(\[.*?\])\s*;",
        raw_text,
        flags=re.DOTALL
    )
    if not match:
        raise ValueError("Invalid Tennis Abstract career data.")
    return json.loads(match.group(1))



def _parse_date(value):
    """Convert YYYYMMDD strings to dates."""
    return pd.to_datetime(value, format="%Y%m%d", errors="coerce")


def _calculate_opponent_age(row, match_date):
    """Handle female DOBs and male numeric ages."""
    value = row[16]
    if re.fullmatch(r"\d{8}", value):
        dob = _parse_date(value)
        return (match_date - dob).days / 365.25 if pd.notna(dob) else float("nan")
    return pd.to_numeric(value, errors="coerce")


def _process_match(row, player_dob):
    """Convert one raw match into a cleaned record."""
    if len(row) <= 16 or row[4] not in ("W", "L"):
        return None
    match_date = _parse_date(row[0])
    if pd.isna(match_date):
        return None
    player_age = (match_date - player_dob).days / 365.25
    opponent_age = _calculate_opponent_age(row, match_date)
    return {
        "match_date": match_date,
        "tournament": row[1],
        "surface": row[2],
        "opponent_name": row[11],
        "result": row[4],
        "player_age": player_age,
        "opponent_age": opponent_age,
        "age_diff": player_age - opponent_age,
    }


def _clean_matches(raw_text, player_dob):
    """Create a clean DataFrame from career match records."""
    matches = _extract_matches(raw_text)
    dob = pd.Timestamp(player_dob)
    records = [_process_match(row, dob) for row in matches]
    data = pd.DataFrame([record for record in records if record is not None])
    if data.empty:
        raise ValueError("No valid match records were found.")
    data = data.dropna(subset=["player_age", "opponent_age"])
    return data.sort_values("match_date").reset_index(drop=True)


def _format_player_name(player_name):
    """Normalize a player name for Tennis Abstract URLs."""
    name = player_name.strip()
    if not name:
        raise ValueError("Please provide a player name.")

    if " " in name:
        return "".join(part.capitalize() for part in name.split())

    if name.islower():
        raise ValueError(
            "Please separate first and last names with a space."
        )

    return name[0].upper() + name[1:]


def _download_career_data(player_name):
    """Download a player's career matches from Tennis Abstract."""
    name = _format_player_name(player_name)

    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ValueError(
                f"Player '{player_name}' was not found on Tennis Abstract."
            ) from error
        raise
    except urllib.error.URLError as error:
        raise ConnectionError(
            "Could not connect to Tennis Abstract."
        ) from error


def _fetch_profile(player_name, profile_type):
    """Download a male or female player's profile."""
    name = _format_player_name(player_name)
    url = f"https://www.tennisabstract.com/cgi-bin/{profile_type}.cgi?p={name}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def _get_player_birth_date(player_name):
    """Find a player's birth date from their Tennis Abstract profile."""
    for profile_type in ("wplayer", "player"):
        html = _fetch_profile(player_name, profile_type)
        if html is None:
            continue
        match = re.search(r"\bvar\s+dob\s*=\s*(\d{8})\s*;", html)
        if match:
            return pd.to_datetime(match.group(1), format="%Y%m%d")
    raise ValueError(f"Player '{player_name}' was not found.")


def get_player_matches(player_name):
    """Download and clean a player's career matches."""
    birth_date = _get_player_birth_date(player_name)
    raw_data = _download_career_data(player_name)
    return _clean_matches(raw_data, birth_date)


def plot_player_matches(data):
    """Plot player age against opponent age difference, colored by result."""
    required = {"player_age", "age_diff", "result"}
    if not required.issubset(data.columns):
        raise ValueError("DataFrame is missing required plotting columns.")

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = {"W": "#247BA0", "L": "#E76F51"}

    for result, label in [("W", "Win"), ("L", "Loss")]:
        subset = data[data["result"] == result]
        ax.scatter(subset["player_age"], subset["age_diff"],
                   c=colors[result], label=label, alpha=0.5, s=12)

    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Player's Age (Years)")
    ax.set_ylabel("Player Age − Opponent Age (Years)")
    ax.set_title("Career Matches by Player and Opponent Age")
    ax.legend()
    return fig
