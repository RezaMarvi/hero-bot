import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# بازیابی مقدار BASE64 و تبدیل آن به دیکشنری
credentials_base64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
if not credentials_base64:
    raise ValueError("GOOGLE_CREDENTIALS_BASE64 not set")

creds_dict = json.loads(base64.b64decode(credentials_base64))
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)
sheet = client.open("BearingDataBase").sheet1

# ربات تلگرام
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["جستجو قیمت بلبرینگ"]]
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "جستجو قیمت بلبرینگ":
        await update.message.reply_text("لطفاً شماره فنی بلبرینگ را وارد کنید:")
    else:
        data = sheet.get_all_records()
        matched = [row for row in data if str(row.get("شماره فنی", "")).strip() == text.strip()]
        if matched:
            row = matched[0]
            response = f"✅ مشخصات بلبرینگ:\n\nشماره فنی: {row.get('شماره فنی')}\nبرند: {row.get('برند')}\nقیمت: {row.get('قیمت')}\nکاربرد: {row.get('کاربرد')}\nتوضیحات: {row.get('توضیحات')}"
        else:
            response = "❌ بلبرینگ موردنظر یافت نشد."
        await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
