"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = float(0.0)
        self._current_cookies = float(0.0)
        self._current_time = float(0.0)
        self._cps = float(1.0)
        self._history = [(0.0, None,0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time:" + str(self._current_time) + " Current Cookies: " + str(self._current_cookies) + " cps: " + str(self._cps) + " Total Cookies:  " + str(self._total_cookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current _cps

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return _history list

        _history list should be a list of tuples of the form

        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies)/self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        else:
            #codeskulptor.set_timeout(int(time))
            self._total_cookies += self._cps * time
            self._current_cookies += self._cps * time
            self._current_time += time
            #self._history.append((self._current_time, None,None, self._total_cookies))
            
    
    def buy_item(self, item_name, cost, additional__cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._current_cookies:
            return
        self._current_cookies -= cost
        self._cps += additional__cps
        self._history.append((self._current_time, item_name,cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    build_info_clone = build_info.clone()
    clicker_state = ClickerState()
    while True:
        if clicker_state.get_time() > duration:
            break
        item_name = strategy(clicker_state.get_cookies(),clicker_state.get_cps(),duration-clicker_state.get_time(),build_info_clone)
        if item_name is None:
            break
        time = clicker_state.time_until(build_info_clone.get_cost(item_name))
        if time > duration - clicker_state.get_time():
            break
        clicker_state.wait(clicker_state.time_until(build_info_clone.get_cost(item_name)))
        clicker_state.buy_item(item_name,build_info_clone.get_cost(item_name),build_info_clone.get_cps(item_name))
        build_info_clone.update_item(item_name)
        
    clicker_state.wait(duration-clicker_state.get_time())
        
    return clicker_state


def strategy_cursor(cookies, cps, time_left, build_info):

    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    cant buy in the time left.
    """
    if cookies + cps * time_left < build_info.get_cost("Cursor"):
        return None
    else:
        return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    min_cost = float('inf')
    min_cost_item = None
    for dummy_item in build_info.build_items():
        cost = build_info.get_cost(dummy_item)
        if cost < min_cost:
            min_cost = cost
            min_cost_item = dummy_item
    if cookies + cps * time_left < min_cost:
        return None
    else:
        return min_cost_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
     always select the most expensive item you can afford in the time left.
    """
    max_cost = float('-inf')
    max_cost_item = None
    for dummy_item in build_info.build_items():
        cost = build_info.get_cost(dummy_item)
        if cost > max_cost:
            if cookies + cps * time_left >= cost:
                max_cost = cost
                max_cost_item = dummy_item
    if cookies + cps * time_left < max_cost:
        return None
    else:
        return max_cost_item

def strategy_best(cookies, cps, time_left, build_info):
    """
     best strategy that you can come up with.
    """
    items = build_info.build_items()
    while True:
        item = random.choice(items)
        return item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    
    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # _history = state.get_history()
    # _history = [(item[0], item[3]) for item in _history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [_history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor)
    # print "-------------------------"
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # print "-------------------------"
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # print "-------------------------"
    run_strategy("Best", SIM_TIME, strategy_best)
    
    
    
    
run()