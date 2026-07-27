import requests

from config import (
    ODDS_API_KEY,
    SPORT,
    REGION,
    BOOKMAKER,
)

BASE_URL = "https://api.the-odds-api.com/v4/sports"


def get_match(match_name):
    url = f"{BASE_URL}/{SPORT}/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGION,
        "markets": "h2h",
        "bookmakers": BOOKMAKER,
        "oddsFormat": "decimal",
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        matches = response.json()

        for match in matches:

            full_name = (
                f"{match['home_team']} - "
                f"{match['away_team']}"
            )

            if full_name.lower() != match_name.lower():
                continue

            bookmaker = match["bookmakers"][0]
            market = bookmaker["markets"][0]

            home = None
            draw = None
            away = None

            for outcome in market["outcomes"]:

                if outcome["name"] == match["home_team"]:
                    home = outcome["price"]

                elif outcome["name"] == "Draw":
                    draw = outcome["price"]

                elif outcome["name"] == match["away_team"]:
                    away = outcome["price"]

            return {
                "bookmaker": bookmaker["title"],
                "home": home,
                "draw": draw,
                "away": away,
            }

    except Exception:
        return None

    return None