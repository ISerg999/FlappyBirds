import pygame

from res import CResourse
from static import CStaticParam


class CGame:
    """
    Класс управляющий игровым процессом.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        # Ссылка на объект рисующий фон игры.
        self._game_bg = CGameBG(CResourse.PATH_BASE_RESOURSE + CResourse.PATH_STARRY_SKY_SHORT)
        self.start()

    def start(self):
        """
        Начальная инициализация игры.
        """
        self._game_bg.start(0.5)
        self._static_param.game_life = 3

    def event_handling(self, event):
        """
        Обработка события игрового процесса.
        :param event: обрабатываемое событие
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return -1
        return 0

    def paint(self, sc):
        """
        Рисование всей игры.
        :param sc: контекст устройства.
        """
        self._game_bg.paint(sc)

    def next_state(self):
        """
        Вычисление нового состояния игры.
        """
        self._game_bg.next_state()


# ----------------------------------------------------------------------------------------------------------------------

class CGameInfoLine:
    """
    Класс вывода информационной линии во время игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._static_param.game_life = 0
        self._full_rect = (0, 0, self._static_param.full_size[0], self._static_param.game_info_line_size)
        self._img_life = pygame.image.load(CResourse.PATH_BASE_RESOURSE + CResourse.PATH_GAME_HEART)
        self._life_width, self._life_height = self._img_life.get_size()
        self._life_dy = int((self._static_param.game_info_line_size - self._life_height) / 2)

    def paint(self, sc):
        """
        Рисование информационной линии.
        :param sc: контекст устройства.
        """
        pygame.draw.rect(sc, CResourse.COLOR_BLACK, self._full_rect)
        pygame.draw.rect(sc, CResourse.COLOR_WHITE, self._full_rect, 1)
        r = self._img_life.get_rect()
        r[0], r[1] = self._static_param.full_size[0] - self._life_width - 3, self._life_dy
        for i in range(self._static_param.game_life):
            # Рисование сердечек.
            sc.blit(self._img_life, r)
            r[0] -= self._life_width + 2


# ----------------------------------------------------------------------------------------------------------------------

class CGameBG:
    """
    Класс вывода заднего фона во время игры.
    """

    def __init__(self, img_name, offset: float = 0.0):
        self._static_param = CStaticParam()
        self._offset = self._cur_offset = 0.0
        self._cur_x = 0
        surf = pygame.image.load(img_name)
        self._width, self._height = surf.get_size()
        self._bg_img = pygame.Surface((self._width * 2, self._height))
        self._bg_img.blit(surf, (0, 0, self._width, self._height))
        self._bg_img.blit(surf, (self._width, 0, self._width, self._height))
        self.start(offset)

    def start(self, offset):
        """
        Базовая инициализация вывода фона.
        :param offset: начальная скорость смещения фона
        """
        self._cur_x = 0
        self._offset = offset
        self._cur_offset = 0.0

    def paint(self, sc):
        """
        Рисование заднего фона игры.
        :param sc: контекст устройства.
        """
        r = self._bg_img.get_rect()
        r[1] += self._static_param.game_info_line_size
        r[0] = self._cur_x
        sc.blit(self._bg_img, r)

    def next_state(self):
        """
        Смещение заднего фона игры.
        """
        self._cur_offset += self._offset
        t = int(self._cur_offset)
        self._cur_offset = self._cur_offset - t
        if t > 0:
            self._cur_x -= t
            if self._cur_x <= -self._width:
                self._cur_x += self._width
            elif self._cur_x >= self._width:
                self._cur_x -= self._width

    def change_add_offset(self, delta):
        """
        Изменение скорости смещения игры.
        :param delta: изменение скорости смещения
        """
        self._offset += delta
