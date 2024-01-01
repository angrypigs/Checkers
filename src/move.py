class Move:

    def __init__(self, 
                 start: tuple[int, int], 
                 end: tuple[int, int],
                 kill: tuple[int, int] | None) -> None:
        self.start = start
        self.end = end
        self.kill = kill
    
    def is_kill(self) -> bool:
        return self.kill is not None

    def __str__(self) -> str:
        return f"{self.start} {self.end} {self.kill}"