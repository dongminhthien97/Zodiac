from datetime import datetime, timezone
from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError

from models.schemas import CompatibilityRequest, CompatibilityResponse, NatalInsights, NatalRequest, NatalResponse
from services.astrology_service import AstrologyService
from services.geocoding_service import GeocodingService
from supabase_client import get_supabase_client

router = APIRouter(tags=["astrology"])


@router.post("/compatibility", response_model=CompatibilityResponse)
def compatibility(raw_payload: dict = Body(...)) -> CompatibilityResponse:
    try:
        payload = CompatibilityRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()

    lat_a, lon_a, addr_a = geocoder.geocode(payload.person_a.birth_place)
    lat_b, lon_b, addr_b = geocoder.geocode(payload.person_b.birth_place)

    if lat_a is None or lon_a is None:
        raise HTTPException(status_code=400, detail="Không thể tìm được vị trí sinh của người A")
    if lat_b is None or lon_b is None:
        raise HTTPException(status_code=400, detail="Không thể tìm được vị trí sinh của người B")

    chart_a = astrology.build_natal_chart(payload.person_a, lat_a, lon_a)
    chart_b = astrology.build_natal_chart(payload.person_b, lat_b, lon_b)

    details = astrology.compatibility(
        chart_a,
        chart_b,
        payload.person_a.gender,
        payload.person_b.gender,
    )

    generated_at = datetime.now(timezone.utc).isoformat()
    response = CompatibilityResponse(generated_at=generated_at, person_a=chart_a, person_b=chart_b, details=details)

    supabase = get_supabase_client()
    if supabase:
        try:
            supabase.table("compatibility_checks").insert(
                {
                    "person_a_name": payload.person_a.name,
                    "person_b_name": payload.person_b.name,
                    "person_a_place": addr_a or payload.person_a.birth_place,
                    "person_b_place": addr_b or payload.person_b.birth_place,
                    "score": details.score,
                    "created_at": "now()",
                }
            ).execute()
        except Exception:
            pass

    return response


@router.post("/natal", response_model=NatalResponse)
def natal(raw_payload: dict = Body(...)) -> NatalResponse:
    try:
        payload = NatalRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()

    lat, lon, _addr = geocoder.geocode(payload.person.birth_place)
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Không thể tìm được vị trí sinh")

    chart = astrology.build_natal_chart(payload.person, lat, lon)
    insights = astrology.build_natal_insights(chart)
    return NatalResponse(generated_at=datetime.now(timezone.utc).isoformat(), person=chart, insights=insights)
