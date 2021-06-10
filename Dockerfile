#Dockerfile, Image, Container
FROM python:3.9.4

ADD ocr.py .
ADD bot.py .
ADD .env .
ADD help_message.txt .
ADD nlp.py .
RUN apt update
RUN apt-get -y install tesseract-ocr

ADD . /tesseract-python
WORKDIR /tesseract-python

RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install pytesseract numpy opencv-python pillow python-dotenv pyTelegramBotAPI nltk networkx

CMD ["python", "./bot.py"]
