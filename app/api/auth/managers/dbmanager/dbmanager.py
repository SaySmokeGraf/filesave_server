"""Менеджер БД для аутентификации-авторизации.

Classes:
    DBManager: Менеджер БД пользователей.
"""

from pathlib import Path

from sqlmodel import create_engine, func, select, Session, SQLModel

from app.api.auth.managers.dbmanager.config import PATH_DB_DIR, SQLITE_URL
from app.api.auth.managers.dbmanager.models import (
    PagedUsers, User, UserCreate, PaginationParams, UsersFilterParams,
    UserUpdateRights
)


_path_db_dir = Path(PATH_DB_DIR)


class DBManager:
    """Менеджер БД пользователей.
    
    Methods:
        get_users: Получить страницу из списка пользователей.
        get_user: Получить пользователя.
        create_user: Создать пользователя.
        delete_user: Удалить пользователя.
        update_user_rights: Обновить права доступа пользователя.
    """

    def __init__(self):
        """Инициализация экземпляра менеджера БД."""
        self._create_db_directory()
        self._engine = create_engine(SQLITE_URL,
                                     connect_args={'check_same_thread': False})
        self._create_db_and_tables()
    
    def _create_db_directory(self) -> None:
        """Создать папку хранения БД, если нужно."""
        if not _path_db_dir.exists():
            _path_db_dir.mkdir(parents=True)

    def _create_db_and_tables(self) -> None:
        """Создать БД и таблицы, если нужно."""
        SQLModel.metadata.create_all(self._engine)
    
    def get_users(
        self, pagination: PaginationParams, filters: UsersFilterParams
    ) -> PagedUsers:
        """Получить страницу из списка пользователей.

        Args:
            pagination (PaginationParams): Параметры пагинации.
            filters (UsersFilterParams): Параметры фильтрации.

        Returns:
            PagedUsers: Страница из списка пользователей.
        """
        with Session(self._engine) as session:
            page, limit = pagination.page, pagination.limit
            filters_dump = filters.filters_dump()

            total = session.exec(
                select(func.count())
                .select_from(User)
                .where(*filters_dump)
            ).one()

            users = session.exec(
                select(User)
                .where(*filters_dump)
                .offset((page - 1) * limit)
                .limit(limit)
            ).all()
        return PagedUsers(items=users, total=total, page=page, limit=limit)
    
    def get_user(self, username: str) -> User | None:
        """Получить данные пользователя из БД.

        Args:
            username (str): Имя пользователя.

        Returns:
            User | None: Данные пользователя из БД или None, если такого
                пользователя нет.
        """
        with Session(self._engine) as session:
            user = session.exec(
                select(User)
                .where(User.username == username)
            ).first()
        return user
    
    def create_user(self, user: UserCreate) -> User | None:
        """Создание нового пользователя в БД.

        Args:
            user (UserCreate): Данные пользователя для создания.

        Returns:
            User | None: Результат попытки создания пользователя: либо данные
                пользователя, либо None в случае, когда пользователь не был
                создан по причине наличия пользователя с таким логином.
        """
        if self.get_user(user.username) is not None:
            return None
        with Session(self._engine) as session:
            db_user = User.model_validate(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user
    
    def delete_user(self, username: str) -> User | None:
        """Удаление пользователя из БД.

        Args:
            username (str): Имя пользователя.

        Returns:
            User | None: Удаленный пользователь или None, если пользователя с
                таким именем нет.
        """
        user = self.get_user(username)
        if user is None:
            return None
        with Session(self._engine) as session:
            session.delete(user)
            session.commit()
        return user
    
    def update_user_rights(
        self, username: str, user_rights: UserUpdateRights
    ) -> User | None:
        """Обновить права доступа пользователя в БД.

        Args:
            username (str): Имя пользователя.
            user_rights (UserUpdateRights): Обновления прав пользователя.

        Returns:
            User | None: Обновленный пользователь или None, если пользователь с
                таким именем не найден.
        """
        user = self.get_user(username)
        if user is None:
            return None
        user_rights_dump = user_rights.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_rights_dump)
        with Session(self._engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
