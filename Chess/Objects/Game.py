from Objects.Board import Board
from Scripts.GUIController import *
from Scripts.TurnValidator import *
from Scripts.FunkyLittleComputer import FunkyLittleComputer

"""
Class for managing all game logic.

Turn conventions:
    white - 0
    black - 1
"""
class Game:
    """Setup new game"""
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.selected = (0,0)
        self.down_press = (0,0)
        # slots 1 -> 8 keep track of en passant
        # slots 0 and 9 keep track for castling
        self.en_passant = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.computer = FunkyLittleComputer()

    """
    Determines the type of game based on arguments and starts it.
    
    Args:
        arg (str): String containing a valid command line argument.
    """
    def start(self, arg):
        display, clock, FPS = setup_display()

        if arg == "computer":
            self.__run_1_player(display, clock, FPS)
            return
        if arg == "player":
            self.__run_2_player(display, clock, FPS)
            return


    """
    Runs the game cycle of the single player game.
    
    Args:
        display (Surface): Pygame object which represents the display itself.
        clock (Clock): Pygame object which regulates the FPS of the game.
        FPS (int): The framerate the game runs at.
    """
    def __run_1_player(self, display, clock, FPS):
        pieces, index, misc = load_assets()

        # main game loop
        while True:
            mouse_pos = pygame.mouse.get_pos()

            if self.turn == 1:
                move = self.computer.select_a_move(self.board.get_pieces(), self.turn, self.en_passant)

                # don't draw the frame where the computer makes a move
                if move != 0:
                    self.selected = move[0]
                    self.__make_move(move[1])
                # draw the end of game screen if you win
                else:
                    draw_board(pieces, index, misc, display, self.board, self.turn, mouse_pos, self.selected,
                               self.en_passant)
                    pygame.display.update()
                    clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # save location of mouse_down
                    self.down_press = (int(mouse_pos[1] / 96), int(mouse_pos[0] / 96))

                if event.type == pygame.MOUSEBUTTONUP:
                    i, j = (int(mouse_pos[1] / 96), int(mouse_pos[0] / 96))

                    # if MOUSEBUTTONUP and MOUSEBUTTONDOWN were done on the same tile
                    if (i, j) == self.down_press:
                        self.__handle_MOUSEBUTTONUP(mouse_pos)  # handle the click
                    # otherwise ignore press (cancel action)
                    else:
                        self.down_press = (0, 0)

            if self.turn == 0:
                draw_board(pieces, index, misc, display, self.board, self.turn, mouse_pos, self.selected, self.en_passant)
                pygame.display.update()
                clock.tick(FPS)

    """
    Runs the game cycle of the 2 players game.
    
    Args:
        display (Surface): Pygame object which represents the display itself.
        clock (Clock): Pygame object which regulates the FPS of the game.
        FPS (int): The framerate the game runs at.
    """
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

    """
    Event handler for mouse click.
    
    Args:
        mouse_pos (tuple): The position of the mouse at the moment of the click.
    """
    def __handle_MOUSEBUTTONUP(self, mouse_pos):
        reference = 6 + self.turn * 6
        layout = self.board.get_pieces()
        # the coords of the tile the mouse click is on
        i = int(mouse_pos[1] / 96)
        j = int(mouse_pos[0] / 96)
        field = layout[i][j]

        # checks selected piece for pawn promotion
        if layout[self.selected[0]][self.selected[1]] % 6 == 1 and self.selected[0] == 1:
            self.__handle_click_pawn_promotion((i, j), layout[self.selected[0]][self.selected[1]])
            return

        # if I click on a piece that is mine and isn't the selected piece
        if field != 0 and is_same_color(reference, field) and (i, j) != self.selected:
            # if the piece has valid moves
            if len(get_all_valid_moves(layout, self.turn, (i, j), self.en_passant)) != 0:
                self.selected = (i, j)

        # if a piece is already selected
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
                self.__make_move((i, j))

    """
    Particular click event handling for castling.
    
    Args:
        target (tuple): The coords of the tile on which the click was performed.
    """
    def __handle_click_castling(self, target):
        i, j = self.selected[0], self.selected[1]
        board = self.board.get_pieces()
        piece = board[i][j]

        if j < target[1]: # castling to the right
            board[i][ j + 2] = piece
            board[i][j] = 0
            board[i][j + 1] = piece - 4
            board[8][8] = 0
        else: # castling to the left
            board[i][j - 2] = piece
            board[i][j] = 0
            board[i][j - 1] = piece - 4
            board[8][1] = 0

        self.selected = (0, 0)
        self.__change_turn()

    """
    Particular click event handling for pawn promotion.
    
    Args:
        mouse_pos (tuple): The coords of the tile on which the click was performed.
        pawn (int): The value of the pawn which performs the promotion.
    """
    def __handle_click_pawn_promotion(self, mouse_pos, pawn):
        i, j = mouse_pos[0], mouse_pos[1]

        switch = {
            2: 4,
            3: 3,
            4: 2,
            5: 1
        }

        if j != self.selected[1] or i < 1 or i > 5:
            self.selected = (0,0)
        else:
            if i == 1:
                return

            self.board.get_pieces()[self.selected[0]][self.selected[1]] = pawn + switch[i]
            self.__change_turn()


    """
    Performs a move.
    
    Args:
        target_pos (tuple): The coords of the tile onto which the piece moves.
    """
    def __make_move(self, target_pos):
        i, j = target_pos[0], target_pos[1]

        layout = self.board.get_pieces()

        matrix = move_matrix(layout, self.selected, self.en_passant)

        if matrix[i][j] == 3:
            layout[i + 1][j] = 0  # execute en passant

        # if the piece is a pawn and it moves 2 spaces
        if layout[self.selected[0]][self.selected[1]] % 6 == 1 and (self.selected[0] - i) == 2:
            self.en_passant[self.turn][8 - j + 1] = 1  # mark it for en passant

        # if the rooks move, you cannot perform castling on that side anymore
        if self.selected == (8, 1):
            self.en_passant[self.turn][0] = 1
        if self.selected == (8, 8):
            self.en_passant[self.turn][9] = 1

        # if the king moves, you cannot perform castling anymore
        if layout[self.selected[0]][self.selected[1]] % 6 == 0:
            self.en_passant[self.turn][0], self.en_passant[self.turn][9] = 1, 1

            # if the castling is performed on this click
            difference = j - self.selected[1]
            if difference > 1 or difference < -1:
                self.__handle_click_castling((i, j))
                return


        pieces = self.board.get_pieces()

        # make the move itself
        pieces[target_pos[0]][target_pos[1]] = pieces[self.selected[0]][self.selected[1]]
        pieces[self.selected[0]][self.selected[1]] = 0

        #deselect piece
        self.selected = (0, 0)

        self.__change_turn()

    """Changes the turn to the other player"""
    def __change_turn(self):
        self.turn = (self.turn + 1) % 2 # turn indicator
        self.board.pieces = self.board.get_flipped_board() # flip the board
        # index flip
        self.board.height.reverse()
        self.board.width.reverse()

        # you can only perform en passant in the turn immediately after a pawn has moved 2 spaces
        for i in range(1,9):
          self.en_passant[self.turn][i] = 0