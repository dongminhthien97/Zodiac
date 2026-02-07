export interface MappedZodiacAIReportResponse {
  report: string;
  generatedAt: string;
  chartData: any;
  placements?: any;
}

export function mapZodiacAIReportResponse(response: any): MappedZodiacAIReportResponse {
  return {
    report: response?.report || '',
    generatedAt: response?.generated_at || '',
    chartData: response?.chart_data || null,
    placements: response?.placements || null,
  };
}