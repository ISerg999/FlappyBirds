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
        self._dict_object.setdefault(CResourse.WINDOW_FULL_SIZE, value)

    # Параметры размера игрового окна.
    @property
    def game_win_rect(self):
        return self._dict_object.get(CResourse.GAME_WINDOW_RECT)

    @game_win_rect.setter
    def game_win_rect(self, value):
        self._dict_object.setdefault(CResourse.GAME_WINDOW_RECT, value)

    # Размер игрового окна в спрайтовых размеров (по умолчанию 40x20)
    @property
    def game_win_spr_size(self):
        return self._dict_object.get(CResourse.GAME_WIN_SPR_SIZE)

    @game_win_spr_size.setter
    def game_win_spr_size(self, value):
        self._dict_object.setdefault(CResourse.GAME_WIN_SPR_SIZE, value)

    # Высота игровой информационной полосы.
    @property
    def game_info_line_size(self):
        return self._dict_object.get(CResourse.GAME_INFO_LINE_SIZE)

    @game_info_line_size.setter
    def game_info_line_size(self, value):
        self._dict_object.setdefault(CResourse.GAME_INFO_LINE_SIZE, value)

    # Объект управляющий игрой.
    @property
    def game_process(self):
        return self._dict_object.get(CResourse.GAME_PROCESS)

    @game_process.setter
    def game_process(self, value):
        self._dict_object.setdefault(CResourse.GAME_PROCESS, value)

    # Количестов жизней игрока.
    @property
    def game_life(self):
        return self._dict_object.get(CResourse.GAME_LIFE)

    @game_life.setter
    def game_life(self, value):
        self._dict_object.setdefault(CResourse.GAME_LIFE, value)

    # Объект информационной линии
    @property
    def game_info_line(self):
        return self._dict_object.get(CResourse.GAME_INFO_LINE)

    @game_info_line.setter
    def game_info_line(self, value):
        self._dict_object.setdefault(CResourse.GAME_INFO_LINE, value)

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
                color = img.get_at((0, 0))
            img.set_colorkey(color)
        return img, img.get_rect()
