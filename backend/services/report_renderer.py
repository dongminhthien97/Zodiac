from __future__ import annotations
from typing import Dict

SIGN_VN = {
    'Aries': 'Bạch Dương', 'Taurus': 'Kim Ngưu', 'Gemini': 'Song Tử', 'Cancer': 'Cự Giải',
    'Leo': 'Sư Tử', 'Virgo': 'Xử Nữ', 'Libra': 'Thiên Bình', 'Scorpio': 'Hổ Cáp',
    'Sagittarius': 'Nhân Mã', 'Capricorn': 'Ma Kết', 'Aquarius': 'Bảo Bình', 'Pisces': 'Song Ngư'
}

SIGN_TRAITS = {
    'Aries': 'Lửa|Hành động, độc lập, can đảm, thẳng thắn, thích lãnh đạo',
    'Taurus': 'Đất|Ổn định, kiên nhẫn, thực tế, tận hưởng vật chất, trung thành',
    'Gemini': 'Khí|Tò mò, linh hoạt, giao tiếp tốt, đa năng, thích học hỏi',
    'Cancer': 'Nước|Nhạy cảm, nuôi dưỡng, trực giác mạnh, bảo vệ gia đình, cảm xúc sâu sắc',
    'Leo': 'Lửa|Tự tin, sáng tạo, hào phóng, thích được công nhận, ấm áp',
    'Virgo': 'Đất|Tỉ mỉ, phân tích, thực dụng, cầu toàn, thích giúp đỡ',
    'Libra': 'Khí|Hòa nhã, công bằng, thẩm mỹ, xã giao, tránh xung đột',
    'Scorpio': 'Nước|Sâu sắc, quyết tâm, đam mê, bí ẩn, thích kiểm soát',
    'Sagittarius': 'Lửa|Tự do, lạc quan, phiêu lưu, trung thực, thích khám phá',
    'Capricorn': 'Đất|Kiên trì, có trách nhiệm, tham vọng, kỷ luật, thực tế',
    'Aquarius': 'Khí|Độc lập, sáng tạo, nhân đạo, khác biệt, tư tưởng tiến bộ',
    'Pisces': 'Nước|Nhạy cảm, mơ mộng, trực giác, đồng cảm, nghệ sĩ'
}

def _fmt_degree(longitude: float) -> str:
    deg = (longitude % 360.0) % 30.0
    return f"{deg:.2f}°"

def _get_sign_traits(sign: str) -> tuple[str, str]:
    """Get element and traits for a sign"""
    if sign in SIGN_TRAITS:
        element, traits = SIGN_TRAITS[sign].split('|', 1)
        return element, traits
    return "Unknown", "Không xác định"

def _get_sun_insights(sign: str) -> list[str]:
    """Get specific insights for Sun sign"""
    insights = {
        'Aries': [
            "Bạn có năng lượng lãnh đạo bẩm sinh và thích khởi xướng các dự án mới",
            "Sự tự tin và can đảm giúp bạn vượt qua thử thách một cách nhanh chóng",
            "Bạn cần học cách kiên nhẫn và lắng nghe người khác trước khi hành động"
        ],
        'Taurus': [
            "Bạn đánh giá cao sự ổn định và an toàn trong mọi khía cạnh cuộc sống",
            "Sự kiên nhẫn và bền bỉ giúp bạn đạt được mục tiêu dài hạn",
            "Bạn cần học cách linh hoạt hơn khi môi trường thay đổi"
        ],
        'Gemini': [
            "Trí tò mò và khả năng giao tiếp giúp bạn kết nối với nhiều người",
            "Bạn thích học hỏi và tiếp thu kiến thức mới một cách nhanh chóng",
            "Bạn cần học cách tập trung sâu hơn thay vì lan man nhiều chủ đề"
        ],
        'Cancer': [
            "Trực giác mạnh mẽ giúp bạn hiểu được cảm xúc của người khác",
            "Bạn có khả năng chăm sóc và nuôi dưỡng những người xung quanh",
            "Bạn cần học cách thiết lập ranh giới cảm xúc để tránh bị quá tải"
        ],
        'Leo': [
            "Sự tự tin và ấm áp giúp bạn trở thành trung tâm của mọi nhóm",
            "Khả năng sáng tạo và biểu đạt bản thân rất mạnh mẽ",
            "Bạn cần học cách chia sẻ ánh đèn sân khấu với người khác"
        ],
        'Virgo': [
            "Khả năng phân tích và chú ý đến chi tiết giúp bạn hoàn thành công việc xuất sắc",
            "Bạn có xu hướng hoàn hảo và luôn muốn cải thiện bản thân",
            "Bạn cần học cách buông bỏ tiêu chuẩn quá cao với bản thân và người khác"
        ],
        'Libra': [
            "Bạn có khiếu thẩm mỹ và khả năng tạo sự hòa hợp trong các mối quan hệ",
            "Sự công bằng và khéo léo giúp bạn giải quyết xung đột hiệu quả",
            "Bạn cần học cách ra quyết định dứt khoát thay vì do dự quá lâu"
        ],
        'Scorpio': [
            "Sự quyết tâm và đam mê giúp bạn đạt được những mục tiêu sâu sắc",
            "Khả năng nhìn thấu bản chất vấn đề rất mạnh mẽ",
            "Bạn cần học cách tin tưởng và buông bỏ nhu cầu kiểm soát quá mức"
        ],
        'Sagittarius': [
            "Tinh thần phiêu lưu và khát khao khám phá giúp bạn mở rộng tầm nhìn",
            "Sự lạc quan và trung thực giúp bạn truyền cảm hứng cho người khác",
            "Bạn cần học cách kiên nhẫn với những cam kết dài hạn"
        ],
        'Capricorn': [
            "Sự kỷ luật và tham vọng giúp bạn xây dựng nền tảng vững chắc",
            "Khả năng quản lý và tổ chức rất xuất sắc",
            "Bạn cần học cách thư giãn và tận hưởng thành quả đã đạt được"
        ],
        'Aquarius': [
            "Tư tưởng tiến bộ và sự độc lập giúp bạn mang lại những ý tưởng đổi mới",
            "Khả năng nhìn xa trông rộng và tư duy logic mạnh mẽ",
            "Bạn cần học cách kết nối cảm xúc sâu hơn với người khác"
        ],
        'Pisces': [
            "Trực giác nhạy bén và sự đồng cảm giúp bạn hiểu được thế giới nội tâm",
            "Khả năng sáng tạo nghệ thuật và tưởng tượng phong phú",
            "Bạn cần học cách thiết lập ranh giới rõ ràng để bảo vệ năng lượng"
        ]
    }
    return insights.get(sign, ["Không có thông tin chi tiết cho cung này"])

def _get_moon_insights(sign: str) -> list[str]:
    """Get specific insights for Moon sign"""
    insights = {
        'Aries': [
            "Bạn phản ứng nhanh chóng và trực tiếp với các tình huống cảm xúc",
            "Cần không gian cá nhân để xử lý cảm xúc một cách độc lập"
        ],
        'Taurus': [
            "Bạn cần sự ổn định và an toàn cảm xúc để cảm thấy bình yên",
            "Thích những thói quen và môi trường quen thuộc để thư giãn"
        ],
        'Gemini': [
            "Bạn xử lý cảm xúc thông qua giao tiếp và chia sẻ suy nghĩ",
            "Cần sự đa dạng trong các hoạt động để tránh nhàm chán cảm xúc"
        ],
        'Cancer': [
            "Bạn có trực giác mạnh mẽ và dễ dàng cảm nhận được bầu không khí xung quanh",
            "Cần cảm giác được yêu thương và chăm sóc để cảm thấy an toàn"
        ],
        'Leo': [
            "Bạn cần được công nhận và trân trọng để cảm thấy tự tin về cảm xúc",
            "Thích thể hiện cảm xúc một cách hào phóng và ấm áp"
        ],
        'Virgo': [
            "Bạn xử lý cảm xúc thông qua việc phân tích và tìm giải pháp",
            "Cần sự hoàn hảo và trật tự để cảm thấy bình yên nội tâm"
        ],
        'Libra': [
            "Bạn cần sự hòa hợp và cân bằng trong các mối quan hệ cảm xúc",
            "Dễ bị ảnh hưởng bởi cảm xúc của người khác"
        ],
        'Scorpio': [
            "Bạn có cảm xúc sâu sắc và mãnh liệt, thường giấu kín bên trong",
            "Cần sự tin tưởng tuyệt đối để mở lòng hoàn toàn"
        ],
        'Sagittarius': [
            "Bạn cần tự do cảm xúc và không thích bị gò bó trong các quy tắc",
            "Thích tìm kiếm ý nghĩa sâu sắc thông qua trải nghiệm mới"
        ],
        'Capricorn': [
            "Bạn có xu hướng kìm nén cảm xúc và thể hiện sự kiềm chế",
            "Cần cảm giác kiểm soát và thành tựu để cảm thấy an tâm"
        ],
        'Aquarius': [
            "Bạn có cảm xúc độc lập và không theo quy chuẩn thông thường",
            "Thích kết nối với những người có tư tưởng tiến bộ giống mình"
        ],
        'Pisces': [
            "Bạn có trực giác nhạy bén và dễ dàng đồng cảm với người khác",
            "Cần không gian nghệ thuật và thiền định để cân bằng cảm xúc"
        ]
    }
    return insights.get(sign, ["Không có thông tin chi tiết cho cung này"])

def _get_mercury_insights(sign: str) -> list[str]:
    """Get specific insights for Mercury sign"""
    insights = {
        'Aries': [
            "Bạn suy nghĩ nhanh chóng và đưa ra quyết định một cách trực tiếp",
            "Thích tranh luận và thể hiện quan điểm cá nhân một cách mạnh mẽ"
        ],
        'Taurus': [
            "Bạn suy nghĩ chậm rãi và có hệ thống, thích sự chắc chắn",
            "Có khả năng trình bày ý tưởng một cách rõ ràng và thực tế"
        ],
        'Gemini': [
            "Bạn có tư duy linh hoạt và khả năng giao tiếp xuất sắc",
            "Thích học hỏi và chia sẻ kiến thức với người khác"
        ],
        'Cancer': [
            "Bạn suy nghĩ dựa trên cảm xúc và trực giác",
            "Thích giao tiếp qua những câu chuyện cảm xúc và cá nhân"
        ],
        'Leo': [
            "Bạn có khả năng diễn đạt tốt và thích được lắng nghe",
            "Thích chia sẻ ý tưởng một cách hào phóng và sáng tạo"
        ],
        'Virgo': [
            "Bạn có tư duy phân tích và chú ý đến chi tiết nhỏ",
            "Thích tổ chức thông tin một cách logic và hệ thống"
        ],
        'Libra': [
            "Bạn có khả năng nhìn nhận vấn đề từ nhiều góc độ khác nhau",
            "Thích giao tiếp hòa nhã và tìm kiếm sự đồng thuận"
        ],
        'Scorpio': [
            "Bạn có tư duy sâu sắc và thích đào sâu vào bản chất vấn đề",
            "Có khả năng nhìn thấu động cơ và ý định thực sự"
        ],
        'Sagittarius': [
            "Bạn có tư duy rộng mở và thích khám phá những chân trời mới",
            "Thích chia sẻ quan điểm một cách trung thực và lạc quan"
        ],
        'Capricorn': [
            "Bạn có tư duy thực tế và có tổ chức, thích lập kế hoạch dài hạn",
            "Thích giao tiếp qua những ý tưởng có tính xây dựng"
        ],
        'Aquarius': [
            "Bạn có tư duy độc lập và thích những ý tưởng tiến bộ, khác biệt",
            "Thích giao tiếp qua những chủ đề về tương lai và đổi mới"
        ],
        'Pisces': [
            "Bạn có tư duy trực giác và sáng tạo, thích tưởng tượng phong phú",
            "Thích giao tiếp qua nghệ thuật và những câu chuyện cảm xúc"
        ]
    }
    return insights.get(sign, ["Không có thông tin chi tiết cho cung này"])

def _get_venus_insights(sign: str) -> list[str]:
    """Get specific insights for Venus sign"""
    insights = {
        'Aries': [
            "Bạn yêu một cách chủ động và thẳng thắn, thích sự mới mẻ",
            "Cần đối tác có thể theo kịp năng lượng và đam mê của bạn"
        ],
        'Taurus': [
            "Bạn yêu một cách chậm rãi và bền bỉ, coi trọng sự ổn định",
            "Thích những biểu hiện tình cảm qua hành động thiết thực"
        ],
        'Gemini': [
            "Bạn yêu qua giao tiếp và chia sẻ ý tưởng, thích sự đa dạng",
            "Cần đối tác có thể kích thích trí tò mò và tư duy của bạn"
        ],
        'Cancer': [
            "Bạn yêu một cách nuôi dưỡng và bảo vệ, coi trọng cảm xúc sâu sắc",
            "Cần cảm giác an toàn và được chăm sóc trong mối quan hệ"
        ],
        'Leo': [
            "Bạn yêu một cách hào phóng và ấm áp, thích được công nhận",
            "Cần đối tác có thể trân trọng và ngưỡng mộ bạn"
        ],
        'Virgo': [
            "Bạn yêu qua việc chăm sóc và giúp đỡ, thích sự hoàn hảo",
            "Cần đối tác có thể đánh giá cao sự quan tâm đến chi tiết của bạn"
        ],
        'Libra': [
            "Bạn yêu một cách hòa nhã và công bằng, thích sự cân bằng",
            "Cần đối tác có thể chia sẻ thẩm mỹ và gu品味 của bạn"
        ],
        'Scorpio': [
            "Bạn yêu một cách sâu sắc và đam mê, cần sự tin tưởng tuyệt đối",
            "Thích sự kết nối cảm xúc mạnh mẽ và biến đổi sâu sắc"
        ],
        'Sagittarius': [
            "Bạn yêu một cách tự do và lạc quan, thích sự phiêu lưu",
            "Cần đối tác có thể cùng bạn khám phá thế giới và triết lý sống"
        ],
        'Capricorn': [
            "Bạn yêu một cách chín chắn và có trách nhiệm, coi trọng cam kết",
            "Thích đối tác có cùng mục tiêu và tham vọng trong cuộc sống"
        ],
        'Aquarius': [
            "Bạn yêu một cách độc lập và tiến bộ, thích sự khác biệt",
            "Cần đối tác có thể tôn trọng không gian cá nhân và tư tưởng độc lập"
        ],
        'Pisces': [
            "Bạn yêu một cách nhạy cảm và mơ mộng, thích sự đồng cảm sâu sắc",
            "Cần đối tác có thể hiểu được thế giới nội tâm phong phú của bạn"
        ]
    }
    return insights.get(sign, ["Không có thông tin chi tiết cho cung này"])

def _get_mars_insights(sign: str) -> list[str]:
    """Get specific insights for Mars sign"""
    insights = {
        'Aries': [
            "Bạn hành động nhanh chóng và quyết đoán, thích dẫn đầu",
            "Có năng lượng chiến đấu mạnh mẽ và không ngại thách thức"
        ],
        'Taurus': [
            "Bạn hành động chậm rãi nhưng kiên định, có sức bền cao",
            "Thích làm việc có hệ thống và không dễ bị lay chuyển"
        ],
        'Gemini': [
            "Bạn hành động linh hoạt và đa nhiệm, thích sự đa dạng",
            "Có khả năng thích ứng nhanh với các tình huống khác nhau"
        ],
        'Cancer': [
            "Bạn hành động dựa trên cảm xúc và trực giác, thích bảo vệ người thân",
            "Có năng lượng nuôi dưỡng và chăm sóc mạnh mẽ"
        ],
        'Leo': [
            "Bạn hành động hào phóng và tự tin, thích được công nhận",
            "Có năng lượng lãnh đạo và khả năng truyền cảm hứng"
        ],
        'Virgo': [
            "Bạn hành động cẩn thận và có tổ chức, chú ý đến chi tiết",
            "Có năng lượng phục vụ và thích giúp đỡ người khác"
        ],
        'Libra': [
            "Bạn hành động hòa nhã và công bằng, thích hợp tác",
            "Có năng lượng ngoại giao và khả năng đàm phán tốt"
        ],
        'Scorpio': [
            "Bạn hành động quyết liệt và có sức mạnh nội tâm mạnh mẽ",
            "Có khả năng biến đổi và tái sinh sau những thử thách"
        ],
        'Sagittarius': [
            "Bạn hành động tự do và lạc quan, thích khám phá",
            "Có năng lượng phiêu lưu và khát khao học hỏi"
        ],
        'Capricorn': [
            "Bạn hành động có kỷ luật và kiên trì, thích xây dựng nền tảng",
            "Có năng lượng quản lý và khả năng chịu trách nhiệm cao"
        ],
        'Aquarius': [
            "Bạn hành động độc lập và sáng tạo, thích đổi mới",
            "Có năng lượng nhân đạo và tư tưởng tiến bộ"
        ],
        'Pisces': [
            "Bạn hành động nhạy cảm và trực giác, thích giúp đỡ người khác",
            "Có năng lượng nghệ thuật và khả năng đồng cảm mạnh mẽ"
        ]
    }
    return insights.get(sign, ["Không có thông tin chi tiết cho cung này"])

def render_personal_report(astrology_data: Dict) -> str:
    """Render the personal report in the exact requested structure (Vietnamese).

    Input: astrology_data dictionary with keys like 'sun','moon','mercury', etc.
    Output: multi-line string formatted per user's template.
    """
    ad = astrology_data

    def sign_name(k):
        s = ad.get(k, {}).get('sign')
        return s if s else 'Unknown'

    def deg(k):
        v = ad.get(k, {}).get('longitude')
        return _fmt_degree(v) if v is not None else 'Unknown'

    # Helper counts for big picture
    ELEMENT_MAP = {
        'Aries':'Fire','Leo':'Fire','Sagittarius':'Fire',
        'Gemini':'Air','Libra':'Air','Aquarius':'Air',
        'Taurus':'Earth','Virgo':'Earth','Capricorn':'Earth',
        'Cancer':'Water','Scorpio':'Water','Pisces':'Water'
    }
    counts = {'Fire':0,'Air':0,'Earth':0,'Water':0}
    for body in ['sun','moon','mercury','venus','mars','jupiter','uranus','neptune','pluto','north_node','chiron']:
        s = ad.get(body, {}).get('sign')
        if s and s in ELEMENT_MAP:
            counts[ELEMENT_MAP[s]] += 1

    dominant = max(counts, key=counts.get)

    lines = []
    # 1. Tổng quan nhanh
    lines.append('1. Tổng quan nhanh (Big Picture)')
    lines.append('')
    # Stellium detection: 3+ in same sign among personal planets
    personal = ['sun','moon','mercury','venus','mars']
    sign_freq = {}
    for p in personal:
        s = ad.get(p, {}).get('sign')
        if s:
            sign_freq[s] = sign_freq.get(s,0)+1
    stellium = None
    for s,c in sign_freq.items():
        if c >= 3:
            stellium = s
            break
    if stellium:
        lines.append(f"- Cụm / trọng tâm nổi bật: Stellium ở {stellium} ({', '.join([p for p in personal if ad.get(p,{}).get('sign')==stellium])}) — tập trung vào các chủ đề liên quan đến cung này.")
    else:
        lines.append(f"- Cụm / trọng tâm nổi bật: Không thấy stellium rõ rệt; các hành tinh phân bổ theo nhiều cung.")

    # Main axis guess: if Libra present vs Aries
    axis = 'Libra ↔ Aries' if ('Libra' in sign_freq or 'Aries' in sign_freq) else 'Unknown'
    lines.append(f"- Trục chiêm tinh chính: {axis} — cân bằng giữa mối quan hệ và khẳng định cá nhân.")
    lines.append(f"- Phân bố nguyên tố: Khí / Lửa / Đất / Nước → {counts['Air']}/{counts['Fire']}/{counts['Earth']}/{counts['Water']}. (Trội: {dominant})")
    lines.append('- Điểm thiếu / điểm cần học: Thiếu các nguyên tố thấp hơn nếu số đếm nhỏ; chú trọng phát triển thực hành và chiều sâu cảm xúc.')
    lines.append('👉 Kết luận: Người thiên về giao tiếp và kết nối; thách thức là chuyển tư duy thành hành động cụ thể.')
    lines.append('')

    # 2. Nhân dạng cốt lõi
    lines.append('2. Nhân dạng cốt lõi')
    lines.append('')
    # Sun
    sun_sign = sign_name('sun')
    lines.append(f"☉ Mặt Trời {sun_sign} ({deg('sun')})")
    lines.append('Bản ngã – con người muốn trở thành')
    sun_insights = _get_sun_insights(sun_sign)
    for insight in sun_insights:
        lines.append(f"- {insight}")
    lines.append('⚠️ Mặt hạn chế:')
    lines.append('- Trì hoãn quyết định;')
    lines.append('- Phụ thuộc phản hồi xã hội;')
    lines.append('')
    # Moon
    moon_sign = sign_name('moon')
    lines.append(f"☽ Mặt Trăng {moon_sign} ({deg('moon')})")
    lines.append('Cảm xúc – nhu cầu tinh thần')
    moon_insights = _get_moon_insights(moon_sign)
    for insight in moon_insights:
        lines.append(f"- {insight}")
    lines.append('⚠️ Khi mất cân bằng:')
    lines.append('- Kìm nén cảm xúc;')
    lines.append('- Tìm kiếm chấp thuận bên ngoài;')
    lines.append('')
    # Mercury
    mercury_sign = sign_name('mercury')
    lines.append(f"☿ Sao Thủy {mercury_sign} ({deg('mercury')})")
    lines.append('Tư duy – giao tiếp')
    mercury_insights = _get_mercury_insights(mercury_sign)
    for insight in mercury_insights:
        lines.append(f"- {insight}")
    lines.append('⚠️ Điểm yếu:')
    lines.append('- Quyết định chậm;')
    lines.append('- Né tránh luận điểm gây tranh cãi;')
    lines.append('')

    # 3. Tình yêu – ham muốn – động lực
    lines.append('3. Tình yêu – ham muốn – động lực')
    lines.append('')
    venus_sign = sign_name('venus')
    lines.append(f"♀ Sao Kim {venus_sign} ({deg('venus')})")
    lines.append('Cách yêu & giá trị tình cảm')
    venus_insights = _get_venus_insights(venus_sign)
    for insight in venus_insights:
        lines.append(f"- {insight}")
    lines.append('⚠️ Mặt bóng:')
    lines.append('- Rủi ro cảm xúc khi thiếu an toàn;')
    lines.append('- Xu hướng kiểm soát hoặc nghi ngờ;')
    lines.append('👉 1 câu đối lập nội tâm: Bề ngoài tìm hòa hợp nhưng bên trong khao khát chiều sâu.')
    lines.append('')
    mars_sign = sign_name('mars')
    lines.append(f"♂ Sao Hỏa {mars_sign} ({deg('mars')})")
    lines.append('Hành động – động lực')
    mars_insights = _get_mars_insights(mars_sign)
    for insight in mars_insights:
        lines.append(f"- {insight}")
    lines.append('⚠️ Nhược điểm:')
    lines.append('- Thiếu kiên nhẫn với chi tiết;')
    lines.append('- Hành vi bộc phát khi stress;')
    lines.append('')

    # 4. Thế hệ – xã hội – tầm nhìn
    lines.append('4. Thế hệ – xã hội – tầm nhìn')
    lines.append('')
    for b in ['jupiter','uranus','neptune','pluto']:
        sign = sign_name(b)
        element, traits = _get_sign_traits(sign)
        lines.append(f"{b.capitalize()} {sign} ({deg(b)})")
        lines.append(f"- {element}: {traits}")
        lines.append('')

    # 5. Bài học linh hồn
    lines.append('5. Bài học linh hồn')
    lines.append('')
    north_node_sign = sign_name('north_node')
    if north_node_sign != 'Unknown':
        lines.append(f"☊ Nút Bắc {north_node_sign} ({deg('north_node')})")
        lines.append('Hướng phát triển của kiếp này')
        lines.append('- Học cách tổ chức và chú ý chi tiết.')
        lines.append('- Ưu tiên sức khỏe và quản trị đời sống.')
        lines.append('- Biến ý tưởng thành hành động cụ thể.')
        lines.append('Rời xa xu hướng:')
        lines.append('- Trì hoãn bằng ngoại giao bề ngoài;')
        lines.append('- Né tránh trách nhiệm chi tiết;')
        lines.append('👉 1 câu công thức thành công (A → B): Kết nối xã hội → Kỷ luật thực thi.')
        lines.append('')
    else:
        lines.append("☊ Nút Bắc Unknown (0.00°)")
        lines.append("Hướng phát triển của kiếp này")
        lines.append("- Cần xác định vị trí Nút Bắc để có hướng dẫn cụ thể.")
        lines.append('')

    chiron_sign = sign_name('chiron')
    if chiron_sign != 'Unknown':
        lines.append(f"⚷ Chiron {chiron_sign} ({deg('chiron')})")
        lines.append('Vết thương sâu kín')
        lines.append('- Tổn thương liên quan tới quyền lực nội tâm.')
        lines.append('- Cảm giác bị phản bội hoặc mất kiểm soát trong thân mật.')
        lines.append('👉 Chữa lành bằng cách:')
        lines.append('- Thiết lập ranh giới rõ ràng;')
        lines.append('- Tìm môi trường an toàn để tử tế với bản thân;')
        lines.append('')
    else:
        lines.append("⚷ Chiron Unknown (0.00°)")
        lines.append("Vết thương sâu kín")
        lines.append("- Cần xác định vị trí Chiron để có hướng dẫn cụ thể.")
        lines.append('')

    # 6. Kết luận ngắn gọn
    lines.append('6. Kết luận ngắn gọn')
    lines.append('')
    lines.append('Bạn là người:')
    lines.append('- Hướng tới kết nối và công bằng trong giao tiếp.')
    lines.append('- Tư duy xã hội, giỏi thương lượng và kết nối.')
    lines.append('- Có chiều sâu cảm xúc tiềm ẩn và khao khát cam kết.')
    lines.append('- Có xu hướng đổi mới và tầm nhìn cộng đồng.')
    lines.append('')
    lines.append('Bài học lớn nhất:')
    lines.append('- Biến năng lực kết nối và phân tích thành kỹ năng thực thi để tạo kết quả cụ thể và bền vững.')

    return '\n'.join(lines)
