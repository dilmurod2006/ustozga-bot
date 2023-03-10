import telebot
from telebot import types
from deep_translator import GoogleTranslator
import glob
import json
bolim={"1":"s"}
bolim.clear()
files={"67361118":{"audio":[]}}
files.clear()
###########################################################
with open("obb.json","r",encoding="utf-8") as file1:
	files=json.load(file1)
with open("bolim.json","r",encoding="utf-8") as file2:
	bolim=json.load(file2)
############################################################################
bot_token="5988492660:AAFMWzbtYP4z8zbB4DHAlQErwSbFA6g-T_c"
bot = telebot.TeleBot(bot_token)
admin = [5420071824,67361118]
@bot.message_handler(commands=["start","help"])
def start_help(message):
    if message.chat.id == admin[0] or message.chat.id == admin[1]:
        if str(message.chat.id) not in files:
            files[str(message.chat.id)]={"audio":[]}
        else:
            if "audio" not in files[str(message.chat.id)]:
                files[str(message.chat.id)]["audio"]=[]
        data1=json.dumps(files)
        data1=json.loads(str(data1))
        with open("obb.json","w",encoding="utf-8") as file:
            json.dump(data1,file,indent=2)
        data2=json.dumps(bolim)
        data2=json.loads(str(data2))
        with open("bolim.json","w",encoding="utf-8") as file:
            json.dump(data2,file,indent=2)
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🎧Audio")
        bolim[str(message.chat.id)]=1
        bot.send_message(message.chat.id,GoogleTranslator(
            source='uz', target='en',).translate("Salom O'qituvchi!\nFile Cloud botga hush kelibsiz"),
                         reply_markup=markup)
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
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🎧Audio")
        bolim[str(message.chat.id)]=1
        bot.send_message(message.chat.id,"Assalomu alaykum!\nFile Cloud botga hush kelibsiz",reply_markup=markup)
@bot.message_handler(content_types=["text"])
def control(message):
	if message.chat.id == admin[0] or message.chat.id == admin[1]:
		if message.text in ("🎧Audio",):
			fgfg=False
		else:
			fgfg=True
		# Audio
		if message.text=="🎧Audio":
			try:
				i=len(files[str(message.chat.id)]["audio"])
				bolim[str(message.chat.id)]="audio"
				bot.send_message(
					message.chat.id,GoogleTranslator(source='uz', target='en').translate(
						f"Audiolar {i}ta fayl bor\nIxtiyoriny qo'shiq raqamini yuboring yoki 03:8 "
						f"kabi oraliqdan foydalanishingiz ham mumkin!"))
			except:
				bot.send_message(message.chat.id,GoogleTranslator(
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
				bot.send_message(message.chat.id,GoogleTranslator(source='uz', target='en').translate("Nimadir xato "
																									 "ketdi!"))
		else:
			if message.text in ("🎧Audio",):
				fgfg = False
			else:
				fgfg = True
			# Audio
			if message.text == "🎧Audio":
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
@bot.message_handler(content_types=["audio"])
def audio(message):
	try:
		files[str(message.chat.id)]["audio"].append(message.audio.file_id)
		# save audio.json file
		data1=json.dumps(files)
		data1=json.loads(str(data1))
		with open("obb.json","w",encoding="utf-8") as file:
			json.dump(data1,file,indent=2)
		bot.send_message(message.chat.id,f"Bitta qo'shiq yuklandi\nindex: {len(files[str(message.chat.id)]['audio'])}")
	except:
		bot.send_message(message.chat.id,"Nimadir Xato Ketdi\nqayta urinib ko'ring")
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
bot.polling(none_stop=True)
