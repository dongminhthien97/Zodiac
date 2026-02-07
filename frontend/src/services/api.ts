import api from '../lib/api';
import { mapCompatibilityResponse } from '../lib/mappers/compatibilityMapper';
import { mapStandardReportResponse } from '../lib/mappers/standardReportMapper';
import { mapZodiacAIReportResponse } from '../lib/mappers/zodiacAIReportMapper';

export const fetchCompatibility = async (payload: any) => {
  const response = await api.post('/compatibility', payload);
  console.log('🔍 Raw compatibility API response:', JSON.stringify(response.data, null, 2));
  
  // Map the response to ensure consistent data structure
  const mappedData = mapCompatibilityResponse(response.data);
  return mappedData;
}

export const fetchNatal = async (payload: any) => {
  const { data } = await api.post('/natal', payload);
  return data;
}

export const fetchStandardReport = async (payload: any) => {
  const { data } = await api.post('/natal/standard', payload);
  
  // Map the response to ensure consistent data structure
  const mappedData = mapStandardReportResponse(data);
  return mappedData;
}

export default api

export type BirthRequest = {
  datetime_utc: string;
  lat: number;
  lon: number;
};

export const fetchReport = async (payload: BirthRequest) => {
  // POST directly to the FastAPI backend
  const res = await fetch(`${api.defaults.baseURL}/report`, {
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
  const response = await api.post('/zodiac-ai/report', payload);
  
  // Map the response to ensure consistent data structure
  const mappedData = mapZodiacAIReportResponse(response.data);
  return mappedData;
};
