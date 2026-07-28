import logging
import requests
from datetime import datetime, timezone, timedelta

from config import (
    ODDS_API_KEY,
    REGIONS,
    BOOKMAKERS,
    MARKETS,
    ODDS_FORMAT,
)

BASE_URL = "https://api.the-odds-api.com/v4"


def get_soccer_leagues():
    """
    Връща всички активни футболни лиги.
    """

    try:
        response = requests.get(
            f"{BASE_URL}/sports",
            params={
                "apiKey": ODDS_API_KEY
            },
            timeout=30
        )

        response.raise_for_status()

        sports = response.json()

        leagues = []

        for sport in sports:
            if (
                sport["key"].startswith("soccer_")
                and sport["active"]
            ):
                leagues.append(
                    {
                        "key": sport["key"],
                        "name": sport["title"]
                    }
                )

        logging.info(f"Football leagues: {len(leagues)}")

        return leagues

    except Exception as e:
        logging.exception(e)
        return []


def get_odds(league_key):
    """
    Връща само днешните мачове и коефициентите им.
    """

    try:

        now = datetime.now(timezone.utc)

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        end = start + timedelta(days=1)

        response = requests.get(
            f"{BASE_URL}/sports/{league_key}/odds",
            params={
                "apiKey": ODDS_API_KEY,
                "regions": REGIONS,
                "bookmakers": BOOKMAKERS,
                "markets": MARKETS,
                "oddsFormat": ODDS_FORMAT,
                "commenceTimeFrom": start.isoformat().replace("+00:00", "Z"),
                "commenceTimeTo": end.isoformat().replace("+00:00", "Z"),
            },
            timeout=30
        )

        response.raise_for_status()

        logging.info(
            "Remaining requests: %s",
            response.headers.get("x-requests-remaining")
        )

        events = []

        for event in response.json():

            bookmakers = event.get("bookmakers", [])

            if not bookmakers:
                continue

            bookmaker = bookmakers[0]

            markets = bookmaker.get("markets", [])

            if not markets:
                continue

            outcomes = markets[0].get("outcomes", [])

            home = None
            draw = None
            away = None

            for outcome in outcomes:

                if outcome["name"] == event["home_team"]:
                    home = outcome["price"]

                elif outcome["name"] == event["away_team"]:
                    away = outcome["price"]

                elif outcome["name"].lower() == "draw":
                    draw = outcome["price"]

            if home is None or draw is None or away is None:
                continue

            events.append(
                {
                    "match_id": event["id"],
                    "league_key": league_key,
                    "home_team": event["home_team"],
                    "away_team": event["away_team"],
                    "kickoff": event["commence_time"],
                    "home": home,
                    "draw": draw,
                    "away": away,
                    "last_update": bookmaker["last_update"],
                }
            )

        return events

    except Exception as e:
        logging.exception(e)
        return []