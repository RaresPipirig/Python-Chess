
"""Checks if the player whose turn it is is in check"""
def is_in_check(turn, board):
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
            if not __is_same_color(king, cell) and (cell % 6) != 0:
                if __checks(board, (i,j), king_pos):
                    return True

            j += 1
        i += 1
        j = 0

    return False


"""Given a coord on the board, checks if the given piece puts the enemy king in check"""
def __checks(board, piece_pos, king_pos):
    matrix = __move_matrix(board, piece_pos)
    if matrix[king_pos[0]][king_pos[1]] != 0:
        return True

    return False

"""Given the coord of a piece on the board, checks all places a piece can move including by capturing"""
def __move_matrix(board, piece_pos):
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
        matrix = __navigate_pawn(board, piece_pos, matrix)

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
def __navigate_pawn(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    if board[x - 1][y - 1] != 0 and not __is_same_color(piece, board[x - 1][y - 1]):
        matrix[x - 1][y - 1] = 2

    if board[x - 1][y + 1] != 0 and not __is_same_color(piece, board[x - 1][y + 1]):
        matrix[x - 1][y + 1] = 2

    """to implement: en passant"""

    if board[x - 1][y] == 0:
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
            elif not __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
        elif __is_same_color(piece, field):
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
def __is_same_color(piece_1, piece_2):
    if (piece_1 < 7 and piece_2 < 7) or (piece_1 > 7 and piece_2 > 7):
        return True

    return False

"""Determines if given coordinates are out of bounds"""
def __is_out_of_bounds(coord):
    x = coord[0]
    y = coord[1]

    if x > 8 or x < 1 or y > 8 or y < 1:
        return True

    return False