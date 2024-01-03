from pygame import Surface, Rect


class Button:

    def __init__(self, screen: Surface,
                 x: int, y: int,
                 img: Surface) -> None:
        self.screen = screen
        self.image = img
        self.coords = (x - (img.get_width() // 2),
                       y - (img.get_height() // 2))
        self.rect = Rect(self.coords, img.get_size())
        
    def draw(self) -> None:
        self.screen.blit(self.image, self.coords)
    
    def is_colliding(self, pos: tuple[int, int]) -> bool:
        if self.rect.collidepoint(pos):
            return True
        return False