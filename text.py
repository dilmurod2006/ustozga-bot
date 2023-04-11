import telebot
import pyttsx3
from pydub import AudioSegment


token = "6261129884:AAFPC_91q0trhW1ByTV-zRandOLHDbltkyg"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!')
engine = pyttsx3.init()
engine.setProperty('rate', 150)    # taxminan 150 soat tezlikda
engine.setProperty('volume', 1) 
voices = getProperty('voices')
engine.setProperty('voice', voices[1].id)

# text to speech and audio send message.chat.id
@bot.message_handler(content_types=['text'])
def text_to_speech(message):
    engine.save_to_file(message.text, 'audio.wav')
    engine.runAndWait()

    sound = AudioSegment.from_wav('audio.wav')
    sound.export('audio.ogg', format='ogg')

    audio = open('audio.ogg', 'rb')
    bot.send_audio(message.chat.id, audio)
bot.polling()
