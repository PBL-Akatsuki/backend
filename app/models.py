try:
    from app.database import Base
except ImportError:
    from database import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # Tracks chapter progression
    progress = Column(Integer, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text(
        'CURRENT_TIMESTAMP'), nullable=False)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)

    chapters = relationship("Chapter", back_populates="module")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    module = relationship("Module", back_populates="chapters")
    quizzes = relationship("Quiz", back_populates="chapter")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    hint_a = Column(String, nullable=True)
    hint_b = Column(String, nullable=True)
    hint_c = Column(String, nullable=True)

    chapter = relationship("Chapter", back_populates="quizzes")
