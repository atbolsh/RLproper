import numpy as np

class QL:
    
    def __init__(self, initial = str((0, 0)), gamma = 1.0, alpha = 0.5, eps=0.1):
        self.initial = initial
        self.current = initial
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.Q1 = {'EndEnd':0}
        self.Q2 = {'EndEnd':0}
        self.Q = self.Q1
        self.nQ = self.Q2
    
    def switchQs(self):
        temp = self.Q
        self.Q = self.nQ
        self.Q = temp
   
    def reset(self):
        self.current = self.initial
    
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
    
    def greedyAction(self, env):
        actions = env.actions(self.current)
        v = [self.lookup(self.current, action) for action in actions]
        inds = self.inclusiveArgMax(v)
        ind = np.random.choice(inds)
        return actions[ind]

    def exploringAction(self, env):
        actions = env.actions(self.current)
        return np.random.choice(actions)
    
    def move(self, env):
        if np.random.random() < self.eps:
            a = self.exploringAction(env)
        else:
            a = self.greedyAction(env)
        
        newState, R = env.move(self.current, a) 

        newActions = env.actions(newState)
        ind = np.argmax(np.array([self.lookup(newState, action) for action in newActions]))
        action = newAction[ind]
        self.switchQs()
        newMaxQ = self.lookup(newState, action)
        
        key = self.current + a
        self.Q[key] = self.Q[key] + self.alpha*(R + (self.gamma*newMaxQ) - self.Q[key])
        
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





 
