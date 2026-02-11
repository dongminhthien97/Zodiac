from datetime import datetime, timezone
from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError
import logging

from models.schemas import (
    CompatibilityRequest, CompatibilityResponse, NatalRequest, NatalResponse, 
    StandardReportResponse, CompatibilityResponseNew, CompatibilityDetails
)
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


@router.post("/compatibility/new", response_model=CompatibilityResponseNew)
def compatibility_new(raw_payload: dict = Body(...)) -> CompatibilityResponseNew:
    """New compatibility endpoint with 2 calculation modes and comprehensive analysis"""
    try:
        payload = CompatibilityRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()

    # Get coordinates for both people (best-effort; compatibility can still be computed without houses)
    lat_a, lon_a, addr_a = geocoder.geocode(payload.person_a.birth_place)
    lat_b, lon_b, addr_b = geocoder.geocode(payload.person_b.birth_place)
    logger.info(f"Geocoding results (compatibility/new) - Person A: lat={lat_a}, lon={lon_a}, addr={addr_a}")
    logger.info(f"Geocoding results (compatibility/new) - Person B: lat={lat_b}, lon={lon_b}, addr={addr_b}")
    
    # Calculate compatibility with new system
    try:
        response = astrology.calculate_compatibility_new(
            payload.person_a,
            payload.person_b,
            lat_a=lat_a,
            lon_a=lon_a,
            lat_b=lat_b,
            lon_b=lon_b,
        )
        logger.info(f"New compatibility calculation successful")
        
        # Try to save to database, but don't fail the request if it fails
        try:
            supabase = get_supabase_client()
            if supabase:
                supabase.table("compatibility_checks").insert(
                    {
                        "person_a_name": payload.person_a.name,
                        "person_b_name": payload.person_b.name,
                        "person_a_place": payload.person_a.birth_place,
                        "person_b_place": payload.person_b.birth_place,
                        "score": response.scores.personality,
                        "created_at": "now()",
                    }
                ).execute()
        except Exception as e:
            logger.warning(f"Database save failed: {e}")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"New compatibility calculation failed: {e}")
        raise HTTPException(status_code=500, detail="Compatibility calculation failed")


@router.post("/natal", response_model=NatalResponse)
def natal(raw_payload: dict = Body(...)) -> NatalResponse:
    """Generate natal chart with unknown birth time support and robust fallback"""
    try:
        payload = NatalRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()

    # Validate API contract
    if payload.person.time_unknown and payload.person.birth_time is not None:
        raise HTTPException(
            status_code=400,
            detail="birth_time must be null when time_unknown is true"
        )
    
    if not payload.person.time_unknown and payload.person.birth_time is None:
        raise HTTPException(
            status_code=400,
            detail="birth_time must not be null when time_unknown is false"
        )

    # Get coordinates with fallback
    lat, lon, addr = geocoder.geocode(payload.person.birth_place)
    
    # Log coordinate resolution results
    if lat is not None and lon is not None:
        logger.info(f"Geocoding successful for {payload.person.name}: lat={lat}, lon={lon}, addr={addr}")
    else:
        logger.warning(f"Geocoding failed for {payload.person.name}, using fallback coordinates")
        # Use fallback coordinates for major Vietnamese cities
        fallback_coords = {
            "Đà Nẵng": (16.0544, 108.2022),
            "TP.HCM": (10.8231, 106.6297),
            "Hồ Chí Minh": (10.8231, 106.6297),
            "Sài Gòn": (10.8231, 106.6297),
            "Hà Nội": (21.0285, 105.8542),
            "Hanoi": (21.0285, 105.8542),
            "Ho Chi Minh": (10.8231, 106.6297),
        }
        
        # Try to find coordinates for known cities
        city_found = False
        for city, coords in fallback_coords.items():
            if city.lower() in payload.person.birth_place.lower():
                lat, lon = coords
                addr = f"{city} (fallback)"
                logger.info(f"Using fallback coordinates for {city}: lat={lat}, lon={lon}")
                city_found = True
                break
        
        # If no city found, use default coordinates
        if not city_found:
            lat, lon = 10.8231, 106.6297  # Default to Ho Chi Minh City
            addr = "Ho Chi Minh City (default fallback)"
            logger.info(f"Using default fallback coordinates: lat={lat}, lon={lon}")

    # Build chart with coordinates
    try:
        chart = astrology.build_natal_chart(payload.person, lat, lon)
        logger.info(f"Natal chart generation successful for {payload.person.name}")
    except HTTPException:
        # Re-raise HTTP exceptions from astrology service
        raise
    except Exception as e:
        logger.error(f"Critical error in natal chart generation for {payload.person.name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chart generation failed: {str(e)}"
        )

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


@router.post("/compatibility/professional", response_model=CompatibilityResponseNew)
def compatibility_professional(raw_payload: dict = Body(...)) -> CompatibilityResponseNew:
    """Professional compatibility analysis with 1000+ words detailed analysis"""
    try:
        payload = CompatibilityRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = GeocodingService()
    
    # Get coordinates for both people
    lat_a, lon_a, _ = geocoder.geocode(payload.person_a.birth_place)
    lat_b, lon_b, _ = geocoder.geocode(payload.person_b.birth_place)
    
    # Calculate compatibility with professional analysis
    try:
        response = astrology.calculate_compatibility_new(
            payload.person_a, payload.person_b,
            lat_a=lat_a, lon_a=lon_a, lat_b=lat_b, lon_b=lon_b
        )
        
        # Generate professional analysis if aspects are available
        if hasattr(response, 'planetaryAspects') and response.planetaryAspects:
            # Build chart data for professional analysis
            person_a_data = {
                'sun': {'sign': response.personality.summary.split(':')[1].split('/')[0].strip()},
                'moon': {'sign': response.personality.strengths[1].split(':')[1].strip()},
                'mercury': {'sign': response.work.teamwork.split(':')[1].strip()},
                'venus': {'sign': response.love.emotionalConnection.split(':')[1].strip()},
                'mars': {'sign': response.work.leadershipDynamic.split(':')[1].strip()},
                'ascendant': {'sign': response.personality.summary.split(':')[1].split('/')[0].strip()}
            }
            
            person_b_data = {
                'sun': {'sign': response.personality.summary.split(':')[1].split('/')[0].strip()},
                'moon': {'sign': response.personality.strengths[1].split(':')[1].strip()},
                'mercury': {'sign': response.work.teamwork.split(':')[1].strip()},
                'venus': {'sign': response.love.emotionalConnection.split(':')[1].strip()},
                'mars': {'sign': response.work.leadershipDynamic.split(':')[1].strip()},
                'ascendant': {'sign': response.personality.summary.split(':')[1].split('/')[0].strip()}
            }
            
            # Convert aspects to list format
            aspects_list = [aspect.aspect for aspect in response.planetaryAspects]
            
            # Generate professional analysis
            professional_analysis = astrology.generate_professional_compatibility_analysis(
                person_a_data, person_b_data, aspects_list
            )
            
            # Replace the detailed analysis with professional version
            response.detailedAnalysis = professional_analysis
        
        logger.info(f"Professional compatibility analysis successful")
        
        # Try to save to database, but don't fail the request if it fails
        try:
            supabase = get_supabase_client()
            if supabase:
                supabase.table("compatibility_checks").insert(
                    {
                        "person_a_name": payload.person_a.name,
                        "person_b_name": payload.person_b.name,
                        "person_a_place": payload.person_a.birth_place,
                        "person_b_place": payload.person_b.birth_place,
                        "score": response.scores.personality,
                        "created_at": "now()",
                    }
                ).execute()
        except Exception as e:
            logger.warning(f"Database save failed: {e}")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Professional compatibility analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Professional compatibility analysis failed")
