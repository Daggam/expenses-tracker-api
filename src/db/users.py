from typing import List
from src.db.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship

class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(30))
    password_hash:Mapped[str] = mapped_column(String(100))

    expenses:Mapped[List['Expense']] = relationship(back_populates="user")
