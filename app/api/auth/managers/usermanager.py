"""Менеджер пользователей для аутентификации-авторизации.

Classes:
    UserManager: Менеджер пользователей.
"""

from pwdlib import PasswordHash

from app.api.auth.managers.config import DUMMY_PASSWORD
from app.api.auth.managers.dbmanager import (
    DBManager,
    PagedUsersPublic, User, UserCreate, UserPublic, UserUpdateRights,
    PaginationParams, UsersFilterParams
)


class UserManager:
    """Менеджер пользователей.
    
    Включает в себя менеджер БД с пользователями и хэшер паролей. Отвечает за
    все взаимодействия с пользователями как элементами БД и их учетными и
    вспомогательными данными.

    Methods:
        authenticate_user: Аутентифицировать пользователя.
        get_users: Получить страницу из списка пользователей.
        get_user: Получить пользователя.
        create_user: Создать пользователя.
        delete_user: Удалить пользователя.
        update_user_rights: Обновить права доступа пользователя.
    """

    def __init__(self):
        """Инициализация экземпляра менеджера пользователей."""
        self._pwd_hasher = PasswordHash.recommended()
        self._db_manager = DBManager()

        # нужен далее для "пустой" верификации для защиты от тайминговых атак
        self._DUMMY_HASH = self._pwd_hasher.hash(DUMMY_PASSWORD)
    
    def _convert_public(self, user: User | None) -> UserPublic | None:
        """Конвертировать пользователя из БД в публичную версию.

        Args:
            user (User | None): Пользователь или None.

        Returns:
            UserPublic | None: Публичная информация о пользователе или None,
                если на вход поступило None.
        """
        if user is None:
            return None
        return UserPublic.model_validate(user)
    
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
        return self._convert_public(user)

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
        return self._convert_public(user)
    
    def delete_user(self, username: str) -> UserPublic | None:
        """Удалить пользователя.

        Args:
            username (str): Имя пользователя.

        Returns:
            UserPublic | None: Публичная информация об удаленном пользователе
                или None в случае, если пользователя с таким именем нет.
        """
        user = self._db_manager.delete_user(username)
        return self._convert_public(user)
    
    def update_user_rights(self, username: str,
                           user_rights: UserUpdateRights) -> UserPublic | None:
        """Обновить права доступа пользователя.

        Args:
            username (str): Имя пользователя.
            user_rights (UserUpdateRights): Обновления прав пользователя.

        Returns:
            UserPublic | None: Публичная информация о пользователе или None,
                если пользователь с таким именем не найден.
        """
        user = self._db_manager.update_user_rights(username, user_rights)
        return self._convert_public(user)
