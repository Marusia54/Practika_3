from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

BaseUser = declarative_base()


class UserEntity(BaseUser):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_sequence"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hash_password = Column(String)
    additional_info = relationship("UserAdditionalInfoEntity", cascade="all,delete", backref="UserEntity")


class UserAdditionalInfoEntity(BaseUser):
    __tablename__ = "additional_info"
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    data = Column(String)


class UserAdditionalInfo(BaseModel):
    id: int
    id_user: int
    data: str


class User(BaseModel):
    id: int
    name: str
    hash_password: str
