import numpy as np


class Cliff():
    """Env with cliff, page 131."""

    def __init__(self, length = 12, height = 4):
        self.cells = np.zeros((height, length)) - 1
        self.cells[height-1, 1:(length-1)] = -100
        self.height = height
        self.length = length
    
    def state2coords(self, state):
        s = eval(state)
        return s[0], s[1]
    
    def coords2position(self, x, y):
        """Translation between user-friendly coords 
        (left-right, lower-upper) into array position"""
        return (self.height - 1 - y, x)

    def actions(self, state):
        """Avaliable actions at state"""
        if state == 'End':
            return ['End']
        x, y = self.state2coords(state)
        a = []
        if x > 0:
            a.append('l')
        if x < self.length-1:
            a.append('r')
        if y > 0:
            a.append('d')
        if y < self.height -1:
            a.append('u')
        return a
                
    def move(self, state, action):
        """Give a state str(y0, x0), and an action, finds the next state and reward and returns."""
        if state == 'End':
            return 'End', 0
        x, y = self.state2coords(state)
        if action == 'l':
            x -= 1
        elif action == 'r':
            x += 1
        elif action == 'u':
            y += 1
        elif action == 'd':
            y -= 1
        else:
            print("Error: action undefined.")
            return None, None
        t = self.coords2position(x, y)
        r = self.cells[t[0], t[1]]
        if r == -100:
            x = 0
            y = 0
        if x == (self.length - 1)  and y == 0:
            newstate = 'End'
        else:
            newstate = str((x, y))
        return newstate, r



