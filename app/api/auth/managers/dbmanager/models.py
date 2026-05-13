"""Модели для менеджера БД."""

from sqlmodel import Field, SQLModel


class AbscractUser(SQLModel):
    """Абстрактная модель пользователя.
    
    Params:
        username (str): Имя пользователя.
    """
    username: str
    

class User(AbscractUser, table=True):
    """Модель-таблица пользователей.
    
    Params:
        id (int | None): ID пользователя. PRIMARY KEY. По умолчанию None.
            Предполагается использование сугубо стандартного значения для того,
            чтобы ID пользователя назначала БД.
        username (str): Имя пользователя. UNIQUE.
        hashed_password (str): Хешированный пароль.
        is_verified (bool): Флаг верифицированности пользователя. По умолчанию
            False.
        is_moderator (bool): Флаг, является ли пользователь модератором. По
            умолчанию False.
        is_banned (bool): Флаг забаненности пользователя. По умолчанию False.
    """
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    is_verified: bool = Field(default=False)
    is_moderator: bool = Field(default=False)
    is_banned: bool = Field(default=False)


class UserPublic(AbscractUser):
    """Модель публичных данных о пользователе.
    
    Params:
        id (int): ID пользователя.
        username (str): Имя пользователя.
        is_verified (bool): Флаг верифицированности пользователя.
        is_moderator (bool): Флаг, является ли пользователь модератором.
        is_banned (bool): Флаг забаненности пользователя.
    """
    id: int
    is_verified: bool
    is_moderator: bool
    is_banned: bool


class UserCreate(AbscractUser):
    """Модель данных для создания пользователя.
    
    Params:
        username (str): Имя пользователя.
        hashed_password (str): Хешированный пароль.
    """
    hashed_password: str
