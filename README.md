## Nice and simple ocr bot for telegram. Built just because I didn't wanna install a seperate ocr app on my phone (and pc too for that matter).

This repository contains all the source code needed to reproduce the bot. The Dockerfile is pre-configured as well (but see the note below).

*A bot token is needed to make it work - Get a token from '**@BotFather**' on telegram, and use it in line 12 in **bot.py**.*

**To run without docker:**
* Select the python interpreter from env/Scripts.
* Make sure you have tesseract installed and added to PATH.
  * For **Windows** users, even if you don't have the tesseract engine up and running, you can run it by uncommenting line 2 in **ocr.py**, as I have provided a tesseract build in the repo itself.
  * For **linux** users, just have tesseract in PATH and don't change anything. You can also change line 2 in **ocr.py** to point to your tesseract installation, if not in PATH.

### Update: Also includes text summarization
An extractive summarization service has been added as well!

### To see the bot in action, search for '**@tescannerbot**' in Telegram and add it.

Possible issues: 
* If running on Linux, you might need to install the packeges in requirements.txt in a local environment, as opencv-python tends to face dependency problems.
