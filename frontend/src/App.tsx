import Home from './pages/Home'
import ResultPage from './pages/ResultPage'
import { useCompatibilityStore } from './store/useCompatibilityStore'

export default function App() {
  const result = useCompatibilityStore((state) => state.result)

  return (
    <>
      <div className="stars-overlay"></div>
      <div className="app-container">
        {result ? <ResultPage /> : <Home />}
      </div>
    </>
  )
}
