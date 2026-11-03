from app.users.exceptions import UserAlreadyExists, UserNotFound
from app.users.models import UserModel
from app.users.ports import UserRepository


def create_user(repository: UserRepository, username: str, password_hash: str) -> UserModel:
    if repository.get_by_username(username):
        raise UserAlreadyExists("El usuario ya existe")
    return repository.add(UserModel(username=username, password_hash=password_hash))


def find_user_by_username(repository: UserRepository, username: str) -> UserModel:
    user = repository.get_by_username(username)
    if user is None:
        raise UserNotFound("Usuario no encontrado")
    return user
