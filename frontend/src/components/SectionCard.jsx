import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

export default function SectionCard({ title, text }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{text}</p>
      </CardContent>
    </Card>
  )
}
