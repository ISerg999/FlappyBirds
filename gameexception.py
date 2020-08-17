class CGamesException(Exception):
    """
    Базовый класс игровых изключений.
    """
    pass


class CGamesExceptionExitGame(CGamesException):
    """
    Изключение возникающее при выходе из игры.
    """
    pass


class CGamesExceptionStopMaze(CGamesException):
    """
    Изключение возникающее если выводимый лабиринт закончился.
    """
    pass
