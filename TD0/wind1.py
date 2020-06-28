import numpy as np


class Wind():
    """Env with wind"""

    def __init__(self, length = 10, height = 7):
        self.cells = np.zeros((height, length)) - 1
        self.wind = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
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
        return ['l', 'r', 'd', 'u']
                
    def move(self, state, action):
        """Give a state str(y0, x0), and an action, finds the next state and reward and returns."""
        if state == 'End':
            return 'End', 0
        x, y = self.state2coords(state)
        y = min(self.height -1, y + self.wind[x]) 
        if action == 'l':
            x = max(0, x-1)
        elif action == 'r':
            x = min(self.length -1, x + 1)
        elif action == 'u':
            y = min(self.height -1, y+1)
        elif action == 'd':
            y = max(0, y - 1)
        else:
            print("Error: action undefined.")
            return None, None
        t = self.coords2position(x, y)
        r = self.cells[t[0], t[1]]
        if x == 7  and y == 3:
            newstate = 'End'
        else:
            newstate = str((x, y))
        return newstate, r



