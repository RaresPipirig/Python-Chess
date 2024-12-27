import sys

from Objects.Game import Game
from Scripts.ValidateArgs import validate_args

arg = validate_args(sys.argv)

if arg == 0:
    raise Exception("Invalid argument(s).")

current_game = Game()
current_game.start(arg)
