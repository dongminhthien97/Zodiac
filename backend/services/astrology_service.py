from __future__ import annotations
import os
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import traceback

from models.schemas import (
    BirthInfo, CompatibilityDetails, NatalChart, PlanetPosition,
    NatalResponse, ResponseMeta, ZodiacMeta, ResultSection, ResultSectionId,
    InsightBlock, InsightBlockType, InsightEmphasis, StandardReportResponse
)
from utils.compatibility_data import ELEMENT_COMPATIBILITY, SIGN_TRAITS, SUN_SIGN_RANGES
from google import genai

# 1. THIẾT LẬP CẤU HÌNH HỆ THỐNG
GEONAMES_USER = "century.boy"
os.environ["GEONAMES_USERNAME"] = GEONAMES_USER

from utils.compatibility_data import GENDER_TONE

logger = logging.getLogger(__name__)


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
        # Initialize Google AI client for enhanced compatibility analysis
        try:
            self.ai_client = genai.Client()
        except Exception as e:
            self._logger.warning(f"Google AI client initialization failed: {e}")
            self.ai_client = None

    def build_natal_chart(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float], tz_name: Optional[str] = None
    ) -> NatalChart:
        """Build natal chart with fault-tolerant chart generation"""
        self._logger.debug(f"Building natal chart for: {person.name} at {lat}, {lon}")
        
        try:
            sun_sign = self._calculate_sun_sign(person.birth_date)
            time_str = person.birth_time if (person.birth_time and not person.time_unknown) else "12:00"

            moon_sign, ascendant, planets, svg_chart = None, None, [], None

            # Only attempt Kerykeion if coordinates are available
            if KERYKEION_AVAILABLE and lat is not None and lon is not None:
                try:
                    moon_sign, ascendant, planets, svg_chart = self._kerykeion_chart(person, time_str, lat, lon)
                    self._logger.info(f"Kerykeion chart generation successful for {person.name}")
                except Exception as e:
                    self._logger.warning(f"Kerykeion chart generation failed for {person.name}: {e}")
                    # Continue without Kerykeion data - this is not fatal
                    moon_sign, ascendant, planets, svg_chart = None, None, [], None

            # Build basic chart with available data
            natal = NatalChart(
                name=person.name,
                sun_sign=sun_sign or "Unknown",
                moon_sign=moon_sign,
                ascendant=ascendant if not person.time_unknown else None,
                planets=planets,
                svg_chart=svg_chart,
            )

            # Only generate fallback SVG if we don't have one and time is unknown
            if not natal.svg_chart and person.time_unknown:
                try:
                    natal.svg_chart = self._build_fallback_svg(natal, person.time_unknown)
                    self._logger.info(f"Generated fallback SVG for {person.name}")
                except Exception as e:
                    self._logger.warning(f"Fallback SVG generation failed for {person.name}: {e}")
                    # Set to None instead of crashing
                    natal.svg_chart = None

            return natal
            
        except Exception as e:
            self._logger.error(f"Critical error in build_natal_chart for {person.name}: {e}")
            # Return minimal chart instead of crashing
            return NatalChart(
                name=person.name,
                sun_sign=self._calculate_sun_sign(person.birth_date) or "Unknown",
                moon_sign=None,
                ascendant=None,
                planets=[],
                svg_chart=None,
            )

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

    def build_standard_report(
        self, chart: NatalChart, person: BirthInfo
    ) -> StandardReportResponse:
        """Generate standard format report matching the required template"""
        from services.report_renderer import render_personal_report
        
        # Build astrology data structure for report renderer
        astrology_data = self._build_astrology_data(chart, person)
        
        # Generate report using the renderer
        report = render_personal_report(astrology_data)
        
        generated_at = datetime.now().isoformat()
        
        return StandardReportResponse(
            report=report,
            generated_at=generated_at,
            chart_data=chart
        )

    def _build_astrology_data(self, chart: NatalChart, person: BirthInfo) -> dict:
        """Build astrology data structure for report renderer"""
        astrology_data = {}
        
        # Map planets to their positions
        for planet in chart.planets:
            astrology_data[planet.name.lower()] = {
                'sign': planet.sign,
                'longitude': planet.longitude
            }
        
        # Add basic info
        astrology_data['sun'] = {
            'sign': chart.sun_sign,
            'longitude': self._get_planet_longitude(chart, 'Sun')
        }
        
        if chart.moon_sign:
            astrology_data['moon'] = {
                'sign': chart.moon_sign,
                'longitude': self._get_planet_longitude(chart, 'Moon')
            }
        
        if chart.ascendant:
            astrology_data['ascendant'] = {
                'sign': chart.ascendant,
                'longitude': 0.0  # Ascendant longitude not available in current structure
            }
        
        return astrology_data

    def _get_planet_longitude(self, chart: NatalChart, planet_name: str) -> float:
        """Get longitude for a specific planet"""
        for planet in chart.planets:
            if planet.name == planet_name:
                return planet.longitude
        return 0.0

    def compatibility(
        self, chart_a: NatalChart, chart_b: NatalChart, gender_a: str, gender_b: str
    ) -> CompatibilityDetails:
        """Calculate compatibility between two charts with AI-enhanced analysis"""
        score = self._element_score(chart_a.sun_sign, chart_b.sun_sign)
        
        # Apply gender tone adjustments
        tone = GENDER_TONE.get((gender_a, gender_b), "bổ trợ")
        
        # Calculate compatibility scores for different areas
        venus_a = self._get_planet_sign(chart_a, "Venus") or chart_a.sun_sign
        venus_b = self._get_planet_sign(chart_b, "Venus") or chart_b.sun_sign
        love_score = self._element_score(venus_a, venus_b)
        
        mercury_a = self._get_planet_sign(chart_a, "Mercury") or chart_a.sun_sign
        mercury_b = self._get_planet_sign(chart_b, "Mercury") or chart_b.sun_sign
        career_score = self._element_score(mercury_a, mercury_b)
        
        mars_a = self._get_planet_sign(chart_a, "Mars") or chart_a.sun_sign
        mars_b = self._get_planet_sign(chart_b, "Mars") or chart_b.sun_sign
        relationship_score = self._element_score(mars_a, mars_b)
        
        # Generate AI-enhanced compatibility analysis
        ai_analysis = self._get_ai_compatibility_analysis(chart_a, chart_b, score)
        
        # Generate advice based on compatibility
        if score >= 80:
            advice = "Mối quan hệ thuận lợi, hãy tận dụng điểm mạnh của nhau để phát triển."
        elif score >= 60:
            advice = "Cần nỗ lực thấu hiểu và điều chỉnh để đạt được sự hòa hợp."
        else:
            advice = "Cần nhiều nỗ lực và kiên nhẫn để xây dựng mối quan hệ bền vững."
        
        # Identify conflict points
        conflict_points = self._challenge_phrase(
            SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0],
            SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
        )
        
        # Generate recommended activities
        activities = self._recommended_activities(
            SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0],
            SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
        )
        
        # Generate aspects with AI insights
        aspects = [
            f"Sun {chart_a.sun_sign} - Sun {chart_b.sun_sign}: {self._strength_phrase(score)}",
            f"Venus {venus_a} - Venus {venus_b}: {self._strength_phrase(love_score)}",
            f"Mars {mars_a} - Mars {mars_b}: {self._strength_phrase(relationship_score)}"
        ]
        
        # Add AI-generated detailed reasoning
        detailed_reasoning = self._get_ai_detailed_reasoning(chart_a, chart_b)

        return CompatibilityDetails(
            score=score,
            summary=f"Độ tương thích tổng thể: {score}/100 - {tone}",
            personality=f"Phù hợp {tone} nhau với điểm số {score}/100",
            love_style=f"Phong cách yêu thương: {tone} với điểm số {love_score}/100",
            career=f"Hợp tác công việc: {tone} với điểm số {career_score}/100",
            relationships=f"Động lực mối quan hệ: {tone} với điểm số {relationship_score}/100",
            advice=advice,
            conflict_points=conflict_points,
            recommended_activities=activities,
            aspects=aspects,
            ai_analysis=ai_analysis,
            detailed_reasoning=detailed_reasoning
        )

    def _get_planet_sign(self, chart: NatalChart, planet_name: str) -> Optional[str]:
        """Get sign for a specific planet"""
        for planet in chart.planets:
            if planet.name == planet_name:
                return planet.sign
        return None

    def _get_ai_compatibility_analysis(self, chart_a: NatalChart, chart_b: NatalChart, base_score: int) -> str:
        """Get concise AI-enhanced compatibility analysis"""
        # Build concise chart information
        chart_a_info = self._build_concise_chart_info(chart_a)
        chart_b_info = self._build_concise_chart_info(chart_b)
        
        # Generate concise analysis
        return self._generate_concise_compatibility_analysis(chart_a, chart_b, base_score)

    def _get_ai_detailed_reasoning(self, chart_a: NatalChart, chart_b: NatalChart) -> str:
        """Get AI-generated detailed reasoning for compatibility"""
        try:
            # Get element information
            element_a = SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0]
            element_b = SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
            
            # Get planet information
            venus_a = self._get_planet_sign(chart_a, "Venus") or chart_a.sun_sign
            venus_b = self._get_planet_sign(chart_b, "Venus") or chart_b.sun_sign
            mars_a = self._get_planet_sign(chart_a, "Mars") or chart_a.sun_sign
            mars_b = self._get_planet_sign(chart_b, "Mars") or chart_b.sun_sign
            
            # Generate enhanced detailed reasoning
            return self._generate_enhanced_detailed_reasoning(chart_a, chart_b, element_a, element_b, venus_a, venus_b, mars_a, mars_b)
        except Exception as e:
            self._logger.error(f"AI detailed reasoning failed: {e}")
            return "Lý do chi tiết không khả dụng do lỗi hệ thống."

    def _build_concise_chart_info(self, chart: NatalChart) -> str:
        """Build concise chart information for AI analysis"""
        info = f"- Mặt Trời: {chart.sun_sign}\n"
        if chart.moon_sign:
            info += f"- Mặt Trăng: {chart.moon_sign}\n"
        if chart.ascendant:
            info += f"- Cung Mọc: {chart.ascendant}\n"
        
        # Add key planet positions concisely
        for planet in chart.planets:
            info += f"- {planet.name}: {planet.sign}\n"
        
        return info

    def _get_element_interaction(self, element_a: str, element_b: str) -> str:
        """Get element interaction description"""
        if element_a == element_b:
            return "Cùng nguyên tố - Tương đồng mạnh mẽ"
        elif {element_a, element_b} in [{"Fire", "Air"}, {"Water", "Earth"}]:
            return "Tương sinh - Hỗ trợ tốt"
        elif {element_a, element_b} in [{"Fire", "Water"}, {"Air", "Earth"}]:
            return "Tương khắc - Cần nỗ lực hòa hợp"
        else:
            return "Khác biệt - Học hỏi lẫn nhau"

    def _get_dominant_planets_description(self, chart: NatalChart) -> str:
        """Get description of dominant planets"""
        descriptions = []
        
        # Check for strong placements
        for planet in chart.planets:
            if planet.sign in [chart.sun_sign, chart.ascendant]:
                descriptions.append(f"{planet.name} mạnh ở {planet.sign}")
        
        if not descriptions:
            descriptions.append("Mặt Trời và Mặt Trăng là hành tinh chủ đạo")
        
        return ", ".join(descriptions)

    def _generate_concise_compatibility_analysis(self, chart_a: NatalChart, chart_b: NatalChart, base_score: int) -> str:
        """Generate concise compatibility analysis"""
        element_a = SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0]
        element_b = SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
        
        element_interaction = self._get_element_interaction(element_a, element_b)
        
        # Generate concise analysis
        analysis = f"""🤖 **Phân tích AI: Độ tương thích {base_score}/100**

**Tổng quan:** Sự kết hợp năng lượng độc đáo giữa {element_a} và {element_b}, tạo nên nền tảng {element_interaction.lower()}.

**Điểm mạnh:** Cả hai có thể học hỏi lẫn nhau để phát triển bản thân toàn diện.

**Thách thức:** Cần kiên nhẫn để thấu hiểu những khác biệt trong cách suy nghĩ.

**Lời khuyên:** Hãy dành thời gian để tìm hiểu và trân trọng những điểm khác biệt - đây chính là cơ hội để cả hai cùng trưởng thành."""
        
        return analysis

    def _generate_enhanced_detailed_reasoning(self, chart_a: NatalChart, chart_b: NatalChart, element_a: str, element_b: str, venus_a: str, venus_b: str, mars_a: str, mars_b: str) -> str:
        """Generate concise detailed reasoning"""
        element_interaction = self._get_element_interaction(element_a, element_b)
        
        # Generate concise reasoning
        reasoning = f"""🔍 **Lý Do Chi Tiết:**

**NGUYÊN TỐ TƯƠNG TÁC:**
- Người A: {element_a} (năng lượng {element_a.lower()})
- Người B: {element_b} (năng lượng {element_b.lower()})
→ **Tương tác nguyên tố: {element_interaction.lower()}**

**CUNG HOÀNG ĐẠO CHỦ ĐẠO:**
- Mặt Trời A: {chart_a.sun_sign} - Năng lượng cốt lõi, bản chất con người
- Mặt Trời B: {chart_b.sun_sign} - Năng lượng cốt lõi, bản chất con người
- Kim Tinh A: {venus_a} - Cách yêu thương và giá trị cảm xúc
- Kim Tinh B: {venus_b} - Cách yêu thương và giá trị cảm xúc  
- Hỏa Tinh A: {mars_a} - Động lực, đam mê và cách hành động
- Hỏa Tinh B: {mars_b} - Động lực, đam mê và cách hành động

**GIẢI THÍCH CHI TIẾT:**
1. **Sự hòa hợp tiềm năng:** Cả hai có thể học hỏi lẫn nhau để phát triển bản thân toàn diện hơn thông qua việc bổ sung những điểm mạnh khác biệt.

2. **Xung đột cần lưu ý:** Sự khác biệt trong cách thể hiện cảm xúc và nhu cầu có thể dẫn đến hiểu lầm nếu không có sự thấu hiểu.

3. **Phát triển mối quan hệ:** Cả hai cần kiên nhẫn lắng nghe và thấu hiểu điểm khác biệt, đây là chìa khóa để xây dựng mối quan hệ bền vững.

**Kết luận:** Đây là một sự kết hợp có tiềm năng phát triển mạnh mẽ nếu cả hai cùng nỗ lực thấu hiểu và tôn trọng sự khác biệt của đối phương."""
        
        return reasoning

    def _build_fallback_svg(self, natal: NatalChart, time_unknown: bool) -> Optional[str]:
        """Generate a minimal fallback SVG when Kerykeion fails"""
        try:
            if time_unknown:
                # For unknown time, create a simple sun sign chart
                return f"""<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100%" height="100%" fill="white"/>
                    <circle cx="200" cy="200" r="180" fill="none" stroke="#333" stroke-width="2"/>
                    <text x="200" y="50" text-anchor="middle" font-size="24" font-family="Arial">Bản Đồ Sao</text>
                    <text x="200" y="80" text-anchor="middle" font-size="16" font-family="Arial">Cung Mặt Trời: {natal.sun_sign}</text>
                    <text x="200" y="350" text-anchor="middle" font-size="12" font-family="Arial">* Thời gian sinh không xác định</text>
                </svg>"""
            else:
                # For known time, create a basic chart structure
                return f"""<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100%" height="100%" fill="white"/>
                    <circle cx="200" cy="200" r="180" fill="none" stroke="#333" stroke-width="2"/>
                    <line x1="200" y1="20" x2="200" y2="380" stroke="#666" stroke-width="1"/>
                    <line x1="20" y1="200" x2="380" y2="200" stroke="#666" stroke-width="1"/>
                    <text x="200" y="50" text-anchor="middle" font-size="24" font-family="Arial">Bản Đồ Sao</text>
                    <text x="200" y="80" text-anchor="middle" font-size="16" font-family="Arial">Cung Mặt Trời: {natal.sun_sign}</text>
                    <text x="200" y="350" text-anchor="middle" font-size="12" font-family="Arial">* Dữ liệu hạn chế</text>
                </svg>"""
        except Exception as e:
            self._logger.error(f"Fallback SVG generation failed: {e}")
            return None
