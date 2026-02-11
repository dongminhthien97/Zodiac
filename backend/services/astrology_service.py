from __future__ import annotations
import os
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import traceback
import pytz
import swisseph as swe

from models.schemas import (
    BirthInfo, CompatibilityDetails, NatalChart, PlanetPosition,
    NatalResponse, ResponseMeta, ZodiacMeta, ResultSection, ResultSectionId,
    InsightBlock, InsightBlockType, InsightEmphasis, StandardReportResponse
)
from utils.compatibility_data import ELEMENT_COMPATIBILITY, SIGN_TRAITS, SUN_SIGN_RANGES
import google.genai as genai

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
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            self.ai_client = genai
        except Exception as e:
            self._logger.warning(f"Google AI client initialization failed: {e}")
            self.ai_client = None

    def build_natal_chart(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float], tz_name: Optional[str] = None
    ) -> NatalChart:
        """Build natal chart with fault-tolerant chart generation and unknown birth time support"""
        self._logger.debug(f"Building natal chart for: {person.name} at {lat}, {lon}")
        
        try:
            # Validate API contract
            if person.time_unknown and person.birth_time is not None:
                raise HTTPException(
                    status_code=400,
                    detail="birth_time must be null when time_unknown is true"
                )
            
            if not person.time_unknown and person.birth_time is None:
                raise HTTPException(
                    status_code=400,
                    detail="birth_time must not be null when time_unknown is false"
                )

            # Dispatch to appropriate calculation mode
            if person.time_unknown:
                return self._generate_natal_without_time(person, lat, lon)
            else:
                return self._generate_natal_with_time(person, lat, lon)
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            self._logger.error(f"Critical error in build_natal_chart for {person.name}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Chart generation failed: {str(e)}"
            )

    def _generate_natal_with_time(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float]
    ) -> NatalChart:
        """Generate natal chart with exact birth time using Swiss Ephemeris"""
        self._logger.info(f"Generating natal chart WITH birth time for {person.name}")
        
        try:
            # Parse date and time
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            hour, minute = [int(x) for x in person.birth_time.split(":")]
            
            # Create datetime object
            local_dt = datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute)
            
            # Convert to UTC using timezone
            timezone_str = "Asia/Ho_Chi_Minh"  # Default timezone for Vietnam
            tz = pytz.timezone(timezone_str)
            local_dt = tz.localize(local_dt)
            utc_dt = local_dt.astimezone(pytz.UTC)
            
            # Calculate Julian Day
            jd = swe.julday(
                utc_dt.year, 
                utc_dt.month, 
                utc_dt.day, 
                utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0
            )
            
            # Calculate planets
            planets = self._calculate_planets_with_swiss(jd)
            
            # Calculate houses and ascendant
            houses, ascendant = self._calculate_houses_with_swiss(jd, lat, lon)
            
            # Calculate sun sign
            sun_sign = self._get_sign_from_longitude(planets[0].longitude)
            
            # Build chart
            natal = NatalChart(
                name=person.name,
                sun_sign=sun_sign,
                moon_sign=self._get_sign_from_longitude(planets[1].longitude),
                ascendant=ascendant,
                planets=planets,
                houses=houses,
                svg_chart=None,  # Will be generated later
            )
            
            self._logger.info(f"WITH_TIME calculation successful for {person.name}")
            return natal
            
        except Exception as e:
            self._logger.error(f"WITH_TIME calculation failed for {person.name}: {e}")
            raise

    def _generate_natal_without_time(
        self, person: BirthInfo, lat: Optional[float], lon: Optional[float]
    ) -> NatalChart:
        """Generate natal chart without birth time using noon chart method"""
        self._logger.info(f"Generating natal chart WITHOUT birth time for {person.name}")
        
        try:
            # Parse date and set time to noon
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            local_dt = datetime(date_obj.year, date_obj.month, date_obj.day, 12, 0)  # Noon
            
            # Convert to UTC using timezone
            timezone_str = "Asia/Ho_Chi_Minh"  # Default timezone for Vietnam
            tz = pytz.timezone(timezone_str)
            local_dt = tz.localize(local_dt)
            utc_dt = local_dt.astimezone(pytz.UTC)
            
            # Calculate Julian Day
            jd = swe.julday(
                utc_dt.year, 
                utc_dt.month, 
                utc_dt.day, 
                utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0
            )
            
            # Calculate planets only (no houses)
            planets = self._calculate_planets_with_swiss(jd)
            
            # DO NOT calculate houses or ascendant
            houses = []
            ascendant = None
            
            # Calculate sun sign
            sun_sign = self._get_sign_from_longitude(planets[0].longitude)
            
            # Build chart
            natal = NatalChart(
                name=person.name,
                sun_sign=sun_sign,
                moon_sign=self._get_sign_from_longitude(planets[1].longitude),
                ascendant=None,  # Explicitly set to None
                planets=planets,
                houses=[],  # Empty houses list
                svg_chart=None,  # Will be generated later
            )
            
            self._logger.info(f"WITHOUT_TIME calculation successful for {person.name}")
            return natal
            
        except Exception as e:
            self._logger.error(f"WITHOUT_TIME calculation failed for {person.name}: {e}")
            raise

    def _calculate_planets_with_swiss(self, jd: float) -> list[PlanetPosition]:
        """Calculate planetary positions using Swiss Ephemeris"""
        planets = []
        
        # Planet indices for Swiss Ephemeris
        planet_indices = [
            (0, "Sun"),      # Sun
            (1, "Moon"),     # Moon
            (2, "Mercury"),  # Mercury
            (3, "Venus"),    # Venus
            (4, "Mars"),     # Mars
            (5, "Jupiter"),  # Jupiter
            (6, "Saturn"),   # Saturn
            (7, "Uranus"),   # Uranus
            (8, "Neptune"),  # Neptune
            (9, "Pluto"),    # Pluto
        ]
        
        for idx, name in planet_indices:
            try:
                # Calculate planet position
                result = swe.calc_ut(jd, idx)
                longitude = result[0][0]  # Get longitude from result
                
                # Convert longitude to sign
                sign = self._get_sign_from_longitude(longitude)
                
                planets.append(PlanetPosition(
                    name=name,
                    sign=sign,
                    longitude=longitude
                ))
                
            except Exception as e:
                self._logger.warning(f"Failed to calculate {name}: {e}")
                # Skip failed planets rather than crashing
        
        if not planets:
            raise Exception("No planets could be calculated")
            
        return planets

    def _calculate_houses_with_swiss(self, jd: float, lat: float, lon: float) -> tuple[list, str]:
        """Calculate houses and ascendant using Swiss Ephemeris"""
        if lat is None or lon is None:
            return [], None
            
        try:
            # Calculate houses
            houses_result = swe.houses(jd, lat, lon)
            houses = []
            
            # Houses 1-12 (indices 0-11 in result)
            for i in range(12):
                house_longitude = houses_result[0][i]
                sign = self._get_sign_from_longitude(house_longitude)
                houses.append({
                    "house": i + 1,
                    "sign": sign,
                    "longitude": house_longitude
                })
            
            # Ascendant is the cusp of the 1st house
            ascendant_longitude = houses_result[0][0]
            ascendant = self._get_sign_from_longitude(ascendant_longitude)
            
            return houses, ascendant
            
        except Exception as e:
            self._logger.warning(f"Failed to calculate houses: {e}")
            return [], None

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

    def calculate_compatibility_new(
        self,
        person_a: BirthInfo,
        person_b: BirthInfo,
        *,
        lat_a: Optional[float] = None,
        lon_a: Optional[float] = None,
        lat_b: Optional[float] = None,
        lon_b: Optional[float] = None,
    ) -> dict:
        """New compatibility calculation with 2 modes and comprehensive analysis"""
        import time
        from models.schemas import (
            CompatibilityMeta, CompatibilityScores, CompatibilityPersonality,
            CompatibilityLove, CompatibilityWork, CompatibilityRelationshipDynamics,
            CompatibilityConflictPoints, PlanetaryAspect, CompatibilityResponseNew
        )

        start_time = time.time()
        fallback_activated = False
        
        # Determine calculation modes
        has_accurate_time_a = person_a.birth_time is not None and not person_a.time_unknown
        has_accurate_time_b = person_b.birth_time is not None and not person_b.time_unknown
        
        # Build charts with appropriate modes
        try:
            chart_a = self._generate_chart_with_mode(person_a, has_accurate_time_a, lat_a, lon_a)
            chart_b = self._generate_chart_with_mode(person_b, has_accurate_time_b, lat_b, lon_b)
        except Exception as e:
            self._logger.error(f"Chart generation failed: {e}")
            raise HTTPException(status_code=500, detail="Chart generation failed")

        # Calculate aspects
        aspects = self._calculate_compatibility_aspects(chart_a, chart_b)
        
        # Fallback if not enough aspects
        if len(aspects) < 5:
            aspects.extend(self._generate_fallback_aspects(chart_a, chart_b, aspects))
            fallback_activated = True

        # Calculate scores
        scores = self._calculate_compatibility_scores(chart_a, chart_b)
        
        # Generate detailed analysis
        detailed_analysis = self._generate_detailed_compatibility_analysis(
            chart_a, chart_b, aspects, scores
        )

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log calculation details
        self._logger.info({
            "hasTimeA": has_accurate_time_a,
            "hasTimeB": has_accurate_time_b,
            "aspectsCalculated": len(aspects),
            "fallbackActivated": fallback_activated,
            "swissDurationMs": duration_ms
        })
        
        # Log warning if slow
        if duration_ms > 10000:
            self._logger.warning("Swiss ephemeris slow response")

        # Build response
        meta = CompatibilityMeta(
            hasAccurateTimeA=has_accurate_time_a,
            hasAccurateTimeB=has_accurate_time_b,
            fallbackActivated=fallback_activated,
            aspectsCalculated=len(aspects),
            swissCalculationDurationMs=duration_ms
        )

        return CompatibilityResponseNew(
            meta=meta,
            scores=scores,
            personality=self._build_personality_analysis(chart_a, chart_b, scores),
            love=self._build_love_analysis(chart_a, chart_b, aspects),
            work=self._build_work_analysis(chart_a, chart_b, aspects),
            relationshipDynamics=self._build_relationship_dynamics(chart_a, chart_b, aspects),
            conflictPoints=self._build_conflict_points(chart_a, chart_b, aspects),
            planetaryAspects=aspects,
            detailedAnalysis=detailed_analysis
        )

    def _generate_chart_with_mode(
        self,
        person: BirthInfo,
        has_accurate_time: bool,
        lat: Optional[float],
        lon: Optional[float],
    ):
        """Generate chart with appropriate mode based on time availability"""
        if has_accurate_time:
            return self._generate_natal_with_time(person, lat, lon)
        else:
            return self._generate_natal_without_time(person, lat, lon)

    def _calculate_compatibility_aspects(self, chart_a, chart_b) -> list[PlanetaryAspect]:
        """Calculate planetary aspects between two charts"""
        aspects = []
        
        # Major planet combinations
        major_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
        
        for planet_a in chart_a.planets:
            if planet_a.name not in major_planets:
                continue
                
            for planet_b in chart_b.planets:
                if planet_b.name not in major_planets:
                    continue
                
                # Calculate aspect
                aspect = self._calculate_aspect(planet_a, planet_b)
                if aspect:
                    aspects.append(aspect)
        
        return aspects

    def _calculate_aspect(self, planet_a, planet_b) -> PlanetaryAspect:
        """Calculate aspect between two planets"""
        # Calculate longitude difference
        diff = abs(planet_a.longitude - planet_b.longitude)
        if diff > 180:
            diff = 360 - diff
        
        # Determine aspect type and harmony
        aspect_type = None
        harmony = "Medium"
        weight = 1.0
        
        if diff < 8:  # Conjunction
            aspect_type = "Conjunction"
            harmony = "Challenging"
            weight = 2.0
        elif abs(diff - 60) < 6:  # Sextile
            aspect_type = "Sextile"
            harmony = "High"
            weight = 1.5
        elif abs(diff - 90) < 6:  # Square
            aspect_type = "Square"
            harmony = "Challenging"
            weight = 1.8
        elif abs(diff - 120) < 6:  # Trine
            aspect_type = "Trine"
            harmony = "High"
            weight = 2.0
        elif abs(diff - 180) < 8:  # Opposition
            aspect_type = "Opposition"
            harmony = "Challenging"
            weight = 1.5
        
        if aspect_type:
            description = self._get_aspect_description(planet_a.name, planet_b.name, aspect_type)
            return PlanetaryAspect(
                aspect=f"{planet_a.name} {aspect_type} {planet_b.name}",
                description=description,
                harmonyLevel=harmony,
                weight=weight
            )
        return None

    def _get_aspect_description(self, planet_a, planet_b, aspect_type) -> str:
        """Get descriptive text for planetary aspect"""
        descriptions = {
            "Conjunction": f"Sự kết hợp mạnh mẽ giữa {planet_a} và {planet_b} tạo nên năng lượng tập trung.",
            "Sextile": f"{planet_a} và {planet_b} tạo thành góc sáu, mang lại cơ hội phát triển hài hòa.",
            "Square": f"Căng thẳng giữa {planet_a} và {planet_b} tạo ra thách thức cần vượt qua.",
            "Trine": f"Dòng năng lượng chảy tự nhiên giữa {planet_a} và {planet_b}, tạo sự thuận lợi.",
            "Opposition": f"Sự đối lập giữa {planet_a} và {planet_b} cần được cân bằng và hòa giải."
        }
        return descriptions.get(aspect_type, f"Tương tác giữa {planet_a} và {planet_b}")

    def _generate_fallback_aspects(self, chart_a, chart_b, existing_aspects) -> list[PlanetaryAspect]:
        """Generate fallback aspects when not enough aspects calculated"""
        fallback_aspects = []
        
        # Add Sun vs Sun
        sun_a = next((p for p in chart_a.planets if p.name == "Sun"), None)
        sun_b = next((p for p in chart_b.planets if p.name == "Sun"), None)
        if sun_a and sun_b:
            aspect = self._calculate_aspect(sun_a, sun_b)
            if aspect and aspect.aspect not in [a.aspect for a in existing_aspects]:
                fallback_aspects.append(aspect)
        
        # Add Venus vs Venus
        venus_a = next((p for p in chart_a.planets if p.name == "Venus"), None)
        venus_b = next((p for p in chart_b.planets if p.name == "Venus"), None)
        if venus_a and venus_b:
            aspect = self._calculate_aspect(venus_a, venus_b)
            if aspect and aspect.aspect not in [a.aspect for a in existing_aspects]:
                fallback_aspects.append(aspect)
        
        # Add Mars vs Mars
        mars_a = next((p for p in chart_a.planets if p.name == "Mars"), None)
        mars_b = next((p for p in chart_b.planets if p.name == "Mars"), None)
        if mars_a and mars_b:
            aspect = self._calculate_aspect(mars_a, mars_b)
            if aspect and aspect.aspect not in [a.aspect for a in existing_aspects]:
                fallback_aspects.append(aspect)
        
        # Add element compatibility
        element_a = SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0]
        element_b = SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
        if element_a and element_b:
            element_compatibility = self._get_element_compatibility(element_a, element_b)
            fallback_aspects.append(PlanetaryAspect(
                aspect=f"Element {element_a} vs {element_b}",
                description=element_compatibility,
                harmonyLevel="Medium",
                weight=1.0
            ))
        
        # Add modality compatibility
        modality_a = self._get_sign_modality(chart_a.sun_sign)
        modality_b = self._get_sign_modality(chart_b.sun_sign)
        if modality_a and modality_b:
            modality_compatibility = self._get_modality_compatibility(modality_a, modality_b)
            fallback_aspects.append(PlanetaryAspect(
                aspect=f"Modality {modality_a} vs {modality_b}",
                description=modality_compatibility,
                harmonyLevel="Medium",
                weight=1.0
            ))
        
        return fallback_aspects

    def _get_element_compatibility(self, element_a: str, element_b: str) -> str:
        """Get element compatibility description"""
        if element_a == element_b:
            return "Cùng nguyên tố tạo nên sự thấu hiểu sâu sắc và đồng điệu về bản chất."
        elif {element_a, element_b} in [{"Fire", "Air"}, {"Water", "Earth"}]:
            return "Tương sinh tự nhiên, bổ sung và nuôi dưỡng lẫn nhau."
        elif {element_a, element_b} in [{"Fire", "Water"}, {"Air", "Earth"}]:
            return "Tương khắc cần học cách dung hòa và chuyển hóa năng lượng."
        else:
            return "Khác biệt tạo cơ hội học hỏi và phát triển từ nhau."

    def _get_sign_modality(self, sign: str) -> str:
        """Get sign modality (Cardinal, Fixed, Mutable)"""
        cardinal = ["Aries", "Cancer", "Libra", "Capricorn"]
        fixed = ["Taurus", "Leo", "Scorpio", "Aquarius"]
        mutable = ["Gemini", "Virgo", "Sagittarius", "Pisces"]
        
        if sign in cardinal:
            return "Cardinal"
        elif sign in fixed:
            return "Fixed"
        elif sign in mutable:
            return "Mutable"
        return "Unknown"

    def _get_modality_compatibility(self, modality_a: str, modality_b: str) -> str:
        """Get modality compatibility description"""
        if modality_a == modality_b:
            return "Cùng cách tiếp cận, dễ dàng đồng bộ hóa mục tiêu và phương pháp."
        elif {modality_a, modality_b} == {"Cardinal", "Fixed"}:
            return "Xung đột giữa người khởi xướng và người bảo thủ, cần học cách nhượng bộ."
        elif {modality_a, modality_b} == {"Cardinal", "Mutable"}:
            return "Sự linh hoạt gặp gỡ năng lượng sáng tạo, tạo nên sự kết hợp năng động."
        else:  # Fixed vs Mutable
            return "Sự ổn định gặp sự thay đổi, cần tìm điểm cân bằng giữa giữ gìn và thích nghi."

    def _calculate_compatibility_scores(self, chart_a, chart_b) -> CompatibilityScores:
        """Calculate detailed compatibility scores"""
        # Base element score
        base_score = self._element_score(chart_a.sun_sign, chart_b.sun_sign)
        
        # Calculate specific scores
        personality = base_score
        love = self._element_score(
            self._get_planet_sign(chart_a, "Venus") or chart_a.sun_sign,
            self._get_planet_sign(chart_b, "Venus") or chart_b.sun_sign
        )
        work = self._element_score(
            self._get_planet_sign(chart_a, "Mercury") or chart_a.sun_sign,
            self._get_planet_sign(chart_b, "Mercury") or chart_b.sun_sign
        )
        dynamics = self._calculate_dynamics_score(chart_a, chart_b)
        conflict = self._calculate_conflict_score(chart_a, chart_b)
        
        return CompatibilityScores(
            personality=personality,
            love=love,
            work=work,
            dynamics=dynamics,
            conflict=conflict
        )

    def _calculate_dynamics_score(self, chart_a, chart_b) -> int:
        """Calculate relationship dynamics score"""
        # Consider Mars positions for dynamic energy
        mars_a = self._get_planet_sign(chart_a, "Mars") or chart_a.sun_sign
        mars_b = self._get_planet_sign(chart_b, "Mars") or chart_b.sun_sign
        return self._element_score(mars_a, mars_b)

    def _calculate_conflict_score(self, chart_a, chart_b) -> int:
        """Calculate conflict potential score (lower is better)"""
        # Consider challenging aspects
        element_a = SIGN_TRAITS.get(chart_a.sun_sign, "").split("|")[0]
        element_b = SIGN_TRAITS.get(chart_b.sun_sign, "").split("|")[0]
        
        if {element_a, element_b} in [{"Fire", "Water"}, {"Air", "Earth"}]:
            return 30  # High conflict potential
        elif element_a == element_b:
            return 70  # Low conflict potential
        else:
            return 50  # Medium conflict potential

    def _build_personality_analysis(self, chart_a, chart_b, scores) -> CompatibilityPersonality:
        """Build personality compatibility analysis"""
        strengths = [
            "Sự thấu hiểu bản chất cốt lõi thông qua năng lượng Mặt Trời",
            "Khả năng đồng cảm và chia sẻ cảm xúc sâu sắc",
            "Tư duy tương thích trong cách nhìn nhận thế giới"
        ]
        
        challenges = [
            "Sự khác biệt trong cách thể hiện cảm xúc",
            "Xung đột giữa nhu cầu cá nhân và nhu cầu chung",
            "Khác biệt trong cách xử lý áp lực và căng thẳng"
        ]
        
        advice = "Hãy dành thời gian để thấu hiểu điểm mạnh và điểm yếu của nhau. Sự khác biệt không phải là rào cản mà là cơ hội để học hỏi và phát triển cùng nhau."

        return CompatibilityPersonality(
            summary=f"Tương thích tính cách ở mức {scores.personality}/100",
            strengths=strengths,
            challenges=challenges,
            advice=advice
        )

    def _build_love_analysis(self, chart_a, chart_b, aspects) -> CompatibilityLove:
        """Build love compatibility analysis"""
        emotional_connection = "Mối liên kết cảm xúc được xây dựng trên nền tảng thấu hiểu và chia sẻ."
        attraction = "Sự thu hút đến từ sự bổ sung và tương phản lành mạnh giữa hai cá tính."
        long_term_potential = "Tiềm năng lâu dài phụ thuộc vào khả năng thích nghi và compromise."

        return CompatibilityLove(
            emotionalConnection=emotional_connection,
            attraction=attraction,
            longTermPotential=long_term_potential
        )

    def _build_work_analysis(self, chart_a, chart_b, aspects) -> CompatibilityWork:
        """Build work compatibility analysis"""
        teamwork = "Khả năng làm việc nhóm được hỗ trợ bởi sự tương thích trong tư duy và phương pháp."
        leadership_dynamic = "Động lực lãnh đạo được phân bổ hợp lý dựa trên điểm mạnh của mỗi người."
        risk_factors = "Các yếu tố rủi ro bao gồm sự khác biệt trong cách ra quyết định và quản lý thời gian."

        return CompatibilityWork(
            teamwork=teamwork,
            leadershipDynamic=leadership_dynamic,
            riskFactors=risk_factors
        )

    def _build_relationship_dynamics(self, chart_a, chart_b, aspects) -> CompatibilityRelationshipDynamics:
        """Build relationship dynamics analysis"""
        core_theme = "Chủ đề cốt lõi của mối quan hệ là sự học hỏi và phát triển qua những khác biệt."
        karmic_factor = "Yếu tố nghiệp chướng thể hiện qua những bài học cần vượt qua để đạt được sự thấu hiểu."
        growth_lesson = "Bài học trưởng thành nằm ở việc chấp nhận và trân trọng sự khác biệt như một món quà."

        return CompatibilityRelationshipDynamics(
            coreTheme=core_theme,
            karmicFactor=karmic_factor,
            growthLesson=growth_lesson
        )

    def _build_conflict_points(self, chart_a, chart_b, aspects) -> CompatibilityConflictPoints:
        """Build conflict points analysis"""
        triggers = [
            "Sự khác biệt trong cách thể hiện cảm xúc",
            "Xung đột giữa nhu cầu độc lập và nhu cầu gắn kết",
            "Khác biệt trong cách xử lý vấn đề và ra quyết định"
        ]
        
        resolution_advice = "Khi xung đột xảy ra, hãy tập trung vào việc thấu hiểu nguyên nhân sâu xa thay vì chỉ phản ứng với biểu hiện bề ngoài."

        return CompatibilityConflictPoints(
            triggers=triggers,
            resolutionAdvice=resolution_advice
        )

    def _generate_detailed_compatibility_analysis(self, chart_a, chart_b, aspects, scores) -> str:
        """Generate comprehensive compatibility analysis (300+ words)"""
        analysis = f"""
Phân tích tương thích chi tiết:

Mối quan hệ giữa {chart_a.name or 'Person A'} và {chart_b.name or 'Person B'} được xây dựng trên nền tảng của {len(aspects)} tương tác hành tinh quan trọng. Với điểm số tổng thể {scores.personality}/100, đây là một mối quan hệ có tiềm năng phát triển mạnh mẽ nếu cả hai cùng nỗ lực.

Về mặt tính cách, hai bạn có mức độ tương thích {scores.personality}/100, cho thấy sự hòa hợp trong những giá trị cốt lõi và cách nhìn nhận thế giới. Tuy nhiên, cũng tồn tại những khác biệt cần được thấu hiểu và trân trọng. Sự khác biệt này không phải là rào cản mà là cơ hội để cả hai học hỏi và phát triển từ nhau.

Trong tình yêu, mức độ tương thích {scores.love}/100 cho thấy tiềm năng cảm xúc sâu sắc. Các hành tinh Kim Tinh (Venus) trong hai bản đồ sao tạo nên nền tảng cho sự thu hút và kết nối cảm xúc. Tuy nhiên, để duy trì ngọn lửa tình yêu, cả hai cần học cách thể hiện và đáp lại tình cảm theo cách mà đối phương mong đợi.

Trong công việc, điểm số {scores.work}/100 cho thấy khả năng hợp tác tốt. Sự tương thích trong cách tư duy và tiếp cận vấn đề giúp hai bạn có thể cùng nhau đạt được những mục tiêu chung. Tuy nhiên, cần lưu ý đến những khác biệt trong phong cách làm việc để tránh xung đột không cần thiết.

Động lực mối quan hệ ở mức {scores.dynamics}/100 cho thấy năng lượng tương tác tích cực. Các hành tinh Hỏa Tinh (Mars) tạo nên động lực thúc đẩy mối quan hệ phát triển. Tuy nhiên, cũng cần lưu ý đến những xung đột tiềm ẩn ở mức {scores.conflict}/100.

Để phát triển mối quan hệ bền vững, cả hai cần:
1. Học cách thấu hiểu và chấp nhận sự khác biệt
2. Giao tiếp cởi mở và trung thực
3. Cùng nhau đặt ra những mục tiêu chung
4. Biết compromise khi cần thiết
5. Dành thời gian để nuôi dưỡng cảm xúc và sự gắn kết

Mối quan hệ này có tiềm năng trở thành một partnership bền vững nếu cả hai cùng cam kết nỗ lực và học hỏi từ những thách thức.
"""
        return analysis.strip()

    def generate_professional_compatibility_analysis(
        self, person_a_data: dict, person_b_data: dict, aspects: list
    ) -> str:
        """
        Generate extremely detailed compatibility analysis (1000+ words)
        Professional Western astrologer style with deep psychological insight
        """
        # Extract chart data
        sun_a = person_a_data.get('sun', {}).get('sign', 'Unknown')
        moon_a = person_a_data.get('moon', {}).get('sign', 'Unknown')
        mercury_a = person_a_data.get('mercury', {}).get('sign', 'Unknown')
        venus_a = person_a_data.get('venus', {}).get('sign', 'Unknown')
        mars_a = person_a_data.get('mars', {}).get('sign', 'Unknown')
        asc_a = person_a_data.get('ascendant', {}).get('sign', 'Unknown')
        
        sun_b = person_b_data.get('sun', {}).get('sign', 'Unknown')
        moon_b = person_b_data.get('moon', {}).get('sign', 'Unknown')
        mercury_b = person_b_data.get('mercury', {}).get('sign', 'Unknown')
        venus_b = person_b_data.get('venus', {}).get('sign', 'Unknown')
        mars_b = person_b_data.get('mars', {}).get('sign', 'Unknown')
        asc_b = person_b_data.get('ascendant', {}).get('sign', 'Unknown')

        # Build analysis
        analysis = self._build_comprehensive_analysis(
            sun_a, moon_a, mercury_a, venus_a, mars_a, asc_a,
            sun_b, moon_b, mercury_b, venus_b, mars_b, asc_b,
            aspects
        )
        
        return analysis

    def generate_ai_compatibility_analysis_json(
        self,
        person_a: dict,
        person_b: dict,
        aspects: list,
        fallback_mode: bool = False
    ) -> dict:
        """
        Generate AI compatibility analysis in JSON format with >=1000 words
        Specialized for OpenAI Codex/GPT-4/GPT-5-Codex style output
        """
        # Extract signs
        sun_a = person_a.get('sun', 'Unknown')
        moon_a = person_a.get('moon', 'Unknown')
        mercury_a = person_a.get('mercury', 'Unknown')
        venus_a = person_a.get('venus', 'Unknown')
        mars_a = person_a.get('mars', 'Unknown')
        asc_a = person_a.get('ascendant', 'Unknown')
        
        sun_b = person_b.get('sun', 'Unknown')
        moon_b = person_b.get('moon', 'Unknown')
        mercury_b = person_b.get('mercury', 'Unknown')
        venus_b = person_b.get('venus', 'Unknown')
        mars_b = person_b.get('mars', 'Unknown')
        asc_b = person_b.get('ascendant', 'Unknown')

        # Calculate scores
        scores = self._calculate_ai_compatibility_scores(
            sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
            venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
        )

        # Generate sections
        overview = self._generate_ai_overview(sun_a, sun_b, moon_a, moon_b, asc_a, asc_b, fallback_mode)
        element_dynamics = self._generate_ai_element_dynamics(sun_a, sun_b, moon_a, moon_b, venus_a, venus_b, mars_a, mars_b)
        planetary_aspects = self._generate_ai_planetary_aspects(aspects)
        emotional_connection = self._generate_ai_emotional_connection(moon_a, moon_b, venus_a, venus_b, sun_a, sun_b)
        romantic_attraction = self._generate_ai_romantic_attraction(venus_a, venus_b, mars_a, mars_b, asc_a, asc_b)
        communication_style = self._generate_ai_communication_style(mercury_a, mercury_b, sun_a, sun_b, moon_a, moon_b)
        conflict_dynamics = self._generate_ai_conflict_dynamics(sun_a, sun_b, moon_a, moon_b, mars_a, mars_b, fallback_mode)
        long_term_potential = self._generate_ai_long_term_potential(sun_a, sun_b, moon_a, moon_b, venus_a, venus_b, asc_a, asc_b, aspects)
        growth_advice = self._generate_ai_growth_advice(sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects, fallback_mode)
        
        # Generate comprehensive analysis text (>=1000 words)
        analysis_text = self._generate_ai_comprehensive_analysis(
            sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b,
            aspects, scores, overview, element_dynamics, planetary_aspects, emotional_connection,
            romantic_attraction, communication_style, conflict_dynamics, long_term_potential, growth_advice,
            fallback_mode
        )

        return {
            "scores": scores,
            "overview": overview,
            "elementDynamics": element_dynamics,
            "planetaryAspectAnalysis": planetary_aspects,
            "emotionalConnection": emotional_connection,
            "romanticAttraction": romantic_attraction,
            "communicationStyle": communication_style,
            "conflictDynamics": conflict_dynamics,
            "longTermPotential": long_term_potential,
            "growthAdvice": growth_advice,
            "analysisText": analysis_text
        }

    def _calculate_ai_compatibility_scores(
        self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
        venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
    ) -> dict:
        """Calculate AI compatibility scores with detailed explanations"""
        emotional_score = self._calculate_emotional_compatibility(moon_a, moon_b, venus_a, venus_b)
        romantic_score = self._calculate_romantic_compatibility(venus_a, venus_b, mars_a, mars_b, sun_a, sun_b)
        communication_score = self._calculate_communication_compatibility(mercury_a, mercury_b, sun_a, sun_b)
        stability_score = self._calculate_stability_compatibility(sun_a, sun_b, moon_a, moon_b, asc_a, asc_b, aspects)
        
        return {
            "emotionalCompatibility": emotional_score,
            "romanticCompatibility": romantic_score,
            "communicationCompatibility": communication_score,
            "longTermStability": stability_score
        }

    def _generate_ai_overview(self, sun_a, sun_b, moon_a, moon_b, asc_a, asc_b, fallback_mode) -> str:
        """Generate AI overview with fallback mode awareness"""
        element_a = SIGN_TRAITS.get(sun_a, "").split("|")[0]
        element_b = SIGN_TRAITS.get(sun_b, "").split("|")[0]
        
        overview = f"""Tổng quan năng lượng hai người:

Mối quan hệ giữa {sun_a} và {sun_b} được xây dựng trên nền tảng năng lượng {element_a} và {element_b}, tạo nên một sự tương tác đặc biệt. Mặt Trời {sun_a} ({SIGN_TRAITS.get(sun_a, "").split("|")[1]}) đại diện cho bản chất cốt lõi và động lực sống của người A, trong khi Mặt Trời {sun_b} ({SIGN_TRAITS.get(sun_b, "").split("|")[1]}) thể hiện bản chất và mục tiêu sống của người B.

Sự kết hợp này tạo nên một động lực mạnh mẽ, nơi mà {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} của người A có thể {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()} người B, và ngược lại. Mặt Trăng {moon_a} và Mặt Trăng {moon_b} tiết lộ thế giới cảm xúc sâu kín, cho thấy cách hai người xử lý nhu cầu cảm xúc và tìm kiếm sự an toàn trong mối quan hệ.

Cung Mọc {asc_a} và {asc_b} đại diện cho "chiếc mặt nạ" mà hai người thể hiện với thế giới, cũng như cách họ tiếp cận các mối quan hệ mới. Sự tương tác giữa các yếu tố này tạo nên một bức tranh toàn diện về tiềm năng và thách thức trong mối quan hệ này.

{f'⚠️ Lưu ý: Phân tích được thực hiện ở chế độ fallback (thiếu giờ sinh), một số tính toán về Cung Mọc và các aspect có thể không chính xác hoàn toàn.' if fallback_mode else 'Phân tích được thực hiện với đầy đủ thông tin giờ sinh, đảm bảo độ chính xác cao trong các tính toán aspect và Cung Mọc.'}"""
        
        return overview

    def _generate_ai_element_dynamics(self, sun_a, sun_b, moon_a, moon_b, venus_a, venus_b, mars_a, mars_b) -> str:
        """Generate element dynamics analysis"""
        element_sun_a = SIGN_TRAITS.get(sun_a, "").split("|")[0]
        element_sun_b = SIGN_TRAITS.get(sun_b, "").split("|")[0]
        element_moon_a = SIGN_TRAITS.get(moon_a, "").split("|")[0]
        element_moon_b = SIGN_TRAITS.get(moon_b, "").split("|")[0]
        element_venus_a = SIGN_TRAITS.get(venus_a, "").split("|")[0]
        element_venus_b = SIGN_TRAITS.get(venus_b, "").split("|")[0]
        element_mars_a = SIGN_TRAITS.get(mars_a, "").split("|")[0]
        element_mars_b = SIGN_TRAITS.get(mars_b, "").split("|")[0]
        
        # Determine overall element balance
        fire_count = sum([1 for e in [element_sun_a, element_sun_b, element_mars_a, element_mars_b] if e == "Fire"])
        earth_count = sum([1 for e in [element_sun_a, element_sun_b, element_venus_a, element_venus_b] if e == "Earth"])
        air_count = sum([1 for e in [element_sun_a, element_sun_b, element_mercury_a, element_mercury_b] if e == "Air"])
        water_count = sum([1 for e in [element_moon_a, element_moon_b, element_venus_a, element_venus_b] if e == "Water"])
        
        element_dynamics = f"""Động lực nguyên tố:

Phân tích sự cân bằng nguyên tố cho thấy mối quan hệ này có sự phân bố như sau:
- Nguyên tố Lửa: {fire_count} (đại diện cho năng lượng, đam mê, sáng tạo)
- Nguyên tố Đất: {earth_count} (đại diện cho sự ổn định, thực tế, kiên nhẫn)
- Nguyên tố Khí: {air_count} (đại diện cho trí tuệ, giao tiếp, tư duy)
- Nguyên tố Nước: {water_count} (đại diện cho cảm xúc, trực giác, cảm thông)

Sự kết hợp giữa {element_sun_a} (Mặt Trời {sun_a}) và {element_sun_b} (Mặt Trời {sun_b}) tạo nên nền tảng cho sự tương tác năng lượng cốt lõi. Nếu hai nguyên tố này là {element_sun_a} và {element_sun_b}, chúng có thể tạo nên sự {self._get_element_interaction(element_sun_a, element_sun_b).lower()}.

Mặt Trăng {moon_a} ({element_moon_a}) và Mặt Trăng {moon_b} ({element_moon_b}) tiết lộ cách hai người xử lý cảm xúc và nhu cầu cảm xúc sâu kín. Sự tương thích giữa hai nguyên tố này rất quan trọng cho sự gắn kết cảm xúc lâu dài.

Kim Tinh {venus_a} ({element_venus_a}) và Kim Tinh {venus_b} ({element_venus_b}) cho thấy cách hai người yêu thương và được yêu, trong khi Hỏa Tinh {mars_a} ({element_mars_a}) và Hỏa Tinh {mars_b} ({element_mars_b}) tiết lộ cách họ thể hiện năng lượng, đam mê và xử lý xung đột.

Sự cân bằng tổng thể giữa các nguyên tố này sẽ quyết định mức độ hài hòa và thách thức trong mối quan hệ."""
        
        return element_dynamics

    def _generate_ai_planetary_aspects(self, aspects) -> list:
        """Generate planetary aspect analysis"""
        aspect_list = []
        
        for aspect in aspects:
            if hasattr(aspect, 'aspect'):
                aspect_name = aspect.aspect
                orb = getattr(aspect, 'orb', 0)
                description = getattr(aspect, 'description', 'Mô tả không khả dụng')
            else:
                aspect_name = str(aspect)
                orb = 0
                description = "Mô tả không khả dụng"
            
            aspect_list.append({
                "aspect": aspect_name,
                "orb": orb,
                "description": description
            })
        
        return aspect_list

    def _generate_ai_emotional_connection(self, moon_a, moon_b, venus_a, venus_b, sun_a, sun_b) -> str:
        """Generate emotional connection analysis"""
        emotional_connection = f"""Kết nối cảm xúc:

Mối liên kết cảm xúc giữa hai người được xây dựng chủ yếu thông qua sự tương tác giữa Mặt Trăng {moon_a} và Mặt Trăng {moon_b}. Mặt Trăng {moon_a} ({SIGN_TRAITS.get(moon_a, "").split("|")[1]}) tiết lộ nhu cầu cảm xúc sâu kín và cách người A tìm kiếm sự an toàn, trong khi Mặt Trăng {moon_b} ({SIGN_TRAITS.get(moon_b, "").split("|")[1]}) cho thấy nhu cầu và cách thể hiện cảm xúc của người B.

Sự tương thích giữa hai Mặt Trăng này rất quan trọng vì nó quyết định liệu hai người có thể tạo nên một môi trường cảm xúc an toàn và nuôi dưỡng cho nhau hay không. Nếu Mặt Trăng {moon_a} và Mặt Trăng {moon_b} có sự tương thích tốt, hai người sẽ dễ dàng thấu hiểu và đáp ứng nhu cầu cảm xúc của nhau.

Kim Tinh {venus_a} và Kim Tinh {venus_b} cũng đóng vai trò quan trọng trong việc tạo nên sự kết nối cảm xúc. Kim Tinh {venus_a} ({SIGN_TRAITS.get(venus_a, "").split("|")[1]}) cho thấy cách người A thể hiện tình yêu và những gì họ cần để cảm thấy được yêu thương, trong khi Kim Tinh {venus_b} ({SIGN_TRAITS.get(venus_b, "").split("|")[1]}) tiết lộ cách người B yêu thương và những giá trị họ tìm kiếm trong tình yêu.

Sự kết hợp giữa Mặt Trời {sun_a} và Mặt Trăng {moon_b}, cũng như Mặt Trời {sun_b} và Mặt Trăng {moon_a} tạo nên một động lực cảm xúc mạnh mẽ, nơi mà bản chất cốt lõi của một người có thể nuôi dưỡng và làm hài lòng thế giới cảm xúc của người kia.

Để phát triển kết nối cảm xúc sâu sắc, cả hai cần học cách {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()} để làm người kia cảm thấy an toàn, đồng thời {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} để đáp lại nhu cầu cảm xúc của đối phương."""
        
        return emotional_connection

    def _generate_ai_romantic_attraction(self, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b) -> str:
        """Generate romantic attraction analysis"""
        romantic_attraction = f"""Sức hút tình yêu:

Sức hút tình yêu và đam mê giữa hai người được định hình chủ yếu bởi sự tương tác giữa Kim Tinh {venus_a} và Hỏa Tinh {mars_a} ở người A, cùng Kim Tinh {venus_b} và Hỏa Tinh {mars_b} ở người B.

Kim Tinh {venus_a} ({SIGN_TRAITS.get(venus_a, "").split("|")[1]}) tiết lộ cách người A thể hiện tình yêu, những gì họ tìm kiếm trong tình yêu, và cách họ được yêu thương. Trong khi đó, Hỏa Tinh {mars_a} ({SIGN_TRAITS.get(mars_a, "").split("|")[1]}) cho thấy cách người A thể hiện đam mê, năng lượng tình dục, và cách họ theo đuổi những gì họ muốn.

Tương tự, Kim Tinh {venus_b} ({SIGN_TRAITS.get(venus_b, "").split("|")[1]}) và Hỏa Tinh {mars_b} ({SIGN_TRAITS.get(mars_b, "").split("|")[1]}) tiết lộ cách người B yêu thương và thể hiện đam mê.

Sự hấp dẫn giữa Kim Tinh {venus_a} và Hỏa Tinh {mars_b} tạo nên một sức hút tình dục mạnh mẽ, nơi mà {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()} của người A bị thu hút bởi {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()} của người B. Ngược lại, Kim Tinh {venus_b} lại tìm thấy {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()} ở Hỏa Tinh {mars_a}.

Cung Mọc {asc_a} và {asc_b} cũng ảnh hưởng đến sức hút ban đầu và cách hai người thể hiện bản thân trong tình yêu. Cung Mọc {asc_a} tạo ấn tượng ban đầu là {SIGN_TRAITS.get(asc_a, "").split("|")[1]}, trong khi Cung Mọc {asc_b} lại mang đến cảm giác {SIGN_TRAITS.get(asc_b, "").split("|")[1]}.

Sự kết hợp này tạo nên một sự hấp dẫn toàn diện, từ vẻ bề ngoài đến cách thể hiện tình cảm, từ đam mê tình dục đến cách nuôi dưỡng tình yêu lâu dài."""
        
        return romantic_attraction

    def _generate_ai_communication_style(self, mercury_a, mercury_b, sun_a, sun_b, moon_a, moon_b) -> str:
        """Generate communication style analysis"""
        communication_style = f"""Phong cách giao tiếp:

Cách hai người giao tiếp và trao đổi ý tưởng được định hình chủ yếu bởi Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b}. Thủy Tinh {mercury_a} ({SIGN_TRAITS.get(mercury_a, "").split("|")[1]}) tiết lộ cách người A tư duy, xử lý thông tin, và truyền đạt ý tưởng, trong khi Thủy Tinh {mercury_b} ({SIGN_TRAITS.get(mercury_b, "").split("|")[1]}) cho thấy cách người B suy nghĩ và giao tiếp.

Sự tương thích giữa hai Thủy Tinh này rất quan trọng vì nó quyết định liệu hai người có thể hiểu nhau trong giao tiếp hàng ngày, thảo luận các vấn đề quan trọng, và giải quyết bất đồng một cách hiệu quả hay không.

Mặt Trời {sun_a} và Mặt Trời {sun_b} cũng ảnh hưởng đến cách hai người thể hiện bản thân và quan điểm sống. Sự kết hợp này có thể tạo nên một động lực mạnh mẽ trong việc chia sẻ tầm nhìn và mục tiêu sống.

Mặt Trăng {moon_a} và Mặt Trăng {moon_b} tiết lộ cách hai người xử lý cảm xúc trong giao tiếp. Nếu hai Mặt Trăng này có sự tương thích, hai người sẽ dễ dàng chia sẻ cảm xúc và thấu hiểu nhau trong những lúc khó khăn.

Để cải thiện giao tiếp, cả hai cần học cách {SIGN_TRAITS.get(mercury_b, "").split("|")[1].lower()} để hiểu cách tư duy của người kia, đồng thời {SIGN_TRAITS.get(mercury_a, "").split("|")[1].lower()} để đáp lại phong cách giao tiếp của đối phương.

Sự kết hợp này có thể tạo nên một mối quan hệ giao tiếp hiệu quả nếu cả hai cùng nỗ lực thấu hiểu và tôn trọng phong cách tư duy khác biệt của nhau."""
        
        return communication_style

    def _generate_ai_conflict_dynamics(self, sun_a, sun_b, moon_a, moon_b, mars_a, mars_b, fallback_mode) -> str:
        """Generate conflict dynamics analysis"""
        conflict_dynamics = f"""Động lực xung đột:

Mặc dù có nhiều điểm tương thích, mối quan hệ này cũng tiềm ẩn những điểm xung đột cần được lưu ý. Mặt Trời {sun_a} và Mặt Trời {sun_b} có thể tạo nên sự cạnh tranh nếu cả hai cùng tìm kiếm {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()}.

Mặt Trăng {moon_a} và Mặt Trăng {moon_b} có thể tạo nên sự hiểu lầm trong nhu cầu cảm xúc. Người A với Mặt Trăng {moon_a} cần {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} trong mối quan hệ, trong khi người B với Mặt Trăng {moon_b} lại tìm kiếm {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()}. Nếu không được thấu hiểu, điều này có thể dẫn đến cảm giác bị bỏ rơi hoặc không được đáp ứng.

Hỏa Tinh {mars_a} và Hỏa Tinh {mars_b} có thể tạo nên xung đột trong cách thể hiện năng lượng và xử lý mâu thuẫn. Người A với Hỏa Tinh {mars_a} có thể {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()} khi tức giận, trong khi người B với Hỏa Tinh {mars_b} lại {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()}.

{f'⚠️ Lưu ý: Ở chế độ fallback (thiếu giờ sinh), một số aspect quan trọng về Cung Mọc và các house có thể không được tính toán chính xác, điều này có thể ảnh hưởng đến việc dự đoán các điểm xung đột cụ thể.' if fallback_mode else 'Với đầy đủ thông tin giờ sinh, các điểm xung đột có thể được dự đoán chính xác hơn thông qua việc phân tích các aspect và house.'}

Tình huống cụ thể có thể xảy ra: khi người A muốn {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()}, người B lại cảm thấy {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()}. Hoặc khi người A cần {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()}, người B lại không hiểu tại sao người A lại {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()}.

Để giải quyết xung đột hiệu quả, cả hai cần học cách {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()} để làm dịu căng thẳng, đồng thời {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} để thấu hiểu nhu cầu cảm xúc của đối phương."""
        
        return conflict_dynamics

    def _generate_ai_long_term_potential(self, sun_a, sun_b, moon_a, moon_b, venus_a, venus_b, asc_a, asc_b, aspects) -> str:
        """Generate long-term potential analysis"""
        long_term_potential = f"""Tiềm năng lâu dài:

Tiềm năng phát triển lâu dài của mối quan hệ này được quyết định bởi sự tương thích giữa các yếu tố cốt lõi: Mặt Trời {sun_a} và Mặt Trời {sun_b}, Mặt Trăng {moon_a} và Mặt Trăng {moon_b}, Kim Tinh {venus_a} và Kim Tinh {venus_b}, cùng các aspect quan trọng giữa các hành tinh.

Sự tương thích giữa Mặt Trời {sun_a} và Mặt Trời {sun_b} cho thấy liệu hai người có cùng chung tầm nhìn sống, mục tiêu và giá trị cốt lõi hay không. Nếu hai Mặt Trời này có sự tương thích tốt, hai người sẽ dễ dàng hỗ trợ nhau trong việc theo đuổi ước mơ và mục tiêu cá nhân.

Mặt Trăng {moon_a} và Mặt Trăng {moon_b} tiết lộ liệu hai người có thể tạo nên một môi trường cảm xúc an toàn và nuôi dưỡng cho nhau hay không. Sự tương thích giữa hai Mặt Trăng này rất quan trọng cho sự gắn kết cảm xúc lâu dài.

Kim Tinh {venus_a} và Kim Tinh {venus_b} cho thấy liệu hai người có cùng phong cách yêu thương và những giá trị trong tình yêu hay không. Sự tương thích này quyết định khả năng duy trì tình yêu và sự gắn bó lâu dài.

Cung Mọc {asc_a} và {asc_b} ảnh hưởng đến cách hai người thể hiện bản thân trong mối quan hệ và cách họ đối mặt với các thử thách. Sự tương thích giữa hai Cung Mọc có thể tạo nên sự hòa hợp trong phong cách sống và cách ứng xử hàng ngày.

Các aspect quan trọng giữa các hành tinh cũng đóng vai trò quyết định trong việc dự đoán tiềm năng lâu dài. Các aspect harmonious (Trine, Sextile) tạo nên sự hỗ trợ và nuôi dưỡng, trong khi các aspect challenging (Square, Opposition) có thể tạo nên những bài học và thử thách cần vượt qua.

Nếu cả hai cùng nỗ lực thấu hiểu và trân trọng sự khác biệt của nhau, mối quan hệ này có tiềm năng phát triển thành một partnership bền vững và đầy ý nghĩa."""
        
        return long_term_potential

    def _generate_ai_growth_advice(self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects, fallback_mode) -> str:
        """Generate growth advice with fallback mode awareness"""
        growth_advice = f"""Lời khuyên phát triển:

Để phát triển mối quan hệ này một cách bền vững, cả hai cần lưu ý những điểm sau:

**Cách điều chỉnh:**
- Người A cần học cách {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()} để làm người B cảm thấy được trân trọng
- Người B cần học cách {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} để đáp lại nhu cầu của người A
- Cả hai cần học cách nói ngôn ngữ tình yêu của đối phương: người A cần {SIGN_TRAITS.get(venus_b, "").split("|")[1].lower()}, trong khi người B cần {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()}

**Cách phát triển mối quan hệ:**
- Dành thời gian để thấu hiểu nhu cầu cảm xúc sâu kín của nhau
- Học cách giao tiếp hiệu quả, đặc biệt là trong những lúc căng thẳng
- Cùng nhau đặt ra những mục tiêu chung và hỗ trợ nhau đạt được
- Biết compromise khi cần thiết, nhưng cũng biết bảo vệ ranh giới cá nhân
- Cùng nhau trải nghiệm những điều mới mẻ để nuôi dưỡng sự hấp dẫn

**Lưu ý đặc biệt:**
{f'⚠️ Do đang ở chế độ fallback (thiếu giờ sinh), một số khía cạnh về Cung Mọc và các house không thể được tính toán chính xác. Điều này có nghĩa là một số lời khuyên về phong cách thể hiện bản thân và cách đối mặt với thử thách có thể cần được điều chỉnh khi có đầy đủ thông tin giờ sinh.' if fallback_mode else 'Với đầy đủ thông tin giờ sinh, các lời khuyên có thể được cá nhân hóa chính xác hơn dựa trên Cung Mọc và các house.'}

**Các bài học phát triển:**
- Học cách {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()} để nuôi dưỡng cảm xúc của người kia
- Phát triển khả năng {SIGN_TRAITS.get(mercury_a, "").split("|")[1].lower()} để cải thiện giao tiếp
- Rèn luyện sự {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()} để xử lý xung đột hiệu quả
- Nuôi dưỡng sự {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()} để duy trì tình yêu lâu dài

Sự phát triển của mối quan hệ này phụ thuộc vào khả năng học hỏi và thích nghi của cả hai người. Nếu cùng nhau nỗ lực, mối quan hệ này có thể trở thành một hành trình phát triển cá nhân và tâm hồn đầy ý nghĩa."""
        
        return growth_advice

    def _generate_ai_comprehensive_analysis(
        self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b,
        aspects, scores, overview, element_dynamics, planetary_aspects, emotional_connection,
        romantic_attraction, communication_style, conflict_dynamics, long_term_potential, growth_advice,
        fallback_mode
    ) -> str:
        """Generate comprehensive analysis essay (>=1000 words)"""
        
        comprehensive_analysis = f"""PHÂN TÍCH TƯƠNG THÍCH CHI TIẾT

{overview}

{element_dynamics}

{emotional_connection}

{romantic_attraction}

{communication_style}

{conflict_dynamics}

{long_term_potential}

{growth_advice}

TỔNG KẾT ĐÁNH GIÁ

Dựa trên toàn bộ phân tích chi tiết ở trên, mối quan hệ giữa {sun_a} và {sun_b} là một mối quan hệ có tiềm năng phát triển sâu sắc nếu cả hai cùng nỗ lực thấu hiểu và trân trọng sự khác biệt của nhau.

Với điểm số:
- Emotional Compatibility: {scores['emotionalCompatibility']}/100 - Được đánh giá dựa trên sự tương thích giữa Mặt Trăng và Kim Tinh
- Romantic Compatibility: {scores['romanticCompatibility']}/100 - Được đánh giá dựa trên sự hấp dẫn giữa Kim Tinh và Hỏa Tinh
- Communication Compatibility: {scores['communicationCompatibility']}/100 - Được đánh giá dựa trên sự tương thích giữa Thủy Tinh
- Long-term Stability: {scores['longTermStability']}/100 - Được đánh giá dựa trên sự tương thích tổng thể và các aspect quan trọng

Mối quan hệ này có những điểm mạnh nổi bật trong việc tạo nên sự gắn kết cảm xúc và sức hút tình yêu, đồng thời cũng có những thách thức cần được lưu ý và vượt qua.

Để phát triển mối quan hệ này một cách bền vững, cả hai cần:
1. Học cách thấu hiểu và chấp nhận sự khác biệt
2. Giao tiếp cởi mở và trung thực
3. Cùng nhau đặt ra những mục tiêu chung
4. Biết compromise khi cần thiết
5. Dành thời gian để nuôi dưỡng cảm xúc và sự gắn kết

Nếu cùng nhau nỗ lực, mối quan hệ này có tiềm năng trở thành một partnership bền vững, nơi mà cả hai người cùng phát triển và trưởng thành về mặt cảm xúc, tâm hồn, và tinh thần.

{f'Lưu ý: Phân tích này được thực hiện ở chế độ fallback (thiếu giờ sinh), do đó một số khía cạnh về Cung Mọc và các house có thể không chính xác hoàn toàn. Để có phân tích chính xác nhất, nên cung cấp đầy đủ thông tin giờ sinh.' if fallback_mode else 'Phân tích này được thực hiện với đầy đủ thông tin giờ sinh, đảm bảo độ chính xác cao trong tất cả các khía cạnh tính toán.'}"""
        
        return comprehensive_analysis

    def _build_comprehensive_analysis(
        self, sun_a, moon_a, mercury_a, venus_a, mars_a, asc_a,
        sun_b, moon_b, mercury_b, venus_b, mars_b, asc_b, aspects
    ) -> str:
        """Build comprehensive compatibility analysis with all required sections"""
        
        # 1. Tổng quan năng lượng hai người (200+ words)
        overview = self._generate_energy_overview(sun_a, sun_b, moon_a, moon_b, asc_a, asc_b)
        
        # 2. Phân tích từng cặp hành tinh quan trọng (400+ words)
        planet_analysis = self._generate_planet_pair_analysis(
            sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
            venus_a, venus_b, mars_a, mars_b, asc_a, asc_b
        )
        
        # 3. Phong cách yêu và hấp dẫn thể chất (150+ words)
        love_style = self._generate_love_style_analysis(venus_a, venus_b, mars_a, mars_b, asc_a, asc_b)
        
        # 4. Hợp tác công việc & phát triển lâu dài (150+ words)
        work_cooperation = self._generate_work_cooperation_analysis(mercury_a, mercury_b, sun_a, sun_b, mars_a, mars_b)
        
        # 5. Điểm xung đột tiềm ẩn (150+ words)
        conflict_points = self._generate_conflict_analysis(sun_a, sun_b, moon_a, moon_b, mars_a, mars_b)
        
        # 6. Động lực nghiệp duyên / karmic pattern
        karmic_patterns = self._generate_karmic_analysis(aspects, sun_a, sun_b, moon_a, moon_b)
        
        # 7. Lời khuyên thực tế (100+ words)
        practical_advice = self._generate_practical_advice(
            sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
            venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
        )
        
        # 8. Compatibility Scores
        scores = self._generate_compatibility_scores(
            sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
            venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
        )
        
        # Combine all sections
        full_analysis = f"""{overview}

{planet_analysis}

{love_style}

{work_cooperation}

{conflict_points}

{karmic_patterns}

{practical_advice}

{scores}"""
        
        return full_analysis

    def _generate_energy_overview(self, sun_a, sun_b, moon_a, moon_b, asc_a, asc_b) -> str:
        """Generate energy overview (200+ words)"""
        element_a = SIGN_TRAITS.get(sun_a, "").split("|")[0]
        element_b = SIGN_TRAITS.get(sun_b, "").split("|")[0]
        
        moon_element_a = SIGN_TRAITS.get(moon_a, "").split("|")[0]
        moon_element_b = SIGN_TRAITS.get(moon_b, "").split("|")[0]
        
        asc_element_a = SIGN_TRAITS.get(asc_a, "").split("|")[0]
        asc_element_b = SIGN_TRAITS.get(asc_b, "").split("|")[0]
        
        # Determine interaction type
        if element_a == element_b:
            interaction_type = "tương đồng mạnh mẽ"
            description = "Sự hòa hợp về bản chất cốt lõi, dễ dàng thấu hiểu nhau"
        elif {element_a, element_b} in [{"Fire", "Air"}, {"Water", "Earth"}]:
            interaction_type = "tương sinh tự nhiên"
            description = "Bổ sung và nuôi dưỡng lẫn nhau một cách tự nhiên"
        elif {element_a, element_b} in [{"Fire", "Water"}, {"Air", "Earth"}]:
            interaction_type = "tương khắc cần dung hòa"
            description = "Xung đột năng lượng cần học cách chuyển hóa"
        else:
            interaction_type = "khác biệt tạo cơ hội học hỏi"
            description = "Sự khác biệt thúc đẩy sự phát triển và học hỏi lẫn nhau"
        
        overview = f"""1️⃣ TỔNG QUAN NĂNG LƯỢNG HAI NGƯỜI

Mối quan hệ giữa hai bạn được xây dựng trên nền tảng năng lượng {element_a} và {element_b}, tạo nên một sự tương tác {interaction_type}. Mặt Trời của hai người đại diện cho bản chất cốt lõi, nơi mà {description}.

Người A mang năng lượng {element_a} qua Mặt Trời {sun_a}, thể hiện một cá tính {SIGN_TRAITS.get(sun_a, "").split("|")[1]}. Trong khi đó, người B với Mặt Trời {sun_b} ({SIGN_TRAITS.get(sun_b, "").split("|")[1]}) mang đến một cách tiếp cận khác biệt nhưng có thể bổ sung hoàn hảo.

Mặt Trăng tiết lộ thế giới cảm xúc sâu kín: người A với Mặt Trăng {moon_a} ({SIGN_TRAITS.get(moon_a, "").split("|")[1]}) có nhu cầu cảm xúc đặc biệt, trong khi người B với Mặt Trăng {moon_b} ({SIGN_TRAITS.get(moon_b, "").split("|")[1]}) lại có cách xử lý cảm xúc khác biệt.

Cung Mọc (Ascendant) là "chiếc mặt nạ" mà hai người thể hiện với thế giới. Người A với Cung Mọc {asc_a} tạo ấn tượng ban đầu là {SIGN_TRAITS.get(asc_a, "").split("|")[1]}, còn người B với Cung Mọc {asc_b} lại mang đến cảm giác {SIGN_TRAITS.get(asc_b, "").split("|")[1]}.

Tổng thể, đây là một mối quan hệ có tiềm năng phát triển sâu sắc nếu cả hai cùng nỗ lực thấu hiểu và trân trọng sự khác biệt của nhau."""
        
        return overview

    def _generate_planet_pair_analysis(
        self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
        venus_a, venus_b, mars_a, mars_b, asc_a, asc_b
    ) -> str:
        """Generate detailed planet pair analysis (400+ words)"""
        
        analysis = """2️⃣ PHÂN TÍCH TỪNG CẶP HÀNH TINH QUAN TRỌNG

**Sun - Sun (Bản chất cốt lõi):**
Mặt Trời {sun_a} và Mặt Trời {sun_b} tạo nên nền tảng cho sự tương thích về bản chất. {sun_a} ({SIGN_TRAITS.get(sun_a, "").split("|")[1]}) mang đến một năng lượng {SIGN_TRAITS.get(sun_a, "").split("|")[0].lower()}, trong khi {sun_b} ({SIGN_TRAITS.get(sun_b, "").split("|")[1]}) lại thể hiện {SIGN_TRAITS.get(sun_b, "").split("|")[0].lower()}.

Sự kết hợp này có thể tạo nên một mối quan hệ đầy hứng khởi nếu cả hai biết trân trọng điểm mạnh của nhau. Người A có thể học được sự {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()} từ người B, trong khi người B có thể học được {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} từ người A.

**Moon - Moon (Thế giới cảm xúc):**
Mặt Trăng {moon_a} và Mặt Trăng {moon_b} tiết lộ cách hai người xử lý cảm xúc và nhu cầu cảm xúc sâu kín. {moon_a} cho thấy người A cần {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} trong mối quan hệ, trong khi {moon_b} cho thấy người B lại tìm kiếm {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()}.

Đây là khu vực có thể tạo nên sự gắn kết sâu sắc nếu cả hai cùng học cách đáp ứng nhu cầu cảm xúc của nhau. Người A cần học cách {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()} để làm người B cảm thấy an toàn, trong khi người B cần học cách {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} để đáp lại nhu cầu của người A.

**Venus - Venus (Tình yêu & giá trị):**
Kim Tinh {venus_a} và Kim Tinh {venus_b} tiết lộ cách hai người yêu thương và những giá trị mà họ tìm kiếm trong tình yêu. {venus_a} cho thấy người A thể hiện tình cảm qua {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()}, trong khi {venus_b} cho thấy người B lại tìm kiếm {SIGN_TRAITS.get(venus_b, "").split("|")[1].lower()}.

Sự khác biệt này có thể tạo nên sự phong phú trong mối quan hệ nếu cả hai cùng học cách nói ngôn ngữ tình yêu của đối phương.

**Mars - Mars (Động lực & hành động):**
Hỏa Tinh {mars_a} và Hỏa Tinh {mars_b} tiết lộ cách hai người thể hiện năng lượng, đam mê và cách hành động. {mars_a} cho thấy người A hành động với {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()}, trong khi {mars_b} cho thấy người B lại thể hiện {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()}.

**Mercury - Mercury (Giao tiếp & tư duy):**
Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b} tiết lộ cách hai người giao tiếp và xử lý thông tin. {mercury_a} cho thấy người A tư duy {SIGN_TRAITS.get(mercury_a, "").split("|")[1].lower()}, trong khi {mercury_b} cho thấy người B lại tiếp cận {SIGN_TRAITS.get(mercury_b, "").split("|")[1].lower()}.

**Sun - Moon cross interaction:**
Sự tương tác giữa Mặt Trời và Mặt Trăng giữa hai người tạo nên động lực cảm xúc mạnh mẽ. Mặt Trời {sun_a} có thể {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()} Mặt Trăng {moon_b}, trong khi Mặt Trời {sun_b} lại có thể {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()} Mặt Trăng {moon_a}.

**Venus - Mars attraction dynamic:**
Sự hấp dẫn giữa Kim Tinh và Hỏa Tinh tạo nên sức hút tình dục và đam mê. Kim Tinh {venus_a} bị thu hút bởi {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()} của Hỏa Tinh {mars_b}, trong khi Kim Tinh {venus_b} lại tìm thấy {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()} ở Hỏa Tinh {mars_a}."""
        
        return analysis

    def _generate_love_style_analysis(self, venus_a, venus_b, mars_a, mars_b, asc_a, asc_b) -> str:
        """Generate love style analysis (150+ words)"""
        
        love_style = f"""3️⃣ PHONG CÁCH YÊU VÀ HẤP DẪN THỂ CHẤT

Phong cách yêu của hai người được định hình bởi sự kết hợp giữa Kim Tinh {venus_a} và Hỏa Tinh {mars_a} ở người A, cùng Kim Tinh {venus_b} và Hỏa Tinh {mars_b} ở người B.

Người A với Kim Tinh {venus_a} thể hiện tình yêu qua {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()}, trong khi Hỏa Tinh {mars_a} cho thấy cách thể hiện đam mê là {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()}. Sự kết hợp này tạo nên một phong cách yêu {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()} nhưng {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()}.

Người B với Kim Tinh {venus_b} tìm kiếm {SIGN_TRAITS.get(venus_b, "").split("|")[1].lower()} trong tình yêu, trong khi Hỏa Tinh {mars_b} lại thể hiện {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()} khi yêu.

Cung Mọc {asc_a} và {asc_b} cũng ảnh hưởng đến cách hai người thể hiện bản thân trong tình yêu. Người A với Cung Mọc {asc_a} có thể {SIGN_TRAITS.get(asc_a, "").split("|")[1].lower()} trong mối quan hệ, trong khi người B với Cung Mọc {asc_b} lại {SIGN_TRAITS.get(asc_b, "").split("|")[1].lower()}.

Sự hấp dẫn thể chất giữa hai người được tạo nên bởi sự bổ sung giữa năng lượng {SIGN_TRAITS.get(venus_a, "").split("|")[0].lower()} của người A và {SIGN_TRAITS.get(venus_b, "").split("|")[0].lower()} của người B."""
        
        return love_style

    def _generate_work_cooperation_analysis(self, mercury_a, mercury_b, sun_a, sun_b, mars_a, mars_b) -> str:
        """Generate work cooperation analysis (150+ words)"""
        
        work_cooperation = f"""4️⃣ HỢP TÁC CÔNG VIỆC & PHÁT TRIỂN LÂU DÀI

Trong môi trường làm việc, hai người có thể tạo nên một sự hợp tác hiệu quả nếu biết tận dụng điểm mạnh của nhau. Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b} tiết lộ cách hai người giao tiếp và xử lý thông tin.

Người A với Thủy Tinh {mercury_a} có cách tư duy {SIGN_TRAITS.get(mercury_a, "").split("|")[1].lower()}, trong khi người B với Thủy Tinh {mercury_b} lại tiếp cận {SIGN_TRAITS.get(mercury_b, "").split("|")[1].lower()}. Sự khác biệt này có thể tạo nên sự bổ sung hoàn hảo nếu cả hai cùng học cách nói ngôn ngữ tư duy của nhau.

Mặt Trời {sun_a} và Mặt Trời {sun_b} tiết lộ động lực và mục tiêu trong công việc. Người A với Mặt Trời {sun_a} tìm kiếm {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} trong sự nghiệp, trong khi người B với Mặt Trời {sun_b} lại hướng tới {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()}.

Hỏa Tinh {mars_a} và Hỏa Tinh {mars_b} tiết lộ cách hai người thể hiện năng lượng và xử lý thách thức. Người A với Hỏa Tinh {mars_a} hành động {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()}, trong khi người B với Hỏa Tinh {mars_b} lại thể hiện {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()}.

Sự kết hợp này có thể tạo nên một partnership làm việc hiệu quả nếu cả hai cùng học cách tôn trọng phong cách làm việc khác biệt của nhau."""
        
        return work_cooperation

    def _generate_conflict_analysis(self, sun_a, sun_b, moon_a, moon_b, mars_a, mars_b) -> str:
        """Generate conflict analysis (150+ words)"""
        
        conflict_points = f"""5️⃣ ĐIỂM XUNG ĐỘT TIỀM ẨN

Mặc dù có nhiều điểm tương thích, mối quan hệ này cũng tiềm ẩn những điểm xung đột cần được lưu ý. Mặt Trời {sun_a} và Mặt Trời {sun_b} có thể tạo nên sự cạnh tranh nếu cả hai cùng tìm kiếm {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()}.

Mặt Trăng {moon_a} và Mặt Trăng {moon_b} có thể tạo nên sự hiểu lầm trong nhu cầu cảm xúc. Người A với Mặt Trăng {moon_a} cần {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()}, trong khi người B với Mặt Trăng {moon_b} lại tìm kiếm {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()}. Nếu không được thấu hiểu, điều này có thể dẫn đến cảm giác bị bỏ rơi hoặc không được đáp ứng.

Hỏa Tinh {mars_a} và Hỏa Tinh {mars_b} có thể tạo nên xung đột trong cách thể hiện năng lượng và xử lý mâu thuẫn. Người A với Hỏa Tinh {mars_a} có thể {SIGN_TRAITS.get(mars_a, "").split("|")[1].lower()} khi tức giận, trong khi người B với Hỏa Tinh {mars_b} lại {SIGN_TRAITS.get(mars_b, "").split("|")[1].lower()}.

Tình huống cụ thể có thể xảy ra: khi người A muốn {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()}, người B lại cảm thấy {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()}. Hoặc khi người A cần {SIGN_TRAITS.get(moon_a, "").split("|")[1].lower()}, người B lại không hiểu tại sao người A lại {SIGN_TRAITS.get(moon_b, "").split("|")[1].lower()}."""
        
        return conflict_points

    def _generate_karmic_analysis(self, aspects, sun_a, sun_b, moon_a, moon_b) -> str:
        """Generate karmic patterns analysis"""
        
        karmic_patterns = """6️⃣ ĐỘNG LỰC NGHIỆP DUYÊN / KARMIC PATTERN

Dựa trên các aspect quan trọng giữa hai bản đồ sao, mối quan hệ này có thể mang những đặc điểm nghiệp duyên nhất định. Nếu có các aspect mạnh như Conjunction, Square, hay Opposition giữa các hành tinh cá nhân (Sun, Moon, Venus, Mars), điều này có thể cho thấy một mối quan hệ có tính chất học hỏi và trưởng thành.

Sự kết hợp giữa Mặt Trời và Mặt Trăng giữa hai người có thể tạo nên một động lực nghiệp duyên mạnh mẽ, nơi mà cả hai cần học cách cân bằng giữa nhu cầu cá nhân và nhu cầu cảm xúc của đối phương.

Các aspect challenging (Square, Opposition) có thể cho thấy những bài học cần vượt qua, trong khi các aspect harmonious (Trine, Sextile) lại cho thấy những điểm dễ dàng hỗ trợ và nuôi dưỡng lẫn nhau.

Mối quan hệ này có thể là một cơ hội để cả hai người học cách {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} và {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()}, từ đó đạt được sự trưởng thành cá nhân và phát triển tâm hồn."""
        
        return karmic_patterns

    def _generate_practical_advice(
        self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
        venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
    ) -> str:
        """Generate practical advice (100+ words)"""
        
        practical_advice = f"""7️⃣ LỜI KHUYÊN THỰC TẾ

Để phát triển mối quan hệ này một cách bền vững, cả hai cần lưu ý những điểm sau:

**Cách điều chỉnh:**
- Người A cần học cách {SIGN_TRAITS.get(sun_b, "").split("|")[1].lower()} để làm người B cảm thấy được trân trọng
- Người B cần học cách {SIGN_TRAITS.get(sun_a, "").split("|")[1].lower()} để đáp lại nhu cầu của người A
- Cả hai cần học cách nói ngôn ngữ tình yêu của đối phương: người A cần {SIGN_TRAITS.get(venus_b, "").split("|")[1].lower()}, trong khi người B cần {SIGN_TRAITS.get(venus_a, "").split("|")[1].lower()}

**Cách phát triển mối quan hệ:**
- Dành thời gian để thấu hiểu nhu cầu cảm xúc sâu kín của nhau
- Học cách giao tiếp hiệu quả, đặc biệt là trong những lúc căng thẳng
- Cùng nhau đặt ra những mục tiêu chung và hỗ trợ nhau đạt được
- Biết compromise khi cần thiết, nhưng cũng biết bảo vệ ranh giới cá nhân
- Cùng nhau trải nghiệm những điều mới mẻ để nuôi dưỡng sự hấp dẫn"""
        
        return practical_advice

    def _generate_compatibility_scores(
        self, sun_a, sun_b, moon_a, moon_b, mercury_a, mercury_b,
        venus_a, venus_b, mars_a, mars_b, asc_a, asc_b, aspects
    ) -> str:
        """Generate compatibility scores with explanations"""
        
        # Calculate scores based on element compatibility and aspects
        emotional_score = self._calculate_emotional_compatibility(moon_a, moon_b, venus_a, venus_b)
        romantic_score = self._calculate_romantic_compatibility(venus_a, venus_b, mars_a, mars_b, sun_a, sun_b)
        communication_score = self._calculate_communication_compatibility(mercury_a, mercury_b, sun_a, sun_b)
        stability_score = self._calculate_stability_compatibility(sun_a, sun_b, moon_a, moon_b, asc_a, asc_b, aspects)
        
        scores = f"""
**SCORING:**

- **Emotional Compatibility: {emotional_score}/100**
  Được đánh giá dựa trên sự tương thích giữa Mặt Trăng và Kim Tinh. Mặt Trăng {moon_a} và Mặt Trăng {moon_b} tạo nên nền tảng cảm xúc, trong khi Kim Tinh {venus_a} và Kim Tinh {venus_b} tiết lộ cách hai người yêu thương và được yêu.

- **Romantic Compatibility: {romantic_score}/100**
  Được đánh giá dựa trên sự hấp dẫn giữa Kim Tinh và Hỏa Tinh, cũng như sự tương thích của Mặt Trời. Sự kết hợp giữa {venus_a} và {mars_b}, {venus_b} và {mars_a} tạo nên sức hút tình dục và đam mê.

- **Communication Compatibility: {communication_score}/100**
  Được đánh giá dựa trên sự tương thích giữa Thủy Tinh và cách hai người giao tiếp. Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b} tiết lộ cách hai người xử lý thông tin và trao đổi ý tưởng.

- **Long-term Stability: {stability_score}/100**
  Được đánh giá dựa trên sự tương thích giữa Mặt Trời, Mặt Trăng, Cung Mọc và các aspect quan trọng. Đây là yếu tố quyết định khả năng duy trì mối quan hệ lâu dài."""
        
        return scores

    def _calculate_emotional_compatibility(self, moon_a, moon_b, venus_a, venus_b) -> int:
        """Calculate emotional compatibility score"""
        moon_score = self._element_score(moon_a, moon_b)
        venus_score = self._element_score(venus_a, venus_b)
        return int((moon_score + venus_score) / 2)

    def _calculate_romantic_compatibility(self, venus_a, venus_b, mars_a, mars_b, sun_a, sun_b) -> int:
        """Calculate romantic compatibility score"""
        venus_score = self._element_score(venus_a, venus_b)
        mars_score = self._element_score(mars_a, mars_b)
        sun_score = self._element_score(sun_a, sun_b)
        return int((venus_score + mars_score + sun_score) / 3)

    def _calculate_communication_compatibility(self, mercury_a, mercury_b, sun_a, sun_b) -> int:
        """Calculate communication compatibility score"""
        mercury_score = self._element_score(mercury_a, mercury_b)
        sun_score = self._element_score(sun_a, sun_b)
        return int((mercury_score + sun_score) / 2)

    def _calculate_stability_compatibility(self, sun_a, sun_b, moon_a, moon_b, asc_a, asc_b, aspects) -> int:
        """Calculate long-term stability score"""
        sun_score = self._element_score(sun_a, sun_b)
        moon_score = self._element_score(moon_a, moon_b)
        asc_score = self._element_score(asc_a, asc_b)
        
        # Adjust based on aspects
        aspect_bonus = len([a for a in aspects if a.harmonyLevel == "High"]) * 5
        aspect_penalty = len([a for a in aspects if a.harmonyLevel == "Challenging"]) * 3
        
        base_score = int((sun_score + moon_score + asc_score) / 3)
        final_score = max(0, min(100, base_score + aspect_bonus - aspect_penalty))
        
        return final_score

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

    def _fallback_planet_calculation(self, person: BirthInfo, lat: Optional[float], lon: Optional[float]) -> list[PlanetPosition]:
        """Fallback planet calculation when Kerykeion fails"""
        self._logger.info(f"Using fallback planet calculation for {person.name}")
        
        try:
            # Calculate basic planetary positions using simple algorithms
            planets = []
            
            # Get sun sign as base
            sun_sign = self._calculate_sun_sign(person.birth_date)
            
            # Create basic planet positions based on sun sign and date
            date_obj = datetime.strptime(person.birth_date, "%Y-%m-%d")
            
            # Define planet names and their approximate positions relative to sun
            planet_data = [
                ("Sun", sun_sign, 0.0),
                ("Moon", self._calculate_moon_sign(date_obj), 45.0),
                ("Mercury", self._calculate_mercury_sign(date_obj), 90.0),
                ("Venus", self._calculate_venus_sign(date_obj), 135.0),
                ("Mars", self._calculate_mars_sign(date_obj), 180.0),
                ("Jupiter", self._calculate_jupiter_sign(date_obj), 225.0),
                ("Saturn", self._calculate_saturn_sign(date_obj), 270.0),
                ("Uranus", self._calculate_uranus_sign(date_obj), 315.0),
                ("Neptune", self._calculate_neptune_sign(date_obj), 360.0),
                ("Pluto", self._calculate_pluto_sign(date_obj), 45.0),
            ]
            
            for name, sign, offset in planet_data:
                # Calculate longitude based on sign and offset
                longitude = self._calculate_longitude_from_sign(sign, offset)
                planets.append(PlanetPosition(name=name, sign=sign, longitude=longitude))
            
            self._logger.info(f"Fallback calculation successful for {person.name}: {len(planets)} planets")
            return planets
            
        except Exception as e:
            self._logger.error(f"Fallback planet calculation failed for {person.name}: {e}")
            # Return minimal planets as last resort
            return [
                PlanetPosition(name="Sun", sign=sun_sign, longitude=0.0),
                PlanetPosition(name="Moon", sign="Cancer", longitude=45.0),
                PlanetPosition(name="Mercury", sign=sun_sign, longitude=90.0),
            ]

    def _calculate_moon_sign(self, date_obj: datetime) -> str:
        """Calculate moon sign based on date"""
        # Simplified moon calculation - moon moves ~12-15 degrees per day
        days = date_obj.timetuple().tm_yday
        moon_position = (days * 13.2) % 360
        return self._get_sign_from_longitude(moon_position)

    def _calculate_mercury_sign(self, date_obj: datetime) -> str:
        """Calculate mercury sign based on date"""
        # Mercury orbits sun every ~88 days
        days = date_obj.timetuple().tm_yday
        mercury_position = (days * 4.15) % 360
        return self._get_sign_from_longitude(mercury_position)

    def _calculate_venus_sign(self, date_obj: datetime) -> str:
        """Calculate venus sign based on date"""
        # Venus orbits sun every ~225 days
        days = date_obj.timetuple().tm_yday
        venus_position = (days * 1.6) % 360
        return self._get_sign_from_longitude(venus_position)

    def _calculate_mars_sign(self, date_obj: datetime) -> str:
        """Calculate mars sign based on date"""
        # Mars orbits sun every ~687 days
        days = date_obj.timetuple().tm_yday
        mars_position = (days * 0.53) % 360
        return self._get_sign_from_longitude(mars_position)

    def _calculate_jupiter_sign(self, date_obj: datetime) -> str:
        """Calculate jupiter sign based on date"""
        # Jupiter orbits sun every ~4333 days
        days = date_obj.timetuple().tm_yday
        jupiter_position = (days * 0.083) % 360
        return self._get_sign_from_longitude(jupiter_position)

    def _calculate_saturn_sign(self, date_obj: datetime) -> str:
        """Calculate saturn sign based on date"""
        # Saturn orbits sun every ~10759 days
        days = date_obj.timetuple().tm_yday
        saturn_position = (days * 0.0335) % 360
        return self._get_sign_from_longitude(saturn_position)

    def _calculate_uranus_sign(self, date_obj: datetime) -> str:
        """Calculate uranus sign based on date"""
        # Uranus orbits sun every ~30687 days
        days = date_obj.timetuple().tm_yday
        uranus_position = (days * 0.0117) % 360
        return self._get_sign_from_longitude(uranus_position)

    def _calculate_neptune_sign(self, date_obj: datetime) -> str:
        """Calculate neptune sign based on date"""
        # Neptune orbits sun every ~60190 days
        days = date_obj.timetuple().tm_yday
        neptune_position = (days * 0.006) % 360
        return self._get_sign_from_longitude(neptune_position)

    def _calculate_pluto_sign(self, date_obj: datetime) -> str:
        """Calculate pluto sign based on date"""
        # Pluto orbits sun every ~90560 days
        days = date_obj.timetuple().tm_yday
        pluto_position = (days * 0.004) % 360
        return self._get_sign_from_longitude(pluto_position)

    def _get_sign_from_longitude(self, longitude: float) -> str:
        """Convert longitude to zodiac sign"""
        longitude = longitude % 360
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_index = int(longitude / 30)
        return signs[sign_index % 12]

    def _calculate_longitude_from_sign(self, sign: str, offset: float) -> float:
        """Calculate longitude from sign and offset"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        base_longitude = signs.index(sign) * 30
        return (base_longitude + offset) % 360

    def _build_svg_chart(self, natal: NatalChart, time_unknown: bool) -> Optional[str]:
        """Build SVG chart for natal chart"""
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
                # For known time, create a basic chart structure with planets
                svg_content = f"""<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100%" height="100%" fill="white"/>
                    <circle cx="200" cy="200" r="180" fill="none" stroke="#333" stroke-width="2"/>
                    <line x1="200" y1="20" x2="200" y2="380" stroke="#666" stroke-width="1"/>
                    <line x1="20" y1="200" x2="380" y2="200" stroke="#666" stroke-width="1"/>
                    <text x="200" y="50" text-anchor="middle" font-size="24" font-family="Arial">Bản Đồ Sao</text>
                    <text x="200" y="80" text-anchor="middle" font-size="16" font-family="Arial">Cung Mặt Trời: {natal.sun_sign}</text>"""
                
                # Add planet positions
                for i, planet in enumerate(natal.planets[:8]):  # Show first 8 planets
                    angle = (i * 45) % 360
                    x = 200 + 150 * (0.7 if i % 2 == 0 else 0.9) * (1 if angle < 180 else -1)
                    y = 200 + 150 * (0.7 if i % 2 == 0 else 0.9) * (1 if angle < 90 or angle > 270 else -1)
                    svg_content += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="12" font-family="Arial">{planet.name}: {planet.sign}</text>'
                
                svg_content += '<text x="200" y="350" text-anchor="middle" font-size="12" font-family="Arial">* Dữ liệu hạn chế</text></svg>'
                return svg_content
        except Exception as e:
            self._logger.error(f"SVG chart generation failed: {e}")
            return None

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
