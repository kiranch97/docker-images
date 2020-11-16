from typing import Any, List

from loguru import logger
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.logic.users import get_current_active_user, get_current_active_superuser

from app import models
from app import schemas
from app import crud

router = APIRouter()


@router.get("/users/me", response_model=schemas.User)
def get_current_user(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    return current_user


@router.post("/users", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get_by_id(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.get("/users", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_all(db)
    return users


@router.get("/users-unauth", response_model=List[schemas.UserMinimal])
def read_users_unauthorized(
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_all(db)
    return users


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get_by_id(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
