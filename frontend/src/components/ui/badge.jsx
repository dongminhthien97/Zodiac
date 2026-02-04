import React from 'react'
import { cn } from './utils'

export function Badge({ className, ...props }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-white/80',
        className
      )}
      {...props}
    />
  )
}
