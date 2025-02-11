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

# ================================================= #
# ADD THIS CONTENT TO DATABASE IF NOT ALREADY Added #
# ================================================= #


# INSERT INTO public.quizzes (
#     id, chapter_id, question, option_a, option_b, option_c, correct_option, hint_a, hint_b, hint_c
# )
# VALUES
# (1, 1, 'What’s the first thing Riley should do with the raw data?',
#  'Start analyzing it immediately.',
#  'Clean and organize it.',
#  'Ignore it and rely on intuition.',
#  'B',
#  'Hmm, it’s tempting to dive in, but a good foundation is key. You’ll want to prepare the data first to avoid errors.',
#  'Great job! Cleaning and organizing the data ensures that your analysis is based on accurate and reliable information.',
#  'Relying on intuition alone can lead you astray. Trusting the data will guide you to better insights.'),

# (2, 1, 'The server logs are missing timestamps for the last 24 hours before the shutdown. What should Riley do?',
#  'Remove those rows.',
#  'Fill in the missing timestamps using the average time interval.',
#  'Assume the logs are irrelevant.',
#  'B',
#  'Removing rows might seem like an easy fix, but you could lose valuable insights by discarding data.',
#  'Smart choice! Filling in the missing timestamps ensures that the data remains consistent and usable for analysis.',
#  'Assuming the logs are irrelevant might lead to missing key patterns. It’s always best to find a way to use the data!'),

# (3, 1, 'How would Riley encode the player levels?',
#  'Beginner = 1, Intermediate = 2, Advanced = 3.',
#  'Beginner = 0, Intermediate = 1, Advanced = 2.',
#  'Leave them as text.',
#  'B',
#  'While this might seem like a simple mapping, starting from 0 can make the model interpret the data more naturally.',
#  'Great choice! Encoding the levels numerically helps the model understand the data better and improves processing efficiency.',
#  'Leaving them as text could confuse the model. Encoding helps make the data more meaningful for analysis.'),

# (4, 1, 'Riley finds a transaction where a player spent $1 million in NeoVerse coins. What should they do?',
#  'Remove the transaction as an outlier.',
#  'Investigate it further—it might be a clue.',
#  'Leave it in the dataset.',
#  'B',
#  'Removing outliers might seem like the easy way out, but sometimes outliers hold valuable information.',
#  'Nice approach! Investigating the transaction could uncover an important pattern or insight that helps you understand player behavior.',
#  'Leaving it without investigation could lead to missed opportunities to discover something important.'),

# (5, 1, 'Player levels range from 0 to 100, and transaction amounts range from $0 to $1 million. How should Riley scale them?',
#  'Normalize both to 0-1.',
#  'Standardize both to have a mean of 0.',
#  'Leave them as they are.',
#  'A',
#  'While this split isn’t wrong, giving a bit more focus to validation and test sets might reduce the training data available.',
#  'Great choice! Normalizing both to the 0-1 range ensures that the data is on the same scale, making it easier for the model to process and compare.',
#  'Leaving them as they are could lead to the model being biased by differences in the scale of the features.'),

# (6, 1, 'How should Riley combine the server logs and user profiles?',
#  'Merge them based on user IDs.',
#  'Concatenate them vertically.',
#  'Keep them separate.',
#  'A',
#  'Concatenating vertically might lead to mismatches and inconsistencies, so merging based on user IDs is a safer approach.',
#  'Nice choice! Merging the data based on user IDs allows you to integrate relevant information and analyze the user’s behavior more holistically.',
#  'Keeping them separate might make it harder to draw connections between the server logs and user profiles.'),

# (7, 1, 'Riley has 10,000 rows of cleaned data. How should they split it?',
#  '70% training, 20% validation, 10% test.',
#  '60% training, 20% validation, 20% test.',
#  '80% training, 10% validation, 10% test.',
#  'A',
#  'While this split isn’t wrong, giving a bit more focus to validation and test sets might reduce the training data available.',
#  'Great call! Splitting the data this way gives enough training data for the model, while still reserving a healthy portion for validation and testing.',
#  'Using a heavy split like 80% for training could leave you with too little data for validation and testing, making evaluation less reliable.'),

# (8, 1, 'Riley finds that “age” and “birth year” are highly correlated. What should they do?',
#  'Remove one of the features.',
#  'Keep both features.',
#  'Combine them into a new feature.',
#  'A',
#  'Keeping both could introduce redundancy, making it harder for the model to identify patterns without overfitting.',
#  'Smart move! Removing one of the correlated features helps reduce multicollinearity and keeps the model simpler and more efficient.',
#  'Combining them might not provide much new information and could complicate the feature set unnecessarily.');
