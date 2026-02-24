"""
services/ai/groq_client.py
----------------------------
Clean Groq client for AI service layer.
No Google AI, no response_format=json_object, production-ready.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Optional
import httpx

logger = logging.getLogger(__name__)


class GroqClient:
    """Clean Groq client for AI service layer."""
    
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str = "llama-3.3-70b-versatile",
        timeout_seconds: float = 60.0,
    ):
        """Initialize Groq client."""
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = timeout_seconds
        
        logger.info("GroqClient initialized with model: %s", self.model)
    
    async def generate_json(self, prompt: str, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate JSON response from Groq API.
        
        Args:
            prompt: User prompt
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict
            
        Raises:
            Exception: If API call fails or JSON parsing fails
        """
        request_id = request_id or f"groq_{int(time.time() * 1000)}"
        
        # System message that enforces JSON format
        system_message = """You must respond strictly in valid JSON format only.
Do not add any explanation, markdown, or additional text.
Return only a valid JSON object that can be parsed directly."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        try:
            raw = await self._call_groq(messages, request_id)
            parsed = self._safe_parse_json(raw, request_id)
            
            if parsed is None:
                raise Exception("Failed to parse Groq response as JSON")
            
            logger.info("[%s] Groq JSON generation successful", request_id)
            return parsed
            
        except Exception as e:
            logger.error("[%s] Groq JSON generation failed: %s", request_id, e)
            raise Exception(f"Groq JSON generation failed: {e}") from e
    
    async def _call_groq(
        self,
        messages: list[dict[str, str]],
        request_id: Optional[str] = None,
    ) -> str:
        """Call Groq API with clean error handling.
        
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
            "temperature": 0.7,
            "max_tokens": 4096,
            "stream": False,  # No streaming
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
        cleaned = self._remove_markdown_fences(cleaned)
        
        # Remove trailing commas (common LLM issue)
        cleaned = self._remove_trailing_commas(cleaned)
        
        # Remove comments
        cleaned = self._remove_comments(cleaned)
        
        # Fix unquoted keys
        cleaned = self._fix_unquoted_keys(cleaned)
        
        # Fix single quotes to double quotes
        cleaned = self._fix_single_quotes(cleaned)
        
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
    
    def _remove_markdown_fences(self, text: str) -> str:
        """Remove markdown code fences."""
        text = text.replace("```json", "")
        text = text.replace("```", "")
        return text.strip()
    
    def _remove_trailing_commas(self, text: str) -> str:
        """Remove trailing commas from JSON."""
        import re
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        return text
    
    def _remove_comments(self, text: str) -> str:
        """Remove JavaScript-style comments."""
        import re
        text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text
    
    def _fix_unquoted_keys(self, text: str) -> str:
        """Fix unquoted JSON keys."""
        import re
        text = re.sub(r'(\w+)(?=\s*:)', r'"\1"', text)
        return text
    
    def _fix_single_quotes(self, text: str) -> str:
        """Fix single quotes to double quotes."""
        import re
        text = re.sub(r"(?<!\w)'([^']+)'(?!\w)", r'"\1"', text)
        return text