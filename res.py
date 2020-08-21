class CResourse:
    """
    Класс ресурсов игры.
    """
    # Константы текстовых сообщений.
    MSG_START_GAME = "Начало игры"
    MSG_EXIT_GAME = "Выход из игры"
    MSG_QUESTION_EXIT_TO_MENU = "Вы действительно хотите выйти в главное меню?"
    MSG_YES = "Да"
    MSG_NO = "Нет"

    # Цвета.
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_SILVER = (192, 192, 192)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_CYANIDE = (0, 255, 255)
    COLOR_MAGENTA = (255, 0, 255)

    # Ключи объектов
    WINDOW_FULL_SIZE = "win_full_size"
    GAME_WINDOW_RECT = "game_window_rect"
    GAME_INFO_LINE_SIZE = "game_info_line_size"
    GAME_PROCESS = "game_process"
    GAME_LIFE = "game_life"
    GAME_INFO_LINE = "game_info_line"
    GAME_WIN_SPR_SIZE = "game_win_spr_size"

    # Параметры движения птички - игрока.
    BIRD_G = 2.0
    BIRD_SPEED_VERT = 10.0
    BIRD_SPEED_FLY = 1.0

    # Параметры смещения лабиринта.
    MAZE_BASE_SPEED = 1.0
    MAZE_PERCENT_DIFF_SPEED = 50.0

    # Параметры управления платформы.
    MAZE_PLATFORM_DELAY = 4

    # Индексы игровых спрайтов.
    SPR_DYN_WALL_DOWN_0 = 0
    SPR_DYN_WALL_DOWN_1 = 1
    SPR_DYN_WALL_DOWN_2 = 2
    SPR_DYN_WALL_UP_0 = 3
    SPR_DYN_WALL_UP_1 = 4
    SPR_DYN_WALL_UP_2 = 5
    SPR_DYN_PLATFORM_DOWN_0 = 6
    SPR_DYN_PLATFORM_DOWN_1 = 7
    SPR_DYN_PLATFORM_DOWN_2 = 8
    SPR_DYN_PLATFORM_UP_0 = 9
    SPR_DYN_PLATFORM_UP_1 = 10
    SPR_DYN_PLATFORM_UP_2 = 11
    SPR_DYN_SHOOTER_DOWN = 12
    SPR_DYN_SHOOTER_UP = 13
    SPR_DYN_FIRE_DOWN = 14
    SPR_DYN_FIRE_UP = 15
    SPR_ST_HEART = 0
    SPR_ST_BRAKING = 1
    SPR_ST_ACCELERATION = 2
    SPR_ST_PARALYSIS = 3

    # Константы кодирования лабиринта.
    MAZ_TYPE_NONE = 0
    MAZ_TYPE_WALL = 1
    MAZ_TYPE_PLATFORM = 2
    MAZ_TYPE_SHOOTER_DOWN = 1
    MAZ_TYPE_SHOOTER_UP = 2
    MAZ_TYPE_FLY_HEART = 1
    MAZ_TYPE_FLY_BRAKING = 2
    MAZ_TYPE_FLY_ACCELERATION = 3
    MAZ_TYPE_FLY_PARALYSIS = 4

    # Путь к внешним ресурам.
    PATH_BASE_RESOURSE = "Resource"

    # Внешние ресурсы.
    PATH_STARRY_SKY = "starry-sky-1280_700.png"
    PATH_STARRY_SKY_SHORT = "starry-sky-1280_660.png"
    PATH_IMG_HEART = "heart-32_32.png"
    PATH_IMG_BIRD = "bird.png"
    GROUP_STATIC_SPR = ("maze_static_spr.png", 20, (40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 20))
    GROUP_DYNAMIC_SPR = ("maze_dynamic_spr.png", 20, (20, 20, 20, 20, ))
