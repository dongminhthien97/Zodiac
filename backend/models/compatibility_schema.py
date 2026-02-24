"""
models/compatibility_schema.py
------------------------------
Pydantic schemas for compatibility analysis response.
Ensures clean contract between backend and frontend.
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field, validator


class RelationshipSummary(BaseModel):
    """Summary of relationship dynamics."""
    overview: str = Field(..., description="Overall relationship overview")
    core_dynamic: str = Field(..., description="Core relationship dynamic")
    relationship_purpose: str = Field(..., description="Purpose and direction of relationship")


class CompatibilityResponse(BaseModel):
    """Complete compatibility analysis response."""
    # Core scores (0-100)
    overall_score: int = Field(..., ge=0, le=100, description="Overall compatibility score")
    emotional_compatibility: int = Field(..., ge=0, le=100, description="Emotional compatibility score")
    mental_compatibility: int = Field(..., ge=0, le=100, description="Mental compatibility score")
    physical_chemistry: int = Field(..., ge=0, le=100, description="Physical chemistry score")
    stability_score: int = Field(..., ge=0, le=100, description="Relationship stability score")
    conflict_risk: int = Field(..., ge=0, le=100, description="Conflict risk score")
    long_term_potential: int = Field(..., ge=0, le=100, description="Long-term potential score")
    
    # Relationship analysis
    relationship_summary: RelationshipSummary = Field(..., description="Structured relationship summary")
    
    # Qualitative analysis
    strengths: List[str] = Field(..., description="List of relationship strengths")
    challenges: List[str] = Field(..., description="List of relationship challenges")
    green_flags: List[str] = Field(..., description="Positive indicators")
    red_flags: List[str] = Field(..., description="Potential warning signs")
    
    @validator('strengths', 'challenges', 'green_flags', 'red_flags')
    def validate_lists(cls, v):
        """Ensure lists are not empty and contain only strings."""
        if not v:
            raise ValueError("Lists cannot be empty")
        if not all(isinstance(item, str) for item in v):
            raise ValueError("All list items must be strings")
        return v
    
    @validator('overall_score', 'emotional_compatibility', 'mental_compatibility', 
               'physical_chemistry', 'stability_score', 'conflict_risk', 'long_term_potential')
    def validate_scores(cls, v):
        """Ensure all scores are integers between 0-100."""
        if not isinstance(v, int):
            raise ValueError("Scores must be integers")
        if v < 0 or v > 100:
            raise ValueError("Scores must be between 0 and 100")
        return v
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            int: lambda v: int(v),  # Ensure integers stay as integers
        }
        schema_extra = {
            "example": {
                "overall_score": 75,
                "emotional_compatibility": 80,
                "mental_compatibility": 70,
                "physical_chemistry": 85,
                "stability_score": 65,
                "conflict_risk": 30,
                "long_term_potential": 72,
                "relationship_summary": {
                    "overview": "Harmonious connection with strong emotional bond",
                    "core_dynamic": "Complementary energies with mutual support",
                    "relationship_purpose": "Growth and mutual understanding"
                },
                "strengths": ["Shared values", "Good communication", "Emotional support"],
                "challenges": ["Different communication styles", "Need for compromise"],
                "green_flags": ["Mutual respect", "Shared goals", "Emotional intelligence"],
                "red_flags": ["Trust issues", "Communication gaps"]
            }
        }