class CViewLine:
    """
    Класс вывода полосы с текстом.
    """

    def __init__(self, text, name_font=None, size_font=12, bold=False, italic=False,
                 bg_color=None, bg_lightning_color=None, rec_color=None):
        """
        Инициализация объекта.
        :param text: выводимый текст
        :param name_font: название шрифта, None - по умолчанию
        :param size_font: размер шрифта
        :param bold: True - шрифт жирный, иначе False
        :param italic: True - шрифт наклонный, иначе обычный
        :param bg_color: Цвет фона в обычном состоянии, если None, то без фона.
        :param bg_lightning_color: Цвет фона,  если отмечен / нажат
        :param rec_color: цвет рамки
        """
        # Состояние текста True - отмечено, иначе False
        self._state_text = False

    @property
    def state_text(self):
        return self._state_text

    @state_text.setter
    def state_text(self, value):
        self._state_text = value

    def paint(self, sc, x, y):
        pass

    def is_pos_in_text(self, pos):
        pass