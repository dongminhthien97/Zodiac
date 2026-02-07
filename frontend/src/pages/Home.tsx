import React from 'react'
import CompatibilityForm from '../components/CompatibilityForm'
import SingleZodiacForm from '../components/SingleZodiacForm'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

export default function Home() {
  const loading = useCompatibilityStore((state) => state.loading)
  const error = useCompatibilityStore((state) => state.error)
  const setError = useCompatibilityStore((state) => state.setError)
  const mode = useCompatibilityStore((state) => state.mode)
  const setMode = useCompatibilityStore((state) => state.setMode)

  return (
    <div className="home-page section-py">
      <header className="container">
        <div className="hero-content">
          <p className="subtitle">Khám phá Bản đồ sao</p>
          <h1 className="main-title">
            Khám phá sự tương hợp và năng lượng vũ trụ của bạn.
          </h1>
          <p className="hero-desc">
            Nhập thông tin sinh để nhận bản phân tích chi tiết về Mặt Trời, Mặt Trăng, Cung mọc và chỉ số tương hợp.
          </p>
        </div>
      </header>

      <main className="container">
        <div className="mode-selector-header">
          <h2 className="section-title">Chọn loại tra cứu</h2>
          {loading && <span className="loading-status">Đang tính toán...</span>}
        </div>
        
        <div className="mode-tabs">
          <button
            type="button"
            className={`btn-outline ${mode === 'compatibility' ? 'active' : ''}`}
            onClick={() => setMode('compatibility')}
          >
            Tương hợp 2 người
          </button>
          <button
            type="button"
            className={`btn-outline ${mode === 'natal' ? 'active' : ''}`}
            onClick={() => setMode('natal')}
          >
            Tra cứu 1 người
          </button>
        </div>

        {error && (
          <div className="error-box glass-card">
            <div className="error-content">
              <span>{error}</span>
              <button className="btn-close" onClick={() => setError(null)}>Đóng</button>
            </div>
          </div>
        )}

        <div className="form-container">
          {mode === 'compatibility' ? <CompatibilityForm /> : <SingleZodiacForm />}
        </div>
      </main>
      
      <style>{`
        .hero-content {
          max-width: 800px;
          margin-bottom: 60px;
        }
        .subtitle {
          color: var(--nebula-pink);
          text-transform: uppercase;
          letter-spacing: 4px;
          font-size: 14px;
          font-weight: 600;
          margin-bottom: 16px;
        }
        .main-title {
          font-size: 3.5rem;
          line-height: 1.1;
          margin-bottom: 24px;
          background: linear-gradient(to right, #fff, var(--gold-primary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .hero-desc {
          font-size: 1.1rem;
          color: var(--white-70);
          max-width: 600px;
        }
        .mode-selector-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }
        .mode-tabs {
          display: flex;
          gap: 16px;
          margin-bottom: 40px;
        }
        .loading-status {
          color: var(--nebula-purple);
          font-size: 0.9rem;
          font-weight: 600;
        }
        .error-box {
          margin-bottom: 32px;
          padding: 16px 24px;
          border-left: 4px solid #ef4444;
          background: rgba(239, 68, 68, 0.1);
        }
        .error-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .btn-close {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          text-decoration: underline;
        }
      `}</style>
    </div>
  )
}
