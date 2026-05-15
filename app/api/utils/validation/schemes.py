"""Конкретные схемы валидации или нормализации полей."""

from app.api.utils.validation import parts
from app.api.utils.validation.config import FileConsts, UserConsts


# нормализация
def normalize_filename(filename: str) -> str:
    """Нормализовать имя файла.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Нормализованное имя файла.
    """
    filename = parts.normalize_length(filename, FileConsts.FILENAME_MAX_LENGTH,
                                      cut_left=True)
    filename = parts.normalize_path_traversal(filename)
    filename = parts.normalize_unicode(filename)

    name, ext = parts.split_filename(filename)

    name = parts.normalize_length(name, FileConsts.NAME_MAX_LENGTH)
    name = name.strip('. ')
    name = parts.normalize_chars(name, FileConsts.NAME_UNSAFE_CHARS_REGEX)
    name = parts.normalize_reserved_names(name)
    name = parts.normalize_empty_name(name)
    
    ext = parts.normalize_length(ext, FileConsts.EXT_MAX_LENGTH)
    ext = parts.normalize_chars(ext, FileConsts.EXT_UNSAFE_CHARS_REGEX)

    return parts.build_filename(name, ext)


# валидация
def isvalid_filename(filename: str) -> bool:
    """Проверка валидности имени файла.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: Валидность.
    """
    if not parts.isvalid_length(filename, FileConsts.FILENAME_MIN_LENGTH,
                                FileConsts.FILENAME_MAX_LENGTH):
        return False
    res = parts.isvalid_path_traversal(filename)
    res = res and parts.isvalid_unicode(filename)

    name, ext = parts.split_filename(filename)

    res = res and parts.isvalid_length(name, FileConsts.NAME_MIN_LENGTH,
                                       FileConsts.NAME_MAX_LENGTH)
    res = res and (name == name.strip('. '))
    res = res and parts.isvalid_chars(name, FileConsts.NAME_UNSAFE_CHARS_REGEX)
    res = res and parts.isvalid_reserved_names(name)
    
    res = res and parts.isvalid_length(ext, FileConsts.EXT_MIN_LENGTH,
                                       FileConsts.EXT_MAX_LENGTH)
    res = res and parts.isvalid_chars(ext, FileConsts.EXT_UNSAFE_CHARS_REGEX)

    return res

def isvalid_username_length(username: str) -> bool:
    """Проверка валидности длины имени пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        bool: Валидность.
    """
    return parts.isvalid_length(username,
                                UserConsts.USERNAME_MIN_LENGTH,
                                UserConsts.USERNAME_MAX_LENGTH)

def isvalid_pwd_length(password: str) -> bool:
    """Проверка валидности длины пароля.

    Args:
        password (str): Пароль.

    Returns:
        bool: Валидность.
    """
    return parts.isvalid_length(password,
                                UserConsts.PWD_MIN_LENGTH,
                                UserConsts.PWD_MAX_LENGTH)

def isvalid_username(username: str) -> bool:
    """Проверка валидности имени пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        bool: Валидность.
    """
    if not isvalid_username_length(username):
        return False
    res = parts.isvalid_unicode(username)
    res = res and parts.isvalid_chars(username,
                                      UserConsts.USERNAME_UNSAFE_CHARS_REGEX)
    return res

def isvalid_pwd(password: str) -> bool:
    """Проверка валидности пароля.

    Args:
        password (str): Пароль.

    Returns:
        bool: Валидность.
    """
    if not isvalid_pwd_length(password):
        return False
    res = parts.isvalid_unicode(password)
    res = res and parts.isvalid_chars(password,
                                      UserConsts.PWD_UNSAFE_CHARS_REGEX)
    return res
