# Cloud Task Tracker — Assignment 8

A small Flask web application for demonstrating cloud deployment, functional testing, health checks, logging, and basic security/cost controls.

## Features
- Responsive task list UI
- `GET /health` health endpoint
- `GET /api/tasks` list tasks
- `POST /api/tasks` create a task (validates empty/long titles)
- `PATCH /api/tasks/<id>` mark a task done/open
- Application logs for page requests, task operations, and rejected requests

## Important demo limitation
Tasks are stored in memory, not a database. They reset whenever the service restarts or redeploys. Do not use this version for important or private data. A persistent database is outside the minimum assignment scope.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. Test health at http://127.0.0.1:5000/health.

## Deploy on Render (student must perform deployment)
1. Create a GitHub repository and upload the contents of this folder.
2. Sign in to Render and choose **New + → Web Service**.
3. Connect the repository; use Python runtime, build command `pip install -r requirements.txt`, start command `gunicorn app:app`.
4. Confirm the health check path is `/health`; choose a free/approved plan if currently available and permitted by your instructor.
5. Deploy and copy the actual public URL into the report. Availability, free-tier terms, and pricing can change; confirm before deployment.
6. In Render's service dashboard, open **Logs** and confirm page/API requests appear.
7. Test `https://YOUR-APP.onrender.com/health` and `/api/tasks`.
8. Optional alert: configure an approved uptime monitor to check `/health` every 5 minutes and notify your email after 2 consecutive failures. Do not add secrets to the repository.

## Test checklist
See `../test-cases.csv`. Use the deployed URL after deployment. Capture genuine screenshots of the app, health endpoint, logs, and alert configuration if used.

## Security
- No credentials, API keys, or secrets are required by this application.
- Use platform account MFA where available; grant access only to the project owner/instructor as needed.
- Do not expose admin consoles or use secrets in source code.
- The app is a teaching demo and does not implement user accounts, authorization, CSRF protection, or persistent storage. Do not use it for sensitive data.
