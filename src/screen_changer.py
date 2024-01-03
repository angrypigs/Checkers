from src.utils import lerp
from pygame.draw import rect
from pygame import Surface, SRCALPHA



class ScreenChanger:

    def __init__(self, screen, width: int, height: int) -> None:
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = screen
        self.anim = False
        self.fade_in = True
        self.alpha = 0
        self.rectangle = Surface((self.WIDTH, self.HEIGHT), SRCALPHA)
        rect(self.rectangle, (0, 0, 0, self.alpha,), (0, 0, self.WIDTH, self.HEIGHT))
    
    def __bool__(self) -> bool:
        return not self.anim

    def change(self, func) -> None:
        self.anim = True
        self.func = func

    def draw(self) -> None:
        self.screen.blit(self.rectangle, (0, 0))
        if self.anim:
            if self.fade_in:
                if self.alpha < 255:
                    self.alpha += 5
                else:
                    self.fade_in = False
                    self.func()
            else:
                if self.alpha > 0:
                    self.alpha -= 5
                else:
                    self.fade_in = True
                    self.anim = False
            self.rectangle.fill((0, 0, 0, self.alpha,))