import React from 'react'
import { cn } from './utils'

export function Card({ className, ...props }) {
  return (
    <div
      className={cn(
        'rounded-3xl border border-white/10 bg-white/8 backdrop-blur p-6 shadow-soft',
        className
      )}
      {...props}
    />
  )
}

export function CardHeader({ className, ...props }) {
  return <div className={cn('mb-4', className)} {...props} />
}

export function CardTitle({ className, ...props }) {
  return (
    <h3 className={cn('text-xl font-display text-white', className)} {...props} />
  )
}

export function CardContent({ className, ...props }) {
  return <div className={cn('space-y-3 text-sm text-white/80', className)} {...props} />
}
