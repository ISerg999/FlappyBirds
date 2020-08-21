import pygame

from res import CResourse
from static import CStaticParam
from viewsprite import CViewSprStatic, CViewSprPlatform


class CGameMaze:
    """
    Класс рисования и управления самим лабиринтом.
    """

    def __init__(self, base_offset, percent_diff_offset):
        """
        Инициализация класса
        :type base_offset: базовая скорость смещения
        :param percent_diff_offset: процент максимального увеличения скорости от базовой
        """
        self._static_param = CStaticParam()
        self._base_offset = base_offset
        self._max_offset = self._base_offset * (1.0 + percent_diff_offset / 100.0)
        self._cur_v_off = self._base_offset
        self._cur_off = 0.0
        self._static_param.game_move_to = (0, 0)
        self._maze_param = CMazeParametr()
        self._maze_code = CMazeCode(CResourse.GROUP_STATIC_SPR, CResourse.GROUP_DYNAMIC_SPR, self._maze_param)

    def paint(self, sc):
        """
        Рисование лабиринта.
        :param sc: контекст устройства.
        """
        self._maze_code.paint(sc)

    def update(self):
        """
        Смещение всего игрового поля.
        """
        self._cur_off += self._cur_v_off
        t = int(self._cur_off)
        self._cur_off -= t
        self._maze_code.update(-t)

    def change_add_offset(self, delta):
        """
        Изменение прибавочного смещениия.
        :param delta: прибавочное смещение
        """
        self._cur_v_off += delta
        if self._cur_v_off >= self._max_offset:
            self._cur_v_off = self._max_offset
        if self._cur_v_off <= self._base_offset:
            self._cur_v_off = self._base_offset

    def collision_checking(self, rect):
        """
        Проверка столкновения литуна с объектами.
        :param rect: область занимаемая литуном
        :return: результат проверки, если меньше 0, то потеря жизней, если 0, то столкновения нет, если больше 0,
        то получил какую-то плюшку.
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------

class CMazeParametr:
    """
    Класс задающий параметры рисования лабиринта.
    """

    def __init__(self):
        self._test_max = 4
        self._test_cur = self._test_max
        self._test_type = 0
        pass

    def next_game_line(self):
        """
        Получает следующую игровую линию.
        :return: парметры игровой линии: (высота нижней стенки, высота промежутка,
        тип нижней стенки, тип верхней стенки, объекты на стенке, объекты в полёте)
        """
        r0 = (2, 23, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_NONE, CResourse.MAZ_TYPE_NONE)
        r1 = (
            (2, 23, CResourse.MAZ_TYPE_PLATFORM, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_NONE, CResourse.MAZ_TYPE_NONE),
            (2, 23, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_PLATFORM, CResourse.MAZ_TYPE_NONE, CResourse.MAZ_TYPE_NONE),
        )
        self._test_cur -= 1
        res = r0
        if self._test_cur < 1:
            self._test_cur = self._test_max
            res = r1[self._test_type]
            self._test_type = 1 - self._test_type
        return res


# ----------------------------------------------------------------------------------------------------------------------

class CMazeCode:
    """
    Класс кодирующий лабиринт, не зваисящий от внешнего вида.
    """

    def __init__(self, static_spr, dynamic_spr, labirint: CMazeParametr):
        self._static_param = CStaticParam()
        self._lab = labirint
        self._width, self._height = static_spr[2][0], static_spr[1]
        self._img_st_spr, _ = self._static_param.load_image(static_spr[0])
        x = 0
        self._rect_in_spr_st = [(x, 0, static_spr[2][0], self._height), ]
        for i in range(1, len(static_spr[2])):
            x += static_spr[2][i - 1]
            self._rect_in_spr_st.append((x, 0, static_spr[2][i], self._height))
        self._img_dy_spr, _ = self._static_param.load_image(dynamic_spr[0])
        x = 0
        self._rect_in_spr_dy = [(x, 0, dynamic_spr[2][0], self._height), ]
        for i in range(1, len(dynamic_spr[2])):
            x += dynamic_spr[2][i - 1]
            self._rect_in_spr_dy.append((x, 0, dynamic_spr[2][i], self._height))
        self._offset = 0
        self._group_maze_st = pygame.sprite.Group()
        self._group_maze_pl = pygame.sprite.Group()
        # TODO: Создание группы стрелков, выстрелов, летающих плюшек.

    @property
    def get_group_spr(self):
        return self._group_maze_st, self._group_maze_pl

    def paint(self, sc):
        """
        Рисование лабиринта.
        :param sc: контекст устройства
        """
        for elem in self.get_group_spr:
            elem.draw(sc)

    def update(self, dx=0):
        """
        Возвращает кодированную линию - участок лабиринта.
        :param dx: смещение изображений
        """
        for elem in self.get_group_spr:
            elem.update(dx, 0)
        self._offset += dx
        xs, ys, ws, hs = self._static_param.game_win_rect
        x = xs + ws + self._offset
        yu, yd = ys, ys + hs - self._height
        if self._offset <= -self._width:
            self._offset += self._width
            cur_line = self._lab.next_game_line()
            ll = cur_line[0]
            if cur_line[2] == CResourse.MAZ_TYPE_WALL:
                # Создание статической нижней стенки.
                yd = self._create_wall(ll, x, yd, -1, CResourse.SPR_DYN_WALL_DOWN_0, CResourse.SPR_DYN_WALL_DOWN_1,
                                       CResourse.SPR_DYN_WALL_DOWN_2)
            else:
                # Создание нижней динамической платформы.
                yd = self._create_platform(ll, x, yd, -1, CResourse.SPR_DYN_PLATFORM_DOWN_0,
                                           CResourse.SPR_DYN_PLATFORM_DOWN_1, CResourse.SPR_DYN_PLATFORM_DOWN_2)
            if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_DOWN:
                # Создание нижнего стрелка.
                self._create_shooter(x, yd, -1)
            ll = self._static_param.game_win_spr_size[1] - cur_line[0] - cur_line[1]
            if cur_line[3] == CResourse.MAZ_TYPE_WALL:
                # Создание статической верхней стенки.
                yu = self._create_wall(ll, x, yu, 1, CResourse.SPR_DYN_WALL_UP_0, CResourse.SPR_DYN_WALL_UP_1,
                                       CResourse.SPR_DYN_WALL_UP_2)
            else:
                # Создание верхней динамической платформы.
                yu = self._create_platform(ll, x, yu, 1, CResourse.SPR_DYN_PLATFORM_UP_0,
                                           CResourse.SPR_DYN_PLATFORM_UP_1, CResourse.SPR_DYN_PLATFORM_UP_2)
            if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_UP:
                # Создание верхнего стрелка.
                self._create_shooter(x, yu, 1)

    def _create_shooter(self, x, y, d):
        """
        Создание нижнего стрелка.
        :param x: координата x
        :param y: нижняя доступная координата y
        :param d: направление стрельбы
        :return: новая доступная координата y
        """
        # TODO: Создание стрелка.
        return y

    def _create_wall(self, ll, x, y, d, sp_0, sp_1, sp_2):
        """
        Обобщённый метод по созданию стенки.
        :param ll: длина стенки
        :param x: координата x стенки
        :param y: координата y стенки
        :param d: направление строения стенки
        :param sp_0: спрайт основания стенки
        :param sp_1: спрайт средней, масштабируемой части стенки
        :param sp_2: спрайт навершия стенки
        :return: новая координата y
        """
        if ll > 0:
            # Создание 1-ого элемента стенки.
            info_img = self._rect_in_spr_st[sp_0]
            new_img = pygame.Surface((info_img[2], info_img[3]))
            new_img.blit(self._img_st_spr, (0, 0), info_img)
            CViewSprStatic(new_img, x, y, self._group_maze_st)
            y += d * info_img[3]
            if ll > 1:
                # Создание остальных компонентов стенки.
                elem = ll - 2
                info_img = self._rect_in_spr_st[sp_1]
                while elem > 0:
                    # Создание 2-го элемента стенки.
                    new_img = pygame.Surface((info_img[2], info_img[3]))
                    new_img.blit(self._img_st_spr, (0, 0), info_img)
                    CViewSprStatic(new_img, x, y, self._group_maze_st)
                    y += d * info_img[3]
                    elem -= 1
                # Создание 3-его элемента стенки.
                info_img = self._rect_in_spr_st[sp_2]
                new_img = pygame.Surface((info_img[2], info_img[3]))
                new_img.blit(self._img_st_spr, (0, 0), info_img)
                CViewSprStatic(new_img, x, y, self._group_maze_st)
                y += d * info_img[3]
        return y

    def _create_platform(self, ll, x, y, d, sp_0, sp_1, sp_2):
        """
        Обобщенный метод по созданию платформ.
        :param ll: длина конструкции (основание с платформоай).
        :param x: координата x конструкции
        :param y: координата y конструкции
        :param d: направление строекния конструкции
        :param sp_0: спрайт основания конструкции
        :param sp_1: спрайт средней, масштабируемой части конструкции
        :param sp_2: спрайт платформы
        :return: новая координата y
        """
        if ll > 0:
            info_img = self._rect_in_spr_st[sp_0]
            while ll > 1:
                # Создание основания платформы.
                new_img = pygame.Surface((info_img[2], info_img[3]))
                new_img.blit(self._img_st_spr, (0, 0), info_img)
                CViewSprStatic(new_img, x, y, self._group_maze_st)
                y += d * info_img[3]
                ll -= 1
            info_img = self._rect_in_spr_st[sp_2]
            new_img = pygame.Surface((info_img[2], info_img[3]))
            new_img.blit(self._img_st_spr, (0, 0), info_img)
            CViewSprPlatform((self._img_st_spr, self._rect_in_spr_st[sp_1]), new_img, x, y, d * info_img[3],
                             self._group_maze_pl, self._group_maze_st, self.get_group_spr)
        return y
