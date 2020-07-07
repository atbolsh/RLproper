import numpy as np
from copy import deepcopy

## Files ueue and ueueue have two old implementations.
## ueue has no wasteful operations, but it is slower.
## 
## ueueue has wasteful updates (old priorities not discarded), but is much faster; set theta and maxLen correctly for it.
## 
## myMaxUpdates integrates the best of both worlds, with no duplication but also a proper, fast maxHeap. This is what we use now.
import myMaxHeap as mhp

class PriorityQPlus:
    
    def __init__(self, initial = str((0, 0)), gamma = 0.9, alpha = 0.9, eps=0.1, planSteps = 10, expSteps = None, theta = 0.0, kappa=0.1):
        self.initial = initial
        self.current = initial
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.planSteps = planSteps
        self.Q = {'EndEnd':0}
        self.actions = {'End':['End']}
        self.uniqueStates = ['End']
        self.SModel = {'EndEnd':'End'}
        self.RModel = {'EndEnd':0}
        self.seenFrom = {'End':set([])}
        self.priority = mhp.Queue(theta = theta)
        self.timestamp = 0
        self.traversed = {'EndEnd':0}
        self.kappa = kappa
        if type(expSteps) == type(None):
            self.expSteps = self.planSteps
  
    def reset(self):
        self.current = self.initial

    def traversedLookup(self, key):
        if key=='EndEnd':
            return 0
        try:
            t = self.traversed[key]
        except KeyError:
            t = self.timestamp
            self.traversed[key] = t
        return t
      
    def priorityLookup(self, key):
        try:
            p = self.priority.d[key]
        except KeyError:
            p = 0
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
            self.uniqueStates.append(state)
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
        self.actionLookup(state) # To intialize, esp. uniqueStates
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
       
    def selectState(self):
        return np.random.choice(self.uniqueStates) 
    
    def selectAction(self, state):
        return np.random.choice(self.actionLookup(state))
   
    def updateRandomPriority(self):
        s = self.selectState()
        a = self.selectAction(s)
        newState = self.SModelLookup(s, a)
        R = self.RModelLookup(s, a)
        newActions = self.actionLookup(newState)
        self.updatePriority(s, a, newState, R, newActions)
    
    def updatePriority(self, state, action, newState, reward, newActions, real=False):
        key = state + action
        if real:
            self.traversed[key] = self.timestamp
        tau = self.timestamp - self.traversedLookup(key)
        newMaxQ = max([self.Qlookup(newState, a) for a in newActions])
        currentQ = self.Qlookup(state, action)
        p = abs(reward + self.kappa*np.sqrt(tau) + self.gamma*newMaxQ - currentQ)
        self.priority.push(key, p)

    def SAfromKey(self, key):
        ## Hacky, but it really helps. Only configured right now for gridworlds; will change in other cases.
        if key[0] == 'E':
            return 'End', 'End'
        else:
            return key[:-1], key[-1]
   
    def updateTopQ(self):
        t = self.priority.pop()
        key = t[0]
        if not key:
            return None

        tau = self.timestamp - self.traversedLookup(key)

        state, action = self.SAfromKey(key) 
        newState = self.SModelLookup(state, action)
        reward = self.RModelLookup(state, action) + self.kappa*np.sqrt(tau)
        newActions = self.actionLookup(newState) # No env. interaction here.

        newMaxQ = max([self.Qlookup(newState, a) for a in newActions])
        key = state + action
        currentQ = self.Qlookup(state, action)
        p = reward + self.gamma*newMaxQ - currentQ
        self.Q[key] = currentQ + self.alpha*p
        
        allAs = self.actionLookup(state) 
        allQs = [self.Qlookup(state, a) for a in allAs]
        mq = max(allQs)
        for k in self.seenLookup(state):
            tauK = self.timestamp - self.traversed[k]
            s, a = self.SAfromKey(k)
            Rk = self.RModelLookup(s, a) + self.kappa*np.sqrt(tauK)
            Qk = self.Qlookup(s, a)
            Pk = abs(Rk + self.gamma*mq - Qk)
            self.priority.push(k, Pk)
    
    def move(self, env):
        self.timestamp += 1

        if np.random.random() < self.eps:
            a = self.exploringAction(env)
        else:
            a = self.greedyAction(env)
        
        newState, R = self.makeEnvMove(env, a) 
        newActions = self.getEnvActions(env, newState)

        self.updatePriority(self.current, a, newState, R, newActions, True)

        self.current = newState

        for i in range(self.expSteps):
            self.updateRandomPriority()

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
    
    def episode(self, env, cutoff = 5, reset=True):
        if reset:
            self.reset()
            self.current = env.initial()

        stateTrace = [self.current]
        actionTrace = []
        rewardTrace = []
        R = -1
        
        while R < cutoff:
            a, R = self.move(env)
            actionTrace.append(a)
            rewardTrace.append(R)
            stateTrace.append(self.current)
        
        return sum(rewardTrace), stateTrace, actionTrace, rewardTrace

