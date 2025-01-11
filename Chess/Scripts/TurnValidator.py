import copy

"""Script for handling all move validation"""

"""
Checks if the player whose turn it is is in check.

Args:
    turn (int): Indicates which player makes the next move.
    board (list): Matrix which contains the layout of the game pieces.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    bool: If the player is in check or not.
"""
def is_in_check(turn, board, en_passant):
    king_pos = (0, 0)
    king = 0
    matrix = __non_destructive_flip(board)

    # get the position of the king
    i, j = 0, 0
    for line in matrix:
        for cell in line:
            if cell == (turn * 6 + 6):
                king_pos = (i, j)
                king = cell

            j += 1
        i+= 1
        j = 0

    # for each enemy piece, check if it puts the king in check
    i, j = 0, 0
    for line in matrix:
        for cell in line:
            if not is_same_color(king, cell) and (cell % 6) != 0:
                if __checks(matrix, (i,j), king_pos, en_passant):
                    return True

            j += 1
        i += 1
        j = 0

    return False

"""
Function for safely rotating a matrix 180 degrees

Args:
    matrix (list): The matrix.
    
Returns:
    list: The rotated matrix.
"""
def __non_destructive_flip(matrix):
    board_copy = copy.deepcopy(matrix)
    board_copy = list(zip(*board_copy[::-1]))
    board_copy = list(zip(*board_copy[::-1]))

    return [list(row) for row in board_copy]

"""
Returns a list of all valid moves for all the pieces belonging to the player.

Args:
    turn (int): Indicates which player makes the next move.
    board (list): Matrix which contains the layout of the game pieces.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    list: All possible moves a player can make.
"""
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

"""
Returns a list of all valid moves for a given piece.

Args:
    turn (int): Indicates which player makes the next move.
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    list: All possible moves the piece can make.
"""
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

"""
Checks if a given move is valid.

Args:
    turn (int): Indicates which player makes the next move.
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    target_pos (tuple): The place where the piece is supposed to move.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    bool: If the move is valid.
"""
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


"""
Given a coord on the board, checks if the given piece puts the enemy king in check.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    king_pos (tuple): The position of the king.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    bool: If the given piece puts the king in check.
"""
def __checks(board, piece_pos, king_pos, en_passant):
    matrix = move_matrix(board, piece_pos, en_passant)
    if matrix[king_pos[0]][king_pos[1]] != 0:
        return True

    return False

"""
Given the coord of a piece on the board, checks all places a piece can move including by capturing.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    list: Movement matrix of the given piece.
"""
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
    
    if piece % 6 == 0 and piece != 0: #if piece is a king
        matrix = __navigate_king(board, piece_pos, matrix, en_passant)

    return matrix



"""
Returns move matrix for a pawn at the given position

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    list: Movement matrix of the pawn.
"""
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

    if x == 1: # pawn promotion
        matrix[x - 1][y] = 1
        return matrix

    if board[x - 1][y] == 0 and not __is_out_of_bounds((x - 1, y)):
        matrix[x- 1][y] = 1
    else:
        return matrix

    if x == 7 and board[x - 2][y] == 0:
        matrix[x - 2][y] = 1

    return matrix

"""
Returns move matrix for a rook at the given position.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    
Returns:
    list: Movement matrix of the rook.
"""
def __navigate_rook(board, piece_pos, matrix):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    # could have been implemented in a cleaner way

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

"""
Returns move matrix for a knight at the given position.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    
Returns:
    list: Movement matrix of the knight.
"""
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

"""
Returns move matrix for a bishop at the given position.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    
Returns:
    list: Movement matrix of the bishop.
"""
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

"""
Returns move matrix for a queen at the given position.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    
Returns:
    list: Movement matrix of the queen.
"""
def __navigate_queen(board, piece_pos, matrix):
    matrix = __navigate_rook(board, piece_pos, matrix)
    matrix = __navigate_bishop(board, piece_pos, matrix)

    return matrix

"""
Returns move matrix for a king at the given position

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    matrix (list): The already initialised empty move matrix.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    list: Movement matrix of the king.
"""
def __navigate_king(board, piece_pos, matrix, en_passant):
    x = piece_pos[0]
    y = piece_pos[1]
    piece = board[x][y]

    proximity_matrix = [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]]

    # check all fields in the proximity of the king
    for line in proximity_matrix:
        i = piece_pos[0] + line[0]
        j = piece_pos[1] + line[1]

        if (not __is_out_of_bounds((i, j))
            and not __enemy_king_in_proximity(board, piece, (i,j), proximity_matrix)):

            field = board[i][j]
            if field == 0:
                matrix[i][j] = 1
            elif not is_same_color(piece, field):
                matrix[i][j] = 2

    if __can_castle_right(board, piece_pos, en_passant):
        matrix[x][y + 2] = 1

    if __can_castle_left(board, piece_pos, en_passant):
        matrix[x][y - 2] = 1

    return matrix

"""
Determines if king can castle on the right side.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    bool: If the king can castle on the right side.
"""
def __can_castle_right(board, piece_pos, en_passant):
    if board[piece_pos[0]][piece_pos[1]] < 7:
        turn = 0
    else:
        turn = 1

    # if either the king or rook have moved
    if en_passant[turn][9] != 0:
        return False

    # check if the spaces between the king and rook are empty
    i = piece_pos[1] + 1
    while i < 8:
        if board[8][i] != 0:
            return False

        i += 1

    # check if any of the spaces the king traverses are attacked
    i = piece_pos[1]
    while i <= piece_pos[1] + 2:
        board_copy = copy.deepcopy(board)
        board_copy[piece_pos[0]][i] = 6
        board_copy[piece_pos[0]][piece_pos[1]] = 0
        if is_in_check(turn, board_copy, en_passant):
            return False

        i += 1

    return True

"""
Determines if king can castle on the left side.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    piece_pos (tuple): The position of a piece on the board.
    en_passant (list): Matrix with 2 lines, each keeping track of where en_passant and castling can be performed.
    
Returns:
    bool: If the king can castle on the left side.
"""
def __can_castle_left(board, piece_pos, en_passant):
    if board[piece_pos[0]][piece_pos[1]] < 7:
        turn = 0
    else:
        turn = 1

    # if either the king or rook have moved
    if en_passant[turn][0] != 0:
        return False

    # check if the spaces between the king and rook are empty
    i = piece_pos[1] - 1
    while i > 1:
        if board[8][i] != 0:
            return False

        i -= 1

    # check if any of the spaces the king traverses are attacked
    i = piece_pos[1]
    while i >= piece_pos[1] - 2:
        board_copy = copy.deepcopy(board)
        board_copy[piece_pos[0]][i] = 6
        board_copy[piece_pos[0]][piece_pos[1]] = 0
        if is_in_check(turn, board_copy, en_passant):
            return False

        i -= 1

    return True

"""
Determines if the enemy king is in the proximity of a given field.

Args:
    board (list): Matrix which contains the layout of the game pieces.
    king (int): Value of the king piece.
    pos (tuple): A field on the board.
    proximity_matrix (list): Movement matrix for going around the given field.
    
Returns:
    bool: If the enemy king is in the proximity of the given field.
"""
def __enemy_king_in_proximity(board, king ,pos, proximity_matrix):

    # go around the given field
    for line in proximity_matrix:
        # this function is never called on an out-of-bounds field so this is fine
        field = board[pos[0] + line[0]][pos[1] + line[1]]

        # if we find the enemy king
        if field != 0 and field % 6 == 0 and not is_same_color(king, field):
            return True
    # we haven't found the enemy king in any of the surrounding fields
    return False

"""
Checks if two given pieces are of the same color.

Args:
    piece_1 (int): Value of a given piece.
    piece_2 (int): Value of another given peice.
    
Returns:
    bool: If the pieces are the same color.
"""
def is_same_color(piece_1, piece_2):
    if (piece_1 < 7 and piece_2 < 7) or (piece_1 >= 7 and piece_2 >= 7):
        return True

    return False

"""
Determines if given coordinates are out of bounds.

Args:
    coord (tuple): Coordinates on or off the game board.
    
Returns:
    bool: If the given coordinates are within the bounds of the game board.
"""
def __is_out_of_bounds(coord):
    x = coord[0]
    y = coord[1]

    if x > 8 or x < 1 or y > 8 or y < 1:
        return True

    return False