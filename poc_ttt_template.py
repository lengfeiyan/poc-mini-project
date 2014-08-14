"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
def mc_trial(board, player):
    """
    mc_trial
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        if len(empty_squares) == 0:
            break
        empty_squares = board.get_empty_squares()
        square = random.choice(empty_squares)
        board.move(square[0],square[1],player)
        if player == provided.PLAYERX:
            player = provided.PLAYERO
        else:
            player = provided.PLAYERX
    

def mc_update_scores(scores, board, player):
    """
    mc_update_scores
    """
    #print "-----------------------------------"
    #print scores
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    dim = board.get_dim()
    for dummy_i in range(dim):
        for dummy_j in range(dim):
            square = board.square(dummy_i,dummy_j)
            if square == provided.EMPTY:
                continue
            if winner == player and square == player:
                scores[dummy_i][dummy_j] += MCMATCH
            if winner == player and square != player and square != provided.EMPTY:
                scores[dummy_i][dummy_j] -= MCOTHER
            if winner != player and square == player:
                scores[dummy_i][dummy_j] -= MCMATCH
            if winner != player and square != player and square != provided.EMPTY:
                scores[dummy_i][dummy_j] += MCOTHER
    #print scores
    #print "-----------------------------------"

def get_best_move(board, scores):
    """
    get_best_move
    """
    empty_squares = board.get_empty_squares()
    
    max_score = float("-inf")
    result = (0,0)
    for dummy_square in empty_squares:
        if scores[dummy_square[0]][dummy_square[1]] > max_score:
            max_score = scores[dummy_square[0]][dummy_square[1]]
            result = dummy_square
    return result

def mc_move(board, player, trials):
    """
    mc_move
    """
    dim = board.get_dim()
    scores = [ [0 for dummy_col in range(dim)] for dummy_row in range(dim)]
    for dummy in range(trials):
        board_clone = board.clone()
        current_player = player
        mc_trial(board_clone, current_player)
        mc_update_scores(scores, board_clone, player)
    
    for dummy_i in range(dim):
        for dummy_j in range(dim):
            scores[dummy_i][dummy_j] = scores[dummy_i][dummy_j]/trials
    
    print scores
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
