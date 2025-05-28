from entities import User
from sqlalchemy.orm import Session


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def CreateUser(self, new_user: User) -> User:
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)  # Refresh to get the ID and other fields

        return new_user

    def GetUserByName(self, name: str):

        return self.db.query(User).filter(User.username == name).first()