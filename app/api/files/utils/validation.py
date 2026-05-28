"""Функции валидации и нормализации файловых параметров.

Validation:
    isvalid_file_size: Проверка валидности размера файла.
    isvalid_filename: Проверка валидности имени файла.

Normalization:
    normalize_filename: Нормализация имени файла.
"""

from app.api.files.config import MAX_FILE_SIZE
from app.api.files.utils.file_utils import get_storage_usage_info
from app.api.utils.validation import isvalid_filename, normalize_filename


# проверки файлов и их параметров
def isvalid_file_size(size: int) -> bool:
    """Проверка валидности размера файла.

    По максимально допустимому размеру файла и по доступному месту на диске.

    Args:
        size (int): Размер файла в байтах.

    Returns:
        bool: Валидность.
    """
    return size <= MAX_FILE_SIZE and size <= get_storage_usage_info().free
