"""Setup and remember the state of the board"""
class Board:
    """Game piece conventions:
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

    def __init__(self, state=None):
        self.__init_layout()
        if state is None:
            self.__init_layout() # setup for game start
        else:
            self.__init_pieces(state) # setup for given game state

    def __init_layout(self):
        # the layout of the board itself
        self.layout = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # position identifiers
        self.width = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.height = [1, 2, 3, 4, 5, 6, 7, 8]

    """Setup pieces for the start of a chess game"""
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

    """Setup pieces for a given game state"""
    def __init_pieces(self, state):
        self.pieces = state

    """Saves the state of the current game in a file"""
    def save_state(self):
        # to implement
        return

    """Loads the state of a game given a file path """
    def load_state(self, path):
        # to implement
        return
