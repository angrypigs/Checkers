import pygame

from src.checkers_board import CheckersBoard
from src.pawn import Pawn
from src.move import Move
from src.utils import *


class Game:

    def __init__(self) -> None:
        self.WIDTH = 700
        self.HEIGHT = 700
        # self.BOARD_START = ((self.WIDTH-512)//2, (self.HEIGHT-512)//2)
        self.BOARD_START = (20, 20)
        self.FPS = 60
        self.run = True
        self.pawns : list[Pawn] = []
        self.board = CheckersBoard()
        self.board.reset_board()
        self.matrix = self.board.matrix
        self.__init_assets()
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        for i in range(8):
            for j in range(8):
                pawn = self.board.matrix[i][j]
                if pawn != 'O':
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
                self.handle_moves(a, b)

    def handle_moves(self, a: int, b: int) -> None:
        if 0 <= a <= 7 and 0 <= b <= 7:
            move = self.board.select_pawn(a, b)
            if isinstance(move, Move):
                for pawn in self.pawns:
                    if (pawn.y, pawn.x) == move.start:
                        pawn.move(move.end)
                    if (pawn.y, pawn.x) == move.kill:
                        self.pawns.remove(pawn)


    def draw_game(self) -> None:
        self.screen.blit(self.images["battlefield"], self.BOARD_START)
        for pawn in self.pawns:
            pawn.draw()
        for i in range(8):
            for j in range(8):
                match self.matrix[i][j]:
                    case 'b':
                        color = (206, 68, 22)
                    case 'w':
                        color = (22, 117, 206)
                    case _:
                        color = (255, 255, 255)
                pygame.draw.rect(self.screen, color,
                                 (540+j*18, 540+i*18, 18, 18)
                                 )
        
    
    def __init_assets(self) -> None:
        self.images = {
            "battlefield": pygame.image.load(res_path("assets/battlefield.png")),
            "w": pygame.image.load(res_path("assets/blue_top.png")),
            "W": pygame.image.load(res_path("assets/blue_bottom.png")),
            "b": pygame.image.load(res_path("assets/red_top.png")),
            "B": pygame.image.load(res_path("assets/red_bottom.png"))
        }
        