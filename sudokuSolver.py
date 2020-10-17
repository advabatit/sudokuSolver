# Adding this line for the PR
from protocol import BOARD_SIZE 
from protocol import UNASSIGNED

# Function that prints the board
# Input: List of the sudoku board
# Output: The board on the screen. The function doesn't returning anything.
def print_board(sudoku_board : list):
    for rows in sudoku_board:
        for cols in rows:
            print(cols, end=' ')
        print()


# Function that finds an empty position on the board
# Input: List of the sudoku board
# Output: A tuple of the position, none otherwise 
def empty_pos(sudoku_board : list) -> tuple:
    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if sudoku_board[i][k] == UNASSIGNED:
                return (i ,  k) # (Row, Col)
    return None # Meaning there is no empty position, we finished the sudoku


# Function that checks the validation of the number in the row/column/box
# Input: List of the sudoku board, position tuple of the empty place and the int we want to check
# Output: True if it is a valid number, False otherwise
def check_validation(sudoku_board : list, position : tuple, num : int) -> bool:
    row, col = position
    position = (position[0], position[1])

    # Check Row
    for i in range(BOARD_SIZE):
        if sudoku_board[row][i] == num and (row, i) != position:
            return False

    # Check column
    for i in range(BOARD_SIZE):
        if sudoku_board[i][col] == num and (i, col) != position:
            return False

    # Check Box
    row = row // 3
    col = col // 3

    for i in range(row * 3, row * 3 + 3):
        for k in range (col * 3, col * 3 + 3):
            if sudoku_board[i][k] == num and (i, k) != position:
                return False
 
    return True


# Recursive function that solve the sudoku backtracking
# Input: List of the sudoku board
# Output: True if we finished the sudoku, False if need to change previous values
def solving(sudoku_board : list) -> bool:
    find_empty = empty_pos(sudoku_board)
    if not find_empty:
        return True
    else:
        row, col = find_empty
    
    for i in range(1, BOARD_SIZE+1):
        if(check_validation(sudoku_board, (row, col), i)):
            sudoku_board[row][col] = i

            if(solving(sudoku_board)):
                return True
            
            sudoku_board[row][col] = 0
    
    return False