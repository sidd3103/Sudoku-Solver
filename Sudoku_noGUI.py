BOARD_LENGTH = 9


def solve(matrix):
    """
    Solve sudoku using backtracking. Return True if solvable board
    :param matrix: 2D list of integers representing board
    :return: bool
    """
    (row, col) = findEmptyPosition(matrix)

    if row == -1 and col == -1:
        return True

    for i in range(1, 10):
        if checkIfValid(matrix, row, col, i):
            matrix[row][col] = i
            if solve(matrix):
                return True
            matrix[row][col] = 0

    return False


def checkIfValid(matrix, row, col, num):
    """
    Return True if num can be placed at board[row][col] according to sudoku rules
    :param row: row of the cell
    :param col: column of the cell
    :param num: value of the cell
    :return: bool
    """
    for j in range(BOARD_LENGTH):
        if matrix[row][j] == num and j != col:
            return False

    for i in range(BOARD_LENGTH):
        if matrix[i][col] == num and i != row:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if matrix[i][j] == num and row != i and col != j:
                return False

    return True


def findEmptyPosition(matrix):
    """
    Find the first empty position in board
    :return: (int, int)
    """
    for j in range(BOARD_LENGTH):
        for i in range(BOARD_LENGTH):
            if matrix[i][j] == 0:
                return i, j

    return -1, -1

