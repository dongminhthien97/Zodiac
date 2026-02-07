from datetime import datetime, timezone
from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError
import logging

from models.schemas import CompatibilityRequest, CompatibilityResponse, NatalRequest, NatalResponse, StandardReportResponse
from services.astrology_service import AstrologyService
from services.geocoding_service import GeocodingService
from supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["astrology"])


@router.post("/compatibility", response_model=CompatibilityResponse)
def compatibility(raw_payload: dict = Body(...)) -> CompatibilityResponse:
    """Calculate compatibility between two people with fault-tolerant chart generation"""
    try:
        payload = CompatibilityRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()

    # Get coordinates for both people
    lat_a, lon_a, addr_a = geocoder.geocode(payload.person_a.birth_place)
    lat_b, lon_b, addr_b = geocoder.geocode(payload.person_b.birth_place)

    # Log coordinate resolution results
    logger.info(f"Geocoding results - Person A: lat={lat_a}, lon={lon_a}, addr={addr_a}")
    logger.info(f"Geocoding results - Person B: lat={lat_b}, lon={lon_b}, addr={addr_b}")

    # Build charts with fault tolerance
    try:
        chart_a = astrology.build_natal_chart(payload.person_a, lat_a, lon_a)
        chart_b = astrology.build_natal_chart(payload.person_b, lat_b, lon_b)
        
        logger.info(f"Chart generation successful - Person A: {chart_a.sun_sign}, Person B: {chart_b.sun_sign}")
    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        # Return partial response with available data
        chart_a = astrology.build_natal_chart(payload.person_a, None, None)
        chart_b = astrology.build_natal_chart(payload.person_b, None, None)

    # Calculate compatibility
    try:
        details = astrology.compatibility(
            chart_a,
            chart_b,
            payload.person_a.gender,
            payload.person_b.gender,
        )
        logger.info(f"Compatibility calculation successful: score={details.score}")
    except Exception as e:
        logger.error(f"Compatibility calculation failed: {e}")
        # Return fallback compatibility details
        details = CompatibilityDetails(
            score=50,
            summary="Độ tương thích trung bình - Cần thêm thông tin để phân tích chi tiết",
            personality="Cần thêm thông tin để phân tích chi tiết",
            love_style="Cần thêm thông tin để phân tích chi tiết",
            career="Cần thêm thông tin để phân tích chi tiết",
            relationships="Cần thêm thông tin để phân tích chi tiết",
            advice="Hãy dành thời gian để tìm hiểu nhau nhiều hơn",
            conflict_points="Có thể có sự khác biệt trong cách thể hiện cảm xúc",
            recommended_activities=["Đi dạo và trò chuyện", "Tham gia hoạt động chung"],
            aspects=["Cần thêm thông tin để phân tích chi tiết"],
            ai_analysis="Phân tích AI không khả dụng do thiếu dữ liệu",
            detailed_reasoning="Lý do chi tiết không khả dụng do thiếu dữ liệu"
        )

    generated_at = datetime.now(timezone.utc).isoformat()
    response = CompatibilityResponse(generated_at=generated_at, person_a=chart_a, person_b=chart_b, details=details)

    # Try to save to database, but don't fail the request if it fails
    try:
        supabase = get_supabase_client()
        if supabase:
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
    except Exception as e:
        logger.warning(f"Database save failed: {e}")

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
    return astrology.build_v2_natal_response(chart, payload.person)

@router.post("/natal/standard", response_model=StandardReportResponse)
def natal_standard(raw_payload: dict = Body(...)) -> StandardReportResponse:
    """New endpoint for standard format report"""
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
    return astrology.build_standard_report(chart, payload.person)

