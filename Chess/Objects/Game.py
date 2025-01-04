from Objects.Board import Board
from Scripts.GUIController import *
from Scripts.TurnValidator import *

"""Class for managing all game logic"""
class Game:
    """Turn conventions:
    white - 0
    black - 1
    """

    """Setup new game"""
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.selected = (0,0)
        self.down_press = (0,0)
        # slots 1 -> 8 keep track of en passant
        # slots 0 and 9 keep track for castling
        self.en_passant = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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
        display, clock, FPS = setup_display()

        if arg == "computer":
            self.__run_1_player(display, clock, FPS)
            return
        if arg == "player":
            self.__run_2_player(display, clock, FPS)
            return

        # we should only reach here if the VALID argument is a path to a game state file
        """
        try:
            self.__read_game_state(arg)
            game_type = self.__choose_game_type() # the user is prompted to choose an opponent type
            if game_type == "computer":
                self.__run_1_player(display, clock, FPS)
            else:
                self.__run_2_player(display, clock, FPS)
        except Exception as err:
            print("An exception occurred when loading the game save:")
            print(Exception)
        """


    """Runs the 1 player game until the end or until stopped"""
    def __run_1_player(self, display, clock, FPS):
        pass

    """Runs the 2 player game until the end or until stopped"""
    def __run_2_player(self, display, clock, FPS):
        pieces, index, misc = load_assets()

        # main game loop
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # save location of mouse_down
                    self.down_press = (int(mouse_pos[1] / 96), int(mouse_pos[0] / 96))

                if event.type == pygame.MOUSEBUTTONUP:
                    i, j = (int(mouse_pos[1] / 96), int(mouse_pos[0] / 96))

                    # if MOUSEBUTTONUP and MOUSEBUTTONDOWN were done on the same tile
                    if (i,j) == self.down_press:
                        self.__handle_MOUSEBUTTONUP(mouse_pos) # handle the click
                    # otherwise ignore press (cancel action)
                    else:
                        self.down_press = (0,0)



            draw_board(pieces, index, misc, display, self.board, self.turn, mouse_pos, self.selected, self.en_passant)
            pygame.display.update()
            clock.tick(FPS)

    def __handle_MOUSEBUTTONUP(self, mouse_pos):
        reference = 6 + self.turn * 6
        layout = self.board.get_pieces()
        i = int(mouse_pos[1] / 96)
        j = int(mouse_pos[0] / 96)
        field = layout[i][j]

        # if I click on a piece that is mine and isn't the selected piece
        if field != 0 and is_same_color(reference, field) and (i, j) != self.selected:
            # if the piece has valid moves
            if len(get_all_valid_moves(layout, self.turn, (i, j), self.en_passant)) != 0:
                self.selected = (i, j)

        if self.selected != (0,0):
            matrix = move_matrix(layout, self.selected, self.en_passant)

            # if I click on a place that isn't somewhere the selected piece can move
            if matrix[i][j] == 0:
                # if I click on:
                if (field == 0 # an empty space
                    or field != 0 and not is_same_color(reference, field) # a piece that isn't mine
                ):
                    self.selected = (0,0) # deselect piece
            # if I click on a VALID place the piece can move
            elif is_valid_move(layout, self.turn, self.selected, (i, j), self.en_passant):
                if matrix[i][j] == 3:
                    self.board.get_pieces()[i + 1][j] = 0 # execute en passant

                # if the piece is a pawn and it moves 2 spaces
                if layout[self.selected[0]][self.selected[1]] % 6 == 1 and (self.selected[0] - i) == 2:
                    self.en_passant[self.turn][8 - j + 1] = 1 # mark it for en passant

                self.__make_move((i, j))

    """Moves selected piece to target_pos
    This function is only called after the move has been validated.
    """
    def __make_move(self, target_pos):
        pieces = self.board.get_pieces()

        # make the move itself
        pieces[target_pos[0]][target_pos[1]] = pieces[self.selected[0]][self.selected[1]]
        pieces[self.selected[0]][self.selected[1]] = 0

        #deselect piece
        self.selected = (0,0)

        self.__change_turn()

    """Changes the turn to the other player"""
    def __change_turn(self):
        self.turn = (self.turn + 1) % 2
        self.board.pieces = self.board.get_flipped_board()
        self.board.height.reverse()
        self.board.width.reverse()

        for i in range(1,9):
          self.en_passant[self.turn][i] = 0

    """Loads a game state into self from a game state file"""
    def __read_game_state(self, path):
        # to implement
        pass

    """The used is prompted to choose an opponent type
    Returns either "computer" (1 player game) 
    or "player" (2 player game)
    """
    def __choose_game_type(self):
        # to implement
        return "computer"