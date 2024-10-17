from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()


class User(Base):
    __tablename__ = 'users_of_sportsmen'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  
    height = Column(Float, nullable=False)

class WeightEntry(Base):
    __tablename__ = 'weight_entries'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(Date, default=date.today, nullable=False)