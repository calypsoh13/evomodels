import random
from bridge import *
from cardutil import *

class hand:
    ''' 
    Class representing a hand in a card game.
    Cards are stored as 0 = 2 of clubs to 51 = Ace of spades.
    The first x cards represent the hand.
    ''' 
    drawcount = 0
    maxscore = bridge.maxscore
    cardsinhand = bridge.cardsinhand
    
    
    def __init__(self, cards = None, mr = 0.0):
        ''' 
        constructor allows initialization from scratch
        or from a parent hand
        ''' 
            
        self.module = bridge()
        
        if cards is None:
            self.cards = list(range(0,52))
            random.shuffle(self.cards)
            
            hand.drawcount += self.cardsinhand
        else:
            self.mutate(cards, mr)

        self.score = self.module.calcscore(self.cards)

                        
            
    def mutate(self, cards, mr):
        '''
        static method used by constructor to create a set of child cards
        with mutations
        '''
        self.mutationrate = mr
        self.cards = list(cards)
        
        if mr > 0.0:
        # check for mutation at each card
            for i in range(0, hand.cardsinhand):
                if random.random() < mr:
                
                    # shuffle the cards at the bottom of the deck
                    # this counts as one card shuffle for the total count
                    downcards = self.cards[hand.cardsinhand:]
                    random.shuffle(downcards)
                    hand.drawcount += 1
                    self.cards[hand.cardsinhand:] = downcards
                    
                    # mutation moves the current card
                    # to the bottom of the deck
                    self.cards.insert(51, self.cards.pop(i))
    
    
    def Mate(mom, dad, mr):
        '''
        creates a new hand via sexual reproduction
        '''
        momlist = mom[:hand.cardsinhand]
        random.shuffle(momlist)
        dadlist = dad[:hand.cardsinhand]
        random.shuffle(dadlist)
        upcards = set()
        
        while len(upcards) < hand.cardsinhand:
            upcards.add(momlist.pop())
            if len(upcards) < hand.cardsinhand:
                upcards.add(dadlist.pop())
        
        cards = list(upcards)
        cards.sort()
        
        #add the cards not in the upcard range
        downcards = list(set(range(0, 52)) - upcards)
        
        cards.extend(downcards)
        
        result = hand(cards, mr)
        result.score = result.module.calcscore(cards)
        
        return result

    def tostring(self):
        return cardstostring(self.cards, hand.cardsinhand, self.score)
        
# end class
