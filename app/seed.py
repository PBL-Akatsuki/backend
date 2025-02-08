from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Module, Chapter, Quiz

def seed_data():
    db: Session = SessionLocal()
    try:
        # 1. Seed a Module (required by Chapter)
        module = Module(
            title="Data Science Module",
            description="A module covering data science fundamentals."
        )
        db.add(module)
        db.commit()  # Commit to generate an ID for the module
        db.refresh(module)
        
        # 2. Seed a Chapter that belongs to the module
        chapter = Chapter(
            module_id=module.id,
            title="Data Preprocessing Chapter",
            content="Content explaining data preprocessing steps."
        )
        db.add(chapter)
        db.commit()  # Commit to generate an ID for the chapter
        db.refresh(chapter)
        
        # 3. Seed Quizzes that reference the chapter
        quizzes = [
            Quiz(
                chapter_id=chapter.id,
                question="What is data preprocessing?",
                option_a="Cleaning",
                option_b="Visualization",
                option_c="Analysis",
                correct_option="A",
                hint_a="Correct! Data preprocessing involves cleaning data.",
                hint_b="Hint B",
                hint_c="Hint C"
            ),
            Quiz(
                chapter_id=chapter.id,
                question="Which is a common data preprocessing step?",
                option_a="Data scaling",
                option_b="Data clustering",
                option_c="Model training",
                correct_option="A",
                hint_a="Correct! Scaling is a key preprocessing step.",
                hint_b="Hint B",
                hint_c="Hint C"
            ),
        ]
        db.add_all(quizzes)
        db.commit()
        print("Data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
