import pygame
import Sudoku_noGUI

pygame.init()

# Colours in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
purple = (90, 24, 154)
mauve = (224, 170, 255)
red = (154, 3, 30)

# Constants
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 700
gap = WINDOW_WIDTH // 9
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku Solver")
number_font = pygame.font.SysFont("comicsans", 45)
text_font = pygame.font.SysFont('comicsans', 25)


class Board(object):

    def __init__(self, board):
        """
        Constructor for our main class
        :param board: 2D list representing our sudoku board
        """
        # Original board
        self.board = board
        # Solution
        self.solution = [[board[i][j] for j in range(9)] for i in range(9)]
        Sudoku_noGUI.solve(self.solution)

        # Copy of our board that will remain unchanged
        self.board_copy = [[self.board[i][j] for j in range(9)] for i in range(9)]
        # 9x9 list of cells.
        self.cells = [[Cell(i, j, board[i][j]) for j in range(9)] for i in range(9)]
        # Row of the selected cell
        self.selected_row = -1
        # Column of the selected cell
        self.selected_col = -1

    @staticmethod
    def draw_thicker_lines():
        """
        Method to draw thick column and row lines
        :return: None
        """
        for i in range(4):
            pygame.draw.line(window, black, (0, 3 * i * gap), (WINDOW_WIDTH, 3 * i * gap), 3)
            pygame.draw.line(window, black, (3 * i * gap, 0), (3 * i * gap, WINDOW_WIDTH), 3)

    def draw(self):
        """
        Method to draw the whole sudoku board.
        :return: None
        """
        for i in range(9):
            for j in range(9):
                sq = self.cells[i][j]
                # Cells with fixed value have a colour in them to indicate that they are fixed.
                color = mauve if (self.board_copy[i][j] != 0) else white
                sq.draw_square(color)
        self.draw_thicker_lines()

    def change_selected(self, pos):
        """
        Method to change the selected cell
        :param pos:
        :return: None
        """
        if pos[0] // gap > 8 or pos[1] // gap > 8:
            return
        self.selected_col = pos[0] // gap
        self.selected_row = pos[1] // gap

    def checkIfValid(self, row, col, num):
        """
        Return True if num can be placed at board[row][col] according to sudoku rules
        :param row: row of the cell
        :param col: column of the cell
        :param num: value of the cell
        :return: bool
        """

        # Check columns
        for j in range(9):
            if self.board[row][j] == num and j != col:
                return False
        # Check rows
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        # Check box
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and row != i and col != j:
                    return False

        return True

    def update(self, row, col, num):
        """
        Update the screen with the updated cell
        :param row: row of the updated cell
        :param col: column of the updated cell
        :param num: updated value
        :return: None
        """
        window.fill(white)
        self.board[row][col] = num
        self.cells[row][col].setVal(num)
        self.draw()
        Cell.draw_lines(red, col * gap, row * gap, 4)
        pygame.display.update()
        pygame.time.delay(70)

    def solve(self):
        """
        solves the sudoku board using backtracking
        :return:
        """
        # Find the first empty position in the board
        row, col = self.find_empty()
        # if board is full, return True
        if row == -1:
            return True
        # pygame.event.pump()
        for i in range(1, 10):
            # Check if i can be filled in board[row][col]
            if self.checkIfValid(row, col, i):
                # Uncomment the next two lines and comment the third if board is taking too long to solve
                # self.board[row][col] = i
                # self.cells[row][col].setVal(i)
                self.update(row, col, i)
                if self.solve():
                    return True
                # Uncomment the next two lines and comment the third if board is taking too long to solve
                # self.board[row][col] = 0
                # self.cells[row][col].setVal(0)
                self.update(row, col, 0)
        return False

    def find_empty(self):
        """
        Find the first empty position in board
        :return: (int, int)
        """
        for j in range(9):
            for i in range(9):
                if self.board[i][j] == 0:
                    return i, j

        return -1, -1


class Cell(object):

    def __init__(self, row, col, val):
        """
        Each cell is represented by a row, col and it's value
        :param row: row of the cell
        :param col: column of the cell
        :param val: value of the cell
        """
        self.row = row
        self.col = col
        self.val = val

    @staticmethod
    def draw_lines(colour, x, y, thick=1):
        """
        Draw four lines around a cell
        :param colour: colour of the lines
        :param x: x-coordinate of top-left of cell
        :param y: y-coordinate of top-left of cell
        :param thick: thickness of lines
        :return: None
        """
        pygame.draw.line(window, colour, (x, y), (x + gap, y), thick)
        pygame.draw.line(window, colour, (x, y), (x, y + gap), thick)
        pygame.draw.line(window, colour, (x, y + gap), (x + gap, y + gap), thick)
        pygame.draw.line(window, colour, (x + gap, y), (x + gap, y + gap), thick)

    def draw_square(self, colour):
        """
        Draw the cell, place the number inside it and fill it with colour
        :param colour: colour of cell
        :return: None
        """
        x = self.col * gap
        y = self.row * gap
        self.draw_lines(black, x, y)
        if self.val != 0:
            box = pygame.Rect(x + 1.8, y + 1.8, gap - 1, gap - 1)
            pygame.draw.rect(window, colour, box)
            number = number_font.render(str(self.val), True, black)
            window.blit(number, (x + 20, y + 20))

    def getVal(self):
        """
        Get the value of the cell
        :return: int
        """
        return self.val

    def setVal(self, num):
        """
        Set the value of the cell to num
        :param num:
        :return: None
        """
        self.val = num


def instructions(colour, count):
    """
    Render instruction on bottom of screen
    :param colour: colour of instructions
    :return: None
    """

    m1 = number_font.render("Welcome to Sudoku!", True, colour)
    window.blit(m1, (10, 550))
    m2 = text_font.render("Press R to reset.", True, colour)
    window.blit(m2, (10, 590))
    m3 = text_font.render("Press D to delete.", True, colour)
    window.blit(m3, (10, 610))
    m4 = text_font.render("Press SpaceBar to solve.", True, colour)
    window.blit(m4, (10, 630))

    if count > 0:
        s = "Press H for hint. {} hints remaining".format(count)
    else:
        s = "No hints remaining. You are on your own soldier."

    m6 = text_font.render(s, True, colour)
    window.blit(m6, (10, 650))
    m5 = text_font.render("Created By : Siddharth Mittal", True, colour)
    window.blit(m5, (10, 680))


def invalid_move_error(colour):
    """
    Render error message on screen if user inputs an invalid move
    :param colour: colour of text
    :return: None
    """
    m1 = number_font.render("Invalid Move. Try Again", True, colour)
    window.blit(m1, (10, 550))


def game_over(colour):
    m1 = number_font.render("Game over!", True, colour)
    window.blit(m1, (10, 550))
    m2 = number_font.render("Press R to reset.", True, colour)
    window.blit(m2, (10, 600))

def invalid_board_error(colour):
    """
    Render error message on screen if board is unsolvable or becomes unsolvable after user inputs.
    :param colour: colour of text
    :return: None
    """
    m1 = number_font.render("Can't be solved.", True, colour)
    window.blit(m1, (10, 550))
    m2 = text_font.render("Reset and Try Again", True, colour)
    window.blit(m2, (10, 600))
    m3 = text_font.render("OR", True, colour)
    window.blit(m3, (10, 620))
    m4 = text_font.render("Change Board.", True, black)
    window.blit(m4, (10, 640))


def start():
    # Change the next line to change board

    board = [
        [0, 4, 9, 3, 0, 0, 0, 5, 7],
        [5, 0, 0, 7, 6, 0, 9, 0, 0],
        [0, 2, 7, 0, 5, 0, 6, 1, 0],
        [0, 9, 0, 0, 1, 7, 0, 0, 2],
        [2, 1, 8, 0, 0, 0, 0, 4, 0],
        [0, 0, 3, 0, 2, 0, 0, 0, 6],
        [0, 0, 0, 0, 4, 5, 3, 7, 0],
        [0, 0, 4, 0, 9, 0, 0, 0, 1],
        [1, 8, 0, 6, 7, 3, 0, 0, 9]
    ]

    game = Board(board)
    buttons = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7,
               pygame.K_8: 8, pygame.K_9: 9}
    run = True
    solve = False
    sel = False
    delete = False
    reset = False
    val = -1
    invalid_move = False
    invalid_board = False
    hint = False
    hint_count = 5
    over = False

    while run:
        window.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.change_selected(pygame.mouse.get_pos())
                sel = True

            if event.type == pygame.KEYDOWN:
                e = event.key
                if e in buttons.keys():
                    val = buttons[e]

                solve = (e == pygame.K_SPACE)
                delete = (e == pygame.K_d)
                reset = (e == pygame.K_r)
                hint = (e == pygame.K_h)

        r = game.selected_row
        c = game.selected_col

        if hint and hint_count > 0:
            if game.board_copy[r][c] == 0 and game.board[r][c] == 0:
                game.update(r, c, game.solution[r][c])
                hint_count -= 1
            hint = False

        if reset:
            game.board = [[game.board_copy[i][j] for j in range(9)] for i in range(9)]
            for i in range(9):
                for j in range(9):
                    # game.update(i, j, game.board[i][j])
                    game.cells[i][j].setVal(game.board[i][j])
            reset = False
            hint_count = 5
            invalid_board = False
            invalid_move = False
            over = False

        if delete:
            if game.board_copy[r][c] == 0:
                game.update(r, c, 0)
            delete = False
            invalid_board = False

        if val != -1:
            if game.checkIfValid(r, c, val) and game.board_copy[r][c] == 0:
                game.update(r, c, val)
                invalid_move = False
            else:
                invalid_move = True
            val = -1

        if solve:
            solve = False
            if not game.solve():
                invalid_board = True
            else:
                invalid_board = False

        if Sudoku_noGUI.findEmptyPosition(game.board)[-1] == -1:
            over = True

        game.draw()
        if sel:
            Cell.draw_lines(red, c * gap, r * gap, 4)
        if over:
            game_over(black)
        elif invalid_move or invalid_board:
            if invalid_move:
                invalid_move_error(black)
            else:
                invalid_board_error(black)
        else:
            instructions(black, hint_count)
        pygame.display.update()

    pygame.quit()


start()
