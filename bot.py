import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# بارگذاری اطلاعات Google Credentials از BASE64
credentials_base64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
if not credentials_base64:
    raise ValueError("GOOGLE_CREDENTIALS_BASE64 not set")
creds_dict = json.loads(base64.b64decode(credentials_base64))
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)

# اتصال به Google Sheet
sheet = client.open("BearingDataBase").sheet1

# تعریف پاسخ خوش‌آمدگویی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً شماره فنی بلبرینگ را وارد کنید.")

# جستجوی شماره فنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    data = sheet.get_all_records()
    for row in data:
        if str(row.get("شماره فنی", "")).strip() == query:
            brand = row.get("برند", "—")
            price = row.get("قیمت", "—")
            usage = row.get("کاربرد", "—")
            desc = row.get("توضیحات", "—")
            result = f"✅ نتیجه:\n\n🔹 برند: {brand}\n🔹 قیمت: {price}\n🔹 کاربرد: {usage}\n🔹 توضیحات: {desc}"
            await update.message.reply_text(result)
            return
    await update.message.reply_text("متأسفم، موردی پیدا نشد.")

# اجرای ربات
if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
