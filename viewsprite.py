import pygame

from res import CResourse
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
        :param dx: смещение положения по x
        :param dy: смещения положения по y
        """
        self.rect.x += dx
        self.rect.y += dy
        (ws, hs) = self.rect.size
        (x, y, ww, hw) = self._static_param.game_win_rect
        if (self.rect.x < x - ws) or (self.rect.x > x + ww) or (self.rect.y < y - hs) or (self.rect.y > y + hw):
            self.kill()


# ----------------------------------------------------------------------------------------------------------------------

class CViewSprPlatform(pygame.sprite.Sprite):
    """
    Рисование спрайтов для движущейся платформы.
    """

    def __init__(self, img_constr, img_2, x, y, offset, group, group_st):
        pygame.sprite.Sprite.__init__(self)
        self._static_param = CStaticParam()
        self.image, self.rect = img_2, img_2.get_rect()
        self.rect.x, self.rect.y = x, y
        self.add(group)
        self._img_constr = img_constr
        self._start_y = y
        self._offset = offset
        self._move_to = True
        self._group_st = group_st
        self._stack = []
        self._delay = CResourse.MAZE_PLATFORM_DELAY

    def update(self, dx, dy):
        """
        Изменение состояния спрайта.
        :param dx: смещение положения по x
        :param dy: смещения положения по y
        """
        self.rect.x += dx
        self.rect.y += dy
        self._start_y += dy
        (ws, hs) = self.rect.size
        (x, y, ww, hw) = self._static_param.game_win_rect
        if (self.rect.x < x - ws) or (self.rect.x > x + ww) or (self.rect.y < y - hs) or (self.rect.y > y + hw):
            self.kill()
        self._delay -= 1
        if self._delay < 1:
            self._delay = CResourse.MAZE_PLATFORM_DELAY
            if self._move_to:
                # Платформа увеличивается.
                self._platforma_increases()
            else:
                # Платформа уменьшается.
                self._platforma_decreases()

    def _platforma_increases(self):
        """
        Увеличение размера платформы.
        """
        self.rect.y += self._offset
        if pygame.sprite.spritecollideany(self, self._group_st):
            self.rect.y -= self._offset
            self._move_to = False
        else:
            new_img = pygame.Surface((self._img_constr[1][2], self._img_constr[1][3]))
            new_img.blit(self._img_constr[0], (0, 0), self._img_constr[1])
            self._stack.append(CViewSprStatic(new_img, self.rect.x, self.rect.y - self._offset, self._group_st))

    def _platforma_decreases(self):
        """
        Уменьшение размера платформы.
        """
        if self.rect.y == self._start_y:
            self._move_to = True
        else:
            self.rect.y -= self._offset
            if len(self._stack) > 0:
                spr = self._stack.pop()
                spr.kill()


# ----------------------------------------------------------------------------------------------------------------------

class CViewSprShooter(pygame.sprite.Sprite):

    def __init__(self, img, x, y, offset, group, img_constr, group_d):
        pygame.sprite.Sprite.__init__(self)
        self._static_param = CStaticParam()
        self.image, self.rect = img, img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.add(group)
        self._group_st = group
        self._group_dy = group_d
        self._offset = offset
        self._img_constr = img_constr
        self._is_fire = True

    def update(self, dx, dy):
        """
        Изменение состояния спрайта.
        :param dx: смещение положения по x
        :param dy: смещения положения по y
        """
        self.rect.x += dx
        self.rect.y += dy
        (ws, hs) = self.rect.size
        (x, y, ww, hw) = self._static_param.game_win_rect
        if (self.rect.x < x - ws) or (self.rect.x > x + ww) or (self.rect.y < y - hs) or (self.rect.y > y + hw):
            self.kill()
        else:
            if self._is_fire:
                self._is_fire = False
                # Создание выстрела.
                new_img = pygame.Surface((self._img_constr[1][2], self._img_constr[1][3]))
                new_img.blit(self._img_constr[0], (0, 0), self._img_constr[1])
                CViewSprFire(new_img, self.rect.x, self.rect.y + self._offset * hs, self._offset, ws,
                             self._group_dy, self._group_st, self.new_fire)

    def new_fire(self):
        self._is_fire = True


# ----------------------------------------------------------------------------------------------------------------------

class CViewSprFire(pygame.sprite.Sprite):

    def __init__(self, img, x, y, dy, width, group, gr_tst, fun_fire):
        pygame.sprite.Sprite.__init__(self)
        self._static_param = CStaticParam()
        self.image, self.rect = img, img.get_rect()
        t = int((width - self.rect[2]) / 2)
        self.rect.x, self.rect.y = x + t, y
        self.add(group)
        self._group_st = gr_tst
        self._dy = dy
        self._fun_fire = fun_fire

    def update(self, dx, dy):
        """
        Изменение состояния спрайта.
        :param dx: смещение положения по x
        :param dy: смещения положения по y
        """
        self.rect.x += dx
        self.rect.y += self._dy * CResourse.GAME_FIRE_SPEED
        (ws, hs) = self.rect.size
        (x, y, ww, hw) = self._static_param.game_win_rect
        if (self.rect.x < x - ws) or (self.rect.x > x + ww) or (self.rect.y < y - hs) or (self.rect.y > y + hw) \
                or pygame.sprite.spritecollideany(self, self._group_st):
            self._fun_fire()
            self.kill()
