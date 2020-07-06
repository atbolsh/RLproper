import numpy as np
from copy import deepcopy

## Bad, slow implementation; use myMaxHeap instead

class Ueue:
    def __init__(self, theta=0.0001, maxLen = 5000):
        self.theta = theta
        self.l = [] #Ordered list of stuff.
        self.d = {}
    
    def binarySearch(self, priority, bot = 0, top = None):
        if type(top) == type(None):
            top = len(self.l)
        i = bot + int((top - bot)/2)
        try:
            v = self.l[i][1]
        except IndexError:
            return -1 #Before everything

        if priority == v:
            return i
        elif i == bot:
            if priority < v:
                return i -1
            else:
                return i
        elif priority > v:
            return self.binarySearch(priority, i, top)
        elif priority < v:
            return self.binarySearch(priority, bot, i)
        else:
            return -12 #Error.
    
    def findInd(self, key):
        try:
            v = self.d[key]
        except KeyError:
            return -12 #Not specified

        i = self.binarySearch(v)
        if i == -1:
            return -12 #Not specified
        if self.l[i][1] != v:
            return -12

        j = i
        while j < len(self.l) and self.l[j][1] == v:
            if self.l[j][0] == key:
                return j
            j += 1

        j = i
        while j > -1 and self.l[j][1] == v:
            if self.l[j][0] == key:
                return j
            j -= 1

        return -12 #Keys never matched
       
    def rem(self, key):
        i = self.findInd(key)
        if i == -12: #No match
            return None
        self.l.pop(i)
        try:
            return self.d.pop(key)
        except KeyError:
            return None
    
    def push(self, key, val):
        if val < self.theta:
            return -1

        self.rem(key)
        
        ind = self.binarySearch(val) + 1
        self.l.insert(ind, (key, val))
        
        self.d[key] = val
        return ind

    def pop(self):
        try:
            t = self.l.pop()
        except IndexError:
            return ('', 0)
        self.d.pop(t[0])
        return t
    
    def isEmpty(self):
        return (len(self.l) == 0)
        
 
