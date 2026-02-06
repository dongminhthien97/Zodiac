import { create } from 'zustand'

interface CompatibilityState {
  mode: 'compatibility' | 'natal';
  result: any;
  resultType: string | null;
  loading: boolean;
  error: string | null;
  setMode: (mode: 'compatibility' | 'natal') => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setResult: (resultType: string, result: any) => void;
  reset: () => void;
}

export const useCompatibilityStore = create<CompatibilityState>((set) => ({
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
