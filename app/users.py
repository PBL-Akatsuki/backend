from typing import List, Dict, Any
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
import app.models as models
import app.schemas as schemas
from app.models import User
from app.schemas import CreateUser
from app.database import get_db

router = APIRouter(
    prefix='/user',
    tags=['User']
)

# db = next(get_db())

@router.get('/', response_model=List[schemas.CreateUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

def create_user(db: Session, user: CreateUser,):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/create-user', status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: CreateUser, db:Session = Depends(get_db)):
    created_user = create_user(db, user_data)
    print(f"User created with ID: {created_user.id}, username: {created_user.username}, email: {created_user.email}")
    return created_user

@router.delete('/delete-user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted_user = db.query(models.User).filter(models.User.id == id)
    if deleted_user.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    deleted_user.delete(synchronize_session=False)
    db.commit()

@router.patch('/update-user/{id}', response_model=schemas.CreateUser)
def patch_user(id: int, update_data: Dict[str, Any], db: Session = Depends(get_db)):
    patch_query = db.query(models.User).filter(models.User.id == id)
    patch_user = patch_query.first()

    if patch_user is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The mood with id: {id} does not exist")
    
    for key, value in update_data.items():
        if hasattr(patch_user, key):
            setattr(patch_user, key, value)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid field: {key}")

    db.commit()
    db.refresh(patch_user)

    return patch_user