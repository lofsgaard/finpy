from sqlmodel import create_engine, Session
from app.core.db.models import SQLModel
from app.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_session():
    """Create a new SQLModel session."""
    yield Session(engine)
    