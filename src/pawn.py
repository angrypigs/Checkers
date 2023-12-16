from src.utils import lerp



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
        self.ANIM_LIMIT = 10
        self.anim = False
        self._counter = 0
        self.x = x
        self.y = y
        self.screen_x = self.BOARD_START[0]+64*x
        self.screen_y = self.BOARD_START[1]+64*y
    
    def __bool__(self) -> bool:
        return self.anim

    def draw(self) -> None:
        self.screen.blit(self.image, (self.screen_x, self.screen_y))
        if self.anim:
            if self._counter == self.ANIM_LIMIT - 1:
                self.anim = False
            else:
                self._counter += 1
                self.screen_x = self.x_lerp[self._counter]
                self.screen_y = self.y_lerp[self._counter]

    def move(self, coords: tuple[int, int]) -> None:
        self.y, self.x = coords
        self.anim = True
        self.x_lerp = lerp(self.screen_x, 
                           self.BOARD_START[0] + 64 * self.x, 
                           self.ANIM_LIMIT,
                           True)
        self.y_lerp = lerp(self.screen_y, 
                           self.BOARD_START[1] + 64 * self.y, 
                           self.ANIM_LIMIT,
                           True)
        self.screen_x = self.x_lerp[0]
        self.screen_y = self.y_lerp[1]
        self._counter = 0
        print(self.x_lerp, self.y_lerp, "\n")
        