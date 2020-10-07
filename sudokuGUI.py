import pygame
import time
from sudokuSolver import solving, check_validation, empty_pos
from buttonClass import *
from protocol import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = BOARD
        self.temp_values = {} # Key : Value -> (x, y) : temp_val
        self.selected = None
        self.mouse_pos = None
        self.state = "playing"
        self.finished = False
        self.cell_changed = False
        self.playing_buttons = []
        self.menu_buttons = []
        self.end_buttons = []
        self.lock_cells = []
        self.errors = 0
        self.font = pygame.font.SysFont('comicsans', 40)
        solving(FINISHED_BOARD)
        self.load()


    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()


# Playing state functions # 

    # Function that responsible on the playing differen events
    # Input: Nothing
    # Output: Nothing
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # When the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()

                if selected:
                    self.selected = selected
                else:
                     self.selected = None
            
            # When the user type
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lock_cells: # Checking if the position is a blank rect
                    if self.is_int(event.unicode): # Checking if the user entered a number 
                        self.temp_values[(self.selected[0], self.selected[1])] =  int(event.unicode) # temp_values[(x, y)] = num
                    
                    elif event.key == pygame.K_BACKSPACE:
                        del self.temp_values[(self.selected[0], self.selected[1])]

                if event.key == pygame.K_KP_ENTER: 
                    pos = (self.selected[0], self.selected[1])
                    if FINISHED_BOARD[self.selected[1]][self.selected[0]] == self.temp_values[pos]: # Checking if the entered number is correct
                        self.grid[self.selected[1]][self.selected[0]] = self.temp_values[pos] # Adding to the board
                        self.lock_cells.append((pos[0], pos[1])) # Adding to the locked cell list
                        del self.temp_values[pos] # Delete the value from the temp_values list -> value became permenent
                        self.cell_changed = True
                    else: # Otherwise it is an error
                        self.errors += 1


    
    # Function that updates the game (by user's mouse position/clicking on buttons etc)
    # Input: Nothing
    # Output: Nothing
    def playing_update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.playing_buttons:
            button.update(self.mouse_pos)
        
        if self.cell_changed:
            if empty_pos(self.grid) is None:
                pass
                
                
    # Function that draw the game
    # Input: Nothing
    # Output: Nothing
    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected:
            self.draw_selection(self.window, self.selected)

        self.shade_locked_cells(self.window, self.lock_cells)
        self.draw_numbers(self.window)
        self.draw_errors(self.window, self.errors)
        
        self.draw_grid(self.window)
        pygame.display.update()
        pygame.display.set_caption('Sudoku')
        self.cell_changed = False


# Helper Functions #

    # Function that draws the numbers on the board
    # Input: window element
    # Output: Nothing
    def draw_numbers(self, window):
        # Drawing all the correct numbers on the board
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != UNASSIGNED:
                    pos = [(x_index * CELL_SIZE) + X_GRID, (y_index * CELL_SIZE) + Y_GRID] # Getting the numbers position
                    self.text_to_screen(self.window, str(num), pos, 1) # Drawing the numbers

                    # Deleting from the dict the values of the guessing so only the correct ans will apear on the screen
                    if (x_index, y_index) in self.temp_values:
                        del self.temp_values[(x_index, y_index)]
        
        # Drawing the user's guessing
        for x_index, y_index in self.temp_values:
            pos = [(x_index * CELL_SIZE) + X_GRID, (y_index * CELL_SIZE) + Y_GRID]
            self.text_to_screen(self.window, str(self.temp_values[x_index, y_index]), pos, 2)


    # Function that draws the number of errors the user have
    # Input: The function gets the window element and the number of errors the user have
    # Output: Nothing
    def draw_errors(self, window, errors):
        x_font = pygame.font.SysFont('comicsans', 30)
        font = x_font.render('X', False, RED)
        pos = [0,0]
        for i in range(0, errors):
            pos[0] = WIDTH - 515 + (i * 20)
            pos[1] = HEIGHT - 40
            window.blit(font, pos)
            

    # Function that draws in light blue the selection cell
    # Input: window element and the selected position
    # Output: Nothing
    def draw_selection(self, window, selected : list):
        pygame.draw.rect(window, LIGHTBLUE, ((self.selected[0] * CELL_SIZE) + X_GRID, (self.selected[1] * CELL_SIZE) + Y_GRID, CELL_SIZE, CELL_SIZE))


    # Function that draws the grid on the window
    # Input: The window to draw on
    # Output: Nothing
    def draw_grid(self, window):
        pygame.draw.rect(window, BLACK, (X_GRID, Y_GRID, WIDTH - X_GRID*2, HEIGHT - 150), THICKNESS)
        for x in range(1, BOARD_SIZE + 1):
            pygame.draw.line(window, BLACK, (X_GRID+(x*CELL_SIZE), Y_GRID), (X_GRID+(x*CELL_SIZE), 550), THICKNESS if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (X_GRID, Y_GRID + (x*CELL_SIZE)), (WIDTH-X_GRID, Y_GRID + (x*CELL_SIZE)), THICKNESS if x % 3 == 0 else 1)


    # Function that returns true if the mouse clicked on the grid, false otherwise
    # Input: Nothing
    # Output: True or False
    def mouse_on_grid(self) -> bool:
        # Check if the mouse pressed outside the grid lines (left && up)
        if self.mouse_pos[0] < X_GRID or self.mouse_pos[1] < Y_GRID:
            return False
        
        # Check if the mouse pressed outside the grid lines (right && down)
        if self.mouse_pos[0] > (X_GRID + GRID_SIZE) or self.mouse_pos[1] > (Y_GRID + GRID_SIZE): 
            return False
        
        # Returnning the position of the mouse on the board
        return ((self.mouse_pos[0] - X_GRID) // CELL_SIZE, (self.mouse_pos[1] - Y_GRID) // CELL_SIZE)


    # Function that loads information on the screen (buttons/locked numbers etc)
    # Input: Nothing
    # Output: Nothing
    def load(self):
        self.load_buttons()

        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != UNASSIGNED:
                    self.lock_cells.append([x_index, y_index]) # Locking the numbers


    # Function that loads all the buttons on the board
    # Input: Nothing
    # Output: Nothing
    def load_buttons(self):
        self.playing_buttons.append(Button(20, 40, 100, 40))


    # Function that puts the numbers on the screen
    # Input: Window element, text string and position to put the text in and option (1 - correct ans, 2 - pencil option)
    # Output: Nothing
    def text_to_screen(self, window, text : str, pos : list, option : int):
        font = self.font.render(text, False, BLACK if option == 1 else PENCIL_GRAY)
        font_height = font.get_height()
        font_width = font.get_width()
        pos[0] += (CELL_SIZE - font_width) // 2
        pos[1] += (CELL_SIZE - font_height) // 2
        window.blit(font, pos)


    # Function that shades the permenent cells on the board
    # Input: The window element and a list of cells to lock
    # Output: Nothing.
    def shade_locked_cells(self, window, lock_cells : list):
        for cell in lock_cells:
            pygame.draw.rect(window, GRAY, (cell[0] * CELL_SIZE + X_GRID, cell[1] * CELL_SIZE + Y_GRID, CELL_SIZE, CELL_SIZE))


    # Function that checks if the number is an integer
    # Input: string
    # Output: True if the number is a string, False otherwise
    def is_int(self, string : str) -> bool: 
        try:
            int(string)
            return True
        except:
            return False


# Function that solves the sudoku #

    # Recursive function that solve the sudoku backtracking
    # Input: List of the sudoku board
    # Output: True if we finished the sudoku, False if need to change previous values
    def solved_gui(self):
        self.window.fill(WHITE)

        for button in self.playing_buttons:
            button.draw(self.window)

        self.shade_locked_cells(self.window, self.lock_cells)
        self.draw_grid(self.window)
        pygame.display.update()
        pygame.display.set_caption('Sudoku')

        find = empty_pos(self.grid)
        if not find:
            return True
        else: 
            row, col = find

        for i in range (1, BOARD_SIZE):
            if check_validation(self.grid, (row, col), i):
                self.grid[row][col] = i
                self.draw_numbers(self.window)
                pygame.delay(100)
            
                if self.solved_gui():
                    return True
            
            self.grid[row][col] = 0
            self.draw_numbers(self.window)
            pygame.delay(100)
        
        return False
            