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
        moves : list[Move] = []
        if self.kill_flag:
            moves = list(self.kills)
        else:
            for row in range(8):
                for col in range(8):
                    if self.matrix[row][col] in "bB":
                        moves.extend(possible_moves(self.matrix, row, col))
        weights = [0 for x in range(len(moves))]

        for index, move in enumerate(moves):
            pawn_safety = is_place_safe(self.matrix,
                                        move.start[0],
                                        move.start[1],
                                        self.matrix[move.start[0]][move.start[1]])
            dest_safety = is_place_safe(move_simulation(self.matrix, move), 
                                        move.end[0], 
                                        move.end[1], 
                                        self.matrix[move.start[0]][move.start[1]])
            if dest_safety:
                if pawn_safety:
                    weights[index] += 1
                else:
                    weights[index] += 2
            elif pawn_safety:
                weights[index] -= 1
            if move.is_kill():
                all_kills = kill_recursion(self.matrix, move.start[0], move.start[1])
                weights[index] += all_kills[1]
        print()
        moves_and_weights = list(zip(moves, weights))
        max_weight = max(weights)
        best_moves = tuple(x[0] for x in moves_and_weights if x[1] == max_weight)
        chosen_move = choice(best_moves)
        self.moves.append(chosen_move)
        self.matrix[chosen_move.end[0]][chosen_move.end[1]] = self.matrix[chosen_move.start[0]][chosen_move.start[1]]
        self.matrix[chosen_move.start[0]][chosen_move.start[1]] = "O"
        flag = False
        if chosen_move.is_kill():
            flag = True
            self.matrix[chosen_move.kill[0]][chosen_move.kill[1]] = "O"
        self.kills = possible_kills(self.matrix, 
                                    chosen_move.end[0], 
                                    chosen_move.end[1])
        if self.kills and flag:
            self.kill_flag = True
            self.__move()
        else:
            self.kill_flag = False

        
