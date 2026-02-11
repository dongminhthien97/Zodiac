from __future__ import annotations
import logging
import httpx
import asyncio
from typing import Optional
import re

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-70b-versatile"
        self.timeout = 60.0
        
        logger.info(f"AI Service initialized with model: {self.model}")

    async def generate_long_report(self, prompt: str, min_words: int = 1000) -> str:
        """
        Generate a long report using Groq API with word count validation and retry logic.
        
        Args:
            prompt: The input prompt for the AI model
            min_words: Minimum word count required (default: 1000)
            
        Returns:
            Generated text content
            
        Raises:
            httpx.RequestError: For network-related errors
            httpx.HTTPStatusError: For HTTP errors
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        logger.info(f"Starting AI report generation with prompt length: {len(prompt)} characters")
        
        # First attempt
        try:
            content = await self._call_groq_api(prompt)
            word_count = self._count_words(content)
            
            logger.info(f"First attempt completed. Word count: {word_count}")
            
            # Check if meets minimum word count
            if word_count >= min_words:
                logger.info(f"✅ Word count requirement met: {word_count} >= {min_words}")
                return content
            
            logger.warning(f"⚠️ Word count too low: {word_count} < {min_words}. Retrying with reinforcement...")
            
            # Second attempt with reinforcement
            reinforced_prompt = self._create_reinforced_prompt(prompt, min_words, word_count)
            content = await self._call_groq_api(reinforced_prompt)
            word_count = self._count_words(content)
            
            logger.info(f"Second attempt completed. Word count: {word_count}")
            
            if word_count >= min_words:
                logger.info(f"✅ Word count requirement met after retry: {word_count} >= {min_words}")
                return content
            else:
                logger.warning(f"⚠️ Still too short after retry: {word_count} < {min_words}")
                return self._append_warning(content, word_count, min_words)
                
        except Exception as e:
            logger.error(f"❌ AI report generation failed: {e}")
            raise

    async def _call_groq_api(self, prompt: str) -> str:
        """Make API call to Groq with proper error handling and logging."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.85,
            "max_tokens": 4096,
            "stream": False
        }
        
        logger.debug(f"Making API request to {self.endpoint}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json=payload
                )
                
                response.raise_for_status()
                data = response.json()
                
                if "choices" not in data or not data["choices"]:
                    raise ValueError("No choices returned from API")
                
                content = data["choices"][0]["message"]["content"]
                
                logger.info(f"✅ API request successful. Response status: {response.status_code}")
                return content
                
        except httpx.TimeoutException as e:
            logger.error(f"❌ API request timed out after {self.timeout} seconds: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ API returned error status {e.response.status_code}: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"❌ API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error in API call: {e}")
            raise

    def _count_words(self, text: str) -> int:
        """Count words in text using regex for accurate counting."""
        if not text:
            return 0
        # Use regex to match word boundaries, handling various whitespace
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def _create_reinforced_prompt(self, original_prompt: str, min_words: int, current_words: int) -> str:
        """Create a reinforced prompt to encourage longer output."""
        reinforcement = f"""
IMPORTANT REQUIREMENT: 
- This report MUST be at least {min_words} words long
- Current output is only {current_words} words - significantly expand the analysis
- Add deep psychological, emotional, and planetary analysis
- Include more concrete examples and detailed explanations
- Ensure comprehensive coverage of all requested topics
- Do not summarize or be brief - expand deeply on every point

Please provide a comprehensive analysis that meets the word count requirement."""
        
        return f"{original_prompt}\n\n{reinforcement}"

    def _append_warning(self, content: str, actual_words: int, min_words: int) -> str:
        """Append a warning to content that doesn't meet word count requirements."""
        warning = f"""
---
⚠️ **WARNING**: This report contains {actual_words} words, which is below the required minimum of {min_words} words.
The analysis may be less comprehensive than requested due to content length limitations.
For a more detailed analysis, please request a longer report.
---
"""
        return f"{content}\n{warning}"


# Factory function to create AI service instance
def get_ai_service():
    """Create and return an AI service instance with proper error handling"""
    from core.config import settings
    
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not configured - AI features will be disabled")
        return None
    
    try:
        return AIService(settings.GROQ_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize AI service: {e}")
        return None

# Global AI service instance (lazy initialization)
_ai_service_instance = None

def get_global_ai_service():
    """Get or create the global AI service instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = get_ai_service()
    return _ai_service_instance
