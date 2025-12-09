import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db import Base
#import src.models.expenses
#No hay que llamar a nuestros modelos?
engine = create_engine("sqlite:///:memory:",echo=True)
Session = sessionmaker(bind=engine)

##Creamos unas categorias de prueba


@pytest.fixture()
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()