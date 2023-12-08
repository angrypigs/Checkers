import pygame

from src.checkers_board import CheckersBoard


class Game:

    def __init__(self) -> None:
        self.board = CheckersBoard()
        self.board.reset_board()
        