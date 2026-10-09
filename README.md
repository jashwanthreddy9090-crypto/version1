# Campus 360 — Clean Flask Edition

Campus 360 is a Flask web application for campus complaint submission, complaint tracking, administrator management, and emergency phone access. The login screen and signed-in workspaces are separate pages.

## Features
- Separate login page and protected dashboard after successful sign-in
- Student complaint submission and personal complaint tracking
- Administrator dashboard, student and worker account creation, worker assignment and status updates
- Excel login history download
- Basic campus-help assistant (rule-based; it is not a live AI service)
- Responsive red, cream and white interface
- SQLite database and a `/health` endpoint for deployment checks

## Requirements
Python 3.10 or newer is recommended.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open ` https://jashwanthreddy9090-crypto.github.io/version1/`.

## Initial administrator

- Email: `admin@campus.360`
- Password: `Campus360@Admin2026`

Change these credentials for real deployment by setting environment variables:
- `SECRET_KEY`: a long, random secret
- `ADMIN_EMAIL`: administrator email (must end in `@campus.360`)
- `ADMIN_PASSWORD`: strong administrator password
- `DATABASE_PATH`: optional persistent path for the SQLite database

Student accounts are created from the administrator dashboard. Passwords are stored as hashes.

## Deployment note

GitHub Pages cannot run Flask/Python. Push this repository to GitHub and deploy it to a Python web host that supports Flask/Gunicorn. The included `Procfile` starts Gunicorn. Configure the environment variables above and attach persistent storage for `campuscare.db` if your host's filesystem is ephemeral. Without persistent storage, database records may disappear when the instance restarts or redeploys. The login Excel file is also written to the application directory, so use persistent storage if you need durable login exports.

## Important notes
- The emergency button opens the device's phone dialer for 112; it does not dispatch emergency services automatically.
- The built-in assistant is rule-based and does not connect to an external AI API.
- Administrators can create worker accounts from the admin dashboard. Workers sign in with their `@campus.360` email and password, see only complaints assigned to their worker profile, and can mark assigned work In Progress or Resolved. Existing older databases are upgraded to link worker profiles to login accounts.
- Demo worker phone numbers in `app.py` are placeholders and must be replaced with authorized, verified contacts before real use.
