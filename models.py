from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Password will be hashed
    height = Column(Float, nullable=False)

# Weight Entries model
class WeightEntry(Base):
    __tablename__ = 'weight_entries'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(Date, default=date.today, nullable=False)
