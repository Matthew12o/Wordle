import pandas as pd
import nltk
import pandas as pd
import statistics

def notIn(location, letter, dataset):
    filtered_dataset = dataset[dataset[location]!=letter]
    return filtered_dataset

def In(location, letter, dataset):
    filtered_dataset = dataset[dataset[location]==letter]
    return filtered_dataset

def InSomewhereElse(location, letter, dataset):
    filtered_dataset = notIn(location, letter, dataset)
    for i in range(5):
        filtered_dataset = pd.concat([filtered_dataset, In(i, letter, filtered_dataset)]).drop_duplicates()
    return filtered_dataset

def scoreFirstGuess(guess, word_set=None):
    if word_set is None:
        word_list = nltk.corpus.words.words()
        five_letter_words = []
        word_series = []
        char_series = []
        for word in word_list:
            if len(word) == 5:
                if word[0] == word[0].lower():
                    word_series.append(word)
                    char_series.append([word[0], word[1], word[2], word[3], word[4]])
        word_set = pd.DataFrame(char_series, index=word_series)
    
    prior = 1 / len(word_set.index)

    p_series = []
    counter = 1
    for answer in word_set.index:
        filtered_data = word_set
        for i in range(5):
            m = ''
            if guess[i] == answer[i]:
                m = 'G'
                filtered_data = In(i, guess[i], filtered_data)
            elif guess[i] in answer and guess[i] != answer[i]:
                m = 'Y'
                filtered_data = InSomewhereElse(i, guess[i], filtered_data)
            else:
                m = 'B'
                filtered_data = notIn(i, guess[i], filtered_data)
        prob = 1 / len(filtered_data.index)
        delta_prob = prob - prior
        p_series.append(delta_prob)
        average = statistics.mean(p_series)
        median = statistics.median(p_series)
    return {'Word': guess, 'Average' : average, 'Median' : median}

def solveFirstGuess(data = None):
    if data is None:
        word_list = nltk.corpus.words.words()

        # Get 5 Letter Words
        five_letter_words = []
        word_series = []
        char_series = []
        for word in word_list:
            word = word.lower()
            if len(word) == 5:
                word_series.append(word)
                char_series.append([word[0], word[1], word[2], word[3], word[4]])

        data = pd.DataFrame(char_series, index=word_series)

    prior = 1 / len(data.index)

    p_series = []
    average_series = []
    mean_series = []
    counter = 1
    for guess in data.index:
        print("{} / {} : {}".format(counter, len(data.index), counter/len(data.index)*100))
        p = []
        for answer in data.index:
            filtered_data = data
            for i in range(5):
                m = ''
                if guess[i] == answer[i]:
                    m = 'G'     
                    filtered_data = In(i, guess[i], filtered_data)
                elif guess[i] in answer and guess[i] != answer[i]:
                    m = 'Y'
                    filtered_data = InSomewhereElse(i, guess[i], filtered_data)
                else:
                    m = 'B'
                    filtered_data = notIn(i, guess[i], filtered_data)
            prob = 1 / len(filtered_data.index)
            delta_prob = prob - prior
            p.append(delta_prob)
        counter += 1
        p_series.append(p)
        average_series.append(statistics.mean(p))
        mean_series.append(statistics.median(p))
    data['Score'] = p_series
    data['Average Score'] = average_series
    data['Median Score'] = mean_series
    return data
