from sqlalchemy import create_engine, String, Column, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from contextlib import contextmanager
from lib.initial import CONFIG_DIR
import secrets
import os

ENGINE = create_engine(f'sqlite:///{os.path.join(CONFIG_DIR, "aurbit.db")}', echo=False, future=True)

SessionLocal = scoped_session(sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True, expire_on_commit=False))

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    displayName = Column(String, nullable=False)
    access = Column(Integer, default=0) # 0: superuser, # 1: normal user... ( to be expanded later )
    initialized = Column(Boolean, default=False)
    password = Column(String)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    user = relationship("User", backref="sessions")

class RateLimit(Base):
    __tablename__ = "ratelimit"
    id = Column(Integer, primary_key=True, index=True)
    ip_addr = Column(String, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    seconds = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    url = Column(String, nullable=False)

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
    
def fetch_ratelimit(**kwargs):
    with session_scope() as session:
        
        instance = session.query(RateLimit).filter_by(**kwargs).first()
        if instance: return instance
        instance = RateLimit(**kwargs, attempts=0, seconds=0)
        session.add(instance)
        session.flush()
        return instance
    
def update_ratelimit(id, **kwargs):
    with session_scope() as session:
        session.query(RateLimit).filter_by(id=id).update({**kwargs})

def fetch_session(**kwargs):
    with session_scope() as session:
        return session.query(Session).filter_by(**kwargs).one_or_none()