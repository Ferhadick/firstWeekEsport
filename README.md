# Esports Tournament API

A FastAPI backend for managing esports tournaments, teams, players, and matches.

---

# Stack

- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Pydantic v2
- Uvicorn
- pytest

---

# Project Structure

```
esports-tournament-api/
├── app/
│   ├── __init__.py
│   ├── main.py                       # App entry point, exception handlers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Environment config
│   │   └── database.py               # Engine, session factory
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── match.py
│   ├── schemas/                      # Pydantic DTOs
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── match.py
│   │   └── pagination.py
│   ├── repositories/                 # Data access layer
│   │   ├── tournament_repository.py
│   │   ├── team_repository.py
│   │   ├── player_repository.py
│   │   └── match_repository.py
│   ├── services/                     # Business logic
│   │   ├── tournament_service.py
│   │   ├── team_service.py
│   │   ├── player_service.py
│   │   └── match_service.py
│   ├── controllers/                  # FastAPI routers
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── match.py
│   ├── exceptions/                   # Custom exception classes
│   │   └── __init__.py
│   └── dependencies/                 # FastAPI dependencies
│       └── database.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── services/
│       ├── test_tournament_service.py
│       ├── test_team_service.py
│       ├── test_player_service.py
│       └── test_match_service.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .env.example
└── .gitignore
```

---

# Flow

Every request follows the same path:

```
Client
  ↓
Controller (receives request, returns response)
  ↓
Service  (validates business rules)
  ↓
Repository (runs SQL queries)
  ↓
Database
```

Data flows back the same way in reverse, with ORM objects converted to Pydantic DTOs before reaching the client.

---

# API Endpoints

All entities have the same CRUD endpoints.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/{entity}/` | Create |
| GET | `/{entity}/` | List (paginated, sortable) |
| GET | `/{entity}/{id}` | Get by ID |
| PUT | `/{entity}/{id}` | Update |
| DELETE | `/{entity}/{id}` | Delete |

Entities: `tournaments`, `teams`, `players`, `matches`.

### Pagination & Sorting

List endpoints support pagination and sorting via query parameters.

```
GET /teams?page=1&size=10&sort_by=name&order=asc
```

Defaults are page=1, size=10, order=asc. Max size is 100. Passing an invalid sort column returns a 400 error.

---

# Relationships

- A Tournament has many Matches
- A Team has many Players
- A Team can appear in many Matches (as team1 or team2)
- A Match belongs to one Tournament and involves two Teams

---

# Error Handling

Errors come back in a consistent format:

```json
{
  "success": false,
  "message": "What went wrong",
  "details": null
}
```

HTTP status codes used:
- 400 – validation errors, invalid sort columns
- 404 – resource not found
- 409 – duplicate entry (team tag, player nickname)
- 422 – request body validation
- 500 – unexpected errors

---

# Running the Project

1. Copy `.env.example` to `.env` and set your PostgreSQL connection string.
2. Create a virtual environment: `uv venv`
3. Activate it (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` otherwise).
4. Install deps: `uv sync`
5. Start the server: `uvicorn app.main:app --reload`

The API will be at `http://localhost:8000`. OpenAPI docs at `/docs`.

### Tests

```bash
pytest tests/
```

Tests mock the repository layer so they don't need a real database.

---

# License

Educational project.
