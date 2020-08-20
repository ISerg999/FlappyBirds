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
    GAME_MOVE_TO = "game_move_to"
    GAME_INFO_LINE_SIZE = "game_info_line_size"
    GAME_PROCESS = "game_process"
    GAME_LIFE = "game_life"
    GAME_INFO_LINE = "game_info_line"

    # Параметры движения птички - игрока.
    BIRD_G = 2.0
    BIRD_SPEED_VERT = 10.0
    BIRD_SPEED_FLY = 1.0

    # Путь к внешним ресурам.
    PATH_BASE_RESOURSE = "Resource"

    # Внешние ресурсы.
    PATH_STARRY_SKY = "starry-sky-1280_700.png"
    PATH_STARRY_SKY_SHORT = "starry-sky-1280_660.png"
    PATH_IMG_HEART = "heart-32_32.png"
    PATH_IMG_BIRD = "bird.png"
