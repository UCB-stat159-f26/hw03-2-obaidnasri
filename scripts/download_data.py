"""
download_data.py

Downloads the raw data file used to reproduce the NYT graphic
"Serena Williams Dominated Her Generation, Then the Next One, Too"
(Ziegler & Dominguez, Aug 28, 2022).

The source is the javascript file that backs Serena Williams's
"career matches" page on Tennis Abstract:
https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js

This script only downloads the raw file as-is. No cleaning or
parsing happens here (see clean_data.py for that).

Usage:
    python scripts/download_data.py
"""

import os
import urllib.request

RAW_URL = "https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js"
RAW_DIR = "data/raw"
RAW_FILE = os.path.join(RAW_DIR, "SerenaWilliamsCareer.js")


def download_raw_data(url: str = RAW_URL, out_path: str = RAW_FILE) -> None:
    """Download the raw Serena Williams career matches JS file."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Stat159 HW reproducibility check)"},
    )

    print(f"Downloading {url} ...")
    with urllib.request.urlopen(req) as response:
        content = response.read()

    with open(out_path, "wb") as f:
        f.write(content)

    print(f"Saved raw data to {out_path} ({len(content):,} bytes)")


if __name__ == "__main__":
    download_raw_data()
