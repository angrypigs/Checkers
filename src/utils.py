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
