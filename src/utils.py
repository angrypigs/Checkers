import sys
from os import path
from src.move import Move

def res_path(rel_path: str) -> str:
    """
    Return path to file modified by auto_py_to_exe path if packed to exe already
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = sys.path[0]
    return path.normpath(path.join(base_path, rel_path))


def clamp(val: float, bottom: float, top: float) -> float:
    """
    Clamp val between bottom and top values
    """
    return max(min(val, top), bottom)


def lerp(a: float, 
         b: float, 
         steps: int,
         to_integers: bool = False
         ) -> tuple[float | int]:
    """
    Return tuple of values linear interpolated between 
    a and b in given steps, if to_integer is True then
    return list of int, not float
    """
    result = []
    for i in range(steps):
        t = i / (steps - 1)
        t = 1 - (1 - t) ** 2
        value = a + (b - a) * t
        if to_integers:
            value = int(value)
        result.append(value)
    return tuple(result)



ENEMIES = {'b': 'wW', 'w': 'bB', 'B': 'wW', 'W': 'bB', 'O': ' '}

def possible_kills(matrix: list[list[str]], row: int, col: int) -> tuple[Move]:
    """
    Return tuple of possible kill moves of a given place
    """
    moves = []
    dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    enemies = ENEMIES[matrix[row][col]]
    friends = f"{matrix[row][col].lower()}{matrix[row][col].upper()}"
    match matrix[row][col]:
        case "B" | "W":
            for d in range(4):
                a, b = row + dirs[d][0], col + dirs[d][1]
                flag = False
                while (0 <= a <= 7 and 
                        0 <= b <= 7 and 
                        (not flag or 
                        matrix[a][b] not in enemies) and
                        matrix[a][b] not in friends):
                    if flag:
                        moves.append(Move((row, col), (a, b), kill))
                    if matrix[a][b] in enemies:
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
                    matrix[a][b] in enemies and
                    matrix[c][d] == 'O'):
                    moves.append(Move((row, col), (c, d), (a, b)))
    return tuple(moves)


def possible_moves(matrix: list[list[str]], row: int, col: int) -> tuple[Move]:
    """
    Return tuple of all possible moves (with kills) of a given place
    """
    moves = []
    dirs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    match matrix[row][col]:
        case 'B' | 'W':
            for d in range(4):
                a, b = row + dirs[d][0], col + dirs[d][1]
                while (0 <= a <= 7 and 
                        0 <= b <= 7 and 
                        matrix[a][b] == 'O'):
                    moves.append(Move((row, col), (a, b), None))
                    a += dirs[d][0]
                    b += dirs[d][1]
        case 'b':
            if (0 <= row + 1 <= 7 and
                0 <= col - 1 <= 7 and
                matrix[row + 1][col - 1] == 'O'):
                moves.append(Move((row, col), (row + 1, col - 1), None))
            if (0 <= row + 1 <= 7 and
                0 <= col + 1 <= 7 and
                matrix[row + 1][col + 1] == 'O'):
                moves.append(Move((row, col), (row + 1, col + 1), None))
        case 'w':
            if (0 <= row - 1 <= 7 and
                0 <= col - 1 <= 7 and
                matrix[row - 1][col - 1] == 'O'):
                moves.append(Move((row, col), (row - 1, col - 1), None))
            if (0 <= row - 1 <= 7 and
                0 <= col + 1 <= 7 and
                matrix[row - 1][col + 1] == 'O'):
                moves.append(Move((row, col), (row - 1, col + 1), None))
    return tuple(moves) + possible_kills(matrix, row, col)

def move_simulation(matrix: list[list[str]], move: Move) -> list[list[str]]:
    new_matrix = [x[:] for x in matrix]
    pawn = new_matrix[move.start[0]][move.start[1]]
    if (pawn == 'b' and move.end[0] == 7 or
        pawn == 'w' and move.end[0] == 0):
        pawn = pawn.upper()
    new_matrix[move.end[0]][move.end[1]] = pawn
    new_matrix[move.start[0]][move.start[1]] = "O"
    if move.is_kill():
        new_matrix[move.kill[0]][move.kill[1]] = "O"
    return new_matrix

def kill_recursion(matrix: list[list[str]], 
                   row: int, col: int,
                   kills: tuple[Move] | None = None) -> tuple[list[Move], int]:
    """
    Recursively find all possible kills (with the next ones and next and etc...) of a given pawn in matrix
    """
    if kills is None:
        kills = possible_kills(matrix, row, col)
    all_kills = list(kills)
    next_kills_quantity = 0
    for kill in kills:
        new_matrix = [x[:] for x in matrix]

        new_matrix[kill.end[0]][kill.end[1]] = new_matrix[kill.start[0]][kill.start[1]]
        new_matrix[kill.start[0]][kill.start[1]] = "O"
        new_matrix[kill.kill[0]][kill.kill[1]] = "O"

        new_kills = possible_kills(new_matrix, kill.end[0], kill.end[1])
        if new_kills:
            recursion = kill_recursion(new_matrix, 
                                        kill.end[0], 
                                        kill.end[1], 
                                        new_kills)
            all_kills.extend(recursion[0])
            if recursion[1] > next_kills_quantity:
                next_kills_quantity = recursion[1]
    return (all_kills, next_kills_quantity + 1)

def is_place_safe(matrix: list[list[str]], row: int, col: int, pawn: str) -> bool:
    """
    Return bool depending of whether pawn on given coords can be killed by any enemy
    """
    kills : list[Move] = []
    for i in range(8):
        for j in range(8):
            if matrix[i][j] in ENEMIES[pawn]:
                new_kills = possible_kills(matrix, i, j)
                if new_kills:
                    kills.extend(kill_recursion([x[:] for x in matrix],
                                                i, j, new_kills)[0])
    for kill in kills:
        if (row, col) == kill.kill:
            return False
    return True
                

