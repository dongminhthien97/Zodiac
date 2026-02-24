"""
services/ai/ai_service.py
--------------------------
Clean AI service layer using Groq client.
No Google AI, no inline prompts, production-ready.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from services.ai.groq_client import GroqClient
from services.ai.prompts import NatalPrompts, CompatibilityPrompts

logger = logging.getLogger(__name__)


class AIService:
    """Clean AI service using Groq client."""
    
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str = "llama-3.3-70b-versatile",
        timeout_seconds: float = 60.0,
    ):
        """Initialize AI service."""
        self.groq_client = GroqClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout_seconds=timeout_seconds,
        )
    
    async def generate_natal_interpretations(
        self,
        person_name: str,
        person_birth_date: str,
        person_birth_time: str,
        person_birth_place: str,
        planets_data: list[dict[str, Any]],
        aspects_data: list[dict[str, Any]],
        request_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate natal interpretations using Groq.
        
        Args:
            person_name: Person's name
            person_birth_date: Birth date
            person_birth_time: Birth time
            person_birth_place: Birth place
            planets_data: List of planet data from astrology engine
            aspects_data: List of aspect data from astrology engine
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict or None if generation fails
        """
        request_id = request_id or f"natal_{int(time.time() * 1000)}"
        
        try:
            # Build prompt using prompt templates
            user_prompt = NatalPrompts.build_user_prompt(
                person_name=person_name,
                person_birth_date=person_birth_date,
                person_birth_time=person_birth_time,
                person_birth_place=person_birth_place,
                planets_data=planets_data,
                aspects_data=aspects_data,
            )
            
            # Generate JSON using Groq client
            result = await self.groq_client.generate_json(
                prompt=user_prompt,
                request_id=request_id
            )
            
            logger.info("[%s] Natal interpretations generated successfully", request_id)
            return result
            
        except Exception as e:
            logger.error("[%s] Natal interpretations generation failed: %s", request_id, e)
            return None
    
    async def generate_compatibility_analysis(
        self,
        person_a: dict[str, Any],
        person_b: dict[str, Any],
        aspects: list[str],
        fallback_mode: bool,
        request_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate compatibility analysis using Groq.
        
        Args:
            person_a: Person A data
            person_b: Person B data
            aspects: List of aspects
            fallback_mode: Whether in fallback mode
            request_id: Optional request ID for logging
            
        Returns:
            Parsed JSON dict or None if generation fails
        """
        request_id = request_id or f"compat_{int(time.time() * 1000)}"
        
        try:
            # Build prompt using prompt templates
            user_prompt = CompatibilityPrompts.build_user_prompt(
                person_a=person_a,
                person_b=person_b,
                aspects=aspects,
                fallback_mode=fallback_mode,
            )
            
            # Generate JSON using Groq client
            result = await self.groq_client.generate_json(
                prompt=user_prompt,
                request_id=request_id
            )
            
            logger.info("[%s] Compatibility analysis generated successfully", request_id)
            return result
            
        except Exception as e:
            logger.error("[%s] Compatibility analysis generation failed: %s", request_id, e)
            return None
    
    async def generate_long_report(
        self,
        prompt: str,
        min_words: int = 1000,
        request_id: Optional[str] = None,
    ) -> str:
        """Generate long report using Groq.
        
        Args:
            prompt: User prompt
            min_words: Minimum word count
            request_id: Optional request ID for logging
            
        Returns:
            Generated report text
            
        Raises:
            Exception: If generation fails
        """
        request_id = request_id or f"report_{int(time.time() * 1000)}"
        
        try:
            # Use system message that enforces long format
            system_message = f"""You must generate a comprehensive report with at least {min_words} words.
Use markdown formatting for structure.
Provide detailed analysis with examples and practical advice.
Return only the report content, no additional explanation."""
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            # Generate text using Groq client
            raw = await self.groq_client._call_groq(messages, request_id)
            
            logger.info("[%s] Long report generated successfully. Length: %d", request_id, len(raw))
            return raw
            
        except Exception as e:
            logger.error("[%s] Long report generation failed: %s", request_id, e)
            raise Exception(f"Long report generation failed: {e}") from e


def get_global_ai_service(api_key: str, base_url: str = "https://api.groq.com/openai/v1") -> AIService:
    """Create and return a global AI service instance."""
    return AIService(api_key, base_url=base_url)