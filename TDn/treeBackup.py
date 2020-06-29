import numpy as np

class TreeBackup:
    
    def __init__(self, n = 10, initial = str((0, 0)), gamma = 1.0, alpha = 0.5, eps=0.1):
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
        return np.random.choice(actions)
    
    def action(self, env, state=None):
        if type(state) == type(None):
            state = self.current

        if np.random.random() < self.eps:
            a = self.exploringAction(env, state)
        else:
            a = self.greedyAction(env, state)
        return a
    
    def getProbs(self, vals):
        probs = np.zeros(len(vals)) + (self.eps/len(vals))
        inds = self.inclusiveArgMax(vals)
        for i in inds:
            probs[i] += (1 - self.eps)/len(inds)
        return probs
    
    def getG(self, tau, env):
        ## Access to the environment isn't necessary; a trace of possible actions can be stored.
        actions = env.actions(self.current)
        v = [self.lookup(self.current, action) for action in actions]
        probs = self.getProbs(v)

        G = 0
        for i in range(len(v)):
            G += self.gamma*probs[i]*v[i]
        G += self.rTrace[-1]

        for i in range(len(self.rTrace) -1, tau, -1):
            s = self.sTrace[i]
            a = self.aTrace[i]
            r = self.rTrace[i-1] #state and actions are future; reward is present

            actions = env.actions(s)
            v = [self.lookup(s, action) for action in actions]
            probs = self.getProbs(v)
            
            tally = 0
            for j in range(len(probs)):
                if actions[j] == a:
                    tally += probs[j]*G
                else:
                    tally += probs[j]*self.lookup(s, actions[j])
           
            G = r + self.gamma*tally
        return G
    
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
    
    def update(self, tau, env):
        if tau < 0:
            return None
        G = self.getG(tau, env)

        key = self.sTrace[tau] + self.aTrace[tau]
        self.Q[key] = self.Q[key] + self.alpha*(G - self.Q[key])

    def episode(self, env):
        self.reset()
       
        tau = 0 - self.n
        while ((self.current != "End") or (tau < len(self.sTrace))):
            if self.current != "End":
                a, R = self.move(env)
            if tau >= 0:
                self.update(tau, env)
            tau += 1
        
        return sum(self.rTrace), self.sTrace, self.aTrace, self.rTrace





 
