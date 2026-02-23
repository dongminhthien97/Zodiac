from __future__ import annotations
import logging
import httpx
import re
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from core.config import Settings


class GroqAPIError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, response_text: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class AIService:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str,
        model: str,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.base_url = (base_url or "https://api.groq.com/openai/v1").rstrip("/")
        self.endpoint = f"{self.base_url}/chat/completions"
        self.model = model
        self.timeout = float(timeout_seconds)
        self._groq_client = None

        logger.info("AI Service initialized with model: %s", self.model)

    async def create_chat_completion(
        self,
        *,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> str:
        """Call Groq OpenAI-compatible Chat Completions API.

        Request body example:
        {
          "model": "<model>",
          "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
          ],
          "temperature": 0.7
        }
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, object] = {
            "model": self.model,
            "messages": messages,
            "temperature": float(temperature),
        }
        if max_tokens is not None:
            payload["max_tokens"] = int(max_tokens)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.endpoint, headers=headers, json=payload)
        except httpx.RequestError as e:
            raise GroqAPIError(f"Groq request failed: {e}") from e

        if response.status_code != 200:
            raise GroqAPIError(
                f"Groq API returned non-200 status: {response.status_code}",
                status_code=response.status_code,
                response_text=(response.text[:2000] if response.text else None),
            )

        try:
            data = response.json()
        except Exception as e:
            raise GroqAPIError(
                "Failed to parse Groq JSON response",
                status_code=response.status_code,
                response_text=(response.text[:2000] if response.text else None),
            ) from e

        try:
            content = data["choices"][0]["message"]["content"]
        except Exception as e:
            raise GroqAPIError(
                "Unexpected Groq response shape (missing choices/message/content)",
                status_code=response.status_code,
                response_text=(response.text[:2000] if response.text else None),
            ) from e

        if not content or not str(content).strip():
            raise GroqAPIError(
                "Groq returned empty content",
                status_code=response.status_code,
                response_text=(response.text[:2000] if response.text else None),
            )

        return str(content)

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
        if self._groq_client is not None:
            try:
                completion = await self._groq_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.85,
                    max_tokens=4096,
                )
                content = completion.choices[0].message.content
                if not content:
                    raise ValueError("Empty content returned from Groq SDK")
                return content
            except Exception as e:
                logger.warning("Groq SDK request failed; falling back to HTTP: %s", e)

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
def get_ai_service(app_settings: "Settings") -> "AIService | None":
    """Create and return an AI service instance with proper error handling."""
    if not app_settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not configured - AI features will be disabled")
        return None
    
    try:
        return AIService(
            app_settings.GROQ_API_KEY,
            base_url=app_settings.GROQ_BASE_URL,
            model=app_settings.GROQ_MODEL,
            timeout_seconds=app_settings.GROQ_TIMEOUT_SECONDS,
        )
    except Exception as e:
        logger.error("Failed to initialize AI service: %s", e)
        return None

# Global AI service instance (lazy initialization)
_ai_service_instance = None

def get_global_ai_service(app_settings: "Settings | None" = None) -> "AIService | None":
    """Get or create the global AI service instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        if app_settings is None:
            from core.config import get_settings

            app_settings = get_settings()
        _ai_service_instance = get_ai_service(app_settings)
    return _ai_service_instance
