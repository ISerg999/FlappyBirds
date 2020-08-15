from enum import Enum


class CResourse(Enum):
    """
    Класс ресурсов игры.
    """
    # Константы текстовых сообщений.
    MSG_START_GAME = "Начало игры"
    MSG_EXIT_GAME = "Выход из игры"
    MSG_QUESTION_EXIT_TO_MENU = "Вы действительно хотите выйти в главное меню?"
    MSG_YES = "Да"
    MSG_NO = "Нет"

    # Путь к внешним ресурам.
    PATH_BASE_RESOURSE = "./Resource/"
