import os
import json
import base64
import gspread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from google.oauth2.service_account import Credentials

# بارگذاری و رمزگشایی کلید از متغیر محیطی
creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_BASE64")
creds_dict = json.loads(base64.b64decode(creds_b64).decode("utf-8"))
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)
sheet = client.open("BearingDataBase").sheet1

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["💵 ✅ جستجوی قیمت بلبرینگ"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "به ربات بلبرینگ یاب HERO خوش آمدید.\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup
    )

# بررسی پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    if msg == "💵 ✅ جستجوی قیمت بلبرینگ":
        await update.message.reply_text("لطفاً شماره فنی بلبرینگ مورد نظر را وارد کنید:")
        return

    query = msg.lower()
    data = sheet.get_all_values()
    response = ""

    for row in data[1:]:
        part = str(row[0]).lower()
        if query in part:
            response += f"🔹 شماره فنی: {row[0]}\n"
            response += f"🏷️ برند: {row[1]}\n"
            try:
                price = int(row[2])
                response += f"💵 قیمت: {format(price, ',')} تومان\n"
            except:
                response += f"💵 قیمت: {row[2]}\n"
            response += f"⚙️ کاربرد: {row[3]}\n"
            response += f"📝 توضیحات: {row[4]}\n\n"

    if not response:
        response = "❌ موردی پیدا نشد. لطفاً شماره فنی یا بخشی از آن را دقیق‌تر وارد کنید یا مطمئن شوید کیبورد در حالت انگلیسی قرار دارد."
    await update.message.reply_text(response)

# اجرای ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
