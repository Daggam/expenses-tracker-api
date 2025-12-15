from datetime import date
import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator

class ExpenseRangeType(str,Enum):
    PAST_WEEK = 'past_week'
    PAST_MONTH = 'past_month'
    LAST_THREE_MONTHS = 'past_three_months'
    CUSTOM = 'custom'

class ExpenseOut(BaseModel):
    name:str
    category:str
    createdAt:date

    model_config = ConfigDict(from_attributes=True)
    @field_validator('createdAt',mode='before')
    @classmethod
    def cast_datetime_to_date(cls,value:datetime) -> date:
        return value.date()

class ExpenseIn(BaseModel):
    name:str
    category:str

class ExpenseUpdate(BaseModel):
    name:str|None = None
    category:str|None = None