import pygame
import time
from random import seed, randint
from sudokuSolver import solving, check_validation, empty_pos
from buttonClass import *
from protocol import *


class App:
    def __init__(self):
        seed(1)
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = BOARD
        self.temp_values = {} # Key : Value -> (x, y) : temp_val
        self.selected = None
        self.mouse_pos = None
        self.state = "playing"
        self.caption = "Sudoku"
        self.screen_text = ""
        self.finished = False
        self.cell_changed = False
        self.error_msg = False
        self.playing_buttons = []
        self.menu_buttons = []
        self.lock_cells = []
        self.errors = 0
        self.hints = 3
        self.font = pygame.font.SysFont('comicsans', 40)
        solving(FINISHED_BOARD)
        self.load()


    def run(self):
        while self.running:
            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.state == 'win' or self.state == 'lose':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
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
                if self.mouse_pos:
                    self.error_msg = False
                    selected = self.mouse_on_grid()

                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playing_buttons:
                        if button.highlighted:
                            button.click()

            
            
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
                self.state = 'win'
                self.screen_text = 'You Win'
                self.caption = 'Sudoku - Win screen'
                self.game_over_draw()
                
                
                
    # Function that draw the game
    # Input: Nothing
    # Output: Nothing
    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected: # Checking if there is a place that the user select
            self.draw_selection(self.window, self.selected)

        self.shade_locked_cells(self.window, self.lock_cells)
        self.draw_permenent_numbers(self.window)
        self.draw_user_numbers(self.window)
        self.draw_errors(self.window, self.errors)

        if self.error_msg:
            self.draw_error_msg()

        self.draw_grid(self.window)
        pygame.display.update()
        pygame.display.set_caption(self.caption)
        self.cell_changed = False

        if self.errors == 5:
            self.state = 'lose'
            self.screen_text = 'Game Over'
            self.caption = 'Sudoku - Game over'
            self.game_over_draw()


# Helper Functions #

    # Function that draws the numbers on the board
    # Input: window element
    # Output: Nothing
    def draw_permenent_numbers(self, window):
        # Drawing all the correct numbers on the board
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != UNASSIGNED:
                    pos = [(x_index * CELL_SIZE) + X_GRID, (y_index * CELL_SIZE) + Y_GRID] # Getting the numbers position
                    self.text_to_screen(self.window, str(num), pos, 1) # Drawing the numbers

                    # Deleting from the dict the values of the guessing so only the correct ans will apear on the screen
                    if (x_index, y_index) in self.temp_values:
                        del self.temp_values[(x_index, y_index)]
        

    # Function that draws the numbers of the user on the board
    # Input: window element
    # Output: Nothing        
    def draw_user_numbers(self, window):
        # Drawing the user's guessing
        for x_index, y_index in self.temp_values:
            pos = [(x_index * CELL_SIZE) + X_GRID, (y_index * CELL_SIZE) + Y_GRID]
            self.text_to_screen(self.window, str(self.temp_values[x_index, y_index]), pos, 2)


    # Function that draws the number of errors the user have
    # Input: The function gets the window element and the number of errors the user have
    # Output: Nothing
    def draw_errors(self, window, errors : int):
        x_font = pygame.font.SysFont('comicsans', 30)
        font = x_font.render('X', False, RED)
        pos = [0,0]
        for i in range(0, errors):
            pos[0] = WIDTH - 170 + (i * 20)
            pos[1] = HEIGHT - 520
            window.blit(font, pos)


    # Function that prints to the screen that the user ended all his 3 hints
    # Input: Nothing
    # Output: Nothing
    def draw_error_msg(self):
        pos = [0,0]
        error_font = pygame.font.SysFont('comicsans', 50)
        font = error_font.render('No more hints for you!', False, RED)
        pos[0] = WIDTH - 490
        pos[1] = HEIGHT - 40
        self.window.blit(font, pos)


    # Function that draws in light blue the selection cell
    # Input: window element and the selected position
    # Output: Nothing
    def draw_selection(self, window, selected : list):
        pygame.draw.rect(window, PINK, ((selected[0] * CELL_SIZE) + X_GRID, (selected[1] * CELL_SIZE) + Y_GRID, CELL_SIZE, CELL_SIZE))


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


    # Function that loads all the buttons of the board
    # Input: Nothing
    # Output: Nothing
    def load_buttons(self):
        self.playing_buttons.append(Button(20, 40, 100, 40,
                                            function = self.solved_gui,
                                            text = "Solve" ))
        
        self.playing_buttons.append(Button(140, 40, 100, 40, 
                                            function  = self.hint,
                                            text = "Hint" ))

        # MENU BUTTONS
        self.menu_buttons.append(Button(150, 350, 120, 60,
                                            function = self.exit_game,
                                            colour = WHITE,
                                            highlighted_colour = PENCIL_GRAY,
                                            text = "Exit" ))
        
        self.menu_buttons.append(Button(300, 350, 120, 60, 
                                            function  = self.restart,
                                            colour = WHITE,
                                            highlighted_colour = PENCIL_GRAY,
                                            text = "Try Again" ))


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


    # Function that randomly choose empty place on the board and prints a hint to the user (only if button clicked)
    # Input: Nothing
    # Output: Nothing
    def hint(self):
        if not self.hints:
            self.error_msg = True
            return False

        empty_lst = []

        for i in range(BOARD_SIZE):
            for k in range(BOARD_SIZE):
                if self.grid[i][k] == UNASSIGNED:
                    empty_lst.append((i ,  k)) # (Row, Col)
        
        length = len(empty_lst) - 1
        rand_position = randint(0, length)
        self.grid[empty_lst[rand_position][0]][empty_lst[rand_position][1]] = FINISHED_BOARD[empty_lst[rand_position][0]][empty_lst[rand_position][1]]
        self.hints -= 1


    # Recursive function that solve the sudoku backtracking
    # Input: Nothing
    # Output: True if we finished the sudoku, False if need to change previous values
    def solved_gui(self):
        find = empty_pos(self.grid)
        if not find:
            return True
        else: 
            row, col = find

        for i in range (1, BOARD_SIZE + 1):
            self.grid[row][col] = i
            self.playing_draw()

            if check_validation(self.grid, [row, col], i):
                if self.solved_gui():
                    return True
            
            self.grid[row][col] = 0
            pygame.time.delay(150)
        
        return False


    # Function that responsible on the menu differen events (Exit the game or start over)
    # Input: Nothing
    # Output: Nothing
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # When the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menu_buttons:
                    if button.highlighted:
                        button.click()
    

    # Function that updates the menu (by user's mouse position/clicking on buttons etc)
    # Input: Nothing
    # Output: Nothing
    def game_over_update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.update(self.mouse_pos)


    # Function that prints the user GAME OVER/YOU WIN screen
    # Input: Nothing
    # Output: Nothing
    def game_over_draw(self, pos = [WIDTH - 500, HEIGHT - 350]):
        self.window.fill(BLACK)
        
        for button in self.menu_buttons:
            button.draw(self.window)
        
        error_font = pygame.font.SysFont('comicsans', 100)
        font = error_font.render(self.screen_text, False, PINK)
        self.window.blit(font, pos)

        pygame.display.update()
        pygame.display.set_caption(self.caption)


    # Function that restarts the game
    # Input: Nothing
    # Output: Nothing
    def restart(self):
        self.running = True
        self.grid = BOARD
        self.temp_values = {} 
        self.selected = None
        self.mouse_pos = None
        self.state = "playing"
        self.caption = "Sudoku"
        self.screen_text = ""
        self.cell_changed = False
        self.error_msg = False
        self.playing_buttons = []
        self.menu_buttons = []
        self.lock_cells = []
        self.errors = 0
        self.hints = 3
        self.font = pygame.font.SysFont('comicsans', 40)
        self.load()


    # Function that exit the game
    # Input: Nothing
    # Output: Nothing
    def exit_game(self):
        self.running = False