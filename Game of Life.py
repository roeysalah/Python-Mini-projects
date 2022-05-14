"""
@author: Roey Salah
"""


import matplotlib.pyplot as plt
import game_of_life_interface
import numpy as np


class GameOfLife(game_of_life_interface.GameOfLife):
    def __init__(self, size_of_board, board_start_mode, rules, rle, pattern_position):
        self.size_of_board=size_of_board
        self.board_start_mode=board_start_mode
        self.rules=rules
        self.rle=rle
        self.pattern_position=pattern_position
        self.board=self.init_board()


    def update(self):
        """
        This method updates the board game by the rules of the game. Do a single iteration.
        Input None.
        Output None.
        """
        N = self.size_of_board
        # Get the game rules
        rules = self.rules.split('/')
        birth = rules[0]
        survival = rules[1]
        if len(birth) > 1:
            birth = birth[1:]
        else:
            birth = '0'
        if len(survival) > 1:
            survival = survival[1:]
        else:
            survival = '0'

        next_board = np.zeros((N, N), dtype=int)
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                sum = int((self.board[i, (j - 1) % N] + self.board[i, (j + 1) % N] +
                             self.board[(i - 1) % N, j] + self.board[(i + 1) % N, j] +
                             self.board[(i - 1) % N, (j - 1) % N] + self.board[(i - 1) % N, (j + 1) % N] +
                             self.board[(i + 1) % N, (j - 1) % N] + self.board[(i + 1) % N, (j + 1) % N]) / 255)
                # game rules
                if val == 255 and (str(sum) in survival):
                    next_board[i][j] = 255
                elif val == 0 and (str(sum) in birth):
                    next_board[i][j] = 255
                else:
                    next_board[i][j] = 0
        self.board = next_board

    def save_board_to_file(self, file_name):
        """ This method saves the current state of the game to a file. You should use Matplotlib for this.
        Input img_name donates the file name. Is a string, for example file_name = '1000.png'
        Output a file with the name that donates filename.
        """
        plt.imsave( file_name,self.board ,format="png")

    def display_board(self):
        """ This method displays the current state of the game to the screen. You can use Matplotlib for this.
        Input None.
        Output a figure should be opened and display the board.
        """
        fig, ax = plt.subplots()

        img = ax.imshow(self.board, interpolation='nearest')

        plt.show()



    def init_board(self):
        """
        this function initiate the board with the starting values by the start mode
        :return: return the board
        """
        board = []
        N=self.size_of_board
        
        if self.rle != '' and self.board_start_mode == 0:
            return self.transform_rle_to_matrix(self.rle)

        if self.board_start_mode == 1:
            board=np.random.choice([0,255],(N,N),p=[0.5,0.5])
        elif self.board_start_mode == 2:
            board=np.random.choice([0,255],(N,N),p=[0.2,0.8])
        elif self.board_start_mode == 3:
            board=np.random.choice([0,255],(N,N),p=[0.8,0.2])
        elif self.board_start_mode == 4:
            board = np.zeros((N,N),dtype=int)
            board[14,11] = 255
            board[15,11] = 255
            board[14,10] = 255
            board[15,10] = 255
            board[14,20] = 255
            board[15,20] = 255
            board[16,20] = 255
            board[13,21] = 255
            board[17,21] = 255
            board[12,22] = 255
            board[18,22] = 255
            board[12,23] = 255
            board[18,23] = 255
            board[15,24] = 255
            board[13,25] = 255
            board[17,25] = 255
            board[14:17,26] = 255
            board[15,27] = 255
            board[12:15,30] = 255
            board[12:15,31] = 255
            board[11,32] = 255
            board[15,32] = 255
            board[10:12,34] = 255
            board[15:17,34] = 255
            board[12:14,44] = 255
            board[12:14,45] = 255
            
        return board

    def return_board(self):
        """ This method returns a list of the board position. The board is a two-dimensional list that every
        cell donates if the cell is dead or alive. Dead will be donated with 0 while alive will be donated with 255.
        Input None.
        Output a list that holds the board with a size of size_of_board*size_of_board.
        """
        return self.board.tolist()
    
    
    def encode_rle(self,rle):
        """
        encode the rle string
        :param rle:the rle string
        :return: encoded rle string
        """
        num=''
        rle_str = ""
        for i in rle :  
            if not i.isalpha() and i not in '$!':
                num+=i
            else:
                rle_str += self.encode_sub_rle(i,num)
                num = ''

        rle_str = rle_str.replace('b','0')
        rle_str = rle_str.replace('o','1') 
        return rle_str            
    
    
    
    def encode_sub_rle(self,letter,num):
        """
        this function gets a letter and replicate it 'num' times
        :param letter: letter from the rle string (o or b)
        :param num:the num of times we need to replicate the letter
        :return: 'num' times letter replicate
        """
        rle_substr=''
        
        if num=='':
            return letter
        for i in range(int(num)):
            rle_substr+=letter
        return rle_substr
    
    def transform_rle_to_matrix(self, rle):
        """ This method transforms an rle coded pattern to a two dimensional list that holds the pattern,
         Dead will be donated with 0 while alive will be donated with 255.
        Input an rle coded string.
        Output a two dimensional list that holds a pattern with a size of the bounding box of the pattern.
        :param rle:the rle string

        :return: board N*N after initiated with the rle string
        """
        N = self.size_of_board
        x = self.pattern_position[0]
        y = self.pattern_position[1]
        encoded_rle_str = self.encode_rle(rle)
        board = np.zeros((N,N),dtype=int)
        k=0
        for i in range(x,N+1):
            for j in range(y,N+1):
                if encoded_rle_str[k] == '!':
                    break
                if encoded_rle_str[k] == '$':
                    k+=1
                    break
                board[i][j] = int(encoded_rle_str[k])
                k+=1
        # I initiated the board with 1 and 0 and here i replace 1 with 255
        for i in range(x,N):
            for j in range(y,N):
                if board[i][j] == 1:
                    board[i][j] = 255
            
        return board
        

if __name__ == '__main__':  # You should keep this line for our auto-grading code.

    size_of_board = 100
    board_start_mode = 4
    rle = ""
    pattern_position = 0
    rules = "B3/S23"
    board_iter = 270

    game = GameOfLife(size_of_board, board_start_mode, rules, rle, pattern_position)
    
    for i in range(board_iter):
       game.display_board()
       game.update()
    game.save_board_to_file('1000.png')




