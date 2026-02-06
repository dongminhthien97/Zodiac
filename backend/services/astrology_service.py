from __future__ import annotations
import os
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from models.schemas import BirthInfo, CompatibilityDetails, NatalChart, NatalInsights, PlanetPosition
from utils.compatibility_data import ELEMENT_COMPATIBILITY, SIGN_TRAITS, SUN_SIGN_RANGES

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


NATAL_GUIDE = {
    "Aries": {"love": "Yêu nhanh, rõ ràng và chủ động; cần đối tác tôn trọng không gian cá nhân.", "hobbies": "Thể thao tốc độ, hoạt động ngoài trời, thử thách mới.", "career": "Hợp vai trò tiên phong, bán hàng, quản lý dự án ngắn hạn.", "life_path": "Bài học lớn là kiên nhẫn và hoàn thiện điều đã bắt đầu."},
    "Taurus": {"love": "Tình cảm bền bỉ, coi trọng an toàn và sự nhất quán.", "hobbies": "Nấu ăn, nghệ thuật, làm vườn, trải nghiệm giác quan.", "career": "Mạnh ở tài chính, vận hành, các nghề cần độ ổn định cao.", "life_path": "Học cách linh hoạt khi môi trường thay đổi."},
    "Gemini": {"love": "Kết nối bằng trò chuyện và sự tò mò; cần cảm giác mới mẻ.", "hobbies": "Đọc, viết, podcast, workshop, du lịch ngắn ngày.", "career": "Phù hợp truyền thông, giáo dục, marketing, sản phẩm số.", "life_path": "Rèn khả năng tập trung sâu và cam kết dài hạn."},
    "Cancer": {"love": "Tình yêu chăm sóc và giàu cảm xúc; cần cảm giác được thấu hiểu.", "hobbies": "Gia đình, ẩm thực, decor nhà cửa, hoạt động chữa lành.", "career": "Hợp giáo dục, tư vấn, dịch vụ chăm sóc, nhân sự.", "life_path": "Đặt ranh giới cảm xúc để tránh quá tải."},
    "Leo": {"love": "Lãng mạn, hào phóng, muốn được ghi nhận và trân trọng.", "hobbies": "Biểu diễn, sáng tạo nội dung, sự kiện, nghệ thuật.", "career": "Mạnh ở lãnh đạo, sáng tạo, xây dựng thương hiệu cá nhân.", "life_path": "Cân bằng giữa cái tôi và tinh thần hợp tác."},
    "Virgo": {"love": "Yêu qua hành động thiết thực, quan tâm chi tiết nhỏ.", "hobbies": "Lập kế hoạch, đọc chuyên sâu, chăm sóc sức khỏe.", "career": "Xuất sắc trong phân tích dữ liệu, QA, vận hành hệ thống.", "life_path": "Giảm xu hướng cầu toàn, cho phép bản thân nghỉ ngơi."},
    "Libra": {"love": "Đề cao sự hòa hợp, công bằng và tinh tế trong giao tiếp.", "hobbies": "Thẩm mỹ, nghệ thuật, thời trang, hoạt động xã hội.", "career": "Phù hợp đối ngoại, thiết kế, luật, đàm phán, partnership.", "life_path": "Học ra quyết định dứt khoát, không quá phụ thuộc ý kiến ngoài."},
    "Scorpio": {"love": "Kết nối sâu, trung thành, cần sự tin tưởng tuyệt đối.", "hobbies": "Nghiên cứu tâm lý, điều tra, các chủ đề chiều sâu.", "career": "Hợp tài chính, phân tích rủi ro, nghiên cứu, chiến lược.", "life_path": "Buông kiểm soát quá mức để giữ cân bằng nội tâm."},
    "Sagittarius": {"love": "Yêu tự do, chân thật, thích cùng nhau khám phá.", "hobbies": "Du lịch, ngoại ngữ, triết học, thể thao ngoài trời.", "career": "Mạnh ở giáo dục, nội dung, kinh doanh quốc tế, du lịch.", "life_path": "Biến tầm nhìn lớn thành kế hoạch cụ thể."},
    "Capricorn": {"love": "Tình cảm chín chắn, bền bỉ và có trách nhiệm.", "hobbies": "Lập mục tiêu, xây dự án cá nhân, leo núi, đọc sách nghề.", "career": "Phù hợp quản trị, tài chính, kỹ thuật, vai trò xây nền tảng.", "life_path": "Mở lòng với cảm xúc thay vì chỉ tập trung thành tích."},
    "Aquarius": {"love": "Tình yêu dựa trên tri kỷ tinh thần và tôn trọng khác biệt.", "hobbies": "Công nghệ, cộng đồng, sáng tạo ý tưởng mới.", "career": "Hợp sản phẩm công nghệ, đổi mới, nghiên cứu xu hướng.", "life_path": "Kết nối lý tưởng tập thể với nhu cầu cá nhân."},
    "Pisces": {"love": "Lãng mạn, giàu cảm thông, trực giác mạnh.", "hobbies": "Âm nhạc, hội họa, thiền, hoạt động thiện nguyện.", "career": "Phù hợp nghệ thuật, tư vấn, chăm sóc tinh thần, sáng tạo.", "life_path": "Rèn cấu trúc và kỷ luật để bảo vệ năng lượng cảm xúc."},
}

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


    def build_natal_insights(self, chart: NatalChart) -> NatalInsights:
        sign = chart.sun_sign if chart.sun_sign in NATAL_GUIDE else "Capricorn"
        element = self._element_of_sign(sign)
        trait = self._trait_text(sign)
        guide = NATAL_GUIDE[sign]

        moon_note = f" Mặt Trăng ở {chart.moon_sign} cho thấy nhu cầu cảm xúc sâu bên trong." if chart.moon_sign else ""
        asc_note = f" Cung mọc {chart.ascendant} thể hiện ấn tượng đầu tiên bạn tạo ra với người khác." if chart.ascendant else ""

        return NatalInsights(
            overview=(
                f"Bạn thuộc nhóm {element} với Mặt Trời {sign}. Tổng thể năng lượng thiên về {trait.lower()}"
                f".{moon_note}{asc_note}"
            ),
            personality=(
                f"{sign} thường thể hiện phong cách sống rõ nét: {trait} "
                "Bạn có xu hướng phát triển mạnh khi môi trường tôn trọng giá trị cá nhân và nhịp sống riêng."
            ),
            love=guide["love"],
            hobbies=guide["hobbies"],
            career=guide["career"],
            life_path=guide["life_path"],
            strengths=[
                f"Khí chất đặc trưng của {sign}",
                "Khả năng tự quan sát và điều chỉnh hành vi",
                "Tiềm năng xây dựng các mối quan hệ bền vững khi giao tiếp rõ ràng",
            ],
            challenges=[
                "Dễ bị kéo giữa kỳ vọng cá nhân và kỳ vọng xã hội",
                "Có lúc phản ứng cảm xúc trước khi kịp phân tích đầy đủ",
            ],
            growth_areas=[
                "Lập mục tiêu theo quý để theo dõi tiến bộ ổn định",
                "Thiết lập thói quen phục hồi năng lượng (ngủ, vận động, tĩnh tâm)",
                "Rèn kỹ năng giao tiếp nhu cầu cá nhân một cách trực diện nhưng tinh tế",
            ],
            recommendations=[
                "Mỗi tuần dành 1 phiên self-review 20-30 phút",
                "Chọn 1 kỹ năng nghề nghiệp trọng tâm để nâng cấp trong 90 ngày",
                "Duy trì vòng tròn quan hệ chất lượng thay vì mở rộng quá nhanh",
            ],
        )

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
