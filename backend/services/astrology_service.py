from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.schemas import BirthInfo, NatalChart, PlanetPosition, CompatibilityDetails
from utils.compatibility_data import (
    SUN_SIGN_RANGES,
    SIGN_TRAITS,
    ELEMENT_COMPATIBILITY,
    ASPECT_WEIGHTS,
    GENDER_TONE,
)

try:
    from kerykeion import AstrologicalSubject
    try:
        # Kerykeion 4.x location
        from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
    except Exception:
        # Older versions fallback
        from kerykeion.chart import KerykeionChartSVG
    KERYKEION_AVAILABLE = True
except Exception:
    KERYKEION_AVAILABLE = False

try:
    from flatlib.chart import Chart
    from flatlib.geopos import GeoPos
    from flatlib.datetime import Datetime
    from flatlib import const
    FLATLIB_AVAILABLE = True
except Exception:
    FLATLIB_AVAILABLE = False

@dataclass
class AstroResult:
    sun_sign: str
    moon_sign: Optional[str]
    ascendant: Optional[str]
    planets: list[PlanetPosition]
    svg_chart: Optional[str]

class AstrologyService:
    def __init__(self) -> None:
        pass

    def build_natal_chart(self, person: BirthInfo, lat: Optional[float], lon: Optional[float]) -> NatalChart:
        sun_sign = self._calculate_sun_sign(person.birth_date)

        if person.time_unknown or not person.birth_time:
            time_str = "12:00"
            ascendant = None
        else:
            time_str = person.birth_time
            ascendant = None

        moon_sign: Optional[str] = None
        planets: list[PlanetPosition] = []
        svg_chart: Optional[str] = None

        if KERYKEION_AVAILABLE and lat is not None and lon is not None:
            moon_sign, ascendant, planets, svg_chart = self._kerykeion_chart(
                person, time_str, lat, lon
            )
        elif FLATLIB_AVAILABLE and lat is not None and lon is not None:
            moon_sign, ascendant, planets = self._flatlib_chart(person, time_str, lat, lon)

        return NatalChart(
            name=person.name,
            sun_sign=sun_sign,
            moon_sign=moon_sign,
            ascendant=ascendant if not person.time_unknown else None,
            planets=planets,
            svg_chart=svg_chart,
        )

    def compatibility(self, a: NatalChart, b: NatalChart, gender_a: str, gender_b: str) -> CompatibilityDetails:
        element_score = self._element_score(a.sun_sign, b.sun_sign)
        moon_score = 0
        if a.moon_sign and b.moon_sign:
            moon_score = self._element_score(a.moon_sign, b.moon_sign)
        rising_score = 0
        if a.ascendant and b.ascendant:
            rising_score = self._element_score(a.ascendant, b.ascendant)

        aspect_score, aspect_notes = self._basic_aspects(a, b)

        base_score = int((element_score * 0.5) + (moon_score * 0.25) + (rising_score * 0.15) + (aspect_score * 0.10))
        base_score = max(30, min(95, base_score))

        tone = GENDER_TONE.get((gender_a, gender_b), "balanced")
        trait_a = SIGN_TRAITS.get(a.sun_sign, "").split("|")[-1]
        trait_b = SIGN_TRAITS.get(b.sun_sign, "").split("|")[-1]

        summary = f"{a.sun_sign} và {b.sun_sign} tạo nên sự kết nối {tone}, tập trung vào cùng nhau phát triển và tò mò tích cực."
        personality = f"{trait_a} {trait_b} Khi đi cùng nhau, hai bạn hòa trộn thế mạnh và cần tôn trọng nhịp sống của nhau."
        love_style = "Bạn gắn kết bằng sự chân thành, ổn định và những thói quen chung nuôi dưỡng niềm tin."
        career = "Hợp tác hiệu quả hơn khi vai trò rõ ràng và phản hồi thẳng thắn nhưng tinh tế."
        relationships = "Mối quan hệ bền vững khi bạn trân trọng khác biệt thay vì cố gắng đồng nhất."
        advice = "Dành thời gian trò chuyện định kỳ và giao tiếp cụ thể, nhất là khi căng thẳng."
        conflict_points = "Kỳ vọng lệch nhau và tốc độ ra quyết định khác biệt có thể gây va chạm nếu không nói rõ."
        activities = [
            "Lên kế hoạch một chuyến đi nhẹ nhàng",
            "Tạo playlist chung",
            "Đặt mục tiêu nhỏ cho tháng này",
        ]

        return CompatibilityDetails(
            score=base_score,
            summary=summary,
            personality=personality,
            love_style=love_style,
            career=career,
            relationships=relationships,
            advice=advice,
            conflict_points=conflict_points,
            recommended_activities=activities,
            aspects=aspect_notes,
        )

    def _calculate_sun_sign(self, birth_date: str) -> str:
        date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        for sign, (start, end) in SUN_SIGN_RANGES.items():
            if start <= (date_obj.month, date_obj.day) <= end:
                return sign
        return "Capricorn"

    def _element_score(self, sign_a: str, sign_b: str) -> int:
        element_a = SIGN_TRAITS.get(sign_a, "").split("|")[0]
        element_b = SIGN_TRAITS.get(sign_b, "").split("|")[0]
        return ELEMENT_COMPATIBILITY.get((element_a, element_b), 60)

    def _basic_aspects(self, a: NatalChart, b: NatalChart) -> tuple[int, list[str]]:
        notes: list[str] = []
        score = 70

        if a.sun_sign == b.moon_sign or b.sun_sign == a.moon_sign:
            score += ASPECT_WEIGHTS["sun_moon"]
            notes.append("Mặt Trời – Mặt Trăng hòa hợp giúp thấu hiểu cảm xúc.")

        venus_a = self._find_planet_sign(a.planets, "Venus")
        mars_b = self._find_planet_sign(b.planets, "Mars")
        if venus_a and mars_b and venus_a == mars_b:
            score += ASPECT_WEIGHTS["venus_mars"]
            notes.append("Sao Kim – Sao Hỏa đồng vị trí tăng sức hút và phản ứng hóa học.")

        if not notes:
            notes.append("Chưa có góc chiếu nổi bật; hãy tập trung vào lựa chọn hằng ngày và giao tiếp.")

        return score, notes

    def _find_planet_sign(self, planets: list[PlanetPosition], planet_name: str) -> Optional[str]:
        for planet in planets:
            if planet.name.lower() == planet_name.lower():
                return planet.sign
        return None

    def _kerykeion_chart(
        self, person: BirthInfo, time_str: str, lat: float, lon: float
    ) -> tuple[Optional[str], Optional[str], list[PlanetPosition], Optional[str]]:
        try:
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            hour, minute = [int(x) for x in time_str.split(":")]

            subject = AstrologicalSubject(
                name=person.name or "Anonymous",
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day,
                hour=hour,
                minute=minute,
                lat=lat,
                lon=lon,
                city=person.birth_place,
                nation="",
            )

            planets = []
            for planet_name, data in subject.planets.items():
                planets.append(
                    PlanetPosition(
                        name=planet_name,
                        sign=data["sign"],
                        degree=float(data["position"]),
                    )
                )

            moon_sign = subject.planets.get("Moon", {}).get("sign")
            ascendant = subject.houses.get("First", {}).get("sign")

            svg_chart = None
            try:
                svg_chart = KerykeionChartSVG(subject).makeSVG()
            except Exception:
                svg_chart = None

            return moon_sign, ascendant, planets, svg_chart
        except Exception:
            return None, None, [], None

    def _flatlib_chart(
        self, person: BirthInfo, time_str: str, lat: float, lon: float
    ) -> tuple[Optional[str], Optional[str], list[PlanetPosition]]:
        try:
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            dt = Datetime(date_obj.strftime("%Y/%m/%d"), time_str, "+00:00")
            chart = Chart(dt, GeoPos(lat, lon))

            moon_sign = chart.get(const.MOON).sign
            ascendant = chart.get(const.ASC).sign

            planets = []
            for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS]:
                planet = chart.get(planet_id)
                planets.append(
                    PlanetPosition(name=planet_id, sign=planet.sign, degree=float(planet.lon))
                )

            return moon_sign, ascendant, planets
        except Exception:
            return None, None, []
