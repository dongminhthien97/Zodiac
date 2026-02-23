"""
natal_prompt_builder.py
-----------------------
Builds the system prompt and user prompt for the professional astrologer
natal chart interpretation endpoint.

Tone contract (enforced via system prompt):
- Direct, insightful, slightly provocative
- Emotionally precise, modern
- NOT mystical fantasy, NOT generic positivity

Output contract:
- Valid JSON only, matching the exact schema below
- No markdown, no explanation, no extra text
- All strings in English (the AI writes in English per the persona)
- Under 3200 tokens total
"""
from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Schema template – mirrors models/schemas.py NatalAstrologyAI exactly
# ---------------------------------------------------------------------------
SCHEMA_TEMPLATE: dict[str, Any] = {
    "core_identity": {
        "summary": "",
        "sun_sign": {"sign": "", "house": 0, "interpretation": ""},
        "moon_sign": {"sign": "", "house": 0, "interpretation": ""},
        "rising_sign": {"sign": "", "interpretation": ""},
    },
    "planets": [
        {
            "planet": "",
            "sign": "",
            "house": 0,
            "retrograde": False,
            "interpretation": "",
        }
    ],
    "aspects": [
        {
            "aspect_type": "",
            "planet_1": "",
            "planet_2": "",
            "interpretation": "",
        }
    ],
    "love_profile": {
        "attachment_style": "",
        "strengths": "",
        "challenges": "",
        "advice": "",
    },
    "career_analysis": {
        "best_fields": "",
        "work_style": "",
        "growth_advice": "",
    },
    "psychological_pattern": {
        "core_wound": "",
        "healing_direction": "",
    },
    "practical_guidance": {
        "career": "",
        "relationships": "",
        "self_development": "",
    },
}

# ---------------------------------------------------------------------------
# System prompt – persona + hard output rules
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a professional astrologer and psychological storyteller.

IMPORTANT - LANGUAGE RULES:
- All textual content MUST be written in Vietnamese.
- Use natural Vietnamese.
- No English words.
- No bilingual output.
- Do not translate zodiac names to English.
- Use Vietnamese astrological terminology.
- Maintain premium, mystical tone.
- If any part of the response is not Vietnamese, regenerate internally before output.

Your tone:
- Direct
- Insightful
- Slightly provocative
- Emotionally precise
- Modern
- Not mystical fantasy
- Not generic positivity

WRITING STYLE RULES:
- Write like a sharp astrologer who understands human psychology.
- Call out patterns honestly.
- Avoid vague spiritual clichés.
- Avoid repeating sign stereotypes.
- Show emotional nuance.
- Be specific about internal conflict.
- Each interpretation: 3–5 sentences.
- Use short, punchy sentences mixed with reflective ones.
- Make it feel personal, not textbook.

ASTROLOGY DEPTH REQUIREMENTS:
For each placement:
- Explain how planet + sign + house interact.
- Explain tension or contradiction if present.
- Show how this plays out in real life.
- Avoid generic definitions.

For aspects:
- Describe dynamic between the two planets.
- Is it friction? Support? Obsession? Blind spot?
- Make it psychologically real.

LENGTH CONTROL:
- Keep total output under 3200 tokens.
- Do not exceed 5 sentences per interpretation.
- Avoid repetition.
- Be dense but controlled.

OUTPUT RULES (STRICT):
- You MUST output ONLY valid JSON.
- No markdown. No explanation. No extra text. No comments.
- No trailing commas. No duplicate keys.
- All strings must use double quotes.
- Use integers for all house fields (use 0 if unknown).
- Use boolean for retrograde.
- Do not output null for any string field; use empty string "" if unknown.
- The planets array must include one entry per input planet (same order).
- The aspects array must include entries for the provided aspects input.
- All sign, house, and retrograde values must match the input data exactly.
- If you cannot complete the full JSON structure properly, return:
  {"error":"INCOMPLETE_GENERATION"}"""


# ---------------------------------------------------------------------------
# Public builder function
# ---------------------------------------------------------------------------

def build_natal_prompts(natal_data: dict[str, Any]) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for the natal chart AI call.

    Args:
        natal_data: Structured dict produced by the router containing:
            person, sun, moon, rising, dominant_element,
            planets, houses, aspects.

    Returns:
        Tuple of (system_prompt_str, user_prompt_str).
    """
    natal_json = json.dumps(natal_data, ensure_ascii=False, indent=2, sort_keys=True)
    schema_json = json.dumps(SCHEMA_TEMPLATE, ensure_ascii=False, indent=2)

    user_prompt = _build_user_prompt(natal_json, schema_json)
    return SYSTEM_PROMPT, user_prompt


def _build_user_prompt(natal_json: str, schema_json: str) -> str:
    """Construct the user-turn message sent to the model."""
    return f"""Here is the natal chart data:

{natal_json}

Generate the interpretation following the EXACT schema below.

STRICT OUTPUT RULES:
- Return ONLY a JSON object, nothing else.
- No markdown, no code fences, no commentary.
- Do not add, remove, or rename any keys.
- No extra keys anywhere in the output.
- Use integers for all "house" fields (0 if unknown).
- Use boolean for "retrograde".
- Do not output null for any string field; use "" if unknown.
- The "planets" array must include one item for each planet in the input
  "planets" list, in the same order.
- The "aspects" array must include one item for each aspect in the input
  "aspects" list (you may include fewer only if the input list is empty).
- All "sign", "house", and "retrograde" values must exactly match the
  corresponding values in the input data.
- Each interpretation must be 3–5 sentences, psychologically precise,
  and specific to this person's chart — not generic sign descriptions.
- The "core_identity.summary" must be 3–5 sentences synthesising Sun,
  Moon, and Rising into a coherent psychological portrait.
- The "love_profile", "career_analysis", "psychological_pattern", and
  "practical_guidance" fields must each be substantive paragraphs
  (3–5 sentences), not bullet lists.

REQUIRED SCHEMA (match exactly):
{schema_json}
""".strip()


# ---------------------------------------------------------------------------
# Helper: build the structured natal_data dict from router-computed values
# ---------------------------------------------------------------------------

def build_natal_data_payload(
    *,
    person_info: dict[str, Any],
    sun: str,
    moon: str | None,
    rising: str | None,
    dominant_element: str,
    planets_prompt: list[dict[str, Any]],
    houses_data: list[dict[str, Any]],
    aspects_prompt: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble the structured natal data dict passed to the AI prompt.

    All values come from the router's existing computation logic; this
    function just packages them consistently.
    """
    return {
        "person": person_info,
        "sun": sun,
        "moon": moon,
        "rising": rising,
        "dominant_element": dominant_element,
        "planets": planets_prompt,
        "houses": houses_data,
        "aspects": aspects_prompt,
    }
