#!/usr/bin/env python3
"""
Final verification test for the complete Zodiac AI system.
Tests all components and verifies the architecture works correctly.
"""

import asyncio
import json
import logging
import os
from datetime import datetime

from core.config import settings
from services.ai.ai_service import AIService
from services.ai.groq_client import GroqClient
from services.ai.prompts import NatalPrompts, CompatibilityPrompts
from services.natal_service_new import get_natal_service_new
from services.compatibility_service_new import get_compatibility_service_new
from services.astrology_engine import PersonInput
from services.geocoding_service import OpenCageService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_groq_client():
    """Test Groq client directly"""
    print("🧪 Testing Groq Client...")
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not configured")
        return False
    
    try:
        client = GroqClient(settings.GROQ_API_KEY)
        
        # Test simple JSON generation
        result = await client.generate_json(
            "Return a simple JSON object with a greeting: {\"message\": \"Hello World\"}",
            "test_groq_client"
        )
        
        if result and isinstance(result, dict) and "message" in result:
            print("✅ Groq Client test passed")
            return True
        else:
            print(f"❌ Groq Client test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Groq Client test failed: {e}")
        return False


async def test_ai_service():
    """Test AI service with clean architecture"""
    print("🧪 Testing AI Service...")
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not configured")
        return False
    
    try:
        ai_service = AIService(settings.GROQ_API_KEY)
        
        # Test natal interpretation
        result = await ai_service.generate_natal_interpretations(
            person_name="Test User",
            person_birth_date="1990-01-01",
            person_birth_time="12:00:00",
            person_birth_place="Ho Chi Minh City, Vietnam",
            planets_data=[
                {"planet": "Sun", "sign": "Aries", "longitude": 45.5, "degree": 15.5, "house": 1, "retrograde": False},
                {"planet": "Moon", "sign": "Taurus", "longitude": 90.2, "degree": 0.2, "house": 2, "retrograde": False}
            ],
            aspects_data=[
                {"aspect_type": "trine", "planet_1": "Sun", "planet_2": "Moon", "orb": 2.5}
            ],
            request_id="test_natal"
        )
        
        if result and isinstance(result, dict):
            print("✅ AI Service natal test passed")
            
            # Test compatibility analysis
            compat_result = await ai_service.generate_compatibility_analysis(
                person_a={"sun": "Aries", "moon": "Taurus", "venus": "Gemini"},
                person_b={"sun": "Leo", "moon": "Cancer", "venus": "Virgo"},
                aspects=["trine", "square"],
                fallback_mode=False,
                request_id="test_compat"
            )
            
            if compat_result and isinstance(compat_result, dict):
                print("✅ AI Service compatibility test passed")
                return True
            else:
                print(f"❌ AI Service compatibility test failed: {compat_result}")
                return False
        else:
            print(f"❌ AI Service natal test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ AI Service test failed: {e}")
        return False


async def test_natal_service():
    """Test new natal service architecture"""
    print("🧪 Testing Natal Service...")
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not configured")
        return False
    
    try:
        service = get_natal_service_new(settings.GROQ_API_KEY)
        
        person = PersonInput(
            date="1990-01-01",
            time="12:00:00",
            city="Ho Chi Minh City",
            country="Vietnam",
            name="Test User"
        )
        
        result = await service.analyze(person, lat=10.8231, lon=106.6297, request_id="test_natal_service")
        
        if result and hasattr(result, 'meta') and hasattr(result, 'astrology_ai'):
            print("✅ Natal Service test passed")
            return True
        else:
            print(f"❌ Natal Service test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Natal Service test failed: {e}")
        return False


async def test_compatibility_service():
    """Test new compatibility service architecture"""
    print("🧪 Testing Compatibility Service...")
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not configured")
        return False
    
    try:
        service = get_compatibility_service_new(settings.GROQ_API_KEY)
        
        person_a = PersonInput(
            date="1990-01-01",
            time="12:00:00",
            city="Ho Chi Minh City",
            country="Vietnam",
            name="Person A"
        )
        
        person_b = PersonInput(
            date="1992-05-15",
            time="18:30:00",
            city="Hanoi",
            country="Vietnam",
            name="Person B"
        )
        
        result = await service.analyze(
            person_a=person_a,
            person_b=person_b,
            lat_a=10.8231,
            lon_a=106.6297,
            lat_b=21.0285,
            lon_b=105.8542,
            request_id="test_compat_service"
        )
        
        if result and hasattr(result, 'overall_score'):
            print("✅ Compatibility Service test passed")
            return True
        else:
            print(f"❌ Compatibility Service test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Compatibility Service test failed: {e}")
        return False


async def test_prompt_templates():
    """Test prompt templates"""
    print("🧪 Testing Prompt Templates...")
    
    try:
        # Test natal prompt
        natal_prompt = NatalPrompts.build_user_prompt(
            person_name="Test User",
            person_birth_date="1990-01-01",
            person_birth_time="12:00:00",
            person_birth_place="Ho Chi Minh City, Vietnam",
            planets_data=[
                {"planet": "Sun", "sign": "Aries", "longitude": 45.5, "degree": 15.5, "house": 1, "retrograde": False}
            ],
            aspects_data=[
                {"aspect_type": "trine", "planet_1": "Sun", "planet_2": "Moon", "orb": 2.5}
            ]
        )
        
        if natal_prompt and "Test User" in natal_prompt:
            print("✅ Natal prompt template test passed")
            
            # Test compatibility prompt
            compat_prompt = CompatibilityPrompts.build_user_prompt(
                person_a={"sun": "Aries", "moon": "Taurus"},
                person_b={"sun": "Leo", "moon": "Cancer"},
                aspects=["trine", "square"],
                fallback_mode=False
            )
            
            if compat_prompt and "Aries" in compat_prompt:
                print("✅ Compatibility prompt template test passed")
                return True
            else:
                print("❌ Compatibility prompt template test failed")
                return False
        else:
            print("❌ Natal prompt template test failed")
            return False
            
    except Exception as e:
        print(f"❌ Prompt template test failed: {e}")
        return False


async def test_geocoding():
    """Test geocoding service"""
    print("🧪 Testing Geocoding Service...")
    
    try:
        geocoder = OpenCageService(settings.OPENCAGE_API_KEY)
        
        result = geocoder.geocode("Ho Chi Minh City, Vietnam")
        
        if result and 'lat' in result and 'lon' in result:
            print("✅ Geocoding test passed")
            return True
        else:
            print(f"❌ Geocoding test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Geocoding test failed: {e}")
        return False


async def test_full_integration():
    """Test full integration with real data"""
    print("🧪 Testing Full Integration...")
    
    if not settings.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not configured - skipping integration test")
        return True  # Don't fail if API key not configured
    
    try:
        # Test natal chart generation
        service = get_natal_service_new(settings.GROQ_API_KEY)
        
        person = PersonInput(
            date="1990-01-01",
            time="12:00:00",
            city="Ho Chi Minh City",
            country="Vietnam",
            name="Integration Test User"
        )
        
        result = await service.analyze(person, lat=10.8231, lon=106.6297, request_id="integration_test")
        
        if result and hasattr(result, 'meta') and hasattr(result, 'astrology_ai'):
            print("✅ Full integration test passed")
            
            # Verify structure
            meta = result.meta
            astrology_ai = result.astrology_ai
            
            required_fields = ['name', 'birth_date', 'birth_time', 'birth_place', 'lat', 'lon']
            for field in required_fields:
                if not hasattr(meta, field):
                    print(f"❌ Missing required field in meta: {field}")
                    return False
            
            # Verify astrology_ai structure
            required_ai_fields = ['core_identity', 'love_profile', 'career_analysis', 'psychological_pattern', 'practical_guidance']
            for field in required_ai_fields:
                if not hasattr(astrology_ai, field):
                    print(f"❌ Missing required field in astrology_ai: {field}")
                    return False
            
            print("✅ All required fields present in integration test")
            return True
        else:
            print(f"❌ Full integration test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Full integration test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Starting Final Verification Tests...")
    print("=" * 50)
    
    tests = [
        ("Groq Client", test_groq_client),
        ("AI Service", test_ai_service),
        ("Natal Service", test_natal_service),
        ("Compatibility Service", test_compatibility_service),
        ("Prompt Templates", test_prompt_templates),
        ("Geocoding", test_geocoding),
        ("Full Integration", test_full_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} | {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for production.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)