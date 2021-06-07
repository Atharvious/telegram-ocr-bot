# telegram-ocr-bot

Nice and simple ocr bot for telegram. Built just because I didn't wanna install another app on my phone.

The repository contains the source code to reproduce the bot. However, some additional files are needed to make it work:

* Tesseract - Just install the tesseract engine in ./teserract folder. If you already have it installed and in PATH, comment out line 2 in ocr.py.
* Bot API Token - Get a token from BotFather on telegram and use it in line 12 in bot.py. 
