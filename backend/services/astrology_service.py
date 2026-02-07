from __future__ import annotations
import os
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from models.schemas import (
    BirthInfo, CompatibilityDetails, NatalChart, PlanetPosition,
    NatalResponse, ResponseMeta, ZodiacMeta, ResultSection, ResultSectionId,
    InsightBlock, InsightBlockType, InsightEmphasis
)
from utils.compatibility_data import ELEMENT_COMPATIBILITY, SIGN_TRAITS, SUN_SIGN_RANGES

# 1. THIẾT LẬP CẤU HÌNH HỆ THỐNG
GEONAMES_USER = "century.boy"
os.environ["GEONAMES_USERNAME"] = GEONAMES_USER

from utils.compatibility_data import GENDER_TONE


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
                    planets_res.append(PlanetPosition(name=p.name, sign=p.sign, longitude=pos))
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


    def build_v2_natal_response(
        self, chart: NatalChart, person: BirthInfo
    ) -> NatalResponse:
        sun_sign = chart.sun_sign
        moon_sign = chart.moon_sign or "Unknown"
        rising_sign = chart.ascendant or "Unknown"
        
        # 1. Extract and Map Planets
        planets_map = {p.name: p.sign for p in chart.planets}
        mercury_sign = planets_map.get("Mercury", sun_sign)
        venus_sign = planets_map.get("Venus", sun_sign)
        mars_sign = planets_map.get("Mars", sun_sign)
        jupiter_sign = planets_map.get("Jupiter", sun_sign)
        saturn_sign = planets_map.get("Saturn", sun_sign)
        
        # 2. Dynamic Element Analysis (Premium Feature)
        element_counts = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        for p in chart.planets:
            e = self._element_of_sign(p.sign)
            if e in element_counts:
                # Weighted importance
                weight = 3 if p.name in ["Sun", "Moon"] else 2 if p.name == "Ascendant" else 1
                element_counts[e] += weight
        
        dominant_element = max(element_counts, key=element_counts.get)
        element_summary = ", ".join([f"{k}: {v}" for k, v in element_counts.items()])

        sections = []

        # 3. Meta Data
        meta = ResponseMeta(
            version="v2.1-premium",
            locale="vi",
            chartType="with_birth_time" if not person.time_unknown else "without_birth_time",
            zodiac=ZodiacMeta(
                sun=sun_sign,
                moon=chart.moon_sign,
                rising=chart.ascendant,
                element=dominant_element
            ),
            planets=chart.planets
        )

        # 4. Section: Energy Blueprint (Dynamic)
        sections.append(ResultSection(
            id=ResultSectionId.ENERGY_OVERVIEW,
            title_i18n="Bản Thiết Kế Năng Lượng (Premium)",
            summary=f"Bạn sở hữu cấu trúc năng lượng trội hệ {dominant_element}. Phân bổ: {element_summary}.",
            insights=[
                InsightBlock(type=InsightBlockType.DESCRIPTION, content=f"Mặt Trời tại {sun_sign} là pin năng lượng chính, thúc đẩy bạn hướng tới sự {self._trait_text(sun_sign).lower()}."),
                InsightBlock(type=InsightBlockType.PRINCIPLE, content=f"Mặt Trăng tại {moon_sign} điều phối thế giới nội tâm; bạn xử lý áp lực qua lăng kính của cung này.", emphasis=InsightEmphasis.HIGH),
                InsightBlock(type=InsightBlockType.ACTION, content=f"Ngày hôm nay, hãy tập trung vào các hoạt động thuộc nhóm {dominant_element} để tái tạo sức lao động.")
            ]
        ))

        # 5. Section: Soul Purpose & Destiny
        sections.append(ResultSection(
            id=ResultSectionId.LIFE_DIRECTION,
            title_i18n="Sứ Mệnh & Định Hướng Tâm Hồn",
            summary=f"Cung Mọc {rising_sign} và các hành tinh xã hội định hình lộ trình phát triển của bạn.",
            insights=[
                InsightBlock(type=InsightBlockType.DESCRIPTION, content=f"Cung Mọc {rising_sign} cho thấy 'chiếc mặt nạ' giúp bạn chiến thắng các thử thách ban đầu."),
                InsightBlock(type=InsightBlockType.PRINCIPLE, content=f"Mộc Tinh (Jupiter) tại {jupiter_sign} là chìa khóa mở ra sự may mắn thông qua việc mở rộng tư duy.", emphasis=InsightEmphasis.MEDIUM),
                InsightBlock(type=InsightBlockType.WARNING, content=f"Thổ Tinh {saturn_sign} nhắc nhở về những ranh giới và kỷ luật cần thiết để đạt tới thành công bền vững.", emphasis=InsightEmphasis.HIGH)
            ]
        ))

        # 6. Section: Intellect & Influence (Mercury)
        sections.append(ResultSection(
            id=ResultSectionId.CORE_PERSONALITY,
            title_i18n="Tư Duy & Tầm Ảnh Hưởng",
            summary=f"Phong cách giao tiếp và xử lý thông tin dựa trên Thủy Tinh tại {mercury_sign}.",
            insights=[
                InsightBlock(type=InsightBlockType.DESCRIPTION, content=f"Với Mercury {mercury_sign}, bạn có xu hướng truyền đạt ý tưởng một cách {NATAL_GUIDE.get(mercury_sign, {}).get('career', 'linh hoạt').lower()}."),
                InsightBlock(type=InsightBlockType.ACTION, content="Thực hành viết lách hoặc chia sẻ kiến thức để tối ưu hóa năng lượng Mercury.", emphasis=InsightEmphasis.MEDIUM)
            ]
        ))

        # 7. Section: Love & Intimacy (Venus/Mars)
        sections.append(ResultSection(
            id=ResultSectionId.LOVE_CONNECTION,
            title_i18n="Tình Yêu & Sự Gắn Kết (Premium)",
            summary=f"Sự kết hợp giữa Kim Tinh ({venus_sign}) và Hỏa Tinh ({mars_sign}) tạo nên bản sắc tình cảm của bạn.",
            insights=[
                InsightBlock(type=InsightBlockType.DESCRIPTION, content=f"Kim Tinh {venus_sign} định nghĩa cái đẹp và giá trị mà bạn tìm kiếm trong một người bạn đời."),
                InsightBlock(type=InsightBlockType.PRINCIPLE, content=f"Hỏa Tinh {mars_sign} là đam mê và cách bạn chủ động chinh phục mục tiêu tình cảm.", emphasis=InsightEmphasis.MEDIUM),
                InsightBlock(type=InsightBlockType.ACTION, content="Hãy thành thật với nhu cầu Venus để xây dựng mối quan hệ bền bỉ.")
            ]
        ))

        # 8. Planet Data Table
        sections.append(ResultSection(
            id=ResultSectionId.PLANET_POSITIONS,
            title_i18n="Bảng Tọa Độ Thiên Thể (Swiss Ephemeris)",
            summary="Dữ liệu thiên văn chính xác cao, hỗ trợ cho việc nghiên cứu sâu.",
            insights=[
                InsightBlock(type=InsightBlockType.DESCRIPTION, content=f"{p.name}: {p.sign} ({p.longitude:.2f}°) {'(R)' if getattr(p, 'retrograde', False) else ''}")
                for p in chart.planets
            ]
        ))

        # 9. Practical Recommendations
        sections.append(ResultSection(
            id=ResultSectionId.PRACTICAL_RECOMMENDATIONS,
            title_i18n="Khuyến Nghị Cá Nhân Hóa",
            summary="Các bước hành động cụ thể dựa trên cấu trúc bản đồ sao hiện hành.",
            insights=[
                InsightBlock(type=InsightBlockType.ACTION, content=f"Tối ưu hóa năng lực tiềm tàng của {dominant_element} qua các thói quen hàng ngày."),
                InsightBlock(type=InsightBlockType.ACTION, content=f"Học cách kiềm chế những xung động tiêu cực từ {mars_sign} khi gặp căng thẳng.", emphasis=InsightEmphasis.MEDIUM),
                InsightBlock(type=InsightBlockType.ACTION, content="Tham vấn chuyên gia về các chu kỳ transit quan trọng trong năm.")
            ]
        ))

        return NatalResponse(meta=meta, sections=sections)





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
