import numpy as np

class GeneralMC:
    
    def __init__(self, n = 10, initial = str((0, 0)), gamma = 1.0, alpha = 0.1, eps=0.1):
        self.initial = initial
        self.n = n
        self.reset()
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {'EndEnd':0}
    
    def reset(self):
        self.current = self.initial
        self.nextAction = None
        self.sTrace = []
        self.aTrace = []
        self.rTrace = []
    
    def lookup(self, state, action):
        if state == 'End':
            return 0
        key = state + action
        if key not in self.Q.keys():
            self.Q[key] = 0
        return self.Q[key]
    
    def inclusiveArgMax(self, l):
        M = -1000000
        inds = []
        for i in range(len(l)):
            v = l[i]
            if v > M:
                M = v
                inds = [i]
            elif v == M:
                inds.append(i)
        return inds
    
    def greedyAction(self, env, state=None):
        if type(state) == type(None):
            state = self.current
        actions = env.actions(state)
        v = [self.lookup(state, action) for action in actions]
        inds = self.inclusiveArgMax(v)
        ind = np.random.choice(inds)
        return actions[ind]

    def exploringAction(self, env, state=None):
        if type(state) == type(None):
            state = self.current
        actions = env.actions(state)
        v = [self.lookup(state, action) for action in actions]
        return np.random.choice(actions)
    
    def action(self, env, state=None):
        if type(state) == type(None):
            state = self.current

        if np.random.random() < self.eps:
            a = self.exploringAction(env, state)
        else:
            a = self.greedyAction(env, state)
        return a
       
    def move(self, env):
        if type(self.nextAction) == type(None):
            self.nextAction = self.action(env)
        a = self.nextAction
         
        newState, R = env.move(self.current, a) 
        self.nextAction = self.action(env, newState)

        self.sTrace.append(self.current)
        self.aTrace.append(a)
        self.rTrace.append(R)
        
        self.current = newState
      
        return a, R
    
    def update(self):
        G = 0
        for i in range(1, len(self.rTrace) + 1):
            G = self.gamma*G + self.rTrace[-i]
            
            key = self.sTrace[-i] + self.aTrace[-i]
            self.Q[key] = self.Q[key] + self.alpha*(G - self.Q[key])

    def episode(self, env, train=True):
        self.reset()
       
        while (self.current != "End"):
            self.move(env)

        if train:
            self.update()
               
        return sum(self.rTrace), self.sTrace, self.aTrace, self.rTrace





 
