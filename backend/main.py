from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings
from .database import get_session
from .deps import verify_api_key
from .routes import plans, providers
from .scheduler import schedule_jobs, shutdown_scheduler
from .scrapers.runner import initialize_database, run_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    await schedule_jobs()
    yield
    await shutdown_scheduler()


app = FastAPI(title="Energy Plan Aggregator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"],
)

app.include_router(providers.router)
app.include_router(plans.router)
@app.post("/scrape", dependencies=[Depends(verify_api_key)], status_code=status.HTTP_202_ACCEPTED)
async def trigger_scrape(
    payload: dict | None = None,
    session: AsyncSession = Depends(get_session),
):
    settings = get_settings()
    providers_to_scrape = payload.get("providers") if payload else settings.scrape_providers
    if not providers_to_scrape:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No providers requested")

    results = []
    for slug in providers_to_scrape:
        try:
            result = await run_scraper(session, slug)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        results.append({
            "provider": result.provider.slug,
            "plans": [plan.name for plan in result.plans],
        })

    return {"status": "queued", "results": results}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
