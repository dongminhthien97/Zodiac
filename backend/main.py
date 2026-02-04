from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.astrology import router as astrology_router

app = FastAPI(title="Zodiac Compatibility Checker", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(astrology_router, prefix="/api")

@app.get("/")
def healthcheck() -> dict:
    return {"status": "ok", "service": "zodiac-compatibility-checker"}
