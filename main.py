import pygame

from res import CResourse
from static import CStaticParam


class CMain:
    """
    Базовый класс всей игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._static_param.full_size = (1280, 700)
        self._static_param.game_info_line_size = 24
        self._fps = 30
        pygame.init()
        self._screen = pygame.display.set_mode(self._static_param.full_size)
        pygame.display.set_caption("FlappyBirds")
        self._clock = pygame.time.Clock()
        self._is_game = False
        self._is_exit_to_menu = False

    def run(self):
        """
        Запуск игрового цикла.
        """
        while True:
            self._clock.tick(self._fps)
            # Проверяем события.
            for event in pygame.event.get():
                if self._analize_event(event):
                    return
            # Рисование.
            self._paint()
            # Подготовка новых данных.
            self._next_state()

    def _analize_event(self, event):
        """
        Обработка событий.
        :param event: произошедшее событие.
        :return: True если произошло событие закрывающее приложение, False в остальных случаях.
        """
        if self._is_game:
            if self._is_exit_to_menu:
                # TODO: Запуск анализа событий запроса выхода в основное меню.
                pass
                # res = ...
                # res: -1 - выбор сделан "Нет", 0 - выбор не сделан, 1 - выбор сделан "Да"
            else:
                # TODO: Запуск анализа игровых событий
                pass
        else:
            # TODO: Запуск анализа событий из основного меню.
            pass
            # res = ...
            # res: -1 - Выбор "Выход из игры", 0 - выбор не сделан, 1 - выбр "Начало игры"
        return False

    def _paint(self):
        """
        Рисование экрана.
        """
        self._screen.fill(CResourse.COLOR_BLACK)
        if self._is_game:
            # TODO: Рисование верхней информационной полосы.
            pass
            # TODO: Рисования игры.
            pass
            if self._is_exit_to_menu:
                # TODO: Рисование запроса на выход из игры в основное меню.
                pass
        else:
            # TODO: Рисование основного меню.
            pass

    def _next_state(self):
        """
        Расчёт новых состояний, если это необходимо.
        """
        if self._is_game and not self._is_exit_to_menu:
            # TODO: Расчёт новых игровых состояний.
            pass


if __name__ == '__main__':
    game = CMain()
    game.run()
