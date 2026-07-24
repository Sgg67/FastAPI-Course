#  Courts and Play USA

A full-stack web app for finding pickleball courts and organizing open-play game sessions with other players — built with FastAPI, SQLAlchemy, and Jinja2.

**Courts and Play Web App:** [courts-and-play-usa.onrender.com](https://courts-and-play-usa.onrender.com)
---

## What it does

Courts and Play USA lets pickleball players:

- 🔍 **Search for courts** by city or name, with details like facility type, number of courts, address, and price to play
- 🗓️ **Host open-play sessions** at a court, setting a date/time and player capacity
- 🤝 **Join sessions** hosted by other players in real time, with live "spots remaining" tracking
- 👤 **Create an account, log in, and manage a profile** (change password, update phone number) with secure, cookie-based authentication

## Tech Stack

| Layer | Tech |
|---|---|
| **Backend** | Python, FastAPI |
| **Database / ORM** | SQLAlchemy, SQLite |
| **Templating** | Jinja2 |
| **Frontend** | Bootstrap, vanilla JavaScript (Fetch API) |
| **Auth** | JWT (python-jose), OAuth2, Passlib/bcrypt |
| **Testing** | Pytest, FastAPI TestClient |
| **Config** | python-dotenv |


## Technical Concepts Covered

This project was a way to practice building a complete backend-driven web app from the ground up. Highlights:

### Relational Database Design
- Three core models — `Users`, `Courts`, and `Session` — connected through **one-to-many** (a court has many sessions, a user hosts many sessions) and **many-to-many** relationships (players ↔ sessions) using a proper SQLAlchemy **association table** (`user_sessions`) with `ondelete="CASCADE"` foreign keys.

### Authentication & Authorization
- Stateless **JWT-based auth** issued via an OAuth2 password flow (`/auth/token`) and verified on every protected route with FastAPI's `Depends`.
- Passwords are never stored in plaintext — hashed and verified with **bcrypt** via Passlib.
- Tokens are read from either the `Authorization` header **or** an HTTP-only cookie, so the same auth logic protects both the JSON API and the server-rendered pages, with unauthenticated users automatically redirected to login.

### Dependency Injection
- FastAPI's `Depends` system is used throughout for database sessions (`get_db`) and the current user (`get_current_user`), keeping route handlers thin and testable.

### RESTful API Design
- Resource-oriented routes (`GET /courts/{id}`, `POST /courts/add-court`, `POST /sessions/join/{id}`, etc.) organized into separate **`APIRouter`** modules for auth, courts, users, and sessions, each mounted onto the main app with its own prefix and tags — visible and testable in the auto-generated **Swagger UI** (`/docs`).

### Data Validation
- **Pydantic models** enforce request validation (e.g. minimum-length names, positive court counts) before data ever touches the database, with example payloads wired into the Swagger schema.

### Server-Side Rendering
- Jinja2 templates with a shared `layout.html` base (navbar, static asset includes) and page-specific templates that loop over query results (court listings, session cards) and conditionally render UI based on session state (open / full / already joined).

### Automated Testing
- A Pytest suite using FastAPI's `TestClient`, an **in-memory SQLite database** isolated from production data, and **dependency overrides** (`app.dependency_overrides`) to swap in test auth/DB without touching route code — plus fixtures for reusable test data (`test_user`, `test_court`).

### App Configuration & Middleware
- Environment-based secrets (`SECRET_KEY`, `ALGORITHM`) loaded via `python-dotenv`, **CORS middleware**, and static file mounting for CSS/JS assets.

---

## Project Structure

```
├── main.py                # App entrypoint, middleware, router registration
├── models/
│   └── models.py           # SQLAlchemy models: Users, Courts, Session
├── routers/
│   ├── auth.py              # JWT auth, login/register endpoints
│   ├── courts.py            # Court search/CRUD + page routes
│   ├── users.py              # Profile management endpoints
│   └── sessions.py            # Open-play session create/join logic
├── templates/               # Jinja2 HTML templates
├── static/                   # CSS/JS assets
└── test/
    ├── test_auth.py           # Auth unit tests
    ├── test_courts.py          # Court endpoint tests
    └── utils.py                 # Test fixtures & DB overrides
```

---

## Environment Variables

Create a `.env` file in the project root with:

```dotenv
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

- **`SECRET_KEY`** — used to sign and verify JWT access tokens. Should be a long, random string (e.g. generate one with `openssl rand -hex 32`) and kept out of version control.
- **`ALGORITHM`** — the signing algorithm passed to `python-jose` when encoding/decoding tokens (typically `HS256`).

## Running Locally

```bash
git clone https://github.com/Sgg67/courts-and-play-usa.git
cd courts-and-play-usa
pip install -r requirements.txt
uvicorn main:app --reload
```

Then visit `http://localhost:8000` in your browser.

---

