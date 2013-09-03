# Problem Set 6: 6.00 Word Game, computer player
#

import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code

WORDLIST_FILENAME = "words.txt"

def load_words():
    """ Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def sorted_letters(lst):
    """returns a list of strings, where each string is made by joining a 
    subset of lst.
    
    lst: list
    
    """
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    result.remove([])
    return list(set([''.join(sorted(subset)) for subset in result]))
    
# (end of helper code)
# -----------------------------------

def get_words_to_points(word_list):
    """Return a dict that maps every word in word_list to its point value."""
    word_points = {}
    for word in word_list:
        score = 0.0
        for letter in word:
            score += SCRABBLE_LETTER_VALUES[letter]
        if len(word) == HAND_SIZE:
            score += 50
        word_points[word] = score
    return word_points

def get_word_rearrangements(word_list):
    """For word in word_list, sort the letters in word and make them a string 
    called sorted_letters. Returns a dictionary d, where 
    d[sorted_letters] = word
    
    word_list: list of strings
    return: dict (string -> string)
    
    """
    d = {}
    for word in word_list:
        letter_list = []
        for letter in word:
            letter_list.append(letter)
        sorted(letter_list)
        s = ''.join(letter_list)
        d[s] = word
    return d

    
def get_time_limit(points_dict, k):
    """Return the time limit for the computer player as a function of the
    multiplier k. points_dict should be the same dictionary that is created by
    get_words_to_points.
    
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.
    for word in points_dict:
        pass
    end_time = time.time()
    return (end_time - start_time) * k    

def display_hand(hand):
    """Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,              # print all on the same line
    print                              # print an empty line

def deal_hand(n):
    """Returns a random hand containing n lowercase letters. At least n/3 the 
    letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are letters and the values 
    are the number of times the particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1        
    return hand

def update_hand(hand, word):
    """Assumes that 'hand' has all the letters in word. In other words, this 
    assumes that however many times a letter appears in 'word', 'hand' has at 
    least as many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    
    """
    left_in_hand = hand.copy()
    for letter in word:
        left_in_hand[letter] = left_in_hand[letter] - 1
    return left_in_hand
    
    
def pick_best_word(hand, points_dict):
    """ Return the highest scoring word from points_dict that can be made with 
    the given hand. Return '.' if no words can be made with the given hand.
    
    """    
    temp_list = []
    for letter in hand:
        for i in range(hand[letter]):
            temp_list.append(letter)
    K = len(temp_list)
    temp_dict = {}
    for k in range(K):
        for i in range(K-k):
            key = ''.join(temp_list[i:i+k+1])
            val = temp_list[:i] + temp_list[i+k+1:]
            temp_dict[key] = val        
    highest_score = 0
    best_word = '.'
    for key in temp_dict:
        for half_word in temp_dict[key]:
            possible_word = key + half_word
            possible_word_score = points_dict.get(possible_word,0)
            if highest_score < possible_word_score:
                highest_score = possible_word_score
                best_word = possible_word
    return best_word

def pick_best_word_faster(hand, points_dict, rearrange_dict):
    """Return the highest scoring word from rearrange_dict that can be made 
    with the given hand. Return '.' if no words can be made with the given hand.
    
    """    
    temp_list = []
    for letter in hand:
        for i in range(hand[letter]):
            temp_list.append(letter)
    hand_subsets = sorted_letters(temp_list)

    highest_score = 0
    best_word = '.'

    for elt in hand_subsets:
        if elt in rearrange_dict:
            possible_word = rearrange_dict[elt]
            possible_word_score = points_dict.get(possible_word,0)
            if highest_score < possible_word_score:
                highest_score = possible_word_score
                best_word = possible_word
    return best_word
    
#
# Problem #4: Playing a hand
#
def play_hand(hand, points_dict, rearrage_dict):
    """Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      points_dict: dict (string -> int) (word -> points)
      rearrange_dict: dict (string -> string) (sorted letters -> word)
    
    """
    
    time_limit = get_time_limit(points_dict, 100) # computer play
    print 'Time limit for computer player is: %0.2f' %time_limit
    print
    print "current hand: "
    display_hand(hand)
    total_score = 0.0
    
    while True:
        start_time = time.time()
        # userInput = pick_best_word(hand, points_dict)
        userInput = pick_best_word_faster(hand, points_dict, rearrange_dict)
        end_time = time.time()
        total_time = end_time - start_time
        print 'it took %0.2f seconds to provide an answer.' %total_time
        
        time_limit -= total_time
        if time_limit > 0:
            print 'you have %0.2f seconds remaining.' %time_limit
        else:
            print 'total time exceeds %0.2f seconds.' %abs(time_limit)
            break
            
        divisor = total_time
        if total_time < 0.1: divisor = 1 
        if userInput == '.' or sum(hand.values()) == 0:
            break
        hand = update_hand(hand, userInput)
        word_score = points_dict[userInput] / divisor
        total_score += word_score
        print 'score for your word: %0.2f' %word_score
        print 'your total score: %0.2f' %total_score
        print 'make a word using these remaining letters: '
        display_hand(hand)
    print
    print 'The hand finishes, and your total score is %0.2f' %total_score

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(points_dict, rearrange_dict):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO ...
    # print "play_game not implemented."         # delete this once you've completed Problem #4
    # play_hand(deal_hand(HAND_SIZE), word_list) # delete this once you've completed Problem #4
    
    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    while True:
       cmd = raw_input('Enter n to deal a new hand, r to replay the last ' + 
                       'hand, or e to end game: ')
       if cmd == 'n':
           hand = deal_hand(HAND_SIZE)
           play_hand(hand.copy(), points_dict, rearrange_dict)
           print
       elif cmd == 'r':
           play_hand(hand.copy(), points_dict, rearrange_dict)
           print
       elif cmd == 'e':
           break
       else:
           print "Invalid command."

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    points_dict = get_words_to_points(word_list)
    rearrange_dict = get_word_rearrangements(word_list)
    play_game(points_dict, rearrange_dict)

