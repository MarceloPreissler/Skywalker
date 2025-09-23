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
