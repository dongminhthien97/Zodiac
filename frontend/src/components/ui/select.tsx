import React, { SelectHTMLAttributes } from 'react'
import { cn } from './utils'

export interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {}

export function Select({ className, children, ...props }: SelectProps) {
  return (
    <select
      className={cn(
        'w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white focus:border-gold-400 focus:outline-none',
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
}
