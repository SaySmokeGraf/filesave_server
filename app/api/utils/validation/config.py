"""Конфигурационный скрипт для валидации и нормализации.

Consts:
    UNNAMED_REPLACEMENT (str): Имя для замены пустого имени.
    REPLACEMENT_CHAR (str): Символ для замены небезопасных символов.
    WINDOWS_RESERVED (set[str]): Множество зарезервированных имен Windows.
    FileConsts: Класс с константами для валидации и нормализации файловых
        полей.
    UserConsts: Класс с константами для валидации и нормализации полей
        пользователей.
"""

# константы
UNNAMED_REPLACEMENT = 'unnamed'
REPLACEMENT_CHAR = '_'

WINDOWS_RESERVED = {
    'CON', 'PRN', 'AUX', 'NUL',
    *(f'COM{i}' for i in range(1, 10)),
    *(f'LPT{i}' for i in range(1, 10))
}


class FileConsts:
    """Константы для валидации файловых полей.
    
    Consts:
        NAME_MIN_LENGTH (int): Минимальная длина имени (стэма).
        NAME_MAX_LENGTH (int): Максимальная длина имени (стэма).
        NAME_UNSAFE_CHARS_REGEX (str): Регулярное выражение небезопасных
            символов для имени (стэма).
        EXT_MIN_LENGTH (int): Минимальная длина расширения.
        EXT_MAX_LENGTH (int): Максимальная длина расширения.
        EXT_UNSAFE_CHARS_REGEX (str): Регулярное выражение небезопасных
            символов для расширения.
        FILENAME_MIN_LENGTH (int): Минимальная длина имени файла.
        FILENAME_MAX_LENGTH (int): Максимальная длина имени файла.
    """
    NAME_MIN_LENGTH = 1
    NAME_MAX_LENGTH = 200
    NAME_UNSAFE_CHARS_REGEX = r'[^\w\-_.\d\s(){}\[\]]'
    EXT_MIN_LENGTH = 0
    EXT_MAX_LENGTH = 50
    EXT_UNSAFE_CHARS_REGEX = r'[^A-Za-z0-9\-_.]'
    FILENAME_MIN_LENGTH = 1
    FILENAME_MAX_LENGTH = 250


class UserConsts:
    """Константы для валидации полей пользователей.
    
    Consts:
        USERNAME_MIN_LENGTH (int): Минимальная длина имени пользователя.
        USERNAME_MAX_LENGTH (int): Максимальная длина имени пользователя.
        USERNAME_UNSAFE_CHARS_REGEX (str): Регулярное выражение небезопасных
            символов для имени пользователя.
        PWD_MIN_LENGTH (int): Минимальная длина пароля.
        PWD_MAX_LENGTH (int): Максимальная длина пароля.
        PWD_UNSAFE_CHARS_REGEX (str): Регулярное выражение небезопасных
            символов для пароля.
    """
    USERNAME_MIN_LENGTH = 4
    USERNAME_MAX_LENGTH = 64
    USERNAME_UNSAFE_CHARS_REGEX = r'[^A-Za-z0-9._\-]'
    PWD_MIN_LENGTH = 4
    PWD_MAX_LENGTH = 128
    PWD_UNSAFE_CHARS_REGEX = r'[^A-Za-z0-9._\-!@#$%\^&*()\[\]+={};:\'\",<>/\\?|~]'
