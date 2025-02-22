import copy

"""
Class responsible for storing game board related data.

Game piece conventions:
    no piece - 0
    white pawn - 1
    white rook - 2
    white knight - 3
    white bishop - 4
    white queen - 5
    white king - 6
    black pawn - 7
    black rook - 8
    black knight - 9
    black bishop - 10
    black queen - 11
    black king - 12
"""
class Board:
    def __init__(self):
        self.__init_layout()
        self.__init_pieces_start() # setup for game start


    """
    Sets up the layout of the board.
    
    Conventions:
        0 - white
        1 - black
        2 - border
    """
    def __init_layout(self):
        # the layout of the board itself
        self.layout = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 0, 1, 0, 1, 0, 1, 0, 1, 2],
                       [2, 1, 0, 1, 0, 1, 0, 1, 0, 2],
                       [2, 0, 1, 0, 1, 0, 1, 0, 1, 2],
                       [2, 1, 0, 1, 0, 1, 0, 1, 0, 2],
                       [2, 0, 1, 0, 1, 0, 1, 0, 1, 2],
                       [2, 1, 0, 1, 0, 1, 0, 1, 0, 2],
                       [2, 0, 1, 0, 1, 0, 1, 0, 1, 2],
                       [2, 1, 0, 1, 0, 1, 0, 1, 0, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

        # position identifiers
        self.width = [0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 0]
        self.height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 0]

    """Sets up pieces for the start of a chess game."""
    def __init_pieces_start(self):
        self.pieces = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 8, 9, 10, 11, 12, 10, 9, 8, 0],
                       [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 2, 3, 4, 5, 6, 4, 3, 2, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # stalemate test
        """self.pieces = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 8, 9, 10, 11, 12, 10, 9, 8, 0],
                       [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 11, 0, 8, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]"""

    """
    Returns a flipped copy of the board.

    Returns:
            list: The matrix itself.
    """
    def get_flipped_board(self):
        board_copy = copy.deepcopy(self.pieces)
        board_copy = list(zip(*board_copy[::-1]))
        board_copy = list(zip(*board_copy[::-1]))

        return [list(row) for row in board_copy]

    """Getters"""

    """
    Returns the layout of the chess board itself.
    
    Returns:
        list: The matrix.
    """
    def get_layout(self):
        return self.layout

    """
    Returns the indexes of the width of the board.
    
    Returns:
        list: The array.
    """
    def get_width_index(self):
        return self.width

    """
        Returns the indexes of the height of the board.

        Returns:
            list: The array.
        """
    def get_height_index(self):
        return self.height

    """
        Returns the layout of the game pieces.

        Returns:
            list: The matrix.
        """
    def get_pieces(self):
        return self.pieces
