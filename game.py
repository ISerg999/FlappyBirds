import pygame

from maze import CGameMaze
from player import CGameFlayerPlayer
from res import CResourse
from static import CStaticParam


class CGame:
    """
    Класс управляющий игровым процессом.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        # Ссылка на объект рисующий фон игры.
        self._game_bg = CGameBG()
        self._player = CGameFlayerPlayer(80, int((self._static_param.full_size[1] - 24) / 2),
                                         CResourse.BIRD_G, CResourse.BIRD_SPEED_VERT, CResourse.BIRD_SPEED_FLY)
        self._game_maze = None
        self.start()

    def start(self):
        """
        Начальная инициализация игры.
        """
        self._game_bg.start(0.5)
        self._static_param.game_life = 3
        self._player.start()
        self._game_maze = CGameMaze(CResourse.MAZE_BASE_SPEED, CResourse.MAZE_PERCENT_DIFF_SPEED)

    def event_handling(self, event):
        """
        Обработка события игрового процесса.
        :param event: обрабатываемое событие
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return -1
            if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                # Полет вверх.
                self._player.is_move = -1
            elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                # Полет вниз.
                self._player.is_move = 1
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                # TODO: Замедление полета до базового.
                pass
            elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                # TODO: Ускорение до максимально возможного.
                pass
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_UP) or (event.key == pygame.K_w) or \
                    (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                self._player.is_move = 0
        return 0

    def paint(self, sc):
        """
        Рисование всей игры.
        :param sc: контекст устройства.
        """
        self._game_bg.paint(sc)
        self._game_maze.paint(sc)
        self._player.paint(sc)

    def update(self):
        """
        Вычисление нового состояния игры.
        """
        self._game_bg.next_state()
        self._game_maze.update()
        self._player.update()
        # TODO: Проверка на вылет за пределы игрового экрана
        # TODO: Проверка столкновения.


# ----------------------------------------------------------------------------------------------------------------------

class CGameInfoLine:
    """
    Класс вывода информационной линии во время игры.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._static_param.game_life = 0
        self._full_rect = (0, 0, self._static_param.full_size[0], self._static_param.game_info_line_size)
        self._img_life, self._rect_life = CStaticParam.load_image(CResourse.PATH_IMG_HEART)
        self._life_dy = int((self._static_param.game_info_line_size - self._rect_life[3]) / 2)
        self._rect_life[1] = self._life_dy

    def paint(self, sc):
        """
        Рисование информационной линии.
        :param sc: контекст устройства.
        """
        pygame.draw.rect(sc, CResourse.COLOR_BLACK, self._full_rect)
        pygame.draw.rect(sc, CResourse.COLOR_WHITE, self._full_rect, 1)
        self._rect_life[0] = self._static_param.full_size[0] - self._rect_life[2] - 3
        for i in range(self._static_param.game_life):
            # Рисование сердечек.
            sc.blit(self._img_life, self._rect_life)
            self._rect_life[0] -= self._rect_life[2] + 2


# ----------------------------------------------------------------------------------------------------------------------

class CGameBG:
    """
    Класс вывода заднего фона во время игры.
    """

    def __init__(self, offset: float = 0.0):
        self._static_param = CStaticParam()
        self._offset = self._cur_offset = 0.0
        self._cur_x = 0
        surf, r = CStaticParam.load_image(CResourse.PATH_STARRY_SKY_SHORT)
        self._width, self._height = r[2], r[3]
        self._bg_img = pygame.Surface((self._width * 2, self._height))
        self._bg_img.blit(surf, (0, 0, self._width, self._height))
        self._bg_img.blit(surf, (self._width, 0, self._width, self._height))
        self.start(offset)

    def start(self, offset):
        """
        Базовая инициализация вывода фона.
        :param offset: начальная скорость смещения фона
        """
        self._cur_x = 0
        self._offset = offset
        self._cur_offset = 0.0

    def paint(self, sc):
        """
        Рисование заднего фона игры.
        :param sc: контекст устройства.
        """
        r = self._bg_img.get_rect()
        r[1] += self._static_param.game_info_line_size
        r[0] = self._cur_x
        sc.blit(self._bg_img, r)

    def next_state(self):
        """
        Смещение заднего фона игры.
        """
        self._cur_offset += self._offset
        t = int(self._cur_offset)
        self._cur_offset = self._cur_offset - t
        if t > 0:
            self._cur_x -= t
            if self._cur_x <= -self._width:
                self._cur_x += self._width
            elif self._cur_x >= self._width:
                self._cur_x -= self._width

    def change_add_offset(self, delta):
        """
        Изменение скорости смещения игры.
        :param delta: изменение скорости смещения
        """
        self._offset += delta
