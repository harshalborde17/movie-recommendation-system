# Movie Scraper & Search Platform

An Python project that demonstrates:

- Web scraping with Requests + BeautifulSoup
- Data cleaning and normalization
- SQLite database storage
- FastAPI REST APIs
- Search, filtering, sorting and pagination
- HTML/CSS/JavaScript frontend
- CSV export
- Seed data so the application works immediately

## Architecture

Website -> Scraper -> Clean data -> SQLite -> FastAPI -> Frontend

## Project structure

movie_scraper_internship/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes.py
│   └── scraper.py
├── data/
│   └── sample_movies.json
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env.example
├── .gitignore
└── requirements.txt

## 1. Windows setup

Open PowerShell in this folder:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scripts\Activate.ps1
```

## 2. Seed the database

```powershell
python -m app.seed
```

This creates `movies.db` and inserts sample movies.

## 3. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- Frontend: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 4. Run the scraper

The included scraper targets a public Wikipedia film-list page and extracts movie-table fields where available.

```powershell
python -m app.scraper
```

Or specify another permitted URL:

```powershell
python -m app.scraper --url "https://example.com/movie-list"
```

The scraper saves `data/scraped_movies.json` and upserts records into SQLite.

Only scrape websites whose terms, robots rules, licenses, and applicable law permit the activity. Do not use this project to bypass anti-bot controls or access restrictions.

## 5. API examples

```text
GET /api/movies
GET /api/movies?search=batman
GET /api/movies?genre=Action
GET /api/movies?year=2024
GET /api/movies?min_rating=8
GET /api/movies?sort=rating_desc
GET /api/movies/1
GET /api/genres
GET /api/stats
GET /api/export/csv
```

## PROJECT talking points

1. Requests downloads HTML.
2. BeautifulSoup parses the DOM.
3. The scraper normalizes fields into a common movie schema.
4. SQLite stores structured records.
5. FastAPI exposes the database through REST endpoints.
6. JavaScript consumes the API with fetch().
7. The frontend provides search, filters, sorting and pagination.
8. Duplicate movies are prevented using a unique source URL where possible.

## improvements

- PostgreSQL
- Docker
- Scheduled scraping
- Celery/RQ background jobs
- Authentication
- Redis caching
- React frontend
- Automated tests with pytest
- Multiple permitted data sources
