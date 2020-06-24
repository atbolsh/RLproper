from blackjack import *

def game(p1, p2):
    d = Deck()
    p1.reset()
    p2.reset()
    p1.hit(d)
    p2.hit(d)
    p1.hit(d)
    p2.hit(d)
    p1.visible = p2.cards[0]
    p2.visible = p1.cards[0]
    p1.move(d)
    p2.move(d)
    v1, _ = vnu(p1.cards)
    v2, _ = vnu(p2.cards)
    print(p1.cards)
    print(p2.cards)
    if v1 > v2:
        return 1, -1
    elif v2 > v1:
        return -1, 1
    else:
        return 0, 0

def educate(p1 = None, n = 1000):
    if type(p1) == type(None):
        p1 = PHES()
    p2 = DH()
    for i in range(n):
        r1, r2 = game(p1, p2)
        print((r1, r2))
        print(p1.trace)
        print('\n')
        p1.learn(r1)
    return p1
