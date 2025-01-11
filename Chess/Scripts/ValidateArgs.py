
"""
Validates the commandline arguments.

Args:
    args (list): Command line arguments.

Returns:
        int: 0 if invalid args
        int: 1 if 1 player game
        int: 2 if 2 player game
"""
def validate_args(args):
    if len(args) != 2:
        return 0

    if args[1] == "computer":
        return 1
    elif args[1] == "player":
        return 2

    return 0 #invalid argument