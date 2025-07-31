from sqlalchemy import create_engine, String, Column, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
from contextlib import contextmanager
from lib.initial import CONFIG_DIR
import secrets
import bcrypt
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
    _password = Column("password", String, nullable=True)

    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, raw_password):
        if raw_password is None:
            self._password = None
        else:
            hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
            self._password = hashed.decode("utf-8")

    def verify_password(self, raw_password):
        if not self._password or raw_password is None:
            return False
        return bcrypt.checkpw(raw_password.encode("utf-8"), self._password.encode("utf-8"))

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
    
def fetch_user(**kwargs):
    with session_scope() as session:
        return session.query(User).filter_by(**kwargs).first()
    
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
    
def create_new_user(**kwargs):
    with session_scope() as session:
        user = User(**kwargs)
        session.add(user)
        session.commit()
        return user
    return None

def delete_user_sessions(user_id):
    with session_scope() as session:
        print(session.query(Session).filter(Session.user_id == user_id).all())
        for user_session in session.query(Session).filter(Session.user_id == user_id).all():
            session.delete(user_session)
            session.commit()

def create_user_session(user_id):
    with session_scope() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_session = Session(
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(days=365)
            )

            session.add(user_session)
            session.commit()
            session.refresh(user_session)

            return user_session
        return None
            