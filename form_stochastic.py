from dictionary_histogram import get_histogram
from flask import Flask, request, render_template, redirect
import random
import sys
import re
import string

app = Flask(__name__)
app.config['DEBUG'] = True

def get_clean_data(raw_data):
    '''
    raw_data: String
    Function cleans raw_data from punctuations, numbers, spaces etc, to only leave words
    Returns list
    '''

    crowd_reaction_removed = re.sub('\(\w*\)', '', raw_data)

    crowd_reaction_removed = re.sub('\(\w*\s\w*\)', '', crowd_reaction_removed)

    numbers_removed = re.sub('\d\w*', '', crowd_reaction_removed)

    punctuationless_data = ''.join([char for char in numbers_removed
                                    if char not in string.punctuation])# Removes punctuation from data

    clean_data = re.split('\s*', punctuationless_data)[:-1]  # Splits data based on whitespace

    return clean_data

def get_random_word(histogram):
    '''
    Histogram: Key Value pair. Key: String, Value: Int
    Returns a single word at random
    '''
    list_of_words = list(histogram)

    result_word = ''

    while len(result_word) <= 0:
        rand_index = random.randrange(0, len(list_of_words))

        rand_word = list_of_words[rand_index]

        if random.random() <= (histogram[rand_word] / sum(histogram.values())):

            result_word = rand_word

    return result_word

def test_get_random_word(repetitions, clean_data, histogram):
    '''
    Repetitions: Int
    Clean_data: List
    Histogram: Key Value pair. Key: String | Value: Int
    Function returns histogram of random words returned by (get_random_word) function
    '''
    list_of_words = []

    for _ in range(repetitions):

        rand_word = get_random_word(histogram)

        list_of_words.append(rand_word)

    histogram = get_histogram(list_of_words)

    return histogram

@app.route('/', methods=['GET', 'POST'])
def main():
    ''' Runs testing of get_random function based on command line arguments passed'''
    try:

        with open('obama_speech.txt') as file:

            raw_data = file.read().lower() # Makes sure file name is correct

    except:
        print('Please enter a valid file name')
        return

    if request.method == 'POST':

        clean_data = get_clean_data(raw_data)

        histogram = get_histogram(clean_data)

        repetitions = int(request.form['sentence_length'])

        testing_result = test_get_random_word(repetitions, clean_data, histogram)

    # Turns dictionary into string so that it can be displayed in the browser
        rand_sentence = ' '.join(word for word in testing_result)

        return '<h1>{rand_sentence}</h1>'.format(rand_sentence=rand_sentence)

    else:
        return render_template('display_sentence.html')

if __name__=='__main__':
    app.run()
