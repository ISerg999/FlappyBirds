class CMainMenu:
    """
    Класс основного меню.
    """

    def __init__(self):
        # Объект вывода текста Начало игры.
        self._obj_txt_start = None
        # Объект вывода текста выход.
        self._obj_txt_exit = None

    def event_handling(self, event):
        """
        Обрабокта событий основного меню.
        :param event: обрабатываемые события
        """
        pass

    def paint(self, sc):
        """
        Рисование основного меню.
        :param sc: контекст устройства
        """
        pass


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
