# rental-services-python

FastAPI project with CRUD endpoints for services, technicians, agendas (visits) and users using MySQL and SQLAlchemy.

## Quickstart (local)

1. Create a Python virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the MySQL database and user (example SQL in `create_db.sql`) or run these commands in MySQL client:
```sql
CREATE DATABASE rental_services CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rental_user'@'localhost' IDENTIFIED BY 'rental_pass';
GRANT ALL PRIVILEGES ON rental_services.* TO 'rental_user'@'localhost';
FLUSH PRIVILEGES;
```

4. Copy `.env.example` to `.env` and update credentials.
5. Run the app:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs
