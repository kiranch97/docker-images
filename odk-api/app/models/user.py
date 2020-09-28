import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.sqltypes import Boolean

from app.db.base_class import Base

class User(Base):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    department = Column(String, index=True)
    vehicle_type = Column(String, index=True)
    
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)