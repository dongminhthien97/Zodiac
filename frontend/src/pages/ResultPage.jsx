import React from 'react'
import ChartDisplay from '../components/ChartDisplay'
import ResultCard from '../components/ResultCard'
import SectionCard from '../components/SectionCard'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

export default function ResultPage() {
  const result = useCompatibilityStore((state) => state.result)
  const reset = useCompatibilityStore((state) => state.reset)
  const resultType = useCompatibilityStore((state) => state.resultType)

  if (!result) {
    return null
  }

  if (resultType === 'natal') {
    const { person } = result
    return (
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-pink-400">Lá số cá nhân</p>
            <h1 className="mt-2 text-4xl font-display">Khám phá bản đồ sao của bạn</h1>
            <p className="mt-2 text-white/70">
              Đây là tổng quan về Mặt Trời, Mặt Trăng và Cung mọc dựa trên thông tin sinh.
            </p>
          </div>
          <Button variant="outline" onClick={reset}>Tra cứu mới</Button>
        </div>

        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <ChartDisplay title="Lá số của bạn" chart={person} />
          <ResultCard title="Các hành tinh chính">
            <div className="flex flex-wrap gap-2">
              {person.planets.map((planet) => (
                <Badge key={`${planet.name}-${planet.sign}`}>
                  {planet.name}: {planet.sign}
                </Badge>
              ))}
            </div>
          </ResultCard>
        </div>
      </div>
    )
  }

  const { person_a, person_b, details } = result

  return (
    <div className="mx-auto max-w-6xl px-6 py-12">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-gold-400">Kết quả tương hợp</p>
          <h1 className="mt-2 text-4xl font-display">{details.score}% hợp nhau</h1>
          <p className="mt-2 text-white/70">{details.summary}</p>
        </div>
        <Button variant="outline" onClick={reset}>Tra cứu mới</Button>
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ChartDisplay title="Lá số người A" chart={person_a} />
        <ChartDisplay title="Lá số người B" chart={person_b} />
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <SectionCard title="Tính cách kết hợp" text={details.personality} />
        <SectionCard title="Phong cách yêu" text={details.love_style} />
        <SectionCard title="Công việc & mục tiêu" text={details.career} />
        <SectionCard title="Mối quan hệ" text={details.relationships} />
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ResultCard title="Lời khuyên">
          <p>{details.advice}</p>
        </ResultCard>
        <ResultCard title="Điểm dễ mâu thuẫn">
          <p>{details.conflict_points}</p>
        </ResultCard>
      </div>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        <ResultCard title="Góc chiếu nổi bật">
          <div className="flex flex-wrap gap-2">
            {details.aspects.map((aspect) => (
              <Badge key={aspect}>{aspect}</Badge>
            ))}
          </div>
        </ResultCard>
        <ResultCard title="Gợi ý hoạt động">
          <ul className="list-disc pl-5">
            {details.recommended_activities.map((activity) => (
              <li key={activity}>{activity}</li>
            ))}
          </ul>
        </ResultCard>
      </div>
    </div>
  )
}
