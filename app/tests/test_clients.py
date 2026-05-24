import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Cria um banco de dados SQLite temporário em memória para os testes
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Mantém a conexão aberta na mesma thread durante o teste
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def fixture_session():
    # Cria todas as tabelas na memória antes de cada teste
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpa o banco de dados após o término do teste
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def fixture_client(session):
    # Sobrescreve a dependência get_db do FastAPI para usar a sessão de testes
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Limpa os overrides após o teste finalizar
    del app.dependency_overrides[get_db]