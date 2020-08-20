import pygame

from game import CGame, CGameInfoLine
from menu import CMainMenu, CExitToMenu
from res import CResourse
from static import CStaticParam


class CMain:
    """
    Базовый класс всей игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._static_param.full_size = (1280, 700)
        self._static_param.game_info_line_size = 40
        self._static_param.game_win_rect = (0, self._static_param.game_info_line_size, self._static_param.full_size[0],
                                            self._static_param.full_size[1] - self._static_param.game_info_line_size)
        self._static_param.game_move_to = (0, 0)
        self._fps = 30
        self._static_param.game_process = CGame()
        pygame.init()
        self._screen = pygame.display.set_mode(self._static_param.full_size)
        pygame.display.set_caption("FlappyBirds")
        self._clock = pygame.time.Clock()
        self._is_game = self._is_exit_to_menu = False
        self._main_menu = CMainMenu()
        self._exit_to_menu = CExitToMenu()
        self._static_param.game_info_line = CGameInfoLine()

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
            self._update()
            pygame.time.delay(20)

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
                # Запуск анализа событий запроса выхода в основное меню.
                res = self._exit_to_menu.event_handling(event)
                if res < 0:
                    # Выбран выход в основное меню.
                    self._is_game = self._is_exit_to_menu = False
                elif res > 0:
                    # Выбрано продолжение игры.
                    self._is_exit_to_menu = False
            else:
                # Запуск анализа игровых событий
                res = self._static_param.game_process.event_handling(event)
                if res < 0:
                    # Запуск объекта дополнительного меню.
                    self._is_exit_to_menu = True
        else:
            # Анализ событий основного меню.
            res = self._main_menu.event_handling(event)
            if res < 0:
                return True
            elif res > 0:
                self._is_game = True
                self._static_param.game_process.start()
        return False

    def _paint(self):
        """
        Рисование экрана.
        """
        self._screen.fill(CResourse.COLOR_BLACK)
        if self._is_game:
            # Рисование верхней информационной полосы.
            self._static_param.game_info_line.paint(self._screen)
            # Рисования игры.
            self._static_param.game_process.paint(self._screen)
            if self._is_exit_to_menu:
                # Рисование запроса на выход из игры в основное меню.
                self._exit_to_menu.paint(self._screen)
        else:
            # Рисование основного меню.
            self._main_menu.paint(self._screen)
        pygame.display.flip()

    def _update(self):
        """
        Расчёт новых состояний, если это необходимо.
        """
        if self._is_game and not self._is_exit_to_menu:
            # Расчёт новых игровых состояний.
            self._static_param.game_process.update()


if __name__ == '__main__':
    game = CMain()
    game.run()
