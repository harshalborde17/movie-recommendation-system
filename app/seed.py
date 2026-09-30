## Its purpose is to load the sample JSON into SQLite.

import json
from pathlib import Path

from .crud import create_or_update_movie
from .database import Base, SessionLocal, engine
from .schemas import MovieCreate

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sample_movies.json"


def main():
    Base.metadata.create_all(bind=engine)

    with DATA_FILE.open("r", encoding="utf-8") as file:
        movies = json.load(file)

    db = SessionLocal()
    try:
        for item in movies:
            create_or_update_movie(db, MovieCreate(**item))
        print(f"Seeded/updated {len(movies)} movies.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
