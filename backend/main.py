import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.astrology import router as astrology_router
from routers.chart import router as chart_router
from routers.zodiac_ai import router as zodiac_ai_router

# Import config and startup logging
from core.config import get_settings, settings, log_startup_info

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zodiac Compatibility Checker",
    version="0.1.0",
    description="API for astrology compatibility analysis and natal chart generation"
)

# CORS configuration
allow_origins = settings.cors_allow_origins_list
allow_credentials = settings.CORS_ALLOW_CREDENTIALS

# CORS note:
# - Browsers reject responses when `allow_credentials=True` with wildcard origins.
# - We therefore use explicit frontend origins by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup() -> None:
    """Railway/production startup checks (do not leak secrets)."""
    s = get_settings()
    log_startup_info()

    missing = s.missing_required()
    if missing:
        logger.warning("Missing required environment variables: %s", ", ".join(missing))
        if s.STRICT_ENV:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

# Mount routers
app.include_router(astrology_router, prefix="/api")
app.include_router(chart_router, prefix="/api")
app.include_router(zodiac_ai_router, prefix="/api")

@app.get("/")
def healthcheck() -> dict:
    """Health check endpoint for monitoring and load balancers"""
    return {"status": "ok", "service": "zodiac-compatibility-checker", "version": "0.1.0"}

@app.get("/health")
async def health() -> dict:
    """Health check endpoint for Render"""
    return {"status": "ok"}
