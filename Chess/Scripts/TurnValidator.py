import copy
from subprocess import list2cmdline

"""Checks if the player whose turn it is is in check"""
def is_in_check(turn, board, en_passant):
    king_pos = (0, 0)
    king = 0

    i, j = 0, 0
    for line in board:
        for cell in line:
            if cell == (turn * 6 + 6):
                king_pos = (i, j)
                king = cell

            j += 1
        i+= 1
        j = 0

    i, j = 0, 0
    for line in board:
        for cell in line:
            if not is_same_color(king, cell) and (cell % 6) != 0:
                if __checks(board, (i,j), king_pos, en_passant):
                    return True

            j += 1
        i += 1
        j = 0

    return False

"""Returns a list of all valid moves for all the pieces belonging to the player"""
def get_all_possible_moves(board, turn, en_passant):
    reference = 6 + 6 * turn
    moves = []

    i, j = 0, 0
    for line in board:
        for field in line:
            if field != 0 and is_same_color(reference, field):
                aux = get_all_valid_moves(board, turn, (i, j), en_passant)
                if len(aux) != 0:
                    moves.append(((i, j), aux))
            j += 1
        i += 1
        j = 0

    return moves

"""Returns a list of all valid moves for a given piece"""
def get_all_valid_moves(board, turn, piece_pos, en_passant):
    matrix = move_matrix(board, piece_pos, en_passant)
    moves = []

    i, j = 0, 0
    for line in matrix:
        for field in line:
            if field != 0:
                if is_valid_move(board, turn, piece_pos, (i, j), en_passant):
                    moves.append((i, j))

            j += 1
        i += 1
        j = 0

    return moves

"""Checks if a given move is valid."""
def is_valid_move(board, turn, piece_pos, target_pos, en_passant):
    matrix = move_matrix(board, piece_pos, en_passant)

    if matrix[target_pos[0]][target_pos[1]] == 0:
        return False # the piece cannot physically move there

    # simulate the move and see if it leads to the king being in check
    board_copy = copy.deepcopy(board)

    board_copy[target_pos[0]][target_pos[1]] = board_copy[piece_pos[0]][piece_pos[1]]
    board_copy[piece_pos[0]][piece_pos[1]] = 0

    if matrix[target_pos[0]][target_pos[1]] == 3:
        board_copy[target_pos[0] + 1][target_pos[1]] = 0

    if is_in_check(turn, board_copy, en_passant):
        return False

    return True


"""Given a coord on the board, checks if the given piece puts the enemy king in check"""
def __checks(board, piece_pos, king_pos, en_passant):
    matrix = move_matrix(board, piece_pos, en_passant)
    if matrix[king_pos[0]][king_pos[1]] != 0:
        return True

    return False

"""Given the coord of a piece on the board, checks all places a piece can move including by capturing"""
def move_matrix(board, piece_pos, en_passant):
    # initialise empty move matrix
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    #piece_pos = tuple(reversed(piece_pos))

    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    if piece == 0: # if there is no piece at the given coord
        return matrix

    if piece % 6 == 1: # if piece is a pawn
        matrix = __navigate_pawn(board, piece_pos, matrix, en_passant)

    if piece % 6 == 2: # if piece is a rook
        matrix = __navigate_rook(board, piece_pos, matrix)

    if piece % 6 == 3: # if piece is a knight
        matrix = __navigate_knight(board, piece_pos, matrix)

    if piece % 6 == 4: # if piece is a bishop
        matrix = __navigate_bishop(board, piece_pos, matrix)

    if piece % 6 == 5: # if piece is a queen
        matrix = __navigate_queen(board, piece_pos, matrix)

    """ to implement
    
    if piece % 6 == 6: #if piece is a king
        matrix = __navigate_king(board, piece_pos, matrix)
    """

    return matrix



"""Returns move matrix for a pawn at the given position"""
def __navigate_pawn(board, piece_pos, matrix, en_passant):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    if board[x - 1][y - 1] != 0 and not is_same_color(piece, board[x - 1][y - 1]):
        matrix[x - 1][y - 1] = 2

    if board[x - 1][y + 1] != 0 and not is_same_color(piece, board[x - 1][y + 1]):
        matrix[x - 1][y + 1] = 2

    target = board[x][y - 1]
    # if there is an enemy pawn to the left
    if x == 4 and target % 6 == 1 and not is_same_color(piece, target):
        if target < 7:
            turn = 0
        else:
            turn = 1

        if en_passant[turn][y - 1] == 1: # if en passant is possible
            matrix[x - 1][y - 1] = 3

    target = board[x][y + 1]
    # if there is an enemy pawn to the right
    if x == 4 and target % 6 == 1 and not is_same_color(piece, target):
        if target < 7:
            turn = 0
        else:
            turn = 1

        if en_passant[turn][y + 1] == 1:  # if en passant is possible
            matrix[x - 1][y + 1] = 3

    """to implement: pawn promotion"""

    if board[x - 1][y] == 0 and not __is_out_of_bounds((x - 1, y)):
        matrix[x- 1][y] = 1
    else:
        return matrix

    if x == 7 and board[x - 2][y] == 0:
        matrix[x - 2][y] = 1

    return matrix

"""Returns move matrix for a rook at the given position"""
def __navigate_rook(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    i = 1
    while not __is_out_of_bounds((x + i, y)):
        field = board[x + i][y]

        if field == 0:
            matrix[x + i][y] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x + i][y] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x - i, y)):
        field = board[x - i][y]

        if field == 0:
            matrix[x - i][y] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x - i][y] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x, y + i)):
        field = board[x][y + i]

        if field == 0:
            matrix[x][y + i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x][y + i] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x, y - i)):
        field = board[x][y - i]

        if field == 0:
            matrix[x][y - i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x][y - i] = 2
            break

        i += 1

    return matrix

"""Returns move matrix for a knight at the given position"""
def __navigate_knight(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    # all possible coords the horse can go
    target_x_y = [(x - 2, y - 1),
                  (x - 2, y + 1),
                  (x + 2, y - 1),
                  (x + 2, y + 1),
                  (x - 1, y - 2),
                  (x - 1, y + 2),
                  (x + 1, y - 2),
                  (x + 1, y + 2)]

    for field_x_y in target_x_y:
        if not __is_out_of_bounds((field_x_y[0], field_x_y[1])):
            field = board[field_x_y[0]][field_x_y[1]]

            if field == 0:
                matrix[field_x_y[0]][field_x_y[1]] = 1 # if it's empty I can go there
            elif not is_same_color(piece, field):
                matrix[field_x_y[0]][field_x_y[1]] = 2 # if it's a different color piece I can capture

    return matrix

"""Returns move matrix for a bishop at the given position"""
def __navigate_bishop(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    i = 1
    while not __is_out_of_bounds((x + i, y + i)):
        field = board[x + i][y + i]

        if field == 0:
            matrix[x + i][y + i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x + i][y + i] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x + i, y - i)):
        field = board[x + i][y - i]

        if field == 0:
            matrix[x + i][y - i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x + i][y - i] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x - i, y + i)):
        field = board[x - i][y + i]

        if field == 0:
            matrix[x - i][y + i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x - i][y + i] = 2
            break

        i += 1

    i = 1
    while not __is_out_of_bounds((x - i, y - i)):
        field = board[x - i][y - i]

        if field == 0:
            matrix[x - i][y - i] = 1
        elif is_same_color(piece, field):
            break
        else:
            matrix[x - i][y - i] = 2
            break

        i += 1

    return matrix

"""Returns move matrix for a queen at the given position"""
def __navigate_queen(board, piece_pos, matrix):
    matrix = __navigate_rook(board, piece_pos, matrix)
    matrix = __navigate_bishop(board, piece_pos, matrix)

    return matrix

"""Returns move matrix for a king at the given position"""
def __navigate_king(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    return matrix

"""Checks if two given pieces are of the same color"""
def is_same_color(piece_1, piece_2):
    if (piece_1 < 7 and piece_2 < 7) or (piece_1 >= 7 and piece_2 >= 7):
        return True

    return False

"""Determines if given coordinates are out of bounds"""
def __is_out_of_bounds(coord):
    x = coord[0]
    y = coord[1]

    if x > 8 or x < 1 or y > 8 or y < 1:
        return True

    return False