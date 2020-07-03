import numpy as np
from copy import deepcopy

class dynaQ:
    
    def __init__(self, initial = str((0, 0)), gamma = 1.0, alpha = 0.5, eps=0.1, planSteps = 0):
        self.initial = initial
        self.current = initial
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.planSteps = planSteps
        self.Q = {'EndEnd':0}
        self.actions = {'End':['End']}
        self.Smodel = {'EndEnd':'End'}
        self.Rmodel = {'EndEnd':0}
   
    def reset(self):
        self.current = self.initial
    
    def Qlookup(self, state, action):
        if state == 'End':
            return 0
        key = state + action
        if key not in self.Q.keys():
            self.Q[key] = 0
        return self.Q[key]
    
    def actionLookup(self, state):
        if state == 'End':
            return ['End']
        if state not in self.actions.keys():
            self.actions[state] = ['dummy']
        return self.actions[state]
    
    def SmodelLookup(self, state, action):
        if state == 'End':
            return 'End'
        key = state + action
        if key not in self.Smodel.keys():
            Smodel[key] = state #Initialized as self-return
        return Smodel[key]
    
    def getEnvActions(self, env, state=None):
        if type(state) == type(None):
            state = self.current
        actions = env.actions(state)
        self.actions[state] = deepcopy(actions)
        inSModel = self.Smodel.keys()
        inRModel = self.Rmodel.keys()
        inQ = self.Q.keys()
        for a in actions:
            key = state + a
            if key not in inSModel: 
                self.Smodel[key] = state #Initialized as return to original.
            if key not in inQ:
                self.Q[key] = 0 #Initialized at 0.
            if key not in inRModel:
                self.RModel[key] = 0 #Initialized at 0.
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
        
        newState, R = self.makeEnvMove(a) 
        newActions = self.getEnvActions(env, newState)

        self.updateQ(self.current, a, newState, R, newActions)

        self.current = newState

        for i in range(self.planSteps):
            self.bgPlan()       
       
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





 
