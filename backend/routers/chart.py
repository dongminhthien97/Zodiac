from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
import logging

from models.schemas import ChartRequest, ChartCoreResponse
from services.ephemeris_core import init_ephemeris, compute_planets, detect_aspects, compute_houses

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chart", response_class=JSONResponse)
async def chart_endpoint(payload: ChartRequest):
    """Compute chart core using Swiss Ephemeris only.

    Returns deterministic, structured JSON suitable for downstream interpretation.
    """
    # initialize ephemeris path once (no-op if already set)
    try:
        init_ephemeris()
    except Exception as e:
        logger.exception("Ephemeris initialization failed")
        raise HTTPException(status_code=500, detail=str(e))

    # Validate house_system
    hs = payload.house_system
    if hs not in {None, "whole_sign", "placidus"}:
        raise HTTPException(status_code=400, detail="Unsupported house system")

    mode = "WITH_HOUSE" if payload.time is not None else "NO_HOUSE"

    try:
        planets = compute_planets(payload.date, payload.time, payload.timezone, payload.location)
    except Exception as e:
        logger.exception("Planet computation failed")
        raise HTTPException(status_code=500, detail=str(e))

    # Build points (mean_node, true_node, chiron) if present
    points = {k: v for k, v in planets.items() if k in {"mean_node", "true_node", "chiron"}}

    # Extract only the required planetary bodies for the output (sun..pluto)
    planets_core: Dict[str, object] = {}
    for p in ["sun","moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"]:
        if p in planets:
            planets_core[p] = planets[p].model_dump()

    aspects = detect_aspects(planets)

    houses = None
    if mode == "WITH_HOUSE":
        # default to requested house system or placidus if None
        hs_use = hs or "placidus"
        try:
            houses = compute_houses(payload.date, payload.time, payload.timezone, payload.location, hs_use)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.exception("House computation failed")
            raise HTTPException(status_code=500, detail=str(e))

    response = ChartCoreResponse(
        mode=mode,
        planets=planets_core,
        points={k: v.model_dump() for k, v in points.items()},
        aspects=[a.model_dump() for a in aspects],
        houses=houses.model_dump() if houses else None,
    )

    return JSONResponse(content=response.model_dump())
