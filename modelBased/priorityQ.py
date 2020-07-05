import numpy as np
from copy import deepcopy

### FIXED ME!! Should work with Walled, just like DQPlus

class PriorityQ:
    
    def __init__(self, initial = str((0, 0)), gamma = 0.9, alpha = 0.5, eps=0.1, planSteps = 50, kappa=0.05):
        self.initial = initial
        self.current = initial
        self.eps = eps
        self.kappa = kappa
        self.alpha = alpha
        self.gamma = gamma
        self.planSteps = planSteps
        self.Q = {'EndEnd':0}
        self.traversed = {'EndEnd':0}
        self.actions = {'End':['End']}
        self.SModel = {'EndEnd':'End'}
        self.RModel = {'EndEnd':0}
        self.seenFrom = {'End':set([])}
        self.priority = {'EndEnd':0}
   
    def reset(self):
        self.current = self.initial
    
    def topPriority(self):
        M = -1
        s = 'EndEnd'
        l = self.priority.items()
        for t in l:
            if t[1] > M:
                s = t[0]
                M = t[1]
        return s
    
    def priorityLookup(self, key):
        try:
            p = self.priority[key]
        except KeyError:
            p = 0
            self.priority[key] = p
        return p 
    
    def seenLookup(self, state):
        try:
            l = self.seenFrom[state]
        except KeyError:
            l = set([])
            self.seenFrom[state] = l
        return l

    def seenMod(self, state, prior):
        try:
            self.seenFrom[state].add(prior)
        except KeyError:
            l = set([prior])
            self.seenFrom[state] = l
    
    def traversedLookup(self, key):
        if key=='EndEnd':
            return 0
        try:
            tau = self.traversed[key]
        except KeyError:
            tau = 0
            self.traversed[key] = tau
        return tau
    
    def Qlookup(self, state, action):
        if state == 'End':
            return 0
        key = state + action
        try:
            q = self.Q[key]
        except KeyError:
            q = 0
            self.Q[key] = q
        return q
   
    def actionLookup(self, state):
        if state == 'End':
            return ['End']
        try:
            a = self.actions[state]
        except KeyError:
            a = ['z'] # Dummy value
            self.actions[state] = a
        return a
    
    def SModelLookup(self, state, action):
        if state == 'End':
            return 'End'
        key = state + action
        try:
            s = self.SModel[key]
        except KeyError:
            s = state
            self.SModel[key] = state
        return s

    def RModelLookup(self, state, action):
        if state == 'End':
            return 0
        key = state + action
        try:
            r = self.RModel[key]
        except KeyError:
            r = 0
            self.RModel[key] = r
        return r
   
    def getEnvActions(self, env, state=None):
        if type(state) == type(None):
            state = self.current
        actions = env.actions(state)
        self.actions[state] = deepcopy(actions)
        for a in actions: #Initialize values with defualts with a lookup.
            self.RModelLookup(state, a)
            self.SModelLookup(state, a)
            self.Qlookup(state, a) 
        return actions
    
    def makeEnvMove(self, env, action, state=None):
        if type(state) == type(None):
            state = self.current
        newState, R = env.move(state, action)
        key = state + action
        self.SModel[key] = newState
        self.RModel[key] = R
        self.seenMod(newState, key)
        return newState, R        
    
    def inclusiveArgMax(self, l):
        M = float('-inf')
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
        actions = self.getEnvActions(env)
        v = [self.Qlookup(self.current, action) for action in actions]
        inds = self.inclusiveArgMax(v)
        ind = np.random.choice(inds)
        return actions[ind]

    def exploringAction(self, env):
        actions = self.getEnvActions(env)
        return np.random.choice(actions)
    
    def updatePriority(self, state, action, newState, reward, newActions, real=False):
        newMaxQ = max([self.Qlookup(newState, a) for a in newActions])
        key = state + action
        currentQ = self.Qlookup(state, action)
        p = reward + self.gamma*newMaxQ - currentQ
        self.priority[key] = abs(p)
#        self.Q[key] = currentQ + self.alpha*p
        if real:
            self.traversedLookup(key)
            self.traversed[key] = 0
            for k in self.traversed.keys():
                if k != key:
                    tau = self.traversed[k]
                    self.priority[k] = self.priorityLookup(k) + self.kappa*(np.sqrt(tau + 1) - np.sqrt(tau))
                    self.traversed[k] += 1
      
    def selectState(self):
        return np.random.choice(self.actions.keys())
    
    def selectAction(self, state):
        return np.random.choice(self.actionLookup(state))

    def SAfromKey(self, key):
        ## Hacky, but it really helps. Only configured right now for gridworlds; will change in other cases.
        if key[0] == 'E':
            return 'End', 'End'
        else:
            return key[:-1], key[-1]
   
    def updateTopQ(self):
        key = self.topPriority()

        state, action = self.SAfromKey(key) 
        newState = self.SModelLookup(state, action)
        R = self.RModelLookup(state, action)
        tau = self.traversedLookup(state + action)
        newActions = self.actionLookup(newState) # No env. interaction here.
        reward = R + self.kappa*np.sqrt(tau)

        newMaxQ = max([self.Qlookup(newState, a) for a in newActions])
        key = state + action
        currentQ = self.Qlookup(state, action)
        p = reward + self.gamma*newMaxQ - currentQ
        self.Q[key] = currentQ + self.alpha*p
        
        self.priority[key] = 0
       
        allAs = self.actionLookup(state) 
        allQs = [self.Qlookup(state, a) for a in allAs]
        mq = max(allQs)
        for k in self.seenLookup(state):
            s, a = self.SAfromKey(k)
            tauK = self.traversedLookup(s + a)
            Rk = self.RModelLookup(s, a) + self.kappa*np.sqrt(tau)
            Qk = self.Qlookup(s, a)
            Pk = abs(Rk + self.gamma*mq - Qk)
            self.priority[k] = Pk
    
    def move(self, env):
        if np.random.random() < self.eps:
            a = self.exploringAction(env)
        else:
            a = self.greedyAction(env)
        
        newState, R = self.makeEnvMove(env, a) 
        newActions = self.getEnvActions(env, newState)

        self.updatePriority(self.current, a, newState, R, newActions, True)

        self.current = newState

        for i in range(self.planSteps):
            self.updateTopQ()       
       
        return a, R

    def run(self, env, steps=3000, reset=True):
        if reset:
            self.reset()
            self.current = env.initial()

        stateTrace = [self.current]
        actionTrace = []
        rewardTrace = []
        
        for i in range(steps):
            a, R = self.move(env)
            actionTrace.append(a)
            rewardTrace.append(R)
            stateTrace.append(self.current)
        
        return sum(rewardTrace), stateTrace, actionTrace, rewardTrace

 
