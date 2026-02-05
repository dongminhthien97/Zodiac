from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator

Gender = Literal["male", "female", "other"]


class BirthInfo(BaseModel):
    name: Optional[str] = Field(default=None, max_length=80)
    gender: Gender = Field(default="other")
    birth_date: str = Field(..., description="YYYY-MM-DD")
    birth_time: Optional[str] = Field(default=None, description="HH:MM (24h)")
    time_unknown: bool = Field(default=False)
    birth_place: str = Field(..., description="City, Country")

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: str) -> str:
        if len(v) != 10 or v[4] != "-" or v[7] != "-":
            raise ValueError("birth_date must be in YYYY-MM-DD format")
        return v

    @field_validator("birth_time")
    @classmethod
    def validate_birth_time(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) != 5 or v[2] != ":":
            raise ValueError("birth_time must be in HH:MM format")
        return v


class CompatibilityRequest(BaseModel):
    person_a: BirthInfo
    person_b: BirthInfo


class NatalRequest(BaseModel):
    person: BirthInfo


class PlanetPosition(BaseModel):
    name: str
    sign: str
    degree: float


class NatalChart(BaseModel):
    name: Optional[str]
    sun_sign: str
    moon_sign: Optional[str]
    ascendant: Optional[str]
    planets: list[PlanetPosition]
    svg_chart: Optional[str]


class CompatibilityDetails(BaseModel):
    score: int
    summary: str
    personality: str
    love_style: str
    career: str
    relationships: str
    advice: str
    conflict_points: str
    recommended_activities: list[str]
    aspects: list[str]


class CompatibilityResponse(BaseModel):
    generated_at: str
    person_a: NatalChart
    person_b: NatalChart
    details: CompatibilityDetails


class NatalResponse(BaseModel):
    generated_at: str
    person: NatalChart
