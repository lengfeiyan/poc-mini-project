"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"

class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
        #self.set_full(row,col)
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for dummy_item in self._zombie_list:
            yield (dummy_item[0],dummy_item[1])

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        #self.set_full(row,col)
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        #generator(self._human_list)
        for dummy_item in self._human_list:
            yield (dummy_item[0],dummy_item[1])

        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self.get_grid_height(),self.get_grid_width())
        visited.clear()
        distance_field = [([self.get_grid_width() * self.get_grid_height()] * self.get_grid_width()) for dummy_i in range(self.get_grid_height())]
        boundary = poc_queue.Queue()
        for dummy_item in (self.zombies() if entity_type == ZOMBIE else self.humans()):
            boundary.enqueue(dummy_item)
            visited.set_full(dummy_item[0],dummy_item[1])
            distance_field[dummy_item[0]][dummy_item[1]] = 0
        
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            #for dummy_neighbors in self.four_neighbors(current_cell[0],current_cell[1]) if entity_type == ZOMBIE else self.eight_neighbors(current_cell[0],current_cell[1]):
            for dummy_neighbors in self.four_neighbors(current_cell[0],current_cell[1]):            
                if self.is_empty(dummy_neighbors[0],dummy_neighbors[1]):
                    if visited.is_empty(dummy_neighbors[0],dummy_neighbors[1]):
                        visited.set_full(dummy_neighbors[0],dummy_neighbors[1])
                        boundary.enqueue(dummy_neighbors)
                        if distance_field[dummy_neighbors[0]][dummy_neighbors[1]] > distance_field[current_cell[0]][current_cell[1]] + 1:
                            distance_field[dummy_neighbors[0]][dummy_neighbors[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        
        return distance_field
        
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        print zombie_distance
        temp_humans_list = []
        for dummy_human in self._human_list:
            current_distance = zombie_distance[dummy_human[0]][dummy_human[1]]
            all_neighbors = self.eight_neighbors(dummy_human[0],dummy_human[1])
            faster_neighbors = []
            faster_distance = 0
            for dummy_neighbor in all_neighbors:
                if zombie_distance[dummy_neighbor[0]][dummy_neighbor[1]] > current_distance and zombie_distance[dummy_neighbor[0]][dummy_neighbor[1]] > faster_distance:
                    faster_neighbors= [dummy_neighbor]
                    faster_distance = zombie_distance[dummy_neighbor[0]][dummy_neighbor[1]]
                elif zombie_distance[dummy_neighbor[0]][dummy_neighbor[1]] > current_distance and zombie_distance[dummy_neighbor[0]][dummy_neighbor[1]] == faster_distance:
                    faster_neighbors.append(dummy_neighbor)
                else:
                    pass
            if len(faster_neighbors) == 0:
                temp_humans_list.append(dummy_human)
            else:
                random_choice = random.choice(faster_neighbors)
                temp_humans_list.append((random_choice[0],random_choice[1]))
        
        self._human_list = temp_humans_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_zombies_list = []
        for dummy_zombie in self._zombie_list:
            current_distance = human_distance[dummy_zombie[0]][dummy_zombie[1]]
            all_neighbors = self.four_neighbors(dummy_zombie[0],dummy_zombie[1])
            close_neighbors = []
            close_distance = self.get_grid_width() * self.get_grid_height()
            for dummy_neighbor in all_neighbors:
                if human_distance[dummy_neighbor[0]][dummy_neighbor[1]] < current_distance and human_distance[dummy_neighbor[0]][dummy_neighbor[1]] == close_distance:
                    close_neighbors.append(dummy_neighbor)
                elif human_distance[dummy_neighbor[0]][dummy_neighbor[1]] < current_distance and human_distance[dummy_neighbor[0]][dummy_neighbor[1]] < close_distance:
                    close_neighbors = [dummy_neighbor]
                    close_distance = human_distance[dummy_neighbor[0]][dummy_neighbor[1]]
                else:
                    pass
            if len(close_neighbors) == 0:
                temp_zombies_list.append(dummy_zombie)
            else:
                random_choice = random.choice(close_neighbors)
                temp_zombies_list.append((random_choice[0],random_choice[1]))
        
        self._zombie_list = temp_zombies_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
#poc_zombie_gui.run_gui(Zombie(20, 20,None,[(1,1)],[(7,7)]))

#obj = Zombie(3, 3, [], [], [(2, 2)])
#print obj.compute_distance_field('human')