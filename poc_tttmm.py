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
    max_score = -1
    max_score_square = None
    other_player = provided.switch_player(player)
    for dummy_squares in empty_squares:
        board_temp = board.clone()
        board_temp.move(dummy_squares[0], dummy_squares[1], player)
        score,square = mm_move(board_temp, other_player)
        if score * SCORES[player] > 0:
            return score,dummy_squares
        if score * SCORES[player] > max_score:
            max_score = score * SCORES[player]
            max_score_square = dummy_squares
    return max_score/ SCORES[player],max_score_square
    

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

print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERO) 
#[-25.0 pts] mm_move(TTTBoard(3, False, [[PLAYERX, EMPTY, EMPTY], [PLAYERO, PLAYERO, EMPTY], [EMPTY, PLAYERX, EMPTY]]), PLAYERX) returned bad move (0, (-1, -1))
#[-15.0 pts] mm_move(TTTBoard(3, False, [[EMPTY, EMPTY, PLAYERX], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]), PLAYERO) returned invalid move (0, (-1, -1))