"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    length = len(line)
    merge_flag = range(length)
    for dummy_i in range(length):
        merge_flag[dummy_i] = False
    for dummy_i in range(length):
        if(line[dummy_i] == 0):
            continue
        if(merge_flag[dummy_i]):
            continue

        for dummy_j in range(dummy_i+1,length):
            if(line[dummy_j] == 0):
                continue
            if(line[dummy_j] != line[dummy_i]):
                break
            if(line[dummy_j] == line[dummy_i]):
                line[dummy_i] = line[dummy_i] * 2
                line[dummy_j] = 0
                for dummy_m in range(dummy_i,dummy_j):
                    merge_flag[dummy_m] = True
                break

    newline = []
    for dummy_i in range(length):
        if(line[dummy_i] != 0):
            newline.append(line[dummy_i])
 
    line = [0] * length
    index = 0
    for dummy_i in newline:
        line[index] = dummy_i
        index += 1

    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        #self.grid_values = [[0] * grid_width] * grid_height
        self.grid_values = [([0] * grid_width) for dummy_i in range(grid_height)]

        up_indice = range(grid_width)
        for dummy_i in range(grid_width):
            up_indice[dummy_i] = (0,dummy_i)
        
        down_indice = range(grid_width)
        for dummy_i in range(grid_width):
            down_indice[dummy_i] = (grid_height-1,dummy_i)

        left_indice = range(grid_height)
        for dummy_i in range(grid_height):
            left_indice[dummy_i] = (dummy_i,0)

        right_indice = range(grid_height)
        for dummy_i in range(grid_height):
            right_indice[dummy_i] = (dummy_i,grid_width-1)

        self.initial_indice_dict = {
                                    UP:up_indice,
                                    DOWN:down_indice,
                                    LEFT:left_indice,
                                    RIGHT:right_indice
                                    }
        print self.initial_indice_dict
        self.limit_dict = {
                            UP:grid_height,
                            DOWN:grid_height,
                            LEFT:grid_width,
                            RIGHT:grid_width
                            }

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid_values = [([0] * self.grid_width) for dummy_i in range(self.grid_height)]

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return "Test 2048"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        offset = OFFSETS[direction]
        limit = self.limit_dict[direction]
        indice = self.initial_indice_dict[direction]
        
        for dummy_pos in indice:
            
            dummy_line = range(limit)
            dummy_line[0] = self.get_tile(dummy_pos[0],dummy_pos[1])
            last_pos = [dummy_pos[0],dummy_pos[1]]
            for dummy_i in range(1,limit):
                dummy_line[dummy_i] = self.get_tile(last_pos[0] + offset[0],last_pos[1] + offset[1])
                last_pos = [last_pos[0] + offset[0],last_pos[1] + offset[1]]
                
            
            dummy_line = merge(dummy_line)
            
            self.set_tile(dummy_pos[0],dummy_pos[1],dummy_line[0])
            last_pos = [dummy_pos[0],dummy_pos[1]]
            for dummy_i in range(1,limit):
                self.set_tile(last_pos[0] + offset[0],last_pos[1] + offset[1],dummy_line[dummy_i]) 
                last_pos = [last_pos[0] + offset[0],last_pos[1] + offset[1]]
                
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        dummy_count = 0
        for dummy_i in range(self.grid_height):
            dummy_count += self.grid_values[dummy_i].count(0)
        if dummy_count == 0:
            return
        while(True):
            row = random.randint(0,self.grid_height-1)
            col = random.randint(0,self.grid_width-1)
            if(self.grid_values[row][col] == 0):
                dummy_r = random.random()
                print dummy_r
                if dummy_r < 0.9:
                    self.grid_values[row][col] = 2
                else:
                    self.grid_values[row][col] = 4
                break
        print self.grid_values
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid_values[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid_values[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 5))