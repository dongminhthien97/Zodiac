import React, { ButtonHTMLAttributes } from 'react'
import { cn } from './utils'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'cosmic' | 'glass' | 'ghost' | 'outline' | 'cute'
  size?: 'sm' | 'md' | 'lg'
}

export function Button({ className, variant = 'primary', size = 'md', ...props }: ButtonProps) {
  const variants = {
    primary: 'bg-gold-500 text-ink-900 hover:bg-gold-400 shadow-glow',
    cosmic: 'bg-gradient-to-r from-nebula-500 to-indigo-500 text-white hover:brightness-110 shadow-glow-nebula border border-white/20',
    glass: 'bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 shadow-soft',
    ghost: 'bg-transparent text-white/80 hover:text-white hover:bg-white/5',
    outline: 'border border-gold-500/50 text-gold-400 hover:border-gold-400 hover:bg-gold-500/10',
    cute: 'bg-pink-400 text-ink-900 hover:bg-pink-300 shadow-glow'
  }

  const sizes = {
    sm: 'px-4 py-2 text-xs',
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base'
  }

  return (
    <button
      className={cn(
        'relative overflow-hidden rounded-full font-bold tracking-wide transition-all duration-300 active:scale-95 disabled:opacity-50 disabled:pointer-events-none',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  )
}
