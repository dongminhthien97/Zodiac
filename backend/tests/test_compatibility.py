"""
tests/test_compatibility.py
---------------------------
Unit tests for the CompatibilityService.

Run with:
    cd d:/Zodiac/backend
    python -m pytest tests/test_compatibility.py -v

Or on Windows PowerShell:
    cd d:/Zodiac/backend; python -m pytest tests/test_compatibility.py -v
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.compatibility_service import (
    CompatibilityService,
    PersonInput,
    AspectData,
    ScoreEngine,
    CompatibilityScores,
    safe_parse_json,
    get_fallback_response,
)


class TestScoreEngine:
    """Test the deterministic ScoreEngine."""
    
    def test_empty_aspects(self):
        """Test scoring with no aspects."""
        engine = ScoreEngine([])
        scores = engine.calculate()
        
        assert scores.overall_score == 50
        assert scores.emotional_compatibility == 50
        assert scores.mental_compatibility == 50
        assert scores.physical_chemistry == 50
        assert scores.stability_score == 50
        assert scores.conflict_risk == 20
        assert scores.long_term_potential == 50
    
    def test_harmonious_aspects(self):
        """Test scoring with harmonious aspects."""
        aspects = [
            AspectData(planet_a="Moon", planet_b="Moon", aspect_type="trine", orb=2.0),
            AspectData(planet_a="Venus", planet_b="Mars", aspect_type="sextile", orb=3.0),
        ]
        engine = ScoreEngine(aspects)
        scores = engine.calculate()
        
        # Should have higher emotional due to Moon-Moon trine
        assert scores.emotional_compatibility > 50
        # Should have higher physical due to Venus-Mars sextile
        assert scores.physical_chemistry > 50
    
    def test_challenging_aspects(self):
        """Test scoring with challenging aspects."""
        aspects = [
            AspectData(planet_a="Moon", planet_b="Moon", aspect_type="square", orb=2.0),
            AspectData(planet_a="Mars", planet_b="Venus", aspect_type="opposition", orb=3.0),
        ]
        engine = ScoreEngine(aspects)
        scores = engine.calculate()
        
        # Should have lower emotional due to Moon-Moon square
        assert scores.emotional_compatibility < 50
        # Should have higher conflict risk
        assert scores.conflict_risk > 20


class TestSafeParseJson:
    """Test the safe JSON parser."""
    
    def test_valid_json(self):
        """Test parsing valid JSON."""
        result = safe_parse_json('{"key": "value"}')
        assert result == {"key": "value"}
    
    def test_json_with_markdown(self):
        """Test parsing JSON with markdown fences."""
        result = safe_parse_json('```json\n{"key": "value"}\n```')
        assert result == {"key": "value"}
    
    def test_json_with_trailing_commas(self):
        """Test parsing JSON with trailing commas."""
        result = safe_parse_json('{"key": "value",}')
        assert result == {"key": "value"}
    
    def test_extract_json_from_text(self):
        """Test extracting JSON from surrounding text."""
        result = safe_parse_json('Some text before {"key": "value"} some text after')
        assert result == {"key": "value"}
    
    def test_invalid_json_returns_none(self):
        """Test that invalid JSON returns None."""
        result = safe_parse_json('not json at all')
        assert result is None


class TestFallbackResponse:
    """Test fallback response generation."""
    
    def test_default_fallback(self):
        """Test default fallback response."""
        response = get_fallback_response()
        
        assert "score" in response
        assert "summary" in response
        assert "personality" in response
        assert "love_style" in response
        assert "advice" in response
        assert response["score"] == 50
    
    def test_fallback_with_scores(self):
        """Test fallback with custom scores."""
        scores = CompatibilityScores(
            overall_score=75,
            emotional_compatibility=80,
            mental_compatibility=70,
            physical_chemistry=85,
            stability_score=65,
            conflict_risk=30,
            long_term_potential=72
        )
        response = get_fallback_response(scores)
        
        assert response["score"] == 75


class TestPersonInput:
    """Test PersonInput dataclass."""
    
    def test_person_input_creation(self):
        """Test creating PersonInput."""
        person = PersonInput(
            date="1990-01-15",
            time="10:30",
            city="Ho Chi Minh",
            country="Vietnam",
            name="Test User"
        )
        
        assert person.date == "1990-01-15"
        assert person.time == "10:30"
        assert person.city == "Ho Chi Minh"
        assert person.country == "Vietnam"
        assert person.name == "Test User"
    
    def test_person_input_optional_time(self):
        """Test PersonInput with no time."""
        person = PersonInput(
            date="1990-01-15",
            time=None,
            city="Ho Chi Minh",
            country="Vietnam"
        )
        
        assert person.time is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])