export interface MappedAstrologyResultResponse {
  meta: {
    version: string;
    locale: string;
    chartType: string;
    zodiac: {
      sun: string;
      moon?: string;
      rising?: string;
      element: string;
    };
    planets?: any[];
  };
  sections: any[];
}

export function mapAstrologyResultResponse(response: any): MappedAstrologyResultResponse {
  return {
    meta: response?.meta || {
      version: 'v2',
      locale: 'vi',
      chartType: 'with_birth_time',
      zodiac: {
        sun: '',
        moon: '',
        rising: '',
        element: '',
      },
      planets: [],
    },
    sections: response?.sections || [],
  };
}