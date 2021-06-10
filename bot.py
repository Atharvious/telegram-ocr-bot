import os
from dotenv import load_dotenv

import telebot
import requests

from ocr import TextScanner
from nlp import ExtractiveSummarizer
from PIL import Image
import numpy as np

load_dotenv()
API_KEY = os.getenv("token")
print("Initializing ocr scanner....")
scanner = TextScanner()
print("Done.")
print("Initializing nlp engine....")
e_summarizer = ExtractiveSummarizer()
print("Done.")

print("Initializing the bot....")
bot = telebot.TeleBot(API_KEY)
with open("help_message.txt", 'r') as f:
    help_text = f.read()

print("Bot Active.")



@bot.message_handler(commands=['help', 'about'])
def help(message):
    bot.send_message(message.chat.id,help_text)


    



@bot.message_handler(commands=['summary'])
def summarize(message):
    msg = bot.send_message(message.chat.id, "What do you wanna summarize?")
    bot.register_next_step_handler(msg, summarize)

def summarize(message):
    text = message.text
    original_words, original_sentences = e_summarizer.statistics(text)
    text_stats = f"Original counts:\nWords: {original_words}\nSentences: {original_sentences}"
    bot.send_message(message.chat.id, text_stats)
    summary = e_summarizer.summarize(text)
    bot.reply_to(message, summary)
    summarized_words, summarized_sentences = e_summarizer.statistics(summary)
    summary_stats = f"Summarized counts:\nWords:{summarized_words}\nSentences: {summarized_sentences}"
    bot.send_message(message.chat.id, summary_stats)
    print("Just summarized a passage.")


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
    print("Just did a scan.")

bot.polling()