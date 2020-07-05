import numpy as np
from copy import deepcopy

class DynaQ:
    
    def __init__(self, initial = str((0, 0)), gamma = 0.9, alpha = 0.5, eps=0.0, planSteps = 50):
        self.initial = initial
        self.current = initial
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.planSteps = planSteps
        self.Q = {'EndEnd':0}
        self.actions = {'End':['End']}
        self.SModel = {'EndEnd':'End'}
        self.RModel = {'EndEnd':0}
   
    def reset(self):
        self.current = self.initial
    
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
            a = ['dummy']
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
        return newState, R        
    
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
        actions = self.getEnvActions(env)
        v = [self.Qlookup(self.current, action) for action in actions]
        inds = self.inclusiveArgMax(v)
        ind = np.random.choice(inds)
        return actions[ind]

    def exploringAction(self, env):
        actions = self.getEnvActions(env)
        return np.random.choice(actions)
    
    def updateQ(self, state, action, newState, reward, newActions):
        newMaxQ = max([self.Qlookup(newState, a) for a in newActions])
        key = state + action
        currentQ = self.Qlookup(state, action)
        self.Q[key] = currentQ + self.alpha*(reward + self.gamma*newMaxQ - currentQ)
    
    def selectState(self):
        return np.random.choice(self.actions.keys())
    
    def selectAction(self, state):
        return np.random.choice(self.actionLookup(state))
    
    def bgPlan(self):
        state = self.selectState() # Opens the door to smarter selection in the future
        action = self.selectAction(state)
        newState = self.SModelLookup(state, action)
        R = self.RModelLookup(state, action)
        newActions = self.actionLookup(newState) # No env. interaction here.
        self.updateQ(state, action, newState, R, newActions)
    
    def move(self, env):
        if np.random.random() < self.eps:
            a = self.exploringAction(env)
        else:
            a = self.greedyAction(env)
        
        newState, R = self.makeEnvMove(env, a) 
        newActions = self.getEnvActions(env, newState)

        self.updateQ(self.current, a, newState, R, newActions)

        self.current = newState

        for i in range(self.planSteps):
            self.bgPlan()       
       
        return a, R

    def run(self, env, steps=1000, reset=True):
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





 
