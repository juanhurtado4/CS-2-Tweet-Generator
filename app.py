from markov_sentence_generator import get_histogram, get_clean_data
from flask import Flask, request, render_template, redirect
import random
import sys
import re
import string
import pdb

app = Flask(__name__)
app.config['DEBUG'] = True

# TODO: Look into start and end tokens. 
# NOTE: Second order mk chain is fully functional, but does not produce results like first order.


def get_random_word(histogram):
    '''
    
    Histogram: Key Value pair. Key: String, Value: Int
    Returns a single word at random
    '''

    rand_num = random.random()

    cummulitive_wght = 0

    # pdb.set_trace()
    for key, value in histogram.items():

        word_likelyhood_percent = value / sum(histogram.values())

        cummulitive_wght += word_likelyhood_percent

        if rand_num <= cummulitive_wght:
            random_word = key
            break



    return random_word

    # list_of_words = list(histogram)
    #
    # result_word = ''
    #
    # while len(result_word) <= 0:
    #
    #     rand_index = random.randrange(0, len(list_of_words))
    #
    #     rand_word = list_of_words[rand_index]
    #
    #     if random.random() <= (histogram[rand_word] / sum(histogram.values())):
    #
    #         result_word = rand_word
    #
    # return result_word

def test_get_random_word(repetitions, histogram):
    '''
    Repetitions: Int
    Histogram: Key Value pair. Key: String | Value: Int
    Function returns histogram of random words returned by (get_random_word) function
    '''
    list_of_words = []

    for _ in range(repetitions):

        rand_word = get_random_word(histogram)

        list_of_words.append(rand_word)

    histogram = get_histogram(list_of_words)

    return histogram

def sentence_generator(num_words_in_sentence, histogram, starting_word):
    '''
    Num_words_in_sentence: Int
    Histogram: Dict. Key: String | Value: Int
    Starting_word: str
    Returns a string generated from a source text
    '''

    counter = 0

    list_of_words = list(histogram)

    sentence = starting_word + ' '

    while counter <= (num_words_in_sentence - 1):

        rand_word = get_random_word(histogram[starting_word])

        sentence += rand_word + ' '

        starting_word = rand_word.split(' ')[-1]

        counter += 2

    return sentence.strip().capitalize()
    # sentence = ''
    # for _ in range(num_words_in_sentence):
    #
    #     rand_word = get_random_word(histogram)
    #
    #     sentence += rand_word + ' '
    #
    # return sentence.strip().capitalize()

@app.route('/', methods=['GET', 'POST'])
def main():
    ''' Runs testing of get_random function based on command line arguments passed'''
    try:

        with open('obama_speech.txt') as file:
        # with open('short_version_obama_speech.txt') as file:

            raw_data = file.read().lower() # Makes sure file name is correct
            # get starting tokens based of regex pattern
            starting_words = get_start_end_tokens(raw_data, r'\.\s\w+\s')
            # get ending tokens based of regex pattern
            ending_words = get_start_end_tokens(raw_data, r'\s\w+\.')

    except:
        print('Please enter a valid file name')
        return

    if request.method == 'POST':

        clean_data = get_clean_data(raw_data)

        histogram = get_histogram(clean_data)

        try:

            sentence_length = int(request.form['sentence_length'])
        except:
            raise ValueError('please enter a number')
            return
        if sentence_length > 25:
            raise ValueError('Please enter a number less than 25')


        # test_result = test_get_random_word(sentence_length, histogram)

    # Turns dictionary into string so that it can be displayed in the browser
        # remove period and spaces in the starting token
        starting_word = random.choice(starting_words)[1:].strip()
        end_token = random.choice(ending_words)

        rand_sentence = sentence_generator(sentence_length, histogram, starting_word)
        rand_sentence += ' ' + end_token
        return render_template('display_sentence.html',
                                rand_sentence=rand_sentence)
    else:
        return render_template('show_form.html')

def get_start_end_tokens(text, pattern):
    '''
    text: str
    pattern: regular expression
    returns a list of start or ending token. Start token is found by a token that comes after a period. Ending token is found by a token that comes after a space and has a period at the end
    '''
    words = re.findall(pattern, text)
    clean_words = [word.strip() for word in words]
    return clean_words

if __name__=='__main__':
    app.run()
