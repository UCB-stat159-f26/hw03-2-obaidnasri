"""
make_plot.py

Reads the cleaned `serena` dataset and produces a reproduction of the
NYT graphic "Serena Williams Dominated Her Generation, Then the Next
One, Too" (Ziegler & Dominguez, Aug 28, 2022), saved as a PNG.

Usage:
    python scripts/make_plot.py
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_FILE = "data/processed/serena.csv"
IMAGES_DIR = "images"
OUT_FILE = os.path.join(IMAGES_DIR, "serena_age_plot.png")


def make_plot(data_path: str = PROCESSED_FILE, out_path: str = OUT_FILE) -> None:
    serena = pd.read_csv(data_path, parse_dates=["match_date", "opponent_dob"])

    colors = serena["result"].map({"W": "#59c3e8", "L": "#6b2d5c"})

    fig, ax = plt.subplots(figsize=(12, 7), facecolor="white")
    ax.scatter(
        serena["williams_age"],
        serena["age_diff"],
        c=colors,
        alpha=0.75,
        s=20,
        edgecolors="none",
    )
    ax.axhline(0, color="gray", linewidth=1)

    ax.set(
        title="Serena Williams's Professional Matches, Age 14 to 40",
        xlabel="Williams's age",
        ylabel="Age difference vs. opponent (years)",
    )

    ax.legend(
        handles=[
            plt.scatter([], [], c="#59c3e8", label="Match Williams won"),
            plt.scatter([], [], c="#6b2d5c", label="Match lost"),
        ],
        loc="upper left",
        frameon=False,
    )

    fig.text(
        0.01,
        -0.02,
        "Source: Tennis Abstract. Reproduction for Stat 159 coursework; "
        "not affiliated with the New York Times.",
        fontsize=8,
        color="gray",
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    os.makedirs(IMAGES_DIR, exist_ok=True)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    make_plot()
