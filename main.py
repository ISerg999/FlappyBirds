import pygame

from game import CGame
from menu import CMainMenu
from res import CResourse
from static import CStaticParam


class CMain:
    """
    Базовый класс всей игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._static_param.full_size = (1280, 700)
        self._static_param.game_info_line_size = 30
        self._fps = 30
        self._static_param.game_process = CGame()
        pygame.init()
        self._screen = pygame.display.set_mode(self._static_param.full_size)
        pygame.display.set_caption("FlappyBirds")
        self._clock = pygame.time.Clock()
        self._is_game = False
        self._is_exit_to_menu = False
        self._main_menu = CMainMenu()

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
        if event.type == pygame.QUIT:
            return True
        if self._is_game:
            if self._is_exit_to_menu:
                # TODO: Запуск анализа событий запроса выхода в основное меню.
                pass
                # res = ...
                # res: -1 - выбор сделан "Нет", 0 - выбор не сделан, 1 - выбор сделан "Да"
            else:
                # Запуск анализа игровых событий
                res = self._static_param.game_process.event_handling(event)
                if res < 0:
                    # TODO: Запуск объекта дополнительного меню.
                    # self._is_exit_to_menu = True
                    pass
        else:
            # Анализ событий основного меню.
            res = self._main_menu.event_handling(event)
            if res < 0:
                return True
            elif res > 0:
                self._is_game, self._is_exit_to_menu = True, False
                self._static_param.game_process.start()
        return False

    def _paint(self):
        """
        Рисование экрана.
        """
        self._screen.fill(CResourse.COLOR_BLACK)
        if self._is_game:
            # TODO: Рисование верхней информационной полосы.
            pass
            # Рисования игры.
            self._static_param.game_process.paint(self._screen)
            if self._is_exit_to_menu:
                # TODO: Рисование запроса на выход из игры в основное меню.
                pass
        else:
            # Рисование основного меню.
            self._main_menu.paint(self._screen)
        pygame.display.flip()

    def _next_state(self):
        """
        Расчёт новых состояний, если это необходимо.
        """
        if self._is_game and not self._is_exit_to_menu:
            # Расчёт новых игровых состояний.
            self._static_param.game_process.next_state()


if __name__ == '__main__':
    game = CMain()
    game.run()
