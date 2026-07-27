from config import ALERT_DROP


def has_changes(old_home, old_draw, old_away,
                new_home, new_draw, new_away):

    messages = []

    if (
        old_home is not None
        and new_home is not None
        and old_home - new_home >= ALERT_DROP
    ):
        messages.append(
            f"📉 Домакин: {old_home:.2f} → {new_home:.2f}"
        )

    if (
        old_draw is not None
        and new_draw is not None
        and old_draw - new_draw >= ALERT_DROP
    ):
        messages.append(
            f"📉 Равен: {old_draw:.2f} → {new_draw:.2f}"
        )

    if (
        old_away is not None
        and new_away is not None
        and old_away - new_away >= ALERT_DROP
    ):
        messages.append(
            f"📉 Гост: {old_away:.2f} → {new_away:.2f}"
        )

    return messages