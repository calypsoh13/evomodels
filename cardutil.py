''' 
Utility fields and methods for card models
''' 
suits = ["C", "D", "H", "S"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def toSuit(card):
    return card // 13

def toValue(card):
    return card % 13

    
def cardstostring(cards, numbercards, score = None):
    result = ""
    delim = " "
    upcards = sorted(cards[:numbercards])
    for card in upcards:
        result = result + delim
        delim = ", "
        result = result + values[toValue(card)]
        result = result + suits[toSuit(card)]
    
    if (not score is None):
        result = result + ", " + str(score)
    return result

        
def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data, c):
    """Return sum of square deviations of sequence data."""
    #c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data, c):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data, c)
    pvar = ss/n # the population variance
    return pvar**0.5
    
def printdic(dic):
    keys = [k for k in dic]
    keys.sort()
    for k in keys:
        print(k, " : ", dic[k]) 
        
       
# end class
