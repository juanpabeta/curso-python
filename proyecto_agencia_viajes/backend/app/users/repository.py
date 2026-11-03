from sqlalchemy.orm import Session

from app.users.models import UserModel


class SqlUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> UserModel | None:
        row = self.db.query(UserModel).filter_by(username=username).first()
        return row

    def get(self, user_id: int) -> UserModel | None:
        row = self.db.get(UserModel, user_id)
        return row

    def add(self, user: UserModel) -> UserModel:
        row = UserModel(username=user.username, password_hash=user.password_hash, is_active=user.is_active)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row