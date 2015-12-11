import random
from hand import *

class cardevolution:
    ''' 
    Simulates the evolution of card hands to maximize the score of a bridge hand.
    
    The odds of getting a perfect bridge hand can be found here: 
    http://mathworld.wolfram.com/Bridge.html
    
    The simulation can be customized to use asexual or sexual reproduction.
    The population, mutation rate and selection pressures can also be customized.
    Use the verbose field to produce stats after each generation.
    
    To run a simulation, use Idle 3.3 to open and run cardevolution.py, then type the following:
        > ce = cardevolution()
        > ce.run(500)
    (The parameter for the run call is the maximum number of generations)
    
    Example using customized fields: 
        > ce = cardevolution()
        > ce.mr = 0.2
        > ce.sex = True
        > ce.run(500)
    See the __init__ method for more customizable field  names.
    
    Developers: to use this module for different types of hands and scoring, 
    replace the bridge module.  For example, a poker hands simulation would provide
    an interesting fitness function with many local maximums, while cribbate would provide
    a much smoother fitness function.
    '''
    
    def __init__(self):
        
        self.cardsinhand = hand.cardsinhand
        
        # use these fields to tailor the simulation
        #population
        self.population = 50
        
        # mutation rate: defaults to average 1 mutation per hand
        self.mr   = 1/self.cardsinhand
        
        # use sexual reproduction
        self.sex = False
        
        # baseline number of children for hand with mean score
        self.childrenbaseline = 4
        
        # reproduction survival pressure 
        # percent increase in children for each percent increase in score
        self.rsp = 1.0
        
        # survivor selection pressure
        # percent of survivors chosen by fitness vs random sample
        self.ssp = 0.80        
        
        # fitness goal for the run function
        self.fitnessgoal = hand.maxscore
        
        # whether to print score summaries for each nextgen call
        self.verbose = False
        
        # result
        self.generation = None;
        self.initialstats = None;
        self.lateststats = None;
    
    '''
    Produces the first generation
    '''
    def start(self, silent = False, hands = None):
        self.generation = 0
        
        if hands is None:
            self.hands = []
            for i in range(0, self.population):
                self.hands.append(hand())
                self.hands.sort(key=lambda x: x.score, reverse=True)
        else:
            self.hands = list(hands[:self.population])
        self.handscreated = self.population

        self.initialstats = cardevolution.calcstats(self.hands)
        self.lateststats = self.initialstats
        if not silent:
            self.printsimulationproperties()
            
            print(" ")
            print("Generation 0 results:")
            cardevolution.printstats(self.initialstats)
            if self.verbose: cardevolution.printscores(self.hands)
     
    '''
    Produces the next generation
    '''
    def nextgen(self, silent = False):
        
        if self.generation is None: 
            self.start(silent)
            
        self.generation += 1
        
        if not silent:  
            print("Generation:", self.generation, "results")
            if self.verbose: 
                self.printsimulationproperties()
        
        parents = list(self.hands)
        parentstats = self.lateststats
        
        children = []
        
        while len(children) < self.population:
            for parent in parents:
                parent.numberChildren = self.getNumberChildren(parent.score, parentstats[2])
                for i in range(0, parent.numberChildren):
                    if (self.sex):
                        children.append(self.makeachild(parent, parents))
                    else:
                        children.append(self.makeabud(parent))
        l = len(children)
        self.handscreated += l
        
        if not silent:  
            print("number of hands dealt (cumulative):", self.handscreated)
            
            if self.verbose and self.rsp != 0.0:
            
                print(" ")
                print("Reproduction summary:")
                for i in range(0, hand.maxscore + 1):
                    count = sum(1 for h in parents if h.score == i)
                    if count > 0:
                        p = [h for h in parents if h.score == i][0]
                        print(count, " parents with score ", i, " produced ", p.numberChildren, " children each")
            
            if l > self.population:
                print(" ")
                print("Children summary: count = ", len(children))
                cardevolution.printstats(cardevolution.calcstats(children))
                if self.verbose: cardevolution.printscores(children)
        
        
        # apply selection pressure
        if self.ssp == 0 or l <= self.population:
            selectionsurvivors = children
            if not silent: 
                "No fitness selection applied."
        else:
            sp = l - int((l - self.population) * self.ssp)
            children.sort(key=lambda x: x.score, reverse=True)
            selectionsurvivors = children[:sp]

            if not silent:
                print(" ")
                print("Results after fitness selection: count = ", len(selectionsurvivors))
                cardevolution.printstats(cardevolution.calcstats(selectionsurvivors))        
                if self.verbose:  cardevolution.printscores(selectionsurvivors)
        
        l = len(selectionsurvivors)
        if l > self.population:
            random.shuffle(selectionsurvivors)
        self.hands = selectionsurvivors[:self.population]
        self.lateststats = cardevolution.calcstats(self.hands)
        
        if not silent:
            if l > self.population:
                print(" ")
                print("Results after random bottleneck selection: count = ", len(self.hands))
                cardevolution.printstats(self.lateststats)
                if self.verbose: cardevolution.printscores(self.hands)
            else:
                print("No random bottleneck selection applied.")
            
        return len([h for h in self.hands if h.score >= self.fitnessgoal]) > 0
        
    def makeabud(self, parent):
        return hand(parent.cards, self.mr)
                    
    def makeachild(self, mom, parents):
        dad = None
        while mom != dad:
            dad = random.choice(parents)
        return hand.Mate(mom.cards, dad.cards, self.mr)

    def printsimulationproperties(self):
        print(" ");
        print("Simulation properties: ")
        print("    population                :", self.population)
        print("    mutation rate             :", self.mr)
        print("    sexual reproduction       :", self.sex)
        print("    # children - baseline     :", self.childrenbaseline)
        print("    selection pressures:")
        print("      reproduction            :", self.rsp)
        print("      survival                :", self.ssp)              
                                
    def getNumberChildren(self, score, meanscore):
    
        self.childrenbaseline
        pctincrscore = ((score - meanscore)/meanscore)
        pctincrchildren = pctincrscore * self.rsp
        adj = round(self.childrenbaseline * pctincrchildren)
        return max(0, self.childrenbaseline + adj)    
            
    def calcstats(cards):
        scores = sorted([h.score for h in cards])
        c = mean(scores)
        sd = pstdev(scores, c)
        return (scores[0], scores[-1], c, sd)
        
    def printstats(stats):
        (min, max, c, sd) = stats
        print("    min:  ", min)
        print("    max:  ", max)
        print("    mean: ", c)
        print("    sd:   " , sd)
        return stats
        
    def printscores(cards):
        print(" ")
        for i in range(0, hand.maxscore + 1):
            count = sum(1 for h in cards if h.score == i)
            if count > 0:
                print(count, " hands scored ", i)
    
    def printhands(self, verbose = True):
        for hand in self.hands:
            print(hand.tostring())
            if verbose:
                print(hand.scoredetails())
                
    def getresult(self):
        
        return { 
            'population' : self.population,
            'mr' : self.mr,
            'sex' : self.sex,
            'childrenbaseline' : self.childrenbaseline,
            'rsp' : self.rsp,
            'ssp' : self.ssp,
            'generation' : self.generation,
            'min0' : self.initialstats[0],
            'max0' : self.initialstats[1],
            'mean0' : self.initialstats[2],
            'sd0' : self.initialstats[3],
            'min' : self.lateststats[0],
            'max' : self.lateststats[1],
            'mean' : self.lateststats[2],
            'sd' : self.lateststats[3]
            }
             
        # baseline number of children for hand with mean score
        self.childrenbaseline = 4
        
        # reproduction survival pressure 
        # percent increase in children for each percent increase in score
        self.rsp = 1.0
        
        # survivor selection pressure
        # percent of survivors chosen by fitness vs random sample
        self.ssp = 0.80        
        
        # fitness goal for the run function
        self.fitnessgoal = hand.maxscore
        
        # whether to print score summaries for each nextgen call
        self.verbose = False
        
        # result
        self.generation = None;
        self.initialstats = None;
        self.lateststats = None;
                
    def run(self, maxgenerations, hands = None):
        self.start(False, hands)

        success = False
        
        while (not success and self.generation < maxgenerations):
            success = self.nextgen(True)
        print(" ")
        print("Run complete.  Success = ", success)
        print(" ")
        print("Generation ", self.generation, "results")
        print("    number of hands dealt (cumulative):", self.handscreated)
        cardevolution.printstats(self.lateststats)
        if self.verbose: cardevolution.printscores(self.hands)
        
        if success: 
            goalcards = [h for h in self.hands if h.score >= self.fitnessgoal]
            goalcount = len(goalcards)
            print("Hands meeting fitness goal:", goalcount)
            for h in goalcards[:3]:
                print("    ", h.tostring())
        else:
            self.hands.sort(key=lambda x: x.score, reverse=True)
            
            print("Best hands")
            for i in range(0, 3):
                print("    ", self.hands[i].tostring())
        return success
    #end class
