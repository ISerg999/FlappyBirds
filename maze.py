import os
import random

import pygame

from res import CResourse
from static import CStaticParam
from viewsprite import CViewSprStatic, CViewSprPlatform, CViewSprShooter, CViewSprArt


class CGameMaze:
    """
    Класс рисования и управления самим лабиринтом.
    """

    def __init__(self):
        self._maze_offset = self._player_offset = self._distance = self._cur_offset = None
        self._static_param = CStaticParam()
        self._static_param.maze_full_speed = 0.0
        self._static_param.distance_traveled = 0
        self._static_param.repeated_distance_traveled = CResourse.MAZE_START_RECOVERY
        self._maze_base_offset = CResourse.MAZE_BASE_SPEED
        self._inc_maze_offset = CResourse.MAZE_INCREMENT
        self._player_max_speed = CResourse.PLAYER_MAX_SPEED
        self._inc_player_speed = CResourse.PLAYER_SPEED_INCREMENT
        self._maze_param = CMazeParametrFromFile()
        self._maze_code = CMazeCode(CResourse.GROUP_STATIC_SPR, CResourse.GROUP_DYNAMIC_SPR, self._maze_param)
        self.shift_game()

    def shift_game(self):
        """
        Восстановление дистанции. Вызвается либо в начале, либо в момент смерти.
        """
        self._maze_offset = self._maze_base_offset
        self._player_offset = 0.0
        self._cur_offset = 0.0
        self._distance = CResourse.MAZE_DISTANCE
        self._static_param.repeated_distance_traveled = self._static_param.repeated_distance_traveled + \
                                                        CResourse.MAZE_RECOVERY_DISTANCE
        self._maze_code.shift_maze(CResourse.MAZE_RECOVERY_DISTANCE)

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
        self._static_param.maze_full_speed = self._maze_offset + self._player_offset
        self._cur_offset += self._maze_offset + self._player_offset
        t = int(self._cur_offset)
        self._cur_offset -= t
        self._maze_code.update(-t)
        self._distance -= 1
        if self._distance < 1:
            self._maze_offset += self._inc_maze_offset
            self._distance = CResourse.MAZE_DISTANCE

    def is_collision(self, player):
        """
        Проверка столкновения литуна с объектами.
        :param player: объект летуна.
        :return: результат проверки, если меньше 0, то потеря жизней, если 0, то столкновения нет, если больше 0,
        то получил какую-то плюшку.
        """
        grs = self._maze_code.groups_spr

        if pygame.sprite.spritecollideany(player, grs[0]) or pygame.sprite.spritecollideany(player, grs[1]):
            return -1
        tmp = pygame.sprite.spritecollideany(player, grs[2])
        if tmp:
            r = tmp.type_ar
            tmp.kill()
            return r
        return 0

    def speed_player_change(self, d):
        """
        Изменение скорости летуна.
        :param d: направление изменения
        """
        t = self._player_offset + d * self._inc_player_speed
        if t < 0.0:
            t = 0.0
        elif t > self._player_max_speed:
            t = self._player_max_speed
        self._player_offset = t

    def speed_maze_change(self, d):
        """
        Изменение скорости лабиринта за счёт пойманных артифактов.
        :param d: изменение скорости лабиринта в условных еденицах
        """
        t = self._maze_offset + d * self._inc_maze_offset
        if t < self._maze_base_offset:
            t = self._maze_base_offset
        self._maze_offset = t


# ----------------------------------------------------------------------------------------------------------------------

class CMazeParametrBase:
    """
    Класс выдающий кодированную линию лабиринта базовый.
    """

    def __init__(self):
        self._static_param = CStaticParam()
        self._test_max = 4
        self._test_cur = self._test_max
        self._test_type = 0
        self._r0 = (
            2, 23, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_NONE, CResourse.MAZ_TYPE_NONE)
        self._r1 = (
            (2, 23, CResourse.MAZ_TYPE_PLATFORM, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_NONE,
             CResourse.MAZ_TYPE_NONE),
            (2, 23, CResourse.MAZ_TYPE_WALL, CResourse.MAZ_TYPE_PLATFORM, CResourse.MAZ_TYPE_NONE,
             CResourse.MAZ_TYPE_NONE),
        )

    def shift_maze(self, shift):
        """
        Сместить лабиринт.
        :param shift: параметр смещения
        """
        pass

    def calc_distance_traveled(self):
        """
        Подсёт пройденного разстояния.
        """
        if self._static_param.repeated_distance_traveled > 0:
            self._static_param.repeated_distance_traveled = self._static_param.repeated_distance_traveled - 1
        else:
            self._static_param.distance_traveled = self._static_param.distance_traveled + 1

    def next_game_line(self):
        """
        Получает следующую игровую линию.
        :return: парметры игровой линии: (высота нижней стенки, высота промежутка,
        тип нижней стенки, тип верхней стенки, объекты на стенке, объекты в полёте)
        """
        self._test_cur -= 1
        res = self._r0
        if self._test_cur < 1:
            self._test_cur = self._test_max
            res = self._r1[self._test_type]
            self._test_type = 1 - self._test_type
        self.calc_distance_traveled()
        return res

    # ----------------------------------------------------------------------------------------------------------------------


class CMazeCode:
    """
    Класс кодирующий лабиринт, не зваисящий от внешнего вида.
    """

    def __init__(self, static_spr, dynamic_spr, labirint: CMazeParametrBase):
        self._static_param = CStaticParam()
        self._lab = labirint
        self._width, self._height = static_spr[2][0], static_spr[1]
        self._img_st_spr, _ = self._static_param.load_image(static_spr[0])
        x = 0
        self._rect_in_spr_st = []
        for ws in static_spr[2]:
            self._rect_in_spr_st.append((x, 0, ws, self._height))
            x += ws
        self._img_dy_spr, _ = self._static_param.load_image(dynamic_spr[0])
        x = 0
        self._rect_in_spr_dy = []
        for ws in dynamic_spr[2]:
            self._rect_in_spr_dy.append((x, 0, ws, self._height))
            x += ws
        self._offset = 0
        self._group_maze_st = pygame.sprite.Group()
        self._group_maze_pl = pygame.sprite.Group()
        self._group_maze_ar = pygame.sprite.Group()

    @property
    def groups_spr(self):
        return self._group_maze_st, self._group_maze_pl, self._group_maze_ar

    def paint(self, sc):
        """
        Рисование лабиринта.
        :param sc: контекст устройства
        """
        for elem in self.groups_spr:
            elem.draw(sc)

    def update(self, dx=0):
        """
        Возвращает кодированную линию - участок лабиринта.
        :param dx: смещение изображений
        """
        for elem in self.groups_spr:
            elem.update(dx, 0)
        self._offset += dx
        xs, ys, ws, hs = self._static_param.game_win_rect
        x = xs + ws + self._offset + self._rect_in_spr_st[0][2]
        yu, yd = ys, ys + hs - self._height
        if self._offset <= -self._width:
            self._offset += self._width
            cur_line = self._lab.next_game_line()
            ll = cur_line[0]
            if cur_line[2] == CResourse.MAZ_TYPE_WALL:
                # Создание статической нижней стенки.
                yd = self._create_wall(ll, x, yd, -1, CResourse.SPR_DYN_WALL_DOWN_0, CResourse.SPR_DYN_WALL_DOWN_1,
                                       CResourse.SPR_DYN_WALL_DOWN_2)
                if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_DOWN:
                    # Создание нижнего стрелка.
                    self._create_shooter(x, yd, -1, CResourse.SPR_DYN_SHOOTER_DOWN, CResourse.SPR_DYN_FIRE_DOWN)
            else:
                # Создание нижней динамической платформы.
                self._create_platform(ll, x, yd, -1, CResourse.SPR_DYN_PLATFORM_DOWN_0,
                                      CResourse.SPR_DYN_PLATFORM_DOWN_1, CResourse.SPR_DYN_PLATFORM_DOWN_2)
            ll = self._static_param.game_win_spr_size[1] - cur_line[0] - cur_line[1]
            if cur_line[3] == CResourse.MAZ_TYPE_WALL:
                # Создание статической верхней стенки.
                yu = self._create_wall(ll, x, yu, 1, CResourse.SPR_DYN_WALL_UP_0, CResourse.SPR_DYN_WALL_UP_1,
                                       CResourse.SPR_DYN_WALL_UP_2)
                if cur_line[4] == CResourse.MAZ_TYPE_SHOOTER_UP:
                    # Создание верхнего стрелка.
                    self._create_shooter(x, yu, 1, CResourse.SPR_DYN_SHOOTER_UP, CResourse.SPR_DYN_FIRE_UP)
            else:
                # Создание верхней динамической платформы.
                self._create_platform(ll, x, yu, 1, CResourse.SPR_DYN_PLATFORM_UP_0,
                                      CResourse.SPR_DYN_PLATFORM_UP_1, CResourse.SPR_DYN_PLATFORM_UP_2)
            if (cur_line[4] >= CResourse.MAZ_TYPE_FLY_HEART) or (cur_line[4] <= CResourse.MAZ_TYPE_FLY_PARALYSIS):
                # Создание артифактов.
                self._create_flayer_artefact(cur_line[4], x, cur_line[5])

    def _create_flayer_artefact(self, spr_ar, x, y):
        """
        Создание летающего артифакта.
        :param spr_ar: спрайт летающего артифакта
        :param x: координата x
        :param y: координата y
        """
        info_img = self._rect_in_spr_dy[spr_ar - CResourse.MAZ_TYPE_FLY_HEART]
        new_img = pygame.Surface((info_img[2], info_img[3]))
        new_img.blit(self._img_dy_spr, (0, 0), info_img)
        CViewSprArt(new_img, x, y, self._group_maze_ar, spr_ar)

    def _create_shooter(self, x, y, d, spr, spr_fire):
        """
        Создание нижнего стрелка.
        :param x: координата x
        :param y: нижняя доступная координата y
        :param d: направление стрельбы
        :param spr: спрайт стрелка
        :param spr_fire: спрайт выстрела
        :return: новая доступная координата y
        """
        info_img = self._rect_in_spr_st[spr]
        new_img = pygame.Surface((info_img[2], info_img[3]))
        new_img.blit(self._img_st_spr, (0, 0), info_img)
        CViewSprShooter(new_img, x, y, d, self._group_maze_st,
                        (self._img_st_spr, self._rect_in_spr_st[spr_fire]), self._group_maze_pl)
        y += d * info_img[3]
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
                             self._group_maze_pl, self._group_maze_st)
        return y

    def shift_maze(self, shift):
        """
        Сместить рисуемый лабиринт и начать рисование заного.
        :param shift: параметр смещения.
        """
        for gr in self.groups_spr:
            gr.empty()
        self._lab.shift_maze(shift)


# ----------------------------------------------------------------------------------------------------------------------

class CMazeParametrFromFile(CMazeParametrBase):

    def __init__(self):
        self._static_param = CStaticParam()
        self._rect_win = CStaticParam().game_win_rect
        self._height = CResourse.GROUP_STATIC_SPR[1]
        full_name = os.path.join(CResourse.PATH_BASE_RESOURSE, CResourse.PATH_MAZE_CODE)
        with open(full_name, 'rb') as file_t:
            self._barray = file_t.read()
        self._ind = 0

    def next_game_line(self):
        """
        Получает следующую игровую линию.
        :return: парметры игровой линии: (высота нижней стенки, высота промежутка,
        тип нижней стенки, тип верхней стенки, объекты на стенке, объекты в полёте)
        """
        if self._ind > len(self._barray) - 4:
            self._ind = 0
        l_d = int(self._barray[self._ind])
        self._ind += 1
        l_c = int(self._barray[self._ind])
        self._ind += 1
        k0 = int(self._barray[self._ind])
        self._ind += 1
        k1 = int(k0 / 16)
        k0 = k0 - k1 * 16
        t0 = int(self._barray[self._ind])
        self._ind += 1
        t1 = int(t0 / 16)
        t0 = t0 - t1 * 16
        if t0 >= CResourse.MAZ_TYPE_FLY_HEART:
            if t1 == 0:
                t1 = int(l_c / 2) + random.randint(0, 8) - 4
            else:
                t1 = t1 + int(l_c / 2) - 8
            if t1 < 1:
                t1 = 1
            if t1 > l_c - 2:
                t1 = l_c - 2
            t1 = self._rect_win[3] - self._height * (t1 + l_d) + self._rect_win[1]
        self.calc_distance_traveled()
        return l_d, l_c, k0, k1, t0, t1

    def shift_maze(self, shift):
        """
        Сместить лабиринт.
        :param shift: параметр смещения
        """
        self._ind -= shift * 4
        if self._ind < 0:
            self._ind = 0
