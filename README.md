# 💸 AI Expense Tracker (Telegram Bot + Gemini + Google Sheets)

## 📌 Overview

This project is a **personal finance assistant powered by AI** that lets you log expenses via Telegram chat in natural language.

It automatically:

* Extracts expense data using AI
* Stores it in Google Sheets
* Provides summaries, details, and insights

Built with:

* Google AI Studio (Gemini API for NLP)
* Telegram Bot API (user interface)
* Google Sheets (data storage & analytics)
* Python (backend logic)

---

## 🚀 Features

### 🧠 AI Expense Extraction

Send messages like:

```text
aku beli nasi goreng 20000
```

Bot automatically extracts:

* item name
* amount
* category

---

### 💬 Dual Response

Bot replies with:

* 🤖 Human-friendly message
* 📦 Structured JSON (optional)

---

### 📊 Summary Commands

| Command    | Description     |
| ---------- | --------------- |
| `/summary` | Today’s summary |
| `/week`    | Last 7 days     |
| `/month`   | Monthly summary |

---

### 🧾 Detail View

```text
/today
```

Shows:

```text
🧾 Pengeluaran Hari Ini:

• kopi → Rp25,000
• nasi goreng → Rp20,000

Total: Rp45,000
```

---

### 📊 Insight (AI-style)

```text
/insight
```

Example:

```text
📊 Insight minggu ini:

🍔 Food: 65%
🚗 Transport: 20%

💡 Kamu cukup sering jajan 😄
```

---

## 🧱 Architecture

```text
Telegram → Python Bot → Gemini API → Google Apps Script → Google Sheets
```

---

## 📁 Project Structure

```text
telegram-ai-expense-tracker/
│
├── src/
│   ├── telegram_bot.py
│   ├── extractor.py
│   ├── utils.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

---

### 2. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Setup Gemini API

1. Go to Google AI Studio
2. Generate API key

Create `.env`:

```env
GEMINI_API_KEY=your_api_key
GOOGLE_SCRIPT_URL=your_apps_script_url
TELEGRAM_TOKEN=your_telegram_token
```

---

### 4. Setup Google Sheets

1. Create new sheet
2. Name it: `expenses`
3. Add columns:

```text
timestamp | item_name | amount | category
```

---

### 5. Setup Google Apps Script

In **Extensions → Apps Script**, paste your backend code.

Then:

* Deploy as Web App
* Access: **Anyone**
* Copy URL → use in `.env`

---

### 6. Create Telegram Bot

1. Open Telegram
2. Search **@BotFather**
3. Run:

```text
/start
/newbot
```

4. Copy BOT TOKEN → put in `.env`

---

## ▶️ Run the Bot

```bash
python src/telegram_bot.py
```

---

## 🧪 Example Usage

### Input

```text
aku beli kopi 25k sama roti 15k
```

---

### Output

```text
💸 Pengeluaran tercatat:

• kopi (food) → Rp25,000
• roti (food) → Rp15,000

Total: Rp40,000
```

---

## 💾 Data Storage

All data stored in:

* Google Sheets
* Real-time updates
* Easy to analyze (charts, pivot tables)

---

## 📊 Built-in Analytics

* Daily summary
* Weekly trends
* Monthly overview
* Category breakdown
* Detail view

---

## ⚠️ Notes

* Gemini free tier has daily limits
* Internet connection required
* LLM output may vary → prompt tuning helps
* Data validation handled in Apps Script

---

## 🔧 Future Improvements

* Natural language queries (no commands needed)
* Advanced insights (trend comparison)
* Streak tracking (habit building)
* Multi-user support
* Dashboard UI (Streamlit / Web)

---

## 🧠 Tech Stack Summary

| Component     | Role           |
| ------------- | -------------- |
| Gemini API    | NLP extraction |
| Telegram Bot  | Chat interface |
| Google Sheets | Database       |
| Apps Script   | Backend API    |
| Python        | Orchestration  |

---

## 📄 License

MIT License
