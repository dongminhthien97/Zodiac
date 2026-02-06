"""
Content Validation Module for Astrology Engine v1.0.0
Enforces all quality constraints before content release
"""

from typing import Dict, List, Tuple
import re


class ContentValidator:
    """
    Production validator ensuring strict compliance with content rules.
    """
    
    @staticmethod
    def validate_sentence_length(sentence: str) -> Tuple[bool, str]:
        """Validate 18-30 word constraint"""
        words = sentence.strip().split()
        word_count = len(words)
        
        if word_count < 18:
            return False, f"Sentence too short: {word_count} words (min 18)"
        if word_count > 30:
            return False, f"Sentence too long: {word_count} words (max 30)"
        return True, "OK"
    
    @staticmethod
    def validate_no_duplicates(response: Dict) -> Tuple[bool, List[str]]:
        """Verify zero sentence duplication across entire response"""
        seen = set()
        duplicates = []
        
        for section in response['sections']:
            for item in section['items']:
                for sentence in item['sentences']:
                    normalized = sentence.strip().lower()
                    if normalized in seen:
                        duplicates.append(sentence[:50] + "...")
                    seen.add(normalized)
        
        if duplicates:
            return False, duplicates
        return True, []
    
    @staticmethod
    def validate_house_logic(response: Dict) -> Tuple[bool, str]:
        """Ensure house numbers only appear when birth_time_known = true"""
        context = response['context']
        
        if not context['birth_time_known']:
            # Check no houses in any item
            for section in response['sections']:
                for item in section['items']:
                    if item.get('house') is not None:
                        return False, f"House number found without birth time: {item['id']}"
            
            if context['house_system'] is not None:
                return False, "House system specified without birth time"
        
        return True, "OK"
    
    @staticmethod
    def validate_section_order(response: Dict) -> Tuple[bool, str]:
        """Verify fixed section ordering"""
        expected_order = [
            "big_picture",
            "core_identity", 
            "love_drive",
            "collective",
            "soul_lessons",
            "conclusion"
        ]
        
        actual_order = [s['key'] for s in response['sections']]
        
        if actual_order != expected_order:
            return False, f"Section order mismatch. Expected {expected_order}, got {actual_order}"
        
        return True, "OK"
    
    @staticmethod
    def validate_schema(response: Dict) -> Tuple[bool, List[str]]:
        """Validate complete schema compliance"""
        errors = []
        
        # Check meta
        if 'meta' not in response:
            errors.append("Missing 'meta' field")
        else:
            required_meta = ['version', 'content_hash', 'locale', 'generated_at']
            for field in required_meta:
                if field not in response['meta']:
                    errors.append(f"Missing meta.{field}")
        
        # Check context
        if 'context' not in response:
            errors.append("Missing 'context' field")
        else:
            required_context = ['zodiac', 'element', 'birth_time_known', 'interpretation_mode']
            for field in required_context:
                if field not in response['context']:
                    errors.append(f"Missing context.{field}")
        
        # Check sections structure
        if 'sections' not in response:
            errors.append("Missing 'sections' array")
        else:
            for idx, section in enumerate(response['sections']):
                if 'key' not in section:
                    errors.append(f"Section {idx} missing 'key'")
                if 'items' not in section:
                    errors.append(f"Section {idx} missing 'items'")
                else:
                    for item_idx, item in enumerate(section['items']):
                        if 'id' not in item:
                            errors.append(f"Section {section.get('key')}, item {item_idx} missing 'id'")
                        if 'layer' not in item:
                            errors.append(f"Section {section.get('key')}, item {item_idx} missing 'layer'")
                        if 'sentences' not in item:
                            errors.append(f"Section {section.get('key')}, item {item_idx} missing 'sentences'")
                        elif not isinstance(item['sentences'], list):
                            errors.append(f"Section {section.get('key')}, item {item_idx} sentences must be array")
                        elif len(item['sentences']) < 1 or len(item['sentences']) > 4:
                            errors.append(f"Section {section.get('key')}, item {item_idx} must have 1-4 sentences")
        
        if errors:
            return False, errors
        return True, []
    
    def validate_full_response(self, response: Dict) -> Dict:
        """
        Run all validation checks.
        Returns validation report.
        """
        report = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Schema validation
        schema_valid, schema_errors = self.validate_schema(response)
        if not schema_valid:
            report['valid'] = False
            report['errors'].extend(schema_errors)
            return report  # Cannot continue if schema invalid
        
        # Section order
        order_valid, order_msg = self.validate_section_order(response)
        if not order_valid:
            report['valid'] = False
            report['errors'].append(order_msg)
        
        # House logic
        house_valid, house_msg = self.validate_house_logic(response)
        if not house_valid:
            report['valid'] = False
            report['errors'].append(house_msg)
        
        # Sentence length validation
        for section in response['sections']:
            for item in section['items']:
                for sentence in item['sentences']:
                    length_valid, length_msg = self.validate_sentence_length(sentence)
                    if not length_valid:
                        report['warnings'].append(f"{item['id']}: {length_msg}")
        
        # Duplication check
        dup_valid, dup_list = self.validate_no_duplicates(response)
        if not dup_valid:
            report['valid'] = False
            report['errors'].append(f"Found {len(dup_list)} duplicate sentences")
            report['errors'].extend(dup_list[:5])  # Show first 5
        
        return report


# USAGE
if __name__ == "__main__":
    validator = ContentValidator()
    
    # Example response
    sample_response = {
        "meta": {
            "version": "v1.0.0",
            "content_hash": "abc123",
            "locale": "vi",
            "generated_at": "2026-02-06T15:00:00Z"
        },
        "context": {
            "zodiac": "Libra",
            "element": "Air",
            "birth_time_known": False,
            "interpretation_mode": "sign_based",
            "house_system": None
        },
        "sections": []
    }
    
    report = validator.validate_full_response(sample_response)
    print(f"Valid: {report['valid']}")
    print(f"Errors: {len(report['errors'])}")
    print(f"Warnings: {len(report['warnings'])}")
