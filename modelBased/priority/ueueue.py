import numpy as np
from copy import deepcopy
import heapq as hq

class Ueue:
    def __init__(self, theta=0.001, maxLen = 5000):
        self.theta = theta
        self.h = [] #Ordered list of priorities
        self.dvk = {}
        self.maxLen = maxLen
    
    def remOne(self, v):
        keys = self.dvk[v]
        key = keys.pop()
        if len(keys) == 0:
            self.dvk.pop(v)
        return (key, v)
    
    def pop(self):
        if len(self.h) == 0:
            return ('', 0)
        
        v = 0 - hq.heappop(self.h)
        return self.remOne(v)
    
    def push(self, key, val):
        if val < self.theta:
            return -1

        if len(self.h) >= self.maxLen:
            v = 0 - self.h[ -np.random.randint(1, int(self.maxLen/2) - 1) ] # Not just last, to prevent "blocking" element
            if val < v:
                return -1
            v = 0 - self.h.pop() # NOT heappop; last, least important element
            self.remOne(v)

        try:
            self.dvk[val].append(key)
        except KeyError:
            self.dvk[val] = [key] 
            
        hq.heappush(self.h, 0 - val)
    
    def isEmpty(self):
        return (len(self.h) == 0)


