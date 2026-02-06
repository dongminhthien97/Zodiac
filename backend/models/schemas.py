from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator



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


class NatalInsights(BaseModel):
    overview: str = "Tổng quan bản đồ sao của bạn đang được cập nhật chi tiết."
    personality: str = "Mặt Trời thể hiện bản ngã cốt lõi và phong cách thể hiện cá nhân."
    love: str = "Thông tin tình yêu đang được cập nhật từ dữ liệu cung hoàng đạo."
    hobbies: str = "Sở thích phù hợp đang được tổng hợp từ năng lượng cung của bạn."
    career: str = "Định hướng nghề nghiệp sẽ được gợi ý theo thế mạnh bản đồ sao."
    life_path: str = "Lộ trình phát triển cuộc sống đang được đề xuất."
    strengths: list[str] = Field(default_factory=list)
    challenges: list[str] = Field(default_factory=list)
    growth_areas: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class NatalResponse(BaseModel):
    generated_at: str
    person: NatalChart
    insights: NatalInsights
