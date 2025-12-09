import datetime
from typing import List
from src.db.db import Base
from sqlalchemy import String,DateTime,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.sql import func

class ExpenseCategory(Base):
    __tablename__ = 'expense_category'
    id:Mapped[int] = mapped_column(primary_key=True)
    category:Mapped[str] = mapped_column(String(50))
    #Relationships
    expenses:Mapped[List['Expense']] = relationship(back_populates='expense_category')

class Expense(Base):
    __tablename__ = 'expense'
    id:Mapped[int] = mapped_column(primary_key=True)
    id_category:Mapped[int] = mapped_column(ForeignKey('expense_category.id'))
    id_user:Mapped[int] = mapped_column(ForeignKey('user.id'))
    name:Mapped[str] = mapped_column(String(50))
    createAt:Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    
    #Relationships
    expense_category:Mapped['ExpenseCategory'] = relationship(back_populates='expenses')
    user:Mapped['User'] = relationship(back_populates='expenses')