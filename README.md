# Tennis Career Age Graphic — Python Package (HW3)

## Overview

This repository contains a Python package inspired by the New York Times article **"Serena Williams Dominated Her Generation, Then the Next One, Too"** (Sara Ziegler and Leo Dominguez, Aug. 28, 2022). Building on HW2, the package retrieves career match data for different professional tennis players and generates scatter plots comparing each player's age to their opponents' ages, colored by match outcome.

## Data Source

Raw data comes directly from Tennis Abstract's JavaScript career match files. For example:

```
https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js
https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js
```

Player birth dates are retrieved from their Tennis Abstract profile pages. Female opponents' ages are calculated from their dates of birth, while male opponents' ages are provided directly in the raw data.

## Repository Structure

```
hw03/
├── README.md
├── pyproject.toml
├── .gitignore
├── report.ipynb
├── tennis_package/
│   ├── __init__.py       # exposes the two public functions
│   └── tennis.py         # retrieves, cleans, and plots match data
├── tests/
│   └── test_tennis.py    # automated tests using mock JS data
├── scripts/              # original HW2 pipeline scripts
│   ├── download_data.py
│   ├── clean_data.py
│   └── make_plot.py
├── data/
│   ├── raw/
│   └── processed/
└── images/
```

The original HW2 scripts and notebook are retained as references. The reusable package functions are implemented in `tennis_package/`.

## Installation and Usage

1. Install the package directly from GitHub:

   ```bash
   pip install git+https://github.com/UCB-stat159-f26/hw03-2-obaidnasri.git
   ```

   Replace `USERNAME/REPOSITORY` with the GitHub repository location.

2. Import the package functions:

   ```python
   from tennis_package import get_player_matches, plot_player_matches
   ```

3. Retrieve career match data and generate a plot:

   ```python
   serena = get_player_matches("Serena Williams")
   plot_player_matches(serena)

   rafa = get_player_matches("Rafael Nadal")
   plot_player_matches(rafa)
   ```

4. Invalid player names return a meaningful error:

   ```python
   get_player_matches("Invalid Player")
   ```

For local development, the package can also be installed using `pip install -e .` from the repository directory.

## Package Functions

1. **`get_player_matches()`** — formats the player's name, retrieves their career match data and birth date from Tennis Abstract, calculates player and opponent ages, and returns a cleaned pandas DataFrame containing match information and age differences.
2. **`plot_player_matches()`** — takes the cleaned DataFrame and generates a scatter plot of player age versus age difference, with points color-coded by wins and losses.

Private helper functions handle downloading, parsing, name formatting, date calculations, and differences between male and female match data.

## Testing

Automated tests use mock JavaScript content rather than requesting data from live Tennis Abstract servers.

Run the tests using:

```bash
python -m pytest tests/test_tennis.py -v
```

The six tests verify match extraction, female and male opponent age calculations, age differences, invalid JavaScript handling, and player name formatting.

## Known Limitations

- Only fields needed for the age-difference visualization are extracted from the raw career match data.
- Match coverage depends on the availability and completeness of Tennis Abstract's career records.
- The visualization approximates the original NYT graphic but does not reproduce its annotations or exact styling.

## Personal Reflections

This assignment helped me understand how to turn the data pipeline from HW2 into a reusable Python package. Instead of writing code for only Serena Williams, I learned how to organize functions that work with multiple players and handle differences in their data formats.

One challenge was processing opponent ages differently for male and female players while keeping the output consistent. I also learned how to write automated tests using mock data, organize public and private functions, and configure a package for installation.

Overall, HW3 helped me better understand how modular code, testing, and package structure make data analysis more reproducible and reusable.

## Author

Obaid Nasri — Stat 159, Fall 2026