"""Менеджер данных по безопасности для аут.-авт."""

from pwdlib import PasswordHash

from app.api.auth.managers.config import DUMMY_PASSWORD
from app.api.auth.managers.dbmanager import (
    DBManager, PagedUsersPublic, UserCreate, UserPublic,
    PaginationParams, UsersFilterParams
)


class UserManager:
    """Менеджер пользователей.
    
    Включает в себя менеджер БД с пользователями и хэшер паролей. Отвечает за
    все взаимодействия с пользователями как элементами БД и их учетными и
    вспомогательными данными.
    """

    def __init__(self):
        """Инициализация экземпляра менеджера пользователей."""
        self._pwd_hasher = PasswordHash.recommended()
        self._db_manager = DBManager()

        # нужен далее для "пустой" верификации для защиты от тайминговых атак
        self._DUMMY_HASH = self._pwd_hasher.hash(DUMMY_PASSWORD)
    
    def authenticate_user(self, username: str,
                          password: str) -> UserPublic | None:
        """Аутентифицировать пользователя по логину и паролю.

        Args:
            username (str): Логин.
            password (str): Пароль.

        Returns:
            UserPublic | None: Данные о пользователе или None в случае
                непрохождения аутентификации.
        """
        user = self._db_manager.get_user(username)
        if not user:
            self._pwd_hasher.verify(password, self._DUMMY_HASH)
            return None
        if not self._pwd_hasher.verify(password, user.hashed_password):
            return None
        return UserPublic.model_validate(user)
    
    def get_users(self, pagination: PaginationParams,
                  filters: UsersFilterParams) -> PagedUsersPublic:
        """Получить страницу из списка пользователей.

        Args:
            pagination (PaginationParams): Параметры пагинации.
            filters (UsersFilterParams): Параметры фильтрации.

        Returns:
            PagedUsersPublic: Страница из списка пользователей.
        """
        users = self._db_manager.get_users(pagination, filters)
        public_users = []
        for user in users.items:
            public_users.append(UserPublic.model_validate(user))
        return PagedUsersPublic(
            items=public_users,
            total=users.total, page=users.page, limit=users.limit
        )

    def get_user(self, username: str) -> UserPublic | None:
        """Получить данные о пользователе.

        Args:
            username (str): Логин.

        Returns:
            UserPublic | None: Данные о пользователе или None, если такого
                пользователя нет.
        """
        user = self._db_manager.get_user(username)
        if user is None:
            return None
        return UserPublic.model_validate(user)

    def create_user(self, username: str, password: str) -> UserPublic | None:
        """Создать пользователя.

        Args:
            username (str): Логин.
            password (str): Пароль.
        
        Returns:
            UserPublic | None: Результат попытки создания пользователя: либо
                данные пользователя, либо None в случае, когда пользователь не
                был создан по причине наличия пользователя с таким логином.
        """
        create_user = UserCreate(
            username=username,
            hashed_password=self._pwd_hasher.hash(password)
        )
        user = self._db_manager.create_user(create_user)
        if user is None:
            return None
        return UserPublic.model_validate(user)
