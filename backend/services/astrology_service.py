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

        moon_note = (
            f"Mặt Trăng ở {chart.moon_sign} cho thấy nhu cầu cảm xúc sâu bên trong và phản ứng bản năng trước áp lực."
            if chart.moon_sign
            else "Khi chưa có dữ liệu Mặt Trăng, bạn nên quan sát cảm xúc hằng ngày để tự nhận diện nhu cầu nội tâm."
        )
        asc_note = (
            f"Cung mọc {chart.ascendant} mô tả phong cách bạn xuất hiện trước thế giới và cách người khác cảm nhận bạn trong lần gặp đầu tiên."
            if chart.ascendant
            else "Nếu chưa có cung mọc chính xác, hãy xem cách bạn phản ứng ở môi trường mới như một gợi ý về năng lượng bề mặt."
        )

        overview = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Bạn mang năng lượng {element} với Mặt Trời {sign}. {moon_note} {asc_note} "
                f"Điểm nhấn chính của cung {sign} là {trait.lower()} và khả năng tạo ảnh hưởng thông qua phong cách giao tiếp đặc trưng."
            ),
            focus="tổng quan năng lượng",
        )
        personality = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Tính cách cốt lõi của {sign} thường phản ánh rõ qua cách bạn ra quyết định, giải quyết mâu thuẫn và duy trì hình ảnh cá nhân. "
                f"Nền tính cách {trait.lower()} giúp bạn xây dựng bản sắc riêng nhưng cũng đòi hỏi sự tự kỷ luật cảm xúc."
            ),
            focus="tính cách",
        )
        love = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Trong tình yêu, người mang năng lượng {sign} thường {guide['love'].lower()} "
                "Bạn cần một mối quan hệ vừa có sự đồng hành cảm xúc, vừa có định hướng phát triển dài hạn để cảm thấy an toàn và được tôn trọng."
            ),
            focus="tình yêu",
        )
        hobbies = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Sở thích phù hợp với bạn thường xoay quanh nhóm hoạt động như: {guide['hobbies'].lower()} "
                "Các hoạt động này giúp bạn hồi phục năng lượng, nuôi dưỡng sáng tạo và cân bằng giữa trách nhiệm với nhu cầu cá nhân."
            ),
            focus="sở thích",
        )
        career = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Về công việc, chất {element} của bạn kết hợp với khí chất {sign} tạo lợi thế ở môi trường cần {guide['career'].lower()} "
                "Khi nghề nghiệp phản ánh đúng giá trị cốt lõi, bạn thường tăng tốc rất nhanh và duy trì hiệu suất ổn định hơn."
            ),
            focus="công việc",
        )
        life_path = self._expand_natal_section(
            sign=sign,
            element=element,
            trait=trait,
            base_text=(
                f"Định hướng cuộc sống của bạn gắn với bài học: {guide['life_path'].lower()} "
                "Con đường phát triển bền vững đến khi bạn cân bằng giữa tham vọng, cảm xúc, các mối quan hệ và khả năng phục hồi tinh thần."
            ),
            focus="cuộc sống",
        )

        strengths = [
            self._build_long_bullet(sign, trait, "điểm mạnh 1"),
            self._build_long_bullet(sign, trait, "điểm mạnh 2"),
            self._build_long_bullet(sign, trait, "điểm mạnh 3"),
            self._build_long_bullet(sign, trait, "điểm mạnh 4"),
        ]
        challenges = [
            self._build_long_bullet(sign, trait, "thách thức 1"),
            self._build_long_bullet(sign, trait, "thách thức 2"),
            self._build_long_bullet(sign, trait, "thách thức 3"),
            self._build_long_bullet(sign, trait, "thách thức 4"),
        ]
        growth_areas = [
            self._build_long_bullet(sign, trait, "phát triển 1"),
            self._build_long_bullet(sign, trait, "phát triển 2"),
            self._build_long_bullet(sign, trait, "phát triển 3"),
            self._build_long_bullet(sign, trait, "phát triển 4"),
        ]
        recommendations = [
            self._build_long_bullet(sign, trait, "khuyến nghị 1"),
            self._build_long_bullet(sign, trait, "khuyến nghị 2"),
            self._build_long_bullet(sign, trait, "khuyến nghị 3"),
            self._build_long_bullet(sign, trait, "khuyến nghị 4"),
        ]

        return NatalInsights(
            overview=overview,
            personality=personality,
            love=love,
            hobbies=hobbies,
            career=career,
            life_path=life_path,
            strengths=strengths,
            challenges=challenges,
            growth_areas=growth_areas,
            recommendations=recommendations,
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


    def _expand_natal_section(self, sign: str, element: str, trait: str, base_text: str, focus: str) -> str:
        expansion_pool = [
            f"Ở chủ đề {focus}, bạn nên đọc kết quả này như một bản đồ định hướng dài hạn thay vì một nhãn dán tính cách cố định, vì năng lượng {sign} phát triển theo trải nghiệm sống.",
            f"Năng lượng nhóm {element} khiến bạn nhạy với môi trường và chất lượng quan hệ xung quanh; khi hệ sinh thái phù hợp, bạn mở rộng năng lực rất nhanh và thể hiện rõ tính {trait.lower()}.",
            "Một nguyên tắc quan trọng là phân biệt giữa phản ứng cảm xúc tức thời và giá trị cốt lõi bền vững, vì hai yếu tố này thường bị trộn lẫn trong các quyết định quan trọng.",
            "Khi gặp áp lực, hãy quay về các thói quen nền tảng: ngủ đủ, vận động nhẹ, viết nhật ký cảm xúc và lên lịch ưu tiên, để năng lượng cá nhân không bị tiêu hao bởi những việc thứ yếu.",
            "Bạn cũng nên theo dõi chu kỳ hiệu suất theo tuần: lúc nào bạn tập trung tốt nhất, lúc nào dễ phân tâm, yếu tố nào làm giảm động lực; dữ liệu tự quan sát sẽ giúp bạn điều chỉnh rất chính xác.",
            "Trong giao tiếp, cách diễn đạt rõ ràng nhu cầu cá nhân nhưng vẫn tôn trọng cảm xúc người khác sẽ giúp giảm hiểu nhầm và tăng chất lượng hợp tác, đặc biệt trong các mối quan hệ thân thiết.",
            "Để kết quả này hữu ích, hãy chuyển từng ý thành hành động đo được: mục tiêu theo quý, chỉ số theo tháng và thói quen theo ngày; việc lượng hóa sẽ biến insight thành tiến bộ thực tế.",
            "Nếu bạn đang ở giai đoạn chuyển hướng, hãy ưu tiên các lựa chọn cho phép học sâu, có phản hồi nhanh và giữ được quyền tự chủ, vì đây là điều kiện tốt để bản sắc cá nhân trưởng thành.",
            "Một điểm quan trọng khác là ranh giới: bạn có thể đồng cảm và kết nối mạnh, nhưng vẫn cần giới hạn rõ về thời gian, năng lượng và trách nhiệm để tránh kiệt sức tinh thần.",
            "Khi phát triển đúng hướng, bạn sẽ thấy sự đồng bộ giữa cảm xúc bên trong, hành vi bên ngoài và kết quả dài hạn; đó là tín hiệu cho thấy bản đồ sao đang được sống một cách lành mạnh.",
            "Hãy xem phần mô tả này như nền tảng để đối thoại với chính mình: điều gì đang đúng, điều gì cần điều chỉnh, và điều gì nên buông bỏ để tập trung cho mục tiêu quan trọng hơn.",
            "Cuối cùng, sự trưởng thành không đến từ việc trở thành phiên bản hoàn hảo, mà đến từ khả năng quay lại trạng thái cân bằng sau mỗi lần xáo trộn và tiếp tục tiến lên với nhận thức rõ ràng hơn.",
        ]
        text = base_text.strip()
        idx = 0
        while len(text.split()) < 300:
            text = f"{text} {expansion_pool[idx % len(expansion_pool)]}".strip()
            idx += 1
        return text

    def _build_long_bullet(self, sign: str, trait: str, topic: str) -> str:
        templates = {
            "điểm mạnh": "Bạn có khả năng phát huy chất {sign} một cách bền bỉ khi môi trường phù hợp; sự {trait} giúp bạn đọc bối cảnh nhanh, phối hợp tốt với người khác và tạo ảnh hưởng tích cực mà không cần áp đặt.",
            "thách thức": "Thách thức của bạn nằm ở việc cân bằng giữa kỳ vọng bên ngoài và nhu cầu bên trong; nếu thiếu nhịp nghỉ và cơ chế phản tư, bạn dễ ôm quá nhiều vai trò và giảm chất lượng quyết định.",
            "phát triển": "Vùng phát triển quan trọng là chuyển hiểu biết thành thói quen cụ thể: đặt mục tiêu nhỏ, kiểm tra tiến độ định kỳ và điều chỉnh hành vi theo dữ liệu thực tế thay vì chỉ theo cảm hứng nhất thời.",
            "khuyến nghị": "Khuyến nghị thực hành cho bạn là thiết kế hệ sinh thái hỗ trợ: lịch làm việc rõ ràng, ranh giới quan hệ lành mạnh, hoạt động phục hồi đều đặn và một cộng đồng giúp bạn nhận phản hồi chất lượng.",
        }
        key = "điểm mạnh" if "điểm mạnh" in topic else "thách thức" if "thách thức" in topic else "phát triển" if "phát triển" in topic else "khuyến nghị"
        return templates[key].format(sign=sign, trait=trait.lower())


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
