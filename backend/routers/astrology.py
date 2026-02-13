from datetime import datetime, timezone
from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError
import logging

from models.schemas import (
    CompatibilityRequest, CompatibilityResponse, NatalRequest, NatalResponse, 
    StandardReportResponse, CompatibilityResponseNew, CompatibilityDetails,
    AICompatibilityReportRequest, AICompatibilityReportResponse
)
from services.astrology_service import AstrologyService
from services.geocoding_service import GeocodingService, OpenCageService
from services.ai_service import get_global_ai_service
from supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["astrology"])


@router.post("/compatibility", response_model=CompatibilityResponse)
async def compatibility(raw_payload: dict = Body(...)) -> CompatibilityResponse:
    """Calculate compatibility between two people with fault-tolerant chart generation"""
    try:
        payload = CompatibilityRequest.model_validate(raw_payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    astrology = AstrologyService()
    geocoder = OpenCageService(settings.OPENCAGE_API_KEY)

    # Get coordinates for both people
    try:
        result_a = geocoder.geocode(payload.person_a.birth_place)
        result_b = geocoder.geocode(payload.person_b.birth_place)
        
        lat_a, lon_a, addr_a = result_a['lat'], result_a['lon'], result_a['formatted']
        lat_b, lon_b, addr_b = result_b['lat'], result_b['lon'], result_b['formatted']
        
        # Log coordinate resolution results
        logger.info(f"Geocoding successful - Person A: lat={lat_a}, lon={lon_a}, confidence={result_a['confidence']}")
        logger.info(f"Geocoding successful - Person B: lat={lat_b}, lon={lon_b}, confidence={result_b['confidence']}")
        
    except ValueError as e:
        logger.error(f"Geocoding failed: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Unable to geocode location: {str(e)}"
        )

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

    # Generate AI report using Groq API
    try:
        # Build structured analysis data for Groq
        analysis_data = {
            "person_a": {
                "sun": chart_a.sun_sign,
                "moon": chart_a.moon_sign or chart_a.sun_sign,
                "mercury": astrology._get_planet_sign(chart_a, "Mercury") or chart_a.sun_sign,
                "venus": astrology._get_planet_sign(chart_a, "Venus") or chart_a.sun_sign,
                "mars": astrology._get_planet_sign(chart_a, "Mars") or chart_a.sun_sign,
                "ascendant": chart_a.ascendant or chart_a.sun_sign
            },
            "person_b": {
                "sun": chart_b.sun_sign,
                "moon": chart_b.moon_sign or chart_b.sun_sign,
                "mercury": astrology._get_planet_sign(chart_b, "Mercury") or chart_b.sun_sign,
                "venus": astrology._get_planet_sign(chart_b, "Venus") or chart_b.sun_sign,
                "mars": astrology._get_planet_sign(chart_b, "Mars") or chart_b.sun_sign,
                "ascendant": chart_b.ascendant or chart_b.sun_sign
            },
            "aspects": details.aspects,
            "score": details.score,
            "fallback_mode": lat_a is None or lon_a is None or lat_b is None or lon_b is None
        }
        
        # Build comprehensive prompt for Groq
        prompt = f"""Hãy phân tích sự tương thích chi tiết giữa hai bản đồ sao sau đây:

**Thông tin hai người:**
- Người A: Mặt Trời {analysis_data['person_a']['sun']}, Mặt Trăng {analysis_data['person_a']['moon']}, Thủy Tinh {analysis_data['person_a']['mercury']}, Kim Tinh {analysis_data['person_a']['venus']}, Hỏa Tinh {analysis_data['person_a']['mars']}, Cung Mọc {analysis_data['person_a']['ascendant']}
- Người B: Mặt Trời {analysis_data['person_b']['sun']}, Mặt Trăng {analysis_data['person_b']['moon']}, Thủy Tinh {analysis_data['person_b']['mercury']}, Kim Tinh {analysis_data['person_b']['venus']}, Hỏa Tinh {analysis_data['person_b']['mars']}, Cung Mọc {analysis_data['person_b']['ascendant']}

**Các aspect quan trọng:** {', '.join(analysis_data['aspects'])}

{f'⚠️ Lưu ý: Phân tích ở chế độ fallback (thiếu giờ sinh), một số tính toán có thể không chính xác hoàn toàn.' if analysis_data['fallback_mode'] else 'Phân tích với đầy đủ thông tin giờ sinh.'}

**Yêu cầu phân tích chi tiết (ít nhất 1000 từ):**

1. **Sự tương thích về cảm xúc (Emotional Compatibility):**
   - Phân tích Mặt Trăng {analysis_data['person_a']['moon']} và Mặt Trăng {analysis_data['person_b']['moon']}
   - Cách hai người đáp ứng nhu cầu cảm xúc của nhau
   - Khả năng tạo môi trường cảm xúc an toàn

2. **Sức hút và tình yêu (Romantic Attraction):**
   - Phân tích Kim Tinh {analysis_data['person_a']['venus']} và Kim Tinh {analysis_data['person_b']['venus']}
   - Cách thể hiện tình yêu và đam mê
   - Sự hấp dẫn tình dục và hóa học

3. **Giao tiếp và tư duy (Communication):**
   - Phân tích Thủy Tinh {analysis_data['person_a']['mercury']} và Thủy Tinh {analysis_data['person_b']['mercury']}
   - Cách trao đổi ý tưởng và giải quyết bất đồng
   - Phong cách giao tiếp hàng ngày

4. **Xung đột và thách thức (Conflict):**
   - Những điểm xung đột tiềm ẩn
   - Cách xử lý mâu thuẫn
   - Cơ chế phòng vệ và phản ứng khi căng thẳng

5. **Ổn định lâu dài (Long-term Stability):**
   - Khả năng duy trì mối quan hệ
   - Sự phù hợp về giá trị và mục tiêu sống
   - Tiềm năng phát triển cùng nhau

6. **Phân tích hành tinh cụ thể:**
   - Tác động của từng cặp hành tinh quan trọng
   - Cách các aspect ảnh hưởng đến mối quan hệ
   - Cơ hội và thách thức từ các vị trí hành tinh

7. **Phát triển bản thân (Growth Path):**
   - Bài học mà mỗi người có thể học được từ nhau
   - Cách hỗ trợ sự phát triển cá nhân
   - Cơ hội trưởng thành tâm hồn

8. **Lời khuyên thực tế (Practical Advice):**
   - Cách nuôi dưỡng mối quan hệ
   - Chiến lược giải quyết xung đột
   - Phương pháp duy trì sự hấp dẫn lâu dài

**Yêu cầu:**
- Sử dụng ngôn ngữ chuyên nghiệp, giàu chiều sâu tâm lý
- Cung cấp ví dụ cụ thể và thiết thực
- Phân tích chi tiết từng khía cạnh
- Đưa ra lời khuyên thực tế và khả thi
- Tổng cộng ít nhất 1000 từ
- Định dạng markdown chuyên nghiệp

Hãy cung cấp một bản phân tích toàn diện, sâu sắc và thực tế."""
        
        # Generate AI report using Groq API
        ai_service_instance = get_global_ai_service()
        if ai_service_instance:
            ai_report = await ai_service_instance.generate_long_report(prompt, min_words=1000)
        else:
            ai_report = "Phân tích AI không khả dụng do thiếu cấu hình API"
        
        logger.info(f"✅ Groq AI report generated successfully. Length: {len(ai_report)} characters")
        
    except Exception as e:
        logger.error(f"❌ Groq AI report generation failed: {e}")
        # Fallback to error message but don't fail the entire request
        ai_report = f"""**LỖI PHÂN TÍCH AI**

Phân tích AI không thể được tạo do lỗi hệ thống. Vui lòng thử lại sau.

**Chi tiết lỗi:** {str(e)}

**Thông tin cơ bản vẫn khả dụng:**
- Điểm tương thích: {details.score}/100
- Tóm tắt: {details.summary}
- Lời khuyên: {details.advice}"""
        logger.warning("⚠️ Using fallback AI report due to Groq API failure")

    generated_at = datetime.now(timezone.utc).isoformat()
    response = CompatibilityResponse(
        generated_at=generated_at, 
        person_a=chart_a, 
        person_b=chart_b, 
        details=details,
        full_report=ai_report  # Add the AI-generated report
    )

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
    geocoder = OpenCageService(settings.OPENCAGE_API_KEY)

    # Get coordinates for both people
    try:
        result_a = geocoder.geocode(payload.person_a.birth_place)
        result_b = geocoder.geocode(payload.person_b.birth_place)
        
        lat_a, lon_a, addr_a = result_a['lat'], result_a['lon'], result_a['formatted']
        lat_b, lon_b, addr_b = result_b['lat'], result_b['lon'], result_b['formatted']
        
        # Log coordinate resolution results
        logger.info(f"Geocoding successful - Person A: lat={lat_a}, lon={lon_a}, confidence={result_a['confidence']}")
        logger.info(f"Geocoding successful - Person B: lat={lat_b}, lon={lon_b}, confidence={result_b['confidence']}")
        
    except ValueError as e:
        logger.error(f"Geocoding failed: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Unable to geocode location: {str(e)}"
        )
    
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
    geocoder = OpenCageService(settings.OPENCAGE_API_KEY)

    # Get coordinates with strict validation
    try:
        result = geocoder.geocode(payload.person.birth_place)
        lat, lon = result['lat'], result['lon']
        
        # Log coordinate resolution results
        logger.info(f"Geocoding successful for {payload.person.name}: lat={lat}, lon={lon}, confidence={result['confidence']}")
        
    except ValueError as e:
        logger.error(f"Geocoding failed for {payload.person.name}: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Không thể tìm được vị trí sinh: {str(e)}"
        )

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


@router.post("/compatibility/ai", response_model=dict)
def compatibility_ai(
    person_a: dict = Body(..., description="Person A chart data"),
    person_b: dict = Body(..., description="Person B chart data"),
    aspects: list = Body(..., description="List of planetary aspects"),
    fallback_mode: bool = Body(False, description="Fallback mode flag")
) -> dict:
    """AI compatibility analysis with JSON output and >=1000 words"""
    try:
        astrology = AstrologyService()
        
        # Generate AI compatibility analysis
        result = astrology.generate_ai_compatibility_analysis_json(
            person_a, person_b, aspects, fallback_mode
        )
        
        logger.info(f"AI compatibility analysis successful")
        
        return result
        
    except Exception as e:
        logger.error(f"AI compatibility analysis failed: {e}")
        raise HTTPException(status_code=500, detail="AI compatibility analysis failed")


@router.post("/compatibility/ai-report", response_model=AICompatibilityReportResponse)
async def compatibility_ai_report(request: AICompatibilityReportRequest) -> AICompatibilityReportResponse:
    """Generate AI compatibility report using Groq API with minimum 1000 words"""
    try:
        from services.ai_service import ai_service
        
        # Build comprehensive prompt
        prompt = _build_compatibility_prompt(
            request.person_a,
            request.person_b,
            request.aspects,
            request.fallback_mode
        )
        
        logger.info(f"Generating AI compatibility report with prompt length: {len(prompt)} characters")
        
        # Generate report using Groq API
        report_content = await ai_service.generate_long_report(prompt, min_words=1000)
        
        # Count words in the final report
        word_count = _count_words(report_content)
        
        logger.info(f"AI report generation completed. Final word count: {word_count}")
        
        return AICompatibilityReportResponse(
            success=True,
            wordCount=word_count,
            report=report_content,
            model=ai_service.model
        )
        
    except httpx.TimeoutException as e:
        logger.error(f"Groq API request timed out: {e}")
        raise HTTPException(status_code=504, detail="AI service timeout - please try again")
    except httpx.HTTPStatusError as e:
        logger.error(f"Groq API returned error: {e}")
        raise HTTPException(status_code=502, detail="AI service temporarily unavailable")
    except Exception as e:
        logger.error(f"AI compatibility report generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI compatibility report")


def _build_compatibility_prompt(person_a: dict, person_b: dict, aspects: list, fallback_mode: bool) -> str:
    """Build a comprehensive prompt for compatibility analysis"""
    
    # Extract signs
    sun_a = person_a.get('sun', 'Unknown')
    moon_a = person_a.get('moon', 'Unknown')
    mercury_a = person_a.get('mercury', 'Unknown')
    venus_a = person_a.get('venus', 'Unknown')
    mars_a = person_a.get('mars', 'Unknown')
    asc_a = person_a.get('ascendant', 'Unknown')
    
    sun_b = person_b.get('sun', 'Unknown')
    moon_b = person_b.get('moon', 'Unknown')
    mercury_b = person_b.get('mercury', 'Unknown')
    venus_b = person_b.get('venus', 'Unknown')
    mars_b = person_b.get('mars', 'Unknown')
    asc_b = person_b.get('ascendant', 'Unknown')
    
    # Build prompt
    prompt = f"""Hãy phân tích sự tương thích chi tiết giữa hai bản đồ sao sau đây:

**Thông tin hai người:**
- Người A: Mặt Trời {sun_a}, Mặt Trăng {moon_a}, Thủy Tinh {mercury_a}, Kim Tinh {venus_a}, Hỏa Tinh {mars_a}, Cung Mọc {asc_a}
- Người B: Mặt Trời {sun_b}, Mặt Trăng {moon_b}, Thủy Tinh {mercury_b}, Kim Tinh {venus_b}, Hỏa Tinh {mars_b}, Cung Mọc {asc_b}

**Các aspect quan trọng:** {', '.join(aspects) if aspects else 'Không có aspect cụ thể'}

{f'⚠️ Lưu ý: Phân tích ở chế độ fallback (thiếu giờ sinh), một số tính toán có thể không chính xác hoàn toàn.' if fallback_mode else 'Phân tích với đầy đủ thông tin giờ sinh.'}

**Yêu cầu phân tích chi tiết (ít nhất 1000 từ):**

1. **Sự tương thích về cảm xúc (Emotional Compatibility):**
   - Phân tích Mặt Trăng {moon_a} và Mặt Trăng {moon_b}
   - Cách hai người đáp ứng nhu cầu cảm xúc của nhau
   - Khả năng tạo môi trường cảm xúc an toàn

2. **Sức hút và tình yêu (Romantic Attraction):**
   - Phân tích Kim Tinh {venus_a} và Kim Tinh {venus_b}
   - Cách thể hiện tình yêu và đam mê
   - Sự hấp dẫn tình dục và hóa học

3. **Giao tiếp và tư duy (Communication):**
   - Phân tích Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b}
   - Cách trao đổi ý tưởng và giải quyết bất đồng
   - Phong cách giao tiếp hàng ngày

4. **Xung đột và thách thức (Conflict):**
   - Những điểm xung đột tiềm ẩn
   - Cách xử lý mâu thuẫn
   - Cơ chế phòng vệ và phản ứng khi căng thẳng

5. **Ổn định lâu dài (Long-term Stability):**
   - Khả năng duy trì mối quan hệ
   - Sự phù hợp về giá trị và mục tiêu sống
   - Tiềm năng phát triển cùng nhau

6. **Phân tích hành tinh cụ thể:**
   - Tác động của từng cặp hành tinh quan trọng
   - Cách các aspect ảnh hưởng đến mối quan hệ
   - Cơ hội và thách thức từ các vị trí hành tinh

7. **Phát triển bản thân (Growth Path):**
   - Bài học mà mỗi người có thể học được từ nhau
   - Cách hỗ trợ sự phát triển cá nhân
   - Cơ hội trưởng thành tâm hồn

8. **Lời khuyên thực tế (Practical Advice):**
   - Cách nuôi dưỡng mối quan hệ
   - Chiến lược giải quyết xung đột
   - Phương pháp duy trì sự hấp dẫn lâu dài

**Yêu cầu:**
- Sử dụng ngôn ngữ chuyên nghiệp, giàu chiều sâu tâm lý
- Cung cấp ví dụ cụ thể và thiết thực
- Phân tích chi tiết từng khía cạnh
- Đưa ra lời khuyên thực tế và khả thi
- Tổng cộng ít nhất 1000 từ
- Định dạng markdown chuyên nghiệp

Hãy cung cấp một bản phân tích toàn diện, sâu sắc và thực tế."""
    
    return prompt


def _count_words(text: str) -> int:
    """Count words in text"""
    import re
    if not text:
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)


# Import httpx for error handling
import httpx
