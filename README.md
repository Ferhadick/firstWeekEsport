# Esports Tournament API

A clean and scalable FastAPI backend foundation for an **Esports Tournament Management System**. This project is designed to manage tournaments, teams, players, and matches while following a modular project architecture.

---

# Technologies

- Python 3.13+
- FastAPI
- SQLAlchemy 2.0 ORM
- PostgreSQL
- Uvicorn
- uv (package and dependency manager)

---

# Project Structure

```text
esports-tournament-api/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── match.py
│   │   └── __init__.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── pyproject.toml
├── uv.lock
├── README.md
├── .env.example
└── .gitignore
```

---

# Architecture

The project follows a simple layered architecture.

- **app/models** – SQLAlchemy ORM entity models
- **app/core** – Database configuration and application settings
- **app/main.py** – FastAPI application entry point

This structure keeps the project organized and scalable for future development.

## Layered Architecture Overview

```text
HTTP Request
   ↓
Controller (FastAPI router)
   ↓
Service (business logic)
   ↓
Repository (database access)
   ↓
SQLAlchemy Model
   ↓
Database
```

**Why use DTOs (Pydantic schemas)?**
- **Decoupling:** DTOs separate the public API contract from internal ORM models, protecting the API from accidental exposure of database implementation details.
- **Validation & Documentation:** Pydantic schemas provide request validation and automatically generate OpenAPI documentation, ensuring clients receive well‑defined data structures.
- **Versioning & Flexibility:** Changes to the database schema (e.g., adding columns) do not automatically affect the API response; DTOs can evolve independently.
- **Security:** Sensitive fields (e.g., internal IDs, timestamps) can be omitted from responses, reducing surface area for leaks.
- **Consistency:** All responses are consistently shaped, making client integration predictable.

The codebase now follows this exact flow for each entity, with one example endpoint (e.g., `POST /teams`) demonstrating the layered approach.

---

# Entity Relationship Diagram

```text
Tournament
-----------
id (PK)
name
game
location
prize_pool
start_date
end_date
status

        1
        │
        │
        *
Match
-----------
id (PK)
tournament_id (FK)
team1_id (FK)
team2_id (FK)
winner_id (FK)
scheduled_at
status
score_team1
score_team2


Team
-----------
id (PK)
name
tag
country
founded_year
logo_url

        1
        │
        │
        *
Player
-----------
id (PK)
nickname
real_name
country
age
role
team_id (FK)
```

### Relationships

- One Tournament has many Matches.
- One Team has many Players.
- One Team can participate in many Matches.
- Each Match belongs to one Tournament.
- Each Player belongs to one Team.

---

# Entity Description

## Tournament

Represents an esports tournament. Stores tournament information including game title, location, prize pool, schedule, and current status.

## Team

Represents an esports team. Stores team information such as name, tag, country, founding year, and logo.

## Player

Represents an individual player belonging to a specific team.

## Match

Represents a scheduled match between two teams inside a tournament, including scores, winner, and match status.

---

# Running the Project

## 1. Create a virtual environment

```bash
uv venv
```

## 2. Activate the virtual environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
uv sync
```

## 4. Configure environment variables

Copy:

```text
.env.example
```

to

```text
.env
```

and configure your PostgreSQL connection string.

## 5. Start the server

```bash
uvicorn app.main:app --reload
```

## 6. Open the API

```
GET /
```

Expected response:

```json
{
  "message": "Esports Tournament API"
}
```

---


# License

This project was created for educational purposes.