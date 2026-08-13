from app.database import Base, engine

from app import models # populate model data

def create_tables() -> None: 
    Base.metadata.create_all(bind=engine)

def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    ans = input("Do you want to drop tables first? (y/n): ")
    if ans.lower() == "y":
        drop_tables()
        print("Database tables dropped.")
    create_tables()
    print("Database tables created.")