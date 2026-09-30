# 🎬 Movie Scraper & Search Platform

A Python-based 
**Movie Scraper and Search Platform** that demonstrates web scraping, data cleaning, SQLite database management, REST API development with FastAPI, and an interactive frontend.

The application allows users to **search, filter, sort, paginate, and export movie data** through a web interface and REST APIs.

---

## 🚀 Features

* 🌐 Web scraping using **Requests + BeautifulSoup**
* 🧹 Data cleaning and normalization
* 🗃️ SQLite database storage
* ⚡ FastAPI REST APIs
* 🔎 Movie search
* 🎭 Genre filtering
* 📅 Year filtering
* ⭐ Rating filtering
* ↕️ Sorting
* 📄 Pagination
* 📊 Movie statistics
* 📥 CSV export
* 🌐 HTML/CSS/JavaScript frontend
* 🌱 Seed data for immediate application startup

---

## 🏗️ Architecture

Website
   ↓
Web Scraper
   ↓
Data Cleaning & Normalization
   ↓
SQLite Database
   ↓
FastAPI REST API
   ↓
Frontend


## 📁 Project Structure


movie_scraper/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes.py
│   ├── scraper.py
│   └── seed.py
│
├── data/
│   └── sample_movies.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env.example
├── .gitignore
├── MUST_READ.txt
├── README.md
└── requirements.txt






# 🛠️ Tech Stack

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Core programming language  |
| FastAPI       | REST API backend           |
| Uvicorn       | Application server         |
| Requests      | HTTP requests for scraping |
| BeautifulSoup | HTML parsing               |
| SQLite        | Database                   |
| SQLAlchemy    | Database ORM               |
| HTML          | Frontend structure         |
| CSS           | Frontend styling           |
| JavaScript    | Frontend functionality     |

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/harshalborde17/movie-recommendation-system.git
cd movie-recommendation-system
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🌱 Seed the Database

Run:

```bash
python -m app.seed
```

This creates the SQLite database and inserts the available sample movie data.

---

# ▶️ Start the Application

Run:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

### 🌐 Frontend

```text
http://127.0.0.1:8000/
```

### 📚 API Documentation

```text
http://127.0.0.1:8000/docs
```

### ❤️ Health Check

```text
http://127.0.0.1:8000/health
```

---

# 🕷️ Run the Movie Scraper

Run the included scraper:

```bash
python -m app.scraper
```

The scraper extracts movie information from the configured source and stores the processed data in the project database/data files.

You can also provide another permitted URL:

```bash
python -m app.scraper --url "https://example.com/movie-list"
```

### ⚠️ Responsible Scraping

Only scrape websites where the activity is permitted by their:

* Terms of Service
* robots.txt rules
* Data licenses
* Applicable laws

Do not use this project to bypass anti-bot systems, authentication, rate limits, or access restrictions.

---

# 🔌 API Endpoints

### Get Movies

```http
GET /api/movies
```

### Search Movies

```http
GET /api/movies?search=batman
```

### Filter by Genre

```http
GET /api/movies?genre=Action
```

### Filter by Year

```http
GET /api/movies?year=2024
```

### Filter by Rating

```http
GET /api/movies?min_rating=8
```

### Sort by Rating

```http
GET /api/movies?sort=rating_desc
```

### Get Movie by ID

```http
GET /api/movies/1
```

### Get Genres

```http
GET /api/genres
```

### Get Statistics

```http
GET /api/stats
```

### Export Movies as CSV

```
GET /api/export/csv

```



# 🔄 How It Works

The application follows this workflow:


1. Requests
      ↓
2. Downloads HTML
      ↓
3. BeautifulSoup
      ↓
4. Parses movie information
      ↓
5. Cleans & normalizes data
      ↓
6. SQLite database
      ↓
7. FastAPI REST API
      ↓
8. JavaScript fetch()
      ↓
9. Interactive frontend



# 🧠 Project Talking Points

This project demonstrates several practical software-development concepts:

1. **Web Scraping**
   Requests downloads web content and BeautifulSoup parses the HTML.

2. **Data Processing**
   Scraped fields are cleaned and normalized into a consistent movie schema.

3. **Database Management**
   Structured movie records are stored in SQLite.

4. **REST API Development**
   FastAPI provides endpoints for searching, filtering, sorting, pagination, statistics, and exporting data.

5. **Frontend Integration**
   JavaScript communicates with the FastAPI backend using `fetch()`.

6. **Duplicate Handling**
   Duplicate movie records can be prevented using unique source URLs where applicable.


# 📸 Screenshots 

![search UI](![<img width="1920" height="1080" alt="search img" src="https://github.com/user-attachments/assets/aecfade7-ea13-4ca1-bf13-019cafbda9a9" />
]()
)

![API docs](![<img width="1920" height="1080" alt="API docs img" src="https://github.com/user-attachments/assets/278571ce-791c-4568-a1ab-918b95056493" />
]()
)




# 🔮 Future Improvements

* 🐘 PostgreSQL database
* 🐳 Docker support
* ⏰ Scheduled scraping
* ⚙️ Celery/RQ background jobs
* 🔐 Authentication and authorization
* ⚡ Redis caching
* ⚛️ React frontend
* 🧪 Automated testing with pytest
* 🌐 Multiple permitted data sources
* ☁️ Cloud deployment
* 📊 Advanced movie analytics
* 🤖 AI-powered movie recommendations



# 🎯 Learning Outcomes

Through this project, I explored:

* Python application development
* REST API development
* FastAPI
* Web scraping
* HTML parsing
* Data cleaning
* Database operations
* Frontend/backend integration
* API testing
* Git and GitHub workflow


# 👨‍💻 Author

**Harshal Borde**

GitHub:
https://github.com/harshalborde17


⭐ If you find this project useful, feel free to explore the repository and give it a star.
