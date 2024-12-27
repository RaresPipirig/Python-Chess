from Objects.Board import Board


class Game:
    """Turn conventions:
    white - 0
    black - 1
    """

    """Setup new game"""
    def __init__(self):
        self.board = Board()
        self.turn = 0

    """Saves the state of the current game in a file"""
    def __save_state(self):
        # to implement
        return

    """Loads the state of a game given a file path """
    def __load_state(self, path):
        # to implement
        return

    """Determines the type of game based on arguments and starts it"""
    def start(self, args):
        # to implement
        return