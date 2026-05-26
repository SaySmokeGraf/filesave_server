"""Конфигурационный скрипт для валидации и нормализации."""

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
    
    Содержит в себе:
        NAME_MIN_LENGTH - минимальная длина имени (стэма).
        NAME_MAX_LENGTH - максимальная длина имени (стэма).
        NAME_UNSAFE_CHARS_REGEX - регулярное выражение небезопасных символов
            для имени (стэма).
        EXT_MIN_LENGTH - минимальная длина расширения.
        EXT_MAX_LENGTH - максимальная длина расширения.
        EXT_UNSAFE_CHARS_REGEX - регулярное выражение небезопасных символов для
            расширения.
        FILENAME_MIN_LENGTH - минимальная длина имени файла.
        FILENAME_MAX_LENGTH - максимальная длина имени файла.
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
    
    Содержит в себе:
        USERNAME_MIN_LENGTH - минимальная длина имени пользователя.
        USERNAME_MAX_LENGTH - максимальная длина имени пользователя.
        USERNAME_UNSAFE_CHARS_REGEX - регулярное выражение небезопасных
            символов для имени пользователя.
        PWD_MIN_LENGTH - минимальная длина пароля.
        PWD_MAX_LENGTH - максимальная длина пароля.
        PWD_UNSAFE_CHARS_REGEX - регулярное выражение небезопасных символов для
            пароля.
    """
    USERNAME_MIN_LENGTH = 4
    USERNAME_MAX_LENGTH = 64
    USERNAME_UNSAFE_CHARS_REGEX = r'[^A-Za-z0-9._\-]'
    PWD_MIN_LENGTH = 4
    PWD_MAX_LENGTH = 128
    PWD_UNSAFE_CHARS_REGEX = r'[^A-Za-z0-9._\-!@#$%\^&*()\[\]+={};:\'\",<>/\\?|~]'
