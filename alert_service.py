from price_analysis import (
    get_price_changes,
    get_all_provinces
)
from user_db import (
    get_user_preferences,
    alert_already_sent,
    save_sent_alert
)

def generate_national_summary(threshold=5.0):

    provinces = get_all_provinces()

    text = (
    f"📊 National PIHPS Changes "
    f"(>{threshold}%)\n\n")

    found = False

    for province in provinces:

        changes = get_price_changes(province)

        if not changes:
            continue

        significant = [
            item for item in changes
            if abs(item["percent_change"]) >= threshold
        ]

        if not significant:
            continue

        significant = sorted(
            significant,
            key=lambda x: abs(x["percent_change"]),
            reverse=True
        )[:3]

        text += f"📍 {province}\n"

        for item in significant:

            emoji = (
                "📈"
                if item["percent_change"] > 0
                else "📉"
            )

            text += (
                f"{emoji} "
                f"{item['commodity'].title()} "
                f"{item['percent_change']}%\n"
            )

        text += "\n"

        found = True

    if not found:
        return "No significant national changes."

    return text

def generate_alert_text(chat_id):

    prefs = get_user_preferences(chat_id)

    if prefs is None:
        return "Please set your province first using /setprovince"

    province, threshold = prefs

    changes = get_price_changes(province)

    if not changes:
        return "No data available."

    text = f"📊 PIHPS {province}\n\n"

    found = False

    for item in changes:

        if abs(item["percent_change"]) < threshold:
            continue

        commodity = item["commodity"]
        alert_date = item["latest_date"]

        if alert_already_sent(chat_id, alert_date, commodity):
            continue

        found = True

        emoji = "📈" if item["percent_change"] > 0 else "📉"

        text += (
            f"{emoji} {commodity.title()}\n"
            f"Rp{item['previous_price']:,.0f} → "
            f"Rp{item['latest_price']:,.0f}\n"
            f"{item['percent_change']}%\n\n"
            f"Date: {alert_date}\n\n"
        )

        save_sent_alert(chat_id, alert_date, commodity)

    if not found:
        return None

    return text