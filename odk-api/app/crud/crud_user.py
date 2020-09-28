from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import get_password_hash

from app.models import User
from app.schemas import UserCreate

class CRUDUser():
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            department = obj_in.department,
            vehicle_type = obj_in.vehicle_type,
            is_superuser=obj_in.is_superuser,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user = CRUDUser()