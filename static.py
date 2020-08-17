class CStaticParam:
    """
    Класс статических параметров игры. Синглтон.
    """

    # Ключи объектов
    _WINDOW_FULL_SIZE = "win_full_size"
    _GAME_INFO_LINE_SIZE = "game_info_line_size"

    # _GAME_FLAYER_PLAYER = "game_flayer_player"
    # _GAME_INFO_LINE = "game_info_line"
    # _GAME_MAZE = "game_maze"

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
        return self._dict_object.get(CStaticParam._WINDOW_FULL_SIZE)

    @full_size.setter
    def full_size(self, value):
        self._dict_object.setdefault(CStaticParam._WINDOW_FULL_SIZE, value)

    # Высота игровой информационной полосы.
    @property
    def game_info_line_size(self):
        return self._dict_object.get(CStaticParam._GAME_INFO_LINE_SIZE)

    @game_info_line_size.setter
    def game_info_line_size(self, value):
        self._dict_object.setdefault(CStaticParam._GAME_INFO_LINE_SIZE, value)
