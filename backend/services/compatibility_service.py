"""
services/compatibility_service.py
---------------------------------
Production-safe compatibility analysis service.

Key guarantees:
- Deterministic scoring (no AI for scores)
- Groq only writes narrative
- Strict JSON mode
- Retry + auto-fix
- Fallback when needed
- Never returns HTTP 500
- Token optimized
"""
from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Optional
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 2
REQUEST_TIMEOUT = 60.0
TEMPERATURE = 0.7


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class PersonInput:
    """Input data for a person."""
    date: str
    time: Optional[str]
    city: str
    country: str
    name: Optional[str] = None


@dataclass
class AspectData:
    """Aspect between two planets."""
    planet_a: str
    planet_b: str
    aspect_type: str
    orb: float


@dataclass
class CompatibilityScores:
    """Deterministic compatibility scores."""
    overall_score: int
    emotional_compatibility: int
    mental_compatibility: int
    physical_chemistry: int
    stability_score: int
    conflict_risk: int
    long_term_potential: int


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
    
    # Method 1: Extract JSON object from text
    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start != -1 and end != -1:
            extracted = raw_text[start:end]
            return json.loads(extracted)
    except json.JSONDecodeError as e:
        logger.debug("[%s] Extract-and-parse failed: %s", request_id, e)
    
    # Method 2: Clean and repair
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
    
    # Fix unquoted keys
    cleaned = re.sub(r'(\w+)(?=\s*:)', r'"\1"', cleaned)
    
    # Fix single quotes to double quotes
    cleaned = re.sub(r"(?<!\w)'([^']+)'(?!\w)", r'"\1"', cleaned)
    
    # Try to extract again after cleaning
    try:
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != -1:
            extracted = cleaned[start:end]
            return json.loads(extracted)
    except json.JSONDecodeError as e:
        logger.debug("[%s] Clean-and-extract failed: %s", request_id, e)
    
    # Final attempt: parse cleaned
    try:
        result = json.loads(cleaned)
        logger.info("[%s] JSON repaired successfully", request_id)
        return result
    except json.JSONDecodeError as e:
        logger.warning(
            "[%s] JSON parse failed after all repair attempts: %s. Raw length: %d",
            request_id, e, len(raw_text)
        )
        # Log the malformed JSON for debugging (truncated)
        logger.debug("[%s] Malformed JSON (first 500 chars): %s", request_id, raw_text[:500])
        return None


# ---------------------------------------------------------------------------
# Fallback Response
# ---------------------------------------------------------------------------

def get_fallback_response(scores: Optional[CompatibilityScores] = None) -> dict:
    """Return structured fallback response that matches FE contract."""
    if scores is None:
        scores = CompatibilityScores(
            overall_score=50,
            emotional_compatibility=50,
            mental_compatibility=50,
            physical_chemistry=50,
            stability_score=50,
            conflict_risk=50,
            long_term_potential=50
        )
    
    return {
        "overall_score": scores.overall_score,
        "emotional_compatibility": scores.emotional_compatibility,
        "mental_compatibility": scores.mental_compatibility,
        "physical_chemistry": scores.physical_chemistry,
        "stability_score": scores.stability_score,
        "conflict_risk": scores.conflict_risk,
        "long_term_potential": scores.long_term_potential,
        "relationship_summary": {
            "overview": "Phân tích tương thích đang được xử lý. Vui lòng thử lại sau.",
            "core_dynamic": "Đang phân tích động lực cốt lõi của mối quan hệ.",
            "relationship_purpose": "Đang xác định mục đích và hướng phát triển của mối quan hệ."
        },
        "strengths": [
            "Cả hai đều có tiềm năng phát triển tích cực",
            "Có khả năng học hỏi và thích nghi",
            "Có nền tảng tương thích cơ bản"
        ],
        "challenges": [
            "Cần thêm thời gian để hiểu nhau sâu sắc hơn",
            "Có thể gặp khó khăn trong giao tiếp ban đầu",
            "Cần xây dựng niềm tin lẫn nhau"
        ],
        "green_flags": [
            "Có tiềm năng tương thích cảm xúc",
            "Có khả năng hỗ trợ lẫn nhau",
            "Có xu hướng phát triển tích cực"
        ],
        "red_flags": [
            "Cần thận trọng trong việc thể hiện cảm xúc",
            "Có thể xảy ra hiểu lầm trong giao tiếp",
            "Cần thời gian để xây dựng sự tin tưởng"
        ]
    }


# ---------------------------------------------------------------------------
# Score Engine (Deterministic)
# ---------------------------------------------------------------------------

class ScoreEngine:
    """Deterministic scoring engine based on astrological aspects."""
    
    # Aspect weights for scoring
    HARMONIOUS_ASPECTS = {"trine", "sextile", "conjunction"}
    CHALLENGING_ASPECTS = {"square", "opposition"}
    
    # Planet pairs for different compatibility areas
    EMOTIONAL_PAIRS = [
        ("Moon", "Moon"),
        ("Moon", "Venus"),
        ("Venus", "Moon"),
        ("Sun", "Moon"),
        ("Moon", "Sun"),
    ]
    
    PHYSICAL_PAIRS = [
        ("Mars", "Venus"),
        ("Venus", "Mars"),
        ("Mars", "Mars"),
        ("Sun", "Mars"),
    ]
    
    MENTAL_PAIRS = [
        ("Mercury", "Mercury"),
        ("Mercury", "Sun"),
        ("Sun", "Mercury"),
        ("Jupiter", "Mercury"),
    ]
    
    STABILITY_PAIRS = [
        ("Saturn", "Sun"),
        ("Saturn", "Moon"),
        ("Saturn", "Venus"),
        ("Jupiter", "Sun"),
    ]
    
    def __init__(self, aspects: list[AspectData]):
        self.aspects = aspects
    
    def calculate(self) -> CompatibilityScores:
        """Calculate all compatibility scores deterministically."""
        emotional = self._calculate_area(self.EMOTIONAL_PAIRS)
        physical = self._calculate_area(self.PHYSICAL_PAIRS)
        mental = self._calculate_area(self.MENTAL_PAIRS)
        stability = self._calculate_area(self.STABILITY_PAIRS)
        conflict = self._calculate_conflict()
        
        # Calculate long term potential
        long_term = round(
            stability * 0.4 +
            emotional * 0.3 +
            mental * 0.2 +
            (100 - conflict) * 0.1
        )
        
        # Calculate overall score
        overall = round(
            emotional * 0.25 +
            physical * 0.20 +
            mental * 0.15 +
            stability * 0.20 +
            long_term * 0.20
        )
        
        return CompatibilityScores(
            overall_score=max(0, min(100, overall)),
            emotional_compatibility=max(0, min(100, emotional)),
            mental_compatibility=max(0, min(100, mental)),
            physical_chemistry=max(0, min(100, physical)),
            stability_score=max(0, min(100, stability)),
            conflict_risk=max(0, min(100, conflict)),
            long_term_potential=max(0, min(100, long_term))
        )
    
    def _calculate_area(self, planet_pairs: list[tuple[str, str]]) -> int:
        """Calculate score for a specific compatibility area."""
        score = 50  # Base score
        
        for aspect in self.aspects:
            pair = (aspect.planet_a, aspect.planet_b)
            reverse_pair = (aspect.planet_b, aspect.planet_a)
            
            if pair in planet_pairs or reverse_pair in planet_pairs:
                aspect_type = aspect.aspect_type.lower()
                
                if aspect_type in self.HARMONIOUS_ASPECTS:
                    # Harmonious aspects add points
                    if aspect_type == "trine":
                        score += 15
                    elif aspect_type == "sextile":
                        score += 12
                    elif aspect_type == "conjunction":
                        score += 10
                elif aspect_type in self.CHALLENGING_ASPECTS:
                    # Challenging aspects subtract points
                    if aspect_type == "square":
                        score -= 10
                    elif aspect_type == "opposition":
                        score -= 8
        
        return max(0, min(100, score))
    
    def _calculate_conflict(self) -> int:
        """Calculate conflict risk score."""
        base_conflict = 20
        
        for aspect in self.aspects:
            aspect_type = aspect.aspect_type.lower()
            
            if aspect_type in self.CHALLENGING_ASPECTS:
                base_conflict += 10
            elif aspect_type == "conjunction":
                # Conjunctions can be intense
                base_conflict += 5
        
        return max(0, min(100, base_conflict))


# ---------------------------------------------------------------------------
# Groq Narrative Engine
# ---------------------------------------------------------------------------

class GroqNarrativeEngine:
    """Generate narrative text using Groq API."""
    
    SYSTEM_PROMPT = """Bạn là một nhà chiêm tinh học chuyên nghiệp về mối quan hệ.
Nhiệm vụ: Phân tích tương thích giữa hai người dựa trên dữ liệu chiêm tinh.

QUAN TRỌNG:
- Trả về CHÍNH XÁC một object JSON hợp lệ
- KHÔNG sử dụng markdown
- KHÔNG thêm giải thích
- Tất cả nội dung bằng tiếng Việt
- Điểm số phải là số nguyên từ 0 đến 100
- Mỗi phần narrative tối đa 120 từ

Schema JSON yêu cầu:
{
  "summary": "tóm tắt tổng quan (max 120 từ)",
  "personality": "phân tích tính cách (max 120 từ)",
  "love_style": "phong cách tình yêu (max 120 từ)",
  "career": "tương thích công việc (max 120 từ)",
  "relationships": "động lực mối quan hệ (max 120 từ)",
  "advice": "lời khuyên thiết thực (max 120 từ)",
  "conflict_points": "điểm xung đột tiềm ẩn (max 120 từ)",
  "recommended_activities": ["hoạt động 1", "hoạt động 2", "hoạt động 3"],
  "aspects": ["aspect 1", "aspect 2", "aspect 3"],
  "ai_analysis": "phân tích AI chi tiết (max 200 từ)",
  "detailed_reasoning": "lý do chi tiết cho điểm số (max 200 từ)"
}"""
    
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str = GROQ_MODEL,
        timeout_seconds: float = REQUEST_TIMEOUT,
    ):
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = timeout_seconds
        
        logger.info("GroqNarrativeEngine initialized with model: %s", self.model)
    
    def _build_user_prompt(
        self,
        person_a: PersonInput,
        person_b: PersonInput,
        scores: CompatibilityScores,
        aspects: list[AspectData]
    ) -> str:
        """Build user prompt for Groq API."""
        
        aspects_str = "\n".join([
            f"- {a.planet_a} {a.aspect_type} {a.planet_b} (orb: {a.orb}°)"
            for a in aspects[:10]  # Limit to 10 aspects
        ]) if aspects else "- Không có aspect cụ thể"
        
        return f"""Phân tích tương thích chi tiết cho:

NGƯỜI A:
- Tên: {person_a.name or 'Không xác định'}
- Ngày sinh: {person_a.date}
- Giờ sinh: {person_a.time or 'Không xác định'}
- Nơi sinh: {person_a.city}, {person_a.country}

NGƯỜI B:
- Tên: {person_b.name or 'Không xác định'}
- Ngày sinh: {person_b.date}
- Giờ sinh: {person_b.time or 'Không xác định'}
- Nơi sinh: {person_b.city}, {person_b.country}

ĐIỂM SỐ (đã tính toán):
- Tổng quan: {scores.overall_score}/100
- Tương thích cảm xúc: {scores.emotional_compatibility}/100
- Tương thích tư duy: {scores.mental_compatibility}/100
- Hóa học thể chất: {scores.physical_chemistry}/100
- Điểm ổn định: {scores.stability_score}/100
- Rủi ro xung đột: {scores.conflict_risk}/100
- Tiềm năng lâu dài: {scores.long_term_potential}/100

CÁC ASPECT QUAN TRỌNG:
{aspects_str}

YÊU CẦU:
Trả về CHÍNH XÁC JSON theo schema đã cho. Đảm bảo:
1. Tất cả nội dung bằng tiếng Việt
2. Phân tích sâu sắc, chuyên nghiệp
3. Lời khuyên thiết thực
4. JSON hợp lệ, không markdown"""
    
    async def generate_narrative(
        self,
        person_a: PersonInput,
        person_b: PersonInput,
        scores: CompatibilityScores,
        aspects: list[AspectData],
        request_id: Optional[str] = None,
    ) -> Optional[dict]:
        """Generate narrative with retry logic.
        
        Args:
            person_a: First person's data
            person_b: Second person's data
            scores: Calculated compatibility scores
            aspects: List of astrological aspects
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict or None if all attempts fail
        """
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        
        user_prompt = self._build_user_prompt(person_a, person_b, scores, aspects)
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                raw = await self._call_groq(
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    request_id=request_id
                )
                
                # Log raw response for debugging
                logger.debug("[%s] Raw Groq response (first 500 chars): %s", request_id, raw[:500])
                
                parsed = safe_parse_json(raw, request_id)
                
                if parsed is not None:
                    logger.info("[%s] Narrative generated successfully on attempt %d", request_id, attempt + 1)
                    return parsed
                
                logger.warning(
                    "[%s] Attempt %d/%d: JSON parsing failed",
                    request_id, attempt + 1, MAX_RETRIES + 1
                )
                
            except Exception as e:
                logger.warning(
                    "[%s] Attempt %d/%d: API error: %s",
                    request_id, attempt + 1, MAX_RETRIES + 1, e
                )
        
        # All attempts failed
        logger.error("[%s] All %d attempts failed for narrative generation", request_id, MAX_RETRIES + 1)
        return None
    
    async def _call_groq(
        self,
        messages: list[dict[str, str]],
        request_id: Optional[str] = None,
    ) -> str:
        """Call Groq API with strict JSON mode.
        
        Args:
            messages: Chat messages
            request_id: Optional request ID for tracing
            
        Returns:
            Raw response text
            
        Raises:
            Exception: If API call fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": TEMPERATURE,
            "stream": False,  # IMPORTANT: No streaming
            "response_format": {"type": "json_object"},  # Strict JSON mode
        }
        
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
            raise Exception(f"Groq API timeout: {e}") from e
        except httpx.RequestError as e:
            logger.error("[%s] Groq API request error: %s", request_id, e)
            raise Exception(f"Groq API request failed: {e}") from e
        
        if response.status_code != 200:
            logger.error(
                "[%s] Groq API returned status %d: %s",
                request_id, response.status_code, response.text[:500]
            )
            raise Exception(f"Groq API returned status {response.status_code}")
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error("[%s] Failed to parse Groq response as JSON: %s", request_id, e)
            raise Exception("Failed to parse Groq response as JSON") from e
        
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            logger.error("[%s] Unexpected Groq response shape: %s", request_id, e)
            raise Exception("Unexpected Groq response shape") from e
        
        if not content or not str(content).strip():
            logger.error("[%s] Groq returned empty content", request_id)
            raise Exception("Groq returned empty content")
        
        logger.info("[%s] Groq API call successful. Response length: %d", request_id, len(content))
        return str(content)


# ---------------------------------------------------------------------------
# Compatibility Service (Main Entry Point)
# ---------------------------------------------------------------------------

class CompatibilityService:
    """Main compatibility analysis service.
    
    Guarantees:
    - Never throws exceptions to caller
    - Always returns valid JSON
    - Deterministic scoring
    - Groq only for narrative
    - Retry + fallback logic
    """
    
    def __init__(self, groq_api_key: str, base_url: str = "https://api.groq.com/openai/v1"):
        self.groq_engine = GroqNarrativeEngine(groq_api_key, base_url=base_url)
    
    async def analyze(
        self,
        person_a: PersonInput,
        person_b: PersonInput,
        aspects: list[AspectData],
        request_id: Optional[str] = None,
    ) -> dict:
        """Analyze compatibility between two people.
        
        This method NEVER raises exceptions and ALWAYS returns valid JSON.
        
        Args:
            person_a: First person's data
            person_b: Second person's data
            aspects: List of astrological aspects
            request_id: Optional request ID for tracing
            
        Returns:
            Valid JSON dict matching FE contract
        """
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        
        try:
            # Step 1: Calculate deterministic scores
            scores = ScoreEngine(aspects).calculate()
            logger.info(
                "[%s] Scores calculated: overall=%d, emotional=%d, mental=%d, physical=%d, stability=%d, conflict=%d, longterm=%d",
                request_id, scores.overall_score, scores.emotional_compatibility,
                scores.mental_compatibility, scores.physical_chemistry,
                scores.stability_score, scores.conflict_risk, scores.long_term_potential
            )
            
            # Step 2: Generate narrative using Groq
            narrative = await self.groq_engine.generate_narrative(
                person_a, person_b, scores, aspects, request_id
            )
            
            # Step 3: Build response
            if narrative:
                # Validate and merge narrative with scores
                response = self._build_response(scores, narrative)
                logger.info("[%s] Compatibility analysis completed successfully", request_id)
                return response
            else:
                # Return fallback with calculated scores
                logger.warning("[%s] Using fallback response due to narrative failure", request_id)
                return get_fallback_response(scores)
                
        except Exception as e:
            logger.error("[%s] Compatibility analysis failed: %s", request_id, e)
            # Return fallback response
            return get_fallback_response()
    
    def _build_response(self, scores: CompatibilityScores, narrative: dict) -> dict:
        """Build final response merging scores and narrative.
        
        Ensures all required fields are present and valid.
        """
        # Validate numeric fields in narrative
        def safe_int(value, default=50):
            try:
                val = int(value)
                return max(0, min(100, val))
            except (TypeError, ValueError):
                return default
        
        # Ensure arrays are present
        def safe_list(value, default=None):
            if default is None:
                default = []
            if isinstance(value, list):
                return value
            return default
        
        # Build response with validated data - NEW STRUCTURE
        response = {
            "overall_score": scores.overall_score,
            "emotional_compatibility": scores.emotional_compatibility,
            "mental_compatibility": scores.mental_compatibility,
            "physical_chemistry": scores.physical_chemistry,
            "stability_score": scores.stability_score,
            "conflict_risk": scores.conflict_risk,
            "long_term_potential": scores.long_term_potential,
            "relationship_summary": {
                "overview": narrative.get("summary", "Phân tích tương thích hoàn tất."),
                "core_dynamic": narrative.get("relationships", "Đang phân tích động lực cốt lõi của mối quan hệ."),
                "relationship_purpose": narrative.get("advice", "Đang xác định mục đích và hướng phát triển của mối quan hệ.")
            },
            "strengths": safe_list(narrative.get("personality", []), [
                "Cả hai đều có tiềm năng phát triển tích cực",
                "Có khả năng học hỏi và thích nghi",
                "Có nền tảng tương thích cơ bản"
            ]),
            "challenges": safe_list(narrative.get("conflict_points", []), [
                "Cần thêm thời gian để hiểu nhau sâu sắc hơn",
                "Có thể gặp khó khăn trong giao tiếp ban đầu",
                "Cần xây dựng niềm tin lẫn nhau"
            ]),
            "green_flags": safe_list(narrative.get("recommended_activities", []), [
                "Có tiềm năng tương thích cảm xúc",
                "Có khả năng hỗ trợ lẫn nhau",
                "Có xu hướng phát triển tích cực"
            ]),
            "red_flags": safe_list(narrative.get("aspects", []), [
                "Cần thận trọng trong việc thể hiện cảm xúc",
                "Có thể xảy ra hiểu lầm trong giao tiếp",
                "Cần thời gian để xây dựng sự tin tưởng"
            ])
        }
        
        return response


# ---------------------------------------------------------------------------
# Factory Function
# ---------------------------------------------------------------------------

def get_compatibility_service(api_key: str, base_url: str = "https://api.groq.com/openai/v1") -> CompatibilityService:
    """Create and return a compatibility service instance."""
    return CompatibilityService(api_key, base_url=base_url)