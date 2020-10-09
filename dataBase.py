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


    
    # Function that rands a board
    def get_rand_board(self, level : int) -> list:
        rnd = -1
        if level == 0:
            while(self.pre_game[level] == rnd or rnd == -1):
                rnd = randint(0, len(self.easy) - 1)
            
            self.pre_game[level] = rnd
            return self.easy[rnd]

        elif level == 1:
            while(self.pre_game[level] == rnd or rnd == -1):
                rnd = randint(0, len(self.medium) - 1)
            
            self.pre_game[level] = rnd
            return self.medium[rnd]

        elif level == 2:
            while(self.pre_game[level] == rnd or rnd == -1):
                rnd = randint(0, len(self.hard) - 1)

            self.pre_game[level] = rnd
            return self.hard[rnd]

        elif level == 3:
            while(self.pre_game[level] == rnd or rnd == -1):
                rnd = randint(0, len(self.extreme) - 1)
            
            self.pre_game[level] = rnd
            return self.extreme[rnd]
        
        print("Wrong level")
        return None