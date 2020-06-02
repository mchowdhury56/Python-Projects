def solve(board):
    found_cell = find_empty(board)
    # Search the table for any empty cells if none found then everything is done
    if not found_cell:
        return True
    else:
        row, col = found_cell

    for i in range(1, 10):
        # insert numbers 1-9 into board one at a time until reaching condition
        if valid(board, i, (row, col)):
            board[row][col] = i
            # check if the board can be solved after the insertion
            if solve(board):
                return True
            # otherwise set cell value back to 0 and continue next iteration
            board[row][col] = 0

    return False


def valid(board, num, pos):
    """Checks if the board is valid after inserting a number into a certain position"""
    for col in range(len(board[0])):  # Check row
        # check every other position in the row does not have the same value you just inserted
        if board[pos[0]][col] == num and pos[1] != col:
            return False

    for row in range(len(board)):  # Check column
        if board[row][pos[1]] == num and pos[0] != row:
            return False

    # Find which 3x3 box currently in
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    # check each cell of the box
    for col in range(box_y*3, box_y*3 + 3):
        for row in range(box_x * 3, box_x*3 + 3):
            if board[col][row] == num and (col, row) != pos:
                return False

    return True


def print_board(board):
    for row in range(len(board)):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - - - ")
        for col in range(len(board[0])):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")

            if col == 8:
                print(board[row][col])
            else:
                print(str(board[row][col]) + " ", end="")


def find_empty(board):
    """Searches for an empty cell in the board and returns it if there is one"""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None


