import logging
import asyncio
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from extractor import extract_order

TOKEN = "8471148674:AAEpHnowtVM6fLvii34jZuJPL-7B0lf8Fw0"

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an order message 🧾")



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Run extraction safely (non-blocking)
    result = await asyncio.to_thread(extract_order, user_text)

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

    name = data.get("person", "kamu")
    expenses = data.get("expenses", [])

    lines = [
        f"Siap Alex! 💸",
        "Pengeluaran kamu tercatat:"
    ]

    total = 0

    for item in expenses:
        amount = item.get("amount", 0)
        item_name = item.get("name", "")
        total += amount

        lines.append(f"• {item_name} → Rp{amount:,}")

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