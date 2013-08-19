def find_defining_class(obj, meth_name):
    """obj: any object
       meth_name: string
       returns the class that provides the definition of the method
    """
    for ty in type(obj).mro():
        if meth_name in ty.__dict__:
            return ty

class Card(object):
    """Represents a standard playing card.
       Map the following 4 suits to numbers:
       Spades -> 3
       Hearts -> 2
       Diamonds -> 1
       Clubs -> 0
    """
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                  'Jack', 'Queen', 'King']
    def __init__(self, suit=0, rank=2):
        # default card is 2 of Clubs
        self.suit = suit
        self.rank = rank
               
    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank], Card.suit_names[self.suit])
        
    def __cmp__(self, other):
        # # check the suits
        # if self.suit > other.suit: return 1
        # if self.suit < other.suit: return -1
        # # suits are the same... check ranks
        # if self.rank > other.rank: return 1
        # if self.rank < other.rank: return -1
        # # ranks are the same... it's a tie
        # return 0
        
        # Alternatively, use
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)

import random        
class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)
    def pop_card(self):
        return self.cards.pop()
    def add_card(self, card):
        self.cards.append(card)
    def shuffle(self):
        random.shuffle(self.cards)
    def sort(self):
        self.cards.sort()
    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())    
    def deal_hands(self, num_of_hands, cards_per_hand):
        hands = []
        for i in range(num_of_hands):
            hand = Hand()
            self.move_cards(hand, cards_per_hand)
            hands.append(hand)
        return hands
        
class Hand(Deck):
    """Represents a hand of playing cards."""
    def __init__(self, label=''):
        self.cards = []
        self.label = label
    def get_label(self):
        return self.label
        
if __name__ == '__main__':
    # card1 = Card(2, 11)
    # print card1
    # deck = Deck()
    # print deck
    # deck.shuffle()
    # print deck
    # deck.sort()
    # print deck
    # hand = Hand('new hand')
    # print hand.cards
    # print hand.label
    deck = Deck()
    deck.shuffle()
    for hand in deck.deal_hands(5, 5):
        print hand, '\n'
    hand = Hand()
    print find_defining_class(hand, 'shuffle')