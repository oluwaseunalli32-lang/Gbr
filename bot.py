import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Fetch a random fact from a free API
async def get_random_fact():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=10)
            response.raise_for_status()
            return response.json()["text"]
    except Exception:
        return "Could not fetch a fact right now. Please try again later."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Güncel Bağlantı Rehberi!\n"
        "Send /fact to get a random interesting fact."
    )

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact = await get_random_fact()
    await update.message.reply_text(f"💡 **Did you know?**\n\n{fact}")

def main():
    # Uses polling mode (perfect for Background Workers)
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fact", fact_command))
    app.run_polling()

if __name__ == "__main__":
    main()
