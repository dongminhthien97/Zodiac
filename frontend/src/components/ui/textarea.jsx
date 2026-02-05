import React from 'react'
import { cn } from './utils'

export function Textarea({ className, ...props }) {
  return (
    <textarea
      className={cn(
        'w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder:text-white/40 focus:border-gold-400 focus:outline-none',
        className
      )}
      {...props}
    />
  )
}
