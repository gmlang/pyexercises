from Card import *

class PokerHand(Hand):
    """represent a poker hand"""
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand. Stores the 
        result in attribute suits.
        
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
    
    def rank_hist(self):
        """Builds a histogram of the ranks that appear in the hand. Stores the 
        result in attribute ranks.
        
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) +1
            
    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise. 
        
        Works correctly for hands with 2 or more cards.
        
        """
        self.rank_hist()
        for val in self.ranks.values():
            if val == 2:
                return True
        return False
        
    def has_twopair(self):
        """Returns True if the hand has two pairs, False otherwise.
        
        Works correctly for hands with 4 or more cards.
        
        """
        self.rank_hist()
        count_pairs = 0
        for val in self.ranks.values():
            if val == 2:
                count_pairs += 1
        if count_pairs >= 2:
            return True
        return False
    
    def has_threeOfaKind(self):
        """Returns True if the hand has three cards with the same rank, and
        False otherwise.
        
        Works correctly for hands with 3 or more cards
        
        """
        self.rank_hist()
        for val in self.ranks.values():
            if val == 3:
                return True
        return False
        
    def has_straight(self):
        """Returns True if the hand has a straight, False otherwise.
        
        A straight is 5 cards with ranks in sequence (aces can be high or low, 
        so Ace-2-3-4-5 is a straight and so is 10-Jack-Queen-King-Ace, but 
        Queen-King-Ace-2-3 is not.) 
        
        Works correctly for hands with 5 or more cards
        
        """
        self.rank_hist()
        sorted_ranks = sorted(self.ranks.keys())
        # print sorted_ranks
        counter = 0
        for i in range(len(sorted_ranks)):
            if counter == 4:
                return True
            if i < len(sorted_ranks)-1:
                if counter == 3 and sorted_ranks[i] == 13:
                    return sorted_ranks[i+1] == 1
                if sorted_ranks[i] + 1 == sorted_ranks[i+1]:
                    counter += 1
                    # print i, counter
                else:
                    counter = 0
        return False        
        
    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
        
        Works correctly for hands with 5 or more cards.
        
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
    
    def has_fullhouse(self):
        """Returns True if the hand has a full house, False otherwise.
        
        A full house has 3 cards with one rank and 2 cards with another.
        
        Works correctly for hands with 5 or more cards.
        
        """
        return self.has_threeOfaKind() and self.has_pair()
      
    def has_fourOfaKind(self):
        """Returns True if the hand has four cards with the same rank, and 
        False otherwise.
        
        Works correctly for hands with 4 or more cards.
        
        """
        self.rank_hist()
        for val in self.ranks.values():
            if val == 4:
                return True
        return False
        
    def has_straightFlush(self):
        """Returns True if the hand has a straight flush, False otherwise.
        
        Works correctly for hands with 5 or more cards
        
        """
        return self.has_straight() and self.has_flush()
    
    def classify(self):
        """Finds the highest-value classification for a hand and sets the label
        attribute accordingly"""
        highest = 'normal'
        if self.has_pair():
            highest = 'a pair'
        if self.has_twopair():
            highest = 'two pairs'
        if self.has_threeOfaKind():
            highest = 'three of a kind'
        if self.has_straight():
            highest = 'straight'
        if self.has_flush():
            highest = 'flush'
        if self.has_fullhouse():
            highest = 'full house'
        if self.has_fourOfaKind():
            highest = 'four of a kind'        
        if self.has_straightFlush():
            highest = 'straight flush'
        self.label = highest

def check_has_straight():
    hand=PokerHand()
    hand.cards = [Card(0, 1),Card(0, 2),Card(0, 3),Card(0, 4),Card(0, 5)]
    print hand.has_straight()
        
def probs_of_classifications(deck, classification = {}):
    """shuffles a deck of cards, divides it into hands, classifies the hands,
    and counts the number of times various classifications appear.
    
    deck: Deck
    
    returns a dictionary of classifications as keys and their counts as values.
    
    """
    # shuffle the deck
    deck.shuffle()
    # deal the cards and classify the hands
    for i in range(10):
        hand = PokerHand()
        deck.move_cards(hand, 5)
        hand.sort()
        hand.classify()
        classification[hand.get_label()] = \
            classification.get(hand.get_label(), 0) + 1
    return classification

    
if __name__ == '__main__':
    # make a deck
    # deck = Deck()
    # deck.shuffle()

    # # deal the cards and classify the hands
    # for i in range(3):
        # hand = PokerHand()
        # deck.move_cards(hand, 7)
        # hand.sort()
        # hand.classify()
        # print hand.get_label()
        # print hand
        # # print hand.has_pair()
        # # print hand.has_twopair()
        # # print hand.has_threeOfaKind()
        # # print hand.has_straight()
        # # print hand.has_flush()
        # # print hand.has_fullhouse()
        # # print hand.has_fourOfaKind()
        # # print hand.has_straightFlush()
        # print ''
        # check_has_straight()
    
    deck = Deck()
    classification = probs_of_classifications(deck)
    N = 200000
    # N = 100000
    for i in range(N):
        deck = Deck()
        classification = probs_of_classifications(deck, classification)    
    print 'classification\t\tprobability'
    for key in sorted(classification, key=classification.get):
        print str(key) + '\t\t\t' +\
              str(classification[key] * 100.0 / (N * 10)) + '%'
    print 'sum\t\t\t' +\
          str(sum(classification.values()) * 100.0 / (N * 10))+ '%'