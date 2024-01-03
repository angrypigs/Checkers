from src.checkers_board import CheckersBoard
from src.move import Move
from src.utils import *

from threading import Thread
from random import choice



class ComputerSide:

    def __init__(self, board: CheckersBoard) -> None:
        self.board = board
        self.moves : list[Move] = []
        self.kill_flag = False

    def computer_move(self) -> None:
        """
        Start Thread calculating computer move,
        which will be added on top of moves list
        """
        self.matrix = [x[:] for x in self.board.matrix]
        Thread(target = self.__move, daemon = True).start()

    def __move(self) -> None:
        """
        Calculate and return move from computer side
        """
        # getting all possible moves depending of whether side is in kill mode
        moves : list[Move] = []
        if self.kill_flag:
            moves = list(self.kills)
        else:
            for row in range(8):
                for col in range(8):
                    if self.matrix[row][col] in "bB":
                        moves.extend(possible_moves(self.matrix, row, col))
        # list to storage moves values
        weights = [0 for x in range(len(moves))]
        # going through all moves and getting their data
        for index, move in enumerate(moves):
            matrix_after_move = move_simulation(self.matrix, move)
            pawn_safety = is_place_safe(self.matrix,
                                        move.start[0],
                                        move.start[1],
                                        self.matrix[move.start[0]][move.start[1]])
            dest_safety = is_place_safe(matrix_after_move, 
                                        move.end[0], 
                                        move.end[1], 
                                        self.matrix[move.start[0]][move.start[1]])
            # evaluate moves
            if dest_safety:
                if pawn_safety:
                    weights[index] += 1
                else:
                    weights[index] += 4
            elif pawn_safety:
                weights[index] -= 2
            if move.is_kill():
                all_kills = kill_recursion(self.matrix, move.start[0], move.start[1])
                weights[index] += all_kills[1] * 2
            if move.end[1] in (0, 7):
                weights[index] += 1
            if (self.matrix[move.start[0]][move.start[1]] == 'b' and
                move.end[0] == 7):
                weights[index] += 1
            for neighbor in ((-1, 1), (-1, -1), (1, -1), (1, 1)):
                a, b = move.end[0] + neighbor[0], move.end[1] + neighbor[1]
                if (0 <= a <= 7 and 0 <= b <= 7 and
                    (a, b) != move.start and
                    self.matrix[a][b] in 'bB'):
                    neighbor_before = is_place_safe(self.matrix,
                                                    a, b, self.matrix[a][b])
                    neighbor_after = is_place_safe(matrix_after_move,
                                                   a, b, self.matrix[a][b])
                    if not neighbor_before and neighbor_after:
                        weights[index] += 3


        # taking move with the greatest value
        moves_and_weights = list(zip(moves, weights))
        max_weight = max(weights)
        best_moves = tuple(x[0] for x in moves_and_weights if x[1] == max_weight)
        chosen_move = choice(best_moves)
        self.moves.append(chosen_move)
        self.matrix = move_simulation(self.matrix, chosen_move)
        self.kills = possible_kills(self.matrix, 
                                    chosen_move.end[0], 
                                    chosen_move.end[1])
        if self.kills and chosen_move.is_kill():
            self.kill_flag = True
            self.__move()
        else:
            self.kill_flag = False

        
