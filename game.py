import sys
import pygame
from pygame.locals import *
# creating a class for players
class player:
	def __init__(self,name,turn):
		self.name=name
		self.turn=turn
	def switch(self,other):
		self.turn,other.turn=other.turn,self.turn
	def win(self):
		pass

# p1=player(sys.argv[1],True)
# p2=player(sys.argv[2],False)

pygame.init()
pygame.display.set_caption("Game Hub")

screen_width=720
screen_height=720

menu_scr=pygame.display.set_mode((screen_width,screen_height))
menu_bkgnd=pygame.image.load("./Images/menu_bkgnd.png")
menu_bkgnd_f=pygame.transform.scale(menu_bkgnd,(screen_width,screen_height))

tic_rect= pygame.Rect(130, 200, 470, 90)
rev_rect= pygame.Rect(130, 310, 470, 90)
four_rect= pygame.Rect(130, 430, 470, 90)
settings_rect= pygame.Rect(130, 540, 470, 90)

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


