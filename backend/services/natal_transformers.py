"""
services/natal_transformers.py
------------------------------
Transformers for single person natal chart analysis.
Merges astrology engine data with AI interpretations.
No calculations, no AI, pure mapping and validation.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from datetime import datetime

from models.schemas import NatalAstrologyAI, NatalAIPlanet, NatalAIAspect
from services.astrology_engine import ChartData, PlanetData


class NatalTransformer:
    """Transforms raw natal data to frontend-compatible schema."""
    
    @staticmethod
    def transform_to_natal_response(
        chart: ChartData,
        person_name: str,
        person_birth_date: str,
        person_birth_time: Optional[str],
        person_time_unknown: bool,
        person_birth_place: str,
        lat: float,
        lon: float,
        ai_interpretations: Optional[Dict[str, Any]] = None
    ) -> NatalAstrologyAI:
        """Transform chart data and AI interpretations to NatalAstrologyAI.
        
        Args:
            chart: Natal chart data from astrology engine
            person_name: Person's name
            person_birth_date: Birth date
            person_birth_time: Birth time
            person_time_unknown: Whether time is unknown
            person_birth_place: Birth place
            lat: Latitude
            lon: Longitude
            ai_interpretations: Optional AI interpretations
            
        Returns:
            Validated NatalAstrologyAI response
        """
        # Build core identity
        core_identity = NatalTransformer._build_core_identity(
            chart, ai_interpretations, person_name
        )
        
        # Build planets with merged data
        planets = NatalTransformer._build_planets(
            chart.planets, ai_interpretations
        )
        
        # Build aspects
        aspects = NatalTransformer._build_aspects(
            chart.aspects, ai_interpretations
        )
        
        # Build other sections from AI interpretations
        love_profile = NatalTransformer._build_love_profile(ai_interpretations)
        career_analysis = NatalTransformer._build_career_analysis(ai_interpretations)
        psychological_pattern = NatalTransformer._build_psychological_pattern(ai_interpretations)
        practical_guidance = NatalTransformer._build_practical_guidance(ai_interpretations)
        
        # Create response
        response = NatalAstrologyAI(
            core_identity=core_identity,
            planets=planets,
            aspects=aspects,
            love_profile=love_profile,
            career_analysis=career_analysis,
            psychological_pattern=psychological_pattern,
            practical_guidance=practical_guidance
        )
        
        return response
    
    @staticmethod
    def _build_core_identity(
        chart: ChartData,
        ai_interpretations: Optional[Dict[str, Any]],
        person_name: str
    ) -> Dict[str, Any]:
        """Build core identity from chart and AI interpretations."""
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign
        rising_sign = chart.ascendant

        # Try to use real houses from engine when available
        sun_house = next((p.house for p in chart.planets if p.name == "Sun" and p.house is not None), 1)
        moon_house = next((p.house for p in chart.planets if p.name == "Moon" and p.house is not None), 4)

        # Prefer core_identity block when available
        core_identity = (ai_interpretations or {}).get("core_identity") or {}

        # Get interpretations from AI or use defaults
        def _as_nonempty_str(value: Any) -> Optional[str]:
            if isinstance(value, str) and value.strip():
                return value.strip()
            return None

        sun_interpretation = (
            (_as_nonempty_str(core_identity.get("sun_sign")) if isinstance(core_identity, dict) else None)
            or NatalTransformer._get_planet_interpretation(ai_interpretations, "Sun")
        )
        moon_interpretation = (
            (_as_nonempty_str(core_identity.get("moon_sign")) if isinstance(core_identity, dict) else None)
            or NatalTransformer._get_planet_interpretation(ai_interpretations, "Moon")
        )
        rising_interpretation = (
            (_as_nonempty_str(core_identity.get("rising_sign")) if isinstance(core_identity, dict) else None)
            or NatalTransformer._get_planet_interpretation(ai_interpretations, "Ascendant")
        )
        
        # Build summary
        summary = f"{person_name} - Mặt Trời {sun_sign}, Mặt Trăng {moon_sign}, Cung Mọc {rising_sign}"
        
        return {
            "summary": summary,
            "sun_sign": {
                "sign": sun_sign,
                "house": sun_house,
                "interpretation": sun_interpretation or f"Phân tích Mặt Trời {sun_sign} đang được xử lý..."
            },
            "moon_sign": {
                "sign": moon_sign,
                "house": moon_house,
                "interpretation": moon_interpretation or f"Phân tích Mặt Trăng {moon_sign} đang được xử lý..."
            },
            "rising_sign": {
                "sign": rising_sign,
                "interpretation": rising_interpretation or f"Phân tích Cung Mọc {rising_sign} đang được xử lý..."
            }
        }
    
    @staticmethod
    def _build_planets(
        planets_data: List[PlanetData],
        ai_interpretations: Optional[Dict[str, Any]]
    ) -> List[NatalAIPlanet]:
        """Build planets list with merged engine data and AI interpretations."""
        planets = []
        
        for planet_data in planets_data:
            # Get AI interpretation for this planet
            interpretation = NatalTransformer._get_planet_interpretation(
                ai_interpretations, planet_data.name
            )
            
            # Ensure degree is not null
            degree = planet_data.degree
            if degree is None:
                degree = round(planet_data.longitude % 30, 2)
            
            # Create planet entry
            planet = NatalAIPlanet(
                planet=NatalTransformer._get_vietnamese_planet_name(planet_data.name),
                sign=planet_data.sign,
                house=planet_data.house,
                retrograde=planet_data.speed < 0,
                interpretation=interpretation or f"Phân tích {planet_data.name} đang được xử lý...",
                longitude=round(planet_data.longitude, 2),
                degree=degree
            )
            
            planets.append(planet)
        
        return planets
    
    @staticmethod
    def _build_aspects(
        aspects_data: List[AspectData],
        ai_interpretations: Optional[Dict[str, Any]]
    ) -> List[NatalAIAspect]:
        """Build aspects list with AI interpretations."""
        aspects = []
        
        for aspect_data in aspects_data:
            # Get AI interpretation for this aspect
            interpretation = NatalTransformer._get_aspect_interpretation(
                ai_interpretations, aspect_data
            )
            
            aspect = NatalAIAspect(
                aspect_type=aspect_data.aspect_type,
                planet_1=aspect_data.planet_a,
                planet_2=aspect_data.planet_b,
                interpretation=interpretation or f"Phân tích aspect {aspect_data.aspect_type} đang được xử lý..."
            )
            
            aspects.append(aspect)
        
        return aspects
    
    @staticmethod
    def _build_love_profile(ai_interpretations: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """Build love profile from AI interpretations."""
        if not ai_interpretations or "love_profile" not in ai_interpretations:
            return {
                "attachment_style": "Đang phân tích...",
                "strengths": "Đang phân tích...",
                "challenges": "Đang phân tích...",
                "advice": "Đang phân tích..."
            }
        
        love_profile = ai_interpretations["love_profile"]
        return {
            "attachment_style": love_profile.get("attachment_style", "Đang phân tích..."),
            "strengths": love_profile.get("strengths", "Đang phân tích..."),
            "challenges": love_profile.get("challenges", "Đang phân tích..."),
            "advice": love_profile.get("advice", "Đang phân tích...")
        }
    
    @staticmethod
    def _build_career_analysis(ai_interpretations: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """Build career analysis from AI interpretations."""
        if not ai_interpretations or "career_analysis" not in ai_interpretations:
            return {
                "best_fields": "Đang phân tích...",
                "work_style": "Đang phân tích...",
                "growth_advice": "Đang phân tích..."
            }
        
        career_analysis = ai_interpretations["career_analysis"]
        return {
            "best_fields": career_analysis.get("best_fields", "Đang phân tích..."),
            "work_style": career_analysis.get("work_style", "Đang phân tích..."),
            "growth_advice": career_analysis.get("growth_advice", "Đang phân tích...")
        }
    
    @staticmethod
    def _build_psychological_pattern(ai_interpretations: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """Build psychological pattern from AI interpretations."""
        if not ai_interpretations or "psychological_pattern" not in ai_interpretations:
            return {
                "core_wound": "Đang phân tích...",
                "healing_direction": "Đang phân tích..."
            }
        
        psychological_pattern = ai_interpretations["psychological_pattern"]
        return {
            "core_wound": psychological_pattern.get("core_wound", "Đang phân tích..."),
            "healing_direction": psychological_pattern.get("healing_direction", "Đang phân tích...")
        }
    
    @staticmethod
    def _build_practical_guidance(ai_interpretations: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """Build practical guidance from AI interpretations."""
        if not ai_interpretations or "practical_guidance" not in ai_interpretations:
            return {
                "career": "Đang phân tích...",
                "relationships": "Đang phân tích...",
                "self_development": "Đang phân tích..."
            }
        
        practical_guidance = ai_interpretations["practical_guidance"]
        return {
            "career": practical_guidance.get("career", "Đang phân tích..."),
            "relationships": practical_guidance.get("relationships", "Đang phân tích..."),
            "self_development": practical_guidance.get("self_development", "Đang phân tích...")
        }
    
    @staticmethod
    def _get_planet_interpretation(
        ai_interpretations: Optional[Dict[str, Any]],
        planet_name: str
    ) -> Optional[str]:
        """Get interpretation for a specific planet from AI interpretations."""
        if not ai_interpretations:
            return None
        
        # Try to get interpretations from 'planet_interpretations' first
        interpretations_list = ai_interpretations.get("planet_interpretations")
        
        # If 'planet_interpretations' is not found or empty, fallback to 'planets'
        if not interpretations_list:
            interpretations_list = ai_interpretations.get("planets")
        
        if not interpretations_list: # If still no interpretations, return None
            return None
        
        for planet_data in interpretations_list:
            if planet_data.get("planet") == planet_name:
                return planet_data.get("interpretation")
        
        return None
    
    @staticmethod
    def _get_aspect_interpretation(
        ai_interpretations: Optional[Dict[str, Any]],
        aspect_data: AspectData
    ) -> Optional[str]:
        """Get interpretation for a specific aspect from AI interpretations."""
        if not ai_interpretations:
            return None
        
        # Try to get interpretations from 'aspect_interpretations' first
        interpretations_list = ai_interpretations.get("aspect_interpretations")
        
        # If 'aspect_interpretations' is not found or empty, fallback to 'aspects'
        if not interpretations_list:
            interpretations_list = ai_interpretations.get("aspects")
        
        if not interpretations_list: # If still no interpretations, return None
            return None
        
        target_type = str(aspect_data.aspect_type or "").strip().lower()
        target_a = str(aspect_data.planet_a or "").strip()
        target_b = str(aspect_data.planet_b or "").strip()

        for aspect in interpretations_list:
            if not isinstance(aspect, dict):
                continue

            aspect_type = str(aspect.get("aspect_type") or aspect.get("type") or "").strip().lower()
            if aspect_type != target_type:
                continue

            planet_1 = str(
                aspect.get("planet_1")
                or aspect.get("planet1")
                or aspect.get("planet_a")
                or ""
            ).strip()
            planet_2 = str(
                aspect.get("planet_2")
                or aspect.get("planet2")
                or aspect.get("planet_b")
                or ""
            ).strip()

            if (planet_1 == target_a and planet_2 == target_b) or (planet_1 == target_b and planet_2 == target_a):
                interpretation = aspect.get("interpretation")
                if isinstance(interpretation, str) and interpretation.strip():
                    return interpretation.strip()
        
        return None
    
    @staticmethod
    def _get_vietnamese_planet_name(english_name: str) -> str:
        """Convert English planet name to Vietnamese."""
        translations = {
            "Sun": "Mặt Trời",
            "Moon": "Mặt Trăng",
            "Mercury": "Sao Thủy",
            "Venus": "Sao Kim",
            "Mars": "Sao Hỏa",
            "Jupiter": "Sao Mộc",
            "Saturn": "Sao Thổ",
            "Uranus": "Sao Thiên Vương",
            "Neptune": "Sao Hải Vương",
            "Pluto": "Sao Diêm Vương"
        }
        return translations.get(english_name, english_name)
    
    @staticmethod
    def create_fallback_response(person_name: str) -> NatalAstrologyAI:
        """Create fallback response when AI fails."""
        return NatalAstrologyAI(
            core_identity={
                "summary": f"{person_name} - Đang phân tích...",
                "sun_sign": {"sign": "Unknown", "house": 1, "interpretation": "Đang phân tích..."},
                "moon_sign": {"sign": "Unknown", "house": 4, "interpretation": "Đang phân tích..."},
                "rising_sign": {"sign": "Unknown", "interpretation": "Đang phân tích..."}
            },
            planets=[
                NatalAIPlanet(
                    planet="Mặt Trời",
                    sign="Unknown",
                    house=1,
                    retrograde=False,
                    interpretation="Đang phân tích..."
                ),
                NatalAIPlanet(
                    planet="Mặt Trăng",
                    sign="Unknown",
                    house=4,
                    retrograde=False,
                    interpretation="Đang phân tích..."
                )
            ],
            aspects=[],
            love_profile={
                "attachment_style": "Đang phân tích...",
                "strengths": "Đang phân tích...",
                "challenges": "Đang phân tích...",
                "advice": "Đang phân tích..."
            },
            career_analysis={
                "best_fields": "Đang phân tích...",
                "work_style": "Đang phân tích...",
                "growth_advice": "Đang phân tích..."
            },
            psychological_pattern={
                "core_wound": "Đang phân tích...",
                "healing_direction": "Đang phân tích..."
            },
            practical_guidance={
                "career": "Đang phân tích...",
                "relationships": "Đang phân tích...",
                "self_development": "Đang phân tích..."
            }
        )
    
    @staticmethod
    def validate_response(response: NatalAstrologyAI) -> bool:
        """Validate that response meets all requirements."""
        try:
            # Check all planets have longitude and degree
            for planet in response.planets:
                if planet.longitude is None or planet.degree is None:
                    return False
                
                # Ensure degree is calculated correctly
                expected_degree = round(planet.longitude % 30, 2)
                if abs(planet.degree - expected_degree) > 0.1:
                    return False
            
            # Check all required fields are present
            required_sections = [
                "core_identity", "planets", "aspects",
                "love_profile", "career_analysis", 
                "psychological_pattern", "practical_guidance"
            ]
            
            for section in required_sections:
                if not hasattr(response, section):
                    return False
            
            return True
            
        except Exception:
            return False
