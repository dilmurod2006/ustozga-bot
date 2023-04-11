import telebot
import pyttsx3
from pydub import AudioSegment

# Telebot kutubxonasi bilan bog'lanish
bot = telebot.TeleBot("6261129884:AAFPC_91q0trhW1ByTV-zRandOLHDbltkyg")

# Pyttsx3 kutubxonasi bilan bog'lanish
engine = pyttsx3.init()

# Matnni ovozga aylantirish va ogg formatida saqlash funktsiyasi
def text_to_speech(text):
    engine.save_to_file(text, 'audio.wav')
    engine.runAndWait()
    sound = AudioSegment.from_wav('audio.wav')
    sound.export('audio.ogg', format='ogg')

    audio = open('audio.ogg', 'rb')
    return audio

# Matn yuborilganda ishga tushiriladigan funktsiya
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    audio = text_to_speech(text)
    bot.send_voice(message.chat.id, audio)

# Botni ishga tushirish
bot.polling()
