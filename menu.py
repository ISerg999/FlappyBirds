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
        # Объект вывода текста Начало игры.
        x, y = 0, 240
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
        self._bg_img_surf = pygame.image.load(CResourse.PATH_BASE_RESOURSE + CResourse.PATH_STARRY_SKY)

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
        sc.blit(self._bg_img_surf, self._bg_img_surf.get_rect())
        self._obj_txt_start.paint(sc)
        self._obj_txt_exit.paint(sc)


# ----------------------------------------------------------------------------------------------------------------------

class CExitToMenu:
    """
    Класс запроса выхода из игры в основное меню.
    """

    def __init__(self):
        # Объект строки с запросом.
        self._obj_txt_question = None
        # Объект строки с ответом Да.
        self._obj_txt_yes = None
        # Объект строки с ответмо Нет.
        self._obj_txt_no = None

    def event_handling(self, event):
        """
        Обрабокта событий запроса выхода из игры в меню
        :param event: обрабатываемые события
        """
        pass

    def paint(self, sc):
        """
        Рисование запроса выхода из игры в меню.
        :param sc: контекст устройства
        """
        pass
