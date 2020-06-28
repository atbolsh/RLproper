import numpy as np


class mini():
    """Maximization Bias example, pg 135"""

    def __init__(self, length = 12, height = 4):
        self.states = ['A', 'B', 'End']
   
    def actions(self, state):
        """Avaliable actions at state"""
        if state == 'End':
            return ['End']
        if state == 'A':
            return ['l', 'r']
        if state == 'B':
            return ['l' + str(i) for i in range(10)]
               
    def move(self, state, action):
        """Give a state str(y0, x0), and an action, finds the next state and reward and returns."""
        if state == 'End':
            return 'End', 0
        if state == 'A':
            r = 0
            if action == 'r':
                newstate = 'End'
            else:
                newstate = 'B'
        if state == 'B':
            newstate = 'End'
            r = np.random.randn() - 0.1
        return newstate, r


