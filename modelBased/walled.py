import numpy as np


class Walled():
    """Walls are 1, everything else is 0. Goal and initial cell specially marked"""

    def __init__(self, length = 9, height = 6):
        self.cells = np.zeros((height, length))
        self.default_walls()

        self.goal_cell = (8, 5)
        self.initial_cell = (3, 0)
        self.typical_reward = -1
        self.goal_reward = 100
    
        self.height = height
        self.length = length
    
    def default_walls(self):
        for x in range(1, 9):
            self.cells[3, -x] = 1
    
    def initial(self):
        return str(self.initial_cell)
    
    def state2coords(self, state):
        s = eval(state)
        return s[0], s[1]
    
    def coords2position(self, x, y):
        """Translation between user-friendly coords 
        (left-right, lower-upper) into array position"""
        return (self.height - 1 - y, x)

    def actions(self, state):
        """Avaliable actions at state"""
        if state == 'End':
            return ['End']
        return ['l', 'r', 'd', 'u']
                
    def move(self, state, action):
        """Give a state str(y0, x0), and an action, finds the next state and reward and returns."""
        if state == 'End':
            return 'End', 0
        x, y = self.state2coords(state)
        t = self.coords2position(x, y)

        if action == 'l':
            newx = x - 1
            if newx < 0: #Ran off grid
                return str((x, y)), self.typical_reward
            t2 = self.coords2position(newx, y)
            if self.cells[t2[0], t2[1]] == 1: #Ran into wall
                return str((x, y)), self.typical_reward
            x = newx
            
        elif action == 'r':
            newx = x + 1

            if newx >= self.length: #Ran off grid
                return str((x, y)), self.typical_reward
            t2 = self.coords2position(newx, y)
            if self.cells[t2[0], t2[1]] == 1: #Ran into wall
                return str((x, y)), self.typical_reward
            x = newx

        elif action == 'u':
            newy= y + 1

            if newy >= self.height: #Ran off grid
                return str((x, y)), self.typical_reward
            t2 = self.coords2position(x, newy)
            if self.cells[t2[0], t2[1]] == 1: #Ran into wall
                return str((x, y)), self.typical_reward
            y = newy

        elif action == 'd':
            newy= y - 1

            if newy < 0: #Ran off grid
                return str((x, y)), self.typical_reward
            t2 = self.coords2position(x, newy)
            if self.cells[t2[0], t2[1]] == 1: #Ran into wall
                return str((x, y)), self.typical_reward
            y = newy

        else:
            print("Error: action undefined.")
            return None, None
        
        if x == self.goal_cell[0] and y == self.goal_cell[1]:
            return str(self.initial_cell), self.goal_reward
        else:
            return str((x, y)), self.typical_reward


