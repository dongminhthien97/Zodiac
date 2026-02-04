import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

export default function ResultCard({ title, children }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  )
}
