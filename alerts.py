from config import ALERT_DROP


def has_changes(
    old_home,
    old_draw,
    old_away,
    new_home,
    new_draw,
    new_away,
):

    checks = [
        ("📉 Домакин", old_home, new_home),
        ("📉 Равен", old_draw, new_draw),
        ("📉 Гост", old_away, new_away),
    ]

    messages = []

    for label, old, new in checks:

        if (
            old is None
            or new is None
        ):
            continue

        if old - new >= ALERT_DROP:

            messages.append(
                f"{label}: {old:.2f} → {new:.2f}"
            )

    return messages