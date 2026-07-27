import requests
import logging

from config import (
    ODDS_API_KEY,
    SPORT,
    REGIONS,
    BOOKMAKERS,
    MARKETS,
    ODDS_FORMAT
)

BASE_URL = "https://api.the-odds-api.com/v4"


def get_soccer_leagues():
    """
    Връща всички налични футболни лиги.
    """

    try:
        response = requests.get(
            f"{BASE_URL}/sports",
            params={
                "apiKey": ODDS_API_KEY
            },
            timeout=20
        )

        response.raise_for_status()

        sports = response.json()

        football = []

        for sport in sports:
            if sport["key"].startswith("soccer_"):
                football.append(sport)

        logging.info(f"Намерени лиги: {len(football)}")

        return football

    except Exception as e:
        logging.error(f"League error: {e}")
        return []


def get_league_odds(sport_key):
    """
    Връща коефициентите за дадена лига.
    """

    try:

        response = requests.get(
            f"{BASE_URL}/sports/{sport_key}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": REGIONS,
                "markets": MARKETS,
                "bookmakers": BOOKMAKERS,
                "oddsFormat": ODDS_FORMAT
            },
            timeout=30
        )

        remaining = response.headers.get(
            "x-requests-remaining",
            "?"
        )

        used = response.headers.get(
            "x-requests-used",
            "?"
        )

        logging.info(
            f"Remaining requests: {remaining} | Used: {used}"
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        logging.error(f"Odds error ({sport_key}): {e}")
        return []