import pygame

from src.checkers_board import CheckersBoard
from src.screen_changer import screenChanger
from src.pawn import Pawn
from src.move import Move
from src.utils import *



class Game:

    def __init__(self) -> None:
        self.WIDTH = 700
        self.HEIGHT = 700
        self.BOARD_START = ((self.WIDTH-512)//2, (self.HEIGHT-512)//2)
        self.BOARD_START = (20, 20)
        self.FPS = 60
        self.run = True
        self.ingame = False
        
        self.pawns : list[Pawn] = []
        self.moves : tuple[tuple[int, int]] = ()
        self.board = CheckersBoard()
        self.board.reset_board()
        self.matrix = self.board.matrix
        self.__init_assets()
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.screen_changer = screenChanger(self.screen, self.WIDTH, self.HEIGHT)
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
            self.screen_changer.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def handle_events(self) -> None:
        """
        Handle events in main loop
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if (event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1 and
                not any(self.pawns) and
                self.screen_changer):
                a = (event.pos[1] - self.BOARD_START[1]) // 64
                b = (event.pos[0] - self.BOARD_START[0]) // 64
                if 0 <= a <= 7 and 0 <= b <= 7:
                    self.handle_moves(a, b)

    def handle_moves(self, a: int, b: int) -> None:
        """
        Handle board input
        """
        move = self.board.select_pawn(a, b)
        if move[0] is not None:
            self.moves = ()
            pawn_to_remove = None
            for pawn in self.pawns:
                if (pawn.y, pawn.x) == move[0].start:
                    pawn.move(move[0].end)
                    pawn.image = self.images[self.matrix[move[0].end[0]][move[0].end[1]]]
                if (pawn.y, pawn.x) == move[0].kill:
                    pawn_to_remove = pawn
            if pawn_to_remove is not None:
                self.pawns.remove(pawn_to_remove)
        self.moves = tuple([x.end for x in move[1]])


    def draw_game(self) -> None:
        """
        Draw game components
        """
        self.screen.blit(self.images["battlefield"], self.BOARD_START)
        for pos in self.moves:
            color = (211, 24, 24, 120) if self.board.turn == 'b' else (24, 107, 211, 120)
            pygame.draw.rect(self.screen, 
                             color,
                             (self.BOARD_START[0]+pos[1]*64,
                             self.BOARD_START[1]+pos[0]*64,
                             64, 64))
        for pawn in self.pawns:
            pawn.draw()
        # for i in range(8):
        #     for j in range(8):
        #         match self.matrix[i][j]:
        #             case 'b':
        #                 color = (206, 68, 22)
        #             case 'w':
        #                 color = (22, 117, 206)
        #             case 'B':
        #                 color = (156, 50, 15)
        #             case 'W':
        #                 color = (14, 84, 149)
        #             case _:
        #                 color = (255, 255, 255)
        #         pygame.draw.rect(self.screen, color,
        #                          (540+j*18, 540+i*18, 18, 18))
    
    def __init_assets(self) -> None:
        """
        Create dict with assets
        """
        self.images = {
            "battlefield": pygame.image.load(res_path("assets/battlefield.png")),
            "w": pygame.image.load(res_path("assets/blue_top.png")),
            "W": pygame.image.load(res_path("assets/blue_bottom.png")),
            "b": pygame.image.load(res_path("assets/red_top.png")),
            "B": pygame.image.load(res_path("assets/red_bottom.png"))
        }
        