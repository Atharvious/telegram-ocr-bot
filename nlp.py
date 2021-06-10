#--------------------------Imports--------------------------

#For Extractive Summarization
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

#For Abstract Summarization
#import torch
#import json
#from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

#--------------------------Extractive Classificaiton--------------------------
class ExtractiveSummarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))


    def statistics(self, text):
        num_words = len(word_tokenize(text))
        num_sentences = len(sent_tokenize(text))
        return num_words, num_sentences
    def summarize(self, text):
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        #-----------------Word scoring--------------------
        frequency_table = {}
        for word in words:
            word = word.lower()
            if word in self.stop_words:
                continue
            if word in frequency_table:
                frequency_table[word] += 1
            else:
                frequency_table[word] = 1
        #-----------------Sentence scoring----------------
        sentence_values = {}
        for sentence in sentences:
            for word, freq in frequency_table.items():
                if word in sentence.lower():
                    if sentence in sentence_values:
                        sentence_values[sentence] += freq
                    else:
                        sentence_values[sentence] = freq
        #----------------Calculate Average------------------

        value_sum = 0
        for sentence in sentence_values:
            value_sum += sentence_values[sentence]
        
        avg = int(value_sum / len(sentence_values))

        summary = ""

        for sentence in sentences:
            if (sentence in sentence_values) and (sentence_values[sentence] > (1.3 * avg)):
                summary += " " + sentence
        return summary

#-----------------------------------------------Abstract Classification--------------------------------------------
"""class AbstractSummarizer:
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def summarize(self, text):
        preprocess_text = text.strip().replace("\n","")
        t5_prepared_text = "summarize: " + preprocess_text
        tokenized_text = self.tokenizer.encode(t5_prepared_text, return_tensors="pt").to(self.device)

        summary_ids = self.model.generate(
            tokenized_text,
            num_beams=4,
            no_repeat_ngram_size=2,
            min_length = 50,
            max_length = 150,
            early_stopping = True,
            )
        summary = self.tokenizer.decode(summary_ids[0],
                    skip_special_tokens = True,
        )
        return summary"""
#--------------------------------------------------Test Function--------------------------------------------------

def test():
    with open("sample_text.txt", 'r') as f:
        sample_text = f.read()
    print(f"Sample Text:\n{sample_text}\n Number of Characters:\t {len(sample_text)}\n\n")


    #Asummarizer = AbstractSummarizer()
    Esummarizer = ExtractiveSummarizer()


    extractive_summary = Esummarizer.summarize(sample_text)
    print(f"Extractive Summary:\n{extractive_summary}\n Number of Characters:\t {len(extractive_summary)}\n\n")

    #abstract_summary = Asummarizer.summarize(sample_text)
    #print(f"Abstract Summary:\n{abstract_summary}\n Number of Characters:\t {len(abstract_summary)}")

#-----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    test()