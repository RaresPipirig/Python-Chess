from Scripts.TurnValidator import get_all_possible_moves
import random

"""Class for handling the computer opponent"""
class FunkyLittleComputer:

    """From all possible valid moves it selects a random one and returns it"""
    def select_a_move(self, board, turn, en_passant):
        moves = get_all_possible_moves(board, turn, en_passant)
        if len(moves) == 0:
            return 0

        rand = random.random() * 100000
        piece = moves[int(rand % len(moves))]

        rand = random.random() * 100000
        target = piece[1][int(rand % len(piece[1]))]

        return [piece[0], target]