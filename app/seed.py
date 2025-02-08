from sqlalchemy.orm import Session
from app.models import Module, Chapter, Quiz
from app.database import engine, SessionLocal


def seed_data():
    db: Session = SessionLocal()

    # Clear existing data (for development purposes only)
    db.query(Quiz).delete()
    db.query(Chapter).delete()
    db.query(Module).delete()
    db.commit()

    # Seed modules
    module = Module(title="Introduction to Machine Learning", description="Learn the basics of machine learning.")
    db.add(module)
    db.commit()

    # Seed chapters
    chapter1 = Chapter(module_id=module.id, title="Data Preprocessing", content="This is content about data preprocessing.")
    chapter2 = Chapter(module_id=module.id, title="EDA (Exploratory Data Analysis)", content="This is content about EDA.")
    db.add_all([chapter1, chapter2])
    db.commit()

    # Seed quizzes
    quiz1 = Quiz(
        chapter_id=chapter1.id,
        question="What should you do first with raw data?",
        option_a="Start analyzing immediately",
        option_b="Clean and organize it",
        option_c="Ignore it and rely on intuition",
        correct_option="b",
        hint_a="Jumping into analysis without cleaning can lead to incorrect insights.",
        hint_c="Ignoring the data isn't a good practice!"
    )
    quiz2 = Quiz(
        chapter_id=chapter2.id,
        question="What is the purpose of EDA?",
        option_a="To clean the dataset",
        option_b="To explore and visualize data",
        option_c="To build the final model",
        correct_option="b",
        hint_a="Cleaning is part of preprocessing, not EDA.",
        hint_c="Model building happens after EDA, not during."
    )
    db.add_all([quiz1, quiz2])
    db.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
