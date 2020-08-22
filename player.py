import pygame

from res import CResourse
from static import CStaticParam


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
        self._static_param = CStaticParam()
        self._image, r = CStaticParam.load_image(CResourse.PATH_IMG_BIRD)
        w = int(r[2] / 3)
        self._str_pos = (x, y)
        self._rect = pygame.Rect(x, y, w, r[3])
        self._is_move = self._y = self._curr_pos_type = 0
        self._curr_vert = self._cur_pos_fly = 0.0
        self._speed_vert, self._g = speed_vert, g
        self._speed_fly = speed_fly
        self._spr_win = (
            (0, 0, w, r[3]),
            (w, 0, w, r[3]),
            (2 * w, 0, w, r[3]),
        )

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, r):
        self._rect = r

    @property
    def size(self):
        return self._rect[2], self._rect[3]

    @property
    def pos(self):
        return self._rect[0], self._rect[1]

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
        sc.blit(self._image, self.pos, self._spr_win[self._curr_pos_type])

    def start(self):
        """
        Инициализация в начале игры.
        """
        self._curr_vert = self._cur_pos_fly = 0.0
        (self._rect[0], self._rect[1]) = self._str_pos
        self._speed_fly = abs(self._speed_fly)
        self._curr_pos_type = 1
        self._is_move = 0

    def pos_to_middle(self):
        """
        Выставляет среднюю позицию для игрока.
        """
        (_, yw, _, hw) = self._static_param.game_win_rect
        self._rect[1] = int(yw + hw / 2)

    def update(self):
        """
        Расчёт нового состояния летуна.
        """
        self._curr_vert += self._g + self._is_move * self._speed_vert
        t = int(self._curr_vert)
        self._curr_vert -= t
        self._rect[1] += t
        self._cur_pos_fly += self._speed_fly
        if (self._cur_pos_fly >= 2.0) or (self._cur_pos_fly <= -2.0):
            self._speed_fly = -self._speed_fly
        if self._cur_pos_fly >= 1.0:
            self._curr_pos_type = 2
        elif self._cur_pos_fly <= -1.0:
            self._curr_pos_type = 0
        else:
            self._curr_pos_type = 1
        (_, yw, _, hw) = self._static_param.game_win_rect
        if self._rect[1] < yw:
            self._rect[1] = yw
        elif self._rect[1] > yw + hw - self._rect[3]:
            self._rect[1] = yw + hw - self._rect[3]
