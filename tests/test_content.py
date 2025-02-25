import pytest
import os
import pandas as pd
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use the same import pattern as your test_users.py
try:
    from app.database import get_db, Base
    from app.main import app
    from app.models import Module, Chapter, Quiz, NeoverseLog
except ImportError:
    from database import get_db, Base
    from main import app
    from models import Module, Chapter, Quiz, NeoverseLog

# Test database setup - use the same connection string as your test_users.py
TEST_DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after tests are done
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(test_db):
    # Override the dependency to use our test database
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # Don't close here as it's managed by the test_db fixture

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Remove the override after testing
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def seed_test_data(test_db):
    """Create test data for modules, chapters, quizzes, and neoverse logs"""

    # Create a test module
    module = Module(
        title="Test Module",
        description="This is a test module"
    )
    test_db.add(module)
    test_db.commit()
    test_db.refresh(module)

    # Create test chapters
    chapter1 = Chapter(
        module_id=module.id,
        title="Test Chapter 1",
        content="This is test chapter 1 content"
    )
    chapter2 = Chapter(
        module_id=module.id,
        title="Test Chapter 2",
        content="This is test chapter 2 content"
    )
    test_db.add_all([chapter1, chapter2])
    test_db.commit()
    test_db.refresh(chapter1)
    test_db.refresh(chapter2)

    # Create test quizzes
    quiz1 = Quiz(
        chapter_id=chapter1.id,
        question="Test Question 1?",
        option_a="Test Option A",
        option_b="Test Option B",
        option_c="Test Option C",
        correct_option="A",
        hint_a="This is the correct answer",
        hint_b="This is incorrect",
        hint_c="This is also incorrect"
    )
    quiz2 = Quiz(
        chapter_id=chapter1.id,
        question="Test Question 2?",
        option_a="Another Option A",
        option_b="Another Option B",
        option_c="Another Option C",
        correct_option="B",
        hint_a="This is incorrect",
        hint_b="This is the correct answer",
        hint_c="This is also incorrect"
    )
    test_db.add_all([quiz1, quiz2])
    test_db.commit()

    # Create test neoverse log
    neoverse_log = NeoverseLog(
        player_id="TEST123",
        timestamp=datetime.now(),
        hours_played=10,
        money_spent=500,
        criminal_score=25,
        missions_completed=5,
        player_rank="Novice",
        team_affiliation="Blue",
        vip_status="Premium",
        cash_on_hand=1000,
        sync_stability=0.85,
        quest_exploit_score=70,
        player_level="5",
        dark_market_transactions="Low",
        transaction_amount=150,
        neural_link_stability=0.95
    )
    test_db.add(neoverse_log)
    test_db.commit()

    # Return IDs for use in tests
    return {
        "module_id": module.id,
        "chapter_ids": [chapter1.id, chapter2.id],
        "quiz_ids": [quiz1.id, quiz2.id],
        "player_id": "TEST123"
    }


# Module Tests
def test_module_creation(test_db, seed_test_data):
    """Test that a module can be created and retrieved"""
    module_id = seed_test_data["module_id"]
    module = test_db.query(Module).filter(Module.id == module_id).first()

    assert module is not None
    assert module.title == "Test Module"
    assert module.description == "This is a test module"


# Chapter Tests
def test_chapters_for_module(test_db, seed_test_data):
    """Test that chapters are associated with the correct module"""
    module_id = seed_test_data["module_id"]
    module = test_db.query(Module).filter(Module.id == module_id).first()

    assert len(module.chapters) == 2
    assert module.chapters[0].title.startswith("Test Chapter")
    assert module.chapters[1].title.startswith("Test Chapter")


def test_chapter_content(test_db, seed_test_data):
    """Test that chapter content is correctly stored"""
    chapter_id = seed_test_data["chapter_ids"][0]
    chapter = test_db.query(Chapter).filter(Chapter.id == chapter_id).first()

    assert chapter is not None
    assert "content" in chapter.content


# Quiz Tests
def test_get_quizzes_endpoint(client, seed_test_data):
    """Test the endpoint for getting quizzes for a chapter"""
    chapter_id = seed_test_data["chapter_ids"][0]
    response = client.get(f"/quiz/{chapter_id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["question"].startswith("Test Question")
    assert data[1]["question"].startswith("Test Question")


def test_validate_correct_answer(client, seed_test_data):
    """Test validating a correct quiz answer"""
    quiz_id = seed_test_data["quiz_ids"][0]
    response = client.post(f"/quiz/validate/{quiz_id}?user_answer=A")

    assert response.status_code == 200
    assert response.json()["result"] == "correct"


def test_validate_incorrect_answer(client, seed_test_data):
    """Test validating an incorrect quiz answer with hint"""
    quiz_id = seed_test_data["quiz_ids"][0]
    response = client.post(f"/quiz/validate/{quiz_id}?user_answer=B")

    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "incorrect"
    assert "hint" in data
    assert data["hint"] == "This is incorrect"


def test_quiz_not_found(client):
    """Test handling of non-existent quiz ID"""
    response = client.post("/quiz/validate/9999?user_answer=A")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# NeoverseLog Tests
def test_neoverse_log_creation(test_db, seed_test_data):
    """Test that a neoverse log can be created and retrieved"""
    player_id = seed_test_data["player_id"]
    log = test_db.query(NeoverseLog).filter(
        NeoverseLog.player_id == player_id).first()

    assert log is not None
    assert log.player_id == "TEST123"
    assert log.hours_played == 10
    assert log.money_spent == 500
    assert log.player_rank == "Novice"
    assert log.team_affiliation == "Blue"


# Relationship Tests
def test_module_chapter_relationship(test_db, seed_test_data):
    """Test the relationship between modules and chapters"""
    module_id = seed_test_data["module_id"]
    module = test_db.query(Module).filter(Module.id == module_id).first()
    chapter = module.chapters[0]

    # Test bidirectional relationship
    assert chapter.module.id == module.id
    assert chapter.module.title == "Test Module"


def test_chapter_quiz_relationship(test_db, seed_test_data):
    """Test the relationship between chapters and quizzes"""
    chapter_id = seed_test_data["chapter_ids"][0]
    chapter = test_db.query(Chapter).filter(Chapter.id == chapter_id).first()

    assert len(chapter.quizzes) == 2
    quiz = chapter.quizzes[0]

    # Test bidirectional relationship
    assert quiz.chapter.id == chapter.id
    assert quiz.chapter.title.startswith("Test Chapter")
