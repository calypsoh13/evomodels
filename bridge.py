import random
from cardutil import *

class bridge:
    ''' 
    Module to be used with hand class containing details specific to bridge hands and scoring
    ''' 
    maxscore = 37
    cardsinhand = 13
    
    
    def __init__(self):
        ''' 
        initialize scoring values
        ''' 
        # facecard value
        self.fcv = [0, 0, 0, 0]
        
        #distribution value
        self.dv = [0, 0, 0, 0]
        
        #broken suit penalty
        self.bsp = [0, 0, 0, 0]
        
        self.score = 0
        
        
    def Broken(cards, suit, count):
        '''
        This applies to singletons or doubles only.
        The following suits are considered broken: 
        K, Q, J, KQ, KJ, QJ, Qx or Jx
        '''
        suitstart = suit * 13
        upcards = cards[:13]
        
        # singletons or doubles only
        if count == 0 or count > 2:
            return False
        
        # an ace means it's not broken
        gotace = (suitstart + 12) in upcards
        
        if gotace:
            return False
        
        # no face cards means it's not broken
        gotking = (suitstart + 11) in upcards
        gotqueen = (suitstart + 10) in upcards
        gotjack = (suitstart + 9) in upcards
        
        if not (gotking or gotqueen or gotjack): 
            return False
        
        # at this point all suits are broken except Kx
        return not(count == 2 and gotking and not (gotqueen or gotjack))
            
    
    def calcscore(self, cards): 
        ''' 
        scores the hand by calculating face card score and distribution score
        ''' 
        counts = [0, 0, 0, 0]  
        self.fcv = [0, 0, 0, 0]
        self.dv = [0, 0, 0, 0]
        self.bsp = [0, 0, 0, 0]     
        
        # face card scoring: A-4, K-3, Q-2, J-1
        for i in range(0, 13):
            suit = toSuit(cards[i])
            counts[suit] += 1
            value = toValue(cards[i]) - 8
            if value > 0: 
                self.fcv[suit] += value
         
        # distribution scoring: Void-3, singleton-2, double-1  
        for i in range(0, 4):
            if counts[i] < 3: 
                self.dv[i] = 3 - counts[i]
                
            if bridge.Broken(cards, i, counts[i]):
                if self.fcv[i] > self.dv[i]:
                    self.bsp[i] = -self.fcv[i]
                else:
                    self.bsp[i] = -self.dv[i] 

        return sum(self.fcv) + sum(self.dv) + sum(self.bsp)
        
        
    def scoredetails(self):
    
        result = "face card values = " + str(self.fcv)
        result += " distribution values = " + str(self.dv)
        result += " broken suit penalties = " + str(self.bsp)
        
        return result 
        
# end class
