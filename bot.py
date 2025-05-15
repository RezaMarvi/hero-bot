import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# اتصال به گوگل‌شیت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("hopeful-vim-442810-v0-2502ef69b2da.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BearingDataBase").sheet1

# پیام start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["✅  جستجوی قیمت بلبرینگ 💰"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "به ربات بلبرینگ یاب HERO خوش آمدید.\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

# پیام‌های ورودی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()

    if msg == "✅  جستجوی قیمت بلبرینگ 💰":
        await update.message.reply_text("لطفا شماره فنی بلبرینگ مد نظر یا قسمتی از آن رو وارد کنید.:")
        return

    query = msg.lower()
    data = sheet.get_all_values()
    response = ""

    for row in data[1:]:
        part_number = str(row[0]).lower()
        if query in part_number:
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
def main():
    app = ApplicationBuilder().token("7713306717:AAGeR504yzmHN7sZaPyuV4X4ljBh5yXeyxY").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ربات با موفقیت اجرا شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
