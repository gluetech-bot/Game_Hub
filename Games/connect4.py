import numpy as np
import sys
import pygame
import os
from numpy.lib.stride_tricks import sliding_window_view

# import game

WIDTH, HEIGHT = 720, 720
Board_Size = 364
ROWS, COLS = 7, 7
CELL_SIZE = Board_Size // COLS  # 51
OFFSET_X = 180#(WIDTH - Board_Size) // 2   # center horizontally
OFFSET_Y = 110#(HEIGHT - Board_Size) // 2  # center vertically
BLACK = (0, 0, 0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from game import BoardGame

class Connect4(BoardGame):
    def __init__(self, player1, player2):
        self.size = 7
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1  # 1 = X, 2 = O
        self.player_names   = {1: player1, 2: player2}
        self.game_over = False
        self.winner         = None
        self.move_count     = 0
        self.reset()
    def make_move(self, col):
        if 0 <= col < COLS:
            return self.board[0][col] == 0
        return False
        
    def change_board(self,col):
        for r in range(6,-1,-1):
         if self.board[r][col] == 0:
           self.board[r][col] = self.current_player
           return 
         
    def reset(self):
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def check_win(self):
    
     mask = (self.board == self.current_player)

    # --- Horizontal ---
     h_windows = sliding_window_view(mask, (1, 4))
     h_check = np.any(np.all(h_windows, axis=(2, 3)))

    # --- Vertical ---
     v_windows = sliding_window_view(mask, (4, 1))
     v_check = np.any(np.all(v_windows, axis=(2, 3)))

    # --- Diagonal ---
     d_windows = sliding_window_view(mask, (4, 4))

    # main diagonal
     main_diag = np.all(
        np.diagonal(d_windows, axis1=2, axis2=3),
        axis=2
    )

    # anti-diagonal
     anti_diag = np.all(
        np.diagonal(np.flip(d_windows, axis=3), axis1=2, axis2=3),
        axis=2
    )

     d_check = np.any(main_diag) or np.any(anti_diag)

     return h_check or v_check or d_check
       
   

    def draw_grid(self,screen):
        
        for i in range(ROWS + 1):
        # horizontal
           pygame.draw.line(screen, (80, 140, 255),
            (OFFSET_X, 2*OFFSET_Y + i * CELL_SIZE),
            (OFFSET_X + Board_Size, 2*OFFSET_Y + i * CELL_SIZE))

        # vertical
           pygame.draw.line(screen,(80, 140, 255),
            (OFFSET_X + i * CELL_SIZE, 2*OFFSET_Y),
            (OFFSET_X + i * CELL_SIZE,2*OFFSET_Y + Board_Size))
    #def run_game(self,scr:pygame.Surface):
        #self.draw_grid(self,scr)
    def fill_board(self,screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, (0, 220, 0),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),20)
                     
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, (0, 220, 255),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),20)

    def run_connect4(self):
        pygame.init()
        pygame.display.set_caption("Connect 4")
        
        acc=pygame.display.set_mode((WIDTH,HEIGHT))
        bg_img = pygame.image.load("./Images/connect_bkgnd.png")   # your image file
        bg_img = pygame.transform.scale(bg_img, (720, 720))
        def draw(screen, a):
            screen.blit(bg_img,(0,0))
            a.draw_grid(screen)

        reset_rect= pygame.Rect(135, 625, 215, 55)
        back_rect= pygame.Rect(375, 625, 215, 55)
        hover_surface = pygame.Surface((215, 55), pygame.SRCALPHA)
        hover_surface.fill((0, 0, 0, 100))
        
        


        
 
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            draw(acc,self)   
            self.fill_board(acc)
            
            g = pygame.font.SysFont("segoeui", 40)
            f = pygame.font.SysFont("consolas", 20)
            # text = g.render("Connect 4", True, (0, 220, 255))
            # text_rect = text.get_rect(center=(WIDTH//2, 20))
            if reset_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, reset_rect.topleft)
            if back_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, back_rect.topleft)
            # acc.blit(text, text_rect)
            # glow layer
            if not self.game_over:
                glow = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (0, 220, 255))
                acc.blit(glow, (210,130))
                text = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (180, 240, 255)) 
                acc.blit(text, (210,130))
            if self.game_over:
                glow = f.render(self.player_names[self.winner] + " Wins", True, (0, 220, 255))
                acc.blit(glow, (210,130))

                text = f.render(self.player_names[self.winner] + " Wins", True, (180, 240, 255))
                acc.blit(text, (210,130))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos):
                        self.reset()
                        continue

                    if back_rect.collidepoint(event.pos):
                        return

                    if not self.game_over:
                        col = (event.pos[0] - OFFSET_X) // CELL_SIZE
                        row = (event.pos[1] - 2 * OFFSET_Y) // CELL_SIZE

                        if 0 <= row < ROWS and 0 <= col < COLS:
                            if self.make_move(col):
                                self.change_board(col)

                                if self.check_win():
                                    self.game_over = True
                                    self.winner = self.current_player
                                else:
                                    self.switch_turn()
            pygame.display.update()