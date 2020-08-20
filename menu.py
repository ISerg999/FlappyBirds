import pygame

from res import CResourse
from static import CStaticParam
from viewline import CViewLine


class CMainMenu:
    """
    Класс основного меню.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        s_w, _ = self._static_param.full_size
        txt_size = 80
        k = 1.1
        x, y = 0, 240
        # Объект вывода текста Начало игры.
        self._obj_txt_start = CViewLine(CResourse.MSG_START_GAME, (x, y), CResourse.COLOR_YELLOW,
                                        size_font=txt_size, bld=True, bg_lightning_color=CResourse.COLOR_SILVER)
        t_w, t_h = self._obj_txt_start.rect_size
        t_w, t_h = int(t_w * k), int(t_h * k)
        self._obj_txt_start.rect_size = (t_w, t_h)
        x = int((s_w - t_w) / 2)
        self._obj_txt_start.pos = (x, y)
        # Объект вывода текста выход.
        y += int(txt_size * 1.5)
        self._obj_txt_exit = CViewLine(CResourse.MSG_EXIT_GAME, (x, y), CResourse.COLOR_YELLOW,
                                       size_font=txt_size, bld=True, bg_lightning_color=CResourse.COLOR_SILVER)
        t_w, t_h = self._obj_txt_exit.rect_size
        t_w, t_h = int(t_w * k), int(t_h * k)
        self._obj_txt_exit.rect_size = (t_w, t_h)
        x = int((s_w - t_w) / 2)
        self._obj_txt_exit.pos = (x, y)
        # Получение изображения фона.
        self._bg_img_surf, self._bg_rect = CStaticParam.load_image(CResourse.PATH_STARRY_SKY)

    def event_handling(self, event):
        """
        Обрабокта событий основного меню.
        :param event: обрабатываемые события
        :return: -1 - Выбор "Выход из игры", 0 - выбор не сделан, 1 - выбр "Начало игры"
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self._obj_txt_start.is_pos_in_text(event.pos):
                    return 1
                elif self._obj_txt_exit.is_pos_in_text(event.pos):
                    return -1
        return 0

    def paint(self, sc):
        """
        Рисование основного меню.
        :param sc: контекст устройства
        """
        p = pygame.mouse.get_pos()
        self._obj_txt_start.state_text = 1 if self._obj_txt_start.is_pos_in_text(p) else 0
        self._obj_txt_exit.state_text = 1 if self._obj_txt_exit.is_pos_in_text(p) else 0
        sc.blit(self._bg_img_surf, self._bg_rect)
        self._obj_txt_start.paint(sc)
        self._obj_txt_exit.paint(sc)


# ----------------------------------------------------------------------------------------------------------------------

class CExitToMenu:
    """
    Класс запроса выхода из игры в основное меню.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        s_w, _ = self._static_param.full_size
        txt_size = 54
        k_text = 1.1
        y0 = 50
        x, y = 0, y0 + 20
        # Объект строки с запросом.
        self._obj_txt_question = CViewLine(CResourse.MSG_QUESTION_EXIT_TO_MENU, (x, y), CResourse.COLOR_RED,
                                           size_font=txt_size, itl=True)
        t_w, t_h = self._obj_txt_question.rect_size
        t_w, t_h = int(t_w * k_text), int(t_h * k_text)
        full_width = t_w + 40
        x0 = int((s_w - full_width) / 2)
        self._obj_txt_question.rect_size = (t_w, t_h)
        x = int((full_width - t_w) / 2) + x0
        self._obj_txt_question.pos = (x, y)
        # Объект строки с ответом Да.
        y += int(txt_size * 1.5)
        x = x0 + 20
        self._obj_txt_yes = CViewLine(CResourse.MSG_YES, (x, y), CResourse.COLOR_WHITE,
                                      size_font=txt_size, bld=True, bg_lightning_color=CResourse.COLOR_RED)
        t_w, t_h = self._obj_txt_yes.rect_size
        t_w, t_h = int(t_w * k_text), int(t_h * k_text)
        full_height = y + t_h + 20 - y0
        self._full_rect = (x0, y0, full_width, full_height)
        self._obj_txt_yes.rect_size = (t_w, t_h)
        # Объект строки с ответмо Нет.
        x = x0 + full_width - 20
        self._obj_txt_no = CViewLine(CResourse.MSG_NO, (x, y), CResourse.COLOR_WHITE,
                                     size_font=txt_size, bld=True, bg_lightning_color=CResourse.COLOR_RED)
        t_w, t_h = self._obj_txt_no.rect_size
        t_w, t_h = int(t_w * k_text), int(t_h * k_text)
        self._obj_txt_no.rect_size = (t_w, t_h)
        x -= t_w
        self._obj_txt_no.pos = (x, y)

    def event_handling(self, event):
        """
        Обрабокта событий запроса выхода из игры в меню
        :param event: обрабатываемые события
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self._obj_txt_yes.is_pos_in_text(event.pos):
                    return -1
                elif self._obj_txt_no.is_pos_in_text(event.pos):
                    return 1
        return 0

    def paint(self, sc):
        """
        Рисование запроса выхода из игры в меню.
        :param sc: контекст устройства
        """
        pygame.draw.rect(sc, CResourse.COLOR_BLACK, self._full_rect)
        pygame.draw.rect(sc, CResourse.COLOR_WHITE, self._full_rect, 1)
        p = pygame.mouse.get_pos()
        self._obj_txt_yes.state_text = 1 if self._obj_txt_yes.is_pos_in_text(p) else 0
        self._obj_txt_no.state_text = 1 if self._obj_txt_no.is_pos_in_text(p) else 0
        self._obj_txt_question.paint(sc)
        self._obj_txt_yes.paint(sc)
        self._obj_txt_no.paint(sc)