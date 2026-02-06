import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

interface SectionCardProps {
  title: string;
  text: string;
}

export default function SectionCard({ title, text }: SectionCardProps) {
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
