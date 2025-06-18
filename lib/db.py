from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine, String, Column, Integer
from contextlib import contextmanager
from lib.initial import CONFIG_DIR
import os

ENGINE = create_engine(f'sqlite:///{os.path.join(CONFIG_DIR, "aurbit.db")}', echo=False, future=True)

SessionLocal = scoped_session(sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True))

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    displayName = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=ENGINE)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        SessionLocal.remove()

def fetch_users():
    with session_scope() as session:
        return session.query(User).all()