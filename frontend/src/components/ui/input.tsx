import React, { InputHTMLAttributes } from "react";
import { cn } from "./utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        "glass-input w-full rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10",
        className,
      )}
      {...props}
    />
  );
}

export function InputDark({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        "glass-input dark-bg w-full rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10",
        className,
      )}
      {...props}
    />
  );
}

export function InputLight({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        "glass-input light-bg w-full rounded-xl px-4 py-3 text-sm shadow-inner transition-all hover:bg-white/10",
        className,
      )}
      {...props}
    />
  );
}
