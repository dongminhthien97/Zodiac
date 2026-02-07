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

export const fetchStandardReport = async (payload: any) => {
  const { data } = await api.post('/api/natal/standard', payload)
  return data
}

export default api

export type BirthRequest = {
  datetime_utc: string;
  lat: number;
  lon: number;
};

export const fetchReport = async (payload: BirthRequest) => {
  // POST directly to the FastAPI backend running on port 8001
  const res = await fetch(((import.meta as any).env.VITE_BACKEND_URL || 'http://localhost:8001') + '/report', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) throw new Error(`Report request failed: ${res.status}`)
  return res.json()
}

export const fetchZodiacAIReport = async (payload: {
  datetime_utc: string;
  lat: number;
  lon: number;
}) => {
  const response = await axios.post(`${api.defaults.baseURL}/zodiac-ai/report`, payload);
  return response.data;
};
