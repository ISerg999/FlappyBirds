class CViewSprite:
    """
    Рисование спрайтов.
    """

    def __init__(self, img):
        """
        Начальная инициализация.
        :param img: путь к спрайту
        """
        self._width = self._height = None

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def paint(self, sc, x, y):
        """
        Рисование спрайта.
        :param sc: контекст устройства
        :param x: координата x
        :param y: координата y
        :return:
        """
        pass