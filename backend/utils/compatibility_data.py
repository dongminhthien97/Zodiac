﻿SUN_SIGN_RANGES = {
    "Aries": ((3, 21), (4, 19)),
    "Taurus": ((4, 20), (5, 20)),
    "Gemini": ((5, 21), (6, 20)),
    "Cancer": ((6, 21), (7, 22)),
    "Leo": ((7, 23), (8, 22)),
    "Virgo": ((8, 23), (9, 22)),
    "Libra": ((9, 23), (10, 22)),
    "Scorpio": ((10, 23), (11, 21)),
    "Sagittarius": ((11, 22), (12, 21)),
    "Capricorn": ((12, 22), (12, 31)),
    "Aquarius": ((1, 20), (2, 18)),
    "Pisces": ((2, 19), (3, 20)),
}

SIGN_TRAITS = {
    "Aries": "Fire|Mạnh mẽ, thẳng thắn và thích hành động.",
    "Taurus": "Earth|Ổn định, tinh tế và chung thủy.",
    "Gemini": "Air|Hiếu kỳ, duyên dáng và linh hoạt.",
    "Cancer": "Water|Bảo vệ, trực giác tốt và giàu chăm sóc.",
    "Leo": "Fire|Ấm áp, giàu biểu đạt và tự tin.",
    "Virgo": "Earth|Thực tế, tỉ mỉ và chu đáo.",
    "Libra": "Air|Khéo léo, duyên dáng và coi trọng hòa hợp.",
    "Scorpio": "Water|Mãnh liệt, kín đáo và biến đổi sâu.",
    "Sagittarius": "Fire|Lạc quan, thích khám phá và nhìn xa.",
    "Capricorn": "Earth|Tham vọng, vững vàng và kỷ luật.",
    "Aquarius": "Air|Sáng tạo, độc lập và hướng tương lai.",
    "Pisces": "Water|Đồng cảm, mơ mộng và nghệ sĩ.",
}

ELEMENT_COMPATIBILITY = {
    ("Fire", "Fire"): 82,
    ("Earth", "Earth"): 80,
    ("Air", "Air"): 84,
    ("Water", "Water"): 78,
    ("Fire", "Air"): 86,
    ("Air", "Fire"): 86,
    ("Earth", "Water"): 83,
    ("Water", "Earth"): 83,
    ("Fire", "Earth"): 62,
    ("Earth", "Fire"): 62,
    ("Air", "Water"): 60,
    ("Water", "Air"): 60,
    ("Fire", "Water"): 68,
    ("Water", "Fire"): 68,
    ("Earth", "Air"): 65,
    ("Air", "Earth"): 65,
}

ASPECT_WEIGHTS = {
    "sun_moon": 8,
    "venus_mars": 6,
}

GENDER_TONE = {
    ("male", "female"): "bổ trợ",
    ("female", "male"): "bổ trợ",
    ("male", "male"): "năng động",
    ("female", "female"): "tinh tế",
}
