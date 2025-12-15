from datetime import datetime, timedelta, timezone
from typing import List
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db import Base
from src.db.expenses import Expense, ExpenseCategory
from src.db.users import User

engine = create_engine("sqlite:///:memory:",
                       connect_args={
                           "check_same_thread":False
                       },
                       poolclass=StaticPool)
TestingSession = sessionmaker(autocommit=False,autoflush=True,bind=engine)

## No es taan necesario hacerlo fixture, pero en caso de que manejemos una conexión distinta a una en memoria, si sería necesario por el Teardown
@pytest.fixture(scope="session",autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    with TestingSession() as session:
     ##Creamos unas categorias de prueba
     categorias = [ExpenseCategory(category='Prueba1'),
                   ExpenseCategory(category='Prueba2'),
                   ExpenseCategory(category='Prueba3')]
     session.add_all(categorias)
     ## Creamos usuarios de prueba
     users = [
         User(username='daggam',email='benjaminvilla409@gmail.com',password_hash='123456'),
         User(username='benja',email='daggamarg@gmail.com',password_hash='123456'),
         ]
     session.add_all(users)
     session.commit()
    yield


@pytest.fixture
def db_session():
    with engine.connect() as conn:
        conn.begin()
        session = TestingSession(bind=conn)
        try:
            yield session
        finally:
            session.close()
            conn.rollback()

@pytest.fixture
def create_expense(db_session):
    expenses = [
        Expense(name='Expensa 1 U1', id_user=1,id_category=1),
        Expense(name='Expensa 2 U1', id_user=1,id_category=2),
        Expense(name='Expensa 3 U1', id_user=1,id_category=2),
        Expense(name='Expensa 1 U2', id_user=2,id_category=1)
    ]

    db_session.add_all(expenses)
    db_session.commit()

@pytest.fixture
def create_expenses_datetimes(db_session):
    # Voy a crear 4 expenses con cada fecha.
    dates_dict:dict[str,datetime] = {}
    dates_dict["today"] = datetime.now(timezone.utc)
    dates_dict["today_week"] = dates_dict["today"] - timedelta(days=7) 
    dates_dict["today_month"] = dates_dict["today"] - timedelta(days=30)
    dates_dict["today_three_months"] = dates_dict["today"] - timedelta(days=90)
    
    expenses:List[Expense] = []
    for date_type,date_value in dates_dict.items():
        exps = [
            Expense(name=f'Expensa 1 U1 {date_type}', createdAt=date_value, id_user=1, id_category=1),
            Expense(name=f'Expensa 2 U1 {date_type}', createdAt=date_value, id_user=1, id_category=2),
            Expense(name=f'Expensa 3 U1 {date_type}', createdAt=date_value, id_user=1, id_category=2),
            Expense(name=f'Expensa 1 U2 {date_type}', createdAt=date_value, id_user=2, id_category=1)
        ]
        expenses+=exps

    db_session.add_all(expenses)
    db_session.commit()