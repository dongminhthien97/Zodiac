import React from 'react'
import ChartDisplay from '../components/ChartDisplay'
import ResultCard from '../components/ResultCard'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

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

const INSIGHT_LABELS = {
  summary: 'Tổng quan lá số',
  personality: 'Tính cách',
  emotional_style: 'Cảm xúc nội tâm',
  love_style: 'Phong cách tình yêu',
  career_style: 'Định hướng sự nghiệp',
  strengths: 'Điểm mạnh nổi bật',
  growth_edges: 'Điểm cần phát triển',
  advice: 'Khuyến nghị cá nhân'
}

function formatGeneratedAt(value) {
  if (!value) return 'Chưa có dữ liệu thời gian'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return date.toLocaleString('vi-VN', { hour12: false })
}

function renderValue(value) {
  if (Array.isArray(value)) {
    return (
      <ul className="list-disc pl-5">
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

function PlanetsDisplay({ planets = [] }) {
  if (!planets.length) return <p>Chưa có dữ liệu hành tinh chi tiết.</p>

  return (
    <div className="flex flex-wrap gap-2">
      {planets.map((planet) => (
        <Badge key={`${planet.name}-${planet.sign}-${planet.degree}`}>
          {planet.name}: {planet.sign} ({planet.degree.toFixed(2)}°)
        </Badge>
      ))}
    </div>
  )
}

export default function ResultPage() {
  const result = useCompatibilityStore((state) => state.result)
  const reset = useCompatibilityStore((state) => state.reset)
  const resultType = useCompatibilityStore((state) => state.resultType)

  if (!result) return null

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
          <ResultCard title="Danh sách hành tinh (realtime từ API)">
            <PlanetsDisplay planets={person.planets} />
          </ResultCard>
        </div>

        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          {insightEntries.map(([key, value]) => (
            <ResultCard key={key} title={INSIGHT_LABELS[key] || key}>
              {renderValue(value)}
            </ResultCard>
          ))}
        </div>
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
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ResultCard title="Hành tinh người A">
          <PlanetsDisplay planets={person_a.planets} />
        </ResultCard>
        <ResultCard title="Hành tinh người B">
          <PlanetsDisplay planets={person_b.planets} />
        </ResultCard>
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
