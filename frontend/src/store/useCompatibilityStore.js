import { create } from 'zustand'

export const useCompatibilityStore = create((set) => ({
  mode: 'compatibility',
  result: null,
  resultType: null,
  loading: false,
  error: null,
  setMode: (mode) => set({ mode }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setResult: (resultType, result) => set({ resultType, result, error: null, loading: false }),
  reset: () => set({ result: null, resultType: null, error: null, loading: false })
}))
