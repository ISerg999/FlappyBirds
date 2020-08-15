from static import CStaticParam


class CGame:
    """
    Класс управляющий игровым процессом.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        # Ссылка на объект рисующий фон игры.
        self._game_bg = None

    def event_handling(self, event):
        """
        Обработка события игрового процесса.
        :param event: обрабатываемое событие
        """
        pass

    def paint(self, sc):
        """
        Рисование всей игры.
        :param sc: контекст устройства.
        """
        pass

    def next_state(self):
        """
        Вычисление нового состояния игры.
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------

class CGameInfoLine:
    """
    Класс вывода информационной линии во время игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()

    def paint(self, sc):
        """
        Рисование информационной линии.
        :param sc: контекст устройства.
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------

class CGameBG:
    """
    Класс вывода заднего фона во время игры.
    """

    def __init__(self, img, offset):
        self._offset = offset

    def paint(self, sc):
        """
        Рисование заднего фона игры.
        :param sc: контекст устройства.
        """
        pass

    def next_state(self):
        """
        Смещение заднего фона игры.
        """
        pass

    def change_add_offset(self, delta):
        """
        Изменение скорости смещения игры.
        :param delta: изменение скорости смещения
        """
        pass
