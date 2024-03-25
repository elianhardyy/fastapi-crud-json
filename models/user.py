from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum, Boolean, DateTime
from config.database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, autoincrement=True)
    username=Column(String(255))
    email=Column(String(255),unique=True)
    password=Column(String(255))
    is_active=Column(Boolean,default=False)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    # class Config:
    #     schema_extra = [
    #         {
    #             "id": 0
    #         }
    #     ]

    