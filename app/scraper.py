## this is the actual web scraper component 

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .crud import create_or_update_movie
from .database import Base, SessionLocal, engine
from .schemas import MovieCreate

DEFAULT_URL = "https://en.wikipedia.org/wiki/List_of_American_films_of_2024"
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "scraped_movies.json"


def clean(value):
    if value is None:
        return None
    return re.sub(r"\s+", " ", value).strip()


def first_link_text(cell):
    link = cell.find("a")
    return clean(link.get_text(" ", strip=True)) if link else clean(cell.get_text(" ", strip=True))


def find_column(headers, keywords):
    for index, header in enumerate(headers):
        normalized = header.lower()
        if any(keyword in normalized for keyword in keywords):
            return index
    return None


def scrape_wikipedia_movie_table(url=DEFAULT_URL):
    headers = {
        "User-Agent": "MovieScraperInternship/1.0 (educational project)"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    movies = []

    for table in soup.select("table.wikitable"):
        header_row = table.find("tr")
        if not header_row:
            continue

        header_cells = header_row.find_all(["th", "td"])
        headers_text = [clean(cell.get_text(" ", strip=True)) or "" for cell in header_cells]

        title_idx = find_column(headers_text, ["title", "film"])
        if title_idx is None:
            continue

        director_idx = find_column(headers_text, ["director"])
        cast_idx = find_column(headers_text, ["cast", "starring"])
        genre_idx = find_column(headers_text, ["genre"])
        date_idx = find_column(headers_text, ["release date", "release"])

        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if not cells or len(cells) <= title_idx:
                continue

            title = first_link_text(cells[title_idx])
            if not title or title.lower() in {"title", "film"}:
                continue

            def get(idx):
                return clean(cells[idx].get_text(" ", strip=True)) if idx is not None and idx < len(cells) else None

            release = get(date_idx)
            year = 2024
            if release:
                match = re.search(r"(20\d{2})", release)
                if match:
                    year = int(match.group(1))

            movie = {
                "title": title,
                "year": year,
                "genre": get(genre_idx),
                "rating": None,
                "director": get(director_idx),
                "cast": get(cast_idx),
                "runtime": None,
                "description": "Scraped from a public Wikipedia film-list table.",
                "poster_url": None,
                "source_url": url,
            }
            movies.append(movie)

    # Deduplicate by title.
    unique = {}
    for movie in movies:
        unique[movie["title"].lower()] = movie

    return list(unique.values())


def save_and_import(movies):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(movies, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for item in movies:
            create_or_update_movie(db, MovieCreate(**item))
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Movie web scraper")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    movies = scrape_wikipedia_movie_table(args.url)
    save_and_import(movies)
    print(f"Scraped {len(movies)} movies.")
    print(f"Saved JSON: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
