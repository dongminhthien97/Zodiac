﻿from __future__ import annotations

import os
import logging
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

# 1. THIẾT LẬP CẤU HÌNH HỆ THỐNG
GEONAMES_USER = "century.boy"
os.environ["GEONAMES_USERNAME"] = GEONAMES_USER

from models.schemas import BirthInfo, NatalChart, PlanetPosition, CompatibilityDetails
from utils.compatibility_data import (
    SUN_SIGN_RANGES,
    SIGN_TRAITS,
    ELEMENT_COMPATIBILITY,
    GENDER_TONE,
)

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

    # -------------------------
    # Public API
    # -------------------------
    def build_natal_chart(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float], tz_name: Optional[str] = None
    ) -> NatalChart:
        self._logger.debug(f"Đang xử lý Natal cho: {person.name} tại {lat}, {lon}")

        sun_sign = self._calculate_sun_sign(person.birth_date)
        time_str = person.birth_time if (person.birth_time and not person.time_unknown) else "12:00"

        moon_sign, ascendant, planets, svg_chart = None, None, [], None

        if KERYKEION_AVAILABLE and lat is not None and lon is not None:
            moon_sign, ascendant, planets, svg_chart = self._kerykeion_chart(person, time_str, lat, lon)

        return NatalChart(
            name=person.name,
            sun_sign=sun_sign or "Unknown",
            moon_sign=moon_sign,
            ascendant=ascendant if not person.time_unknown else None,
            planets=planets,
            svg_chart=svg_chart,
        )

    # -------------------------
    # Kerykeion Integration (Fixed Search Path)
    # -------------------------
    def _kerykeion_chart(
        self, person: BirthInfo, time_str: str, lat: float, lon: float
    ) -> tuple[Optional[str], Optional[str], list[PlanetPosition], Optional[str]]:
        try:
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            hour, minute = [int(x) for x in time_str.split(":")]
            
            # Khử dấu: "Đồng Minh Thiện" -> "DongMinhThien"
            safe_name = "".join(c for c in person.name if c.isalnum()) or "User"
            
            subject = AstrologicalSubject(
                name=safe_name, 
                year=date_obj.year, 
                month=date_obj.month, 
                day=date_obj.day,
                hour=hour, 
                minute=minute, 
                city=person.birth_place or "Unknown", 
                lat=lat, 
                lng=lon
            )

            # 1. Trích xuất dữ liệu hành tinh
            planets_res = []
            moon_sign = None
            if hasattr(subject, "planets_list"):
                for p in subject.planets_list:
                    pos = float(p.abs_pos) if hasattr(p, 'abs_pos') else 0.0
                    planets_res.append(PlanetPosition(name=p.name, sign=p.sign, degree=pos))
                    if p.name == "Moon":
                        moon_sign = p.sign
            
            ascendant = subject.houses_list[0].sign if getattr(subject, "houses_list", []) else None

            # 2. Tạo và đọc SVG (Logic tìm kiếm đa điểm)
            svg_data = None
            if KerykeionChartSVG:
                try:
                    # Tạo chart
                    chart_instance = KerykeionChartSVG(subject, chart_type="Natal")
                    chart_instance.makeSVG()

                    # --- Search Logic ---
                    search_dirs = [Path.cwd(), Path.home()]
                    search_pattern = f"*{safe_name}*.svg"
                    
                    found_file = None
                    
                    for directory in search_dirs:
                        self._logger.debug(f"🔍 Searching for SVG in: {directory} with pattern: {search_pattern}")
                        try:
                            files = list(directory.glob(search_pattern))
                            if files:
                                files.sort(key=os.path.getmtime, reverse=True)
                                found_file = files[0]
                                self._logger.info(f"✅ Found SVG file at: {found_file}")
                                break
                        except Exception as e:
                            self._logger.warning(f"⚠️ Error searching in {directory}: {e}")

                    if found_file:
                        try:
                            svg_data = found_file.read_text(encoding="utf-8")
                            os.remove(found_file)
                            self._logger.info(f"🧹 Cleaned up SVG file: {found_file.name}")
                        except Exception as read_err:
                            self._logger.error(f"❌ Failed to read/delete file: {read_err}")
                    else:
                        self._logger.error(f"❌ SVG Generated but NOT FOUND in: {[str(d) for d in search_dirs]}")

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
        except:
            pass
        return "Capricorn"

    # -------------------------
    # Compatibility Logic (Đã sửa lỗi thiếu trường)
    # -------------------------
    def compatibility(self, a: NatalChart, b: NatalChart, gender_a: str, gender_b: str) -> CompatibilityDetails:
        element_score = self._element_score(a.sun_sign, b.sun_sign)
        trait_a = self._trait_text(a.sun_sign)
        trait_b = self._trait_text(b.sun_sign)
        element_a = self._element_of_sign(a.sun_sign)
        element_b = self._element_of_sign(b.sun_sign)
        tone = GENDER_TONE.get((gender_a, gender_b), "cân bằng")

        strengths = self._strength_phrase(element_score)
        challenge = self._challenge_phrase(element_a, element_b)

        return CompatibilityDetails(
            score=element_score,
            summary=(
                f"{a.sun_sign} ({element_a}) và {b.sun_sign} ({element_b}) có mức hòa hợp {element_score}%. "
                f"Năng lượng tổng thể thiên về {tone}."
            ),
            personality=f"Người A {trait_a} Trong khi đó người B {trait_b}",
            love_style=f"Khi yêu, cặp đôi này phát huy {strengths.lower()} nhưng cần chú ý {challenge.lower()}.",
            career=(
                f"Trong công việc, {element_a} kết hợp với {element_b} phù hợp cho vai trò phân chia rõ ràng: "
                "một người dẫn dắt, một người duy trì nhịp độ."
            ),
            relationships=(
                f"Mối quan hệ có sắc thái {tone}, phù hợp khi cả hai thống nhất nguyên tắc giao tiếp "
                "và phản hồi định kỳ."
            ),
            conflict_points=challenge,
            advice=(
                "Ưu tiên đối thoại thẳng thắn, đặt lịch trao đổi cố định mỗi tuần và luôn tôn trọng khác biệt cảm xúc."
            ),
            recommended_activities=self._recommended_activities(element_a, element_b),
            aspects=[
                f"Sun {a.sun_sign} - Sun {b.sun_sign}",
                f"Element pairing: {element_a}/{element_b}",
                f"Relationship tone: {tone}",
            ],
        )


    def _element_of_sign(self, sign: str) -> str:
        return SIGN_TRAITS.get(sign, "Unknown|").split("|")[0] or "Unknown"

    def _trait_text(self, sign: str) -> str:
        parts = SIGN_TRAITS.get(sign, "Unknown|khó xác định").split("|", 1)
        return parts[1] if len(parts) > 1 else "khó xác định"

    def _strength_phrase(self, score: int) -> str:
        if score >= 82:
            return "độ đồng điệu rất cao"
        if score >= 72:
            return "độ tương tác tốt"
        return "tiềm năng phát triển nếu cùng nỗ lực"

    def _challenge_phrase(self, element_a: str, element_b: str) -> str:
        if element_a == element_b:
            return "xu hướng phản chiếu cảm xúc quá giống nhau"
        if {element_a, element_b} == {"Fire", "Water"}:
            return "nhịp cảm xúc nóng - lạnh thay đổi nhanh"
        if {element_a, element_b} == {"Air", "Earth"}:
            return "khác biệt giữa tư duy linh hoạt và nhu cầu ổn định"
        return "khác biệt về tốc độ ra quyết định"

    def _recommended_activities(self, element_a: str, element_b: str) -> list[str]:
        options = {
            "Fire": "Hoạt động thể chất ngoài trời",
            "Earth": "Lập kế hoạch tài chính hoặc dự án cá nhân",
            "Air": "Workshop sáng tạo hoặc thảo luận sách/phim",
            "Water": "Hoạt động nghệ thuật hoặc mindfulness",
        }
        return [
            options.get(element_a, "Đi dạo và trò chuyện"),
            options.get(element_b, "Đi dạo và trò chuyện"),
            "Du lịch ngắn ngày để làm mới kết nối",
        ]

    def _element_score(self, sign_a: str, sign_b: str) -> int:
        element_a = SIGN_TRAITS.get(sign_a, "").split("|")[0]
        element_b = SIGN_TRAITS.get(sign_b, "").split("|")[0]
        return ELEMENT_COMPATIBILITY.get((element_a, element_b), 60)
