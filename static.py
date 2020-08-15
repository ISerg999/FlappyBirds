class CStaticParam:
    """
    Класс статических параметров игры. Синглтон.
    """

    # Ключи объектов
    _GAME_FLAYER_PLAYER = "game_flayer_player"
    _GAME_INFO_LINE = "game_info_line"
    _GAME_MAZE = "game_maze"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CStaticParam, cls).__new__(cls)
        return cls.instance

    _dict_object = {}

    # Список объектов задающих внешний вид рисования лабиринта.
    _list_maze_parametr = []
    # Список объектов задающих кодирование самого лабиринта.
    _list_maze_code = []

    def set_game_flayer_player(self, game_flayer_player):
        """
        Задаём объект летуна.
        :param game_flayer_player: объект летуна.
        """
        self._dict_object.setdefault(CStaticParam._GAME_FLAYER_PLAYER, game_flayer_player)

    def get_game_flayer_player(self):
        """
        Получаем объект летуна.
        :return: объект летуна
        """
        return self._dict_object.get(CStaticParam._GAME_FLAYER_PLAYER)

    def set_game_info_line(self, game_info_line):
        """
        Задаём объект игровой информационной линии.
        :param game_info_line: объект игровой информационной линии
        """
        self._dict_object.setdefault(CStaticParam._GAME_INFO_LINE, game_info_line)

    def get_game_info_line(self):
        """
        Получаем объект игровой информационной линии.
        :return: объект игровой информационной линии
        """
        return self._dict_object.get(CStaticParam._GAME_INFO_LINE)

    def set_game_maze(self, game_maze):
        """
        Задаём объект управляющий выводом лабиринта
        :param game_maze: объект управляющий выводом лабиринта
        """
        self._dict_object.setdefault(CStaticParam._GAME_MAZE, game_maze)

    def get_game_maze(self):
        """
        Получаем объект управляющий выводом лабиринта
        :return: объект управляющий выводом лабиринта
        """
        return self._dict_object.get(CStaticParam._GAME_MAZE)
