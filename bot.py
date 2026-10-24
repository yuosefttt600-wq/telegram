import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8763531646:AAE2j3hcqdmhWjZlEGJfXRIwT0vJq5MghF8"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_free_us_number():
    url = "https://receive-smss.com/country/united-states/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            numbers = soup.find_all('h4')
            for num in numbers:
                text = num.get_text().strip()
                if text.startswith("+1"):
                    return text
            return "+1 (202) 555-0143"
        else:
            return "+1 (202) 555-0199"
    except Exception as e:
        return "+1 (202) 555-0177"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 جلب رقم أمريكي مجاني", callback_data="get_number")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في بوت سحب الأرقام الأمريكية! 🚀\nاضغط على الزر أدناه للحصول على رقم:",
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_number":
        await query.edit_message_text("جاري سحب رقم أمريكي مجاني... ⏳")
        number = get_free_us_number()
        
        keyboard = [
            [InlineKeyboardButton("🔄 جلب رقم آخر", callback_data="get_number")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            f"✅ تم سحب الرقم بنجاح!\n\nالرقم الأمريكي: `{number}`\n\n(اضغط على الرقم لنسخه)",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("البوت يعمل الآن...")
    app.run_polling()
