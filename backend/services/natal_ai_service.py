"""
services/natal_ai_service.py
----------------------------
AI service for natal chart interpretations only.
Pure AI logic, no calculations, no planet generation.
Only provides interpretations for planets and aspects.
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Optional, Dict, List
import httpx

logger = logging.getLogger(__name__)

# Configuration
GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 2
REQUEST_TIMEOUT = 60.0
TEMPERATURE = 0.7


class NatalAIService:
    """AI service for natal chart interpretations only."""
    
    SYSTEM_PROMPT = """Bạn là một nhà chiêm tinh học chuyên nghiệp.
Nhiệm vụ: Cung cấp giải thích chi tiết cho các hành tinh và aspect đã được cung cấp.

QUAN TRỌNG:
- Trả về CHÍNH XÁC một object JSON hợp lệ
- KHÔNG sử dụng markdown
- KHÔNG thêm giải thích
- Tất cả nội dung bằng tiếng Việt
- Mỗi giải thích 3-5 câu, chuyên sâu và cụ thể
- KHÔNG tạo ra các hành tinh mới
- Chỉ giải thích các hành tinh và aspect đã được cung cấp

Schema JSON yêu cầu:
{
  "planet_interpretations": [
    {
      "planet": "Sun",
      "interpretation": "giải thích chi tiết 3-5 câu"
    }
  ],
  "aspect_interpretations": [
    {
      "aspect_type": "trine",
      "planet_1": "Sun",
      "planet_2": "Moon",
      "interpretation": "giải thích chi tiết 3-5 câu"
    }
  ],
  "core_identity": {
    "summary": "tổng hợp 3-5 câu về bản chất cốt lõi",
    "sun_sign": "giải thích Mặt Trời",
    "moon_sign": "giải thích Mặt Trăng",
    "rising_sign": "giải thích Cung Mọc"
  },
  "love_profile": {
    "attachment_style": "phong cách gắn bó",
    "strengths": "điểm mạnh trong tình yêu",
    "challenges": "thách thức trong tình yêu",
    "advice": "lời khuyên về tình yêu"
  },
  "career_analysis": {
    "best_fields": "lĩnh vực phù hợp nhất",
    "work_style": "phong cách làm việc",
    "growth_advice": "lời khuyên phát triển sự nghiệp"
  },
  "psychological_pattern": {
    "core_wound": "vết thương tâm lý cốt lõi",
    "healing_direction": "hướng phát triển lành mạnh"
  },
  "practical_guidance": {
    "career": "hướng dẫn thực tế về sự nghiệp",
    "relationships": "hướng dẫn thực tế về các mối quan hệ",
    "self_development": "hướng dẫn thực tế về phát triển bản thân"
  }
}"""
    
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str = GROQ_MODEL,
        timeout_seconds: float = REQUEST_TIMEOUT,
    ):
        """Initialize Natal AI service."""
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = timeout_seconds
        
        logger.info("NatalAIService initialized with model: %s", self.model)
    
    def _build_user_prompt(
        self,
        person_name: str,
        person_birth_date: str,
        person_birth_time: Optional[str],
        person_birth_place: str,
        planets_data: List[Dict[str, Any]],
        aspects_data: List[Dict[str, Any]]
    ) -> str:
        """Build user prompt for Natal AI interpretation."""
        
        # Format planets data
        planets_str = "\n".join([
            f"- {p['planet']}: {p['sign']} (longitude: {p['longitude']:.2f}°, degree: {p['degree']:.2f}°, house: {p['house']}, retrograde: {p['retrograde']})"
            for p in planets_data
        ]) if planets_data else "- Không có dữ liệu hành tinh"
        
        # Format aspects data
        aspects_str = "\n".join([
            f"- {a['aspect_type']}: {a['planet_1']} ↔ {a['planet_2']} (orb: {a['orb']:.2f}°)"
            for a in aspects_data
        ]) if aspects_data else "- Không có aspect"
        
        return f"""Hãy phân tích bản đồ sao chi tiết cho:

**Thông tin cá nhân:**
- Tên: {person_name}
- Ngày sinh: {person_birth_date}
- Giờ sinh: {person_birth_time or "Không rõ"}
- Nơi sinh: {person_birth_place}

**Dữ liệu hành tinh:**
{planets_str}

**Dữ liệu aspect:**
{aspects_str}

**YÊU CẦU PHÂN TÍCH:**

1. **Giải thích hành tinh:** Mỗi hành tinh cần được giải thích chi tiết 3-5 câu, tập trung vào:
   - Ý nghĩa của hành tinh ở cung và nhà cụ thể
   - Cách hành tinh này biểu hiện trong cuộc sống
   - Những thách thức và cơ hội tiềm ẩn
   - Tác động đến tính cách và hành vi

2. **Giải thích aspect:** Mỗi aspect cần được giải thích chi tiết 3-5 câu, tập trung vào:
   - Ý nghĩa của mối quan hệ giữa hai hành tinh
   - Cách aspect này tạo ra năng lượng trong bản đồ
   - Những biểu hiện cụ thể trong cuộc sống
   - Cơ hội phát triển và thách thức cần vượt qua

3. **Phân tích tổng thể:** Các phần còn lại cần:
   - Phân tích chuyên sâu, không chung chung
   - Cung cấp ví dụ cụ thể và thiết thực
   - Đưa ra lời khuyên thực tế và khả thi
   - Tập trung vào phát triển bản thân

**LƯU Ý:**
- KHÔNG tạo ra các hành tinh mới
- Chỉ giải thích các hành tinh và aspect đã được cung cấp
- Tất cả nội dung bằng tiếng Việt
- Giải thích phải chuyên sâu, tránh mô tả chung chung
- Mỗi giải thích 3-5 câu, không quá dài hoặc quá ngắn"""
    
    async def generate_interpretations(
        self,
        person_name: str,
        person_birth_date: str,
        person_birth_time: Optional[str],
        person_birth_place: str,
        planets_data: List[Dict[str, Any]],
        aspects_data: List[Dict[str, Any]],
        request_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate natal interpretations with retry logic.
        
        Args:
            person_name: Person's name
            person_birth_date: Birth date
            person_birth_time: Birth time
            person_birth_place: Birth place
            planets_data: List of planet data from astrology engine
            aspects_data: List of aspect data from astrology engine
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict or None if all attempts fail
        """
        request_id = request_id or f"natal_{int(time.time() * 1000)}"
        
        user_prompt = self._build_user_prompt(
            person_name, person_birth_date, person_birth_time, person_birth_place,
            planets_data, aspects_data
        )
        
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
                
                parsed = self._safe_parse_json(raw, request_id)
                
                if parsed is not None:
                    logger.info("[%s] Natal interpretations generated successfully on attempt %d", request_id, attempt + 1)
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
        logger.error("[%s] All %d attempts failed for natal interpretations", request_id, MAX_RETRIES + 1)
        return None
    
    async def _call_groq(
        self,
        messages: List[Dict[str, str]],
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
    
    def _safe_parse_json(self, raw_text: str, request_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
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