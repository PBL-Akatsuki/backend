import os
import sys
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Module, Chapter, Quiz, NeoverseLog

# Ensure `app/` is in the module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def seed_data():
    """Seeds initial module, chapter, and quiz data if not already present."""
    db: Session = SessionLocal()
    try:
        # Check if the module already exists to avoid duplicate seeding
        existing_module = db.query(Module).filter_by(
            title="Data Science Module").first()
        if existing_module:
            print("Data already seeded, skipping seeding process.")
        else:
            # 1. Seed a Module (required by Chapters)
            module = Module(
                title="Data Science Module",
                description="A module covering data science fundamentals."
            )
            db.add(module)
            db.commit()  # Commit to generate an ID for the module
            db.refresh(module)

            # 2. Seed Chapter 1 for Data Preprocessing
            chapter1 = Chapter(
                module_id=module.id,
                title="Data Preprocessing Chapter",
                content="Content explaining data preprocessing steps."
            )
            db.add(chapter1)
            db.commit()  # Commit to generate an ID for chapter 1
            db.refresh(chapter1)

            # 3. Seed Quizzes for Chapter 1 (Data Preprocessing)
            quizzes_ch1 = [
                Quiz(
                    chapter_id=chapter1.id,
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
                    chapter_id=chapter1.id,
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
                    chapter_id=chapter1.id,
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
                    chapter_id=chapter1.id,
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
                    chapter_id=chapter1.id,
                    question="Player levels range from 0 to 100, and transaction amounts range from $0 to $1 million. How should Riley scale them?",
                    option_a="Normalize both to 0-1.",
                    option_b="Standardize both to have a mean of 0.",
                    option_c="Leave them as they are.",
                    correct_option="A",
                    hint_a="While this split isn't wrong, normalization ensures all features contribute equally.",
                    hint_b="Great choice! Normalizing both to the 0-1 range makes it easier for the model to process and compare features.",
                    hint_c="Leaving them as they are could lead to the model being biased by differences in scale."
                ),
                Quiz(
                    chapter_id=chapter1.id,
                    question="How should Riley combine the server logs and user profiles?",
                    option_a="Merge them based on user IDs.",
                    option_b="Concatenate them vertically.",
                    option_c="Keep them separate.",
                    correct_option="A",
                    hint_a="Concatenating vertically might lead to mismatches and inconsistencies.",
                    hint_b="Nice choice! Merging based on user IDs integrates relevant information for a holistic analysis.",
                    hint_c="Keeping them separate might make it harder to draw meaningful connections."
                ),
                Quiz(
                    chapter_id=chapter1.id,
                    question="Riley has 10,000 rows of cleaned data. How should they split it?",
                    option_a="70% training, 20% validation, 10% test.",
                    option_b="60% training, 20% validation, 20% test.",
                    option_c="80% training, 10% validation, 10% test.",
                    correct_option="A",
                    hint_a="While other splits are possible, this balance provides enough data for training while preserving samples for validation and testing.",
                    hint_b="Great call! This split provides a robust balance between training and evaluation data.",
                    hint_c="Using a heavy training split may reduce the reliability of validation and testing results."
                ),
                Quiz(
                    chapter_id=chapter1.id,
                    question="Riley finds that 'age' and 'birth year' are highly correlated. What should they do?",
                    option_a="Remove one of the features.",
                    option_b="Keep both features.",
                    option_c="Combine them into a new feature.",
                    correct_option="A",
                    hint_a="Keeping both can lead to redundancy and overfitting.",
                    hint_b="Smart move! Removing one helps reduce multicollinearity and simplifies the model.",
                    hint_c="Combining them might add complexity without offering additional value."
                ),
            ]
            db.add_all(quizzes_ch1)
            db.commit()

            # 4. Seed Chapter 2 for Exploratory Data Analysis (EDA)
            chapter2 = Chapter(
                module_id=module.id,
                title="Exploratory Data Analysis Chapter",
                content="Content explaining exploratory data analysis, trends, and feature selection."
            )
            db.add(chapter2)
            db.commit()  # Commit to generate an ID for chapter 2
            db.refresh(chapter2)

            # 5. Seed Quizzes for Chapter 2 (EDA)
            quizzes_ch2 = [
                Quiz(
                    chapter_id=chapter2.id,
                    question="Which visualization is most useful for quickly spotting outliers in a dataset?",
                    option_a="Scatterplot",
                    option_b="Boxplot",
                    option_c="Line Chart",
                    correct_option="B",
                    hint_a="Scatterplots are useful for showing relationships but not specifically designed to highlight outliers.",
                    hint_b="Correct! Boxplots clearly display the distribution and pinpoint outliers in the data.",
                    hint_c="Line charts are typically used to show trends over time, not to identify outliers."
                ),
                Quiz(
                    chapter_id=chapter2.id,
                    question="Which visualization is best suited to show the overall strength of relationships between multiple features simultaneously?",
                    option_a="Scatterplot",
                    option_b="Heatmap",
                    option_c="Histogram",
                    correct_option="B",
                    hint_a="Scatterplots work well for two variables, but not for many features at once.",
                    hint_b="Correct! Heatmaps provide a color-coded overview of the correlation coefficients between multiple features.",
                    hint_c="Histograms display distributions rather than inter-feature relationships."
                ),
                Quiz(
                    chapter_id=chapter2.id,
                    question="Which feature selection method transforms multiple original features into a few key components that capture most of the data's variance?",
                    option_a="Random Forest Feature Importance",
                    option_b="Principal Component Analysis (PCA)",
                    option_c="Heatmap Visualization",
                    correct_option="B",
                    hint_a="Random Forest ranks features based on their importance, but doesn't combine them into fewer components.",
                    hint_b="Correct! PCA reduces the dimensionality of the dataset by converting the original features into principal components.",
                    hint_c="Heatmaps are used to visualize correlations, not to reduce feature dimensions."
                ),

            ]
            db.add_all(quizzes_ch2)
            db.commit()

            print("Data seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

# def seed_data():
#     """Seeds initial module, chapter, and quiz data unconditionally."""
#     db: Session = SessionLocal()
#     try:
#         # 1. Seed a Module (required by Chapters)
#         module = Module(
#             title="Data Science Module",
#             description="A module covering data science fundamentals."
#         )
#         db.add(module)
#         db.commit()  # Commit to generate an ID for the module
#         db.refresh(module)

#         # 2. Seed Chapter 1 for Data Preprocessing
#         chapter1 = Chapter(
#             module_id=module.id,
#             title="Data Preprocessing Chapter",
#             content="Content explaining data preprocessing steps."
#         )
#         db.add(chapter1)
#         db.commit()  # Commit to generate an ID for chapter 1
#         db.refresh(chapter1)

#         # 3. Seed Quizzes for Chapter 1 (Data Preprocessing)
#         quizzes_ch1 = [
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="What's the first thing Riley should do with the raw data?",
#                 option_a="Start analyzing it immediately.",
#                 option_b="Clean and organize it.",
#                 option_c="Ignore it and rely on intuition.",
#                 correct_option="B",
#                 hint_a="Hmm, it's tempting to dive in, but a good foundation is key. You'll want to prepare the data first to avoid errors.",
#                 hint_b="Great job! Cleaning and organizing the data ensures that your analysis is based on accurate and reliable information.",
#                 hint_c="Relying on intuition alone can lead you astray. Trusting the data will guide you to better insights."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="The server logs are missing timestamps for the last 24 hours before the shutdown. What should Riley do?",
#                 option_a="Remove those rows.",
#                 option_b="Fill in the missing timestamps using the average time interval.",
#                 option_c="Assume the logs are irrelevant.",
#                 correct_option="B",
#                 hint_a="Removing rows might seem like an easy fix, but you could lose valuable insights by discarding data.",
#                 hint_b="Smart choice! Filling in the missing timestamps ensures that the data remains consistent and usable for analysis.",
#                 hint_c="Assuming the logs are irrelevant might lead to missing key patterns. It's always best to find a way to use the data!"
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="How would Riley encode the player levels?",
#                 option_a="Beginner = 1, Intermediate = 2, Advanced = 3.",
#                 option_b="Beginner = 0, Intermediate = 1, Advanced = 2.",
#                 option_c="Leave them as text.",
#                 correct_option="B",
#                 hint_a="While this might seem like a simple mapping, starting from 0 can make the model interpret the data more naturally.",
#                 hint_b="Great choice! Encoding the levels numerically helps the model understand the data better and improves processing efficiency.",
#                 hint_c="Leaving them as text could confuse the model. Encoding helps make the data more meaningful for analysis."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="Riley finds a transaction where a player spent $1 million in NeoVerse coins. What should they do?",
#                 option_a="Remove the transaction as an outlier.",
#                 option_b="Investigate it further—it might be a clue.",
#                 option_c="Leave it in the dataset.",
#                 correct_option="B",
#                 hint_a="Removing outliers might seem like the easy way out, but sometimes outliers hold valuable information.",
#                 hint_b="Nice approach! Investigating the transaction could uncover an important pattern or insight that helps you understand player behavior.",
#                 hint_c="Leaving it without investigation could lead to missed opportunities to discover something important."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="Player levels range from 0 to 100, and transaction amounts range from $0 to $1 million. How should Riley scale them?",
#                 option_a="Normalize both to 0-1.",
#                 option_b="Standardize both to have a mean of 0.",
#                 option_c="Leave them as they are.",
#                 correct_option="A",
#                 hint_a="While this split isn't wrong, normalization ensures all features contribute equally.",
#                 hint_b="Great choice! Normalizing both to the 0-1 range makes it easier for the model to process and compare features.",
#                 hint_c="Leaving them as they are could lead to the model being biased by differences in scale."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="How should Riley combine the server logs and user profiles?",
#                 option_a="Merge them based on user IDs.",
#                 option_b="Concatenate them vertically.",
#                 option_c="Keep them separate.",
#                 correct_option="A",
#                 hint_a="Concatenating vertically might lead to mismatches and inconsistencies.",
#                 hint_b="Nice choice! Merging based on user IDs integrates relevant information for a holistic analysis.",
#                 hint_c="Keeping them separate might make it harder to draw meaningful connections."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="Riley has 10,000 rows of cleaned data. How should they split it?",
#                 option_a="70% training, 20% validation, 10% test.",
#                 option_b="60% training, 20% validation, 20% test.",
#                 option_c="80% training, 10% validation, 10% test.",
#                 correct_option="A",
#                 hint_a="While other splits are possible, this balance provides enough data for training while preserving samples for validation and testing.",
#                 hint_b="Great call! This split provides a robust balance between training and evaluation data.",
#                 hint_c="Using a heavy training split may reduce the reliability of validation and testing results."
#             ),
#             Quiz(
#                 chapter_id=chapter1.id,
#                 question="Riley finds that 'age' and 'birth year' are highly correlated. What should they do?",
#                 option_a="Remove one of the features.",
#                 option_b="Keep both features.",
#                 option_c="Combine them into a new feature.",
#                 correct_option="A",
#                 hint_a="Keeping both can lead to redundancy and overfitting.",
#                 hint_b="Smart move! Removing one helps reduce multicollinearity and simplifies the model.",
#                 hint_c="Combining them might add complexity without offering additional value."
#             ),
#         ]
#         db.add_all(quizzes_ch1)
#         db.commit()

#         # 4. Seed Chapter 2 for Exploratory Data Analysis (EDA)
#         chapter2 = Chapter(
#             module_id=module.id,
#             title="Exploratory Data Analysis Chapter",
#             content="Content explaining exploratory data analysis, trends, and feature selection."
#         )
#         db.add(chapter2)
#         db.commit()  # Commit to generate an ID for chapter 2
#         db.refresh(chapter2)

#         # 5. Seed Quizzes for Chapter 2 (EDA)
#         quizzes_ch2 = [
#             Quiz(
#                 chapter_id=chapter2.id,
#                 question="Which visualization is most useful for quickly spotting outliers in a dataset?",
#                 option_a="Scatterplot",
#                 option_b="Boxplot",
#                 option_c="Line Chart",
#                 correct_option="B",
#                 hint_a="Scatterplots are useful for showing relationships but not specifically designed to highlight outliers.",
#                 hint_b="Correct! Boxplots clearly display the distribution and pinpoint outliers in the data.",
#                 hint_c="Line charts are typically used to show trends over time, not to identify outliers."
#             ),
#             Quiz(
#                 chapter_id=chapter2.id,
#                 question="Which visualization is best suited to show the overall strength of relationships between multiple features simultaneously?",
#                 option_a="Scatterplot",
#                 option_b="Heatmap",
#                 option_c="Histogram",
#                 correct_option="B",
#                 hint_a="Scatterplots work well for two variables, but not for many features at once.",
#                 hint_b="Correct! Heatmaps provide a color-coded overview of the correlation coefficients between multiple features.",
#                 hint_c="Histograms display distributions rather than inter-feature relationships."
#             ),
#             Quiz(
#                 chapter_id=chapter2.id,
#                 question="Which feature selection method transforms multiple original features into a few key components that capture most of the data's variance?",
#                 option_a="Random Forest Feature Importance",
#                 option_b="Principal Component Analysis (PCA)",
#                 option_c="Heatmap Visualization",
#                 correct_option="B",
#                 hint_a="Random Forest ranks features based on their importance, but doesn't combine them into fewer components.",
#                 hint_b="Correct! PCA reduces the dimensionality of the dataset by converting the original features into principal components.",
#                 hint_c="Heatmaps are used to visualize correlations, not to reduce feature dimensions."
#             ),

#         ]
#         db.add_all(quizzes_ch2)
#         db.commit()

#         print("Data seeded successfully!")
#     except Exception as e:
#         db.rollback()
#         print(f"Error seeding data: {e}")
#     finally:
#         db.close()


def upload_neoverse_logs():
    """Uploads `neoverse_logs.csv` to the database if not already inserted."""
    db: Session = SessionLocal()
    try:
        # Check if logs exist
        if db.query(NeoverseLog).first():
            print("Neoverse logs already exist, skipping upload.")
            return

        # Construct absolute path to CSV file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, "neoverse_logs.csv")

        # Check if CSV file exists
        if not os.path.exists(csv_file):
            print(f"Error: CSV file '{csv_file}' not found!")
            return

        print("Loading Neoverse logs from CSV...")

        # Load CSV file into DataFrame
        df = pd.read_csv(csv_file)

        # Ensure column names match database schema
        df.columns = [
            "player_id", "timestamp", "hours_played", "money_spent", "criminal_score",
            "missions_completed", "player_rank", "team_affiliation", "vip_status",
            "cash_on_hand", "sync_stability", "quest_exploit_score", "player_level",
            "dark_market_transactions", "transaction_amount", "neural_link_stability"
        ]

        # Convert timestamp to datetime format
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Debug: Show first few rows
        print("First 3 rows from CSV:")
        print(df.head(3))

        # Convert DataFrame to dictionary records and insert into the database
        records = df.to_dict(orient="records")
        db.bulk_insert_mappings(NeoverseLog, records)
        db.commit()
        print("Neoverse logs seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding Neoverse logs: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
    upload_neoverse_logs()
