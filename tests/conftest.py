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