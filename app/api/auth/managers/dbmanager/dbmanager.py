"""Менеджер БД для аут.-авт."""

import os

from sqlmodel import Session, SQLModel, create_engine, select

from app.api.auth.managers.dbmanager.config import PATH_DB_DIR, SQLITE_URL
from app.api.auth.managers.dbmanager.models import User, UserCreate


class DBManager:
    def __init__(self):
        """Инициализация экземпляра менеджера БД."""
        self._create_db_directory()
        self._engine = create_engine(SQLITE_URL,
                                     connect_args={'check_same_thread': False})
        self._create_db_and_tables()
    
    def _create_db_directory(self) -> None:
        """Создать папку хранения БД, если нужно."""
        if not os.path.exists(PATH_DB_DIR):
            os.makedirs(PATH_DB_DIR)

    def _create_db_and_tables(self) -> None:
        """Создать БД и таблицы, если нужно."""
        SQLModel.metadata.create_all(self._engine)
    
    def get_user(self, username: str) -> User | None:
        """Получить данные пользователя из БД.

        Args:
            username (str): Имя пользователя.

        Returns:
            User | None: Данные пользователя из БД или None, если такого
                пользователя нет.
        """
        with Session(self._engine) as session:
            statement = select(User).where(User.username == username)
            result = session.exec(statement)
            user = result.first()
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
