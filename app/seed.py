from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Module, Chapter, Quiz


def seed_data():
    db: Session = SessionLocal()
    try:
        # Check if the module already exists to avoid duplicate seeding
        existing_module = db.query(Module).filter_by(
            title="Data Science Module").first()
        if existing_module:
            print("Data already seeded, skipping seeding process.")
            return

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
                question="What's the first thing Riley should do with the raw data?",
                option_a="Start analyzing it immediately.",
                option_b="Clean and organize it.",
                option_c="Ignore it and rely on intuition.",
                correct_option="B",
                hint_a="Hmm, it's tempting to dive in, but a good foundation is key. You'll want to prepare the data first to avoid errors.",
                hint_b="Great job! Cleaning and organizing the data ensures that your analysis is based on accurate and reliable information.",
                hint_c="Relying on intuition alone can lead you astray. Trusting the data will guide you to better insights."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="The server logs are missing timestamps for the last 24 hours before the shutdown. What should Riley do?",
                option_a="Remove those rows.",
                option_b="Fill in the missing timestamps using the average time interval.",
                option_c="Assume the logs are irrelevant.",
                correct_option="B",
                hint_a="Removing rows might seem like an easy fix, but you could lose valuable insights by discarding data.",
                hint_b="Smart choice! Filling in the missing timestamps ensures that the data remains consistent and usable for analysis.",
                hint_c="Assuming the logs are irrelevant might lead to missing key patterns. It's always best to find a way to use the data!"
            ),
            Quiz(
                chapter_id=chapter.id,
                question="How would Riley encode the player levels?",
                option_a="Beginner = 1, Intermediate = 2, Advanced = 3.",
                option_b="Beginner = 0, Intermediate = 1, Advanced = 2.",
                option_c="Leave them as text.",
                correct_option="B",
                hint_a="While this might seem like a simple mapping, starting from 0 can make the model interpret the data more naturally.",
                hint_b="Great choice! Encoding the levels numerically helps the model understand the data better and improves processing efficiency.",
                hint_c="Leaving them as text could confuse the model. Encoding helps make the data more meaningful for analysis."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="Riley finds a transaction where a player spent $1 million in NeoVerse coins. What should they do?",
                option_a="Remove the transaction as an outlier.",
                option_b="Investigate it further—it might be a clue.",
                option_c="Leave it in the dataset.",
                correct_option="B",
                hint_a="Removing outliers might seem like the easy way out, but sometimes outliers hold valuable information.",
                hint_b="Nice approach! Investigating the transaction could uncover an important pattern or insight that helps you understand player behavior.",
                hint_c="Leaving it without investigation could lead to missed opportunities to discover something important."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="Player levels range from 0 to 100, and transaction amounts range from $0 to $1 million. How should Riley scale them?",
                option_a="Normalize both to 0-1.",
                option_b="Standardize both to have a mean of 0.",
                option_c="Leave them as they are.",
                correct_option="A",
                hint_a="While this split isn't wrong, giving a bit more focus to validation and test sets might reduce the training data available.",
                hint_b="Great choice! Normalizing both to the 0-1 range ensures that the data is on the same scale, making it easier for the model to process and compare.",
                hint_c="Leaving them as they are could lead to the model being biased by differences in the scale of the features."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="How should Riley combine the server logs and user profiles?",
                option_a="Merge them based on user IDs.",
                option_b="Concatenate them vertically.",
                option_c="Keep them separate.",
                correct_option="A",
                hint_a="Concatenating vertically might lead to mismatches and inconsistencies, so merging based on user IDs is a safer approach.",
                hint_b="Nice choice! Merging the data based on user IDs allows you to integrate relevant information and analyze the user's behavior more holistically.",
                hint_c="Keeping them separate might make it harder to draw connections between the server logs and user profiles."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="Riley has 10,000 rows of cleaned data. How should they split it?",
                option_a="70% training, 20% validation, 10% test.",
                option_b="60% training, 20% validation, 20% test.",
                option_c="80% training, 10% validation, 10% test.",
                correct_option="A",
                hint_a="While this split isn't wrong, giving a bit more focus to validation and test sets might reduce the training data available.",
                hint_b="Great call! Splitting the data this way gives enough training data for the model, while still reserving a healthy portion for validation and testing.",
                hint_c="Using a heavy split like 80% for training could leave you with too little data for validation and testing, making evaluation less reliable."
            ),
            Quiz(
                chapter_id=chapter.id,
                question="Riley finds that \"age\" and \"birth year\" are highly correlated. What should they do?",
                option_a="Remove one of the features.",
                option_b="Keep both features.",
                option_c="Combine them into a new feature.",
                correct_option="A",
                hint_a="Keeping both could introduce redundancy, making it harder for the model to identify patterns without overfitting.",
                hint_b="Smart move! Removing one of the correlated features helps reduce multicollinearity and keeps the model simpler and more efficient.",
                hint_c="Combining them might not provide much new information and could complicate the feature set unnecessarily."
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
