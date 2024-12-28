from logging import exception

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
    def start(self, arg):
        if arg == "computer":
            self.__run_1_player()
            return
        if arg == "player":
            self.__run_2_player()
            return

        # we should only reach here if the VALID argument is a path to a game state file
        try:
            self.__read_game_state(arg)
            game_type = self.__choose_game_type() # the user is prompted to choose an opponent type
            if game_type == "computer":
                self.__run_1_player()
            else:
                self.__run_2_player()
        except Exception as err:
            print("An exception occurred when loading the game save:")
            print(Exception)



    """Runs the 1 player game until the end or until stopped"""
    def __run_1_player(self):
        # to implement
        return

    """Runs the 2 player game until the end or until stopped"""
    def __run_2_player(self):
        # to implement
        return

    """Loads a game state into self from a game state file"""
    def __read_game_state(self, path):
        # to implement
        return

    """The used is prompted to choose an opponent type
    Returns either "computer" (1 player game) 
    or "player" (2 player game)
    """
    def __choose_game_type(self):
        # to implement
        return "computer"