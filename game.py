import sys
import pygame

class player:
	def __init__(self,name,turn):
		self.name=name
    	self.turn=turn
	def switch(self,other):
    	self.turn,other.turn=other.turn,self.turn
  	def win(self):
    	pass

p1=player(sys.argv[1],True)
p2=player(sys.argv[2],False)

pygame.init()

screen=pygame.display.set_mode((720,720))
running=True

while running:
	for event in pygame.event.get():
    	if event.type==pygame.QUIT:
      	running=False

pygame.quit()

