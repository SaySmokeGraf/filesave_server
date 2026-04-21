"""Менеджер БД для аут.-авт."""

from sqlmodel import Session, SQLModel, create_engine, select

from app.api.auth.managers.dbmanager.config import RoleToID, SQLITE_URL
from app.api.auth.managers.dbmanager.models import (
    Role, User, UserCreate
)


class DBManager:
    def __init__(self):
        """Инициализация экземпляра менеджера БД."""
        self._engine = create_engine(SQLITE_URL,
                                     connect_args={'check_same_thread': False})
        self._create_db_and_tables()
        self._add_roles()
    
    def _create_db_and_tables(self):
        """Создать БД и таблицы, если нужно."""
        SQLModel.metadata.create_all(self._engine)
    
    def _add_roles(self):
        """Добавить все предусмотренные роли в таблицу ролей, если нужно."""
        roles = (Role(id=RoleToID.UNVERIFIED, name='unverified'),
                 Role(id=RoleToID.USER, name='user'),
                 Role(id=RoleToID.REJECTED, name='rejected'),
                 Role(id=RoleToID.ADMIN, name='admin'))
        with Session(self._engine) as session:
            for role in roles:
                db_role = session.get(Role, role.id)
                if not db_role:
                    session.add(role)
                    session.commit()
    
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
