from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from province_service import get_all_provinces
from price_analysis import get_price_changes
from alert_service import generate_alert_text
from user_db import (
    save_user_preferences,
    get_user_preferences
)
import os
from dotenv import load_dotenv
from alert_service import generate_national_summary

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
Welcome to PIHPS Alert Bot 📊

Commands:
/setprovince <province>
/provinces
/mysettings
/setthreshold
/check
/national <threshold>
"""

    await update.message.reply_text(message)


async def setprovince(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = str(update.effective_chat.id)

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/setprovince Jawa Timur"
        )
        return

    available_provinces = get_all_provinces()
    province = " ".join(context.args)

    if province not in available_provinces:
        await update.message.reply_text(
            "❌ Province not found.\n\nUse /provinces to see available provinces."
        )
        return
    save_user_preferences(chat_id, province)

    await update.message.reply_text(
        f"✅ Province set to: {province}"
    )

async def setthreshold(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = str(update.effective_chat.id)

    prefs = get_user_preferences(chat_id)

    if prefs is None:
        await update.message.reply_text(
            "Please set your province first using /setprovince"
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/setthreshold 10"
        )
        return

    try:
        threshold = float(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Threshold must be a number."
        )
        return

    if threshold < 0:
        await update.message.reply_text(
            "Threshold must be positive."
        )
        return

    province, _ = prefs

    save_user_preferences(chat_id, province, threshold)

    await update.message.reply_text(
        f"✅ Threshold set to: {threshold}%"
    )

async def mysettings(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = str(update.effective_chat.id)

    prefs = get_user_preferences(chat_id)

    if prefs is None:
        await update.message.reply_text(
            "No settings found."
        )
        return

    province, threshold = prefs

    text = f"""
📌 Your Settings

Province: {province}
Threshold: {threshold}%
"""

    await update.message.reply_text(text)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = str(update.effective_chat.id)

    text = generate_alert_text(chat_id)

    if not text:
        text = "📊 No significant changes today."

    await update.message.reply_text(text)

async def provinces(update: Update, context: ContextTypes.DEFAULT_TYPE):

    province_list = get_all_provinces()

    text = "📍 Available Provinces\n\n"

    for province in province_list:
        text += f"• {province}\n"

    await update.message.reply_text(text)

async def national(update: Update, context: ContextTypes.DEFAULT_TYPE):

    threshold = 5.0

    if context.args:

        try:
            threshold = float(context.args[0])

        except:
            await update.message.reply_text(
                "Usage:\n/national 5"
            )
            return

    text = generate_national_summary(threshold)

    await update.message.reply_text(text)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setprovince", setprovince))
app.add_handler(CommandHandler("mysettings", mysettings))
app.add_handler(CommandHandler("provinces", provinces))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("setthreshold", setthreshold))
app.add_handler(CommandHandler("national", national))

print("Bot running...")

app.run_polling()