from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import os
import psycopg2

app = FastAPI()


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "skywalker"),
        user=os.getenv("POSTGRES_USER", "skywalker"),
        password=os.getenv("POSTGRES_PASSWORD", "skywalker"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


@app.get("/healthz")
def health_check():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as exc:  # pragma: no cover - defensive log
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "detail": str(exc)},
        )


@app.get("/")
def read_root():
    return {"message": "Welcome to the Skywalker API"}
