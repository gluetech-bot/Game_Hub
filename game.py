import sys
import numpy as np
import pygame
import subprocess
from pygame.locals import *
import matplotlib.pyplot as plt


class BoardGame:
    def __init__(self, player1: str, player2: str):
        self.player_names = {1: player1, 2: player2}   # map id → name
        self.current_player = 1                        # player 1 starts
        self.board: np.ndarray = None                  # board defined in child
        self.winner = None                             # winner state
        self.move_count = 0                            # move counter
        self.reset()                                   # initialize board

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1   # toggle player

    def is_game_over(self) -> bool:
        return self.winner is not None   # game ends if winner exists

    def current_player_name(self) -> str:
        return self.player_names[self.current_player]   # get current player name

    def opponent_player(self) -> int:
        return 2 if self.current_player == 1 else 1   # get opponent id

    def get_result_string(self) -> str:
        if self.winner == 0:
            return "It's a draw!"
        return f"{self.player_names[self.winner]} wins!"   # winner message

    def get_font(self, size: int, bold: bool = False):
        return pygame.font.SysFont("segoeui", size, bold=bold)   # font creator


def Get_graph():
    t_count, c_count, o_count = 0, 0, 0   # game counters
    users = {}                             # user → total wins

    with open("inter.txt", "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 5:
                continue   # skip invalid lines

            name = parts[0]
            wins = int(parts[1])
            game = parts[4]

            if game == "Tic-Tac-Toe":
                t_count += 1
            elif game == "Connect4":
                c_count += 1
            elif game == "Othello":
                o_count += 1

            users[name] = users.get(name, 0) + wins   # accumulate wins

    label = ["TicTacToe", "Connect4", "Othello"]
    value = [t_count, c_count, o_count]

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), dpi=150)   # 2 plots

    axs[0].pie(value, labels=label, autopct="%1.1f%%")        # pie chart
    axs[0].set_title("Proportion of Games Played")
    axs[0].axis("equal")

    top5 = sorted(users.items(), key=lambda x: x[1], reverse=True)[:5]   # top players
    labels = [x[0] for x in top5]
    values = [x[1] for x in top5]

    axs[1].barh(labels, values)   # horizontal bar
    axs[1].set_title("Top 5 Winners")
    axs[1].set_xlabel("No. of Wins")

    plt.tight_layout()
    plt.savefig("analysis.png", bbox_inches="tight", dpi=150)   # save image
    plt.close(fig)   # free memory


def start_tic():
    from Games.tictactoe import TicTacToe
    game = TicTacToe(p1, p2)
    con = game.run_tic()                              # run game
    subprocess.run(["bash", "leaderboard.sh", str(con)])   # show leaderboard
    return "post_game"                                # trigger popup


def start_connect4():
    from Games.connect4 import Connect4
    game = Connect4(p1, p2)
    con = game.run_connect4()
    subprocess.run(["bash", "leaderboard.sh", str(con)])
    return "post_game"


def start_othello():
    from Games.othello import Othello
    game = Othello(p1, p2)
    con = game.run_othello()
    subprocess.run(["bash", "leaderboard.sh", str(con)])
    return "post_game"


p1 = sys.argv[1]   # player 1 name
p2 = sys.argv[2]   # player 2 name


def main():
    pygame.init()
    pygame.display.set_caption("Game Hub")

    screen_width, screen_height = 720, 720
    menu_scr = pygame.display.set_mode((screen_width, screen_height))

    menu_bkgnd = pygame.image.load("./Images/menu_bkgnd.png")
    menu_bkgnd_f = pygame.transform.scale(menu_bkgnd, (screen_width, screen_height))

    tic_rect = pygame.Rect(130, 200, 470, 90)       # button areas
    othello_rect = pygame.Rect(130, 310, 470, 90)
    four_rect = pygame.Rect(130, 430, 470, 90)
    settings_rect = pygame.Rect(130, 545, 470, 90)

    hover_surface = pygame.Surface((470, 90), pygame.SRCALPHA)
    hover_surface.fill((0, 0, 0, 100))   # hover effect

    show_graph = False        # state: graph screen
    show_post_popup = False   # state: post-game popup
    graph_img = None

    gback_rect = pygame.Rect(20, 20, 140, 70)   # back button
    back_btn=pygame.image.load("./Images/back_btn.png")
    back_btn=pygame.transform.smoothscale(back_btn, (140, 70))
    back_hover = pygame.Surface((140, 70), pygame.SRCALPHA)
    back_hover.fill((0, 0, 0, 100))   # hover for back button
    
    end=pygame.image.load("./Images/end.png")
    end=pygame.transform.smoothscale(end, (500, 400))
    
    play_again_rect = pygame.Rect(110+90, 160+115, 325, 55)   # popup buttons
    analysis_rect = pygame.Rect(110+90, 160+190, 325, 55)
    exit_rect = pygame.Rect(110+90, 160+265, 325, 55)
    end_hover = pygame.Surface((325, 55), pygame.SRCALPHA)
    end_hover.fill((0, 0, 0, 100))   # hover for popup buttons

    font = pygame.font.SysFont("segoeui", 28, bold=True)
    title_font = pygame.font.SysFont("segoeui", 30, bold=True)

    running = True

    while running:
        menu_scr.blit(menu_bkgnd_f, (0, 0))   # draw background
        mouse_pos = pygame.mouse.get_pos()

        if show_post_popup:
            menu_scr.blit(end, (110, 160))   # show end popup
            pygame.draw.rect(menu_scr, (255, 255, 255), (110, 160, 500, 400), 3)
            if play_again_rect.collidepoint(mouse_pos):
                menu_scr.blit(end_hover, play_again_rect.topleft)
            elif analysis_rect.collidepoint(mouse_pos):
                menu_scr.blit(end_hover, analysis_rect.topleft)
            elif exit_rect.collidepoint(mouse_pos):
                menu_scr.blit(end_hover, exit_rect.topleft)
            # pygame.draw.rect(menu_scr, (20, 20, 40), (140, 220, 440, 300), border_radius=20)
            # pygame.draw.rect(menu_scr, (255, 255, 255), (140, 220, 440, 300), 3, border_radius=20)

            # title = title_font.render("What do you want to do?", True, (255, 255, 255))
            # menu_scr.blit(title, (190, 245))

            # pygame.draw.rect(menu_scr, (40, 150, 80), play_again_rect, border_radius=10)
            # pygame.draw.rect(menu_scr, (50, 100, 180), analysis_rect, border_radius=10)
            # pygame.draw.rect(menu_scr, (180, 50, 50), exit_rect, border_radius=10)

            # menu_scr.blit(font.render("Play Again", True, (255, 255, 255)),
            #               (play_again_rect.x + 95, play_again_rect.y + 10))

            # menu_scr.blit(font.render("Game Analysis", True, (255, 255, 255)),
            #               (analysis_rect.x + 70, analysis_rect.y + 10))

            # menu_scr.blit(font.render("Exit", True, (255, 255, 255)),
            #               (exit_rect.x + 145, exit_rect.y + 10))

        elif show_graph and graph_img is not None:
            menu_scr.blit(graph_img, (35, 180))   # show graph

            # pygame.draw.rect(menu_scr, (200, 50, 50), gback_rect, border_radius=10)
            # text = font.render("Back", True, (255, 255, 255))
            # menu_scr.blit(text, (gback_rect.x + 20, gback_rect.y + 10))
            menu_scr.blit(back_btn, gback_rect.topleft)
            if gback_rect.collidepoint(mouse_pos):
                menu_scr.blit(back_hover, gback_rect.topleft)

        else:
            if tic_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, tic_rect.topleft)

            if othello_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, othello_rect.topleft)

            if four_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, four_rect.topleft)

            if settings_rect.collidepoint(mouse_pos):
                menu_scr.blit(hover_surface, settings_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   # exit

            if event.type == pygame.MOUSEBUTTONDOWN:

                if show_post_popup:
                    if play_again_rect.collidepoint(event.pos):
                        show_post_popup = False   # back to menu

                    elif analysis_rect.collidepoint(event.pos):
                        Get_graph()
                        graph_img = pygame.image.load("analysis.png").convert()
                        graph_img = pygame.transform.smoothscale(graph_img, (650, 350))
                        show_graph = True
                        show_post_popup = False

                    elif exit_rect.collidepoint(event.pos):
                        running = False   # quit game

                elif show_graph:
                    if gback_rect.collidepoint(event.pos):
                        show_graph = False   # back to menu

                else:
                    if tic_rect.collidepoint(event.pos):
                        if start_tic() == "post_game":
                            show_post_popup = True

                    elif othello_rect.collidepoint(event.pos):
                        if start_othello() == "post_game":
                            show_post_popup = True

                    elif four_rect.collidepoint(event.pos):
                        if start_connect4() == "post_game":
                            show_post_popup = True

                    elif settings_rect.collidepoint(event.pos):
                        Get_graph()
                        graph_img = pygame.image.load("analysis.png").convert()
                        graph_img = pygame.transform.smoothscale(graph_img, (650, 350))
                        show_graph = True

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
