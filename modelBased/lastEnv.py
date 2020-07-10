import numpy as np


# Random connections and rewards.
# No branching factor; use long runs with discount, or else runs of specific length.

# Two actions from each state.

class randomConnections:
    def __init__(self, n):
        self.n = n
        self.states = [str(i) for i in range(n)]
        self.afterStates = {}
        self.rewards = {}
        for i in range(n): #SLow, but fuck it. n log n ; ideally, should be n
            for action in ['l', 'r']:
                key = self.states[i] + action
                self.afterStates[ key ] = np.random.choice(self.states)
                self.rewards[ key ] = np.random.randn()
       
    def initial(self):
        return "0"
    
    def actions(self, state):
        return ['l', 'r']
   
    def move(self, state, action):
        """Give a state str(y0, x0), and an action, finds the next state and reward and returns."""
        key = state + action
        r = self.rewards[ key ]
        newState = self.afterStates[ key ]
        return newState, r

