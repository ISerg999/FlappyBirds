import os

import pygame

from res import CResourse


class CStaticParam:
    """
    Класс статических параметров игры. Синглтон.
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CStaticParam, cls).__new__(cls)
        return cls.instance

    # Словарь статических параметров.
    _dict_object = {}

    # Список объектов задающих внешний вид рисования лабиринта.
    _list_maze_parametr = []
    # Список объектов задающих кодирование самого лабиринта.
    _list_maze_code = []

    # Параметры размера всего окна.
    @property
    def full_size(self):
        return self._dict_object.get(CResourse.WINDOW_FULL_SIZE)

    @full_size.setter
    def full_size(self, value):
        if CResourse.WINDOW_FULL_SIZE in self._dict_object:
            self._dict_object[CResourse.WINDOW_FULL_SIZE] = value
        else:
            self._dict_object.setdefault(CResourse.WINDOW_FULL_SIZE, value)

    # Параметры размера игрового окна.
    @property
    def game_win_rect(self):
        return self._dict_object.get(CResourse.GAME_WINDOW_RECT)

    @game_win_rect.setter
    def game_win_rect(self, value):
        if CResourse.GAME_WINDOW_RECT in self._dict_object:
            self._dict_object[CResourse.GAME_WINDOW_RECT] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_WINDOW_RECT, value)

    # Размер игрового окна в спрайтовых размеров (по умолчанию 40x20)
    @property
    def game_win_spr_size(self):
        return self._dict_object.get(CResourse.GAME_WIN_SPR_SIZE)

    @game_win_spr_size.setter
    def game_win_spr_size(self, value):
        if CResourse.GAME_WIN_SPR_SIZE in self._dict_object:
            self._dict_object[CResourse.GAME_WIN_SPR_SIZE] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_WIN_SPR_SIZE, value)

    # Высота игровой информационной полосы.
    @property
    def game_info_line_size(self):
        return self._dict_object.get(CResourse.GAME_INFO_LINE_SIZE)

    @game_info_line_size.setter
    def game_info_line_size(self, value):
        if CResourse.GAME_INFO_LINE_SIZE in self._dict_object:
            self._dict_object[CResourse.GAME_INFO_LINE_SIZE] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_INFO_LINE_SIZE, value)

    # Объект управляющий игрой.
    @property
    def game_process(self):
        return self._dict_object.get(CResourse.GAME_PROCESS)

    @game_process.setter
    def game_process(self, value):
        if CResourse.GAME_PROCESS in self._dict_object:
            self._dict_object[CResourse.GAME_PROCESS] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_PROCESS, value)

    # Количестов жизней игрока.
    @property
    def game_life(self):
        return self._dict_object.get(CResourse.GAME_LIFE)

    @game_life.setter
    def game_life(self, value):
        if CResourse.GAME_LIFE in self._dict_object:
            self._dict_object[CResourse.GAME_LIFE] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_LIFE, value)

    # Объект информационной линии
    @property
    def game_info_line(self):
        return self._dict_object.get(CResourse.GAME_INFO_LINE)

    @game_info_line.setter
    def game_info_line(self, value):
        if CResourse.GAME_INFO_LINE in self._dict_object:
            self._dict_object[CResourse.GAME_INFO_LINE] = value
        else:
            self._dict_object.setdefault(CResourse.GAME_INFO_LINE, value)

    # Пройденное и повторно пройденное разстояние игроком.
    @property
    def distance_traveled(self):
        return self._dict_object.get(CResourse.BIRD_DISTANCE_TRAVELED)

    @distance_traveled.setter
    def distance_traveled(self, value):
        if CResourse.BIRD_DISTANCE_TRAVELED in self._dict_object:
            self._dict_object[CResourse.BIRD_DISTANCE_TRAVELED] = value
        else:
            self._dict_object.setdefault(CResourse.BIRD_DISTANCE_TRAVELED, value)

    @property
    def repeated_distance_traveled(self):
        return self._dict_object.get(CResourse.BIRD_REPEATED_DISTANCE_TRAVELED)

    @repeated_distance_traveled.setter
    def repeated_distance_traveled(self, value):
        if CResourse.BIRD_REPEATED_DISTANCE_TRAVELED in self._dict_object:
            self._dict_object[CResourse.BIRD_REPEATED_DISTANCE_TRAVELED] = value
        else:
            self._dict_object.setdefault(CResourse.BIRD_REPEATED_DISTANCE_TRAVELED, value)

    # Счётчик периода парализации игрока.
    @property
    def bird_paralys(self):
        return self._dict_object.get(CResourse.BIRD_PARALYS)

    @bird_paralys.setter
    def bird_paralys(self, value):
        if CResourse.BIRD_PARALYS in self._dict_object:
            self._dict_object[CResourse.BIRD_PARALYS] = value
        else:
            self._dict_object.setdefault(CResourse.BIRD_PARALYS, value)

    # Полная текущая скорость.
    @property
    def maze_full_speed(self):
        return self._dict_object.get(CResourse.MAZE_FULL_SPEED)

    @maze_full_speed.setter
    def maze_full_speed(self, value):
        if CResourse.MAZE_FULL_SPEED in self._dict_object:
            self._dict_object[CResourse.MAZE_FULL_SPEED] = value
        else:
            self._dict_object.setdefault(CResourse.MAZE_FULL_SPEED, value)

    @staticmethod
    def load_image(file_name, colorkey=None):
        """
        Загрузка изображения.
        :param file_name: имя файла
        :param colorkey: цвет альфа канала
        :return: поверхность изображения
        """
        full_name = os.path.join(CResourse.PATH_BASE_RESOURSE, file_name)
        try:
            img = pygame.image.load(full_name)
        except pygame.error:
            print("Cannot load image:" + file_name)
            raise SystemExit
        if colorkey is not None:
            if not isinstance(colorkey, tuple) and colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey)
        return img, img.get_rect()
