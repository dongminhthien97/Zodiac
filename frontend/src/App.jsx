import Home from './pages/Home'
import ResultPage from './pages/ResultPage'
import { useCompatibilityStore } from './store/useCompatibilityStore'

export default function App() {
  const result = useCompatibilityStore((state) => state.result)

  return (
    <div className="min-h-screen">
      {result ? <ResultPage /> : <Home />}
    </div>
  )
}
