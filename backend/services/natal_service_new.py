"""
services/natal_service_new.py
-----------------------------
New natal service with clean layered architecture.
Orchestrates astrology engine, AI service, and transformers.
Never exposes raw engine or AI data to frontend.
"""

from __future__ import annotations

import logging
import time
from typing import Optional, Dict, List, Any

from models.schemas import NatalAIResponse, NatalAstrologyAI
from services.astrology_engine import AstrologyEngine, PersonInput, ChartData
from services.natal_ai_service import NatalAIService
from services.natal_transformers import NatalTransformer
from core.config import settings

logger = logging.getLogger(__name__)


class NatalServiceNew:
    """New natal service with clean layered architecture."""
    
    def __init__(self, groq_api_key: str, base_url: str = "https://api.groq.com/openai/v1"):
        """Initialize the new natal service."""
        self.astrology_engine = AstrologyEngine()
        self.ai_service = NatalAIService(groq_api_key, base_url=base_url)
        self.transformer = NatalTransformer()
    
    async def analyze(
        self,
        person: PersonInput,
        lat: float,
        lon: float,
        request_id: Optional[str] = None,
    ) -> NatalAIResponse:
        """Analyze natal chart for a person.
        
        Orchestrates:
        1. Astrological calculations
        2. AI interpretation generation
        3. Schema transformation
        4. Validation
        
        Args:
            person: Person's data
            lat: Latitude
            lon: Longitude
            request_id: Optional request ID for logging
            
        Returns:
            Validated NatalAIResponse
        """
        request_id = request_id or f"natal_{int(time.time() * 1000)}"
        
        try:
            # Step 1: Build natal chart
            logger.info("[%s] Building natal chart", request_id)
            chart = self.astrology_engine.build_natal_chart(person, lat, lon)
            
            logger.info(
                "[%s] Chart built: Sun=%s, Moon=%s, Rising=%s",
                request_id, chart.sun_sign, chart.moon_sign, chart.ascendant
            )
            
            # Step 2: Prepare data for AI service
            planets_data = []
            for planet_data in chart.planets:
                # Ensure degree is not null
                degree = planet_data.degree
                if degree is None:
                    degree = round(planet_data.longitude % 30, 2)
                
                planet_dict = {
                    "planet": planet_data.name,
                    "sign": planet_data.sign,
                    "longitude": round(planet_data.longitude, 2),
                    "degree": degree,
                    "house": planet_data.house,
                    "retrograde": planet_data.speed < 0
                }
                planets_data.append(planet_dict)
            
            aspects_data = []
            for aspect_data in chart.aspects:
                aspect_dict = {
                    "aspect_type": aspect_data.aspect_type,
                    "planet_1": aspect_data.planet_a,
                    "planet_2": aspect_data.planet_b,
                    "orb": aspect_data.orb
                }
                aspects_data.append(aspect_dict)
            
            logger.info("[%s] Prepared %d planets and %d aspects for AI", request_id, len(planets_data), len(aspects_data))
            
            # Step 3: Generate AI interpretations
            logger.info("[%s] Generating AI interpretations", request_id)
            ai_interpretations = await self.ai_service.generate_interpretations(
                person_name=person.name or "Person",
                person_birth_date=person.birth_date,
                person_birth_time=person.birth_time,
                person_birth_place=person.birth_place,
                planets_data=planets_data,
                aspects_data=aspects_data,
                request_id=request_id
            )
            
            if ai_interpretations:
                logger.info("[%s] AI interpretations generated successfully", request_id)
            else:
                logger.warning("[%s] AI interpretations generation failed, using fallback", request_id)
            
            # Step 4: Transform to frontend schema
            logger.info("[%s] Transforming to frontend schema", request_id)
            astrology_ai = self.transformer.transform_to_natal_response(
                chart=chart,
                person_name=person.name or "Person",
                person_birth_date=person.birth_date,
                person_birth_time=person.birth_time,
                person_time_unknown=person.time_unknown,
                person_birth_place=person.birth_place,
                lat=lat,
                lon=lon,
                ai_interpretations=ai_interpretations
            )
            
            # Step 5: Validate response
            logger.info("[%s] Validating response", request_id)
            if not self.transformer.validate_response(astrology_ai):
                logger.error("[%s] Response validation failed, using fallback", request_id)
                astrology_ai = self.transformer.create_fallback_response(person.name or "Person")
            
            # Build final response
            meta = {
                "name": person.name,
                "birth_date": person.date,
                "birth_time": person.time,
                "time_unknown": False,
                "birth_place": person.city + ", " + person.country,
                "lat": lat,
                "lon": lon,
                "resolved_address": f"{person.city}, {person.country}",
            }
            
            response = NatalAIResponse(
                meta=meta,
                astrology_ai=astrology_ai
            )
            
            logger.info("[%s] Natal analysis completed successfully", request_id)
            
            return response
            
        except Exception as e:
            logger.error("[%s] Natal analysis failed: %s", request_id, e)
            # Return fallback response
            fallback_astrology_ai = self.transformer.create_fallback_response(person.name or "Person")
            return NatalAIResponse(
                meta={
                    "name": person.name,
                    "birth_date": person.date,
                    "birth_time": person.time,
                    "time_unknown": True,
                    "birth_place": person.city + ", " + person.country,
                    "lat": lat,
                    "lon": lon,
                    "resolved_address": "Fallback mode",
                },
                astrology_ai=fallback_astrology_ai
            )


def get_natal_service_new(api_key: str, base_url: str = "https://api.groq.com/openai/v1") -> NatalServiceNew:
    """Create and return a new natal service instance."""
    return NatalServiceNew(api_key, base_url=base_url)