import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CommandHandler
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

async def summary(update, context):
    data = await asyncio.to_thread(get_summary, "today")
    text = format_summary(data, "Hari ini")
    await update.message.reply_text(text)

async def today(update, context):
    data = await asyncio.to_thread(get_today_detail)
    text = format_today_detail(data)
    await update.message.reply_text(text)

async def week(update, context):
    data = await asyncio.to_thread(get_summary, "week")
    text = format_summary(data, "7 Hari Terakhir")
    await update.message.reply_text(text)

async def month(update, context):
    data = await asyncio.to_thread(get_summary, "month")
    text = format_summary(data, "Bulan Ini")
    await update.message.reply_text(text)


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

def get_summary(type_="today"):
    try:
        url = f"{GOOGLE_SCRIPT_URL}?type={type_}"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        print("❌ Error fetching summary:", e)
        return {}

def format_summary(data, label):
    if not data:
        return "⚠️ Gagal mengambil data."

    summary = data.get("summary", {})
    total = data.get("total", 0)

    lines = [f"📊 {label}:\n"]

    for category, amount in summary.items():
        try:
            amount = int(amount)
        except:
            amount = 0

        lines.append(f"• {category} → Rp{amount:,}")

    try:
        total = int(total)
    except:
        total = 0

    lines.append(f"\nTotal: Rp{total:,}")

    return "\n".join(lines)

def format_today_detail(data):
    if not data:
        return "⚠️ Gagal ambil data."

    details = data.get("details", [])
    total = data.get("total", 0)

    if not details:
        return "🧾 Belum ada pengeluaran hari ini."

    lines = ["🧾 Pengeluaran Hari Ini:\n"]

    for item in details:
        name = item.get("name", "unknown").upper()
        amount = int(item.get("amount", 0))

        lines.append(f"• {name} → Rp{amount:,}")

    lines.append(f"\nTotal: Rp{int(total):,}")

    return "\n".join(lines)

def get_today_detail():
    try:
        url = f"{GOOGLE_SCRIPT_URL}?type=detail_today"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        print("❌ Error:", e)
        return {}


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("month", month))
    app.add_handler(CommandHandler("today", today))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()