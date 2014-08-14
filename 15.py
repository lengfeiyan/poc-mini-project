"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
#        print self
#        print move_string
#        print "-------------------------"
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        flag1 = self._grid[target_row][target_col] == 0
        flag2 = True
        if target_row < (self.get_height() - 1):
            flag2 = self._grid[target_row + 1] == sorted(self._grid[target_row + 1]) and self._grid[target_row + 1][0] == (target_row + 1) * self.get_width()
        flag3 = True
        if target_col < (self.get_width() - 1):
            flag3 = self._grid[target_row][target_col+1:] == sorted(self._grid[target_row][target_col+1:]) and self._grid[target_row][target_col+1] == (target_row * self.get_width() + target_col + 1) 
        return flag1 and flag2 and flag3

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(target_row,target_col)
        move_string = ""
        target_pos = self.current_position(target_row,target_col)

        move_string_temp = self.swap_zero_target_tile(target_pos)
        if move_string_temp == "l":
            return move_string_temp
        else:
            move_string += move_string_temp
        #move zero to current target_pos and then move to left of its init position
        iter_times = 0
        while (target_row, target_col) != target_pos:
            iter_times += 1
            if iter_times == 10:
                break
            target_pos = self.current_position(target_row,target_col)
            move_string += self.position_tile(target_pos,target_row, target_col)
        
        zero_row,zero_col = self.current_position(0,0)
        move_string_temp = "l" * zero_col
        move_string_temp += "d" * (target_row - zero_row)
        zero_row = target_row
        move_string_temp += "r" * (target_col - 1)
        zero_col = target_col - 1
        move_string_temp += "u" * (zero_row - target_row)
        target_row = target_row
        self.update_puzzle(move_string_temp)
        move_string += move_string_temp
        return move_string
    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row,0)
        move_string = "ur"
        self.update_puzzle(move_string)
        
        if self._grid[target_row][0] != target_row * self.get_width() :
            target_pos = self.current_position(target_row,0)
            move_string += self.swap_zero_target_tile(target_pos)
            iter_times = 0
            while self._grid[target_row-1][1] != target_row * self.get_width() or self._grid[target_row-1][0] != 0:
                iter_times += 1
                if iter_times == 10:
                    break
                target_pos = self.current_position(target_row,0)
                move_string += self.position_tile(target_pos,target_row - 1, 1)
                if self._grid[target_row-1][1] == target_row * self.get_width() and self._grid[target_row-1][0] != 0:
                     zero_row,zero_col = self.current_position(0,0)
                     if zero_col == 1 and zero_row == target_row-2:
                         move_string += "ld"
                         self.update_puzzle("ld")
                     elif zero_col == 2 and zero_row == target_row-1:
                         move_string += "ulld"
                         self.update_puzzle("ulld")
                     break
            move_string += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
            
            zero_row,zero_col = self.current_position(0,0)
            move_string_temp = ""
            if zero_row != target_row - 1:
                move_string_temp += "d" * (target_row - 1 - zero_row)
            move_string_temp += "r" * (self.get_width()-1-zero_col)
            move_string += move_string_temp
            self.update_puzzle(move_string_temp)
        else:
            move_string_temp = "r" * (self.get_width()-2)
            self.update_puzzle(move_string_temp)
            move_string += move_string_temp
        return move_string

    def position_tile(self,target_pos,target_row,target_col):
        """
            position_tile
        """
        zero_row,zero_col = self.current_position(0,0)
        move_string = ""
        if target_pos[0] == target_row and target_pos[1] < target_col:
            if zero_row == target_pos[0] and zero_col < target_pos[1]:
                move_string += "urrdl"
            elif zero_row == target_pos[0] and zero_col > target_pos[1]:
                move_string = "l"
            else:
                move_string = "rdl"
        elif target_pos[0] < target_row and target_pos[1] <= target_col:
            move_string += self._position_tile_helper(target_pos,target_row,target_col)
        elif target_pos[0] < target_row and target_pos[1] > target_col:
            if zero_row == target_pos[0] and zero_col < target_pos[1]:#left
                move_string += "r"
            elif zero_row == target_pos[0] and zero_col > target_pos[1]:#right
                if target_pos[1] == target_col - 1:
                    move_string += "ulldr"
                else:
                    move_string += "dllur"
            elif zero_row < target_pos[0] and zero_col == target_pos[1]:#top
                move_string += "ldr"
        self.update_puzzle(move_string)
        
        return move_string
        
    def _position_tile_helper(self,target_pos,target_row,target_col):
        """
        position_tile_helper
        """
        zero_row,zero_col = self.current_position(0,0)
        move_string = ""
        if zero_row == target_pos[0] and zero_col < target_pos[1]:#left
             move_string += "dru"
        elif zero_row == target_pos[0] and zero_col > target_pos[1]:#right
            if zero_row > 0:
                move_string += "ullddru"
            else:
                move_string += "dlu"
        elif zero_row < target_pos[0] and zero_col == target_pos[1]:#top
            if target_pos[1] == 0 and target_col == 1:
                move_string += "rdl"
            else:
                move_string += "lddru"
        else:#bottom
            move_string += "u"
        return move_string
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        for dummy_i in range(target_col+1,self.get_width()):
            if self._grid[0][dummy_i] != dummy_i:
                return False
        if self._grid[1][target_col] != self.get_width() + target_col:
            return False
        arr = []
        arr.extend(self._grid[1][target_col:])
        for dummy_row in range(2,self.get_height()):
            arr.extend(self._grid[dummy_row])
        if arr == sorted(arr):
            return True
        else:
            return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        if self._grid[1][target_col+1] != self.get_width() + target_col+1:
            return False
        arr = []
        arr.extend(self._grid[1][target_col+1:])
        for dummy_row in range(2,self.get_height()):
            arr.extend(self._grid[dummy_row])
        if arr == sorted(arr):
            return True
        else:
            return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = "ld"
        self.update_puzzle(move_string)
        if self._grid[0][target_col] != target_col:
            zero_row,zero_col = self.current_position(0,0)
            target_value_pos = self.current_position(0,target_col)
            if zero_row != target_value_pos[0]:
                move_string += "u"
                self.update_puzzle("u")
            move_string += "l" * (zero_col - target_value_pos[1])
            self.update_puzzle("l" * (zero_col - target_value_pos[1]))
            iter_times = 0
            while self._grid[1][target_col-1] != target_col or self._grid[1][target_col-2] != 0:
                if self._grid[1][target_col-1] == target_col and self._grid[1][target_col-2] != 0:
                    move_string += "ld"
                    self.update_puzzle("ld")
                    break
                iter_times += 1
                if iter_times == 10:
                    break
                move_string += self.solve_row0_tile_helper(target_col)
                if self._grid[1][target_col-2] == target_col and self._grid[1][target_col-1] == 0:
                    move_string += "l"
                    self.update_puzzle("l")
                    break
            move_string += "urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")
            
        zero_row,zero_col = self.current_position(0,0)
        move_string_temp = ""
        if zero_row != 1 and zero_col != target_col - 1:
            move_string_temp += "d" * (1 - zero_row)
            move_string_temp += "r" * target_col - 1 - zero_col
            move_string += move_string_temp
            self.update_puzzle(move_string_temp)
        return move_string
        
    def solve_row0_tile_helper(self,target_col):
        """
        solve_row0_tile_helper
        """
        move_string = ""
        zero_row,zero_col = self.current_position(0,0)
        target_value_pos = self.current_position(0,target_col)
        if target_value_pos[0] == 0:
            if zero_row == 1 and zero_col == target_value_pos[1]:
                move_string += "u"
            elif zero_row == 0 and zero_col < target_value_pos[1]:
                move_string += "dru"
            else:
                move_string += "dlu"
        elif target_value_pos[0] == 1:
            if zero_row == 1 and zero_col > target_value_pos[1]:
                move_string += "l"
            elif zero_row == 0 and zero_col == target_value_pos[1]:
                move_string += "rdl"
            else:
                move_string += "urrdl"
        self.update_puzzle(move_string)
        return move_string
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        target_pos = self.current_position(1,target_col)
        move_string +=  self.swap_zero_target_tile(target_pos)
        print self._grid[1][target_col]
        if self._grid[1][target_col] != self.get_width() + target_col:
            iter_times = 0
            while self._grid[1][target_col] != self.get_width() + target_col:
                iter_times += 1
                if iter_times == 10:
                    break
                target_pos = self.current_position(1,target_col)
                move_string += self.position_tile(target_pos,1, target_col)
        zero_row,zero_col = self.current_position(0,0)
        move_string_temp = ""
        if zero_row != 0:
            move_string_temp += "u" * zero_row
        move_string_temp += "r" * (target_col-zero_col)
        move_string += move_string_temp
        self.update_puzzle(move_string_temp)
        
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        if zero_row == 0 and zero_col == 1:
             move_string += "l"
        elif zero_row == 1 and zero_col == 0:
             move_string += "u"
        elif zero_row == 1 and zero_col == 1:
            move_string += "lu"
        self.update_puzzle(move_string)
        iter_times = 0
        while not self.is_solved():
            iter_times += 1
            #not every  2x2 grid can be solve
            if iter_times == 10:
                break
            self.update_puzzle("rdlu")
            move_string += "rdlu"
            
        return move_string
    
    def is_solved(self):
        """
            check the 2 by 2 grid is solved
            return boolean value
        """
        for dummy_i in range(2):
            for dummy_j in range(2):
                if self._grid[dummy_i][dummy_j] != dummy_i * self.get_width() + dummy_j:
                    return False
        return True

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        for dummy_row in range(2,self.get_height())[::-1]:
            for dummy_col in range(self.get_width())[::-1]:
                print self
                if dummy_col > 0:
                    print "solve_interior_tile",dummy_row,dummy_col
                    move_string += self.solve_interior_tile(dummy_row,dummy_col)
                else:
                    print "solve_col0_tile",dummy_row
                    move_string += self.solve_col0_tile(dummy_row)
                print "-------------------------------------------------------"
        for dummy_col in range(2,self.get_width())[::-1]:
            print self
            print "solve_row1_tile",dummy_col
            print "-------------------------------------------------------"
            move_string += self.solve_row1_tile(dummy_col)
            print self
            print "solve_row0_tile",dummy_col
            print "-------------------------------------------------------"
            move_string += self.solve_row0_tile(dummy_col)
        move_string += self.solve_2x2()
        return move_string
        
    def swap_zero_target_tile(self,target_pos):
        """
            swap_zero_target_tile
        """
        zero_row, zero_col = self.current_position(0,0)
        move_string = "u" * (zero_row - target_pos[0])
        self.update_puzzle(move_string)
        zero_row, zero_col = self.current_position(0,0)
        move_string_temp = ""
        if zero_col < target_pos[1]:
            move_string_temp += "r" * (target_pos[1] - zero_col)
        elif zero_col > target_pos[1]:
            move_string_temp += "l" * (zero_col - target_pos[1])
        
        self.update_puzzle(move_string_temp)
        return move_string + move_string_temp
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))uull
#obj = Puzzle(4, 4, [[4,13,1,3], [5,10,2,7], [8,12,6,11], [9,0,14,15]])
#print obj
#print obj.solve_interior_tile(3,1)
#print obj
#print "************************************"
#print obj.solve_col0_tile(3)
#print obj

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj
#obj.solve_interior_tile(2, 2)
#print obj
#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print obj
#print obj.row0_invariant(0)

#obj = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#print obj
#print obj.solve_interior_tile(2, 2) 
#print obj

#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print obj
#obj.solve_col0_tile(3)
#print obj

#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#print obj
#obj.solve_col0_tile(2)
#print obj
#
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj
#obj.solve_puzzle()
#print obj

#obj = Puzzle(4, 5, [[1, 5, 0, 3, 4], [6, 2, 7, 8, 9], [10, 11, 12, 13, 14],[15, 16, 17, 18, 19]])
#print obj
#obj.solve_row0_tile(2) 
#print obj
#
#obj = Puzzle(4, 5, [[1, 2, 3, 8, 4], [6, 7, 5, 0, 9], [10, 11, 12, 13, 14],[15, 16, 17, 18, 19]])
#print obj
#obj.solve_row1_tile(3)
#print obj
#obj = Puzzle(2, 3, [[3,4,1],[0,2,5]])
#print obj
#obj.update_puzzle("urdlurrdluldrruld")
#print obj
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj
#obj.solve_row0_tile(4)
#print obj

#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj
#obj.solve_puzzle() 
#print obj

puzzle = Puzzle(10, 10, [[10, 2, 13, 12, 4, 5, 0, 7, 18, 8],
[11, 1, 22, 3, 14, 15, 6, 16, 17, 29],
[20, 21, 32, 23, 24, 25, 26, 28, 19, 9],
[30, 31, 42, 33, 34, 35, 36, 27, 38, 39],
[40, 41, 52, 43, 44, 56, 46, 37, 48, 49],
[50, 51, 53, 54, 57, 75, 45, 47, 59, 69],
[60, 61, 62, 63, 55, 85, 65, 58, 67, 68],
[70, 71, 72, 73, 74, 66, 64, 77, 78, 79],
[80, 81, 82, 83, 84, 95, 76, 87, 88, 89],
[90, 91, 92, 93, 94, 96, 86, 97, 98, 99]])
sol=puzzle.solve_puzzle()
print sol
print len(sol)
print puzzle