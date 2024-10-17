from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User, WeightEntry
from database import engine, get_db
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import date
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str
    height: float

class WeightCreate(BaseModel):
    username: str
    weight: float
    date: date  

    def __init__(self, **data):
        if 'date' not in data or data['date'] is None:
            data['date'] = date.today()  
        super().__init__(**data)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password, height=user.height)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/new_weight")
def new_weight(weight_data: WeightCreate, db: Session = Depends(get_db)):
    if not weight_data.date:
        weight_data.date = date.today()  
    
    db_weight = db.query(WeightEntry).filter(WeightEntry.username == weight_data.username,WeightEntry.date == weight_data.date).first()
    if db_weight:
        db_weight.weight = weight_data.weight  
    else:
        new_entry = WeightEntry(username=weight_data.username, weight=weight_data.weight, date=weight_data.date)
        db.add(new_entry)
    
    db.commit()
    return {"message": "Weight entry updated/created successfully"}

@app.get("/current_weight/{username}")
def current_weight(username: str, db: Session = Depends(get_db)):
    latest_entry = db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date.desc()).first()
    if not latest_entry:
        raise HTTPException(status_code=404, detail="No weight entries found for this user")
    return {"username": username, "current_weight": latest_entry.weight}

@app.get("/weight_change/{username}")
def weight_change(username: str, db: Session = Depends(get_db)):
    entries = db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No weight entries found for this user")
    first_weight = entries[0].weight
    last_weight = entries[-1].weight
    return {"username": username, "weight_change": last_weight - first_weight}

@app.get("/bmi/{username}")
def calculate_bmi(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    latest_entry = db.query(WeightEntry).filter(WeightEntry.username == username).order_by(WeightEntry.date.desc()).first()
    
    if not user or not latest_entry:
        raise HTTPException(status_code=404, detail="User or weight entry not found")
    
    height_m = user.height / 100  
    bmi = latest_entry.weight / (height_m ** 2)
    return {"username": username, "bmi": bmi}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)