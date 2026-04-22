import numpy as np
import sys
import pygame
import os
from numpy.lib.stride_tricks import sliding_window_view
pygame.init()
WIDTH, HEIGHT = 720, 720
Board_Size = 600
ROWS, COLS = 10, 10
CELL_SIZE = Board_Size // COLS  # 72
OFFSET_X = (WIDTH - Board_Size) // 2   # center horizontally
OFFSET_Y = (HEIGHT - Board_Size) // 2  # center vertically
BLACK = (0, 0, 0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from game import BoardGame

class TicTacToe(BoardGame):
    def __init__(self, player1, player2):
        self.size = 10
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1  # 1 = X, -1 = O
        self.player_names   = {1: player1, 2: player2}
        self.game_over = False
        self.winner         = None
        self.move_count     = 0
        self.reset()
    def make_move(self, row, col):
        if self.board[row][col] == 0:
            return True
        else:
            return False
    def change_board(self,row,col):
        self.board[row][col] = self.current_player
    def reset(self):
        pass
        
    def check_win(self):
    
     mask = (self.board == self.current_player)

    # --- Horizontal ---
     h_windows = sliding_window_view(mask, (1, 5))
     h_check = np.any(np.all(h_windows, axis=(2, 3)))

    # --- Vertical ---
     v_windows = sliding_window_view(mask, (5, 1))
     v_check = np.any(np.all(v_windows, axis=(2, 3)))

    # --- Diagonal ---
     d_windows = sliding_window_view(mask, (5, 5))

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
                    pygame.draw.line(screen,(0, 220, 255),(CELL_SIZE*(i+1)+5,CELL_SIZE*(j+2)+5),(CELL_SIZE*(i+2)-5,CELL_SIZE*(j+3)-5),2)
                    pygame.draw.line(screen,(0, 220, 255),(CELL_SIZE*(i+2)-5,CELL_SIZE*(j+2)+5),(CELL_SIZE*(i+1)+5,CELL_SIZE*(j+3)-5),2)
                    
                     #draw X
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, (0, 220, 255),(60*i+90,60*j+150),25,3)
        
bg_img = pygame.image.load("./Images/tic_bkgnd.png")   # your image file
bg_img = pygame.transform.scale(bg_img, (720, 720))
def draw(screen, a):
    screen.blit(bg_img,(0,0))
    a.draw_grid(screen)




acc=pygame.display.set_mode((WIDTH,HEIGHT))

a = TicTacToe("ram","shyam")   
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    draw(acc,a)   
    a.fill_board(acc)
    g = pygame.font.SysFont("segoeui", 40)
    f = pygame.font.SysFont("consolas", 20)
    text = g.render("Tic Tac Toe", True, (0, 220, 255))
    text_rect = text.get_rect(center=(WIDTH//2, 20))

    acc.blit(text, text_rect)
    # glow layer
    if not a.game_over:
      glow = f.render(a.player_names[a.current_player]+"'s turn"+" :", True, (0, 220, 255))
      acc.blit(glow, (22, 62))
      text = f.render(a.player_names[a.current_player]+"'s turn"+" :", True, (180, 240, 255)) 
      acc.blit(text, (20, 60))
    if a.game_over:
        glow = f.render(a.player_names[a.winner] + " Wins", True, (0, 220, 255))
        acc.blit(glow, (22, 62))

        text = f.render(a.player_names[a.winner] + " Wins", True, (180, 240, 255))
        acc.blit(text, (20, 60))
    
    for event in pygame.event.get():
       
       
       if event.type == pygame.MOUSEBUTTONDOWN:
            if not a.game_over: 
              d = (mouse_pos[0]-60)//60
              h = (mouse_pos[1]-120)//60
         
              if a.make_move(d,h):
                
                a.change_board(d,h)
                
                if a.check_win():
                   a.game_over = True
                   a.winner = a.current_player
            
                else:    
                   a.switch_turn()
                   glow = f.render(a.player_names[a.current_player]+"'s turn"+" :Place X", True, (0, 220, 255))
                   acc.blit(glow, (22, 62))
                   text = f.render(a.player_names[a.current_player]+"'s turn"+" :Place X", True, (180, 240, 255)) 
                   acc.blit(text, (20, 60))

              else:
                  pass   #can print invalid move  
            else:
              
             glow = f.render(a.player_names[a.winner] + " Wins", True, (0, 220, 255))
             acc.blit(glow, (22, 62))

             text = f.render(a.player_names[a.winner] + " Wins", True, (180, 240, 255))
             acc.blit(text, (20, 60))
             
            

       if event.type == pygame.QUIT:
            running = False   
    pygame.display.update()

pygame.quit()
