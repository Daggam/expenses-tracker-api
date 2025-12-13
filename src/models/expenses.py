from datetime import date
from enum import Enum
from pydantic import BaseModel

class ExpenseRangeType(str,Enum):
    PAST_WEEK = 'past_week'
    PAST_MONTH = 'past_month'
    LAST_THREE_MONTHS = 'past_three_months'
    CUSTOM = 'custom'

class ExpenseOut(BaseModel):
    name:str
    category:str
    createdAt:date

class ExpenseIn(BaseModel):
    name:str
    category:str

class ExpenseUpdate(BaseModel):
    name:str|None = None
    category:str|None = None