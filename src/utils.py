import sys
from os import path

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
