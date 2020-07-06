import numpy as np
from copy import deepcopy
import heapq as hq

def bubble_up(h, ind):
    if ind == 0:
        return None
    root = int((ind-1)/2)
    if h[ind] < h[root]:
        temp = h[root]
        h[root] = h[ind]
        h[ind] = temp
        bubble_up(h, root)

class Ueue:
    def __init__(self, theta=0.001, maxLen = 4096):
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
            ind = len(self.h) - np.random.randint(1, int(self.maxLen/2))
            v = 0 - self.h[ ind ] # Not just last, to prevent "blocking" element
            if val < v:
                return -1
            self.remOne(v)
            self.h[ind] = - val
            bubble_up(self.h, ind)
        else:
            hq.heappush(self.h, 0 - val)

        try:
            self.dvk[val].append(key)
        except KeyError:
            self.dvk[val] = [key] 
                
    def isEmpty(self):
        return (len(self.h) == 0)



