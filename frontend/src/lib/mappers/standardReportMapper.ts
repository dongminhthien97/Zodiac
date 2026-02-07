export interface MappedStandardReportResponse {
  report: string;
  generatedAt: string;
  chartData: any;
}

export function mapStandardReportResponse(response: any): MappedStandardReportResponse {
  return {
    report: response?.report || '',
    generatedAt: response?.generated_at || '',
    chartData: response?.chart_data || null,
  };
}