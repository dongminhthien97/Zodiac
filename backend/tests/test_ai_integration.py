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


def test_core_identity_uses_ai_core_identity_block_and_real_houses():
    transformer = NatalTransformer()

    chart = ChartData(
        sun_sign="Pisces",
        moon_sign="Aquarius",
        ascendant="Gemini",
        planets=[
            PlanetData(name="Sun", longitude=343.91, latitude=0, speed=1, sign="Pisces", degree=13.91, house=10),
            PlanetData(name="Moon", longitude=320.09, latitude=0, speed=1, sign="Aquarius", degree=20.09, house=9),
        ],
        houses=[0] * 12,
        aspects=[],
    )

    ai_result = {
        "core_identity": {
            "summary": "ignored-by-transformer",
            "sun_sign": "Core Sun interpretation",
            "moon_sign": "Core Moon interpretation",
            "rising_sign": "Core Rising interpretation",
        }
    }

    response = transformer.transform_to_natal_response(
        chart=chart,
        person_name="Test Person",
        person_birth_date="2000-03-04",
        person_birth_time="11:34",
        person_time_unknown=False,
        person_birth_place="Hà Nội, Vietnam",
        lat=21.0285,
        lon=105.8542,
        ai_interpretations=ai_result,
    )

    assert response.core_identity.sun_sign.house == 10
    assert response.core_identity.moon_sign.house == 9
    assert response.core_identity.sun_sign.interpretation == "Core Sun interpretation"
    assert response.core_identity.moon_sign.interpretation == "Core Moon interpretation"
    assert response.core_identity.rising_sign.interpretation == "Core Rising interpretation"


def test_aspect_interpretation_matches_swapped_planet_order():
    transformer = NatalTransformer()

    chart = ChartData(
        sun_sign="Aries",
        moon_sign="Taurus",
        ascendant="Gemini",
        planets=[
            PlanetData(name="Sun", longitude=0, latitude=0, speed=1, sign="Aries", degree=0, house=1),
            PlanetData(name="Moon", longitude=30, latitude=0, speed=1, sign="Taurus", degree=0, house=2),
        ],
        houses=[0] * 12,
        aspects=[AspectData(planet_a="Sun", planet_b="Moon", aspect_type="sextile", orb=0.0)],
    )

    ai_result = {
        "aspect_interpretations": [
            {
                "planet_1": "Moon",
                "planet_2": "Sun",
                "aspect_type": "sextile",
                "interpretation": "Swapped order aspect interpretation",
            }
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
        ai_interpretations=ai_result,
    )

    assert response.aspects[0].interpretation == "Swapped order aspect interpretation"

if __name__ == "__main__":
    test_transformer_key_mapping()
    test_transformer_fallback_keys()
