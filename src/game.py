import pygame

from src.checkers_board import CheckersBoard
from src.pawn import Pawn
from src.utils import *


class Game:

    def __init__(self) -> None:
        self.WIDTH = 700
        self.HEIGHT = 700
        self.BOARD_START = ((self.WIDTH-512)//2, (self.HEIGHT-512)//2)
        self.FPS = 60
        self.run = True
        self.pawns : list[Pawn] = []
        self.board = CheckersBoard()
        self.board.reset_board()
        self.__init_assets()
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        for i in range(8):
            for j in range(8):
                pawn = self.board.matrix[i][j]
                if pawn != '':
                    self.pawns.append(Pawn(self.screen, 
                                           self.images[pawn], 
                                           self.BOARD_START,
                                           j, i))
        while self.run:
            self.screen.fill((0, 0, 0))
            self.handle_events()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                a = (event.pos[1] - self.BOARD_START[1]) // 64
                b = (event.pos[0] - self.BOARD_START[0]) // 64
                if 0 <= a <= 7 and 0 <= b <= 7:
                    self.board.select_pawn(a, b)

    def draw_game(self) -> None:
        self.screen.blit(self.images["battlefield"], self.BOARD_START)
        for pawn in self.pawns:
            pawn.draw()
    
    def __init_assets(self) -> None:
        self.images = {
            "battlefield": pygame.image.load(res_path("assets/battlefield.png")),
            "w": pygame.image.load(res_path("assets/blue_top.png")),
            "W": pygame.image.load(res_path("assets/blue_bottom.png")),
            "b": pygame.image.load(res_path("assets/red_top.png")),
            "B": pygame.image.load(res_path("assets/red_bottom.png"))
        }
        