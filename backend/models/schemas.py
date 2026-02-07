from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic import RootModel



class BirthInfo(BaseModel):
    name: Optional[str] = Field(default=None, max_length=80)
    gender: str = Field(default="other")
    birth_date: str = Field(..., description="YYYY-MM-DD")
    birth_time: Optional[str] = Field(default=None, description="HH:MM (24h)")
    time_unknown: bool = Field(default=False)
    birth_place: str = Field(..., description="City, Country")


    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v not in {"male", "female", "other"}:
            raise ValueError('gender must be one of: male, female, other')
        return v

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
    longitude: float
    degree: float | None = None


class NatalChart(BaseModel):
    name: Optional[str]
    sun_sign: str
    moon_sign: Optional[str]
    ascendant: Optional[str]
    planets: list[PlanetPosition]
    svg_chart: Optional[str]


# New chart API schemas
class Location(BaseModel):
    lat: float
    lon: float


class ChartRequest(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    time: Optional[str] = Field(default=None, description="HH:MM or null")
    timezone: str = Field(..., description="+HH:MM or -HH:MM")
    location: Location
    house_system: Optional[str] = Field(default=None, description="whole_sign | placidus | null")


class Aspect(BaseModel):
    body1: str
    body2: str
    type: str
    orb: float


class Houses(BaseModel):
    system: str
    cusps: list[float]
    ascendant: float
    midheaven: float


class ChartCoreResponse(BaseModel):
    mode: str  # NO_HOUSE | WITH_HOUSE
    planets: dict[str, PlanetPosition]
    points: dict[str, PlanetPosition]
    aspects: list[Aspect]
    houses: Houses | None


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
    ai_analysis: Optional[str] = None
    detailed_reasoning: Optional[str] = None


class CompatibilityResponse(BaseModel):
    generated_at: str
    person_a: NatalChart
    person_b: NatalChart
    details: CompatibilityDetails



from enum import Enum


class InsightBlockType(str, Enum):
    DESCRIPTION = "description"
    PRINCIPLE = "principle"
    WARNING = "warning"
    ACTION = "action"


class InsightEmphasis(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InsightBlock(BaseModel):
    type: InsightBlockType
    content: str
    emphasis: Optional[InsightEmphasis] = None


class ResultSectionId(str, Enum):
    ENERGY_OVERVIEW = "energy_overview"
    CORE_PERSONALITY = "core_personality"
    LOVE_CONNECTION = "love_connection"
    HOBBIES = "hobbies"
    CAREER_DIRECTION = "career_direction"
    LIFE_DIRECTION = "life_direction"
    STRENGTHS = "strengths"
    CHALLENGES = "challenges"
    GROWTH_SUGGESTIONS = "growth_suggestions"
    PRACTICAL_RECOMMENDATIONS = "practical_recommendations"
    PLANET_POSITIONS = "planet_positions"


class ResultSection(BaseModel):
    id: ResultSectionId
    title_i18n: str
    summary: str
    insights: list[InsightBlock]


class ZodiacMeta(BaseModel):
    sun: str
    moon: Optional[str] = None
    rising: Optional[str] = None
    element: str


class ResponseMeta(BaseModel):
    version: str = "v2"
    locale: str = "vi"
    chartType: str = "with_birth_time"
    zodiac: ZodiacMeta
    planets: list[PlanetPosition] = Field(default_factory=list)


class NatalResponse(BaseModel):
    meta: ResponseMeta
    sections: list[ResultSection]

class StandardReportResponse(BaseModel):
    """Standard format report response - plain text output"""
    report: str
    generated_at: str
    chart_data: NatalChart

