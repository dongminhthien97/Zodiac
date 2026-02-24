"""
services/ai_service_groq.py
---------------------------
AI service for Groq API calls only.
Pure AI logic, no calculations, no schema mapping.
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


class GroqAIService:
    """AI service for Groq API calls."""
    
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
        """Initialize Groq AI service."""
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = timeout_seconds
        
        logger.info("GroqAIService initialized with model: %s", self.model)
    
    def _build_user_prompt(
        self,
        person_a_name: str,
        person_b_name: str,
        scores: Dict[str, int],
        aspects: List[Dict[str, Any]]
    ) -> str:
        """Build user prompt for Groq API."""
        
        aspects_str = "\n".join([
            f"- {a['planet_a']} {a['aspect_type']} {a['planet_b']} (orb: {a['orb']}°)"
            for a in aspects[:10]  # Limit to 10 aspects
        ]) if aspects else "- Không có aspect cụ thể"
        
        return f"""Phân tích tương thích chi tiết cho:

NGƯỜI A: {person_a_name}
NGƯỜI B: {person_b_name}

ĐIỂM SỐ (đã tính toán):
- Tổng quan: {scores['overall_score']}/100
- Tương thích cảm xúc: {scores['emotional_compatibility']}/100
- Tương thích tư duy: {scores['mental_compatibility']}/100
- Hóa học thể chất: {scores['physical_chemistry']}/100
- Điểm ổn định: {scores['stability_score']}/100
- Rủi ro xung đột: {scores['conflict_risk']}/100
- Tiềm năng lâu dài: {scores['long_term_potential']}/100

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
        person_a_name: str,
        person_b_name: str,
        scores: Dict[str, int],
        aspects: List[Dict[str, Any]],
        request_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate narrative with retry logic.
        
        Args:
            person_a_name: First person's name
            person_b_name: Second person's name
            scores: Calculated compatibility scores
            aspects: List of astrological aspects
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict or None if all attempts fail
        """
        request_id = request_id or f"req_{int(time.time() * 1000)}"
        
        user_prompt = self._build_user_prompt(person_a_name, person_b_name, scores, aspects)
        
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