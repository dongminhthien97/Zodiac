export interface MappedCompatibilityResponse {
  score: number;
  summary: string;
  personality: string;
  loveStyle: string;
  career: string;
  relationships: string;
  advice: string;
  conflictPoints: string;
  recommendedActivities: string[];
  aspects: string[];
  aiAnalysis?: string;
  detailedReasoning?: string;
}

export function mapCompatibilityResponse(response: any): MappedCompatibilityResponse {
  // Handle nested structure: response.details contains the actual compatibility data
  const details = response?.details || response;

  const mappedData: MappedCompatibilityResponse = {
    score: details?.score || 0,
    summary: details?.summary || '',
    personality: details?.personality || '',
    loveStyle: details?.love_style || '',
    career: details?.career || '',
    relationships: details?.relationships || '',
    advice: details?.advice || '',
    conflictPoints: details?.conflict_points || '',
    recommendedActivities: details?.recommended_activities || [],
    aspects: details?.aspects || [],
  };

  // Add optional fields if they exist
  if (details?.ai_analysis) {
    mappedData.aiAnalysis = details.ai_analysis;
  }

  if (details?.detailed_reasoning) {
    mappedData.detailedReasoning = details.detailed_reasoning;
  }

  // Log missing fields for debugging
  const requiredFields = [
    'score', 'summary', 'personality', 'love_style', 'career', 
    'relationships', 'advice', 'conflict_points'
  ];

  requiredFields.forEach(field => {
    if (!details[field]) {
      console.warn(`Missing field in compatibility response: ${field}`);
    }
  });

  return mappedData;
}