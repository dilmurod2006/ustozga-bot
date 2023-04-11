import telebot
import pyttsx3


token = "6261129884:AAFPC_91q0trhW1ByTV-zRandOLHDbltkyg"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!')

#  text to speech and audio send message.chat.id
@bot.message_handler(content_types=['text'])
def text_to_speech(message):
    engine = pyttsx3.init()
    engine.save_to_file(message.text, 'audio.ogg')
    engine.runAndWait()
    audio = open('audio.ogg', 'rb')
    bot.send_audio(message.chat.id, audio)

bot.polling()
