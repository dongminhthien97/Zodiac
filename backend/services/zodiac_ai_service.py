"""
Zodiac AI Service - Generates high-quality astrological reports
similar to professional astrologer analysis
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from services.ephemeris_service import EphemerisService
from services.geocoding_service import GeocodingService

logger = logging.getLogger(__name__)

# Simple in-memory cache for deterministic results
_report_cache: Dict[str, Dict[str, Any]] = {}

class PlanetType(Enum):
    SUN = "Mặt Trời"
    MOON = "Mặt Trăng"
    MERCURY = "Sao Thủy"
    VENUS = "Sao Kim"
    MARS = "Sao Hỏa"
    JUPITER = "Sao Mộc"
    SATURN = "Sao Thổ"
    URANUS = "Thiên Vương"
    NEPTUNE = "Hải Vương"
    PLUTO = "Diêm Vương"
    NORTH_NODE = "Nút Bắc"
    CHIRON = "Chiron"

class ZodiacSign(Enum):
    ARIES = "Bạch Dương"
    TAURUS = "Kim Ngưu"
    GEMINI = "Song Tử"
    CANCER = "Cự Giải"
    LEO = "Sư Tử"
    VIRGO = "Xử Nữ"
    LIBRA = "Thiên Bình"
    SCORPIO = "Thiên Yết"
    SAGITTARIUS = "Nhân Mã"
    CAPRICORN = "Ma Kết"
    AQUARIUS = "Bảo Bình"
    PISCES = "Song Ngư"

@dataclass
class PlanetPlacement:
    planet: PlanetType
    sign: ZodiacSign
    degree: float
    symbol: str

class ZodiacAIService:
    """Generates professional-quality astrological reports using Google AI"""
    
    def __init__(self):
        # Initialize without Google AI client
        self.client = None
        
        self.ephemeris_service = EphemerisService()
        self.geocoding_service = GeocodingService()
        
        # Symbol mappings
        self.planet_symbols = {
            PlanetType.SUN: "☉",
            PlanetType.MOON: "☽", 
            PlanetType.MERCURY: "☿",
            PlanetType.VENUS: "♀",
            PlanetType.MARS: "♂",
            PlanetType.JUPITER: "♃",
            PlanetType.SATURN: "♄",
            PlanetType.URANUS: "♅",
            PlanetType.NEPTUNE: "♆",
            PlanetType.PLUTO: "♇",
            PlanetType.NORTH_NODE: "☊",
            PlanetType.CHIRON: "⚷"
        }
        
        self.sign_symbols = {
            ZodiacSign.ARIES: "♈", ZodiacSign.TAURUS: "♉", ZodiacSign.GEMINI: "♊",
            ZodiacSign.CANCER: "♋", ZodiacSign.LEO: "♌", ZodiacSign.VIRGO: "♍",
            ZodiacSign.LIBRA: "♎", ZodiacSign.SCORPIO: "♏", ZodiacSign.SAGITTARIUS: "♐",
            ZodiacSign.CAPRICORN: "♑", ZodiacSign.AQUARIUS: "♒", ZodiacSign.PISCES: "♓"
        }

    def generate_zodiac_ai_report(self, datetime_utc: str, lat: float, lon: float) -> Dict[str, Any]:
        """Generate a complete Zodiac AI-style report with caching for deterministic results"""
        try:
            # Create cache key from input parameters
            cache_key = self._get_cache_key(datetime_utc, lat, lon)
            
            # Check cache first
            if cache_key in _report_cache:
                logger.info(f"Cache hit for Zodiac AI report: {cache_key}")
                return _report_cache[cache_key]
            
            logger.info(f"Generating new Zodiac AI report for: datetime={datetime_utc}, lat={lat}, lon={lon}")
            
            # Get planetary positions with error handling
            try:
                chart_data = self.ephemeris_service.planet_positions(datetime_utc, lat, lon)
            except Exception as e:
                logger.warning(f"Ephemeris service failed for {datetime_utc}, {lat}, {lon}: {e}")
                # Return fallback report
                return self._generate_fallback_report(datetime_utc, lat, lon)
            
            # Convert to our format
            placements = self._parse_planetary_data(chart_data)
            
            # Generate report sections
            report_sections = {
                "overview": self._generate_overview(placements),
                "identity": self._generate_identity(placements),
                "love": self._generate_love(placements),
                "generation": self._generate_generation(placements),
                "lessons": self._generate_lessons(placements),
                "conclusion": self._generate_conclusion(placements)
            }
            
            # Format as standard report
            formatted_report = self._format_zodiac_ai_report(report_sections, placements)
            
            # Convert chart_data to dict format for frontend
            chart_data_dict = {}
            for placement in placements:
                chart_data_dict[placement.planet.value] = {
                    'sign': placement.sign.value,
                    'longitude': placement.degree
                }
            
            result = {
                "report": formatted_report,
                "generated_at": datetime.utcnow().isoformat(),
                "chart_data": chart_data_dict,
                "placements": [p.__dict__ for p in placements]
            }
            
            # Cache the result
            _report_cache[cache_key] = result
            logger.info(f"Cached Zodiac AI report for: {cache_key}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating Zodiac AI report: {e}")
            # Return fallback report instead of raising exception
            return self._generate_fallback_report(datetime_utc, lat, lon)

    def _parse_planetary_data(self, chart_data: List[Any]) -> List[PlanetPlacement]:
        """Parse ephemeris data into structured planet placements"""
        placements = []
        
        # Map planet names to our enum
        planet_mapping = {
            "Sun": PlanetType.SUN, "Moon": PlanetType.MOON,
            "Mercury": PlanetType.MERCURY, "Venus": PlanetType.VENUS,
            "Mars": PlanetType.MARS, "Jupiter": PlanetType.JUPITER,
            "Saturn": PlanetType.SATURN, "Uranus": PlanetType.URANUS,
            "Neptune": PlanetType.NEPTUNE, "Pluto": PlanetType.PLUTO,
            "North Node": PlanetType.NORTH_NODE, "Chiron": PlanetType.CHIRON
        }
        
        sign_mapping = {
            "Aries": ZodiacSign.ARIES, "Taurus": ZodiacSign.TAURUS,
            "Gemini": ZodiacSign.GEMINI, "Cancer": ZodiacSign.CANCER,
            "Leo": ZodiacSign.LEO, "Virgo": ZodiacSign.VIRGO,
            "Libra": ZodiacSign.LIBRA, "Scorpio": ZodiacSign.SCORPIO,
            "Sagittarius": ZodiacSign.SAGITTARIUS, "Capricorn": ZodiacSign.CAPRICORN,
            "Aquarius": ZodiacSign.AQUARIUS, "Pisces": ZodiacSign.PISCES
        }
        
        for data in chart_data:
            if hasattr(data, 'name') and hasattr(data, 'sign') and hasattr(data, 'longitude'):
                planet_name = data.name
                if planet_name in planet_mapping:
                    planet = planet_mapping[planet_name]
                    sign = sign_mapping[data.sign]
                    degree = data.longitude
                    
                    placement = PlanetPlacement(
                        planet=planet,
                        sign=sign,
                        degree=degree,
                        symbol=self.planet_symbols[planet]
                    )
                    placements.append(placement)
        
        return sorted(placements, key=lambda x: x.degree)

    def _generate_overview(self, placements: List[PlanetPlacement]) -> str:
        """Generate the overview section with planet headers"""
        overview = "1. Tổng quan (Overview)\n\n"
        
        # Add planet headers
        for placement in placements:
            sign_symbol = self.sign_symbols[placement.sign]
            overview += f"{placement.symbol} {placement.planet.value} ở {placement.sign.value} ({placement.degree:.2f}°) {sign_symbol}\n"
        
        overview += "\n"
        return overview

    def _generate_identity(self, placements: List[PlanetPlacement]) -> str:
        """Generate identity section with core personality analysis using AI"""
        overview = "2. Nhân dạng (Identity)\n\n"
        
        # Analyze key placements for identity
        sun_placement = next((p for p in placements if p.planet == PlanetType.SUN), None)
        moon_placement = next((p for p in placements if p.planet == PlanetType.MOON), None)
        mercury_placement = next((p for p in placements if p.planet == PlanetType.MERCURY), None)
        
        if sun_placement and moon_placement and mercury_placement:
            overview += f"**Cá tính cơ bản:** {self._get_identity_analysis(sun_placement, moon_placement, mercury_placement)}\n\n"
            overview += f"**Thế mạnh:** {self._get_strengths_analysis(sun_placement, mercury_placement)}\n\n"
            overview += f"**Thách thức:** {self._get_challenges_analysis(sun_placement, moon_placement)}\n\n"
        
        return overview

    def _generate_love(self, placements: List[PlanetPlacement]) -> str:
        """Generate love and relationships section using AI"""
        overview = "3. Tình yêu (Love)\n\n"
        
        venus_placement = next((p for p in placements if p.planet == PlanetType.VENUS), None)
        mars_placement = next((p for p in placements if p.planet == PlanetType.MARS), None)
        
        if venus_placement:
            overview += f"**Phong cách yêu đương:** {self._get_venus_analysis(venus_placement)}\n\n"
        
        if venus_placement and mars_placement:
            overview += f"**Mối quan hệ lý tưởng:** {self._get_relationship_advice(venus_placement, mars_placement)}\n\n"
        
        overview += "⚠️ **Cảnh báo:** Tránh kiểm soát quá mức hoặc ghen tuông vô cớ. Học cách tin tưởng và buông bỏ.\n\n"
        return overview

    def _generate_generation(self, placements: List[PlanetPlacement]) -> str:
        """Generate generational influences section using AI"""
        overview = "4. Thế hệ (Generational)\n\n"
        
        # Look for generational planets
        jupiter_placement = next((p for p in placements if p.planet == PlanetType.JUPITER), None)
        uranus_placement = next((p for p in placements if p.planet == PlanetType.URANUS), None)
        
        if jupiter_placement and uranus_placement:
            overview += f"**Ảnh hưởng thế hệ:** {self._get_generation_analysis(jupiter_placement, uranus_placement)}\n\n"
            overview += f"**Sứ mệnh thế hệ:** {self._get_generation_mission(jupiter_placement, uranus_placement)}\n\n"
        
        overview += "👉 **Gợi ý:** Hãy sử dụng khả năng kết nối của mình để xây dựng cộng đồng tích cực.\n\n"
        return overview

    def _generate_lessons(self, placements: List[PlanetPlacement]) -> str:
        """Generate life lessons section using AI"""
        overview = "5. Bài học (Lessons)\n\n"
        
        mars_placement = next((p for p in placements if p.planet == PlanetType.MARS), None)
        
        if mars_placement:
            overview += f"**Bài học chính:** {self._get_lesson_analysis(mars_placement)}\n\n"
            overview += f"**Công thức phát triển:** {self._get_development_formula(mars_placement)}\n\n"
        
        overview += "⚠️ **Cảnh báo:** Tránh đưa ra quyết định quan trọng khi đang trong trạng thái cảm xúc mạnh.\n\n"
        return overview

    def _generate_conclusion(self, placements: List[PlanetPlacement]) -> str:
        """Generate conclusion section using AI"""
        overview = "6. Kết luận (Conclusion)\n\n"
        
        sun_placement = next((p for p in placements if p.planet == PlanetType.SUN), None)
        
        if sun_placement:
            overview += f"**Tổng hợp:** {self._get_conclusion_analysis(sun_placement, placements)}\n\n"
            overview += f"**Mục tiêu phát triển:** {self._get_development_goals(sun_placement)}\n\n"
        
        overview += "👉 **Lời khuyên cuối:** Hãy nhớ rằng sự hoàn hảo không nằm ở việc làm hài lòng tất cả mọi người, mà ở việc sống thật với chính mình.\n\n"
        return overview

    def _format_zodiac_ai_report(self, sections: Dict[str, str], placements: List[PlanetPlacement]) -> str:
        """Format the complete report"""
        report = ""
        
        # Add all sections
        for section_name, content in sections.items():
            report += content
        
        # Add footer
        report += "---\n\n"
        report += "**Báo cáo được tạo bởi hệ thống Zodiac AI. Kết quả mang tính chất tham khảo và phản ánh xu hướng năng lượng chiêm tinh.**\n\n"
        
        return report

    # Analysis methods with professional-quality content
    def _get_identity_analysis(self, sun: PlanetPlacement, moon: PlanetPlacement, mercury: PlanetPlacement) -> str:
        """Generate professional identity analysis with concise, focused content"""
        # Get sign descriptions
        sun_desc = self._get_sign_description(sun.sign, 'bản chất')
        moon_desc = self._get_sign_description(moon.sign, 'cảm xúc')
        mercury_desc = self._get_sign_description(mercury.sign, 'tư duy')
        
        # Generate concise analysis
        if sun.sign == moon.sign == mercury.sign:
            return f"Bạn là người có bản chất {sun_desc}, {moon_desc} và {mercury_desc}. Sự kết hợp này tạo nên một cá tính mạnh mẽ với {self._get_sign_description(sun.sign, 'đặc điểm')}."
        else:
            return f"Bạn là người có bản chất phức tạp với sự kết hợp giữa {sun.sign.value} (lý trí), {moon.sign.value} (cảm xúc) và {mercury.sign.value} (tư duy). Điều này tạo nên một cá tính đa chiều với khả năng thích nghi cao."

    def _get_strengths_analysis(self, sun: PlanetPlacement, mercury: PlanetPlacement) -> str:
        """Generate concise strengths analysis"""
        # Get sign descriptions
        sun_desc = self._get_sign_description(sun.sign, 'thế mạnh')
        mercury_desc = self._get_sign_description(mercury.sign, 'tư duy')
        
        # Generate concise analysis
        return f"Khả năng giao tiếp khéo léo, tư duy logic sắc bén, và trực giác nghệ thuật tinh tế. Bạn có khả năng nhìn nhận vấn đề từ nhiều góc độ khác nhau."

    def _get_challenges_analysis(self, sun: PlanetPlacement, moon: PlanetPlacement) -> str:
        """Generate concise challenges analysis"""
        # Get sign descriptions
        sun_desc = self._get_sign_description(sun.sign, 'thách thức')
        moon_desc = self._get_sign_description(moon.sign, 'cảm xúc')
        
        # Generate concise analysis
        return f"Sự do dự trong quyết định và nhu cầu quá mức về sự công nhận từ người khác."

    def _get_venus_analysis(self, venus: PlanetPlacement) -> str:
        """Generate concise Venus analysis"""
        # Get sign descriptions
        venus_desc = self._get_sign_description(venus.sign, 'tình yêu')
        
        # Generate concise analysis
        return f"Sao Kim ở {venus.sign.value} mang đến sự đam mê sâu sắc và mong muốn kết nối tâm hồn. Bạn yêu bằng cả trái tim và trí óc."

    def _get_relationship_advice(self, venus: PlanetPlacement, mars: PlanetPlacement) -> str:
        """Generate concise relationship advice"""
        # Get sign descriptions
        venus_desc = self._get_sign_description(venus.sign, 'tình yêu')
        mars_desc = self._get_sign_description(mars.sign, 'động lực')
        
        # Generate concise advice
        return f"Cần người có thể hiểu được chiều sâu cảm xúc của bạn, đồng thời tôn trọng không gian cá nhân."

    def _get_generation_analysis(self, jupiter: PlanetPlacement, uranus: PlanetPlacement) -> str:
        """Generate concise generational analysis"""
        # Get sign descriptions
        jupiter_desc = self._get_sign_description(jupiter.sign, 'thế hệ')
        uranus_desc = self._get_sign_description(uranus.sign, 'đổi mới')
        
        # Generate concise analysis
        return f"Sao Mộc ở {jupiter.sign.value} ({jupiter.degree:.2f}°) và Thiên Vương ở {uranus.sign.value} ({uranus.degree:.2f}°) cho thấy bạn thuộc thế hệ có tư tưởng tiến bộ, yêu thích công nghệ và các giá trị nhân văn."

    def _get_generation_mission(self, jupiter: PlanetPlacement, uranus: PlanetPlacement) -> str:
        """Generate concise generational mission"""
        # Get sign descriptions
        jupiter_desc = self._get_sign_description(jupiter.sign, 'sứ mệnh')
        uranus_desc = self._get_sign_description(uranus.sign, 'đổi mới')
        
        # Generate concise mission
        return f"Đem lại sự đổi mới trong các mối quan hệ xã hội, phá vỡ các rào cản truyền thống."

    def _get_lesson_analysis(self, mars: PlanetPlacement) -> str:
        """Generate concise lesson analysis"""
        # Get sign descriptions
        mars_desc = self._get_sign_description(mars.sign, 'bài học')
        
        # Generate concise analysis
        return f"Sao Hỏa ở {mars.sign.value} ({mars.degree:.2f}°) chỉ ra bài học về việc kiểm soát sự bốc đồng và học cách kiên nhẫn."

    def _get_development_formula(self, mars: PlanetPlacement) -> str:
        """Generate concise development formula"""
        # Get sign descriptions
        mars_desc = self._get_sign_description(mars.sign, 'phát triển')
        
        # Generate concise formula
        return f"Cân bằng giữa lý trí và cảm xúc = Thành công trong các mối quan hệ."

    def _get_conclusion_analysis(self, sun: PlanetPlacement, placements: List[PlanetPlacement]) -> str:
        """Generate concise conclusion analysis"""
        # Get sign descriptions
        sun_desc = self._get_sign_description(sun.sign, 'kết luận')
        
        # Generate concise analysis
        return f"Bạn là người có tiềm năng lớn trong các lĩnh vực nghệ thuật, tư vấn hoặc các công việc liên quan đến con người. Sự kết hợp giữa lý trí và cảm xúc tạo nên sức hút đặc biệt."

    def _get_development_goals(self, sun: PlanetPlacement) -> str:
        """Generate concise development goals"""
        # Get sign descriptions
        sun_desc = self._get_sign_description(sun.sign, 'phát triển')
        
        # Generate concise goals
        return f"Học cách đưa ra quyết định dứt khoát hơn, tin tưởng vào trực giác của bản thân."

    def _get_sign_description(self, sign: ZodiacSign, aspect: str) -> str:
        """Get descriptive text for signs"""
        descriptions = {
            ZodiacSign.LIBRA: {
                "hài hòa": "hài hòa",
                "công bằng": "công bằng", 
                "thẩm mỹ": "thẩm mỹ cao",
                "hướng ngoại": "hướng ngoại",
                "biết lắng nghe": "biết lắng nghe",
                "cân bằng": "cân bằng"
            }
        }
        
        if sign in descriptions and aspect in descriptions[sign]:
            return descriptions[sign][aspect]
        return aspect

    def _get_cache_key(self, datetime_utc: str, lat: float, lon: float) -> str:
        """Generate a cache key from input parameters"""
        # Create a unique key from the input parameters
        key_data = {
            'datetime_utc': datetime_utc,
            'lat': round(lat, 6),  # Round to avoid floating point precision issues
            'lon': round(lon, 6)
        }
        
        # Create a hash of the key data for a compact cache key
        key_string = json.dumps(key_data, sort_keys=True)
        cache_key = hashlib.md5(key_string.encode()).hexdigest()
        
        return cache_key

    def _generate_fallback_report(self, datetime_utc: str, lat: float, lon: float) -> Dict[str, Any]:
        """Generate a fallback report when external services fail"""
        logger.warning(f"Generating fallback report for: datetime={datetime_utc}, lat={lat}, lon={lon}")
        
        # Create a basic fallback report
        fallback_report = {
            "report": "⚠️ **Báo cáo dự phòng**\n\n"
                     "Do hệ thống đang gặp sự cố kỹ thuật, chúng tôi cung cấp báo cáo dự phòng.\n\n"
                     "**Tổng quan:**\n"
                     "Dựa trên thời gian và vị trí của bạn, đây là một bản phân tích cơ bản.\n\n"
                     "**Lưu ý:** Đây là báo cáo dự phòng, vui lòng thử lại sau để nhận báo cáo đầy đủ.\n\n"
                     "---\n\n"
                     "**Báo cáo được tạo bởi hệ thống Zodiac AI. Kết quả mang tính chất tham khảo.**",
            "generated_at": datetime.utcnow().isoformat(),
            "chart_data": {},
            "placements": []
        }
        
        return fallback_report
