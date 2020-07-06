import numpy as np
from initialDynaQ import Walled

class Maze(Walled):

    def __init__(self, length = 9, height = 6):
        Walled.__init__(self, length, height)
        self.initial_cell = (0, 3)
    
    def default_walls(self):
        self.cells[1:4, 2] = 1
        self.cells[4, 5] = 1
        self.cells[0:3, 7] = 1

