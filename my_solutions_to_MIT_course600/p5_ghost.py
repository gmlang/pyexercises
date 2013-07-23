# Problem Set 5: Ghost
#

import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
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

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

# TO DO: your code begins here!

def is_valid(letter):
    """
    returns True if letter is one alphabetic character, False otherwise
    
    letter: string
    return: logical
    """
    if len(letter) == 1 and letter in string.ascii_letters: return True
    else: return False

def end_or_not(word_fragment):
    """
    returns {'because word_fragment is a word!': True} if word_fragment is a word with length > 3 
    returns {'because no word begins with word_fragment!': True} if no words can be formed folowing word_fragment
    returns {'': False} otherwise
    
    word_fragment: string
    return: dictionary
    """
    status = False
    s = ''
    if len(word_fragment) > 3 and word_fragment in wordlist:
        status = True
        s = "because '" + word_fragment + "' is a word!"
    cnt = 0
    for word in wordlist:
        if word_fragment not in word:
            cnt += 1
    if cnt == len(wordlist):
        status = True
        s = "because no word begins with '" + word_fragment + "'!"
    return {s:status}
    
def main():
    print 'Welcome to Ghost!'
    print 'Player 1 goes first.'
    word_fragment = ''

    while True:
        print 'Current word fragment: ', "'"+word_fragment+"'"
        player1_letter = raw_input()
        while not is_valid(player1_letter):
            print 'You entered something invalid. Please enter an alphabetic character: '
            player1_letter = raw_input()
        print 'Player 1 says letter: ', player1_letter
        print        
        word_fragment += player1_letter.lower()
        check = end_or_not(word_fragment) # check is a dict of 1 key-val pair
        if check.values()[0]: # if end of game
            print 'player 1 loses ' + check.keys()[0]
            print 'player 2 wins!'
            break
            
        print 'Current word fragment: ', "'"+word_fragment+"'"
        print "Player 2's turn."
        player2_letter = raw_input()
        while not is_valid(player2_letter):
            print 'You entered something invalid. Please enter an alphabetic character: '
            player2_letter = raw_input()
        print 'Player 2 says letter: ', player2_letter
        print
        word_fragment += player2_letter.lower()
        check = end_or_not(word_fragment) # check is a dict of 1 key-val pair
        if check.values()[0]: # if end of game
            print 'player 2 loses ' + check.keys()[0]
            print 'player 1 wins!'
            break    
    
if __name__ == '__main__':
    main()