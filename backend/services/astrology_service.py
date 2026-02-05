from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from models.schemas import BirthInfo, CompatibilityDetails, NatalChart, PlanetPosition
from utils.compatibility_data import ELEMENT_COMPATIBILITY, SIGN_TRAITS, SUN_SIGN_RANGES

# 1. THIẾT LẬP CẤU HÌNH HỆ THỐNG
GEONAMES_USER = "century.boy"
os.environ["GEONAMES_USERNAME"] = GEONAMES_USER

# Thư viện Kerykeion
try:
    from kerykeion import AstrologicalSubject, settings as kerykeion_settings

    if kerykeion_settings:
        kerykeion_settings.GEONAMES_USERNAME = GEONAMES_USER

    try:
        from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG
    except ImportError:
        try:
            from kerykeion.chart import KerykeionChartSVG
        except ImportError:
            KerykeionChartSVG = None

    KERYKEION_AVAILABLE = True
except Exception as e:
    logging.error(f"Kerykeion initialization failed: {e}")
    KERYKEION_AVAILABLE = False


class AstrologyService:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def build_natal_chart(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float], tz_name: Optional[str] = None
    ) -> NatalChart:
        self._logger.debug(f"Đang xử lý Natal cho: {person.name} tại {lat}, {lon}")

        sun_sign = self._calculate_sun_sign(person.birth_date)
        time_str = person.birth_time if (person.birth_time and not person.time_unknown) else "12:00"

        moon_sign, ascendant, planets, svg_chart = None, None, [], None

        if KERYKEION_AVAILABLE and lat is not None and lon is not None:
            moon_sign, ascendant, planets, svg_chart = self._kerykeion_chart(person, time_str, lat, lon)

        natal = NatalChart(
            name=person.name,
            sun_sign=sun_sign or "Unknown",
            moon_sign=moon_sign,
            ascendant=ascendant if not person.time_unknown else None,
            planets=planets,
            svg_chart=svg_chart,
        )

        if not natal.svg_chart:
            natal.svg_chart = self._build_fallback_svg(natal, person.time_unknown)

        return natal

    def _kerykeion_chart(
        self, person: BirthInfo, time_str: str, lat: float, lon: float
    ) -> tuple[Optional[str], Optional[str], list[PlanetPosition], Optional[str]]:
        try:
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            hour, minute = [int(x) for x in time_str.split(":")]

            raw_name = person.name or "User"
            safe_name = "".join(c for c in raw_name if c.isalnum()) or "User"

            subject = AstrologicalSubject(
                name=safe_name,
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day,
                hour=hour,
                minute=minute,
                city=person.birth_place or "Unknown",
                lat=lat,
                lng=lon,
            )

            planets_res: list[PlanetPosition] = []
            moon_sign = None
            if hasattr(subject, "planets_list"):
                for p in subject.planets_list:
                    pos = float(p.abs_pos) if hasattr(p, "abs_pos") else 0.0
                    planets_res.append(PlanetPosition(name=p.name, sign=p.sign, degree=pos))
                    if p.name == "Moon":
                        moon_sign = p.sign

            ascendant = subject.houses_list[0].sign if getattr(subject, "houses_list", []) else None

            svg_data = None
            if KerykeionChartSVG:
                try:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        chart_instance = KerykeionChartSVG(
                            subject,
                            chart_type="Natal",
                            new_output_directory=tmp_dir,
                        )
                        chart_instance.makeSVG()

                        svg_candidates = sorted(
                            Path(tmp_dir).glob("*.svg"),
                            key=lambda p: p.stat().st_mtime,
                            reverse=True,
                        )
                        if svg_candidates:
                            svg_data = svg_candidates[0].read_text(encoding="utf-8")
                        else:
                            self._logger.warning("Kerykeion không tạo file SVG trong thư mục tạm")
                except Exception as e:
                    self._logger.error(f"SVG Process Error: {e}")

            return moon_sign, ascendant, planets_res, svg_data

        except Exception as e:
            self._logger.exception(f"Kerykeion calculation failed: {e}")
            return None, None, [], None

    def _calculate_sun_sign(self, birth_date: str) -> str:
        try:
            date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
            for sign, (start, end) in SUN_SIGN_RANGES.items():
                if start <= (date_obj.month, date_obj.day) <= end:
                    return sign
        except Exception:
            pass
        return "Capricorn"

    def compatibility(self, a: NatalChart, b: NatalChart, gender_a: str, gender_b: str) -> CompatibilityDetails:
        element_score = self._element_score(a.sun_sign, b.sun_sign)
        cross_aspects = self._cross_chart_aspects(a.planets, b.planets)

        aspect_bonus = sum(item["weight"] for item in cross_aspects[:6])
        final_score = max(40, min(99, element_score + aspect_bonus))

        dominant_a = self._dominant_element(a.planets, a.sun_sign)
        dominant_b = self._dominant_element(b.planets, b.sun_sign)
        relationship_tone = self._relationship_tone(final_score)

        summary = (
            f"Tương hợp thực tế dựa trên lá số: {a.sun_sign}/{b.sun_sign}, "
            f"điểm nền nguyên tố {element_score} và tương tác góc chiếu +{aspect_bonus}."
        )

        personality = (
            f"Người A thiên {dominant_a}, người B thiên {dominant_b}. "
            f"Mức phối hợp hiện tại thuộc nhóm {relationship_tone}."
        )

        love_style = self._love_style_from_aspects(cross_aspects, dominant_a, dominant_b)
        career = self._career_style_from_elements(dominant_a, dominant_b)
        relationships = self._relationships_note(cross_aspects)
        conflict_points = self._conflict_points(cross_aspects, dominant_a, dominant_b)
        advice = self._advice_from_data(cross_aspects, final_score)

        return CompatibilityDetails(
            score=final_score,
            summary=summary,
            personality=personality,
            love_style=love_style,
            career=career,
            relationships=relationships,
            conflict_points=conflict_points,
            advice=advice,
            recommended_activities=self._recommended_activities(dominant_a, dominant_b),
            aspects=[item["label"] for item in cross_aspects[:8]]
            or ["Chưa đủ dữ liệu hành tinh để tính góc chiếu chi tiết"],
        )

    def _element_of_sign(self, sign: str) -> str:
        return SIGN_TRAITS.get(sign, "Unknown|").split("|")[0] or "Unknown"

    def _element_score(self, sign_a: str, sign_b: str) -> int:
        element_a = self._element_of_sign(sign_a)
        element_b = self._element_of_sign(sign_b)
        return ELEMENT_COMPATIBILITY.get((element_a, element_b), 60)

    def _dominant_element(self, planets: list[PlanetPosition], fallback_sign: str) -> str:
        if not planets:
            return self._element_of_sign(fallback_sign)

        counters: dict[str, int] = {}
        for p in planets:
            e = self._element_of_sign(p.sign)
            counters[e] = counters.get(e, 0) + 1
        return max(counters, key=counters.get)

    def _cross_chart_aspects(self, a_planets: list[PlanetPosition], b_planets: list[PlanetPosition]) -> list[dict]:
        if not a_planets or not b_planets:
            return []

        aspect_defs = [
            ("Conjunction", 0, 8, 4),
            ("Sextile", 60, 4, 2),
            ("Square", 90, 6, -2),
            ("Trine", 120, 6, 3),
            ("Opposition", 180, 8, -3),
        ]

        results = []
        for pa in a_planets:
            for pb in b_planets:
                delta = abs(pa.degree - pb.degree)
                if delta > 180:
                    delta = 360 - delta

                for name, target, orb, weight in aspect_defs:
                    if abs(delta - target) <= orb:
                        results.append(
                            {
                                "label": f"{pa.name} {name} {pb.name} (orb {abs(delta-target):.1f}°)",
                                "weight": weight,
                                "challenging": weight < 0,
                            }
                        )
                        break

        results.sort(key=lambda x: abs(x["weight"]), reverse=True)
        return results

    def _relationship_tone(self, score: int) -> str:
        if score >= 85:
            return "rất hòa hợp"
        if score >= 72:
            return "khá hòa hợp"
        if score >= 60:
            return "cần điều chỉnh"
        return "nhiều khác biệt"

    def _love_style_from_aspects(self, aspects: list[dict], dominant_a: str, dominant_b: str) -> str:
        supportive = sum(1 for a in aspects[:8] if not a["challenging"])
        challenging = sum(1 for a in aspects[:8] if a["challenging"])
        return (
            f"Trong tình cảm, năng lượng chính là {dominant_a}/{dominant_b}. "
            f"Góc thuận: {supportive}, góc thử thách: {challenging}."
        )

    def _career_style_from_elements(self, element_a: str, element_b: str) -> str:
        return (
            f"Trong công việc, tổ hợp {element_a} - {element_b} phù hợp khi phân vai rõ ràng, "
            "định nghĩa KPI và cadence trao đổi cố định."
        )

    def _relationships_note(self, aspects: list[dict]) -> str:
        if not aspects:
            return "Quan hệ được đánh giá từ dữ liệu nền (chưa đủ giờ sinh/planet detail để mở rộng)."

        top = ", ".join(a["label"] for a in aspects[:3])
        return f"Các tương tác nổi bật hiện tại: {top}."

    def _conflict_points(self, aspects: list[dict], element_a: str, element_b: str) -> str:
        hard = [a["label"] for a in aspects if a["challenging"]][:3]
        if hard:
            return f"Điểm dễ mâu thuẫn đến từ: {', '.join(hard)}."
        return f"Mâu thuẫn chủ yếu đến từ khác biệt nhịp quyết định giữa {element_a} và {element_b}."

    def _advice_from_data(self, aspects: list[dict], score: int) -> str:
        if score >= 80:
            return "Giữ nhịp giao tiếp đều; tận dụng các góc thuận để cùng triển khai mục tiêu dài hạn."
        if any(a["challenging"] for a in aspects[:6]):
            return "Ưu tiên nguyên tắc tranh luận không công kích cá nhân và chốt quyết định theo từng bước nhỏ."
        return "Tăng thời gian chia sẻ kỳ vọng và rà soát cảm xúc định kỳ mỗi tuần."

    def _recommended_activities(self, element_a: str, element_b: str) -> list[str]:
        options = {
            "Fire": "Hoạt động thể chất ngoài trời",
            "Earth": "Lập kế hoạch tài chính hoặc dự án cá nhân",
            "Air": "Workshop sáng tạo hoặc thảo luận sách/phim",
            "Water": "Hoạt động nghệ thuật hoặc mindfulness",
            "Unknown": "Đi dạo và trò chuyện định kỳ",
        }
        return [
            options.get(element_a, options["Unknown"]),
            options.get(element_b, options["Unknown"]),
            "Du lịch ngắn ngày để làm mới kết nối",
        ]

    def _build_fallback_svg(self, chart: NatalChart, time_unknown: bool) -> str:
        note = "Giờ sinh chưa rõ: dùng mốc 12:00 để ước lượng." if time_unknown else "Dữ liệu sinh đầy đủ."
        planets = ", ".join(f"{p.name}:{p.sign}" for p in chart.planets[:8]) or "Không có dữ liệu hành tinh chi tiết"

        lines = [
            f"Mặt Trời: {chart.sun_sign}",
            f"Mặt Trăng: {chart.moon_sign or 'Chưa xác định'}",
            f"Cung mọc: {chart.ascendant or 'Chưa xác định'}",
            note,
            planets,
        ]

        y = 30
        text_nodes = []
        for line in lines:
            safe_line = (
                line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            text_nodes.append(
                f'<text x="20" y="{y}" fill="#E5E7EB" font-size="14" font-family="Arial">{safe_line}</text>'
            )
            y += 26

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="220" viewBox="0 0 720 220">'
            '<rect width="720" height="220" rx="16" fill="#111827"/>'
            '<text x="20" y="20" fill="#F472B6" font-size="16" font-family="Arial">Tóm tắt lá số (fallback)</text>'
            + "".join(text_nodes)
            + "</svg>"
        )
