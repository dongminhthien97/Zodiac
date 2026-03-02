
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.astrology_engine import AstrologyEngine, PersonInput, PlanetData

def test_trine_detection():
    engine = AstrologyEngine()
    
    # Create two planets with a 120 degree difference
    p1 = PlanetData(name="Sun", longitude=0.0, latitude=0.0, speed=1.0, sign="Aries", degree=0.0, house=1)
    p2 = PlanetData(name="Moon", longitude=120.0, latitude=0.0, speed=13.0, sign="Leo", degree=0.0, house=5)
    
    planets = [p1, p2]
    
    print("--- Testing _calculate_aspects ---")
    aspects = engine._calculate_aspects(planets, orb=6.0)
    
    found_trine = False
    for aspect in aspects:
        print(f"Detected: {aspect.planet_a} {aspect.aspect_type} {aspect.planet_b} (orb: {aspect.orb})")
        if aspect.aspect_type.lower() == "trine":
            found_trine = True
            
    if not found_trine:
        print("FAILED: Trine not detected between 0° and 120°")
    else:
        print("SUCCESS: Trine detected")

if __name__ == "__main__":
    test_trine_detection()
