import os
import requests
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.text:
        return

    text = message.text.strip()

    if not text or text.startswith("/"):
        return

    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": "ar|en" if any(
                    "\u0600" <= char <= "\u06ff" for char in text
                ) else "en|ar",
            },
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()
        translation = result["responseData"]["translatedText"]

        if not translation:
            raise ValueError("Empty translation")

        await message.reply_text(translation)

    except Exception:
        await message.reply_text(
            "Sorry, translation failed. Please try again."
        )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

app.run_polling()
