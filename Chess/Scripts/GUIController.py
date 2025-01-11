import pygame
from Scripts.TurnValidator import move_matrix, is_in_check, is_valid_move, get_all_valid_moves, get_all_possible_moves, \
    is_same_color

"""Script for handling all GUI operations"""

"""
Sets up the display window upon opening the game.

Returns:
    Surface: Pygame object which represents the display itself.
    Clock: Pygame object which regulates the FPS of the game.
    int: The framerate the game runs at.
"""
def setup_display():
    pygame.init()
    display = pygame.display.set_mode((960,960))
    clock = pygame.time.Clock()
    FPS = 60
    return display, clock, FPS

"""
Loads the images into objects and adjusts the scale.

Returns:
    list: 3 lists containing the loaded game assets.
"""
def load_assets():
    # load the pieces assets
    pieces = [pygame.image.load("Assets/empty_pixel.png"), # the first asset is an empty pixel for the sake of convenience
              pygame.image.load("Assets/pieces/white_pawn.png"),
              pygame.image.load("Assets/pieces/white_rook.png"),
              pygame.image.load("Assets/pieces/white_knight.png"),
              pygame.image.load("Assets/pieces/white_bishop.png"),
              pygame.image.load("Assets/pieces/white_queen.png"),
              pygame.image.load("Assets/pieces/white_king.png"),
              pygame.image.load("Assets/pieces/black_pawn.png"),
              pygame.image.load("Assets/pieces/black_rook.png"),
              pygame.image.load("Assets/pieces/black_knight.png"),
              pygame.image.load("Assets/pieces/black_bishop.png"),
              pygame.image.load("Assets/pieces/black_queen.png"),
              pygame.image.load("Assets/pieces/black_king.png")]

    # adjust the scale of the piece assets
    index = 0
    for image in pieces:
        pieces[index] = pygame.transform.scale(image, (96,96))
        index += 1

    # load the index assets
    index = {
        0 : pygame.transform.scale(pygame.image.load("Assets/empty_pixel.png"), (96,96)), # for corners, this is also for the sake of convenience
        1 : pygame.transform.scale(pygame.image.load("Assets/Index/index_1.png"), (96,96)),
        2 : pygame.transform.scale(pygame.image.load("Assets/Index/index_2.png"), (96,96)),
        3 : pygame.transform.scale(pygame.image.load("Assets/Index/index_3.png"), (96,96)),
        4 : pygame.transform.scale(pygame.image.load("Assets/Index/index_4.png"), (96,96)),
        5 : pygame.transform.scale(pygame.image.load("Assets/Index/index_5.png"), (96,96)),
        6 : pygame.transform.scale(pygame.image.load("Assets/Index/index_6.png"), (96,96)),
        7 : pygame.transform.scale(pygame.image.load("Assets/Index/index_7.png"), (96,96)),
        8 : pygame.transform.scale(pygame.image.load("Assets/Index/index_8.png"), (96,96)),
        "a" : pygame.transform.scale(pygame.image.load("Assets/Index/index_a.png"), (96,96)),
        "b" : pygame.transform.scale(pygame.image.load("Assets/Index/index_b.png"), (96,96)),
        "c" : pygame.transform.scale(pygame.image.load("Assets/Index/index_c.png"), (96,96)),
        "d" : pygame.transform.scale(pygame.image.load("Assets/Index/index_d.png"), (96,96)),
        "e" : pygame.transform.scale(pygame.image.load("Assets/Index/index_e.png"), (96,96)),
        "f" : pygame.transform.scale(pygame.image.load("Assets/Index/index_f.png"), (96,96)),
        "g" : pygame.transform.scale(pygame.image.load("Assets/Index/index_g.png"), (96,96)),
        "h" : pygame.transform.scale(pygame.image.load("Assets/Index/index_h.png"), (96,96))
    }

    # load miscellaneous assets
    misc = {
        0 : pygame.transform.scale(pygame.image.load("Assets/turn_white.png"), (960,96)),
        1 : pygame.transform.scale(pygame.image.load("Assets/turn_black.png"), (960,96)),
        3 : pygame.transform.scale(pygame.image.load("Assets/check.png"), (96,960)),
        4 : pygame.transform.scale(pygame.image.load("Assets/mate.png"), (96,960)),
        5 : pygame.transform.scale(pygame.image.load("Assets/white_wins.png"), (960,192)),
        6 : pygame.transform.scale(pygame.image.load("Assets/black_wins.png"), (960,192)),
        7 : pygame.transform.scale(pygame.image.load("Assets/stalemate.png"), (960,192))
    }

    return pieces, index, misc

"""
Draws the game board upon being given a game state.

Args:
    pieces (list): List containing game assets representing game pieces.
    index (list): List containing game assets representing the board indexes.
    misc (list): List containing game assets representing miscellaneous assets.
    display (Surface): Pygame object which represents the display itself.
    board (Board): Game object containing information about the game state.
    turn (int): Indicates which player makes the next move.
    mouse_pos (tuple): The position of the mouse.
    selected (tuple): Coordinates of the selected piece or (0, 0) if no piece is selected.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
"""
def draw_board(pieces, index, misc, display, board, turn, mouse_pos, selected, en_passant):
    __draw_game_board(board, display, index)
    __draw_gameplay_elements(board, display, pieces, misc, turn, en_passant)

    # if the game has ended, don't draw the mouse interaction
    if (is_in_check(turn, board.get_pieces(), en_passant)
        and len(get_all_possible_moves(board.get_pieces(), turn, en_passant)) == 0):
            __draw_game_end(display, turn, misc) # check mate
    elif len(get_all_possible_moves(board.get_pieces(), turn, en_passant)) == 0:
        display.blit(misc[7], (0, 4 * 96)) # stalemate
    # if the selected piece is a pawn on promotion
    elif board.get_pieces()[selected[0]][selected[1]] % 6 == 1 and selected[0] == 1:
        # custom interaction
        __pawn_promotion_interaction(display,
                                     mouse_pos,
                                     pieces,
                                     selected,
                                     board.get_pieces()[selected[0]][selected[1]])
    else:
        # normal mouse interaction
        __draw_mouse_interaction(board, display, turn, mouse_pos, selected, en_passant)

    """tests"""
    #__draw_matrix(board, display)
    #print(is_valid_move(board.get_pieces(), turn, (7, 5), (5, 6)))
    #print(get_all_valid_moves(board.get_pieces(), turn, (8, 2)))
    #print(get_all_possible_moves(board.get_pieces(), turn))

"""
Custom mouse/GUI interaction for selecting a piece on pawn promotion.

Args:
    display (Surface): Pygame object which represents the display itself.
    mouse_pos (tuple): The position of the mouse.
    pieces (list): List containing game assets representing game pieces.
    selected (tuple): Coordinates of the selected piece or (0, 0) if no piece is selected.
    pawn (int): Value of the selected pawn.
"""
def __pawn_promotion_interaction(display, mouse_pos, pieces, selected, pawn):
    yellow = (252, 237, 106)
    green = (106, 252, 143)

    # selected box
    pygame.draw.rect(display, yellow, pygame.Rect((selected[1] * 96, selected[0] * 96), (96, 96)), 8)
    # dropdown box
    pygame.draw.rect(display, yellow, pygame.Rect((selected[1] * 96, 2 * 96), (96, 4 * 96)))

    # draw pieces pawn can promote to
    display.blit(pieces[pawn + 4], (selected[1] * 96, 2 * 96))
    display.blit(pieces[pawn + 3], (selected[1] * 96, 3 * 96))
    display.blit(pieces[pawn + 2], (selected[1] * 96, 4 * 96))
    display.blit(pieces[pawn + 1], (selected[1] * 96, 5 * 96))

    i = int(mouse_pos[1] / 96)
    j = int(mouse_pos[0] / 96)

    if j == selected[1] and 1 < i < 6:
        pygame.draw.rect(display, green, pygame.Rect((j * 96, i * 96), (96, 96)), 8)

"""
Draws the game end pop-up.

Args:
    display (Surface): Pygame object which represents the display itself.
    turn (int): Indicates which player makes the next move.
    misc (list): List containing game assets representing miscellaneous assets.
"""
def __draw_game_end(display, turn, misc):
    if turn == 0:
        display.blit(misc[6], (0, 4 * 96))
    else:
        display.blit(misc[5], (0, 4 * 96))

"""
Makes the GUI interactive with the mouse.

Args:
    board (Board): Game object containing information about the game state.
    display (Surface): Pygame object which represents the display itself.
    turn (int): Indicates which player makes the next move.
    mouse_pos (tuple): The position of the mouse.
    selected (tuple): Coordinates of the selected piece or (0, 0) if no piece is selected.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
"""
def __draw_mouse_interaction(board, display, turn, mouse_pos, selected, en_passant):
    reference = 6 + turn * 6
    green = (106, 252, 143)
    red = (252, 106, 130)
    yellow = (252, 237, 106)

    if selected != (0,0):
        pygame.draw.rect(display, yellow, pygame.Rect((selected[1] * 96, selected[0] * 96), (96, 96)), 8)

    layout = board.get_pieces()
    i = int(mouse_pos[1] / 96)
    j = int(mouse_pos[0] / 96)
    field = layout[i][j]

    # if there is a piece that belongs to the player and isn't selected
    if field != 0 and is_same_color(reference, field) and (i, j) != selected:
        # if the piece has valid moves
        if len(get_all_valid_moves(layout, turn, (i, j), en_passant)) != 0:
            pygame.draw.rect(display, green, pygame.Rect((j * 96, i * 96), (96, 96)), 8)
        # if the piece has no valid moves
        else:
            pygame.draw.rect(display, red, pygame.Rect((j * 96, i * 96), (96, 96)), 8)

    # if a piece is selected
    if selected != (0,0):
        matrix = move_matrix(layout, selected, en_passant)

        field = matrix[i][j]
        if field != 0: # if the selected piece can move to the field under the cursor
            if is_valid_move(layout, turn, selected, (i,j), en_passant):
                if field == 1: # move normally
                    pygame.draw.rect(display, green, pygame.Rect((j * 96, i * 96), (96, 96)), 8)
                else: # move by capturing
                    pygame.draw.rect(display, yellow, pygame.Rect((j * 96, i * 96), (96, 96)), 8)

            else: # coloring red if the piece can move there but is not a valid move
                pygame.draw.rect(display, red, pygame.Rect((j * 96, i * 96), (96, 96)), 8)

"""
Draws the chess board itself.

Args:
    board (Board): Game object containing information about the game state.
    display (Surface): Pygame object which represents the display itself.
    index (list): List containing game assets representing the board indexes.
"""
def __draw_game_board(board, display, index):
    display.fill((255, 255, 255))

    # drawing the chess board
    i, j = 0, 0
    layout = board.get_layout()
    for lines in layout:
        for fields in lines:
            if layout[i][j] == 0:
                color = (255, 253, 219)  # white
            elif layout[i][j] == 1:
                color = (98, 135, 80)  # black
            else:
                color = (219, 255, 220)  # border

            pygame.draw.rect(display, color, pygame.Rect((i * 96, j * 96), (96, 96)))
            j += 1
        i += 1
        j = 0

    # drawing the number indexes
    i = 10
    layout = board.get_height_index()
    while i > -1:
        display.blit(index[layout[9 - i]], (0, 96 * i))
        i -= 1

    # drawing the letter indexes

    i = 0
    layout = board.get_width_index()
    while i < 10:
        display.blit(index[layout[i]], (96 * i, 96 * (10 - 1)))
        i += 1

"""
Draws the gameplay elements (game pieces and turn indicators).

Args:
    board (Board): Game object containing information about the game state.
    display (Surface): Pygame object which represents the display itself.
    pieces (list): List containing game assets representing game pieces.
    misc (list): List containing game assets representing miscellaneous assets.
    turn (int): Indicates which player makes the next move.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
"""
def __draw_gameplay_elements(board, display, pieces, misc, turn, en_passant):
    # drawing the pieces
    layout = board.get_layout()
    i, j = 0, 0
    pieces_layout = board.get_pieces()
    for lines in layout:
        for fields in lines:
            display.blit(pieces[pieces_layout[i][j]], (j * 96, i * 96))
            j += 1
        i += 1
        j = 0

    # drawing player turn
    if not (is_in_check(turn, board.get_pieces(), en_passant)
            and len(get_all_possible_moves(board.get_pieces(), turn, en_passant)) == 0):
                display.blit(misc[turn], (0, 0))

    if is_in_check(turn, board.get_pieces(), en_passant):
        if len(get_all_possible_moves(board.get_pieces(), turn, en_passant)) == 0:
            display.blit(misc[4], (9 * 96, 0))
        else:
            display.blit(misc[3], (9 * 96, 0))

"""
Test function
Draws the movement matrix for a given piece.

Args:
    board (Board): Game object containing information about the game state.
    display (Surface): Pygame object which represents the display itself.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
"""
def __draw_matrix(board, display, en_passant):
    i, j = 0, 0
    game_board = board.get_pieces()
    layout = move_matrix(game_board, (8, 7), en_passant)
    for lines in layout:
        for fields in lines:
            if layout[i][j] == 1:
                color = (148, 255, 48)
                pygame.draw.rect(display, color, pygame.Rect((j * 96, i * 96), (96, 96)), 12)
            elif layout[i][j] == 2:
                color = (245, 237, 12)
                pygame.draw.rect(display, color, pygame.Rect((j * 96, i * 96), (96, 96)), 12)

            j += 1
        i += 1
        j = 0
