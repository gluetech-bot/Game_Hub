import sys
import numpy as np
import pygame
import subprocess
from pygame.locals import *
import matplotlib.pyplot as plt
# from Games.tictactoe import TicTacToe
# creating a class for players
class BoardGame:
   

    def __init__(self, player1: str, player2: str):
        self.player_names   = {1: player1, 2: player2}           # map player id → name
        self.current_player = 1                                   # player 1 starts
        self.board: np.ndarray = None                               # board will be defined in child class
        self.winner         = None                                       # stores winner (None / 0 / player id)
        self.move_count     = 0                                     # number of moves played
        self.reset()                                                  # initialize board

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1          # toggle player

    def is_game_over(self) -> bool:
        return self.winner is not None                                        # game ends if winner is decided

    def current_player_name(self) -> str:
        return self.player_names[self.current_player]                         # get current player name

    def opponent_player(self) -> int:
        return 2 if self.current_player == 1 else 1

    def get_result_string(self) -> str:
        if self.winner == 0:
            return "It's a draw!"
        return f"{self.player_names[self.winner]} wins!"

    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:  ####
        return pygame.font.SysFont("segoeui", size, bold=bold)                   # create font

# Function to generate graph image using matplotlib
def Get_graph():
    t_count,c_count,o_count =0,0,0
    users = {}
    with open("inter.txt", "r") as f:
     for line in f:
        parts = line.strip().split()
        if parts[4] == "Tic-Tac-Toe":
            t_count += 1                 # increment tic-tac-toe count
            if parts[0] not in users:
                users[parts[0]]=0      
            users[parts[0]] += int(parts[1])
        if parts[4] == "Connect4":
            c_count += 1                      # increment connect4 count
            if parts[0] not in users:
                users[parts[0]]=0      
            users[parts[0]] += int(parts[1])
        if parts[4] == "Othello":               
            o_count += 1                        # increment othello count
            if parts[0] not in users:
                users[parts[0]]=0      
            users[parts[0]] += int(parts[1])
    label = ['Tictactoe','Connect4','Othello']
    value = [t_count,c_count,o_count]
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), dpi=150)
    axs[0].pie(value,labels=label,autopct='%1.1f%%')           # pie chart
    axs[0].set_title("Proportion of Games Played")
    axs[0].axis('equal')
    
    top5 = sorted(users.items(),key=lambda x: x[1],reverse=True)[:5]
    labels = [x[0] for x in top5]
    values = [x[1] for x in top5]
    axs[1].bar(labels,values)                                  #bargragh
    axs[1].set_title("Top 5 Winners")
    axs[1].set_xlabel("Players")
    axs[1].set_ylabel("No.Of wins")
    plt.tight_layout()
    plt.savefig("analysis.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
   
# Start tic tac toe game
def start_tic():
    from Games.tictactoe import TicTacToe   
    game = TicTacToe(p1, p2)
    con = game.run_tic()                             # run game
    subprocess.run(["bash","leaderboard.sh",str(con)])      # Printing leaderboard 
  # Start connect4  
def start_connect4():
    from Games.connect4 import Connect4  
    game = Connect4(p1, p2)
    con = game.run_connect4() 
    subprocess.run(["bash","leaderboard.sh",str(con)])
  
    # Start othello
def start_othello():
    from Games.othello import Othello  
    game = Othello(p1, p2)
    con = game.run_othello()
    subprocess.run(["bash","leaderboard.sh",str(con)])
    
    # Read players from command line
p1=sys.argv[1]
p2=sys.argv[2]

def main():
    pygame.init()
    pygame.display.set_caption("Game Hub")

    screen_width=720
    screen_height=720

    menu_scr=pygame.display.set_mode((screen_width,screen_height))
    menu_bkgnd=pygame.image.load("./Images/menu_bkgnd.png")
    menu_bkgnd_f=pygame.transform.scale(menu_bkgnd,(screen_width,screen_height))

    tic_rect= pygame.Rect(130, 200, 470, 90)
    othello_rect= pygame.Rect(130, 310, 470, 90)
    four_rect= pygame.Rect(130, 430, 470, 90)
    settings_rect= pygame.Rect(130, 545, 470, 90)

    hover_surface = pygame.Surface((470, 90), pygame.SRCALPHA)
    hover_surface.fill((0, 0, 0, 100))
    show_graph = False
    graph_img = None

    gback_rect = pygame.Rect(20, 20, 120, 50)
    font = pygame.font.SysFont("segoeui", 28, bold=True)
        

    running=True

    while running:
        menu_scr.blit(menu_bkgnd_f, (0, 0))        # draw background

        

        if show_graph and graph_img is not None:
    # draw graph
            menu_scr.blit(graph_img, (35, 180))       # draw graph image
            
            # draw back button
            pygame.draw.rect(menu_scr, (200, 50, 50), gback_rect, border_radius=10)
            text = font.render("Back", True, (255, 255, 255))
            menu_scr.blit(text, (gback_rect.x + 20, gback_rect.y + 10))

        else:
            mouse_pos = pygame.mouse.get_pos()       # get mouse position

            if tic_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, tic_rect.topleft)

            if othello_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, othello_rect.topleft)

            if four_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, four_rect.topleft)

            if settings_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, settings_rect.topleft)


    # drawing hover effects
        if tic_rect.collidepoint(mouse_pos):
            menu_scr.blit(hover_surface, tic_rect.topleft)

        if othello_rect.collidepoint(mouse_pos):
            menu_scr.blit(hover_surface, othello_rect.topleft)

        if four_rect.collidepoint(mouse_pos):
            menu_scr.blit(hover_surface, four_rect.topleft)

        if settings_rect.collidepoint(mouse_pos):
            menu_scr.blit(hover_surface, settings_rect.topleft)
    # for checking mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_graph:
                  if gback_rect.collidepoint(event.pos):
                    show_graph = False                    # go back to menu
                else:    
                    if tic_rect.collidepoint(event.pos):
                        start_tic()
                    if othello_rect.collidepoint(event.pos):
                        start_othello()
                    if four_rect.collidepoint(event.pos):
                        start_connect4()
                    if settings_rect.collidepoint(event.pos):
                        Get_graph()
                        graph_img = pygame.image.load("analysis.png").convert()     # load image
                        graph_img = pygame.transform.smoothscale(graph_img, (650, 350))    # resize
                        show_graph = True   # switch to graph screen

    # for quitting program

            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main()
