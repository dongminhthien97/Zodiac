import React, { useState } from 'react';
import { ChevronDown, ChevronUp, AlertTriangle, Lightbulb, Target, Sparkles } from 'lucide-react';

// ==================== Type Definitions ====================

interface AstrologyResultResponse {
  meta: {
    version: "v2";
    locale: "vi" | "en";
    chartType: "with_birth_time" | "without_birth_time";
    zodiac: {
      sun: string;
      moon?: string;
      rising?: string;
      element: "Fire" | "Earth" | "Air" | "Water";
    };
  };
  sections: ResultSection[];
}

interface ResultSection {
  id:
    | "energy_overview"
    | "core_personality"
    | "love_connection"
    | "hobbies"
    | "career_direction"
    | "life_direction"
    | "strengths"
    | "challenges"
    | "growth_suggestions"
    | "practical_recommendations";
  title_i18n: string;
  summary: string;
  insights: InsightBlock[];
}

interface InsightBlock {
  type: "description" | "principle" | "warning" | "action";
  content: string;
  emphasis?: "low" | "medium" | "high";
}

// ==================== Components ====================

const ResultHeader: React.FC<{ meta: AstrologyResultResponse['meta'] }> = ({ meta }) => {
  const elementColors = {
    Fire: 'from-red-500/20 to-orange-500/20 border-red-500/30',
    Earth: 'from-green-600/20 to-emerald-600/20 border-green-600/30',
    Air: 'from-sky-500/20 to-cyan-500/20 border-sky-500/30',
    Water: 'from-blue-600/20 to-indigo-600/20 border-blue-600/30',
  };

  const elementIcons = {
    Fire: '🔥',
    Earth: '🌿',
    Air: '🌬️',
    Water: '💧',
  };

  return (
    <div className={`rounded-2xl border bg-gradient-to-br p-6 md:p-8 ${elementColors[meta.zodiac.element]}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="mb-2 flex items-center gap-2">
            <span className="text-3xl">{elementIcons[meta.zodiac.element]}</span>
            <span className="text-sm font-medium uppercase tracking-wider text-white/70">
              {meta.chartType === 'with_birth_time' ? 'Bản đồ đầy đủ' : 'Bản đồ cơ bản'}
            </span>
          </div>
          <h1 className="mb-4 font-display text-3xl font-bold text-white md:text-4xl">
            Hồ Sơ Chiêm Tinh
          </h1>
          <div className="space-y-2">
            <div className="flex flex-wrap gap-x-6 gap-y-2 text-white/90">
              <div>
                <span className="text-sm text-white/60">Mặt Trời:</span>{' '}
                <span className="font-semibold">{meta.zodiac.sun}</span>
              </div>
              {meta.zodiac.moon && (
                <div>
                  <span className="text-sm text-white/60">Mặt Trăng:</span>{' '}
                  <span className="font-semibold">{meta.zodiac.moon}</span>
                </div>
              )}
              {meta.zodiac.rising && (
                <div>
                  <span className="text-sm text-white/60">Cung Mọc:</span>{' '}
                  <span className="font-semibold">{meta.zodiac.rising}</span>
                </div>
              )}
            </div>
            <div className="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1 text-sm font-medium text-white backdrop-blur-sm">
              Nguyên tố: {meta.zodiac.element}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const InsightItem: React.FC<{ insight: InsightBlock }> = ({ insight }) => {
  const getInsightStyle = () => {
    const base = 'flex gap-3 transition-all';
    let style = '';
    
    switch (insight.type) {
      case 'principle':
        style = 'bg-purple-500/5 border-l-4 border-purple-500/50 pl-4 italic';
        break;
      case 'warning':
        style = 'bg-amber-500/10 border-l-4 border-amber-500 pl-4';
        break;
      case 'action':
        style = 'bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-4 font-medium';
        break;
      default:
        style = 'text-white/80';
    }

    if (insight.emphasis === 'high') {
      style += ' ring-1 ring-white/20 shadow-lg shadow-white/5';
    } else if (insight.emphasis === 'medium') {
      style += ' text-white';
    }

    return `${base} ${style}`;
  };

  const getIcon = () => {
    switch (insight.type) {
      case 'principle':
        return <Lightbulb className="mt-1 h-4 w-4 shrink-0 text-purple-400" />;
      case 'warning':
        return <AlertTriangle className="mt-1 h-4 w-4 shrink-0 text-amber-500" />;
      case 'action':
        return <Target className="mt-1 h-4 w-4 shrink-0 text-emerald-400" />;
      default:
        return <Sparkles className="mt-1 h-4 w-4 shrink-0 text-sky-400" />;
    }
  };

  return (
    <div className={getInsightStyle()}>
      {getIcon()}
      <p className="leading-relaxed">
        {insight.content}
        {insight.emphasis === 'high' && (
          <span className="ml-2 inline-flex items-center rounded-full bg-white/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-tighter text-white">
            Quan trọng
          </span>
        )}
      </p>
    </div>
  );
};

const SectionCard: React.FC<{ section: ResultSection; defaultExpanded?: boolean }> = ({
  section,
  defaultExpanded = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className="overflow-hidden rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm transition-all hover:bg-white/[0.07]">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex w-full items-center justify-between gap-4 p-6 text-left transition-colors hover:bg-white/5"
        aria-expanded={isExpanded}
      >
        <div className="flex-1">
          <h2 className="mb-2 font-display text-xl font-bold text-white md:text-2xl">
            {section.title_i18n}
          </h2>
          <p className="text-sm text-white/60 md:text-base">{section.summary}</p>
        </div>
        <div className="text-white/50 transition-transform duration-200">
          {isExpanded ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
        </div>
      </button>

      <div
        className={`transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="space-y-4 border-t border-white/10 p-6 pt-4">
          {section.insights.map((insight, idx) => (
            <InsightItem key={idx} insight={insight} />
          ))}
        </div>
      </div>
    </div>
  );
};

import { useCompatibilityStore } from '../store/useCompatibilityStore';

// ==================== Main Component ====================

const ResultPage: React.FC = () => {
  const data = useCompatibilityStore((state) => state.result);
  const resultType = useCompatibilityStore((state) => state.resultType);
  const reset = useCompatibilityStore((state) => state.reset);

  if (!data) return null;

  // Generic render for compatibility or other non-V2 results
  if (resultType === 'compatibility' || !data.sections || !Array.isArray(data.sections)) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-8">
        <div className="mx-auto max-w-4xl">
          <button onClick={reset} className="mb-8 text-sm text-white/60 hover:text-white">← Quay lại</button>
          <h1 className="text-3xl font-bold mb-6">Kết quả tra cứu</h1>
          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <pre className="whitespace-pre-wrap text-sm text-white/70">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    );
  }

  const typedData = data as AstrologyResultResponse;

  return (
    <div className="min-h-screen bg-gradient-to-b from-ink-900 via-ink-800 to-ink-900 text-white">
      <div className="mx-auto max-w-4xl px-4 py-8 md:px-6 md:py-12">
        <button
          onClick={reset}
          className="mb-8 flex items-center gap-2 text-sm text-white/60 transition-colors hover:text-white"
        >
          <span className="text-lg">←</span> Quay lại
        </button>
        <ResultHeader meta={typedData.meta} />

        <div className="mt-8 space-y-4 md:mt-12">
          {typedData.sections.map((section: ResultSection, index: number) => (
            <SectionCard key={section.id || index} section={section} defaultExpanded={index === 0} />
          ))}
        </div>

        <div className="mt-12 rounded-xl border border-white/10 bg-white/5 p-6 text-center">
          <p className="text-sm text-white/60">
            Phân tích dựa trên {typedData.meta.chartType === 'with_birth_time' ? 'thông tin đầy đủ bao gồm giờ sinh' : 'thông tin cơ bản không bao gồm giờ sinh'}.
            Kết quả mang tính tham khảo và phản ánh xu hướng năng lượng, không phải định mệnh cố định.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
