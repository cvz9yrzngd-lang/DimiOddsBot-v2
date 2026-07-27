from datetime import datetime

from alerts import has_changes
from database import get_matches, update_match
from odds_api import get_match


async def check_matches(bot):

    matches = get_matches()

    for match in matches:

        latest = get_match(match["match_name"])

        if latest is None:
            continue

        changes = has_changes(
            match["home"],
            match["draw"],
            match["away"],
            latest["home"],
            latest["draw"],
            latest["away"],
        )

        if changes:

            text = (
                f"⚽ {match['match_name']}\n\n"
                + "\n".join(changes)
                + f"\n\n🏦 {latest['bookmaker']}"
                + f"\n🕒 {datetime.now().strftime('%H:%M')}"
            )

            await bot.send_alert(text)

        update_match(
            match["id"],
            latest["home"],
            latest["draw"],
            latest["away"],
        )