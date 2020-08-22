class CGamesException(Exception):
    """
    Базовый класс игровых изключений.
    """
    pass


class CGamesExceptionGameOver(CGamesException):
    """
    Изключение возникающее при окончании игры.
    """
    pass

