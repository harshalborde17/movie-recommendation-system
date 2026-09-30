from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Scraper API",
    description="Internship project: movie scraping, storage and search API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "movie-scraper"}


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
