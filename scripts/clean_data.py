"""
clean_data.py

Parses the raw SerenaWilliamsCareer.js file and produces the cleaned
`serena` dataset used for the age-vs-opponent-age graphic.

The raw file is a javascript assignment of the form:

    var morematchmx = [
        ["19951030", "Canadian Open", "Carpet", "W", "L", ..., "Anne Miller",
         ..., "19770119", ...],
        ...
    ];

Based on inspection of the raw array (documented in the HW assignment),
the relevant field positions (0-indexed) are:

    0  -> match date (YYYYMMDD)
    1  -> tournament
    2  -> surface
    4  -> result for Serena ("W" = Serena won, "L" = Serena lost)
    11 -> opponent name
    16 -> opponent date of birth (YYYYMMDD)

All other fields (seed/entry codes, rank, score, match id, etc.) are
kept in the raw array but are not needed for this particular graphic,
so they are dropped from the cleaned `serena` table.

Usage:
    python scripts/clean_data.py
"""

import json
import os
import re
from datetime import datetime

import pandas as pd

RAW_FILE = "data/raw/SerenaWilliamsCareer.js"
PROCESSED_DIR = "data/processed"
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "serena.csv")

# Serena Williams's date of birth, as given in the assignment.
WILLIAMS_DOB = datetime.strptime("19810926", "%Y%m%d")

# Field positions in the raw array (see module docstring).
IDX_DATE = 0
IDX_TOURNAMENT = 1
IDX_SURFACE = 2
IDX_RESULT = 4
IDX_OPPONENT = 11
IDX_OPPONENT_DOB = 16


def _extract_json_array(raw_text: str) -> list:
    """Pull the JS array literal out of `var morematchmx = [...];` and
    parse it as JSON (the array contents are valid JSON once the
    surrounding `var ... = ` and trailing `;` are stripped)."""
    match = re.search(r"=\s*(\[.*\])\s*;?\s*$", raw_text, flags=re.DOTALL)
    if not match:
        raise ValueError("Could not find a JS array literal in the raw file.")
    return json.loads(match.group(1))


def _parse_date(yyyymmdd: str):
    if not yyyymmdd:
        return pd.NaT
    try:
        return datetime.strptime(yyyymmdd, "%Y%m%d")
    except ValueError:
        return pd.NaT


def clean_data(raw_path: str = RAW_FILE, out_path: str = PROCESSED_FILE) -> pd.DataFrame:
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    rows = _extract_json_array(raw_text)

    records = []
    for row in rows:
        # Skip malformed/short rows defensively.
        if len(row) <= max(IDX_DATE, IDX_TOURNAMENT, IDX_SURFACE,
                            IDX_RESULT, IDX_OPPONENT, IDX_OPPONENT_DOB):
            continue

        match_date = _parse_date(row[IDX_DATE])
        opponent_dob = _parse_date(row[IDX_OPPONENT_DOB])
        result_code = row[IDX_RESULT]  # "W" or "L" for Serena

        records.append(
            {
                "match_date": match_date,
                "tournament": row[IDX_TOURNAMENT],
                "surface": row[IDX_SURFACE],
                "opponent_name": row[IDX_OPPONENT],
                "opponent_dob": opponent_dob,
                "result": result_code,
            }
        )

    serena = pd.DataFrame.from_records(records)

    # Drop rows where we couldn't parse a match date or an opponent DOB,
    # since both are required to compute the plotted quantities.
    serena = serena.dropna(subset=["match_date", "opponent_dob"]).copy()

    # Compute ages (in years, as decimals) and the derived y-axis quantity.
    serena["williams_age"] = (
        serena["match_date"] - WILLIAMS_DOB
    ).dt.days / 365.25
    serena["opponent_age"] = (
        serena["match_date"] - serena["opponent_dob"]
    ).dt.days / 365.25
    serena["age_diff"] = serena["williams_age"] - serena["opponent_age"]

    serena["result"] = serena["result"].map({"W": "W", "L": "L"})
    serena = serena.dropna(subset=["result"])

    serena = serena.sort_values("match_date").reset_index(drop=True)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    serena.to_csv(out_path, index=False)
    print(f"Wrote cleaned dataset to {out_path} ({len(serena)} matches)")

    return serena


if __name__ == "__main__":
    clean_data()
