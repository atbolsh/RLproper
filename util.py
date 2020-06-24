from blackjack import *

def game(p1, p2, d=None):
    if type(d) == type(None):
        d = Deck()
    ## Initial conditions
    p1.reset()
    p2.reset()
    ## Dealing
    p1.hit(d)
    p2.hit(d)
    p1.hit(d)
    p2.hit(d)
    ## Looking at the one card
    p1.visible = p2.cards[0]
    p2.visible = p1.cards[0]
    ## each one gets hit until done.
    p1.move(d)
    p2.move(d)
    ## Evaluation
    v1, _ = vnu(p1.cards)
    v2, _ = vnu(p2.cards)
    ## Report results
    print(p1.cards)
    print(p2.cards)
    if v1 > v2:
        return 1, -1
    elif v2 > v1:
        return -1, 1
    else:
        return 0, 0


def practiceGame(p1, p2, d=None):
    if type(d) == type(None):
        d = Deck()
    p1.reset()
    p2.reset()
    # "Dealing"
    a = p1.exploringStart()
    p2.cards.append(p1.visible)
    p2.hit(d)
    ## each one gets hit until done.
    p1.move(d, a)
    p2.move(d)
    ## Evaluation
    v1, _ = vnu(p1.cards)
    v2, _ = vnu(p2.cards)
    ## Report results
    print(p1.cards)
    print(p2.cards)
    if v1 > v2:
        return 1, -1
    elif v2 > v1:
        return -1, 1
    else:
        return 0, 0  

def educate(n = 1000, p1 = None, infiniteDeck = True):
    if type(p1) == type(None):
        p1 = PHES()
    p2 = DH()
    if infiniteDeck:
        deck = InfiniDeck()
    else:
        deck = None #Fresh, exhaustible deck for each game
    for i in range(n):
        r1, r2 = practiceGame(p1, p2, deck)
        print((r1, r2))
        print(p1.trace)
        print('\n')
        p1.learn(r1)
    return p1


