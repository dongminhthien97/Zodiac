import React, { SelectHTMLAttributes } from "react";
import { cn } from "./utils";

export interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {}

export function Select({ className, children, ...props }: SelectProps) {
  return (
    <div className="relative">
      <select
        className={cn(
          "glass-input w-full appearance-none rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10 hover:cursor-pointer",
          className,
        )}
        {...props}
      >
        {children}
      </select>
      <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-white/50">
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2.5 4.5L6 8L9.5 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}

export function SelectDark({ className, children, ...props }: SelectProps) {
  return (
    <div className="relative">
      <select
        className={cn(
          "glass-input dark-bg w-full appearance-none rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10 hover:cursor-pointer",
          className,
        )}
        {...props}
      >
        {children}
      </select>
      <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-white/50">
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2.5 4.5L6 8L9.5 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}

export function SelectLight({ className, children, ...props }: SelectProps) {
  return (
    <div className="relative">
      <select
        className={cn(
          "glass-input light-bg w-full appearance-none rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10 hover:cursor-pointer",
          className,
        )}
        {...props}
      >
        {children}
      </select>
      <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-white/50">
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2.5 4.5L6 8L9.5 4.5"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}
