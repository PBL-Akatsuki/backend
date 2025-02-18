from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Quiz
from app.schemas import QuizResponse
from typing import List

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.get("/{chapter_id}", response_model=List[QuizResponse])
def get_quiz_for_chapter(chapter_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.chapter_id == chapter_id).all()
    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No quizzes found for chapter {chapter_id}"
        )
    return quizzes


@router.post("/validate/{quiz_id}")
def validate_quiz_answer(quiz_id: int, user_answer: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quiz with id {quiz_id} not found"
        )
    # Make the comparison case-insensitive
    if quiz.correct_option.lower() == user_answer.lower():
        return {"result": "correct"}
    else:
        hint = getattr(
            quiz, f"hint_{user_answer.lower()}", "No hint available.")
        return {"result": "incorrect", "hint": hint}
