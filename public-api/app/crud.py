from sqlalchemy.orm import Session
from app.models import Meme
from app.schemas import MemeCreate, MemeUpdate


def get_meme(db: Session, meme_id: int):
    return db.query(Meme).filter(Meme.id == meme_id).first()


def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Meme).offset(skip).limit(limit).all()


def create_meme(db: Session, meme: MemeCreate):
    db_meme = Meme(**meme.dict())
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme_id: int, meme: MemeUpdate):
    db_meme = get_meme(db, meme_id=meme_id)
    if db_meme is None:
        return None
    for key, value in meme.dict().items():
        setattr(db_meme, key, value)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = get_meme(db, meme_id=meme_id)
    if db_meme is None:
        return None
    db.delete(db_meme)
    db.commit()
    return db_meme
