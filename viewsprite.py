import pygame

from static import CStaticParam


class CViewSprStatic(pygame.sprite.Sprite):
    """
    Рисование спрайтов для статических объектов.
    """

    def __init__(self, img, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self._static_param = CStaticParam()
        self.image, self.rect = img, img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.add(group)

    def update(self, dx, dy):
        """
        Изменение состояния спрайта.
        """
        self.rect.x += dx
        self.rect.y += dy
        (ws, hs) = self.rect.size
        (x, y, ww, hw) = self._static_param.game_win_rect
        if (self.rect.x < x - ws) or (self.rect.x > x + ww) or (self.rect.y < y - hs) or (self.rect.y > y + hw):
            self.kill()

# ----------------------------------------------------------------------------------------------------------------------

