import numpy as np

def vnu(cards):
    """Value and whether or not there is a usable ace."""
    s = 0
    aces = 0
    for card in cards:
        if card[0] == 'A':
            aces += 1
        else:
            s += int(card)
    acevals = [11 for ace in range(aces)]
    while (s + sum(acevals) > 21) and (11 in acevals):
        i = acevals.index(11)
        acevals[i] = 1
    s = s + sum(acevals)
    if s <= 21:
        return s, (11 in acevals)
    else:
        return -1, False


class Deck:
    """Standard 52 card deck, draws without replacement."""

    def __init__(self):
        self.reset()

    def reset(self):
        normals = [str(x) for x in range(2, 11)]
        faces = ['10' for x in range(3)]
        aces = ['A']
        
        self.cards = []
        for i in range(4):
            self.cards += normals
            self.cards += faces
            self.cards += aces
        
    def deal(self):
        n = len(self.cards)
        i = np.random.randint(0, n)
        return self.cards.pop(i)


class InfiniDeck(Deck):
    """Draws with replacement"""

    def deal(self):
        return np.random.choice(self.cards) 
    

class Player:
    """Abstract class that everyone inherits from."""
    def __init__(self):
        """By default, the first element will be visible."""
        self.reset()
    
    def reset(self):
        self.visible = None
        self.cards = []
    
    def hit(self, deck): 
        """Accepting card"""
        self.cards.append(deck.deal())

    def move(self, deck):
        return None

 
class DH(Player):
    """Dealer Hand; starts with 2 cards, then follows a strict guidlie"""   
    def move(self, deck):
        v, _ = vnu(self.cards)
        while (v > -1) and (v < 17):
            self.hit(deck)
            v, _ = vnu(self.cards)

    
class PHES(Player):
    """Player Hand, Exploring Starts"""
    def __init__(self):
        Player.__init__(self)
        self.hitQ = np.zeros((2, 10, 10))
        self.stickQ = np.zeros((2, 10, 10))
        self.hitN = np.zeros((2, 10, 10))
        self.stickN = np.zeros((2, 10, 10))
        self.startTable()

    def startTable(self):
        """Initially, jealously sticks"""
        for i in range(2):
            for j in range(10):
                for k in range(9):
                    self.hitQ[i, j, k] = 1
                    self.stickQ[i, j, k]= -1
                self.hitQ[i, j, 9] = -1
                self.stickQ[i, j, 9] = 1
        #self.hitN += 100
        #self.stickN += 100
    
    def reset(self):
        Player.reset(self)
        self.trace = []
 
    def decide(self):
        """'h' = hit, 's' = stick"""
        i, j, k = self.inds()
        ## Bust (-2) or obvious hit (-1)
        if i < 0:
            if i == -2:
                return 's'
            else:
                return 'h'
        hq = self.hitQ[i, j, k]
        sq = self.stickQ[i, j, k]
        if hq > sq:
            a = 'h'
        else:
            a = 's'
        self.trace.append(((i, j, k), a))
        return a

    def inds(self):
        v, u = vnu(self.cards)
        ## Bust (-2) or obvious hit (-1)
        if v < 0:
            return -2, -2, -2
        if v < 12:
            return -1, -1, -1
        ## i, usable ace
        i = int(u)
        ## j, visible card
        if self.visible[0] == 'A':
            j = 0
        else:
            j = int(self.visible) - 1
        ## k, score so far.
        k = v - 12
        return i, j, k

    def exploringStart(self):
        i = np.random.randint(0, 2)
        j = np.random.randint(0, 10)
        k = np.random.randint(0, 10)
        a = np.random.choice(['s', 'h'])
        if j == 0:
            self.visible = 'A'
        else:
            self.visible = str(j + 1)
        if i == 0:
            self.cards = [str(k + 12)]
        else:
            self.cards = [str(k + 1), 'A']
        self.trace.append(((i, j, k), a))
        return a

    def move(self, deck, a = 'b'):
        """Move is optional; allows one to seed a first action."""
        while a != 's':
            if a == 'h':
                self.hit(deck)
            a = self.decide()
       
    def learn(self, reward):
        """Use of self.trace in order to change Q-values."""
        for x in self.trace:
            a = x[1]
            i, j, k = x[0][0], x[0][1], x[0][2]
            if a == 'h':
                Q = self.hitQ
                N = self.hitN
            else:
                Q = self.stickQ
                N = self.stickN
            Q[i, j, k] = (Q[i, j, k]*N[i, j, k] + reward)/(N[i, j, k] + 1)
            N[i, j, k] += 1



