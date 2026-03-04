import pytest
from services.natal_transformers import NatalTransformer
from services.astrology_engine import ChartData, PlanetData, AspectData
from services.astrology_service import BirthInfo

def test_transformer_key_mapping():
    transformer = NatalTransformer()
    
    # Mock chart data
    chart = ChartData(
        sun_sign="Aries",
        moon_sign="Taurus",
        ascendant="Gemini",
        planets=[
            PlanetData(name="Sun", longitude=0, latitude=0, speed=1, sign="Aries", degree=0, house=1),
            PlanetData(name="Moon", longitude=30, latitude=0, speed=1, sign="Taurus", degree=0, house=2)
        ],
        houses=[0]*12,
        aspects=[
            AspectData(planet_a="Sun", planet_b="Moon", aspect_type="sextile", orb=0.0)
        ]
    )
    
    # AI interpretations with the NEW keys
    ai_result = {
        "planet_interpretations": [
            {"planet": "Sun", "interpretation": "Real Sun interpretation"},
            {"planet": "Moon", "interpretation": "Real Moon interpretation"}
        ],
        "aspect_interpretations": [
            {"planet_1": "Sun", "planet_2": "Moon", "aspect_type": "sextile", "interpretation": "Real Aspect interpretation"}
        ]
    }
    
    response = transformer.transform_to_natal_response(
        chart=chart,
        person_name="Test Person",
        person_birth_date="1990-01-01",
        person_birth_time="12:00",
        person_time_unknown=False,
        person_birth_place="Hanoi",
        lat=21.0285,
        lon=105.8542,
        ai_interpretations=ai_result
    )
    
    # Verify planet interpretations
    sun_interp = next(p.interpretation for p in response.planets if p.planet == "Mặt Trời")
    moon_interp = next(p.interpretation for p in response.planets if p.planet == "Mặt Trăng")
    
    assert sun_interp == "Real Sun interpretation"
    assert moon_interp == "Real Moon interpretation"
    
    # Verify aspect interpretation
    aspect_interp = response.aspects[0].interpretation
    assert aspect_interp == "Real Aspect interpretation"
    
    print("SUCCESS: AI interpretations correctly mapped with new keys")

def test_transformer_fallback_keys():
    transformer = NatalTransformer()
    chart = ChartData(
        sun_sign="Aries", moon_sign="Taurus", ascendant="Gemini",
        planets=[PlanetData(name="Sun", longitude=0, latitude=0, speed=1, sign="Aries", degree=0, house=1)],
        houses=[0]*12, aspects=[]
    )
    
    # AI interpretations with the OLD keys (for backward compatibility)
    ai_result = {
        "planets": [{"planet": "Sun", "interpretation": "Fallback Sun interpretation"}]
    }
    
    response = transformer.transform_to_natal_response(
        chart=chart,
        person_name="Test Person",
        person_birth_date="1990-01-01",
        person_birth_time="12:00",
        person_time_unknown=False,
        person_birth_place="Hanoi",
        lat=21.0285,
        lon=105.8542,
        ai_interpretations=ai_result
    )
    sun_interp = next(p.interpretation for p in response.planets if p.planet == "Mặt Trời")
    
    assert sun_interp == "Fallback Sun interpretation"
    print("SUCCESS: AI interpretations correctly mapped with fallback keys")

if __name__ == "__main__":
    test_transformer_key_mapping()
    test_transformer_fallback_keys()
