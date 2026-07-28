from datetime import datetime

from alerts import has_changes
from database import (
    get_leagues,
    get_saved_odds,
    save_odds,
    delete_match,
)
from odds_api import get_odds


async def check_matches(bot):

    saved_matches = {
        match["match_id"]: match
        for match in get_saved_odds()
    }

    active_matches = set()

    leagues = get_leagues()

    for league in leagues:

        matches = get_odds(league["league_key"])

        for latest in matches:

            match_id = latest["match_id"]

            active_matches.add(match_id)

            if match_id not in saved_matches:

                save_odds(
                    latest["match_id"],
                    latest["league_key"],
                    latest["home_team"],
                    latest["away_team"],
                    latest["home"],
                    latest["draw"],
                    latest["away"],
                    latest["kickoff"],
                    latest["last_update"],
                )

                continue

            old = saved_matches[match_id]

            changes = has_changes(
                old["home"],
                old["draw"],
                old["away"],
                latest["home"],
                latest["draw"],
                latest["away"],
            )

            if changes:

                text = (
                    f"⚽ {latest['home_team']} - {latest['away_team']}\n"
                    f"🏆 {league['league_name']}\n\n"
                    + "\n".join(changes)
                    + f"\n\n🕒 {datetime.now().strftime('%H:%M')}"
                )

                await bot.send_alert(text)

            save_odds(
                latest["match_id"],
                latest["league_key"],
                latest["home_team"],
                latest["away_team"],
                latest["home"],
                latest["draw"],
                latest["away"],
                latest["kickoff"],
                latest["last_update"],
            )

    # Изтриване на приключилите/липсващи мачове
    for match_id in saved_matches:

        if match_id not in active_matches:
            delete_match(match_id)