# Demo Test Backend

This backend powers the hidden `/demo-test` page.

## Endpoints

- `POST /api/demo-test/demo1/run`
- `POST /api/demo-test/demo2/run`
- `POST /api/demo-test/demo3/run`
- `POST /api/demo-test/demo4/run`

Each endpoint:
- Accepts JSON or multipart form data (file upload supported).
- Runs a configured Python command for that demo.
- Passes request payload to the command via stdin as JSON.
- Sends output email to the `email` field in payload (if SMTP is configured for that demo).

## Expected runner behavior

Your Python script should:
1. Read JSON from stdin.
2. Execute your flow.
3. Print JSON output to stdout.

If stdout is not valid JSON, raw text is returned.

## Setup

1. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

2. Create env file:

```bash
copy backend/.env.example backend/.env
```

3. Fill your per-demo commands/keys/credentials in `backend/.env`.

4. Start API server:

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

## Frontend/API wiring

The page at `/demo-test` calls these relative endpoints:
- `/api/demo-test/demo1/run`
- `/api/demo-test/demo2/run`
- `/api/demo-test/demo3/run`
- `/api/demo-test/demo4/run`

In production, point your reverse proxy to this FastAPI service for `/api/*` routes.
