
class CGameFlayerPlayer:
    """
    Класс управления летуном.
    """

    def __init__(self, x, y, life, img, g, offset):
        """
        Инициализация управления летуном.
        :param x: координата x
        :param y: координата y
        :param life: количество жизней
        :param img: изображение летуна
        :param g: параметр ускорения падения летуна вниз
        :param offset: смещение при перемещении вверх или вниз
        """
        self._x, self._y = x, y
        self._life = life
        self._offset, self._g = offset, g
        # Ширина спрайта
        self._width = None
        # Высота спрайта
        self._height = None
        # Спрайт летуна
        self._spr_flayer = None

    @property
    def pos(self):
        return self._x, self._y

    @property
    def size(self):
        return self._width, self._height

    @property
    def life(self):
        return self._life

    def changing_life(self, add_life):
        """
        Изменение количества жизней.
        :param add_life: измененное количество жизней
        """
        self._life += add_life

    def paint(self, sc):
        """
        Рисование летуна.
        :param sc: контекст устройства.
        """
        pass

    def next_state(self):
        """
        Расчёт нового состояния летуна.
        """
        pass