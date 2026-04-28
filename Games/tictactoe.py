import numpy as np
import sys
import pygame
import os
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")

WIDTH, HEIGHT = 720, 720
Board_Size = 360
ROWS, COLS = 10, 10
CELL_SIZE = Board_Size // COLS  # 36
OFFSET_X = 180 #(WIDTH - Board_Size) // 2   # center horizontally
OFFSET_Y = 110 #(HEIGHT - Board_Size) // 2  # center vertically
BLACK = (0, 0, 0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

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
        self.reset()
    def make_move(self, row, col):
        if self.board[row][col] == 0:
            return True
        else:
            return False
    def change_board(self,row,col):
        self.board[row][col] = self.current_player
    def reset(self):
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
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
        bg_img = pygame.transform.scale(bg_img, (720, 720))
        def draw(screen, a):
            screen.blit(bg_img,(0,0))
            a.draw_grid(screen)
        def draw_popup(screen):
            screen_w, screen_h = 720, 720
            popup_w, popup_h = 450, 400
            btn_w, btn_h = 400, 60

            popup_x = (screen_w - popup_w) // 2
            popup_y = (screen_h - popup_h) // 2

            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

            pygame.draw.rect(screen, (20, 20, 20), popup_rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2, border_radius=15)
            h_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 10, btn_w, btn_h)
            wins_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 80, btn_w, btn_h)
            loss_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 160, btn_w, btn_h)
            ratio_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 240, btn_w, btn_h)

            font = pygame.font.SysFont("segoeui", 26, bold=True)

            for rect, text in [
                (h_rect, "How Do You Want Leaderboard"),
                (wins_rect, "By Wins"),
                (loss_rect, "By Losses"),
                (ratio_rect, "By W/L Ratio")
            ]:
                pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)

                label = font.render(text, True, (255, 255, 255))
                screen.blit(label, label.get_rect(center=rect.center))

            return h_rect,wins_rect, loss_rect, ratio_rect
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
            # acc.blit(text, text_rect)
            
            # glow layer
            if not self.game_over:
                glow = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (0, 220, 255))
                acc.blit(glow, (210,130))
                text = f.render(self.player_names[self.current_player]+"'s turn"+" :", True, (180, 240, 255)) 
                acc.blit(text, (210, 130))
            if self.game_over:
                glow = f.render(self.player_names[self.winner] + " Wins", True, (0, 220, 255))
                acc.blit(glow, (210,130))

                text = f.render(self.player_names[self.winner] + " Wins", True, (180, 240, 255))
                acc.blit(text, (210, 130))
                h_rect, wins_rect, loss_rect, ratio_rect = draw_popup(acc)
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
                            if self.make_move(row, col):
                                self.change_board(row, col)

                                if self.check_win():
                                    self.game_over = True
                                    winner = self.player_names[self.current_player]
                                    loser = self.player_names[2 if self.current_player == 1 else 1]
                                    self.winner = self.current_player
                                    
                                    with open("history.csv", "a") as f:
                                        f.write(f"{winner},{loser},{now},Tic-Tac-Toe\n")
                                else:
                                     self.switch_turn()

                    if self.game_over:
                       
                       if wins_rect is not None and wins_rect.collidepoint(event.pos):
                           return "wins"
                       if loss_rect is not None and loss_rect.collidepoint(event.pos):
                           return "loss"
                       if ratio_rect is not None and ratio_rect.collidepoint(event.pos):
                           return "ratio"
            pygame.display.update()