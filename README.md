# 💸 AI Expense Tracker (Telegram Bot + Ollama + Gemma)

## 📌 Overview

This project is a **local AI-powered expense tracking system** that reads natural language messages (from Telegram), extracts structured expense data, and logs it for daily tracking.

It uses:

* Ollama for running models locally
* Gemma for parsing text into structured data
* Telegram Bot API as the user interface

---

## 🚀 Features

* 🧠 Extract expenses from messy chat messages
* 💬 Dual response:

  * Human-friendly reply
  * Structured JSON output
* 💸 Automatically calculates totals
* 💾 Logs expenses into CSV
* 🔌 Runs fully offline (no external API)

---

## 🧾 Example

### Input (Telegram message)

```
Beli kopi 25k sama roti 15k - Alex
```

---

### 🤖 Bot Reply

```
Siap Alex! 💸
Pengeluaran kamu tercatat:

• kopi → Rp25,000
• roti → Rp15,000

Total: Rp40,000
```

---

### 📦 Structured Output

```json
{
  "person": "Alex",
  "expenses": [
    {"name": "kopi", "amount": 25000},
    {"name": "roti", "amount": 15000}
  ]
}
```

---

## 📁 Project Structure

```
whatsapp-order-extractor/
│
├── data/
│   ├── messages.txt
│   └── ground_truth.csv
│
├── src/
│   ├── extractor.py
│   ├── evaluator.py
│   ├── telegram_bot.py
│   ├── utils.py
│   └── main.py
│
├── expenses_log.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install Ollama

Download from: https://ollama.com

---

### 2. Pull Model

```bash
ollama pull gemma
```

> Optional (better performance):

```bash
ollama pull mistral
```

---

### 3. Run Ollama

```bash
ollama serve
```

---

### 4. Setup Python Environment

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

### 5. Create Telegram Bot

1. Open Telegram
2. Search **@BotFather**
3. Run:

```
/start
/newbot
```

4. Copy your **BOT TOKEN**

---

### 6. Configure Bot Token

Edit:

```
src/telegram_bot.py
```

```python
TOKEN = "YOUR_BOT_TOKEN"
```

---

## ▶️ Run the Bot

```bash
python src/telegram_bot.py
```

Send a message to your bot and start tracking expenses.

---

## 💾 Data Storage

All expenses are saved in:

```
expenses_log.csv
```

Format:

```
timestamp,person,item_name,amount
```

---

## 📊 Evaluation (Optional)

You can still evaluate extraction accuracy using:

```bash
python src/main.py
```

Metrics:

* Precision
* Recall
* F1-score

---

## ⚠️ Notes

* Model output may vary → prompt tuning improves results
* Supports formats like:

  * `25k` → 25000
  * `10rb` → 10000
  * `1jt` → 1000000
* JSON cleaning is applied to handle LLM formatting

---

## 🔧 Improvements

* Add category classification (food, transport, etc.)
* Add database (PostgreSQL / Supabase)
* Add dashboard (Streamlit / React)
* Add multi-user tracking
* Add conversation memory

---

## 🧠 Tech Summary

| Component    | Role                         |
| ------------ | ---------------------------- |
| Ollama       | Local LLM runtime            |
| Gemma        | Text → structured extraction |
| Telegram Bot | User interface               |
| Python       | Backend logic                |

---

## 📄 License

MIT License
