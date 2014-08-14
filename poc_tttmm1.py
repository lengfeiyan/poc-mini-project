"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() == provided.DRAW:
        return 0, (-1, -1)
    elif board.check_win() == provided.PLAYERX:
        return SCORES[provided.PLAYERX],(-1, -1)
    elif board.check_win() == provided.PLAYERO:
        return SCORES[provided.PLAYERO],(-1, -1)
    
    empty_squares = board.get_empty_squares()
    scores = []
    squares = []
    for dummy_squares in empty_squares:
        board_temp = board.clone()
        board_temp.move(dummy_squares[0], dummy_squares[1], player)
        player_temp = provided.switch_player(player)
        score,square = mm_move(board_temp, player_temp)
        scores.append(score * SCORES[player])
        squares.append(dummy_squares)
        if score * SCORES[player] > 0:
            break
    max_score = max(scores) 
    return max_score/ SCORES[player],squares[scores.index(max_score)]
    

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERO) 

#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX) 

mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX) 