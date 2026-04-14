from app.api.auth.managers.tokenmanager import TokenManager
from app.api.auth.managers.usermanager import UserManager


# экземпляры менеджеров для реализации синглтонов через импортирование
token_manager = TokenManager()
user_manager = UserManager()
