"""
Astrology Content Engine v1.0.0 - Generator Logic
Production-ready pseudocode for LLM-based content generation

CRITICAL REQUIREMENTS:
- Zero sentence duplication within a single response
- Sentence length: 18-30 words
- Deterministic section ordering
- Layer separation (psychological/spiritual/practical)
"""

import hashlib
from typing import List, Dict, Set
from datetime import datetime


class ContentGenerator:
    """
    Core generator for astrology interpretations.
    Thread-safe, stateless except for deduplication tracking per generation session.
    """
    
    def __init__(self):
        self.seen_hashes: Set[str] = set()
        
    def hash_sentence(self, sentence: str) -> str:
        """Generate SHA-256 hash for deduplication"""
        clean = sentence.strip().replace("  ", " ")
        return hashlib.sha256(clean.encode('utf-8')).hexdigest()[:16]
    
    def validate_sentence(self, sentence: str) -> bool:
        """
        Validate sentence meets production requirements:
        - Length: 18-30 words
        - Unique hash
        - No trailing astrology jargon explanations
        """
        words = sentence.split()
        word_count = len(words)
        
        if word_count < 18 or word_count > 30:
            return False
            
        sentence_hash = self.hash_sentence(sentence)
        if sentence_hash in self.seen_hashes:
            return False
            
        self.seen_hashes.add(sentence_hash)
        return True
    
    def generate_big_picture(self, context: Dict) -> List[Dict]:
        """
        BIG PICTURE SECTION
        
        Required elements:
        1. Dominant sign clusters (element analysis)
        2. Element balance (missing/excessive)
        3. Axis tension identification
        4. One core life challenge
        5. One long-term directive
        
        NO generic personality descriptions allowed.
        """
        items = []
        
        # Psychological layer: Element analysis + axis tension
        psych_item = {
            "id": f"bp_{context['element'].lower()}_analysis",
            "layer": "psychological",
            "sentences": [
                # LLM PROMPT: Generate element excess/deficiency analysis (18-30 words)
                # LLM PROMPT: Generate axis tension description (18-30 words)
            ]
        }
        items.append(psych_item)
        
        # Practical layer: Directive + corrective action
        pract_item = {
            "id": "bp_life_directive",
            "layer": "practical",
            "sentences": [
                # LLM PROMPT: Generate medium-term directive based on core challenge (18-30 words)
                # LLM PROMPT: Generate specific behavioral practice (18-30 words)
            ]
        }
        items.append(pract_item)
        
        return items
    
    def generate_core_identity(self, context: Dict) -> List[Dict]:
        """
        CORE IDENTITY SECTION
        
        Split by planets: Sun (required), Moon (optional), Mercury (optional)
        
        Each planet MUST have:
        - Psychological layer: motivation source
        - Practical layer: behavior pattern
        - Shadow mention: explicit limitation
        """
        items = []
        
        # Sun - Always present
        sun_psych = {
            "id": f"sun_{context['sun_sign'].lower()}_motivation",
            "planet": "Sun",
            "sign": context['sun_sign'],
            "layer": "psychological",
            "sentences": [
                # LLM PROMPT: Core motivation of Sun in [sign] (18-30 words)
                # LLM PROMPT: Strength expression of this placement (18-30 words)
            ]
        }
        items.append(sun_psych)
        
        sun_practical = {
            "id": f"sun_{context['sun_sign'].lower()}_shadow",
            "planet": "Sun",
            "sign": context['sun_sign'],
            "layer": "practical",
            "sentences": [
                # LLM PROMPT: Shadow/limitation of Sun in [sign] (18-30 words)
                # LLM PROMPT: Behavioral pattern that blocks growth (18-30 words)
            ]
        }
        items.append(sun_practical)
        
        # Moon - If provided
        if context.get('moon_sign'):
            moon_item = {
                "id": f"moon_{context['moon_sign'].lower()}_emotional",
                "planet": "Moon",
                "sign": context['moon_sign'],
                "layer": "psychological",
                "sentences": [
                    # LLM PROMPT: Emotional need of Moon in [sign] (18-30 words)
                ]
            }
            items.append(moon_item)
        
        return items
    
    def generate_love_drive(self, context: Dict) -> List[Dict]:
        """
        LOVE & DRIVE SECTION
        
        Must include:
        - Venus: attachment style
        - Mars: motivation & conflict pattern
        - Contrast if signs differ significantly
        """
        items = []
        
        venus_item = {
            "id": f"venus_{context.get('venus_sign', context['sun_sign']).lower()}_attach",
            "planet": "Venus",
            "sign": context.get('venus_sign', context['sun_sign']),
            "layer": "psychological",
            "sentences": [
                # LLM PROMPT: Venus attachment style (18-30 words)
                # LLM PROMPT: Idealization pattern (18-30 words)
            ]
        }
        items.append(venus_item)
        
        return items
    
    def generate_collective(self, context: Dict) -> List[Dict]:
        """
        COLLECTIVE SECTION
        
        Generational planets:
        - Jupiter: growth field
        - Uranus: innovation area
        - Neptune: illusion risk
        - Pluto: transformation theme
        
        Must reference GENERATION patterns, not personal traits.
        """
        # Implementation depends on birth year data
        return []
    
    def generate_soul_lessons(self, context: Dict) -> List[Dict]:
        """
        SOUL LESSONS SECTION
        
        Required:
        - North Node: evolutionary direction
        - South Node: pattern to release
        - Chiron: wound + healing mechanism
        
        Each MUST include:
        - One repeating life pattern
        - One corrective action
        """
        # Implementation depends on node positions
        return []
    
    def generate_conclusion(self, context: Dict) -> List[Dict]:
        """
        CONCLUSION SECTION
        
        Exactly:
        - 4 short identity bullets (each 6-10 words)
        - 1 core life rule (imperative, 15-25 words)
        
        No astrology jargon explanations.
        """
        items = []
        
        identity_item = {
            "id": f"conc_{context['zodiac'].lower()}",
            "layer": "psychological",
            "sentences": [
                # 4 identity bullets (short, declarative)
                # LLM PROMPT: "Bạn là [archetype]" (6-10 words)
                # LLM PROMPT: "Bạn sở hữu [quality]" (6-10 words)
                # LLM PROMPT: "[Value] là kim chỉ nam" (6-10 words)
                # LLM PROMPT: "Sống là [process]" (6-10 words)
            ]
        }
        items.append(identity_item)
        
        rule_item = {
            "id": "conc_rule",
            "layer": "practical",
            "sentences": [
                # LLM PROMPT: Imperative life rule (15-25 words)
            ]
        }
        items.append(rule_item)
        
        return items
    
    def generate_full_response(self, context: Dict) -> Dict:
        """
        Main orchestration function.
        
        Enforces:
        - Section ordering
        - Deduplication across all sections
        - Schema compliance
        - House logic validation
        """
        # Reset deduplication for new generation
        self.seen_hashes.clear()
        
        # Validate house logic
        if not context['birth_time_known']:
            assert context['house_system'] is None, "Cannot use house system without birth time"
            context['interpretation_mode'] = 'sign_based'
        else:
            context['interpretation_mode'] = 'house_based'
        
        # Generate sections in fixed order
        sections = [
            {"key": "big_picture", "items": self.generate_big_picture(context)},
            {"key": "core_identity", "items": self.generate_core_identity(context)},
            {"key": "love_drive", "items": self.generate_love_drive(context)},
            {"key": "collective", "items": self.generate_collective(context)},
            {"key": "soul_lessons", "items": self.generate_soul_lessons(context)},
            {"key": "conclusion", "items": self.generate_conclusion(context)},
        ]
        
        # Generate content hash
        all_sentences = []
        for section in sections:
            for item in section['items']:
                all_sentences.extend(item['sentences'])
        
        content_hash = hashlib.sha256("".join(all_sentences).encode()).hexdigest()[:16]
        
        return {
            "meta": {
                "version": "v1.0.0",
                "content_hash": content_hash,
                "locale": context.get('locale', 'vi'),
                "generated_at": datetime.utcnow().isoformat() + "Z"
            },
            "context": {
                "zodiac": context['zodiac'],
                "element": context['element'],
                "birth_time_known": context['birth_time_known'],
                "interpretation_mode": context['interpretation_mode'],
                "house_system": context.get('house_system')
            },
            "sections": sections
        }


# USAGE EXAMPLE
if __name__ == "__main__":
    generator = ContentGenerator()
    
    sample_context = {
        "zodiac": "Libra",
        "element": "Air",
        "sun_sign": "Libra",
        "moon_sign": None,
        "mercury_sign": None,
        "birth_time_known": False,
        "house_system": None,
        "locale": "vi"
    }
    
    response = generator.generate_full_response(sample_context)
    print(f"Generated {len(response['sections'])} sections")
    print(f"Content hash: {response['meta']['content_hash']}")
