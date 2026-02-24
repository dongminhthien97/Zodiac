"""
services/ai/prompts.py
-----------------------
Prompt templates for AI service layer.
Clean separation of concerns, no inline prompts in business logic.
"""

from typing import Dict, Any


class NatalPrompts:
    """Prompt templates for natal chart analysis."""
    
    SYSTEM_PROMPT = """Bạn là một nhà chiêm tinh học chuyên nghiệp.
Nhiệm vụ: Cung cấp giải thích chi tiết cho các hành tinh và aspect đã được cung cấp.

QUAN TRỌNG:
- Trả về CHÍNH XÁC một object JSON hợp lệ
- KHÔNG sử dụng markdown
- KHÔNG thêm giải thích
- Tất cả nội dung bằng tiếng Việt
- Mỗi giải thích 3-5 câu, chuyên sâu và cụ thể
- KHÔNG tạo ra các hành tinh mới
- Chỉ giải thích các hành tinh và aspect đã được cung cấp

Schema JSON yêu cầu:
{
  "planet_interpretations": [
    {
      "planet": "Sun",
      "interpretation": "giải thích chi tiết 3-5 câu"
    }
  ],
  "aspect_interpretations": [
    {
      "aspect_type": "trine",
      "planet_1": "Sun",
      "planet_2": "Moon",
      "interpretation": "giải thích chi tiết 3-5 câu"
    }
  ],
  "core_identity": {
    "summary": "tổng hợp 3-5 câu về bản chất cốt lõi",
    "sun_sign": "giải thích Mặt Trời",
    "moon_sign": "giải thích Mặt Trăng",
    "rising_sign": "giải thích Cung Mọc"
  },
  "love_profile": {
    "attachment_style": "phong cách gắn bó",
    "strengths": "điểm mạnh trong tình yêu",
    "challenges": "thách thức trong tình yêu",
    "advice": "lời khuyên về tình yêu"
  },
  "career_analysis": {
    "best_fields": "lĩnh vực phù hợp nhất",
    "work_style": "phong cách làm việc",
    "growth_advice": "lời khuyên phát triển sự nghiệp"
  },
  "psychological_pattern": {
    "core_wound": "vết thương tâm lý cốt lõi",
    "healing_direction": "hướng phát triển lành mạnh"
  },
  "practical_guidance": {
    "career": "hướng dẫn thực tế về sự nghiệp",
    "relationships": "hướng dẫn thực tế về các mối quan hệ",
    "self_development": "hướng dẫn thực tế về phát triển bản thân"
  }
}"""
    
    @staticmethod
    def build_user_prompt(
        person_name: str,
        person_birth_date: str,
        person_birth_time: str,
        person_birth_place: str,
        planets_data: list[dict[str, Any]],
        aspects_data: list[dict[str, Any]]
    ) -> str:
        """Build user prompt for Natal AI interpretation."""
        
        # Format planets data
        planets_str = "\n".join([
            f"- {p['planet']}: {p['sign']} (longitude: {p['longitude']:.2f}°, degree: {p['degree']:.2f}°, house: {p['house']}, retrograde: {p['retrograde']})"
            for p in planets_data
        ]) if planets_data else "- Không có dữ liệu hành tinh"
        
        # Format aspects data
        aspects_str = "\n".join([
            f"- {a['aspect_type']}: {a['planet_1']} ↔ {a['planet_2']} (orb: {a['orb']:.2f}°)"
            for a in aspects_data
        ]) if aspects_data else "- Không có aspect"
        
        return f"""Hãy phân tích bản đồ sao chi tiết cho:

**Thông tin cá nhân:**
- Tên: {person_name}
- Ngày sinh: {person_birth_date}
- Giờ sinh: {person_birth_time or "Không rõ"}
- Nơi sinh: {person_birth_place}

**Dữ liệu hành tinh:**
{planets_str}

**Dữ liệu aspect:**
{aspects_str}

**YÊU CẦU PHÂN TÍCH:**

1. **Giải thích hành tinh:** Mỗi hành tinh cần được giải thích chi tiết 3-5 câu, tập trung vào:
   - Ý nghĩa của hành tinh ở cung và nhà cụ thể
   - Cách hành tinh này biểu hiện trong cuộc sống
   - Những thách thức và cơ hội tiềm ẩn
   - Tác động đến tính cách và hành vi

2. **Giải thích aspect:** Mỗi aspect cần được giải thích chi tiết 3-5 câu, tập trung vào:
   - Ý nghĩa của mối quan hệ giữa hai hành tinh
   - Cách aspect này tạo ra năng lượng trong bản đồ
   - Những biểu hiện cụ thể trong cuộc sống
   - Cơ hội phát triển và thách thức cần vượt qua

3. **Phân tích tổng thể:** Các phần còn lại cần:
   - Phân tích chuyên sâu, không chung chung
   - Cung cấp ví dụ cụ thể và thiết thực
   - Đưa ra lời khuyên thực tế và khả thi
   - Tập trung vào phát triển bản thân

**LƯU Ý:**
- KHÔNG tạo ra các hành tinh mới
- Chỉ giải thích các hành tinh và aspect đã được cung cấp
- Tất cả nội dung bằng tiếng Việt
- Giải thích phải chuyên sâu, tránh mô tả chung chung
- Mỗi giải thích 3-5 câu, không quá dài hoặc quá ngắn"""


class CompatibilityPrompts:
    """Prompt templates for compatibility analysis."""
    
    SYSTEM_PROMPT = """Bạn là một chuyên gia chiêm tinh học về tương thích cặp đôi.
Nhiệm vụ: Phân tích sự tương thích chi tiết giữa hai bản đồ sao.

QUAN TRỌNG:
- Trả về CHÍNH XÁC một object JSON hợp lệ
- KHÔNG sử dụng markdown
- KHÔNG thêm giải thích
- Tất cả nội dung bằng tiếng Việt
- Phân tích chuyên sâu, ít nhất 1000 từ
- Cung cấp ví dụ cụ thể và lời khuyên thực tế"""
    
    @staticmethod
    def build_user_prompt(
        person_a: dict[str, Any],
        person_b: dict[str, Any],
        aspects: list[str],
        fallback_mode: bool
    ) -> str:
        """Build user prompt for compatibility analysis."""
        
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
        
        return f"""Hãy phân tích sự tương thích chi tiết giữa hai bản đồ sao sau đây:

**Thông tin hai người:**
- Người A: Mặt Trời {sun_a}, Mặt Trăng {moon_a}, Thủy Tinh {mercury_a}, Kim Tinh {venus_a}, Hỏa Tinh {mars_a}, Cung Mọc {asc_a}
- Người B: Mặt Trời {sun_b}, Mặt Trăng {moon_b}, Thủy Tinh {mercury_b}, Kim Tinh {venus_b}, Hỏa Tinh {mars_b}, Cung Mọc {asc_b}

**Các aspect quan trọng:** {', '.join(aspects) if aspects else 'Không có aspect cụ thể'}

{f'⚠️ Lưu ý: Phân tích ở chế độ fallback (thiếu giờ sinh), một số tính toán có thể không chính xác hoàn toàn.' if fallback_mode else 'Phân tích với đầy đủ thông tin giờ sinh.'}

**Yêu cầu phân tích chi tiết (ít nhất 1000 từ):**

1. **Sự tương thích về cảm xúc (Emotional Compatibility):**
   - Phân tích Mặt Trăng {moon_a} và Mặt Trăng {moon_b}
   - Cách hai người đáp ứng nhu cầu cảm xúc của nhau
   - Khả năng tạo môi trường cảm xúc an toàn

2. **Sức hút và tình yêu (Romantic Attraction):**
   - Phân tích Kim Tinh {venus_a} và Kim Tinh {venus_b}
   - Cách thể hiện tình yêu và đam mê
   - Sự hấp dẫn tình dục và hóa học

3. **Giao tiếp và tư duy (Communication):**
   - Phân tích Thủy Tinh {mercury_a} và Thủy Tinh {mercury_b}
   - Cách trao đổi ý tưởng và giải quyết bất đồng
   - Phong cách giao tiếp hàng ngày

4. **Xung đột và thách thức (Conflict):**
   - Những điểm xung đột tiềm ẩn
   - Cách xử lý mâu thuẫn
   - Cơ chế phòng vệ và phản ứng khi căng thẳng

5. **Ổn định lâu dài (Long-term Stability):**
   - Khả năng duy trì mối quan hệ
   - Sự phù hợp về giá trị và mục tiêu sống
   - Tiềm năng phát triển cùng nhau

6. **Phân tích hành tinh cụ thể:**
   - Tác động của từng cặp hành tinh quan trọng
   - Cách các aspect ảnh hưởng đến mối quan hệ
   - Cơ hội và thách thức từ các vị trí hành tinh

7. **Phát triển bản thân (Growth Path):**
   - Bài học mà mỗi người có thể học được từ nhau
   - Cách hỗ trợ sự phát triển cá nhân
   - Cơ hội trưởng thành tâm hồn

8. **Lời khuyên thực tế (Practical Advice):**
   - Cách nuôi dưỡng mối quan hệ
   - Chiến lược giải quyết xung đột
   - Phương pháp duy trì sự hấp dẫn lâu dài

**Yêu cầu:**
- Sử dụng ngôn ngữ chuyên nghiệp, giàu chiều sâu tâm lý
- Cung cấp ví dụ cụ thể và thiết thực
- Phân tích chi tiết từng khía cạnh
- Đưa ra lời khuyên thực tế và khả thi
- Tổng cộng ít nhất 1000 từ
- Định dạng markdown chuyên nghiệp

Hãy cung cấp một bản phân tích toàn diện, sâu sắc và thực tế."""