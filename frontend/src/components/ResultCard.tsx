import React, { ReactNode } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

interface ResultCardProps {
  title: string;
  children: ReactNode;
}

export default function ResultCard({ title, children }: ResultCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  )
}
