import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'

export default function ChartDisplay({ title, chart }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          <Badge>Mặt Trời: {chart.sun_sign}</Badge>
          <Badge>Mặt Trăng: {chart.moon_sign || 'Chưa rõ'}</Badge>
          <Badge>Cung mọc: {chart.ascendant || 'Chưa rõ'}</Badge>
        </div>
        {chart.svg_chart ? (
          <div
            className="mt-4 rounded-2xl bg-white/5 p-4"
            dangerouslySetInnerHTML={{ __html: chart.svg_chart }}
          />
        ) : (
          <p className="mt-4 text-sm text-white/60">
            Chưa thể hiển thị SVG lá số. Hãy cung cấp giờ sinh để có biểu đồ chính xác hơn.
          </p>
        )}
      </CardContent>
    </Card>
  )
}
