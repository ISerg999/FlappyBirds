import pygame

from gameexception import CGamesExceptionGameOver
from maze import CGameMaze
from player import CGameFlayerPlayer
from res import CResourse
from static import CStaticParam


class CGame:
    """
    Класс управляющий игровым процессом.
    """

    def __init__(self):
        self._game_maze = self._state_player = None
        self._static_param = CStaticParam()
        # Ссылка на объект рисующий фон игры.
        self._game_bg = CGameBG()
        self._player = CGameFlayerPlayer(80, int((self._static_param.full_size[1] - 24) / 2),
                                         CResourse.BIRD_G, CResourse.BIRD_SPEED_VERT, CResourse.BIRD_SPEED_FLY)
        self._static_param.bird_paralys = 0
        self.start()

    @property
    def state_player(self):
        return self._state_player

    def start(self):
        """
        Начальная инициализация игры.
        """
        self._game_bg.start(0.5)
        self._static_param.game_life = 3
        self._player.start()
        self._game_maze = CGameMaze()
        self._state_player = 0

    def event_handling(self, event):
        """
        Обработка события игрового процесса.
        :param event: обрабатываемое событие
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return -2
            if self._state_player < 0:
                return -1
            if self._static_param.bird_paralys < 1:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    # Полет вверх.
                    self._player.is_move = -1
                elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    # Полет вниз.
                    self._player.is_move = 1
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    # Замедление полета до базового.
                    self._game_maze.speed_player_change(-1)
                elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    # Ускорение до максимально возможного.
                    self._game_maze.speed_player_change(1)
            else:
                self._static_param.bird_paralys = self._static_param.bird_paralys - 1
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
        # Проверка на вылет за пределы игрового экрана
        if self._player_is_not_window():
            self._state_player = -1
        # Проверка столкновения.
        if self._state_player >= 0:
            self._state_player = self._game_maze.is_collision(self._player)
        if self._state_player < 0:
            if self._static_param.game_life < 1:
                raise CGamesExceptionGameOver()
            self._static_param.game_life = self._static_param.game_life - 1
            self._player.pos_to_middle()
            self._state_player = 0
            self._game_maze.shift_game()
        if self._state_player > 0:
            if (self._state_player == CResourse.MAZ_TYPE_FLY_HEART) and (self._static_param.game_life < 6):
                self._static_param.game_life = self._static_param.game_life + 1
            elif self._state_player == CResourse.MAZ_TYPE_FLY_BRAKING:
                self._game_maze.speed_maze_change(-4)
            elif self._state_player == CResourse.MAZ_TYPE_FLY_ACCELERATION:
                self._game_maze.speed_maze_change(4)
            elif self._state_player == CResourse.MAZ_TYPE_FLY_PARALYSIS:
                # TODO:
                self._static_param.bird_paralys = CResourse.BIRD_TIME_PARALYS

    def _player_is_not_window(self):
        """
        Проверка игрока на вылет за пределы экрана.
        :return: True - игрок вылетел за пределы экрана, False - игрок не вылетел за пределы экрана.
        """
        res = False
        y = self._player.pos[1]
        (xw, yw, ww, hw) = self._static_param.game_win_rect
        if (y <= yw + 5) or (y >= yw + hw - self._player.size[1] - 5):
            res = True
        return res


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
        self._ft = pygame.font.SysFont(None, 28, bold=True)

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
        t = int(self._static_param.maze_full_speed * 10000) / 10000.0
        text = "l: " + str(self._static_param.distance_traveled) + "  v: " + str(t)
        _, text_height = self._ft.size(text)
        sc_text = self._ft.render(text, 1, CResourse.COLOR_WHITE)
        y = int((self._static_param.game_info_line_size - text_height) / 2)
        sc.blit(sc_text, (2, y))


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
