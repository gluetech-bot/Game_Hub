import sys
import pygame
from pygame.locals import *
# creating a class for players,if it's turn of player 1 the turn=1 and if it's turn of player 2 the turn=-1
class Board:
    def __init__(self, player_1, player_2, total_rows, turn=1):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = np.zeros((total_rows, total_rows), dtype=int)
        self.turn = turn

    def change_turn(self):
        self.turn *= -1
    
    def make_move(self, row, col):
        if self.board[row, col] == 0:
            self.board[row, col] = self.turn
            if self.check_winner():
                return f"Player {self.player_1 if self.turn == 1 else self.player_2} wins!"
            elif np.all(self.board != 0):
                return "It's a draw!"
            else:
                self.change_turn()
                return "Move accepted."
        else:
            return "Invalid move. Try again."

    def check_winner(self):
        pass

    def reset_game(self):
        self.board.fill(0)
        self.turn = 1


pygame.init()
pygame.display.set_caption("Game Hub")

screen_width=720
screen_height=720

menu_scr=pygame.display.set_mode((screen_width,screen_height))
menu_bkgnd=pygame.image.load("./Images/menu_bkgnd.png")
menu_bkgnd_f=pygame.transform.scale(menu_bkgnd,(screen_width,screen_height))

tic_rect= pygame.Rect(130, 200, 470, 90)
rev_rect= pygame.Rect(130, 315, 470, 90)
four_rect= pygame.Rect(130, 430, 470, 90)
settings_rect= pygame.Rect(130, 545, 470, 90)

hover_surface = pygame.Surface((470, 90), pygame.SRCALPHA)
hover_surface.fill((0, 0, 0, 100))



running=True

while running:
    menu_scr.blit(menu_bkgnd_f, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

# drawing hover effects
    if tic_rect.collidepoint(mouse_pos):
        menu_scr.blit(hover_surface, tic_rect.topleft)

    if rev_rect.collidepoint(mouse_pos):
        menu_scr.blit(hover_surface, rev_rect.topleft)

    if four_rect.collidepoint(mouse_pos):
        menu_scr.blit(hover_surface, four_rect.topleft)

    if settings_rect.collidepoint(mouse_pos):
        menu_scr.blit(hover_surface, settings_rect.topleft)
# for checking mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tic_rect.collidepoint(event.pos):
                print("Tic Tac Toe")
            if rev_rect.collidepoint(event.pos):
                print("Reversi")
            if four_rect.collidepoint(event.pos):
                print("4 in a row")
            if settings_rect.collidepoint(event.pos):
                print("Settings")
# for quitting program
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()


