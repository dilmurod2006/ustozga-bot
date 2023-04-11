import telebot
import pyttsx3

# Telebot kutubxonasi bilan bog'lanish
bot = telebot.TeleBot("BOT_TOKEN")

# Pyttsx3 kutubxonasi bilan bog'lanish
engine = pyttsx3.init()

# Matnni ovozga aylantirish funktsiyasi
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Matn yuborilganda ishga tushiriladigan funktsiya
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    text_to_speech(text)

# Botni ishga tushirish
bot.polling(none_stop=True)
