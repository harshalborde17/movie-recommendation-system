## can not insert duplicate movie with the same source_url, so we will update the existing one if it exists...

from sqlalchemy import or_
from sqlalchemy.orm import Session
from .models import Movie
from .schemas import MovieCreate


def get_movies(
    db: Session,
    search=None,
    genre=None,
    year=None,
    min_rating=None,
    max_rating=None,
    sort="title_asc",
    skip=0,
    limit=20,
):
    query = db.query(Movie)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Movie.title.ilike(term),
                Movie.director.ilike(term),
                Movie.cast.ilike(term),
                Movie.genre.ilike(term),
            )
        )

    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre.strip()}%"))

    if year:
        query = query.filter(Movie.year == year)

    if min_rating is not None:
        query = query.filter(Movie.rating >= min_rating)

    if max_rating is not None:
        query = query.filter(Movie.rating <= max_rating)

    sort_map = {
        "title_asc": Movie.title.asc(),
        "title_desc": Movie.title.desc(),
        "rating_desc": Movie.rating.desc(),
        "rating_asc": Movie.rating.asc(),
        "year_desc": Movie.year.desc(),
        "year_asc": Movie.year.asc(),
    }
    query = query.order_by(sort_map.get(sort, Movie.title.asc()))

    return query.offset(skip).limit(limit).all()


def count_movies(db: Session):
    return db.query(Movie).count()


def get_movie(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.id == movie_id).first()


def create_or_update_movie(db: Session, movie_data: MovieCreate):
    existing = None
    if movie_data.source_url:
        existing = db.query(Movie).filter(
            Movie.source_url == movie_data.source_url
        ).first()

    if existing:
        for key, value in movie_data.model_dump().items():
            if value is not None:
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    movie = Movie(**movie_data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie
