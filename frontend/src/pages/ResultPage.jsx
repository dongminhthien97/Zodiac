import React from 'react'
import ChartDisplay from '../components/ChartDisplay'
import ResultCard from '../components/ResultCard'
import { Button } from '../components/ui/button'
import { useCompatibilityStore } from '../store/useCompatibilityStore'
import AstrologyProfile from '../components/astrology/AstrologyProfile'
import { UserPreferencesProvider } from '../contexts/UserPreferencesContext'

const DETAIL_LABELS = {
  summary: 'Tổng quan',
  personality: 'Tính cách kết hợp',
  love_style: 'Phong cách yêu',
  career: 'Công việc & mục tiêu',
  relationships: 'Mối quan hệ',
  advice: 'Lời khuyên',
  conflict_points: 'Điểm dễ mâu thuẫn',
  recommended_activities: 'Gợi ý hoạt động',
  aspects: 'Góc chiếu nổi bật'
}

const CHART_LABELS = {
  name: 'Tên',
  sun_sign: 'Mặt Trời',
  moon_sign: 'Mặt Trăng',
  ascendant: 'Cung mọc'
}

const INSIGHT_LABELS = {
  overview: 'Tổng quan năng lượng',
  personality: 'Tính cách cốt lõi',
  love: 'Tình yêu & kết nối',
  hobbies: 'Sở thích phù hợp',
  career: 'Định hướng công việc',
  life_path: 'Định hướng cuộc sống',
  strengths: 'Điểm mạnh nổi bật',
  challenges: 'Thách thức thường gặp',
  growth_areas: 'Gợi ý phát triển',
  recommendations: 'Khuyến nghị thực hành'
}

const PLANET_LABELS = {
  Sun: 'Mặt Trời',
  Moon: 'Mặt Trăng',
  Mercury: 'Sao Thủy',
  Venus: 'Sao Kim',
  Mars: 'Sao Hỏa',
  Jupiter: 'Sao Mộc',
  Saturn: 'Sao Thổ',
  Uranus: 'Thiên Vương',
  Neptune: 'Hải Vương',
  Pluto: 'Diêm Vương',
  Mean_Node: 'Nút Bắc (Mean)',
  True_Node: 'Nút Bắc (True)',
  Chiron: 'Chiron'
}

const SIGN_LABELS = {
  Ari: 'Aries', Tau: 'Taurus', Gem: 'Gemini', Can: 'Cancer', Leo: 'Leo', Vir: 'Virgo',
  Lib: 'Libra', Sco: 'Scorpio', Sag: 'Sagittarius', Cap: 'Capricorn', Aqu: 'Aquarius', Pis: 'Pisces'
}

function formatGeneratedAt(value) {
  if (!value) return 'Chưa có dữ liệu thời gian'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return date.toLocaleString('vi-VN', { hour12: false })
}

function normalizeSign(sign) {
  return SIGN_LABELS[sign] || sign
}

function renderValue(value) {
  if (Array.isArray(value)) {
    return (
      <ul className="list-disc space-y-1 pl-5">
        {value.map((item, index) => (
          <li key={`${index}-${typeof item === 'object' ? JSON.stringify(item) : item}`}>
            {typeof item === 'object' ? JSON.stringify(item) : item}
          </li>
        ))}
      </ul>
    )
  }

  if (typeof value === 'object' && value !== null) {
    return <pre className="overflow-x-auto text-sm text-white/80">{JSON.stringify(value, null, 2)}</pre>
  }

  return <p>{value || 'Chưa có dữ liệu'}</p>
}

function ChartMetadata({ chart }) {
  const chartEntries = Object.entries(chart).filter(([key]) => key !== 'planets' && key !== 'svg_chart')

  return (
    <ResultCard title="Dữ liệu lá số chi tiết">
      <div className="space-y-2 text-sm text-white/80">
        {chartEntries.map(([key, value]) => (
          <div key={key}>
            <span className="font-semibold text-white">{CHART_LABELS[key] || key}:</span> {String(value || 'Chưa có dữ liệu')}
          </div>
        ))}
      </div>
    </ResultCard>
  )
}

function PlanetSummary({ planets }) {
  return (
    <ResultCard title="Các hành tinh chính">
      <div className="grid gap-3 sm:grid-cols-2">
        {planets.map((planet) => (
          <div key={`${planet.name}-${planet.degree}`} className="rounded-xl border border-white/10 bg-white/5 p-3">
            <p className="font-semibold text-white">{PLANET_LABELS[planet.name] || planet.name}</p>
            <p className="text-sm text-white/70">Cung: {normalizeSign(planet.sign)}</p>
            <p className="text-sm text-white/70">Kinh độ: {Number(planet.degree).toFixed(2)}°</p>
          </div>
        ))}
      </div>
    </ResultCard>
  )
}

export default function ResultPage() {
  const result = useCompatibilityStore((state) => state.result)
  const reset = useCompatibilityStore((state) => state.reset)
  const resultType = useCompatibilityStore((state) => state.resultType)

  if (!result) return null

  // Check if we have the new astrology profile format
  // We prioritize this new view if available
  const hasAstrologyProfile = !!result.astrology_profile

  if (resultType === 'natal') {
    const { person, generated_at, insights } = result
    const insightEntries = Object.entries(insights || {}).filter(([, value]) => value !== null && value !== undefined)

    return (
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-pink-400">Lá số cá nhân</p>
            <h1 className="mt-2 text-4xl font-display">Khám phá bản đồ sao của bạn</h1>
            <p className="mt-2 text-white/70">Kết quả realtime: {formatGeneratedAt(generated_at)}</p>
          </div>
          <Button variant="outline" onClick={reset}>Tra cứu mới</Button>
        </div>

        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <ChartDisplay title="Lá số của bạn" chart={person} />
          <ChartMetadata chart={person} />
        </div>

        <div className="mt-10">
          <PlanetSummary planets={person.planets || []} />
        </div>

        {/* New Astrology Profile Rendering */}
        {hasAstrologyProfile ? (
          <div className="mt-16 border-t border-white/10 pt-10">
            <h2 className="text-3xl font-display text-center mb-10 text-gold-400">
              Luận giải chuyên sâu
            </h2>
            <UserPreferencesProvider>
              <AstrologyProfile contentJson={result.astrology_profile} />
            </UserPreferencesProvider>
          </div>
        ) : (
          <div className="mt-10 grid gap-6 lg:grid-cols-2">
            {insightEntries.map(([key, value]) => (
              <ResultCard key={key} title={INSIGHT_LABELS[key] || key}>
                {renderValue(value)}
              </ResultCard>
            ))}
          </div>
        )}
      </div>
    )
  }

  const { person_a, person_b, details, generated_at } = result
  const detailEntries = Object.entries(details).filter(([, value]) => value !== null && value !== undefined)

  return (
    <div className="mx-auto max-w-6xl px-6 py-12">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-gold-400">Kết quả tương hợp</p>
          <h1 className="mt-2 text-4xl font-display">{details.score}% hợp nhau</h1>
          <p className="mt-2 text-white/70">Kết quả realtime: {formatGeneratedAt(generated_at)}</p>
        </div>
        <Button variant="outline" onClick={reset}>Tra cứu mới</Button>
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ChartDisplay title="Lá số người A" chart={person_a} />
        <ChartDisplay title="Lá số người B" chart={person_b} />
        <ChartMetadata chart={person_a} />
        <ChartMetadata chart={person_b} />
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        {detailEntries.map(([key, value]) => (
          <ResultCard key={key} title={DETAIL_LABELS[key] || key}>
            {renderValue(value)}
          </ResultCard>
        ))}
      </div>
    </div>
  )
}
