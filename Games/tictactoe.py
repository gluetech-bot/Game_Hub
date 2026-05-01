import numpy as np
import sys
import pygame
import os
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")   # current date

WIDTH, HEIGHT = 720, 720
Board_Size = 360
ROWS, COLS = 10, 10
CELL_SIZE = Board_Size // COLS      # size of each cell
OFFSET_X = 180 #(WIDTH - Board_Size) // 2   # center horizontally
OFFSET_Y = 110 #(HEIGHT - Board_Size) // 2  # center vertically
BLACK = (0, 0, 0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))            # allow parent imports

from game import BoardGame

class TicTacToe(BoardGame):
    def __init__(self, player1, player2):
        self.size = 10
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1  # 1 = X, 2 = O
        self.player_names   = {1: player1, 2: player2}
        self.game_over = False
        self.winner         = None
        self.move_count     = 0
        self.reset()                                       # reset game state
    def make_move(self, row, col):
        if self.board[row][col] == 0:                       # valid move if cell empty
            return True
        else:
            return False
    def change_board(self,row,col):
        self.board[row][col] = self.current_player             # place move
    def reset(self):
        self.board = np.zeros((self.size, self.size))           # clear board
        self.current_player = 1
        self.game_over = False
        self.winner = None
    def is_full(self):
     return np.all(self.board != 0)                              # check if board is full


    def check_win(self):
    
     mask = (self.board == self.current_player)               # positions of current player

    # --- Horizontal ---
     h_windows = sliding_window_view(mask, (1, 5))            # sliding window 1x5
     h_check = np.any(np.all(h_windows, axis=(2, 3)))           # all 5 true

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

     return h_check or v_check or d_check         # win if any direction

    
    def draw_grid(self,screen):
        
        for i in range(ROWS + 1):
        # horizontal
           pygame.draw.line(screen, (80, 140, 255),
            (OFFSET_X, 2*OFFSET_Y + i * CELL_SIZE),
            (OFFSET_X + Board_Size, 2*OFFSET_Y + i * CELL_SIZE))   # horizontal

        # vertical
           pygame.draw.line(screen,(80, 140, 255),
            (OFFSET_X + i * CELL_SIZE, 2*OFFSET_Y),
            (OFFSET_X + i * CELL_SIZE,2*OFFSET_Y + Board_Size))      # vertical
    #def run_game(self,scr:pygame.Surface):
        #self.draw_grid(self,scr)
    def fill_board(self, screen):
        pad = 6
        for row in range(ROWS):
            for col in range(COLS):
                x0 = OFFSET_X + col * CELL_SIZE
                y0 = 2 * OFFSET_Y + row * CELL_SIZE
                cx = x0 + CELL_SIZE // 2
                cy = y0 + CELL_SIZE // 2

                if self.board[row][col] == 1:   # X
                    pygame.draw.line(screen, (0, 220, 255),
                                    (x0 + pad, y0 + pad),
                                    (x0 + CELL_SIZE - pad, y0 + CELL_SIZE - pad), 2)
                    pygame.draw.line(screen, (0, 220, 255),
                                    (x0 + CELL_SIZE - pad, y0 + pad),
                                    (x0 + pad, y0 + CELL_SIZE - pad), 2)

                elif self.board[row][col] == 2: # O
                    pygame.draw.circle(screen, (0, 220, 255),
                                    (cx, cy), CELL_SIZE // 2 - pad, 3)


    def run_tic(self):
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")       
        bg_img = pygame.image.load("./Images/tic_bkgnd.png")
        bg_img = pygame.transform.scale(bg_img, (720, 720))   # resize background
        def draw(screen, a):
            screen.blit(bg_img,(0,0))      # draw background
            a.draw_grid(screen)            # draw grid
        def draw_popup(screen):
            screen_w, screen_h = 720, 720
            popup_w, popup_h = 450, 400
            btn_w, btn_h = 295, 30

            popup_x = (screen_w - popup_w) // 2            # center popup
            popup_y = (screen_h - popup_h) // 2

            leaderboard= pygame.image.load("./Images/tic_leaderboard.png")
            leaderboard = pygame.transform.scale(leaderboard, (popup_w, popup_h))
            screen.blit(leaderboard, (popup_x, popup_y))
            pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_w, popup_h), 5)
            
            wins_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 270, btn_w, btn_h)
            loss_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 310, btn_w, btn_h)
            ratio_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 350, btn_w, btn_h)

            hover_leader = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            hover_leader.fill((0, 0, 0, 100))
                                                                             #text on mainbar
            font = pygame.font.SysFont("segoeui", 26, bold=True)
            box_width = 260
            if self.winner == 1 or self.winner ==2:
             winnner_text = font.render(self.player_names[self.winner]+"'s VICTORY!", True, (180, 240, 255))
            if self.winner ==0:
                winnner_text = font.render("Game is a Draw ", True, (180, 240, 255)) 
            if winnner_text.get_width() > box_width:
                scale_factor = box_width / winnner_text.get_width()
                new_width = int(winnner_text.get_width() * scale_factor)
                new_height = int(winnner_text.get_height() * scale_factor)
                winnner_text = pygame.transform.smoothscale(winnner_text, (new_width, new_height))
            screen.blit(winnner_text, (popup_x + 100, popup_y + 90))
            
            
            if wins_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hover_leader, wins_rect.topleft)
            if loss_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hover_leader, loss_rect.topleft)              #hovering
            if ratio_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hover_leader, ratio_rect.topleft)
            return wins_rect, loss_rect, ratio_rect
        
        
        reset_rect= pygame.Rect(135, 625, 215, 55)
        back_rect= pygame.Rect(375, 625, 215, 55)
        hover_surface = pygame.Surface((215, 55), pygame.SRCALPHA)
        hover_surface.fill((0, 0, 0, 100))


        acc=pygame.display.set_mode((WIDTH,HEIGHT))
        wins_rect = loss_rect = ratio_rect = None
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            draw(acc,self)   
            self.fill_board(acc)
            g = pygame.font.SysFont("segoeui", 40)
            f = pygame.font.SysFont("consolas", 20)
            # text = g.render("Tic Tac Toe", True, (0, 220, 255))
            # text_rect = text.get_rect(center=(WIDTH//2, 20))
            if reset_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, reset_rect.topleft)
            if back_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, back_rect.topleft)
           
            
                                                                                                   # glow layer
            glow = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (0, 220, 255))
            text = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (180, 240, 255)) 
                
            game_box = 300
            if text.get_width() > game_box:
                scale_factor = game_box / text.get_width()
                new_width = int(text.get_width() * scale_factor)
                new_height = int(text.get_height() * scale_factor)
                text = pygame.transform.smoothscale(text, (new_width, new_height))
                glow = pygame.transform.smoothscale(glow, (new_width, new_height))
            acc.blit(glow, (210, 130))
            acc.blit(text, (210, 130))
            
            if self.game_over:
                wins_rect, loss_rect, ratio_rect = draw_popup(acc)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()               #to go out of game

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos):
                        self.reset()
                        continue

                    if back_rect.collidepoint(event.pos):    #goback
                        return

                    if not self.game_over:
                        col = (event.pos[0] - OFFSET_X) // CELL_SIZE
                        row = (event.pos[1] - 2 * OFFSET_Y) // CELL_SIZE

                        if 0 <= row < ROWS and 0 <= col < COLS:
                            if self.make_move(row, col):
                                self.change_board(row, col)

                                if self.check_win():
                                    self.game_over = True
                                    winner = self.player_names[self.current_player]
                                    loser = self.player_names[2 if self.current_player == 1 else 1]
                                    self.winner = self.current_player
                                    if winner != "guest" and loser != "guest" :    
                                        with open("history.csv", "a") as f:                     #appending result to history.csv
                                            f.write(f"{winner},{loser},{now},Tic-Tac-Toe\n")  
                                elif self.is_full():
                                    self.game_over = True 
                                    self.winner = 0      
                                else:
                                     self.switch_turn()

                    if self.game_over:
                       
                       if wins_rect is not None and wins_rect.collidepoint(event.pos):    #arguments for leaderboard.sh
                           return "wins"
                       if loss_rect is not None and loss_rect.collidepoint(event.pos):
                           return "loss"
                       if ratio_rect is not None and ratio_rect.collidepoint(event.pos):
                           return "ratio"
            pygame.display.update()