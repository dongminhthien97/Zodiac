"""
services/compatibility_service_new.py
-------------------------------------
New compatibility service - clean layered architecture.
Orchestrates astrology engine, AI service, and transformers.
Never exposes raw engine or AI data to frontend.
"""

from __future__ import annotations

import logging
import time
from typing import Optional, Dict, List, Any

from models.compatibility_schema import CompatibilityResponse
from services.astrology_engine import AstrologyEngine, PersonInput, AspectData, ChartData
from services.ai_service_groq import GroqAIService
from services.compatibility_transformers import CompatibilityTransformer
from core.config import settings

logger = logging.getLogger(__name__)


class CompatibilityServiceNew:
    """New compatibility service with clean layered architecture."""
    
    def __init__(self, groq_api_key: str, base_url: str = "https://api.groq.com/openai/v1"):
        """Initialize the new compatibility service."""
        self.astrology_engine = AstrologyEngine()
        self.ai_service = GroqAIService(groq_api_key, base_url=base_url)
        self.transformer = CompatibilityTransformer()
    
    async def analyze(
        self,
        person_a: PersonInput,
        person_b: PersonInput,
        lat_a: float,
        lon_a: float,
        lat_b: float,
        lon_b: float,
        request_id: Optional[str] = None,
    ) -> CompatibilityResponse:
        """Analyze compatibility between two people.
        
        Orchestrates:
        1. Astrological calculations
        2. Compatibility scoring
        3. AI narrative generation
        4. Schema transformation
        5. Validation
        
        Args:
            person_a: First person's data
            person_b: Second person's data
            lat_a: Latitude for person A
            lon_a: Longitude for person A
            lat_b: Latitude for person B
            lon_b: Longitude for person B
            request_id: Optional request ID for logging
            
        Returns:
            Validated CompatibilityResponse
        """
        request_id = request_id or f"compat_{int(time.time() * 1000)}"
        
        try:
            # Step 1: Build natal charts
            logger.info("[%s] Building natal charts", request_id)
            chart_a = self.astrology_engine.build_natal_chart(person_a, lat_a, lon_a)
            chart_b = self.astrology_engine.build_natal_chart(person_b, lat_b, lon_b)
            
            logger.info(
                "[%s] Charts built: A=%s/%s, B=%s/%s",
                request_id, chart_a.sun_sign, chart_a.moon_sign, chart_b.sun_sign, chart_b.moon_sign
            )
            
            # Step 2: Calculate compatibility aspects
            logger.info("[%s] Calculating compatibility aspects", request_id)
            aspects = self.astrology_engine.calculate_compatibility_aspects(chart_a, chart_b)
            
            # Convert aspects to dict format for AI service
            aspects_dict = [
                {
                    "planet_a": aspect.planet_a,
                    "planet_b": aspect.planet_b,
                    "aspect_type": aspect.aspect_type,
                    "orb": aspect.orb
                }
                for aspect in aspects
            ]
            
            logger.info("[%s] Calculated %d compatibility aspects", request_id, len(aspects))
            
            # Step 3: Calculate deterministic scores
            logger.info("[%s] Calculating compatibility scores", request_id)
            scores = self.astrology_engine.calculate_compatibility_scores(aspects)
            
            logger.info(
                "[%s] Scores calculated: overall=%d, emotional=%d, mental=%d, physical=%d, stability=%d, conflict=%d, longterm=%d",
                request_id, scores["overall_score"], scores["emotional_compatibility"],
                scores["mental_compatibility"], scores["physical_chemistry"],
                scores["stability_score"], scores["conflict_risk"], scores["long_term_potential"]
            )
            
            # Step 4: Generate AI narrative
            logger.info("[%s] Generating AI narrative", request_id)
            narrative = await self.ai_service.generate_narrative(
                person_a_name=person_a.name or "Person A",
                person_b_name=person_b.name or "Person B",
                scores=scores,
                aspects=aspects_dict,
                request_id=request_id
            )
            
            if narrative:
                logger.info("[%s] AI narrative generated successfully", request_id)
            else:
                logger.warning("[%s] AI narrative generation failed, using fallback", request_id)
            
            # Step 5: Transform to frontend schema
            logger.info("[%s] Transforming to frontend schema", request_id)
            response = self.transformer.transform_to_response(
                scores=scores,
                narrative=narrative,
                person_a_name=person_a.name or "Person A",
                person_b_name=person_b.name or "Person B"
            )
            
            # Step 6: Validate response
            logger.info("[%s] Validating response", request_id)
            if not self.transformer.validate_response(response):
                logger.error("[%s] Response validation failed, using fallback", request_id)
                response = self.transformer.create_fallback_response(
                    person_a_name=person_a.name or "Person A",
                    person_b_name=person_b.name or "Person B"
                )
            
            logger.info("[%s] Compatibility analysis completed successfully", request_id)
            
            return response
            
        except Exception as e:
            logger.error("[%s] Compatibility analysis failed: %s", request_id, e)
            # Return fallback response
            return self.transformer.create_fallback_response(
                person_a_name=person_a.name or "Person A",
                person_b_name=person_b.name or "Person B"
            )


def get_compatibility_service_new(api_key: str, base_url: str = "https://api.groq.com/openai/v1") -> CompatibilityServiceNew:
    """Create and return a new compatibility service instance."""
    return CompatibilityServiceNew(api_key, base_url=base_url)