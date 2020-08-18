import pygame

from res import CResourse, full_path


class CGameFlayerPlayer:
    """
    Класс управления летуном.
    """

    def __init__(self, x, y, g, speed_vert, speed_fly):
        """
        Инициализация управления летуном.
        :param x: начальная координата x
        :param y: начальная координата y
        :param g: параметр ускорения падения летуна вниз
        :param speed_vert: смещение при перемещении вверх или вниз
        :param speed_fly: скрость махания крыльями
        """
        self._is_move = self._y = self._curr_pos_type = 0
        self._curr_vert = self._cur_pos_fly = 0.0
        self._str_x, self._str_y = x, y
        self._speed_vert, self._g = speed_vert, g
        self._speed_fly = speed_fly
        self._img_bird = pygame.image.load(full_path(CResourse.PATH_IMG_BIRD))
        self._width, self._height = self._img_bird.get_size()
        self._width = int(self._width / 3)
        self._r = (
            (0, 0, self._width, self._height),
            (self._width, 0, self._width, self._height),
            (2 * self._width, 0, self._width, self._height),
        )

    def start(self):
        """
        Инициализация в начале игры.
        """
        self._curr_vert = self._cur_pos_fly = 0.0
        self._y = self._str_y
        self._speed_fly = abs(self._speed_fly)
        self._curr_pos_type = 1
        self._is_move = 0

    @property
    def pos(self):
        return self._str_x, self._y

    @property
    def size(self):
        return self._width, self._height

    @property
    def is_move(self):
        return self._is_move

    @is_move.setter
    def is_move(self, value: int):
        self._is_move = value

    def paint(self, sc):
        """
        Рисование летуна.
        :param sc: контекст устройства.
        """
        sc.blit(self._img_bird, self.pos, self._r[self._curr_pos_type])

    def next_state(self):
        """
        Расчёт нового состояния летуна.
        """
        self._curr_vert += self._g + self._is_move * self._speed_vert
        t = int(self._curr_vert)
        self._curr_vert -= t
        self._y += t
        self._cur_pos_fly += self._speed_fly
        if (self._cur_pos_fly >= 2.0) or (self._cur_pos_fly <= -2.0):
            self._speed_fly = -self._speed_fly
        if self._cur_pos_fly >= 1.0:
            self._curr_pos_type = 2
        elif self._cur_pos_fly <= -1.0:
            self._curr_pos_type = 0
        else:
            self._curr_pos_type = 1
