from protocol import BOARD_SIZE
from random import seed, randint
from copy import deepcopy

class DataBase:
    def __init__(self): 
        seed(1)
        self.data = None
        self.pre_game = {0 : -1, 1 : -1, 2 : -1, 3 : -1} # 0 - easy, 1 - medium, 2 - hard, 3 - extreme
        self.easy = []
        self.medium = []
        self.hard = []
        self.extreme = []
        self.get_data_from_file()
        self.process_data(self.data)

    
    # Function that gets the data from the file
    # Input: Nothing
    # Output: Nothing
    def get_data_from_file(self):
        file_object = open('sudokuData.txt', 'r')
        self.data = file_object.readlines()
        file_object.close()


    # Function that process the data from the file, split it to 4 strings, dependes on the level
    # Input: Nothing
    # Output: Nothing
    def process_data(self, data : list):
        for i in range(0,len(data)):
            boards = str(data[i]).split('$')

            if 'EASY' in data[i]:
                boards[len(boards) - 1] = boards[len(boards) - 1][:-1] # Removing backspace
                self.strings_to_boards(boards[1::], self.easy)
            
            elif 'MEDIUM' in data[i]:
                boards = boards[:-1] # Removing backspace
                self.strings_to_boards(boards[1::], self.medium)
            
            elif 'HARD' in data[i]:
                boards = boards[:-1] # Removing backspace
                self.strings_to_boards(boards[1::], self.hard)

            elif 'EXTREME' in data[i]:
                self.strings_to_boards(boards[1::], self.extreme)


    # Function that splites the different boards in one level to 2D list
    # Input: The level list and the boards list
    # Output: Nothing
    def strings_to_boards(self, board : list, level : list):        
        temp = [[0] * BOARD_SIZE for i in range(BOARD_SIZE)]
        
        for string in board:
            if len(string) != (BOARD_SIZE*BOARD_SIZE):
                print("Board size not correct!")
                continue
            j = 0
            for i in range(0, BOARD_SIZE):
                for k in range(0, BOARD_SIZE):
                    temp[i][k] = int(string[j])
                    j += 1

            level.append(deepcopy(temp)) 


    
    # Function that sends a random board
    # Input: The requested level
    # Output: The board
    def get_rand_board(self, level : int) -> list:
        if level == 0:
            return self.easy[self.rand_num(self.easy, level)]

        elif level == 1:
            return self.medium[self.rand_num(self.medium, level)]

        elif level == 2:
            return self.hard[self.rand_num(self.hard, level)]

        elif level == 3:
            return self.extreme[self.rand_num(self.extreme, level)]
        
        print("Wrong level")
        return None


    # Function that rands an index to the board, while checking if the user didn't play that board before.
    # Input: The level list (easy, medium etx) and the level number (0, 1 etc)
    # Output: The index of the random board
    def rand_num(self, level_lst : list, level_num):
        if len(level_lst) == 1: # If there is only one board no need to use wile loop
            return 0

        rnd = -1
        while(self.pre_game[level_num] == rnd or rnd == -1):
                rnd = randint(0, len(level_lst) - 1)
        
        self.pre_game[level_num] = rnd
        return rnd
