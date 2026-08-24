import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = "8906879876:AAEEmd-mC2WPKBJzNd5qrFFTOVDusoTeohc"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Le bot L'Artisan 06 est en ligne !"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    photo_url = "https://raw.githubusercontent.com/skdesignshop/photo-image-/refs/heads/main/IMG_9326.jpeg"
    
    caption = """Bienvenue sur le bot officiel de L'artisan06🛍️

Disponible 24h/24 et 7j/7. 🕒

📳 Besoin d'aide ? 
Contactez-Nous : @lartisan06

🚀 Accès direct à la mini app : Lancez l'application intégrée en un clin d'œil depuis le chat⬇️"""

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    
    btn_webapp = telebot.types.InlineKeyboardButton("🕹️ MINI APPLICATION", web_app={"url": "https://t.me/lartisan06bot/miniapp"})
    btn_telegram = telebot.types.InlineKeyboardButton("🌐 TELEGRAM", url="https://t.me/+MFHN9W_pqmNlODg8")
    btn_whatsapp = telebot.types.InlineKeyboardButton("✳️ WHATSAPP", url="https://wa.me/33628007778")
    btn_potato = telebot.types.InlineKeyboardButton("🥔 POTATO", url="https://tato.im/lartisan06000")

    markup.add(btn_webapp, btn_telegram, btn_whatsapp, btn_potato)
    bot.send_photo(chat_id, photo_url, caption=caption, reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
