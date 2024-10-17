from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User, WeightEntry
from datetime import date
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_new_user(db: Session, username: str, password: str, height: float):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password, height=height)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def add_or_update_weight(db: Session, username: str, weight: float, entry_date: date):
    db_weight = db.query(WeightEntry).filter(
        WeightEntry.username == username,
        WeightEntry.date == entry_date
    ).first()
    if db_weight:
        db_weight.weight = weight  
    else:
        new_entry = WeightEntry(username=username, weight=weight, date=entry_date)
        db.add(new_entry)
    db.commit()
    return {"message": "Weight entry updated/created successfully"}

def get_latest_weight(db: Session, username: str):
    latest_entry = db.query(WeightEntry).filter(
        WeightEntry.username == username
    ).order_by(WeightEntry.date.desc()).first()
    if not latest_entry:
        raise HTTPException(status_code=404, detail="No weight entries found for this user")
    return latest_entry.weight

def calculate_weight_change(db: Session, username: str):
    entries = db.query(WeightEntry).filter(
        WeightEntry.username == username
    ).order_by(WeightEntry.date).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No weight entries found for this user")
    first_weight = entries[0].weight
    last_weight = entries[-1].weight
    return last_weight - first_weight

def calculate_bmi(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    latest_weight = get_latest_weight(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    height_m = user.height / 100  
    bmi = latest_weight / (height_m ** 2)
    return bmi
