from Scripts.TurnValidator import get_all_possible_moves
import random

class FunkyLittleComputer:
    """Class for handling the computer opponent"""

    """
    From all possible valid moves it selects a random one and returns it.
    
    Args:
        board (list): Matrix which contains the layout of the game pieces.
        turn (int): Indicates which player makes the next move.
        en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
        
    Returns:
        int: 0 if there are no possible moves (game end).
        list: List containing 2 coords (a piece on the board and where it moves).
    """
    def select_a_move(self, board, turn, en_passant):
        moves = get_all_possible_moves(board, turn, en_passant)
        if len(moves) == 0:
            return 0

        rand = random.random() * 100000
        piece = moves[int(rand % len(moves))]

        rand = random.random() * 100000
        target = piece[1][int(rand % len(piece[1]))]

        return [piece[0], target]