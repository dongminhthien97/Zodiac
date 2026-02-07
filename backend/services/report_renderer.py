from __future__ import annotations
from typing import Dict

SIGN_VN = {
    'Aries': 'Bạch Dương', 'Taurus': 'Kim Ngưu', 'Gemini': 'Song Tử', 'Cancer': 'Cự Giải',
    'Leo': 'Sư Tử', 'Virgo': 'Xử Nữ', 'Libra': 'Thiên Bình', 'Scorpio': 'Hổ Cáp',
    'Sagittarius': 'Nhân Mã', 'Capricorn': 'Ma Kết', 'Aquarius': 'Bảo Bình', 'Pisces': 'Song Ngư'
}


def _fmt_degree(longitude: float) -> str:
    # degree within sign = longitude % 30
    deg = (longitude % 360.0) % 30.0
    return f"{deg:.2f}°"


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
    # Count by element approximate by sign
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
    lines.append(f"☉ Mặt Trời {sign_name('sun')} ({deg('sun')})")
    lines.append('Bản ngã – con người muốn trở thành')
    lines.append('- '+' '.join([f"Điểm chính liên quan tới {sign_name('sun')}." ]*3))
    lines.append('⚠️ Mặt hạn chế:')
    lines.append('- Trì hoãn quyết định;')
    lines.append('- Phụ thuộc phản hồi xã hội;')
    lines.append('')
    # Moon
    lines.append(f"☽ Mặt Trăng {sign_name('moon')} ({deg('moon')})")
    lines.append('Cảm xúc – nhu cầu tinh thần')
    lines.append('- '+' '.join([f"Cách phản ứng liên quan tới {sign_name('moon')}." ]*3))
    lines.append('⚠️ Khi mất cân bằng:')
    lines.append('- Kìm nén cảm xúc;')
    lines.append('- Tìm kiếm chấp thuận bên ngoài;')
    lines.append('')
    # Mercury
    lines.append(f"☿ Sao Thủy {sign_name('mercury')} ({deg('mercury')})")
    lines.append('Tư duy – giao tiếp')
    lines.append('- '+' '.join([f"Phong cách tư duy liên quan tới {sign_name('mercury')}." ]*3))
    lines.append('⚠️ Điểm yếu:')
    lines.append('- Quyết định chậm;')
    lines.append('- Né tránh luận điểm gây tranh cãi;')
    lines.append('')

    # 3. Tình yêu – ham muốn – động lực
    lines.append('3. Tình yêu – ham muốn – động lực')
    lines.append('')
    lines.append(f"♀ Sao Kim {sign_name('venus')} ({deg('venus')})")
    lines.append('Cách yêu & giá trị tình cảm')
    lines.append('- '+' '.join([f"Phong cách tình cảm liên quan tới {sign_name('venus')}." ]*3))
    lines.append('⚠️ Mặt bóng:')
    lines.append('- Rủi ro cảm xúc khi thiếu an toàn;')
    lines.append('- Xu hướng kiểm soát hoặc nghi ngờ;')
    lines.append('👉 1 câu đối lập nội tâm: Bề ngoài tìm hòa hợp nhưng bên trong khao khát chiều sâu.')
    lines.append('')
    lines.append(f"♂ Sao Hỏa {sign_name('mars')} ({deg('mars')})")
    lines.append('Hành động – động lực')
    lines.append('- '+' '.join([f"Cách hành động liên quan tới {sign_name('mars')}." ]*3))
    lines.append('⚠️ Nhược điểm:')
    lines.append('- Thiếu kiên nhẫn với chi tiết;')
    lines.append('- Hành vi bộc phát khi stress;')
    lines.append('')

    # 4. Thế hệ – xã hội – tầm nhìn
    lines.append('4. Thế hệ – xã hội – tầm nhìn')
    lines.append('')
    for b in ['jupiter','uranus','neptune','pluto']:
        lines.append(f"{b.capitalize()} {sign_name(b)} ({deg(b)})")
        lines.append('- Mô tả ngắn gọn liên quan tới vai trò xã hội và tầm nhìn.')
        lines.append('')

    # 5. Bài học linh hồn
    lines.append('5. Bài học linh hồn')
    lines.append('')
    lines.append(f"☊ Nút Bắc {sign_name('north_node')} ({deg('north_node')})")
    lines.append('Hướng phát triển của kiếp này')
    lines.append('- Học cách tổ chức và chú ý chi tiết.')
    lines.append('- Ưu tiên sức khỏe và quản trị đời sống.')
    lines.append('- Biến ý tưởng thành hành động cụ thể.')
    lines.append('Rời xa xu hướng:')
    lines.append('- Trì hoãn bằng ngoại giao bề ngoài;')
    lines.append('- Né tránh trách nhiệm chi tiết;')
    lines.append('👉 1 câu công thức thành công (A → B): Kết nối xã hội → Kỷ luật thực thi.')
    lines.append('')
    lines.append(f"⚷ Chiron {sign_name('chiron')} ({deg('chiron')})")
    lines.append('Vết thương sâu kín')
    lines.append('- Tổn thương liên quan tới quyền lực nội tâm.')
    lines.append('- Cảm giác bị phản bội hoặc mất kiểm soát trong thân mật.')
    lines.append('👉 Chữa lành bằng cách:')
    lines.append('- Thiết lập ranh giới rõ ràng;')
    lines.append('- Tìm môi trường an toàn để tử tế với bản thân;')
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
