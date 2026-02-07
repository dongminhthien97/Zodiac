"""
Zodiac AI Router - Professional-quality astrological reports
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from services.zodiac_ai_service import ZodiacAIService

router = APIRouter(prefix="/api/zodiac-ai", tags=["Zodiac AI"])

class ZodiacAIRequest(BaseModel):
    datetime_utc: str
    lat: float
    lon: float

class ZodiacAIResponse(BaseModel):
    report: str
    generated_at: str
    chart_data: Dict[str, Any]
    placements: list

@router.post("/report", response_model=ZodiacAIResponse)
async def generate_zodiac_ai_report(request: ZodiacAIRequest):
    """
    Generate a professional-quality astrological report similar to Zodiac AI
    
    This endpoint creates comprehensive natal chart analyses with:
    - Professional astrological terminology
    - Structured report format (Overview, Identity, Love, Generation, Lessons, Conclusion)
    - High-quality content similar to professional astrologer analysis
    - Vietnamese language support
    """
    try:
        zodiac_service = ZodiacAIService()
        result = zodiac_service.generate_zodiac_ai_report(
            request.datetime_utc,
            request.lat,
            request.lon
        )
        
        return ZodiacAIResponse(
            report=result["report"],
            generated_at=result["generated_at"],
            chart_data=result["chart_data"],
            placements=result["placements"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating Zodiac AI report: {str(e)}"
        )

@router.get("/health")
async def zodiac_ai_health():
    """Health check for Zodiac AI service"""
    return {
        "status": "healthy",
        "service": "Zodiac AI Professional Reports",
        "version": "1.0.0"
    }