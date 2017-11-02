import random, sys, re, string

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
        if random.random() <= (len(list_of_words) / histogram[rand_word]):
            result_word = rand_word

    return result_word
    # for key, value in histogram.items():
    #     if random.random() <= len(histogram) / value:
    #         result_key = key
    #         break



    # rand_index = random.randrange(0, len(list_of_words))
    #
    # return  list_of_words[rand_index]

def test_get_random_word():



def main():

    try:
        file_name = sys.argv[1]
        with open(file_name) as file:

            raw_data = file.read().lower()

    except:
        print('Please enter a valid file name')
        return

    clean_data = get_clean_data(raw_data)

    random_word = get_random_word(clean_data)

if __name__=='__main__':
    main()
