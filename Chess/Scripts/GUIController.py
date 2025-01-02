import pygame
from Scripts.TurnValidator import move_matrix, is_in_check, is_valid_move, get_all_valid_moves, get_all_possible_moves

"""Functions for handling all GUI operations"""

"""Sets up the display window upon opening the game"""
def setup_display():
    pygame.init()
    display = pygame.display.set_mode((960,960))
    clock = pygame.time.Clock()
    FPS = 60
    return display, clock, FPS

"""Loads the images into objects and adjusts the scale"""
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
        3 : pygame.transform.scale(pygame.image.load("Assets/check.png"), (96,960))
    }

    return pieces, index, misc

"""Draws the game board upon being given a game state"""
def draw_board(pieces, index, misc, display, board, turn, mouse_pos, selected):
    __draw_game_board(board, display, index)
    __draw_gameplay_elements(board, display, pieces, misc, turn)
    __draw_mouse_interaction(board, display, turn, mouse_pos, selected)

    """tests"""
    #__draw_matrix(board, display)
    #print(is_valid_move(board.get_pieces(), turn, (7, 5), (5, 6)))
    #print(get_all_valid_moves(board.get_pieces(), turn, (8, 2)))
    #print(get_all_possible_moves(board.get_pieces(), turn))

"""Makes the GUI interactive with the mouse"""
def __draw_mouse_interaction(board, display, turn, mouse_pos, selected):
    pass


"""Draws the chess board itself"""
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

"""Draws the gameplay elements:
Chess pieces
Turn indicator
"""
def __draw_gameplay_elements(board, display, pieces, misc, turn):
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
    display.blit(misc[turn], (0, 0))

    if is_in_check(turn, board.get_flipped_board()):
        display.blit(misc[3], (9 * 96, 0))

"""Test function"""
def __draw_matrix(board, display):
    i, j = 0, 0
    game_board = board.get_pieces()
    layout = move_matrix(game_board, (8, 7))
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
