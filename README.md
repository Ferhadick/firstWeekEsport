# Esports Tournament API

A FastAPI backend for managing esports tournaments, teams, players, and matches with JWT-based authentication and role-based access control.

---

## Stack

- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Pydantic v2
- Uvicorn
- bcrypt / python-jose
- pytest

---

## Project Structure

```
esporttournamentapi/
├── app/
│   ├── __init__.py
│   ├── main.py                       # App entry point, exception handlers, router registration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Environment config readers
│   │   ├── database.py               # Engine, session factory, Base
│   │   └── security.py              # bcrypt hashing, JWT create/decode
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── match.py
│   ├── schemas/                      # Pydantic request/response DTOs
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── match.py
│   │   └── pagination.py
│   ├── repositories/                 # Data access layer
│   │   ├── user_repository.py
│   │   ├── tournament_repository.py
│   │   ├── team_repository.py
│   │   ├── player_repository.py
│   │   └── match_repository.py
│   ├── services/                     # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── tournament_service.py
│   │   ├── team_service.py
│   │   ├── player_service.py
│   │   └── match_service.py
│   ├── controllers/                  # FastAPI routers
│   │   ├── auth_controller.py
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── match.py
│   ├── dependencies/                 # FastAPI dependencies
│   │   ├── database.py               # get_db session yield
│   │   └── auth.py                   # get_token, get_current_user, require_role
│   └── exceptions/
│       └── __init__.py               # Custom exception classes
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── services/
│       ├── test_tournament_service.py
│       ├── test_team_service.py
│       ├── test_player_service.py
│       └── test_match_service.py
├── alembic/                          # DB migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 4b03e79e41a0_initial.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .env.example
└── .gitignore
```

---

## Flow

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

## Authentication

The API uses JWT tokens sent either as an `Authorization: Bearer <token>` header or as an httpOnly cookie (`access_token`).

### Roles

| Role | Permissions |
|------|-------------|
| `USER` | Read resources, create/update/delete own data |
| `ADMIN` | Everything a USER can do, plus create/update/delete any resource and promote users |

### Auth Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | None | Create account, returns JWT + sets cookie. Include `X-Admin-Secret: <secret>` to create an ADMIN. |
| POST | `/auth/login` | None | Authenticate, returns JWT + sets cookie. |
| GET | `/auth/me` | Any | Return profile of the currently authenticated user. |
| POST | `/auth/refresh` | Any | Issue a new JWT from a still-valid existing token. |
| PUT | `/auth/users/{user_id}/role` | ADMIN | Change another user's role (USER or ADMIN). |

### Auth Flow Example

```
1. POST /auth/register  {"username":"admin1","email":"a@b.com","password":"test1234"}
   Header: X-Admin-Secret: change-me
   → Creates ADMIN user, returns JWT, sets cookie

2. GET /auth/me         (cookie auto-sent)
   → Returns { id, username, email, role: "ADMIN", created_at }

3. POST /tournaments    (cookie auto-sent)
   Body: {"name":"...","game":"...",...}
   → Creates tournament (ADMIN-only action)

4. POST /auth/refresh   (cookie auto-sent)
   → Returns new JWT, renews cookie
```

### Resource Endpoint Access

| Method | Auth Required | Allowed Roles |
|--------|---------------|---------------|
| GET (list / get-by-id) | Yes | USER, ADMIN |
| POST (create) | Yes | ADMIN |
| PUT (update) | Yes | ADMIN |
| DELETE | Yes | ADMIN |

### Pagination & Sorting

List endpoints support pagination and sorting via query parameters.

```
GET /teams?page=1&size=10&sort_by=name&order=asc
```

Defaults are page=1, size=10, order=asc. Max size is 100. Passing an invalid sort column returns a 400 error.

---

## Relationships

- A User has an account with role-based access
- A Tournament has many Matches
- A Team has many Players
- A Team can appear in many Matches (as team1 or team2)
- A Match belongs to one Tournament and involves two Teams

---

## Error Handling

Errors come back in a consistent format:

```json
{
  "success": false,
  "message": "What went wrong",
  "details": null
}
```

HTTP status codes used:
- 400 – business validation errors, invalid sort columns
- 401 – missing or invalid authentication token
- 403 – authenticated but insufficient permissions
- 404 – resource not found
- 409 – duplicate entry (username, email, team tag)
- 422 – request body validation failure
- 500 – unexpected errors

---

## Running the Project

1. Copy `.env.example` to `.env` and set your PostgreSQL connection string.  
   The `ADMIN_SECRET` value lets you create ADMIN users at registration via the `X-Admin-Secret` header.
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

## License

Educational project.
