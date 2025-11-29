# Snowflake Query Runner

This repository provides example Python scripts for transferring data
between Snowflake and SQL Server.

* `run_snowflake_query.py` demonstrates how to execute a Snowflake query
  from SQL Server using `OPENQUERY`.
* `snowflake_to_sqlserver.py` connects directly to Snowflake, exports the
  results to CSV, and loads them into a SQL Server table.

## Requirements
Install the dependencies with pip:
```bash
pip install pandas pyodbc snowflake-connector-python
```

## `run_snowflake_query.py`
Edit `SQL_SERVER_CONNECTION_STRING` and run:
```bash
python run_snowflake_query.py
```
The script creates a temporary table in SQL Server with data pulled from
Snowflake and prints a preview.

## `snowflake_to_sqlserver.py`
1. Update the Snowflake credentials (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`,
   etc.) and the SQL Server connection string.
2. Run:
```bash
python snowflake_to_sqlserver.py
```
This will:
- Query Snowflake for call center data after 2024-01-01.
- Save the results to a CSV file in
  `C:\Users\mp311723\OneDrive - Vistra Corp\SQL SSMS\DGL_Repository`.
- Create the table `Skywalker.dbo.MP_SnowflakeData` and insert the data
  so you can query it from SQL Server.
# Skywalker

This repository contains a minimal FastAPI backend and a PostgreSQL database
that can be orchestrated using Docker Compose.

## Getting started

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Adjust any credentials if necessary. When running with Docker Compose the
   database hostname must remain `db`, matching the service name declared in
   `docker-compose.yml` so the backend container can reach it.

3. Build and start the services:

   ```bash
   docker compose up --build
   ```

The backend will be available at <http://localhost:8000>.
# Skywalker Energy Intelligence Platform

This repository provides a full-stack reference implementation for aggregating and visualising competitive Texas retail electricity plans. It includes a FastAPI backend with automated scraping jobs and a Material-UI React dashboard for analysts.

## Features

- **FastAPI backend** with async SQLAlchemy models for providers and plans, REST endpoints (`/providers`, `/plans`, `/plans/{id}`, `/scrape`, `/health`).
- **Scraper modules** for TXU, Reliant, Gexa, and Direct Energy using `requests` + `BeautifulSoup` (and a Selenium-ready architecture) to normalise plan metadata and pricing.
- **APScheduler integration** for recurring scrapes controlled via environment variables, plus API-key protection for manual triggers.
- **Database migrations and seeds** targeting PostgreSQL with optional SQLite support for development/tests.
- **React + TypeScript frontend** featuring a responsive dashboard with filters, comparison drawer, TXU benchmark insights, detail modal, and Chart.js visualisations.
- **Automated tests** covering scrapers and API flows.
- **Makefile & Docker Compose** for streamlined local development.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional but recommended for PostgreSQL)

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy connection string (PostgreSQL in production, SQLite allowed locally). When using Docker Compose, set the host to `db`. |
| `API_KEY` | API key required for `POST /scrape`. |
| `SCRAPE_PROVIDERS` | Comma-separated list of provider slugs to run during scheduled jobs. |
| `SCRAPE_INTERVAL_MINUTES` | Interval for recurring scrapes. |
| `SCHEDULER_ENABLED` | Toggle background scheduler. |

### Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Apply migrations and seed data:

```bash
psql "$DATABASE_URL" -f backend/migrations/0001_init.sql
psql "$DATABASE_URL" -f backend/migrations/seed.sql
```

Run the scraper suite manually:

```bash
http POST :8000/scrape X-API-Key:$API_KEY
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to open the dashboard. Configure the API base URL via `VITE_API_BASE` in `.env` or the command line if your backend runs elsewhere.

### Docker Compose

A convenience stack is provided via `docker-compose.yml`:

```bash
docker-compose up --build
```

This launches PostgreSQL, the FastAPI backend, and the Vite dev server with appropriate environment configuration.

When using Docker Compose, ensure the database host portion of `DATABASE_URL` in your `.env` file points to `db` so the backend container can reach the PostgreSQL service (e.g. `postgresql+asyncpg://postgres:postgres@db:5432/energy`).

### Makefile Commands

```bash
make backend-dev     # Run FastAPI with auto-reload
make frontend-dev    # Start Vite dev server
make test            # Run Python unit/integration tests
make format          # Placeholder for formatting hooks
```

## Testing

The backend includes pytest suites:

```bash
make test
```

During collection pytest reports progress as it moves through the suite. Seeing an intermediate message such as `[ 42% ]`
simply reflects that the first test module has completed (3 of 7 tests) and the run will finish at `[100%]` once every
backend test passes.

Ensure Node.js linting/tests are added as desired.

## Scraping Ethics & Legal Considerations

- Confirm that each provider’s terms of service permit data collection. Public plan pages typically allow access, but automated scraping can be restricted.
- Respect robots.txt and rate limits; the sample scrapers ship with conservative timeouts and are structured for easy throttling.
- Store only necessary plan metadata and avoid personal information.
- Provide clear attribution when visualising competitor data.

## Deployment Notes

- Use a production-ready PostgreSQL cluster and configure `DATABASE_URL` with SSL enforcement.
- Run migrations during deploy pipelines before starting application containers.
- Configure APScheduler to run on a single worker to avoid duplicate scrapes; disable it on secondary replicas.
- Consider deploying the frontend as a static site (e.g., Netlify, Vercel) and expose the FastAPI backend via a reverse proxy (NGINX, Traefik).
- For Selenium-based extensions, provision a headless Chrome/Firefox container and update the scraper modules accordingly.

## Project Structure

```
backend/
  main.py
  config.py
  models.py
  scrapers/
  routes/
  tests/
frontend/
  src/
    components/
Makefile
README.md
```

## Future Enhancements

- Replace sample HTML fixtures with live HTTP/Selenium scrapers and persistent caching.
- Add authentication and role-based access to the dashboard.
- Integrate alerting for significant price deviations.
- Expand charting to include historical trends via TimescaleDB or similar.
