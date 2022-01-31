import pandas as pd
import nltk 
import numpy as np
import statistics

def get_word_list(n_letters=5):
    complete_word_list = nltk.corpus.words.words()
    five_letter_words = []
    word_series = []
    char_series = []
    for word in complete_word_list:
        if len(word) == n_letters:
            if word[0] == word[0].lower(): # removes any proper nouns
                word_series.append(word)