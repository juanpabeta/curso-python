import argparse

from app.auth.services import hash_password
from app.core.config import settings
from app.core.database import SessionLocal
from app.users.services import create_user
from app.users.repository import SqlUserRepository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", nargs="?")
    parser.add_argument("password", nargs="?")
    args = parser.parse_args()

    username = args.username or settings.admin_username
    password = args.password or settings.admin_password
    if not username:
        parser.error("indica un usuario o define ADMIN_USERNAME")
    if not password:
        parser.error("indica una contraseña o define ADMIN_PASSWORD")

    with SessionLocal() as db:
        create_user(SqlUserRepository(db), username, hash_password(password))


if __name__ == "__main__":
    main()
