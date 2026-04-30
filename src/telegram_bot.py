import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from extractor import extract_order

import requests

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an order message 🧾")


def send_to_sheets(data: dict):
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=data)
        print("✅ Sent to Google Sheets:", response.text)
    except Exception as e:
        print("❌ Failed to send:", e)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Run extraction safely (non-blocking)
    result = await asyncio.to_thread(extract_order, user_text)


    send_to_sheets(result)

    # 1️⃣ Human response
    human_reply = format_human_response(result)

    await update.message.reply_text(human_reply)

    # 2️⃣ JSON response
    # await update.message.reply_text(
    #     "📦 Structured Data:\n" + json.dumps(result, indent=2)
    # )

def format_human_response(data: dict) -> str:
    if not data or "expenses" not in data:
        return "⚠️ Gagal membaca pengeluaran."

    lines = ["💸 Pengeluaran tercatat:"]

    total = 0

    for item in data.get("expenses", []):
        name = item.get("name", "")
        amount = item.get("amount", 0)
        category = item.get("category", "other")

        total += amount

        lines.append(f"• {name} ({category}) → Rp{amount:,}")

    lines.append(f"\nTotal: Rp{total:,}")

    return "\n".join(lines)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()