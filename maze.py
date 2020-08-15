from static import CStaticParam


class CGameMaze:
    """
    Класс рисования и управления самим лабиринтом.
    """

    def __init__(self, base_offset, add_offset, max_diff_offset):
        """
        Инициализация класса
        :type base_offset: базовая скорость смещения
        :param add_offset: изменение скорости смещения
        :param max_diff_offset: максимальная разница между текущей и базовой скоростью.
        """
        self._static_param = CStaticParam()
        self._base_offset = base_offset
        self._add_offset = add_offset
        self._max_diff_offset = max_diff_offset

    def paint(self, sc):
        """
        Рисование лабиринта.
        :param sc: контекст устройства.
        """
        pass

    def next_step(self):
        """
        Смещение всего игрового поля.
        """
        pass

    def change_add_offset(self, delta):
        """
        Изменение прибавочного смещениия.
        :param delta: прибавочное смещение
        """
        pass

    def collision_checking(self, rect):
        """
        Проверка столкновения литуна с объектами.
        :param rect: область занимаемая литуном
        :return: результат проверки, если меньше 0, то потеря жизней, если 0, то столкновения нет, если больше 0,
        то получил какую-то плюшку.
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------

class CMazeParametr:
    """
    Класс задающий параметры рисования лабиринта.
    """

    def __init__(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------

class CMazeCode:
    """
    Класс кодирующий лабиринт, не зваисящий от внешнего вида.
    """

    def __init__(self):
        pass

    def clear(self):
        """
        Перевод параметров в начальное состояние.
        """
        pass

    def next_code(self):
        """
        Возвращает кодированную линию - участок лабиринта.
        :return: кодированная линия - участок
        """
        pass