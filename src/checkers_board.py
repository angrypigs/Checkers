from src.move import Move
from src.utils import *

class CheckersBoard:
    """
    Matrix representation of checkers board, with most of needed methods
    """

    def __init__(self) -> None:
        self.ENEMIES = {'b': 'wW', 'w': 'bB', 'B': 'Ww', 'W': 'Bb', 'O': ' '}
        self.moves : tuple[Move] = ()
        self.matrix : list[list[str]]
        self.turn = 'w'
        self.kill_flag = False
        self.row = 0
        self.col = 0

    def change_turn(self) -> str:
        self.turn = 'b' if self.turn == 'w' else 'w'
        return self.turn

    def __move(self, 
               pawn: tuple[int, int], 
               dest: tuple[int, int], 
               kill: tuple[int, int] | None = None) -> None:
        pawn_copy = self.matrix[pawn[0]][pawn[1]]
        self.matrix[dest[0]][dest[1]] = pawn_copy
        if (dest[0] == 0 and pawn_copy == 'w' or
            dest[0] == 7 and pawn_copy == 'b'):
            self.matrix[dest[0]][dest[1]] = pawn_copy.upper()
        if kill is not None:
            self.matrix[kill[0]][kill[1]] = 'O'
        self.matrix[pawn[0]][pawn[1]] = 'O'

    def reset_board(self) -> None:
        """
        Set board to it's initial state
        """
        self.matrix = []
        for i in range(3):
            self.matrix.append([('O' if (i + j) % 2 == 0 else 'b') for j in range(8)])
        for i in range(2):
            self.matrix.append(['O' for j in range(8)])
        for i in range(3):
            self.matrix.append([('w' if (i + j) % 2 == 0 else 'O') for j in range(8)])
 
    def select_pawn(self, row: int, col: int) -> tuple[Move | None, tuple[Move], bool]:
        """
        Select pawn / make move on given place

        Return tuple of:
        - done move (or None if move wasn't done) 
        - tuple of possible moves
        - flag informing about the need for image change for pawn (default False)
        """
        print(is_place_safe(self.matrix, row, col, self.matrix[row][col]))
        move_done = None
        for move in self.moves:
            # check if input coords are in one of possible moves from the last input
            if (row, col) == move.end:
                # check if move is a normal one (no kill)
                if move.is_not_kill():
                    self.__move((self.row, self.col), (row, col))
                    self.row, self.col = -1, -1
                    self.kill_flag = False
                    self.moves = ()
                    self.change_turn()
                else:
                    self.__move((self.row, self.col), (row, col), move.kill)
                    kills = possible_kills(self.matrix, row, col)
                    # check if after kill there are any more available
                    if len(kills) > 0:
                        self.kill_flag = True
                        self.moves = kills
                        self.row, self.col = row, col
                    else:
                        self.row, self.col = -1, -1
                        self.kill_flag = False
                        self.moves = ()
                        self.change_turn()
                move_done = move
                break
        else:
            if (row, col) == (-1, -1):
                turn = 'O'
            else:
                turn = self.matrix[row][col].lower()
            # otherwise if isn't any pawn in 'kill mode' and turn is equal to pawn under coords,
            # then set the current pawn to this coords and get it's possible moves
            if not self.kill_flag and turn == self.turn:
                self.row, self.col = row, col
                self.moves = possible_moves(self.matrix, row, col)
        return (move_done, self.moves)
