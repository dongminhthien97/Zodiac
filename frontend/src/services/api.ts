import axios from 'axios'

const api = axios.create({
  baseURL: (import.meta as any).env.VITE_BACKEND_URL || 'http://localhost:8000'
})

export const fetchCompatibility = async (payload: any) => {
  const { data } = await api.post('/api/compatibility', payload)
  return data
}

export const fetchNatal = async (payload: any) => {
  const { data } = await api.post('/api/natal', payload)
  return data
}

export default api
