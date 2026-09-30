## API routes for the movie scraper application. 
## it defines endpoints for listing movies, retrieving movie details, creating movies, getting genres, statistics, and exporting data in CSV format.

import csv
import io
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from .crud import count_movies, create_or_update_movie, get_movie, get_movies
from .database import get_db
from .models import Movie
from .schemas import MovieCreate, MovieResponse

router = APIRouter(prefix="/api", tags=["Movies"])


@router.get("/movies", response_model=list[MovieResponse])
def list_movies(
    search: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = Query(default=None, ge=0, le=10),
    max_rating: Optional[float] = Query(default=None, ge=0, le=10),
    sort: str = "title_asc",
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    return get_movies(
        db, search, genre, year, min_rating, max_rating,
        sort, skip, limit
    )


@router.get("/movies/{movie_id}", response_model=MovieResponse)
def movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post("/movies", response_model=MovieResponse, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return create_or_update_movie(db, movie)


@router.get("/genres")
def genres(db: Session = Depends(get_db)):
    rows = (
        db.query(Movie.genre)
        .filter(Movie.genre.isnot(None))
        .distinct()
        .all()
    )
    values = set()
    for row in rows:
        for item in (row[0] or "").split(","):
            item = item.strip()
            if item:
                values.add(item)
    return sorted(values)


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    total = count_movies(db)
    average = db.query(func.avg(Movie.rating)).scalar()
    latest_year = db.query(func.max(Movie.year)).scalar()
    return {
        "total_movies": total,
        "average_rating": round(float(average), 2) if average else None,
        "latest_year": latest_year,
    }


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    movies = db.query(Movie).order_by(Movie.title.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "title", "year", "genre", "rating", "director",
        "cast", "runtime", "description", "poster_url", "source_url"
    ])

    for movie in movies:
        writer.writerow([
            movie.id, movie.title, movie.year, movie.genre, movie.rating,
            movie.director, movie.cast, movie.runtime, movie.description,
            movie.poster_url, movie.source_url
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=movies.csv"},
    )
