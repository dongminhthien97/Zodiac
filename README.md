# Zodiac Compatibility Checker

Dự án starter full‑stack để xem **độ tương hợp 2 người** và **tra cứu cung hoàng đạo 1 người** theo Tây phương, dùng Kerykeion (Swiss Ephemeris), FastAPI và React + Tailwind.

## Cấu trúc thư mục

```
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── astrology.py
│   ├── services/
│   │   ├── astrology_service.py
│   │   └── geocoding_service.py
│   ├── models/
│   │   └── schemas.py
│   ├── utils/
│   │   └── compatibility_data.py
│   ├── supabase_client.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── package.json
│   └── .env.example
│
└── README.md
```

## Backend (FastAPI)

1. Tạo venv và cài dependencies:

```bash
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

2. Tạo file env:

```bash
copy .env.example .env
```

3. Chạy server:

```bash
.\.venv\Scripts\python -m uvicorn main:app --reload --port 8000
```

## Frontend (React + Vite)

1. Cài dependencies:

```bash
cd frontend
npm install
```

2. Tạo file env:

```bash
copy .env.example .env
```

3. Chạy dev server:

```bash
npm run dev
```

## API mẫu

### 1) Tương hợp 2 người
**Endpoint:** `POST /api/compatibility`

```json
{
  "person_a": {
    "name": "Linh",
    "gender": "female",
    "birth_date": "1994-08-12",
    "birth_time": "14:30",
    "time_unknown": false,
    "birth_place": "Hà Nội, Việt Nam"
  },
  "person_b": {
    "name": "Minh",
    "gender": "male",
    "birth_date": "1990-02-03",
    "birth_time": "09:10",
    "time_unknown": false,
    "birth_place": "TP. Hồ Chí Minh, Việt Nam"
  }
}
```

### 2) Tra cứu 1 người
**Endpoint:** `POST /api/natal`

```json
{
  "person": {
    "name": "Linh",
    "gender": "female",
    "birth_date": "1994-08-12",
    "birth_time": "14:30",
    "time_unknown": false,
    "birth_place": "Hà Nội, Việt Nam"
  }
}
```

## Supabase (Tuỳ chọn)

1. Tạo project Supabase.
2. Điền `SUPABASE_URL` và `SUPABASE_SERVICE_ROLE_KEY` trong `backend/.env`.
3. Tạo bảng:

```sql
create table if not exists compatibility_checks (
  id uuid primary key default gen_random_uuid(),
  person_a_name text,
  person_b_name text,
  person_a_place text,
  person_b_place text,
  score int,
  created_at timestamptz default now()
);
```

## Geocoding

- Chính: Nominatim (OpenStreetMap).
- Tuỳ chọn: Google Geocoding (cần `GOOGLE_GEOCODING_API_KEY`).

## Deploy

- Backend: Render hoặc Railway.
- Frontend: Vercel (kết nối GitHub, set `VITE_BACKEND_URL`).
- Supabase: tạo project ở supabase.com.
- Mobile tương lai: có thể tái sử dụng UI với React Native + Expo.

## Ghi chú

- Nếu không có giờ sinh, hệ thống giả định 12:00 và bỏ qua Cung mọc.
- Cung cấp đầy đủ ngày/giờ/nơi sinh để kết quả chính xác hơn.
