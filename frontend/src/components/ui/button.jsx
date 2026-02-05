import React from 'react'
import { cn } from './utils'

export function Button({ className, variant = 'primary', ...props }) {
  const variants = {
    primary: 'bg-gold-500 text-ink-900 hover:bg-gold-400',
    ghost: 'bg-transparent text-white hover:bg-white/10',
    outline: 'border border-white/20 text-white hover:border-white/40',
    cute: 'bg-pink-400 text-ink-900 hover:bg-pink-300'
  }

  return (
    <button
      className={cn(
        'px-5 py-2.5 rounded-full text-sm font-semibold transition shadow-soft',
        variants[variant],
        className
      )}
      {...props}
    />
  )
}
