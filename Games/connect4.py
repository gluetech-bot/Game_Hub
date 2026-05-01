import numpy as np
import sys
import pygame
import os
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")
# Define constants for the game dimensions and board configuration
WIDTH, HEIGHT = 720, 720
Board_Size = 364
ROWS, COLS = 7, 7
CELL_SIZE = Board_Size // COLS  # 51
OFFSET_X = 180   # center horizontally
OFFSET_Y = 110   # center vertically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from game import BoardGame
# Connect4 class inherits from the BoardGame class and implements the game logic for Connect 4
class Connect4(BoardGame):
    #Initialize the game board and set the current player
    def __init__(self, player1, player2):
        self.size = 7
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1  # 1 = X, 2 = O
        self.player_names   = {1: player1, 2: player2}
        self.game_over = False
        self.winner         = None
        self.move_count     = 0
        self.reset()
    # Checking if the selected column is valid for placing a piece
    def make_move(self, col):
        if 0 <= col < COLS:
            return self.board[0][col] == 0
        return False
    # Placing the piece in the selected column and checking if the move is valid 
    def change_board(self,col):
        for r in range(6,-1,-1):
         if self.board[r][col] == 0:
           self.board[r][col] = self.current_player
           return 
    # For resetting the game to its initial state    
    def reset(self):
        self.board = np.zeros((self.size, self.size))
        self.current_player = 1
        self.game_over = False
        self.winner = None
    # WIN CONDITION CHECKING: Checking for 4 in a row horizontally, vertically, and diagonally    
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
       
   
    # Drawing the game grid on the screen using Pygame
    def is_full(self):
      return np.all(self.board != 0)

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
    # Filling the game board with the pieces based on the current state of the board
    def fill_board(self,screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, (0, 220, 0),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),20)
                     
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, (0, 220, 255),(OFFSET_X+CELL_SIZE*(j+0.5),2*OFFSET_Y+CELL_SIZE*(i+0.5)),20)
    # Running the main game loop, handling user input, and updating the game state accordingly
    def run_connect4(self):
        pygame.init()
        pygame.display.set_caption("Connect 4")
        
        acc=pygame.display.set_mode((WIDTH,HEIGHT))
        # The image file
        bg_img = pygame.image.load("./Images/connect_bkgnd.png")   
        bg_img = pygame.transform.scale(bg_img, (720, 720))
        # Function to draw the game grid and pieces on the screen
        def draw(screen, a):
            screen.blit(bg_img,(0,0))
            a.draw_grid(screen)
        def draw_popup(screen):
            screen_w, screen_h = 720, 720
            popup_w, popup_h = 450, 400
            btn_w, btn_h = 295, 30
        # Creating the button rectangles for the leaderboard buttons and centering the popup on the screen
            popup_x = (screen_w - popup_w) // 2
            popup_y = (screen_h - popup_h) // 2

            leaderboard= pygame.image.load("./Images/con_leaderboard.png")
            leaderboard = pygame.transform.scale(leaderboard, (popup_w, popup_h))
            screen.blit(leaderboard, (popup_x, popup_y))
            pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_w, popup_h), 5) 
            
            wins_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 270, btn_w, btn_h)
            loss_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 310, btn_w, btn_h)
            ratio_rect = pygame.Rect(popup_x + (popup_w - btn_w)//2, popup_y + 350, btn_w, btn_h)
            # Creating a semi-transparent surface for the hover effect on the buttons
            hover_leader = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            hover_leader.fill((0, 0, 0, 100))
            # If the winner's name is too long, scale down the text to fit within the popup
            font = pygame.font.SysFont("segoeui", 26, bold=True)
            box_width = 260
            if self.winner == 1 or self.winner == 2:
             winnner_text = font.render(self.player_names[self.winner]+"'s VICTORY!", True, (180, 240, 255))
            if self.winner ==0:
                winnner_text = font.render("Game is a Draw", True, (180, 240, 255))
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
        wins_rect = loss_rect = ratio_rect = None
        

        
 
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            draw(acc,self)   
            self.fill_board(acc)
            
            f = pygame.font.SysFont("consolas", 20)
            
            if reset_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, reset_rect.topleft)
            if back_rect.collidepoint(mouse_pos):
                acc.blit(hover_surface, back_rect.topleft)
            # If the player's name is too long, scale down the text to fit within the designated area
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
            # If the game is over, draw the popup with the winner's name and leaderboard buttons
            if self.game_over:
                wins_rect, loss_rect, ratio_rect = draw_popup(acc)
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
                                    winner = self.player_names[self.current_player]
                                    loser = self.player_names[2 if self.current_player == 1 else 1]
                                    self.winner = self.current_player
                                    # Record the game result in the history.csv file with the winner's name, loser's name, date, and game name
                                    if winner != "guest" and loser != "guest" :
                                        with open("history.csv", "a") as f:
                                            f.write(f"{winner},{loser},{now},Connect4\n")
                                elif self.is_full():
                                    self.game_over = True 
                                    self.winner = 0  
                                else:
                                    self.switch_turn()
                    # If the game is over, check if the user clicked on any of the leaderboard buttons and return the corresponding result
                    if self.game_over:
                       
                            if wins_rect is not None and wins_rect.collidepoint(event.pos):
                                return "wins"
                            if loss_rect is not None and loss_rect.collidepoint(event.pos):
                                return "loss"
                            if ratio_rect is not None and ratio_rect.collidepoint(event.pos):
                                return "ratio"            
            pygame.display.update()