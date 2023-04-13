import telebot
from deep_translator import GoogleTranslator as tr
from telebot import types
import speech_recognition as sr
from pydub import AudioSegment
import json
import pyttsx3
import wikipedia


#########################################################################
# Bot Settings
token = '6240379695:AAGGHPg6T6tS9gohX8-6NHW1MTc7OwgMPzU'
bot = telebot.TeleBot(token)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice",]
#########################################################################
##########################################################################
bolim={"1":"s"}
bolim.clear()
files={"67361118":{"audio":[],"video":[],"document":[],"rasm":[]}}
files.clear()
###########################################################
with open("obb.json","r",encoding="utf-8") as file1:
	files=json.load(file1)
with open("bolim.json","r",encoding="utf-8") as file2:
	bolim=json.load(file2)
############################################################################


# Gruhlar
with open('FirstGroup.txt', 'r') as f:
    first_group_id = [int(line.strip()) for line in f]

with open('SecondGroup.txt', 'r') as f:
    second_group_id = [int(line.strip()) for line in f]

#######################################################################
# pyttsx settings
engine = pyttsx3.init()
engine.setProperty('rate', 147.5)    # taxminan 140 soat tezlikda
engine.setProperty('volume', 1) 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#######################################################################
with open('admins.txt', 'r') as f:
    admin_ids = [int(line.strip()) for line in f]
# Start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in admin_ids:
        if str(message.chat.id) not in files:
            files[str(message.chat.id)]={"audio":[],"video":[],"document":[],"rasm":[]}
        else:
            if "audio" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["audio"]=[]
            if "rasm" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["rasm"]=[]
            if "video" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["video"]=[]
            if "document" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["document"]=[]
        data1=json.dumps(files)
        data1=json.loads(str(data1))
        with open("obb.json","w",encoding="utf-8") as file:
            json.dump(data1,file,indent=2)
        data2=json.dumps(bolim)
        data2=json.loads(str(data2))
        with open("bolim.json","w",encoding="utf-8") as file:
            json.dump(data2,file,indent=2)
        bolim[str(message.chat.id)]=1
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("FirstGroup","SecondGroup")
        markup.row("Speech to text","Text to speech")
        bot.send_message(message.chat.id,f"""{tr(source="uz",target="en").translate("Assalomu alaykum O'qituvchi botingiz xizmatingizga tayor")}""", reply_markup=markup)
    else:
        if str(message.chat.id) not in files:
            files[str(message.chat.id)]={"audio":[]}
        else:
            if "audio" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["audio"]=[]
        data1=json.dumps(files)
        data1=json.loads(str(data1))
        with open("audio.json","w",encoding="utf-8") as file:
            json.dump(data1,file,indent=2)
        data2=json.dumps(bolim)
        data2=json.loads(str(data2))
        with open("bolim.json","w",encoding="utf-8") as file:
            json.dump(data2,file,indent=2)
        bolim[str(message.chat.id)]=1
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("FirstGroup","SecondGroup")
        markup.row("Speech to text","Text to speech")
        bot.send_message(message.chat.id,f"""{tr(source="uz",target="en").translate("Assalomu alaykum O'qituvchi botingiz xizmatingizga tayor")}""", reply_markup=markup)
    if message.chat.id in first_group_id:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Translate","Wikiedia")
        bot.send_message(message.chat.id, 'Assalomu leykum PRE-IELTS group at 4 gruh azosi{}!'.format(message.chat.first_name), reply_markup=markup)
    elif message.chat.id in second_group_id:
        bot.send_message(message.chat.id,f"qalesan 2gruh")
    else:
        bot.send_message(message.chat.id, "siz gruh azosi emasiz o'qituvchiga ayting sizning chat id raqamingizni botga kiritish kerak")



# Admin commands

# Admin functions
# for First group
# First group functions
# Translate and wikipedia
# translate en-uz and uz-en
# wikipedia en 
@bot.message_handler(content_types=['text'])
def admin_functions(message):
    if message.text == 'en-uz':
        bot.send_message(message.chat.id, 'Ingiliz tilida tarjima qilinadiga matn yuboring')
        bot.register_next_step_handler(message, translate_en_uz)
    elif message.text == 'uz-en':
        bot.send_message(message.chat.id, "matn yuboring")
        bot.register_next_step_handler(message, translate_uz_en)
    elif message.text == 'Wikiedia':
        bot.send_message(message.chat.id, "Qanday malumot kerak nima hqida bilmoqchisiz?")
        bot.register_next_step_handler(message, wikipedia_en)
    if message.text == "FirstGroup":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("📥Upload file","➕Add pupil id")
        markup.row("📎 Send files","🔙 ortga")
        # markup.row("🖼Pictures","🎥Videos")
        # markup.row("📑Documemts","🎧Audios")
        bot.send_message(message.chat.id, "Choice", reply_markup=markup)
    elif message.text == "SecondGroup":
        bot.send_message(message.chat.id, "Uzur hali ishga tushmagan yaqinda ishga tushadi",)
        # markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        # markup.row("📥Upload file","➕Add pupil id")
        # markup.row("📎 Send files","🔙 ortga")
        # bot.send_message(message.chat.id, "Choice", reply_markup=markup)
    # Speech to text start
    elif message.text == "Speech to text":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("first group","second group")
        bot.send_message(message.chat.id, "Choice Group", reply_markup=markup)
    elif message.text == "first group":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🔙 ortga")
        bot.send_message(message.chat.id, "Send me voice message",reply_markup=markup)
        bot.register_next_step_handler(message, voice_to_text1)
    elif message.text == "second group":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🔙 ortga")
        bot.send_message(message.chat.id, "Send me voice message",reply_markup=markup)
        bot.register_next_step_handler(message, voice_to_text2)
    # Speech to text end
    # Text to speech start
    elif message.text == "Text to speech":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("First group","Second group")
        bot.send_message(message.chat.id, "Choice Group", reply_markup=markup)
    elif message.text == "First group":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🔙 ortga")
        bot.send_message(message.chat.id, "Send me text",reply_markup=markup)
        bot.register_next_step_handler(message, tts1)
    elif message.text == "Second group":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🔙 ortga")
        bot.send_message(message.chat.id, "Send me text",reply_markup=markup)
        bot.register_next_step_handler(message, tts2)
    elif message.text == 'Translate':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("en-uz","uz-en")
        markup.row("🔙 Back")
        bot.send_message(message.chat.id, 'Tilni tanlang', reply_markup=markup)
    elif message.text == '🔙 Back':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Translate","Wikiedia")
        bot.send_message(message.chat.id, 'Asosiy sahifaga qaytingiz qanday yordam kerak tugmalarni tanlashingiz '.format(message.chat.first_name), reply_markup=markup)

# the back button
# @bot.message_handler(content_types=['text'])
# def back(message):
# Send files
##############################################################################################################################
    elif message.text == "📎 Send files":                      
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True) 
        markup.row("First-Group","Second-Group")              
        markup.row("🔙 ortga")                                
        bot.send_message(message.chat.id, "Hali ishga tushmagan yaqinda ishga tushadi", reply_markup=markup) #################
    elif message.text == "First-Group":
        bot.register_next_step_handler(message,document)
    elif message.text == "Second-Group":
        bot.send_message(message.chat.id, "Hali ishga tushmagan yaqinda ishga tushadi")
        # bot.register_next_step_handler(message,document2)
    
###############################################################################################################################
    elif message.text == "🔙 ortga":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("FirstGroup","SecondGroup")
        markup.row("Speech to text","Text to speech")
        bot.send_message(message.chat.id,f"""{tr(source="uz",target="en").translate("Assalomu alaykum O'qituvchi botingiz xizmatingizga tayor")}""", reply_markup=markup)
    # Send files
    elif message.text == "📎 Send files":
        bot.send_message(message.chat.id, "Hali ishga tushmagan yaqinda ishga tushadi")
        # markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        # markup.row("🖼photo","🎥Video")
        # markup.row("📑Documemt","🎧Audio")
        # markup.row("🔙 ortga")
        # bot.send_message(message.chat.id, "Choice", reply_markup=markup)
    # Upload file
    elif message.text == "📥Upload file":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🖼Pictures","🎥Videos")
        markup.row("📑Documemts","🎧Audios")
        markup.row("🔙 ortga")
        bot.send_message(message.chat.id, "Choice", reply_markup=markup)
    if message.text in ("🎧Audios",):
        fgfg=False
    else:
        fgfg=True
    # Rasm
    if message.text=="🖼Pictures":
        try:
            i=len(files[str(message.chat.id)]["rasm"])
            bolim[str(message.chat.id)]="rasm"
            bot.send_message(message.chat.id,f"Sizda {i}ta rasm bor\nIxtiyoriny rasm raqamini yuboring yoki 3:8 kabi oraliqdan foydalanishingiz ham mumkin!")
        except:
            bot.send_message(message.chat.id,"Sizda hozircha birorta ham rasm yo`q...")
    elif fgfg and ((str(message.chat.id) in bolim) and bolim[str(message.chat.id)]=="rasm"):
        try:
            t=(message.text).find(":",0,-1)
            if t not in [-1,0]:
                bosh=int((message.text)[0:t])
                end=int((message.text)[t+1:])
                for i in range(bosh,end+1):
                    markup=types.InlineKeyboardMarkup()
                    b1=types.InlineKeyboardButton("O'chirish",callback_data=f"rasm{i-1}")
                    b2=types.InlineKeyboardButton("❌",callback_data="yop")
                    markup.add(b2,b1)
                    bot.send_photo(message.chat.id,files[str(message.chat.id)]["rasm"][i-1],reply_markup=markup)
            else:
                son=int(message.text)
                markup=types.InlineKeyboardMarkup()
                b1=types.InlineKeyboardButton("O'chirish",callback_data=f"rasm{son-1}")
                b2=types.InlineKeyboardButton("❌",callback_data="yop")
                markup.add(b2,b1)
                bot.send_photo(message.chat.id,files[str(message.chat.id)]["rasm"][son-1],reply_markup=markup)
        except:
            bot.send_message(message.chat.id,"Nimadir xato ketdi!")
    # Document
    if message.text=="📑Documemt":
        try:
            i=len(files[str(message.chat.id)]["document"])
            bolim[str(message.chat.id)]="document"
            bot.send_message(message.chat.id,f"Sizda {i}ta fayl bor\nIxtiyoriny fayl raqamini yuboring yoki 3:8 kabi oraliqdan foydalanishingiz ham mumkin!")
        except:
            bot.send_message(message.chat.id,"Sizda hozircha birorta ham fayl yo`q...")
    elif fgfg and ((str(message.chat.id) in bolim) and bolim[str(message.chat.id)]=="document"):
        try:
            t=(message.text).find(":",0,-1)
            if t not in [-1,0]:
                bosh=int((message.text)[0:t])
                end=int((message.text)[t+1:])
                for i in range(bosh,end+1):
                    markup=types.InlineKeyboardMarkup()
                    b1=types.InlineKeyboardButton("O'chirish",callback_data=f"document{i-1}")
                    b2=types.InlineKeyboardButton("❌",callback_data="yop")
                    markup.add(b2,b1)
                    bot.send_photo(message.chat.id,files[str(message.chat.id)]["document"][i-1],reply_markup=markup)
            else:
                son=int(message.text)
                markup=types.InlineKeyboardMarkup()
                b1=types.InlineKeyboardButton("O'chirish",callback_data=f"document{son-1}")
                b2=types.InlineKeyboardButton("❌",callback_data="yop")
                markup.add(b2,b1)
                bot.send_document(message.chat.id,files[str(message.chat.id)]["document"][son-1],reply_markup=markup)
        except:
            bot.send_message(message.chat.id,"Nimadir xato ketdi!")
    # Video
    if message.text=="🎥Videos":
        try:
            i=len(files[str(message.chat.id)]["video"])
            bolim[str(message.chat.id)]="video"
            bot.send_message(message.chat.id,f"Sizda {i}ta fayl bor\nIxtiyoriny video raqamini yuboring yoki 03:8 kabi oraliqdan foydalanishingiz ham mumkin!")
        except:
            bot.send_message(message.chat.id,"Sizda hozircha birorta ham video yo`q...")
    elif fgfg and ((str(message.chat.id) in bolim) and bolim[str(message.chat.id)]=="video"):
        try:
            t=(message.text).find(":",0,-1)
            if t not in [-1,0]:
                bosh=int((message.text)[0:t])
                end=int((message.text)[t+1:])
                for i in range(bosh,end+1):
                    markup=types.InlineKeyboardMarkup()
                    b1=types.InlineKeyboardButton("O'chirish",callback_data=f"video{i-1}")
                    b2=types.InlineKeyboardButton("❌",callback_data="yop")
                    markup.add(b2,b1)
                    bot.send_video(message.chat.id,files[str(message.chat.id)]["video"][i-1],reply_markup=markup)
            else:
                son=int(message.text)
                markup=types.InlineKeyboardMarkup()
                b1=types.InlineKeyboardButton("O'chirish",callback_data=f"video{son-1}")
                b2=types.InlineKeyboardButton("❌",callback_data="yop")
                markup.add(b2,b1)
                bot.send_video(message.chat.id,files[str(message.chat.id)]["video"][son-1],reply_markup=markup)
        except:
            bot.send_message(message.chat.id,"Nimadir xato ketdi!")
    # Audio
    if message.text=="🎧Audios":
        try:
            i=len(files[str(message.chat.id)]["audio"])
            bolim[str(message.chat.id)]="audio"
            bot.send_message(
                message.chat.id,tr(source='uz', target='en').translate(
                    f"Audiolar {i}ta fayl bor\nIxtiyoriny audio raqamini yuboring yoki 03:8 "
                    f"kabi oraliqdan foydalanishingiz ham mumkin!"))
        except:
            bot.send_message(message.chat.id,tr(
                source='uz', target='en'
            ).translate("Sizda hozircha birorta ham qo'shiq yo'q"))
    elif fgfg and ((str(message.chat.id) in bolim) and bolim[str(message.chat.id)]=="audio"):
        try:
            t=(message.text).find(":",0,-1)
            if t not in [-1,0]:
                bosh=int((message.text)[0:t])
                end=int((message.text)[t+1:])
                for i in range(bosh,end+1):
                    markup=types.InlineKeyboardMarkup()
                    b1=types.InlineKeyboardButton("Delete",callback_data=f"audio{i-1}")
                    b2=types.InlineKeyboardButton("❌",callback_data="close")
                    markup.add(b2,b1)
                    bot.send_audio(message.chat.id,files[str(message.chat.id)]["audio"][i-1],reply_markup=markup)
            else:
                son=int(message.text)
                markup=types.InlineKeyboardMarkup()
                b1=types.InlineKeyboardButton("Delete",callback_data=f"rasm{son-1}")
                b2=types.InlineKeyboardButton("❌",callback_data="close")
                markup.add(b2,b1)
                bot.send_audio(message.chat.id,files[str(message.chat.id)]["audio"][son-1],reply_markup=markup)
        except:
            bot.send_message(message.chat.id,tr(source='uz', target='en').translate("Nimadir xato "
                                                                                                    "ketdi!"))
    else:
        if message.text in ("🎧Audios",):
            fgfg = False
        else:
            fgfg = True
        # Audio
        if message.text == "🎧Audios":
            try:
                i = len(files[str(message.chat.id)]["audio"])
                bolim[str(message.chat.id)] = "audio"
                bot.send_message(message.chat.id,
                                    f"Audiolar {i}ta fayl bor\nIxtiyoriny qo'shiq raqamini yuboring yoki 03:8 "
                                    f"kabi oraliqdan foydalanishingiz ham mumkin!")
            except:
                bot.send_message(message.chat.id, "Bizda hozircha birorta ham qo'shiq yo`q...")
        elif fgfg and ((str(message.chat.id) in bolim) and bolim[str(message.chat.id)] == "audio"):
            try:
                t = (message.text).find(":", 0, -1)
                if t not in [-1, 0]:
                    bosh = int((message.text)[0:t])
                    end = int((message.text)[t + 1:])
                    for i in range(bosh, end + 1):
                        markup = types.InlineKeyboardMarkup()
                        b1 = types.InlineKeyboardButton("❌", callback_data="yop")
                        markup.add(b1)
                        bot.send_audio(message.chat.id, files[str(message.chat.id)]["audio"][i - 1],
                                        reply_markup=markup)
                else:
                    son = int(message.text)
                    markup = types.InlineKeyboardMarkup()
                    b1 = types.InlineKeyboardButton("❌", callback_data="yop")
                    markup.add( b1)
                    bot.send_audio(message.chat.id, files[str(message.chat.id)]["audio"][son - 1],
                                    reply_markup=markup)
            except:
                bot.send_message(message.chat.id, "Nimadir xato ketdi!")

@bot.message_handler(content_types=["photo"])
def image(message):                                      	
     if message.from_user.id in admin_ids:
          for user_id2 in first_group_id:
            files[str(message.chat.id)]["rasm"].append(message.photo[-1].file_id)
            bot.send_message(message.chat.id,f"Bitta photo yuklandi va foydalanuvchilarga yuborildi\nindex: {len(files[str(message.chat.id)]['rasm'])}")
            bot.send_photo(user_id2, message.photo[-1].file_id)
     else:
          bot.send_message(message.chat.id,"Sizda bu buyruq uchun ruxsat yo'q")
############################################################################################################################################################
# DOCUMENT 1 AND 2
@bot.message_handler(content_types=["document"])
def document(message):
     if message.from_user.id in admin_ids:
          for user_id2 in first_group_id:
            bot.send_document(user_id2, message.document.file_id)
            files[str(message.chat.id)]["document"].append(message.document.file_id)
            bot.send_message(message.chat.id,f"Bitta video yuklandi va foydalanuvchilarga yuborildi\nindex: {len(files[str(message.chat.id)]['document'])}")
     else:
         bot.send_message(message.chat.id,"Sizda bu buyruq uchun ruxsat yo'q")
# def document2(message):
#      if message.from_user.id in admin_ids:
#           for user_id2 in second_group_id:
#             bot.send_document(user_id2, message.document.file_id)
#             files[str(message.chat.id)]["document"].append(message.document.file_id)
#             bot.send_message(message.chat.id,f"Bitta video yuklandi va foydalanuvchilarga yuborildi\nindex: {len(files[str(message.chat.id)]['document'])}")
#      else:
#          bot.send_message(message.chat.id,"Sizda bu buyruq uchun ruxsat yo'q")
##############################################################################################################################################################
@bot.message_handler(content_types=["video"])
def video(message):
     if message.from_user.id in admin_ids:
          for user_id2 in first_group_id:
            bot.send_video(user_id2, message.video.file_id)
            files[str(message.chat.id)]["video"].append(message.video.file_id)
            bot.send_message(message.chat.id,f"Bitta video yuklandi va foydalanuvchilarga yuborildi\nindex: {len(files[str(message.chat.id)]['video'])}")
     else:
          bot.send_message(message.chat.id,"Sizda bu buyruq uchun ruxsat yo'q")
@bot.message_handler(content_types=["audio"])
def audio(message):
     if message.from_user.id in admin_ids:
          for user_id2 in first_group_id:
            bot.send_audio(user_id2, message.audio.file_id)
            files[str(message.chat.id)]["audio"].append(message.audio.file_id)
            bot.send_message(message.chat.id,f"Bitta audio yuklandi va foydalanuvchilarga yuborildi\nindex: {len(files[str(message.chat.id)]['audio'])}")
     else:
          bot.send_message(message.chat.id,"Sizda bu buyruq uchun ruxsat yo'q")
@bot.callback_query_handler(func=lambda call:True)
def call(call):
	try:
		chat_id=call.message.chat.id
		if call.data[0:5]=="audio":
			try:
				sdf=int((call.data)[5:])
				(files[str(chat_id)]["audio"]).pop(sdf-1)
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
			except:
				pass
		if call.data=="yop":
			try:
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
			except:
				pass
	except:
		pass

# Speech to text start
@bot.message_handler(content_types=['voice'])
def voice_to_text1(message):
    # Ovozli habarni saqlab olish
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    # ogg formatini wavga aylantiramiz
    sound = AudioSegment.from_file('voice.ogg', format='ogg')
    sound.export('voice.wav', format='wav')
    # Ovozni matga aylantiramiz
    recognizer = sr.Recognizer()

    with sr.AudioFile('voice.wav') as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='uz-UZ')
    # Matnni foydalanuvchiga yuboramiz
    if message.from_user.id in admin_ids:
        for user_id in first_group_id:
                if user_id != message.from_user.id:
                    bot.send_message(user_id, text)
@bot.message_handler(content_types=['voice'])
def voice_to_text2(message):
    # Ovozli habarni saqlab olish
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    # ogg formatini wavga aylantiramiz
    sound = AudioSegment.from_file('voice.ogg', format='ogg')
    sound.export('voice.wav', format='wav')
    # Ovozni matga aylantiramiz
    recognizer = sr.Recognizer()

    with sr.AudioFile('voice.wav') as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='uz-UZ')
    # Matnni foydalanuvchiga yuboramiz
    if message.from_user.id in admin_ids:
        for user_id2 in second_group_id:
                if user_id2 != message.from_user.id:
                    bot.send_message(user_id2, text)
# Speech to text end
# Text to speech start
@bot.message_handler(commands=['text'])
def tts1(message):  
    engine.save_to_file(message.text, 'audio.wav')
    engine.runAndWait()
    sound = AudioSegment.from_wav('audio.wav')
    sound.export('audio.ogg', format='ogg')
    audio = open('audio.ogg', 'rb')
    if message.from_user.id in admin_ids:
        for user_id in first_group_id:
                if user_id != message.from_user.id:
                    bot.send_audio(user_id, audio)
    audio.close()
@bot.message_handler(commands=['text'])
def tts2(message):  
    engine.save_to_file(message.text, 'audio.wav')
    engine.runAndWait()
    sound = AudioSegment.from_wav('audio.wav')
    sound.export('audio.ogg', format='ogg')
    audio = open('audio.ogg', 'rb')
    if message.from_user.id in admin_ids:
        for user_id2 in second_group_id:
                if user_id2 != message.from_user.id:
                    bot.send_audio(user_id2, audio)
    audio.close()
# Text to speech end
def translate_en_uz(message):
    text = tr(source='en', target='uz').translate(message.text)
    bot.send_message(message.chat.id, text)
def translate_uz_en(message):
    text = tr(source='uz', target='en').translate(message.text)
    bot.send_message(message.chat.id, text)
def wikipedia_en(message):
    text = wikipedia.set_lang("en")
    text = wikipedia.summary(message.text)
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
