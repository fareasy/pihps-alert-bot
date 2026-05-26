import schedule
import time
from user_db import get_all_users
from alert_service import generate_alert_text
from telegram_sender import send_message
from daily_update import update_latest_prices

def job():

    print("Running scheduled job...")

    update_latest_prices()

    users = get_all_users()

    print("Users:", users)

    for chat_id in users:

        try:

            print("Generating alert for", chat_id)

            text = generate_alert_text(chat_id)

            print(text)

            if text:
                send_message(text, chat_id)
                print(f"Alert sent to {chat_id}")
            else:
                print(f"No new alerts for {chat_id}")

        except Exception as e:

            print(f"Failed for {chat_id}: {e}")


schedule.every(1).minutes.do(job)

print("Scheduler started...")

while True:

    schedule.run_pending()

    time.sleep(30)