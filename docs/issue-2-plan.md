# Issue #2: PostgreSQL connection and base models

## Delivered
- SQLAlchemy 2.0 engine/session setup via `DATABASE_URL` in `backend/database.py`.
- Core ORM models added: Farmer, Query, Crop with UUID primary keys and required fields.
- Pydantic schemas added for each model under `backend/schemas/`.
- Startup hook creates tables with `Base.metadata.create_all(bind=engine)`.
- `/health` now includes database connection status by executing `SELECT 1`.
