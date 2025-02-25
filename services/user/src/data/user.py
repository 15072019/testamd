from src.data.init import get_db
from src.model.user import User
from error import Missing, Duplicate
from sqlalchemy import exc
from src.data.schemas import UserBase

def get_all() -> list[UserBase]:
    db = next(get_db())
    return db.query(User).all()

def get_one(name: str) -> UserBase:
    db = next(get_db())
    row = db.query(User).filter(User.name == name).first()
    if row:
        return row
    else:
        raise Missing(msg=f"User {name} not found")

def create(user: UserBase) -> UserBase:
    if not user: return None
    db_item = User(user_id= user.id, name = user.name, username= user.username, password = user.password)
    db = next(get_db())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.username)
    except exc.IntegrityError:
        raise Duplicate(msg=f"User {user.username} already exists")

def modify(user_id: str, user: UserBase) -> UserBase:
    if not (user_id and user): return None
    db = next(get_db())
    item = db.query(User).filter(User.id == int(user_id)).one_or_none()
    if item:
        for var, value in vars(user).items():
            setattr(item, var, value) if value else None
        db.add(item)
        db.commit()
        db.refresh(item)
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {user.username} not found")

def delete(user_id: str):
    if not user_id: return False
    db = next(get_db())
    item = db.query(User).filter(User.id == int(user_id)).one_or_none()
    if item:
        db.delete(item)
        db.commit()
        return True
    else:
        raise Missing(msg=f"User not found")
