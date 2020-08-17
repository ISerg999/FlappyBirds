import pygame

from res import CResourse


class CViewLine:
    """
    Класс вывода полосы с текстом.
    """

    def __init__(self, text, pos, txt_color=CResourse.COLOR_BLACK, name_font=None, size_font=12, bld=False, itl=False,
                 bg_color=None, bg_lightning_color=None, rec_color=None):
        """
        Инициализация объекта.
        :param text: выводимый текст
        :param pos: координаты положения рамки с текстом
        :param txt_color: цвет текста
        :param name_font: название шрифта, None - по умолчанию
        :param size_font: размер шрифта
        :param bld: True - шрифт жирный, иначе False
        :param itl: True - шрифт наклонный, иначе обычный
        :param bg_color: Цвет фона в обычном состоянии, если None, то без фона.
        :param bg_lightning_color: Цвет фона,  если отмечен / нажат
        :param rec_color: цвет рамки
        """
        self._text = text
        self._pos = (0, 0)
        # Состояние текста True - отмечено, иначе False
        self._state_text = False
        self._ft = pygame.font.SysFont(name_font, size_font, bold=bld, italic=itl)
        self._text_width, self._text_height = self._ft.size(text)
        self._sc_text = self._ft.render(self._text, 1, self._txt_color)
        self.rect_size = (0, 0)
        self._bg_color = bg_color
        self._bg_lightning_color = bg_lightning_color
        self._rec_color = rec_color
        self._pos = pos
        self._txt_color = txt_color

    @property
    def text(self) -> str:
        return self._text

    @property
    def state_text(self) -> bool:
        return self._state_text

    @state_text.setter
    def state_text(self, value: bool):
        self._state_text = value

    @property
    def rect_size(self) -> tuple:
        return self._width, self._height

    @rect_size.setter
    def rect_size(self, value: tuple):
        self._width = value[0] if value[0] >= self._text_width + 2 else self._text_width + 2
        self._height = value[1] if value[1] >= self._text_height + 2 else self._text_height + 2
        self._txt_offset()

    @property
    def pos(self) -> tuple:
        return self._pos

    @pos.setter
    def pos(self, value: tuple):
        self._pos = value
        self._txt_offset()

    def _txt_offset(self):
        self._dx = int((self._width - self._text_width) / 2 + self._pos[0])
        self._dy = int((self._height - self._text_height) / 2 + self._pos[1])

    def paint(self, sc):
        rect = (self._pos[0], self._pos[1], self._width, self._height)
        if self._state_text and self._bg_lightning_color is not None:
            pygame.draw.rect(sc, self._bg_lightning_color, rect)
        else:
            if self._bg_color is not None:
                pygame.draw.rect(sc, self._bg_color, rect)
        sc.blit(self._sc_text, self._pos)
        if self._rec_color is not None:
            pygame.draw.rect(sc, self._rec_color, rect, 1)

    def is_pos_in_text(self, pos: tuple) -> bool:
        """
        Проверка попадания координат в область рамки с текстом.
        :param pos: проверяемые координаты
        :return: результат проверки. True - есть попадание, False - нет попадания.
        """
        if (self._pos[0] <= pos[0] < self._pos[0] + self._width) and \
                (self._pos[1] <= pos[1] < self._pos[1] + self._height):
            return True
        return False
