"""
natal_micro_service.py
----------------------
Zero-500 architecture for natal chart AI interpretation.

Key principles:
- 4 micro-calls (small, stable JSON)
- Ultra-strict prompts (anti-duplicate, anti-markdown)
- Retry + auto-fix layer
- Validation before merge
- Fallback never returns 500
- ~40% token optimization
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

from services.ai_service import AIService

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Groq configuration (optimized for free tier)
# ---------------------------------------------------------------------------
GROQ_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.8,
    "max_tokens": 700,  # Never exceed 800
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
}

# ---------------------------------------------------------------------------
# SYSTEM PROMPTS (Ultra-strict, anti-duplicate, anti-markdown)
# ---------------------------------------------------------------------------

SYSTEM_IDENTITY = """You are a deterministic JSON generator.

CRITICAL RULES:
- Output ONLY valid JSON.
- No markdown.
- No backticks.
- No explanation.
- No duplicate keys.
- No comments.
- Stop immediately if structure breaks.
- If duplicate key appears, return {"error":"DUPLICATE_KEY"}."""

SYSTEM_PLANETS = """Strict JSON generator.

Rules:
- Output ONLY valid JSON.
- No markdown.
- No explanation.
- No duplicate planet.
- Max 10 planets.
- Stop if structure breaks."""

SYSTEM_ASPECTS = """Strict JSON generator.

Rules:
- Output ONLY JSON.
- Max 8 aspects.
- No duplicate pair.
- intensity integer 1–10.
- Stop if key repeats."""

SYSTEM_NARRATIVE = """Strict JSON generator.

Rules:
- Output ONLY JSON.
- No line breaks inside values.
- Max 2 sentences per field.
- No markdown.
- No extra keys."""

# ---------------------------------------------------------------------------
# USER PROMPTS (Token-optimized)
# ---------------------------------------------------------------------------

def build_identity_prompt(sun: str, moon: str, rising: str, element: str) -> str:
    return f"""Return EXACTLY this JSON schema:

{{
  "sun_sign": "{sun}",
  "moon_sign": "{moon}",
  "rising_sign": "{rising}",
  "dominant_element": "{element}",
  "emotional_intensity": 0
}}

Rules:
- emotional_intensity must be integer 1–10.
- All fields required.
- Return ONLY the JSON object above with values filled in."""


def build_planets_prompt(planets_data: list[dict]) -> str:
    planets_json = json.dumps(planets_data[:10], ensure_ascii=False)
    return f"""Return EXACTLY:

{{
  "planets": {planets_json}
}}

Rules:
- house must be integer 1–12.
- Max 10 items.
- No extra fields.
- Return ONLY the JSON above."""


def build_aspects_prompt(aspects_data: list[dict]) -> str:
    aspects_json = json.dumps(aspects_data[:8], ensure_ascii=False)
    return f"""Return EXACTLY:

{{
  "aspects": {aspects_json}
}}

Rules:
- intensity must be integer 1–10.
- Max 8 items.
- Return ONLY the JSON above."""


def build_narrative_prompt(sun: str, moon: str, rising: str) -> str:
    return f"""Return EXACTLY:

{{
  "core_personality": "string",
  "emotional_pattern": "string",
  "life_theme": "string",
  "shadow_side": "string",
  "growth_direction": "string"
}}

Context: Sun={sun}, Moon={moon}, Rising={rising}

Rules:
- Each field: max 2 sentences.
- Be direct and insightful.
- No generic positivity.
- Return ONLY the JSON above with values filled in."""


# ---------------------------------------------------------------------------
# SAFE JSON PARSER (Auto-fix common issues)
# ---------------------------------------------------------------------------

def safe_parse(text: str) -> Optional[dict]:
    """Parse JSON with auto-fix for common LLM output issues."""
    if not text:
        return None
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Auto-fix common issues
    fixed = text.strip()
    
    # Remove markdown fences
    fixed = fixed.replace("```json", "").replace("```", "")
    fixed = fixed.strip()
    
    # Remove trailing commas
    fixed = re.sub(r",\s*}", "}", fixed)
    fixed = re.sub(r",\s*]", "]", fixed)
    
    # Remove comments
    fixed = re.sub(r"//.*$", "", fixed, flags=re.MULTILINE)
    fixed = re.sub(r"/\*.*?\*/", "", fixed, flags=re.DOTALL)
    
    # Fix unquoted keys
    fixed = re.sub(r'(\w+)(?=\s*:)', r'"\1"', fixed)
    
    # Fix single quotes to double quotes
    fixed = fixed.replace("'", '"')
    
    try:
        return json.loads(fixed)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse failed after auto-fix: {e}")
        return None


# ---------------------------------------------------------------------------
# SCHEMA VALIDATION
# ---------------------------------------------------------------------------

def validate_identity(data: dict) -> bool:
    required = [
        "sun_sign",
        "moon_sign", 
        "rising_sign",
        "dominant_element",
        "emotional_intensity"
    ]
    if not all(k in data for k in required):
        return False
    # Validate emotional_intensity is int 1-10
    ei = data.get("emotional_intensity")
    if not isinstance(ei, int) or ei < 1 or ei > 10:
        data["emotional_intensity"] = 5  # Auto-fix
    return True


def validate_planets(data: dict) -> bool:
    if "planets" not in data:
        return False
    if not isinstance(data["planets"], list):
        return False
    if len(data["planets"]) > 10:
        data["planets"] = data["planets"][:10]  # Truncate
    for p in data["planets"]:
        if not all(k in p for k in ["planet", "sign", "house"]):
            return False
        if not isinstance(p.get("house"), int):
            p["house"] = 1  # Auto-fix
    return True


def validate_aspects(data: dict) -> bool:
    if "aspects" not in data:
        return False
    if not isinstance(data["aspects"], list):
        return False
    if len(data["aspects"]) > 8:
        data["aspects"] = data["aspects"][:8]  # Truncate
    for a in data["aspects"]:
        if not all(k in a for k in ["planet_1", "planet_2", "aspect_type"]):
            return False
        if "intensity" not in a or not isinstance(a.get("intensity"), int):
            a["intensity"] = 5  # Auto-fix
    return True


def validate_narrative(data: dict) -> bool:
    required = [
        "core_personality",
        "emotional_pattern",
        "life_theme",
        "shadow_side",
        "growth_direction"
    ]
    return all(k in data for k in required)


# ---------------------------------------------------------------------------
# FALLBACK DATA (Never returns 500)
# ---------------------------------------------------------------------------

def fallback_identity() -> dict:
    return {
        "sun_sign": "Unknown",
        "moon_sign": "Unknown",
        "rising_sign": "Unknown",
        "dominant_element": "Mixed",
        "emotional_intensity": 5
    }


def fallback_planets() -> dict:
    return {
        "planets": [
            {"planet": "Sun", "sign": "Unknown", "house": 1},
            {"planet": "Moon", "sign": "Unknown", "house": 4},
        ]
    }


def fallback_aspects() -> dict:
    return {
        "aspects": []
    }


def fallback_narrative() -> dict:
    return {
        "core_personality": "Profile temporarily simplified.",
        "emotional_pattern": "Emotional data unavailable.",
        "life_theme": "Theme calculation pending.",
        "shadow_side": "Shadow insight unavailable.",
        "growth_direction": "Growth insight pending."
    }


# ---------------------------------------------------------------------------
# RETRY WRAPPER (Max 1 retry)
# ---------------------------------------------------------------------------

async def call_with_retry(
    ai_service: AIService,
    system_prompt: str,
    user_prompt: str,
    validator: callable,
    fallback: callable,
) -> dict:
    """Call Groq API with retry and auto-fix logic."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    for attempt in range(2):  # Max 2 attempts
        try:
            raw = await ai_service.create_chat_completion(
                messages=messages,
                temperature=GROQ_CONFIG["temperature"],
                max_tokens=GROQ_CONFIG["max_tokens"],
            )
            
            parsed = safe_parse(raw)
            
            if parsed is None:
                logger.warning(f"Attempt {attempt + 1}: JSON parse failed")
                continue
            
            if "error" in parsed:
                logger.warning(f"Attempt {attempt + 1}: LLM returned error: {parsed}")
                continue
            
            if validator(parsed):
                return parsed
            else:
                logger.warning(f"Attempt {attempt + 1}: Validation failed")
                
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: API call failed: {e}")
    
    # All attempts failed, return fallback
    logger.warning("All attempts failed, using fallback")
    return fallback()


# ---------------------------------------------------------------------------
# MAIN SERVICE CLASS
# ---------------------------------------------------------------------------

class NatalMicroService:
    """Zero-500 natal chart interpretation service."""
    
    def __init__(self, api_key: str, base_url: str, model: str, timeout: float = 60.0):
        self.ai_service = AIService(
            api_key,
            base_url=base_url,
            model=model,
            timeout_seconds=timeout,
        )
    
    async def generate_natal_interpretation(
        self,
        sun: str,
        moon: str,
        rising: str,
        element: str,
        planets_data: list[dict],
        aspects_data: list[dict],
    ) -> dict:
        """Generate natal interpretation using 4 micro-calls.
        
        Never returns 500 - always returns valid JSON.
        """
        results = {}
        
        # Call 1: Identity Core
        try:
            identity = await call_with_retry(
                self.ai_service,
                SYSTEM_IDENTITY,
                build_identity_prompt(sun, moon, rising, element),
                validate_identity,
                fallback_identity,
            )
            results["identity"] = identity
        except Exception as e:
            logger.error(f"Identity call failed: {e}")
            results["identity"] = fallback_identity()
        
        # Call 2: Planetary Positions
        try:
            planets = await call_with_retry(
                self.ai_service,
                SYSTEM_PLANETS,
                build_planets_prompt(planets_data),
                validate_planets,
                fallback_planets,
            )
            results["planets"] = planets
        except Exception as e:
            logger.error(f"Planets call failed: {e}")
            results["planets"] = fallback_planets()
        
        # Call 3: Aspects
        try:
            aspects = await call_with_retry(
                self.ai_service,
                SYSTEM_ASPECTS,
                build_aspects_prompt(aspects_data),
                validate_aspects,
                fallback_aspects,
            )
            results["aspects"] = aspects
        except Exception as e:
            logger.error(f"Aspects call failed: {e}")
            results["aspects"] = fallback_aspects()
        
        # Call 4: Narrative
        try:
            narrative = await call_with_retry(
                self.ai_service,
                SYSTEM_NARRATIVE,
                build_narrative_prompt(sun, moon, rising),
                validate_narrative,
                fallback_narrative,
            )
            results["narrative"] = narrative
        except Exception as e:
            logger.error(f"Narrative call failed: {e}")
            results["narrative"] = fallback_narrative()
        
        # Merge results
        final = self._merge_results(results)
        
        # Final validation
        return self._final_validate(final)
    
    def _merge_results(self, results: dict) -> dict:
        """Merge 4 micro-call results into final structure."""
        identity = results.get("identity", fallback_identity())
        planets = results.get("planets", fallback_planets())
        aspects = results.get("aspects", fallback_aspects())
        narrative = results.get("narrative", fallback_narrative())
        
        return {
            "core_identity": {
                "sun_sign": {
                    "sign": identity.get("sun_sign", "Unknown"),
                    "house": 1,
                    "interpretation": narrative.get("core_personality", ""),
                },
                "moon_sign": {
                    "sign": identity.get("moon_sign", "Unknown"),
                    "house": 4,
                    "interpretation": narrative.get("emotional_pattern", ""),
                },
                "rising_sign": {
                    "sign": identity.get("rising_sign", "Unknown"),
                    "interpretation": narrative.get("life_theme", ""),
                },
                "summary": narrative.get("core_personality", ""),
            },
            "planets": planets.get("planets", []),
            "aspects": [
                {
                    "planet_1": a.get("planet_1", ""),
                    "planet_2": a.get("planet_2", ""),
                    "aspect_type": a.get("aspect_type", ""),
                    "interpretation": f"Intensity: {a.get('intensity', 5)}/10",
                }
                for a in aspects.get("aspects", [])
            ],
            "love_profile": {
                "attachment_style": "Complex",
                "strengths": narrative.get("emotional_pattern", ""),
                "challenges": narrative.get("shadow_side", ""),
                "advice": narrative.get("growth_direction", ""),
            },
            "career_analysis": {
                "best_fields": "Various opportunities available",
                "work_style": narrative.get("core_personality", ""),
                "growth_advice": narrative.get("growth_direction", ""),
            },
            "psychological_pattern": {
                "core_wound": narrative.get("shadow_side", ""),
                "healing_direction": narrative.get("growth_direction", ""),
            },
            "practical_guidance": {
                "career": narrative.get("growth_direction", ""),
                "relationships": narrative.get("emotional_pattern", ""),
                "self_development": narrative.get("life_theme", ""),
            },
        }
    
    def _final_validate(self, data: dict) -> dict:
        """Final validation and cleanup."""
        # Ensure all required keys exist
        required_keys = [
            "core_identity",
            "planets",
            "aspects",
            "love_profile",
            "career_analysis",
            "psychological_pattern",
            "practical_guidance",
        ]
        
        for key in required_keys:
            if key not in data:
                data[key] = {}
        
        # Ensure planets is a list
        if not isinstance(data.get("planets"), list):
            data["planets"] = []
        
        # Ensure aspects is a list
        if not isinstance(data.get("aspects"), list):
            data["aspects"] = []
        
        # Limit sizes
        data["planets"] = data["planets"][:10]
        data["aspects"] = data["aspects"][:8]
        
        return data