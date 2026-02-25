from datetime import date, time
from models.schemas import NatalAIPlanet
from services.astrology_engine import PersonInput
from services.natal_transformers import NatalTransformer

def run_tests():
    try:
        planet = NatalAIPlanet(
            planet="Sun",
            sign="Leo",
            house=1,
            retrograde=False,
            interpretation="Test interpretation",
            longitude=120.5,
            degree=0.5
        )
        print("NatalAIPlanet OK")
    except Exception as e:
        print("NatalAIPlanet ERROR:", e)

    try:
        person = PersonInput(
            name="Test Person",
            birth_date="2000-01-01",
            birth_time="12:00",
            birth_place="Hanoi, Vietnam",
            time_unknown=False
        )
        print("PersonInput OK")
    except Exception as e:
        print("PersonInput ERROR:", e)

    try:
        fallback = NatalTransformer.create_fallback_response("Test Person")
        print("Fallback OK")
        print("Planets:", len(fallback.planets))
    except Exception as e:
        print("Fallback ERROR:", e)

if __name__ == "__main__":
    run_tests()