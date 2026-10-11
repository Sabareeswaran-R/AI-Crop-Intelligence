from database.database import Base, engine
from database.models import Farmer, Farm, PredictionHistory


def init_database():
    Base.metadata.create_all(bind=engine)
    print("====================================")
    print("     DATABASE INITIALIZED")
    print("====================================")
    print("SQLite database created successfully.")
    print("Tables:")
    print("- farmers")
    print("- farms")
    print("- prediction_history")


if __name__ == "__main__":
    init_database()