import React from 'react'
import CompatibilityForm from '../components/CompatibilityForm'
import SingleZodiacForm from '../components/SingleZodiacForm'
import { Button } from '../components/ui/button'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

export default function Home() {
  const loading = useCompatibilityStore((state) => state.loading)
  const error = useCompatibilityStore((state) => state.error)
  const setError = useCompatibilityStore((state) => state.setError)
  const mode = useCompatibilityStore((state) => state.mode)
  const setMode = useCompatibilityStore((state) => state.setMode)

  return (
    <div className="bg-hero-glow">
      <header className="mx-auto max-w-6xl px-6 py-12">
        <div className="max-w-2xl">
          <p className="text-sm uppercase tracking-[0.3em] text-pink-400">Bói cung hoàng đạo</p>
          <h1 className="mt-4 text-4xl md:text-6xl font-display">
            Khám phá sự tương hợp và bản đồ sao của bạn.
          </h1>
          <p className="mt-4 text-white/70">
            Nhập thông tin sinh để xem Mặt Trời, Mặt Trăng, Cung mọc và phân tích chi tiết.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 pb-16">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-display">Chọn loại tra cứu</h2>
          {loading && <span className="text-sm text-pink-400">Đang tính toán...</span>}
        </div>
        <div className="mb-8 flex flex-wrap gap-3">
          <Button
            type="button"
            variant={mode === 'compatibility' ? 'cute' : 'outline'}
            onClick={() => setMode('compatibility')}
          >
            Tương hợp 2 người
          </Button>
          <Button
            type="button"
            variant={mode === 'natal' ? 'cute' : 'outline'}
            onClick={() => setMode('natal')}
          >
            Tra cứu 1 người
          </Button>
        </div>
        {error && (
          <div className="mb-6 rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm">
            <div className="flex items-center justify-between">
              <span>{error}</span>
              <Button variant="ghost" onClick={() => setError(null)}>Đóng</Button>
            </div>
          </div>
        )}
        {mode === 'compatibility' ? <CompatibilityForm /> : <SingleZodiacForm />}
      </main>
    </div>
  )
}
