from src.move import Move

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

    def __move(self, 
               pawn: tuple[int, int], 
               dest: tuple[int, int]) -> None:
        self.matrix[dest[0]][dest[1]] = self.matrix[pawn[0]][pawn[1]]
        self.matrix[pawn[0]][pawn[1]] = 'O'
        # print("move", pawn, dest)

    def __kill(self, 
               pawn: tuple[int, int], 
               dest: tuple[int, int], 
               kill: tuple[int, int]) -> None:
        self.matrix[dest[0]][dest[1]] = self.matrix[pawn[0]][pawn[1]]
        self.matrix[kill[0]][kill[1]] = 'O'
        self.matrix[pawn[0]][pawn[1]] = 'O'
        # print("kill", pawn, dest, kill)
    
    def __possible_kills(self, row: int, col: int) -> tuple[Move]:
        """
        Return tuple of possible kill moves of a given place
        """
        moves = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        enemies = self.ENEMIES[self.matrix[row][col]]
        match self.matrix[row][col]:
            case "B" | "W":
                for d in range(4):
                    a, b = row + dirs[d][0], col + dirs[d][1]
                    flag = False
                    while (0 <= a <= 7 and 
                           0 <= b <= 7 and 
                           (not flag or 
                            self.matrix[a][b] not in enemies)):
                        if flag:
                            moves.append(Move((row, col), (a, b), kill))
                        if self.matrix[a][b] in enemies:
                            flag = True
                            kill = (a, b)
                        a += dirs[d][0]
                        b += dirs[d][1]
            case "b" | "w":
                for d in range(4):
                    a, b = row + dirs[d][0], col + dirs[d][1]
                    c, d = row + 2 * dirs[d][0], col + 2 * dirs[d][1]
                    if (0 <= c <= 7 and
                        0 <= d <= 7 and
                        self.matrix[a][b] in enemies and
                        self.matrix[c][d] == 'O'):
                        moves.append(Move((row, col), (c, d), (a, b)))
        return tuple(moves)

    def __possible_moves(self, row: int, col: int) -> tuple[Move]:
        """
        Return tuple of all possible moves (with kills) of a given place
        """
        moves = []
        dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        match self.matrix[row][col]:
            case 'B' | 'W':
                for d in range(4):
                    a, b = row + dirs[d][0], col + dirs[d][1]
                    while (0 <= a <= 7 and 
                           0 <= b <= 7 and 
                            self.matrix[a][b] == 'O'):
                        moves.append(Move((row, col), (a, b), None))
                        a += dirs[d][0]
                        b += dirs[d][1]
            case 'b':
                if (0 <= row + 1 <= 7 and
                    0 <= col - 1 <= 7 and
                    self.matrix[row + 1][col - 1] == 'O'):
                    moves.append(Move((row, col), (row + 1, col - 1), None))
                if (0 <= row + 1 <= 7 and
                    0 <= col + 1 <= 7 and
                    self.matrix[row + 1][col + 1] == 'O'):
                    moves.append(Move((row, col), (row + 1, col + 1), None))
            case 'w':
                if (0 <= row - 1 <= 7 and
                    0 <= col - 1 <= 7 and
                    self.matrix[row - 1][col - 1] == 'O'):
                    moves.append(Move((row, col), (row - 1, col - 1), None))
                if (0 <= row - 1 <= 7 and
                    0 <= col + 1 <= 7 and
                    self.matrix[row - 1][col + 1] == 'O'):
                    moves.append(Move((row, col), (row - 1, col + 1), None))
        return tuple(moves) + self.__possible_kills(row, col)

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

    def swap(self) -> str:
        self.turn = 'b' if self.turn == 'w' else 'w'
        return self.turn
 
    def select_pawn(self, row: int, col: int) -> Move | tuple[Move]:
        """
        Select pawn / make move on given place
        """
        moves = None
        for move in self.moves:
            if (row, col) == move.end:
                if move.is_not_kill():
                    self.__move((self.row, self.col), (row, col))
                    self.row, self.col = -1, -1
                    self.kill_flag = False
                    self.moves = ()
                    self.swap()
                else:
                    self.__kill((self.row, self.col), (row, col), move.kill)
                    kills = self.__possible_kills(row, col)
                    for kill in kills:
                        print(kill)
                    if len(kills) > 0:
                        self.kill_flag = True
                        self.moves = kills
                        self.row, self.col = row, col
                    else:
                        self.row, self.col = -1, -1
                        self.kill_flag = False
                        self.moves = ()
                        self.swap()
                moves = move
                break
        else:
            if (row, col) == (-1, -1):
                turn = 'O'
            else:
                turn = self.matrix[row][col].lower()
            if not self.kill_flag and turn == self.turn:
                self.row, self.col = row, col
                self.moves = self.__possible_moves(row, col)
                moves = self.moves
        print(self.row, self.col)
        print()
        for i in self.matrix:
            print(i)
        return moves

        
         
    
