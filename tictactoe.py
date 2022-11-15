import sys
import copy
import pygame
import numpy as np

from constants import *

#Pygame set up
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares #empty square
        self.marked_squares = 0

    def final_state(self):
        #vertical wins
        for col in range(COLS):
            if (self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0):
                return self.squares[0][col]
        #horizontal wins
        for row in range(ROWS):
            if (self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0):
                return self.squares[row][0]
        #desc diagonal
        if (self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0):
            return self.squares[1][1]
        #asc diagonal
        if (self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0):
            return self.squares[0][2]
        #no winner
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def isFull(self):
        return self.marked_squares == 9

    def isEmpty(self):
        return self.marked_squares == 0

class AI:
    def __init__(self , player=2):
        self.player = player
    
    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        print(f'mark {move} with an eval of {eval}')
        return move

    def minimax(self, board, maximizing):
        #terminal case
        case = board.final_state()

        #player 1 wins
        if (case == 1):
            return 1, None
        
        #player 2 wins
        if (case == 2):
            return -1, None
        
        elif board.isFull():
            return 0, None
        
        if maximizing:
            max_eval = -100000
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if (eval > max_eval):
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100000
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if (eval < min_eval):
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1 = x, 2 = o
        self.gamemode = 'ai' #or ai
        self.running = True
        self.draw_lines()
    
    def draw_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQUARE_SIZE, 0), (WIDTH-SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQUARE_SIZE), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)

    def draw_figure(self, row, col):
        if (self.player == 1):
            start_desc = (col*SQUARE_SIZE + OFFSET, row*SQUARE_SIZE + OFFSET)
            end_desc = (col*SQUARE_SIZE + SQUARE_SIZE - OFFSET, row*SQUARE_SIZE + SQUARE_SIZE - OFFSET)

            start_asc = (col*SQUARE_SIZE + SQUARE_SIZE - OFFSET, row*SQUARE_SIZE + OFFSET)
            end_asc = (col*SQUARE_SIZE + OFFSET, row*SQUARE_SIZE + SQUARE_SIZE - OFFSET)

            pygame.draw.line(screen, CIRCLE_COLOR, start_desc, end_desc, X_WIDTH)
            pygame.draw.line(screen, CIRCLE_COLOR, start_asc, end_asc, X_WIDTH)


        elif (self.player == 2):
            center = (col*SQUARE_SIZE + SQUARE_SIZE // 2, row*SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, LINE_WIDTH)


    def next_turn(self):
        self.player = self.player % 2 + 1

    def isOver(self):
        return self.board.final_state() != 0 or self.board.isFull()



def main():

    game = Game()
    board = game.board
    ai = game.ai
    
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            
            if (event.type == pygame.MOUSEBUTTONDOWN):
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] //SQUARE_SIZE
                
                if (board.empty_square(row, col) and game.running):
                    board.mark_square(row, col, game.player)
                    game.draw_figure(row, col)
                    game.next_turn()
                    if (game.isOver()):
                        game.running = False
            
        if (game.gamemode == 'ai' and game.player == ai.player and game.running):
            pygame.display.update()

            row, col = ai.eval(board)
            board.mark_square(row, col, ai.player)
            game.draw_figure(row, col)
            game.next_turn()
            if (game.isOver()):
                game.running = False

                
                    

                
        pygame.display.update()
        
main()