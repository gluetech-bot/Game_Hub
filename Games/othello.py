import numpy as np
import sys
import pygame
import os
from datetime import datetime
from numpy.lib.stride_tricks import sliding_window_view
now = datetime.now().strftime("%Y-%m-%d")
# import game
WIDTH, HEIGHT = 720, 720
Board_Size = 352
ROWS, COLS = 8, 8
CELL_SIZE = Board_Size // COLS  # 51
OFFSET_X = 184#(WIDTH - Board_Size) // 2   # center horizontally
OFFSET_Y = 111#(HEIGHT - Board_Size) // 2  # center vertically
BLACK = (0, 0, 0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from game import BoardGame

class Othello(BoardGame):
    def __init__(self, player1, player2):
        self.size = 8
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1  # 1 = X, 2 = O
        self.player_names   = {1: player1, 2: player2}
        self.game_over = False
        self.winner         = None
        self.move_count     = 0
        self.reset()
    # def make_move(self, row, col):
    #     if self.board[row][col] == 0:
    #         return True
    #     else:
    #         return False
        
    # def change_board(self,row,col):
    #     self.board[row][col] = self.current_player
         
    def reset(self):
        self.board = np.zeros((self.size, self.size))
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def check_win(self):
        valid_moves = self.get_valid_moves()

        if valid_moves:
            return False

        other_player = 2 if self.current_player == 1 else 1

        # temporarily check opponent moves
        self.current_player = other_player
        opponent_moves = self.get_valid_moves()

        if opponent_moves:
            return False   # game not over, opponent can play

        # both players have no moves => game over
        self.game_over = True

        player1_count = np.sum(self.board == 1)
        player2_count = np.sum(self.board == 2)

        if player1_count > player2_count:
            self.winner = 1
        elif player2_count > player1_count:
            self.winner = 2
        else:
            self.winner = 0

        return True

    def get_valid_moves(self):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0 and self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def draw_valid_moves(self,screen):
        valid_moves = self.get_valid_moves()
        for row, col in valid_moves:
            if self.current_player == 1:
                pygame.draw.circle(screen, (0, 0, 0), (OFFSET_X + CELL_SIZE * (col + 0.5), 2 * OFFSET_Y + CELL_SIZE * (row + 0.5)), 17, 2)
            else:
                pygame.draw.circle(screen, (255, 255, 255), (OFFSET_X + CELL_SIZE * (col + 0.5), 2 * OFFSET_Y + CELL_SIZE * (row + 0.5)), 17, 2)
        
    
    def is_valid_move(self, row, col):
        opponent = 2 if self.current_player == 1 else 1
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent_piece = False
            
            while 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] == opponent:
                    has_opponent_piece = True
                elif self.board[r][c] == self.current_player:
                    if has_opponent_piece:
                        return True
                    break
                else:
                    break
                r += dr
                c += dc
        
        return False
    
    
    def flip_pieces(self, row, col):
        opponent = 2 if self.current_player == 1 else 1
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            while 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c] == self.current_player:
                    for rr, cc in pieces_to_flip:
                        self.board[rr][cc] = self.current_player
                    break
                else:
                    break
                r += dr
                c += dc
    def make_move(self, row, col):
        if self.board[row][col] == 0 and self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.flip_pieces(row, col)
            return True
        return False
     
    
    def draw_grid(self,screen):
        
        board_color = (0, 128, 0)  # Green background
        pygame.draw.rect(screen, board_color, (OFFSET_X, 2*OFFSET_Y, Board_Size, Board_Size))
        
        for i in range(ROWS + 1):
        # horizontal
           pygame.draw.line(screen, (0,0,0),
            (OFFSET_X, 2*OFFSET_Y + i * CELL_SIZE),
            (OFFSET_X + Board_Size, 2*OFFSET_Y + i * CELL_SIZE))

        # vertical
           pygame.draw.line(screen,(0,0,0),
            (OFFSET_X + i * CELL_SIZE, 2*OFFSET_Y),
            (OFFSET_X + i * CELL_SIZE,2*OFFSET_Y + Board_Size))

    def fill_board(self,screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, (0 ,0,0),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),17)
                     
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, (255, 255, 255),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),17)

    def run_othello(self):
        pygame.init()
        pygame.display.set_caption("Othello")
        bg_img = pygame.image.load("./Images/othello_bkgnd.png")   # your image file
        bg_img = pygame.transform.scale(bg_img, (720, 720))
        def draw(screen, a):
            screen.blit(bg_img,(0,0))
            a.draw_grid(screen)
        def draw_popup(screen):
            screen_w, screen_h = 720, 720
            popup_w, popup_h = 450, 400
            btn_w, btn_h = 295, 30

            popup_x = (screen_w - popup_w) // 2
            popup_y = (screen_h - popup_h) // 2

            leaderboard= pygame.image.load("./Images/oth_leaderboard.png")
            leaderboard = pygame.transform.scale(leaderboard, (popup_w, popup_h))
            screen.blit(leaderboard, (popup_x, popup_y))
            pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_w, popup_h), 5)
            
            wins_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 270, btn_w, btn_h)
            loss_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 310, btn_w, btn_h)
            ratio_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 350, btn_w, btn_h)

            hover_leader = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            hover_leader.fill((0, 0, 0, 100))
            
            font = pygame.font.SysFont("segoeui", 26, bold=True)
            box_width = 260
            winnner_text = font.render(self.player_names[self.winner]+"'s VICTORY!", True, (180, 240, 255))

            if winnner_text.get_width() > box_width:
                scale_factor = box_width / winnner_text.get_width()
                new_width = int(winnner_text.get_width() * scale_factor)
                new_height = int(winnner_text.get_height() * scale_factor)
                winnner_text = pygame.transform.smoothscale(winnner_text, (new_width, new_height))
            screen.blit(winnner_text, (popup_x + 100, popup_y + 90))

            if wins_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hover_leader, wins_rect.topleft)
            if loss_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(hover_leader, loss_rect.topleft)
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
            draw(acc, self)
            self.fill_board(acc)
            self.draw_valid_moves(acc)
            f = pygame.font.SysFont("consolas", 20)
            player1_score = np.sum(self.board == 1)
            player2_score = np.sum(self.board == 2)
            
            
            
            glow = f.render("Black:"+str(player1_score)+", White:"+str(player2_score), True, (0, 220, 255))
            text = f.render("Black:"+str(player1_score)+", White:"+str(player2_score), True, (180, 240, 255)) 
            
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
            if reset_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, reset_rect.topleft)
            if back_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, back_rect.topleft)
            
            

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
                                self.switch_turn()

                                if not self.get_valid_moves():
                                    self.switch_turn()

                                    if not self.get_valid_moves():
                                       if self.check_win():
                                           if self.winner ==1:
                                                winner = self.player_names[1]
                                                loser = self.player_names[2]
                                           elif self.winner ==2:
                                                    winner = self.player_names[2]
                                                    loser = self.player_names[1]
                                    
                                           with open("history.csv", "a") as f:
                                            f.write(f"{winner},{loser},{now},Othello\n")
                    if self.game_over:
                       
                       if wins_rect is not None and wins_rect.collidepoint(event.pos):
                           return "wins"
                       if loss_rect is not None and loss_rect.collidepoint(event.pos):
                           return "loss"
                       if ratio_rect is not None and ratio_rect.collidepoint(event.pos):
                           return "ratio"
            pygame.display.update()