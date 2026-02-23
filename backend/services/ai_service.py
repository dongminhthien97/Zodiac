"""
services/ai_service.py
----------------------
Production-safe AI service layer for Groq API.

Key guarantees:
- No JSONDecodeError crash
- No unhandled exception
- No HTTP 500 from AI corruption
- Always returns valid structured JSON
- Retry layer (max 2 retries)
- Deterministic fallback JSON
"""
from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 2
REQUEST_TIMEOUT = 60.0
TEMPERATURE = 0.7

# Circuit breaker configuration
CIRCUIT_BREAKER_THRESHOLD = 5
CIRCUIT_BREAKER_RESET_SECONDS = 60.0


# ---------------------------------------------------------------------------
# Circuit Breaker (Optional but Recommended)
# ---------------------------------------------------------------------------

@dataclass
class CircuitBreaker:
    """Simple circuit breaker to prevent cascading failures."""
    failure_count: int = 0
    last_failure_time: float = 0.0
    is_open: bool = False
    
    def record_failure(self) -> None:
        """Record a failure and potentially open the circuit."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= CIRCUIT_BREAKER_THRESHOLD:
            self.is_open = True
            logger.warning("Circuit breaker OPENED after %d failures", self.failure_count)
    
    def record_success(self) -> None:
        """Record a success and reset the circuit."""
        self.failure_count = 0
        self.is_open = False
    
    def should_allow_request(self) -> bool:
        """Check if requests should be allowed."""
        if not self.is_open:
            return True
        
        # Check if reset time has passed
        elapsed = time.time() - self.last_failure_time
        if elapsed >= CIRCUIT_BREAKER_RESET_SECONDS:
            logger.info("Circuit breaker RESET after %.1f seconds", elapsed)
            self.is_open = False
            self.failure_count = 0
            return True
        
        return False


# Global circuit breaker instance
_circuit_breaker = CircuitBreaker()


# ---------------------------------------------------------------------------
# Safe JSON Parser with Repair
# ---------------------------------------------------------------------------

def safe_parse_json(raw_text: str, request_id: Optional[str] = None) -> Optional[dict]:
    """Parse JSON with automatic repair for common LLM output issues.
    
    Args:
        raw_text: Raw text from LLM response
        request_id: Optional request ID for logging
        
    Returns:
        Parsed dict or None if parsing fails
    """
    if not raw_text:
        logger.warning("[%s] Empty raw text received", request_id)
        return None
    
    # First attempt: direct parse
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.debug("[%s] Initial parse failed: %s", request_id, e)
    
    # Clean and repair
    cleaned = raw_text.strip()
    
    # Remove markdown code fences
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()
    
    # Remove trailing commas (common LLM issue)
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*]', ']', cleaned)
    
    # Remove comments
    cleaned = re.sub(r'//.*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    
    # Fix unquoted keys (basic attempt)
    # This regex finds identifier-like strings followed by colon
    cleaned = re.sub(r'(\w+)(?=\s*:)', r'"\1"', cleaned)
    
    # Fix single quotes to double quotes (be careful with apostrophes)
    # Only replace single quotes that look like JSON string delimiters
    cleaned = re.sub(r"(?<!\w)'([^']+)'(?!\w)", r'"\1"', cleaned)
    
    # Second attempt: parse cleaned
    try:
        result = json.loads(cleaned)
        logger.info("[%s] JSON repaired successfully", request_id)
        return result
    except json.JSONDecodeError as e:
        logger.warning(
            "[%s] JSON parse failed after repair: %s. Raw length: %d",
            request_id, e, len(raw_text)
        )
        # Log the malformed JSON for debugging (truncated)
        logger.debug("[%s] Malformed JSON (first 500 chars): %s", request_id, raw_text[:500])
        return None


# ---------------------------------------------------------------------------
# Fallback JSON Structures
# ---------------------------------------------------------------------------

def fallback_natal_response() -> dict:
    """Return fallback natal response that matches FE contract."""
    return {
        "core_identity": {
            "summary": "Your cosmic profile is stabilizing. Please refresh.",
            "sun_sign": {"sign": "Unknown", "house": 1, "interpretation": "Data temporarily unavailable."},
            "moon_sign": {"sign": "Unknown", "house": 4, "interpretation": "Data temporarily unavailable."},
            "rising_sign": {"sign": "Unknown", "interpretation": "Data temporarily unavailable."},
        },
        "planets": [
            {"planet": "Sun", "sign": "Unknown", "house": 1, "retrograde": False, "interpretation": "Data unavailable."},
            {"planet": "Moon", "sign": "Unknown", "house": 4, "retrograde": False, "interpretation": "Data unavailable."},
        ],
        "aspects": [],
        "love_profile": {
            "attachment_style": "Unknown",
            "strengths": "Focus on self-awareness.",
            "challenges": "Embrace personal growth.",
            "advice": "Practice patience and self-compassion.",
        },
        "career_analysis": {
            "best_fields": "Various opportunities available",
            "work_style": "Focus on balance and awareness.",
            "growth_advice": "Explore your strengths and passions.",
        },
        "psychological_pattern": {
            "core_wound": "Self-reflection is key to growth.",
            "healing_direction": "Embrace self-compassion and awareness.",
        },
        "practical_guidance": {
            "career": "Focus on building stable foundations.",
            "relationships": "Practice open communication.",
            "self_development": "Embrace continuous learning.",
        },
    }


def fallback_compatibility_response() -> dict:
    """Return fallback compatibility response."""
    return {
        "summary": "Compatibility analysis temporarily unavailable.",
        "score": 50,
        "strengths": ["Both individuals have unique strengths."],
        "challenges": ["Focus on understanding each other."],
        "advice": "Practice patience and open communication.",
    }


def fallback_micro_response() -> dict:
    """Return fallback for micro-service calls."""
    return {
        "identity": {
            "sun_sign": "Unknown",
            "moon_sign": "Unknown",
            "rising_sign": "Unknown",
            "dominant_element": "Mixed",
            "emotional_intensity": 5,
        },
        "planets": {"planets": []},
        "aspects": {"aspects": []},
        "narrative": {
            "core_personality": "Profile temporarily simplified.",
            "emotional_pattern": "Emotional data unavailable.",
            "life_theme": "Theme calculation pending.",
            "shadow_side": "Shadow insight unavailable.",
            "growth_direction": "Growth insight pending.",
        },
    }


# ---------------------------------------------------------------------------
# Custom Exceptions (Never exposed to FastAPI)
# ---------------------------------------------------------------------------

class GroqAPIError(RuntimeError):
    """Internal error for Groq API issues. Never exposed to client."""
    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
        self.request_id = request_id


# ---------------------------------------------------------------------------
# AI Service Class
# ---------------------------------------------------------------------------

class AIService:
    """Production-safe AI service for Groq API calls."""
    
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str = GROQ_MODEL,
        timeout_seconds: float = REQUEST_TIMEOUT,
    ) -> None:
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = timeout_seconds
        
        logger.info("AIService initialized with model: %s", self.model)
    
    async def create_chat_completion(
        self,
        *,
        messages: list[dict[str, str]],
        temperature: float = TEMPERATURE,
        max_tokens: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> str:
        """Call Groq API with strict JSON mode enabled.
        
        This method returns raw text. Use generate_json_response() for
        production-safe JSON responses.
        
        Args:
            messages: Chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            request_id: Optional request ID for tracing
            
        Returns:
            Raw response text
            
        Raises:
            GroqAPIError: Internal error (never exposed to client)
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": float(temperature),
            "response_format": {"type": "json_object"},  # Strict JSON mode
        }
        
        if max_tokens is not None:
            payload["max_tokens"] = int(max_tokens)
        
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        logger.debug("[%s] Making Groq API request to %s", request_id, self.endpoint)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                )
        except httpx.TimeoutException as e:
            logger.error("[%s] Groq API timeout after %.1fs", request_id, self.timeout)
            raise GroqAPIError(
                f"Groq API timeout: {e}",
                request_id=request_id,
            ) from e
        except httpx.RequestError as e:
            logger.error("[%s] Groq API request error: %s", request_id, e)
            raise GroqAPIError(
                f"Groq API request failed: {e}",
                request_id=request_id,
            ) from e
        
        if response.status_code != 200:
            logger.error(
                "[%s] Groq API returned status %d: %s",
                request_id, response.status_code, response.text[:500]
            )
            raise GroqAPIError(
                f"Groq API returned status {response.status_code}",
                status_code=response.status_code,
                response_text=response.text[:2000] if response.text else None,
                request_id=request_id,
            )
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error("[%s] Failed to parse Groq response as JSON: %s", request_id, e)
            raise GroqAPIError(
                "Failed to parse Groq response as JSON",
                response_text=response.text[:2000],
                request_id=request_id,
            ) from e
        
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            logger.error("[%s] Unexpected Groq response shape: %s", request_id, e)
            raise GroqAPIError(
                "Unexpected Groq response shape",
                response_text=json.dumps(data)[:2000],
                request_id=request_id,
            ) from e
        
        if not content or not str(content).strip():
            logger.error("[%s] Groq returned empty content", request_id)
            raise GroqAPIError(
                "Groq returned empty content",
                request_id=request_id,
            )
        
        logger.info("[%s] Groq API call successful. Response length: %d", request_id, len(content))
        return str(content)
    
    async def generate_json_response(
        self,
        *,
        messages: list[dict[str, str]],
        temperature: float = TEMPERATURE,
        max_tokens: Optional[int] = None,
        fallback: Optional[dict] = None,
        request_id: Optional[str] = None,
    ) -> dict:
        """Generate JSON response with retry and fallback.
        
        This is the production-safe method that:
        - Retries up to MAX_RETRIES times
        - Uses safe JSON parsing with repair
        - Returns fallback JSON if all attempts fail
        - NEVER throws exceptions to caller
        
        Args:
            messages: Chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            fallback: Custom fallback JSON (uses default if not provided)
            request_id: Optional request ID for tracing
            
        Returns:
            Parsed JSON dict (never None, never raises)
        """
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        fallback = fallback or fallback_natal_response()
        
        # Check circuit breaker
        if not _circuit_breaker.should_allow_request():
            logger.warning("[%s] Circuit breaker OPEN, returning fallback", request_id)
            return fallback
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                raw = await self.create_chat_completion(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    request_id=request_id,
                )
                
                parsed = safe_parse_json(raw, request_id)
                
                if parsed is not None:
                    _circuit_breaker.record_success()
                    return parsed
                
                logger.warning(
                    "[%s] Attempt %d/%d: JSON parsing failed",
                    request_id, attempt + 1, MAX_RETRIES + 1
                )
                
            except GroqAPIError as e:
                logger.warning(
                    "[%s] Attempt %d/%d: API error: %s",
                    request_id, attempt + 1, MAX_RETRIES + 1, e
                )
            except Exception as e:
                logger.error(
                    "[%s] Attempt %d/%d: Unexpected error: %s",
                    request_id, attempt + 1, MAX_RETRIES + 1, e
                )
        
        # All attempts failed
        _circuit_breaker.record_failure()
        logger.error("[%s] All %d attempts failed, returning fallback", request_id, MAX_RETRIES + 1)
        return fallback
    
    async def generate_long_report(
        self,
        prompt: str,
        min_words: int = 1000,
        request_id: Optional[str] = None,
    ) -> str:
        """Generate a long report with word count validation.
        
        Args:
            prompt: Input prompt
            min_words: Minimum word count required
            request_id: Optional request ID for tracing
            
        Returns:
            Generated text (or fallback message)
        """
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            content = await self.create_chat_completion(
                messages=messages,
                temperature=0.85,
                max_tokens=4096,
                request_id=request_id,
            )
            
            word_count = self._count_words(content)
            logger.info("[%s] Generated report with %d words", request_id, word_count)
            
            if word_count >= min_words:
                return content
            
            # Try once more with reinforced prompt
            reinforced = self._create_reinforced_prompt(prompt, min_words, word_count)
            content = await self.create_chat_completion(
                messages=[{"role": "user", "content": reinforced}],
                temperature=0.85,
                max_tokens=4096,
                request_id=request_id,
            )
            
            word_count = self._count_words(content)
            logger.info("[%s] Reinforced report with %d words", request_id, word_count)
            
            return content
            
        except Exception as e:
            logger.error("[%s] Long report generation failed: %s", request_id, e)
            return self._get_fallback_report()
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        if not text:
            return 0
        return len(re.findall(r'\b\w+\b', text))
    
    def _create_reinforced_prompt(self, original: str, min_words: int, current: int) -> str:
        """Create reinforced prompt for longer output."""
        return f"""{original}

CRITICAL REQUIREMENT: 
- This report MUST be at least {min_words} words long
- Current output is only {current} words - significantly expand the analysis
- Add deep psychological, emotional, and planetary analysis
- Include concrete examples and detailed explanations
- Ensure comprehensive coverage of all requested topics"""
    
    def _get_fallback_report(self) -> str:
        """Return fallback report message."""
        return """**Analysis Temporarily Unavailable**

Your cosmic profile is being processed. Please try again in a moment.

**General Guidance:**
- Focus on self-awareness and personal growth
- Practice patience and compassion
- Embrace new opportunities with an open mind
- Trust your intuition when making decisions

*This is a fallback message. For a detailed analysis, please refresh.*"""


# ---------------------------------------------------------------------------
# Factory Functions
# ---------------------------------------------------------------------------

def get_ai_service(app_settings: Any) -> Optional[AIService]:
    """Create and return an AI service instance with error handling."""
    api_key = getattr(app_settings, 'GROQ_API_KEY', None)
    
    if not api_key:
        logger.warning("GROQ_API_KEY not configured - AI features will be disabled")
        return None
    
    try:
        return AIService(
            api_key,
            base_url=getattr(app_settings, 'GROQ_BASE_URL', "https://api.groq.com/openai/v1"),
            model=getattr(app_settings, 'GROQ_MODEL', GROQ_MODEL),
            timeout_seconds=getattr(app_settings, 'GROQ_TIMEOUT_SECONDS', REQUEST_TIMEOUT),
        )
    except Exception as e:
        logger.error("Failed to initialize AI service: %s", e)
        return None


# Global AI service instance (lazy initialization)
_ai_service_instance: Optional[AIService] = None


def get_global_ai_service(app_settings: Any = None) -> Optional[AIService]:
    """Get or create the global AI service instance."""
    global _ai_service_instance
    
    if _ai_service_instance is None:
        if app_settings is None:
            from core.config import get_settings
            app_settings = get_settings()
        _ai_service_instance = get_ai_service(app_settings)
    
    return _ai_service_instance


# ---------------------------------------------------------------------------
# Convenience Functions for Direct Use
# ---------------------------------------------------------------------------

async def generate_natal_reading(
    messages: list[dict[str, str]],
    api_key: str,
    base_url: str = "https://api.groq.com/openai/v1",
    model: str = GROQ_MODEL,
    request_id: Optional[str] = None,
) -> dict:
    """Convenience function for natal reading with all safety guarantees.
    
    This function NEVER raises exceptions and ALWAYS returns valid JSON.
    
    Args:
        messages: Chat messages for the AI
        api_key: Groq API key
        base_url: Groq API base URL
        model: Model to use
        request_id: Optional request ID for tracing
        
    Returns:
        Parsed JSON dict (never None, never raises)
    """
    try:
        service = AIService(api_key, base_url=base_url, model=model)
        return await service.generate_json_response(
            messages=messages,
            fallback=fallback_natal_response(),
            request_id=request_id,
        )
    except Exception as e:
        logger.error("Critical AI failure in generate_natal_reading: %s", e)
        return fallback_natal_response()


async def generate_compatibility_reading(
    messages: list[dict[str, str]],
    api_key: str,
    base_url: str = "https://api.groq.com/openai/v1",
    model: str = GROQ_MODEL,
    request_id: Optional[str] = None,
) -> dict:
    """Convenience function for compatibility reading with all safety guarantees.
    
    This function NEVER raises exceptions and ALWAYS returns valid JSON.
    """
    try:
        service = AIService(api_key, base_url=base_url, model=model)
        return await service.generate_json_response(
            messages=messages,
            fallback=fallback_compatibility_response(),
            request_id=request_id,
        )
    except Exception as e:
        logger.error("Critical AI failure in generate_compatibility_reading: %s", e)
        return fallback_compatibility_response()