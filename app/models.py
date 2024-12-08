try:
    from app.database import Base
except ImportError:
    from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
