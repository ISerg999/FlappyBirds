import pygame

from res import CResourse
from static import CStaticParam
from viewsprite import CViewSprStatic


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
        pass

    def next_game_line(self):
        """
        Получает следующую игровую линию.
        :return: парметры игровой линии: (высота нижней стенки, высота промежутка,
        тип нижней стенки, тип верхней стенки, объекты на стенке, объекты в полёте)
        """
        return 2, 23, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_NONE, CResourse.MAZ_TYPE_NONE


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
        self._group_maze_st = pygame.sprite.Group()
        self._offset = 0

    def paint(self, sc):
        """
        Рисование лабиринта.
        :param sc: контекст устройства
        """
        self._group_maze_st.draw(sc)

    def update(self, dx=0):
        """
        Возвращает кодированную линию - участок лабиринта.
        :param dx: смещение изображений
        """
        self._group_maze_st.update(dx, 0)
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
                yd = self._create_wall_down(ll, x, yd)
            else:
                # Создание нижней динамической платформы.
                yd = self._create_platform_down(ll, x, yd)
            if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_DOWN:
                # Создание нижнего стрелка.
                self._create_shooter_down(x, yd)
            ll = self._static_param.game_win_spr_size[1] - cur_line[0] - cur_line[1]
            if cur_line[3] == CResourse.MAZ_TYPE_WALL:
                # Создание статической верхней стенки.
                yu = self._create_wall_up(ll, x, yu)
            else:
                # Создание верхней динамической платформы.
                yu = self._create_platform_up(ll, x, yu)
            if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_UP:
                # Создание верхнего стрелка.
                self._create_shooter_up(x, yu)

    def _create_wall_down(self, ll, x, y):
        """
        Создание нижней стенки.
        :param ll: длина стенки
        :param x: координата x
        :param y: нижняя доступная координата y
        :return: новая доступная координата y
        """
        return self._create_wall(ll, x, y, -1, CResourse.SPR_DYN_WALL_DOWN_0, CResourse.SPR_DYN_WALL_DOWN_1,
                                 CResourse.SPR_DYN_WALL_DOWN_2)

    def _create_platform_down(self, ll, x, y):
        """
        Создание нижней платформы.
        :param ll: длина платформы
        :param x: координата x
        :param y: нижняя доступная координата y
        :return: новая доступная координата y
        """
        # TODO: Создание нижней платформы.
        return y

    def _create_shooter_down(self, x, y):
        """
        Создание нижнего стрелка.
        :param x: координата x
        :param y: нижняя доступная координата y
        :return: новая доступная координата y
        """
        # TODO: Создание нижнего стрелка.
        return y

    def _create_wall_up(self, ll, x, y):
        """
        Создание верхней стенки.
        :param ll: длина стенки
        :param x: координата x
        :param y: верхняя доступная координата y
        :return: новая доступная координата y
        """
        return self._create_wall(ll, x, y, 1, CResourse.SPR_DYN_WALL_UP_0, CResourse.SPR_DYN_WALL_UP_1,
                                 CResourse.SPR_DYN_WALL_UP_2)

    def _create_platform_up(self, ll, x, y):
        """
        Создание верхней платформы.
        :param ll: длина платформы
        :param x: координата x
        :param y: верхняя координата y
        :return: новая доступная координата y
        """
        # TODO: Создание верхней платформы.
        return y

    def _create_shooter_up(self, x, y):
        """
        Создание верхнего стрелка.
        :param x: координата x
        :param y: верхняя координата y
        :return: новая доступная координата x
        """
        # TODO: Создание верхнего стрелка.
        return y

    def _create_wall(self, ll, x, y, d, sp_0, sp_1, sp_2):
        """
        Обобщённый метод по созданию стенки
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
