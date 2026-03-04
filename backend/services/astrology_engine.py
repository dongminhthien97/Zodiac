"""
services/astrology_engine.py
----------------------------
Astrological calculation engine.
Pure calculation logic, no AI, no schema mapping.
"""

from __future__ import annotations

import logging
import swisseph as swe
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict

from models.compatibility_schema import CompatibilityResponse, RelationshipSummary

logger = logging.getLogger(__name__)


class PersonInput(BaseModel):
    """Input data for a person."""
    name: str | None = None
    birth_date: str
    birth_time: str | None = None
    birth_place: str
    time_unknown: bool = False

    model_config = ConfigDict(extra="forbid")


@dataclass
class AspectData:
    """Aspect between two planets."""
    planet_a: str
    planet_b: str
    aspect_type: str
    orb: float


@dataclass
class PlanetData:
    """Planet position data."""
    name: str
    longitude: float
    latitude: float
    speed: float
    sign: str
    degree: float
    house: int


@dataclass
class ChartData:
    """Complete natal chart data."""
    sun_sign: str
    moon_sign: str
    ascendant: str
    planets: List[PlanetData]
    houses: List[float]
    aspects: List[AspectData]


class AstrologyEngine:
    """Core astrological calculation engine."""
    
    # Aspect definitions
    ASPECT_ANGLES = {
        "conjunction": 0.0,
        "sextile": 60.0,
        "square": 90.0,
        "trine": 120.0,
        "opposition": 180.0,
    }
    
    # Planet constants
    PLANET_CONSTANTS = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO,
    }
    
    # Sign names
    SIGN_NAMES = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    # House system
    HOUSE_SYSTEM = b'P'  # Placidus
    
    def __init__(self):
        """Initialize the astrology engine."""
        # Set Swiss Ephemeris path
        swe.set_ephe_path(None)
    
    def _get_sign_from_longitude(self, longitude: float) -> str:
        """Get zodiac sign from longitude."""
        lon = float(longitude) % 360.0
        return self.SIGN_NAMES[int(lon // 30)]
    
    def _get_degree_from_longitude(self, longitude: float) -> float:
        """Get degree within sign from longitude."""
        lon = float(longitude) % 360.0
        degree = lon % 30.0
        return round(degree, 2)
    
    def _get_house_for_longitude(self, longitude: float, cusps: List[float]) -> int:
        """Get house number for a given longitude."""
        if not cusps or len(cusps) < 12:
            return 0
        
        cusp0 = float(cusps[0]) % 360.0
        normalized = [cusp0]
        current = cusp0
        for i in range(1, 12):
            nxt = float(cusps[i]) % 360.0
            if nxt <= current:
                nxt += 360.0
            normalized.append(nxt)
            current = nxt
        normalized.append(normalized[0] + 360.0)
        
        lon = float(longitude) % 360.0
        if lon < cusp0:
            lon += 360.0
        
        for i in range(12):
            if normalized[i] <= lon < normalized[i + 1]:
                return i + 1
        return 0
    
    def _calculate_julian_day(self, person: PersonInput) -> float:
        """Calculate Julian day for a person's birth data."""
        # Parse date
        date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
        
        # Handle time
        if person.birth_time and not person.time_unknown:
            hh, mm = [int(x) for x in person.birth_time.split(":")]
            # Assume Vietnam timezone (+7:00) for now
            local_tz = timezone(timedelta(hours=7))
            local_dt = datetime(date_obj.year, date_obj.month, date_obj.day, hh, mm, 0, tzinfo=local_tz)
            utc_dt = local_dt.astimezone(timezone.utc)
        else:
            # Use noon if time unknown
            utc_dt = datetime(date_obj.year, date_obj.month, date_obj.day, 12, 0, 0, tzinfo=timezone.utc)
        
        # Calculate Julian day
        return swe.julday(
            utc_dt.year,
            utc_dt.month,
            utc_dt.day,
            utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0,
        )
    
    def _calculate_planets(self, jd: float) -> List[PlanetData]:
        """Calculate planet positions."""
        planets = []
        
        for planet_name, planet_id in self.PLANET_CONSTANTS.items():
            try:
                result = swe.calc_ut(jd, planet_id)
                if isinstance(result[0], (list, tuple)) and len(result[0]) >= 6:
                    longitude = float(result[0][0])
                    latitude = float(result[0][1])
                    speed = float(result[0][3])
                    
                    sign = self._get_sign_from_longitude(longitude)
                    degree = self._get_degree_from_longitude(longitude)
                    
                    planet_data = PlanetData(
                        name=planet_name,
                        longitude=longitude,
                        latitude=latitude,
                        speed=speed,
                        sign=sign,
                        degree=degree,
                        house=0  # Will be calculated later
                    )
                    planets.append(planet_data)
            except Exception as e:
                # Skip planets that can't be calculated
                continue
        
        return planets
    
    def _calculate_houses(self, jd: float, lat: float, lon: float) -> List[float]:
        """Calculate house cusps."""
        try:
            houses_result = swe.houses(jd, float(lat), float(lon), self.HOUSE_SYSTEM)
            return [float(houses_result[0][i]) for i in range(12)]
        except Exception:
            return []
    
    def _calculate_aspects(self, planets: List[PlanetData], orb: float = 6.0) -> List[AspectData]:
        """Calculate aspects between planets."""
        aspects = []
        
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                p1 = planets[i]
                p2 = planets[j]
                
                # Calculate angular distance with normalization
                # angle = abs(long1 - long2)
                # if angle > 180: angle = 360 - angle
                raw_diff = abs(p1.longitude - p2.longitude)
                diff = raw_diff if raw_diff <= 180.0 else 360.0 - raw_diff
                
                logger.info(f"Checking aspect: {p1.name} and {p2.name}, angle: {diff:.2f}°")
                
                # Check for aspects
                found_for_pair = False
                for aspect_type, angle in self.ASPECT_ANGLES.items():
                    d = abs(diff - angle)
                    if d <= orb:
                        logger.info(f"Found aspect: {p1.name} {aspect_type} {p2.name} (orb: {d:.2f}°)")
                        aspect = AspectData(
                            planet_a=p1.name,
                            planet_b=p2.name,
                            aspect_type=aspect_type,
                            orb=round(float(d), 2)
                        )
                        aspects.append(aspect)
                        found_for_pair = True
                        break
                
                # Debugging trine specifically if not found
                if not found_for_pair:
                    trine_angle = self.ASPECT_ANGLES.get("trine", 120.0)
                    trine_d = abs(diff - trine_angle)
                    if trine_d <= 8.0:  # Temp increase to 8 for debugging
                        logger.debug(f"DEBUG: Near-miss trine between {p1.name} and {p2.name}: {diff:.2f}° (orb: {trine_d:.2f}°, limit: {orb})")
        
        return aspects
    
    def _calculate_house_positions(self, planets: List[PlanetData], cusps: List[float]) -> List[PlanetData]:
        """Calculate house positions for planets."""
        if not cusps:
            return planets
        
        updated_planets = []
        for planet in planets:
            house = self._get_house_for_longitude(planet.longitude, cusps)
            updated_planet = PlanetData(
                name=planet.name,
                longitude=planet.longitude,
                latitude=planet.latitude,
                speed=planet.speed,
                sign=planet.sign,
                degree=planet.degree,
                house=house
            )
            updated_planets.append(updated_planet)
        
        return updated_planets
    
    def build_natal_chart(self, person: PersonInput, lat: float, lon: float) -> ChartData:
        """Build complete natal chart for a person."""
        # Calculate Julian day
        jd = self._calculate_julian_day(person)
        
        # Calculate planets
        planets = self._calculate_planets(jd)
        
        # Calculate houses
        cusps = self._calculate_houses(jd, lat, lon)
        
        # Calculate aspects
        aspects = self._calculate_aspects(planets)
        
        # Calculate house positions
        planets_with_houses = self._calculate_house_positions(planets, cusps)
        
        # Get key signs
        sun_sign = next((p.sign for p in planets_with_houses if p.name == "Sun"), "Unknown")
        moon_sign = next((p.sign for p in planets_with_houses if p.name == "Moon"), "Unknown")
        ascendant = self._get_sign_from_longitude(cusps[0]) if cusps else "Unknown"
        
        return ChartData(
            sun_sign=sun_sign,
            moon_sign=moon_sign,
            ascendant=ascendant,
            planets=planets_with_houses,
            houses=cusps,
            aspects=aspects
        )
    
    def calculate_compatibility_aspects(self, chart_a: ChartData, chart_b: ChartData) -> List[AspectData]:
        """Calculate compatibility aspects between two charts."""
        aspects = []
        
        # Get planet positions from both charts
        planets_a = {p.name: p for p in chart_a.planets}
        planets_b = {p.name: p for p in chart_b.planets}
        
        # Calculate cross-chart aspects
        major_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
        
        for planet_a_name in major_planets:
            for planet_b_name in major_planets:
                if planet_a_name in planets_a and planet_b_name in planets_b:
                    lon_a = planets_a[planet_a_name].longitude
                    lon_b = planets_b[planet_b_name].longitude
                    
                    # Calculate angular distance with normalization
                    raw_diff = abs(lon_a - lon_b)
                    diff = raw_diff if raw_diff <= 180.0 else 360.0 - raw_diff
                    
                    logger.info(f"Checking cross-chart aspect: {planet_a_name} (A) and {planet_b_name} (B), angle: {diff:.2f}°")
                    
                    found_for_pair = False
                    for aspect_type, angle in self.ASPECT_ANGLES.items():
                        orb_val = abs(diff - angle)
                        if orb_val <= 6.0:  # Standard orb
                            logger.info(f"Found cross-chart aspect: {planet_a_name} {aspect_type} {planet_b_name} (orb: {orb_val:.2f}°)")
                            aspect = AspectData(
                                planet_a=planet_a_name,
                                planet_b=planet_b_name,
                                aspect_type=aspect_type,
                                orb=round(orb_val, 2)
                            )
                            aspects.append(aspect)
                            found_for_pair = True
                            break
                    
                    # Debugging trine specifically if not found
                    if not found_for_pair:
                        trine_angle = self.ASPECT_ANGLES.get("trine", 120.0)
                        trine_d = abs(diff - trine_angle)
                        if trine_d <= 8.0:
                            logger.debug(f"DEBUG: Near-miss cross-chart trine between {planet_a_name} and {planet_b_name}: {diff:.2f}° (orb: {trine_d:.2f}°, limit: 6.0)")
        
        return aspects
    
    def calculate_compatibility_scores(self, aspects: List[AspectData]) -> Dict[str, int]:
        """Calculate compatibility scores based on aspects."""
        # Aspect weights
        HARMONIOUS_ASPECTS = {"trine", "sextile", "conjunction"}
        CHALLENGING_ASPECTS = {"square", "opposition"}
        
        # Planet pairs for different compatibility areas
        EMOTIONAL_PAIRS = [
            ("Moon", "Moon"), ("Moon", "Venus"), ("Venus", "Moon"),
            ("Sun", "Moon"), ("Moon", "Sun")
        ]
        PHYSICAL_PAIRS = [
            ("Mars", "Venus"), ("Venus", "Mars"), ("Mars", "Mars"), ("Sun", "Mars")
        ]
        MENTAL_PAIRS = [
            ("Mercury", "Mercury"), ("Mercury", "Sun"), ("Sun", "Mercury"), ("Jupiter", "Mercury")
        ]
        STABILITY_PAIRS = [
            ("Saturn", "Sun"), ("Saturn", "Moon"), ("Saturn", "Venus"), ("Jupiter", "Sun")
        ]
        
        def calculate_area_score(planet_pairs: List[Tuple[str, str]]) -> int:
            score = 50  # Base score
            
            for aspect in aspects:
                pair = (aspect.planet_a, aspect.planet_b)
                reverse_pair = (aspect.planet_b, aspect.planet_a)
                
                if pair in planet_pairs or reverse_pair in planet_pairs:
                    aspect_type = aspect.aspect_type.lower()
                    
                    if aspect_type in HARMONIOUS_ASPECTS:
                        if aspect_type == "trine":
                            score += 15
                        elif aspect_type == "sextile":
                            score += 12
                        elif aspect_type == "conjunction":
                            score += 10
                    elif aspect_type in CHALLENGING_ASPECTS:
                        if aspect_type == "square":
                            score -= 10
                        elif aspect_type == "opposition":
                            score -= 8
            
            return max(0, min(100, score))
        
        def calculate_conflict_score() -> int:
            base_conflict = 20
            
            for aspect in aspects:
                aspect_type = aspect.aspect_type.lower()
                
                if aspect_type in CHALLENGING_ASPECTS:
                    base_conflict += 10
                elif aspect_type == "conjunction":
                    base_conflict += 5
            
            return max(0, min(100, base_conflict))
        
        # Calculate scores
        emotional = calculate_area_score(EMOTIONAL_PAIRS)
        physical = calculate_area_score(PHYSICAL_PAIRS)
        mental = calculate_area_score(MENTAL_PAIRS)
        stability = calculate_area_score(STABILITY_PAIRS)
        conflict = calculate_conflict_score()
        
        # Calculate derived scores
        long_term = round(
            stability * 0.4 +
            emotional * 0.3 +
            mental * 0.2 +
            (100 - conflict) * 0.1
        )
        
        overall = round(
            emotional * 0.25 +
            physical * 0.20 +
            mental * 0.15 +
            stability * 0.20 +
            long_term * 0.20
        )
        
        return {
            "overall_score": max(0, min(100, overall)),
            "emotional_compatibility": max(0, min(100, emotional)),
            "mental_compatibility": max(0, min(100, mental)),
            "physical_chemistry": max(0, min(100, physical)),
            "stability_score": max(0, min(100, stability)),
            "conflict_risk": max(0, min(100, conflict)),
            "long_term_potential": max(0, min(100, long_term))
        }