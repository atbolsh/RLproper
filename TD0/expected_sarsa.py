import numpy as np

class eSARSA:
    
    def __init__(self, initial = str((0, 0)), gamma = 1.0, alpha = 0.5, eps=0.1):
        self.initial = initial
        self.reset()
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {'EndEnd':0}
    
    def reset(self):
        self.current = self.initial
        self.nextAction = None
    
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
        return np.random.choice(actions)
    
    def action(self, env, state=None):
        if type(state) == type(None):
            state = self.current

        if np.random.random() < self.eps:
            a = self.exploringAction(env, state)
        else:
            a = self.greedyAction(env, state)
        return a
    
    def expectation(self, env, state=None):
        if type(state) == type(None):
            state = self.current
        actions = env.actions(state)
        v = [self.lookup(state, action) for action in actions]
        re = self.eps*sum(v)/len(v)
        rg = (1 - self.eps)*max(v)
        return re + rg
   
    def move(self, env):
        
        if type(self.nextAction) == type(None):
            self.nextAction = self.action(env)
        a = self.nextAction
        
        newState, R = env.move(self.current, a) 

        self.nextAction = self.action(env, newState)
        newQ = self.expectation(env, newState)
        
        key = self.current + a
        self.Q[key] = self.Q[key] + self.alpha*(R + (self.gamma*newQ) - self.Q[key])
        
        self.current = newState
       
        return a, R

    def episode(self, env):
        self.reset()

        stateTrace = [self.current]
        actionTrace = []
        rewardTrace = []
        
        while self.current != "End":
            a, R = self.move(env)
            actionTrace.append(a)
            rewardTrace.append(R)
            stateTrace.append(self.current)
        
        return sum(rewardTrace), stateTrace, actionTrace, rewardTrace





 
