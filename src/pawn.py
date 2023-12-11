class Pawn:

    def __init__(self, 
                 screen,
                 image,
                 start: tuple[int, int], 
                 x: int, 
                 y: int) -> None:
        self.screen = screen
        self.image = image
        self.BOARD_START = start
        self.x = x
        self.y = y
        self.screen_x = self.BOARD_START[0]+64*x
        self.screen_y = self.BOARD_START[1]+64*y
    
    def draw(self) -> None:
        self.screen.blit(self.image, (self.screen_x, self.screen_y))

    def move(self, coords: tuple[int, int]) -> None:
        self.y, self.x = coords
        self.screen_x = self.BOARD_START[0]+64*self.x
        self.screen_y = self.BOARD_START[1]+64*self.y