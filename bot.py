import os
from dotenv import load_dotenv

import telebot
import requests

from ocr import TextScanner
from PIL import Image
import numpy as np

load_dotenv()
API_KEY = os.getenv("token")
scanner = TextScanner()

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands= ['greet'])
def greet(message):
    bot.reply_to(message, "Hey :)")
@bot.message_handler(content_types=['photo'])
def scan(message):
    #print(f"Photo: {message.photo}")
    file_id = message.photo[-1].file_id
    #print(f"File ID: {file_id}")
    file = bot.get_file(file_id)
    #print(f"File Path: {file.file_path}")
    url = f"https://api.telegram.org/file/bot{API_KEY}/{file.file_path}"
    image = np.array(Image.open(requests.get(url, stream = True).raw))
    processed_image = scanner.pre_process(image)
    text = scanner.image_to_text(processed_image)
    bot.reply_to(message, text)

bot.polling()