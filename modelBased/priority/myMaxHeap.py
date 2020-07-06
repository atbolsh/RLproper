import numpy as np
from copy import deepcopy

## Proper implementation of maxHeap for our purposes (heap with reassignment). 
##
## If push comes to shove, use reasonable theta (eg 0.01) and implement the maxLen idea from ueueue

class Queue:
    def __init__(self, theta=0.001):
        self.theta = theta
        self.h = [] # Heap of key-vals
        self.dkv = {}
        self.inds = {}
    
    def switch(self, i, j):
        t = self.h[i]
        u = self.h[j]
        ## Put in correct inds at the keys
        self.inds[t[0]] = j
        self.inds[u[0]] = i
        ## Put in correct elements of heap
        self.h[i] = u
        self.h[j] = t

    def bubble_up(self, ind):
        if ind == 0:
            return None
        root = int((ind - 1)/2)
        if self.h[root][1] < self.h[ind][1]:
            self.switch(root, ind)
            return self.bubble_up(root)
    
    def bubble_down(self, ind):
        v = self.h[ind][1]

        leftChild = ind*2 + 1
        rightChild = ind*2 + 2

        if leftChild < len(self.h):
            vl = self.h[leftChild][1]
        else:
            vl = float('-inf')

        if rightChild < len(self.h):
            vr = self.h[rightChild][1]
        else:
            vr = float('-inf')

        if (v >= vl) and (v >= vr):
            return None
        elif (vr >= v) and (vr >= vl):
            self.switch(ind, rightChild)
            return self.bubble_down(rightChild)
        else: # vl >= v and vl >= vr:
            self.switch(ind, leftChild)
            return self.bubble_down(leftChild)
    
    def rightmost_child(self, ind):
        j = ind*2 + 2
        if j == len(self.h): ## Just off
            return ind*2 + 1  # Get left child
        elif j > len(self.h):
            return ind
        else:
            return self.rightmost_child(j)

    def leftmost_child(self, ind):
        j = ind*2 + 1
        if j >= len(self.h):
            return ind
        else:
            return self.leftmost_child(j)
    
    def mintrace_child(self, ind):
        j = ind*2 + 1
        k = ind*2 + 2
        if j >= len(self.h): # Reached end
            return ind 
        elif k >= len(self.h): # j == len(self.h) - 1
            return ind
        else:
            if self.h[j][1] <= self.h[k][1]:
                return self.mintrace_child(j)
            else:
                return self.mintrace_child(k)
 
    def pop(self):
        try:
            res = self.h[0]
        except IndexError: # Empty heap
            res = ('', float('-inf'))
        
        try:
            self.h[0] = self.h.pop() #Take off last element and put it at top
            self.inds[self.h[0][0]] = 0 # Assign correct index before bubble-down
            self.bubble_down(0)
        except IndexError: #Only one element in list
            self.h = []

        try:
            self.inds.pop(res[0]) # No more fake root
            self.dkv.pop(res[0])
        except KeyError:
            a = 2 + 2 # Nothing
        return res
    
    def normal_push(self, key, val):
        self.h.append((key, val))
        self.dkv[key] = val
        self.inds[key] = len(self.h) -1
        self.bubble_up(len(self.h) - 1)
    
    def reassign(self, key, val):
        if self.dkv[key] >= val: # Will throw KeyError if not in dict
            return None
        t = (key, val) # New tuple
        ind = self.inds[key]

        c = self.rightmost_child(ind) # Could be others; think!
        self.switch(ind, c)
        self.h[c] = ('', float('-inf')) # Put in dummy val for now
        self.bubble_down(ind)

        self.inds[key] = c # Just to be sure, reassigning this.
        self.h[c] = t # Put in the new tuple
        self.bubble_up(c) # Put it in the correct place
        
        self.dkv[key] = val

    def push(self, key, val):
        if val < self.theta:
            return None
        try:
            self.reassign(key, val)
        except KeyError:
            self.normal_push(key, val)
    
    


 
