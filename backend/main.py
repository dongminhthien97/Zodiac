import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.astrology import router as astrology_router
from routers.chart import router as chart_router
from routers.zodiac_ai import router as zodiac_ai_router

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Zodiac Compatibility Checker",
    version="0.1.0",
    description="API for astrology compatibility analysis and natal chart generation"
)

# CORS configuration
raw_origins = os.getenv(
    "CORS_ALLOW_ORIGINS",
    "https://zodiacs-jet.vercel.app,http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
)
allow_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"

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

# Mount routers
app.include_router(astrology_router, prefix="/api")
app.include_router(chart_router, prefix="/api")
app.include_router(zodiac_ai_router, prefix="/api")

@app.get("/")
def healthcheck() -> dict:
    """Health check endpoint for monitoring and load balancers"""
    return {"status": "ok", "service": "zodiac-compatibility-checker", "version": "0.1.0"}

@app.get("/health")
def health() -> dict:
    """Alternative health check endpoint"""
    return {"status": "healthy", "service": "zodiac-compatibility-checker"}
