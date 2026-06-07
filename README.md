# Smart Resume Python

Python/FastAPI + React reimplementation of Smart Resume.

## Development Ports

- Frontend: http://localhost:3789
- Backend: http://localhost:8000
- API: http://localhost:3789/api through Vite proxy

## Default Login

- Username: `admin`
- Password: `admin123`

Change the password after first login in a later settings implementation.

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3789
```

## One-command Development Start

```bash
./start.sh
```
