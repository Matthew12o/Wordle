from turtle import pd
from numpy import char
import pandas as pd
import nltk 
import pandas as pd
import statistics
import multiprocessing as mp
from functions import scoreFirstGuess
import csv


def main():
    word_list = nltk.corpus.words.words()
    five_letter_words = []
    for word in word_list:
        if len(word) == 5:
            if word[0] == word[0].lower():
                five_letter_words.append(word)
    
    word_series = []
    char_series = []
    for word in five_letter_words:
        word = word.lower()
        word_series.append(word)
        char_series.append([word[0], word[1], word[2], word[3], word[4]])
    wordset = pd.DataFrame(data=char_series, index=word_series)

    pool_size = mp.cpu_count()
    pool = mp.Pool(pool_size)
    ## for testing 
    test_data = wordset[0:pool_size]
    result = pool.starmap(scoreFirstGuess, [(word, wordset) for word in test_data.index])

    ## for full run
    #test_data = wordset[0:pool_size]
    #result = pool.starmap(scoreFirstGuess, [(word, wordset) for word in wordset.index])
    pool.close()

    keys = result[0].keys()
    with open('./results.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)

if __name__ == '__main__':
    main()

