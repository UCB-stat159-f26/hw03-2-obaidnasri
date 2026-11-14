import pytest
import pandas as pd

from tennis_package.tennis import (
    _extract_matches,
    _clean_matches,
    _format_player_name,
)


FEMALE_JS = '''
var morematchmx = [
["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC",
"Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R",
"19770119", "", "USA", "0"]
];
'''

MALE_JS = '''
var morematchmx = [
["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC",
"R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "",
"", "R", "22.264202601", "", "ESP", "0"]
];
'''


def test_extract_matches():
    matches = _extract_matches(FEMALE_JS)
    assert len(matches) == 1
    assert matches[0][11] == "Anne Miller"


def test_female_player_ages():
    data = _clean_matches(FEMALE_JS, "1981-09-26")
    assert len(data) == 1
    assert data.iloc[0]["result"] == "L"
    assert data.iloc[0]["opponent_age"] == pytest.approx(18.78, abs=0.01)


def test_male_player_ages():
    data = _clean_matches(MALE_JS, "1986-06-03")
    assert len(data) == 1
    assert data.iloc[0]["result"] == "L"
    assert data.iloc[0]["opponent_age"] == pytest.approx(22.2642, abs=0.001)


def test_age_difference():
    data = _clean_matches(FEMALE_JS, "1981-09-26")
    row = data.iloc[0]
    assert row["age_diff"] == pytest.approx(
        row["player_age"] - row["opponent_age"]
    )


def test_invalid_js():
    with pytest.raises(ValueError, match="Invalid Tennis Abstract"):
        _extract_matches("invalid javascript")


def test_player_name_formatting():
    assert _format_player_name("serena williams") == "SerenaWilliams"
    assert _format_player_name("Serena Williams") == "SerenaWilliams"
    assert _format_player_name("SerenaWilliams") == "SerenaWilliams"