"""
services/compatibility_transformers.py
--------------------------------------
Schema transformation layer.
Maps raw engine data to frontend-compatible Pydantic models.
No calculations, no AI, pure mapping and validation.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from datetime import datetime

from models.compatibility_schema import CompatibilityResponse, RelationshipSummary
from services.astrology_engine import PersonInput, AspectData, ChartData


class CompatibilityTransformer:
    """Transforms raw data to frontend-compatible schema."""
    
    @staticmethod
    def transform_to_response(
        scores: Dict[str, int],
        narrative: Optional[Dict[str, Any]] = None,
        person_a_name: str = "Person A",
        person_b_name: str = "Person B"
    ) -> CompatibilityResponse:
        """Transform scores and narrative to CompatibilityResponse.
        
        Args:
            scores: Calculated compatibility scores
            narrative: Optional AI-generated narrative
            person_a_name: Name of person A
            person_b_name: Name of person B
            
        Returns:
            Validated CompatibilityResponse
        """
        # Build relationship summary
        relationship_summary = CompatibilityTransformer._build_relationship_summary(
            scores, narrative, person_a_name, person_b_name
        )
        
        # Build qualitative analysis
        strengths = CompatibilityTransformer._build_strengths(scores, narrative)
        challenges = CompatibilityTransformer._build_challenges(scores, narrative)
        green_flags = CompatibilityTransformer._build_green_flags(scores, narrative)
        red_flags = CompatibilityTransformer._build_red_flags(scores, narrative)
        
        # Create response
        response = CompatibilityResponse(
            overall_score=scores["overall_score"],
            emotional_compatibility=scores["emotional_compatibility"],
            mental_compatibility=scores["mental_compatibility"],
            physical_chemistry=scores["physical_chemistry"],
            stability_score=scores["stability_score"],
            conflict_risk=scores["conflict_risk"],
            long_term_potential=scores["long_term_potential"],
            relationship_summary=relationship_summary,
            strengths=strengths,
            challenges=challenges,
            green_flags=green_flags,
            red_flags=red_flags
        )
        
        return response
    
    @staticmethod
    def _build_relationship_summary(
        scores: Dict[str, int],
        narrative: Optional[Dict[str, Any]],
        person_a_name: str,
        person_b_name: str
    ) -> RelationshipSummary:
        """Build relationship summary from scores and narrative."""
        if narrative and "summary" in narrative:
            overview = narrative["summary"]
        else:
            overview = f"Phân tích tương thích giữa {person_a_name} và {person_b_name} - Điểm tổng quan: {scores['overall_score']}/100"
        
        if narrative and "relationships" in narrative:
            core_dynamic = narrative["relationships"]
        else:
            core_dynamic = "Đang phân tích động lực cốt lõi của mối quan hệ."
        
        if narrative and "advice" in narrative:
            relationship_purpose = narrative["advice"]
        else:
            relationship_purpose = "Đang xác định mục đích và hướng phát triển của mối quan hệ."
        
        return RelationshipSummary(
            overview=overview,
            core_dynamic=core_dynamic,
            relationship_purpose=relationship_purpose
        )
    
    @staticmethod
    def _build_strengths(scores: Dict[str, int], narrative: Optional[Dict[str, Any]]) -> List[str]:
        """Build strengths list from scores and narrative."""
        strengths = []
        
        # Add strengths based on scores
        if scores["emotional_compatibility"] >= 70:
            strengths.append("Tương thích cảm xúc cao")
        if scores["mental_compatibility"] >= 70:
            strengths.append("Hiểu biết và chia sẻ tư duy")
        if scores["physical_chemistry"] >= 70:
            strengths.append("Hóa học thể chất mạnh mẽ")
        if scores["stability_score"] >= 70:
            strengths.append("Mối quan hệ ổn định")
        if scores["long_term_potential"] >= 70:
            strengths.append("Tiềm năng lâu dài tốt")
        
        # Add narrative strengths if available
        if narrative and "personality" in narrative:
            if isinstance(narrative["personality"], list):
                strengths.extend(narrative["personality"])
            else:
                strengths.append(narrative["personality"])
        
        # Add default strengths if list is empty
        if not strengths:
            strengths = [
                "Cả hai đều có tiềm năng phát triển tích cực",
                "Có khả năng học hỏi và thích nghi",
                "Có nền tảng tương thích cơ bản"
            ]
        
        return strengths
    
    @staticmethod
    def _build_challenges(scores: Dict[str, int], narrative: Optional[Dict[str, Any]]) -> List[str]:
        """Build challenges list from scores and narrative."""
        challenges = []
        
        # Add challenges based on scores
        if scores["emotional_compatibility"] < 50:
            challenges.append("Khó khăn trong kết nối cảm xúc")
        if scores["mental_compatibility"] < 50:
            challenges.append("Khác biệt trong tư duy và quan điểm")
        if scores["physical_chemistry"] < 50:
            challenges.append("Thiếu hóa học thể chất")
        if scores["stability_score"] < 50:
            challenges.append("Mối quan hệ thiếu ổn định")
        if scores["conflict_risk"] >= 60:
            challenges.append("Rủi ro xung đột cao")
        
        # Add narrative challenges if available
        if narrative and "conflict_points" in narrative:
            if isinstance(narrative["conflict_points"], list):
                challenges.extend(narrative["conflict_points"])
            else:
                challenges.append(narrative["conflict_points"])
        
        # Add default challenges if list is empty
        if not challenges:
            challenges = [
                "Cần thêm thời gian để hiểu nhau sâu sắc hơn",
                "Có thể gặp khó khăn trong giao tiếp ban đầu",
                "Cần xây dựng niềm tin lẫn nhau"
            ]
        
        return challenges
    
    @staticmethod
    def _build_green_flags(scores: Dict[str, int], narrative: Optional[Dict[str, Any]]) -> List[str]:
        """Build green flags list from scores and narrative."""
        green_flags = []
        
        # Add green flags based on scores
        if scores["emotional_compatibility"] >= 80:
            green_flags.append("Tương thích cảm xúc xuất sắc")
        if scores["mental_compatibility"] >= 80:
            green_flags.append("Hiểu biết sâu sắc về nhau")
        if scores["stability_score"] >= 80:
            green_flags.append("Mối quan hệ rất ổn định")
        if scores["long_term_potential"] >= 80:
            green_flags.append("Tiềm năng lâu dài rất tốt")
        
        # Add narrative green flags if available
        if narrative and "recommended_activities" in narrative:
            if isinstance(narrative["recommended_activities"], list):
                green_flags.extend(narrative["recommended_activities"])
            else:
                green_flags.append(narrative["recommended_activities"])
        
        # Add default green flags if list is empty
        if not green_flags:
            green_flags = [
                "Có tiềm năng tương thích cảm xúc",
                "Có khả năng hỗ trợ lẫn nhau",
                "Có xu hướng phát triển tích cực"
            ]
        
        return green_flags
    
    @staticmethod
    def _build_red_flags(scores: Dict[str, int], narrative: Optional[Dict[str, Any]]) -> List[str]:
        """Build red flags list from scores and narrative."""
        red_flags = []
        
        # Add red flags based on scores
        if scores["emotional_compatibility"] < 30:
            red_flags.append("Khó khăn nghiêm trọng trong kết nối cảm xúc")
        if scores["mental_compatibility"] < 30:
            red_flags.append("Khác biệt lớn trong tư duy và quan điểm")
        if scores["physical_chemistry"] < 30:
            red_flags.append("Thiếu hóa học thể chất nghiêm trọng")
        if scores["stability_score"] < 30:
            red_flags.append("Mối quan hệ rất bất ổn")
        if scores["conflict_risk"] >= 80:
            red_flags.append("Rủi ro xung đột rất cao")
        
        # Add narrative red flags if available
        if narrative and "aspects" in narrative:
            if isinstance(narrative["aspects"], list):
                red_flags.extend(narrative["aspects"])
            else:
                red_flags.append(narrative["aspects"])
        
        # Add default red flags if list is empty
        if not red_flags:
            red_flags = [
                "Cần thận trọng trong việc thể hiện cảm xúc",
                "Có thể xảy ra hiểu lầm trong giao tiếp",
                "Cần thời gian để xây dựng sự tin tưởng"
            ]
        
        return red_flags
    
    @staticmethod
    def create_fallback_response(person_a_name: str = "Person A", person_b_name: str = "Person B") -> CompatibilityResponse:
        """Create fallback response when AI fails."""
        scores = {
            "overall_score": 50,
            "emotional_compatibility": 50,
            "mental_compatibility": 50,
            "physical_chemistry": 50,
            "stability_score": 50,
            "conflict_risk": 50,
            "long_term_potential": 50
        }
        
        return CompatibilityTransformer.transform_to_response(
            scores=scores,
            narrative=None,
            person_a_name=person_a_name,
            person_b_name=person_b_name
        )
    
    @staticmethod
    def validate_response(response: CompatibilityResponse) -> bool:
        """Validate that response meets all requirements."""
        try:
            # Check all scores are integers between 0-100
            scores = [
                response.overall_score, response.emotional_compatibility,
                response.mental_compatibility, response.physical_chemistry,
                response.stability_score, response.conflict_risk, response.long_term_potential
            ]
            
            for score in scores:
                if not isinstance(score, int) or score < 0 or score > 100:
                    return False
            
            # Check all lists are non-empty
            lists_to_check = [
                response.strengths, response.challenges,
                response.green_flags, response.red_flags
            ]
            
            for lst in lists_to_check:
                if not lst or not all(isinstance(item, str) for item in lst):
                    return False
            
            # Check relationship summary
            summary = response.relationship_summary
            if not summary.overview or not summary.core_dynamic or not summary.relationship_purpose:
                return False
            
            return True
            
        except Exception:
            return False