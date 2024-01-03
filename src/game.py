import pygame

from src.checkers_board import CheckersBoard
from src.computer_side import ComputerSide
from src.screen_changer import ScreenChanger
from src.button import Button
from src.pawn import Pawn
from src.utils import *



class Game:

    def __init__(self) -> None:
        self.WIDTH = 700
        self.HEIGHT = 700
        self.BOARD_START = ((self.WIDTH - 512) // 2, (self.HEIGHT - 512) // 2)
        # self.BOARD_START = (20, 20)
        self.FPS = 60
        self.run = True
        self.scene = "menu"
        self.pawns : list[Pawn] = []
        self.moves : tuple[tuple[int, int]] = ()
        self.board = CheckersBoard()
        self.computer_side = ComputerSide(self.board)
        self.board.reset_board()
        self.matrix = self.board.matrix
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Checkers game")
        self.screen_changer = ScreenChanger(self.screen, self.WIDTH, self.HEIGHT)
        self.clock = pygame.time.Clock()
        self.__init_assets()
        for i in range(8):
            for j in range(8):
                pawn = self.board.matrix[i][j]
                if pawn != 'O':
                    self.pawns.append(Pawn(self.screen, 
                                           self.IMAGES[pawn], 
                                           self.BOARD_START,
                                           j, i))
        while self.run:
            self.screen.fill((189, 179, 116))
            self.handle_events()
            match self.scene:
                case "game":
                    self.draw_game()
                case "over":
                    self.over_btn.draw()
                case "menu":
                    self.screen.blit(self.IMAGES["logo"], (self.WIDTH // 2 - 256, 40))
                    self.one_btn.draw()
                    self.two_btn.draw()
            self.screen_changer.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def anim(self) -> bool:
        return not any(self.pawns) and self.screen_changer

    def change_scene(self, scene: str,
                     computer: bool | None = None) -> None:
        self.scene = scene
        if computer is not None:
            self.board.computer_mode = computer

    def handle_events(self) -> None:
        """
        Handle events in main loop
        """
        if self.scene == "game":
            if (self.board.computer_mode and
                len(self.computer_side.moves) > 0 and
                self.anim()):
                move = self.computer_side.moves.pop(0)
                self.board.row, self.board.col = move.start
                self.board.handle_move(move, True)
                self.handle_pawns(move)
            if self.board.turn == 'c':
                self.board.turn = 'w'
                self.computer_side.computer_move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if (event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1 and
                self.anim()):
                if self.scene == "game":
                    a = (event.pos[1] - self.BOARD_START[1]) // 64
                    b = (event.pos[0] - self.BOARD_START[0]) // 64
                    if 0 <= a <= 7 and 0 <= b <= 7:
                        self.handle_moves(a, b)
                elif (self.scene == "over" and 
                      self.over_btn.is_colliding(event.pos)):
                    self.screen_changer.change(lambda: self.change_scene("menu"))
                elif self.scene == "menu":
                    if self.one_btn.is_colliding(event.pos):
                        self.screen_changer.change(lambda: self.change_scene("game", True))
                    elif self.two_btn.is_colliding(event.pos):
                        self.screen_changer.change(lambda: self.change_scene("game", False))

    def handle_pawns(self, move: Move) -> None:
        pawn_to_remove = None
        for pawn in self.pawns:
            if (pawn.y, pawn.x) == move.start:
                pawn.move(move.end)
                pawn.image = self.IMAGES[self.matrix[move.end[0]][move.end[1]]]
            if (pawn.y, pawn.x) == move.kill:
                pawn_to_remove = pawn
        if pawn_to_remove is not None:
            self.pawns.remove(pawn_to_remove)

    def handle_moves(self, a: int, b: int) -> None:
        """
        Handle board input
        """
        moves = self.board.board_input(a, b)
        if moves[0] is not None:
            self.handle_pawns(moves[0])
        self.moves = tuple([x.end for x in moves[1]])

    def draw_game(self) -> None:
        """
        Draw game components
        """
        self.screen.blit(self.IMAGES["battlefield"], self.BOARD_START)
        for pos in self.moves:
            color = (211, 24, 24, 120) if self.board.turn == 'b' else (24, 107, 211, 120)
            pygame.draw.rect(self.screen, 
                             color,
                             (self.BOARD_START[0] + pos[1] * 64,
                             self.BOARD_START[1] + pos[0] * 64,
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
        Create assets and objects constants
        """
        self.IMAGES = {
            "battlefield": pygame.image.load(res_path("assets/battlefield.png")),
            "w": pygame.image.load(res_path("assets/blue_top.png")),
            "W": pygame.image.load(res_path("assets/blue_bottom.png")),
            "b": pygame.image.load(res_path("assets/red_top.png")),
            "B": pygame.image.load(res_path("assets/red_bottom.png")),
            "button": pygame.image.load(res_path("assets/button.png")),
            "logo": pygame.image.load(res_path("assets/logo.png"))
        }
        self.over_btn = Button(self.screen, 
                            self.WIDTH // 2,
                            self.HEIGHT // 2,
                            self.IMAGES["button"])
        self.one_btn = Button(self.screen, 
                            self.WIDTH // 2,
                            self.HEIGHT // 2,
                            self.IMAGES["button"])
        self.two_btn = Button(self.screen, 
                            self.WIDTH // 2,
                            self.HEIGHT // 2 + 200,
                            self.IMAGES["button"])
