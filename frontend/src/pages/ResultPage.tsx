import React, { useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Lightbulb,
  Target,
  Sparkles,
  Calendar,
  MapPin,
  Clock,
  User,
  Sun,
  Moon,
} from "lucide-react";
import StandardReportDisplay from "../components/StandardReportDisplay";
import ZodiacAIReportDisplay from "../components/ZodiacAIReportDisplay";

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
    planets?: PlanetPosition[];
  };
  sections: ResultSection[];
}

interface StandardReportResponse {
  report: string;
  generated_at: string;
  chart_data: any;
}

interface PlanetPosition {
  name: string;
  sign: string;
  longitude: number;
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
    | "practical_recommendations"
    | "planet_positions";
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

const ResultHeader: React.FC<{ meta: AstrologyResultResponse["meta"] }> = ({
  meta,
}) => {
  const elementIcons = {
    Fire: "🔥",
    Earth: "🌿",
    Air: "🌬️",
    Water: "💧",
  };

  return (
    <div
      className={`result-header-box element-${meta.zodiac.element.toLowerCase()}`}
    >
      <div className="header-badge">
        <span className="element-icon">
          {elementIcons[meta.zodiac.element]}
        </span>
        <span className="chart-type">
          {meta.chartType === "with_birth_time"
            ? "Bản đồ đầy đủ"
            : "Bản đồ cơ bản"}
        </span>
      </div>

      <h1 className="header-title">Hồ Sơ Chiêm Tinh</h1>

      <div className="zodiac-info-grid">
        <div className="info-item">
          <label>Mặt Trời</label>
          <span>{meta.zodiac.sun}</span>
        </div>
        {meta.zodiac.moon && (
          <div className="info-item">
            <label>Mặt Trăng</label>
            <span>{meta.zodiac.moon}</span>
          </div>
        )}
        {meta.zodiac.rising && (
          <div className="info-item">
            <label>Cung Mọc</label>
            <span>{meta.zodiac.rising}</span>
          </div>
        )}
      </div>

      <div className="element-pill">Nguyên tố: {meta.zodiac.element}</div>

      <style>{`
        .result-header-box {
          padding: 40px;
          border-radius: var(--radius-lg);
          border: 1px solid var(--white-10);
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          position: relative;
          overflow: hidden;
          margin-bottom: 40px;
        }
        .element-fire { border-color: rgba(239, 68, 68, 0.3); background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), transparent); }
        .element-earth { border-color: rgba(22, 163, 74, 0.3); background: linear-gradient(135deg, rgba(22, 163, 74, 0.1), transparent); }
        .element-air { border-color: rgba(14, 165, 233, 0.3); background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), transparent); }
        .element-water { border-color: rgba(37, 99, 235, 0.3); background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), transparent); }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }
        .element-icon { font-size: 2rem; }
        .chart-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 2px;
          color: var(--white-40);
        }
        .header-title {
          font-size: 3rem;
          margin-bottom: 24px;
          color: white;
        }
        .zodiac-info-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 32px;
          margin-bottom: 24px;
        }
        .info-item label {
          display: block;
          font-size: 11px;
          color: var(--white-40);
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 4px;
        }
        .info-item span {
          font-size: 1.2rem;
          font-weight: 600;
          font-family: var(--font-display);
        }
        .element-pill {
          display: inline-block;
          padding: 6px 16px;
          background: var(--white-10);
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
        }
      `}</style>
    </div>
  );
};

const InsightItem: React.FC<{ insight: InsightBlock }> = ({ insight }) => {
  const getIcon = () => {
    switch (insight.type) {
      case "principle":
        return <Lightbulb className="icon-p" />;
      case "warning":
        return <AlertTriangle className="icon-w" />;
      case "action":
        return <Target className="icon-a" />;
      default:
        return <Sparkles className="icon-d" />;
    }
  };

  return (
    <div
      className={`insight-block type-${insight.type} emphasis-${insight.emphasis || "low"}`}
    >
      <div className="insight-icon-box">{getIcon()}</div>
      <div className="insight-content">
        <p>{insight.content}</p>
        {insight.emphasis === "high" && (
          <span className="tag-high">Quan trọng</span>
        )}
      </div>

      <style>{`
        .insight-block {
          display: flex;
          gap: 16px;
          padding: 16px;
          border-radius: var(--radius-md);
          margin-bottom: 12px;
          background: rgba(255, 255, 255, 0.02);
          transition: transform 0.2s ease;
        }
        .insight-block:hover {
          transform: translateX(4px);
          background: rgba(255, 255, 255, 0.04);
        }
        .type-principle { border-left: 3px solid var(--nebula-purple); font-style: italic; }
        .type-warning { border-left: 3px solid #f59e0b; background: rgba(245, 158, 11, 0.05); }
        .type-action { border: 1px solid var(--nebula-blue); background: rgba(59, 130, 246, 0.05); }
        
        .emphasis-high { background: rgba(255, 255, 255, 0.05); }
        .emphasis-medium { color: white; }

        .insight-icon-box { margin-top: 2px; }
        .icon-p { color: var(--nebula-purple); }
        .icon-w { color: #f59e0b; }
        .icon-a { color: var(--nebula-blue); }
        .icon-d { color: var(--white-40); }

        .tag-high {
          font-size: 10px;
          background: var(--white-10);
          padding: 2px 8px;
          border-radius: 10px;
          text-transform: uppercase;
          margin-top: 8px;
          display: inline-block;
        }
      `}</style>
    </div>
  );
};

// ==================== Astrology Chart Components ====================

const SIGN_COLORS: Record<string, string> = {
  Aries: "#ff4d4d",
  Taurus: "#4dff88",
  Gemini: "#ffff4d",
  Cancer: "#4db8ff",
  Leo: "#ff4d4d",
  Virgo: "#4dff88",
  Libra: "#ffff4d",
  Scorpio: "#4db8ff",
  Sagittarius: "#ff4d4d",
  Capricorn: "#4dff88",
  Aquarius: "#ffff4d",
  Pisces: "#4db8ff",
};

const ZODIAC_SIGNS = [
  { name: "Aries", element: "Fire" },
  { name: "Taurus", element: "Earth" },
  { name: "Gemini", element: "Air" },
  { name: "Cancer", element: "Water" },
  { name: "Leo", element: "Fire" },
  { name: "Virgo", element: "Earth" },
  { name: "Libra", element: "Air" },
  { name: "Scorpio", element: "Water" },
  { name: "Sagittarius", element: "Fire" },
  { name: "Capricorn", element: "Earth" },
  { name: "Aquarius", element: "Air" },
  { name: "Pisces", element: "Water" },
];

const ELEMENT_COLORS = {
  Fire: "#ff5f5f",
  Earth: "#82ca9d",
  Air: "#8884d8",
  Water: "#00d1ff",
};

const NatalChartSVG: React.FC<{ planets: PlanetPosition[] }> = ({
  planets,
}) => {
  const size = 600;
  const center = size / 2;
  const outerRadius = size * 0.45;
  const signRingRadius = size * 0.38;
  const innerRadius = size * 0.32;
  const planetRingRadius = size * 0.25;

  return (
    <div className="chart-svg-container glass-card premium-chart">
      <svg viewBox={`0 0 ${size} ${size}`} className="natal-svg">
        <defs>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          <radialGradient id="ringGradient">
            <stop offset="0%" stopColor="rgba(255,255,255,0.05)" />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>
        </defs>

        {/* Outer Decorative Ring */}
        <circle
          cx={center}
          cy={center}
          r={outerRadius}
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="1"
        />
        <circle
          cx={center}
          cy={center}
          r={signRingRadius}
          fill="none"
          stroke="rgba(255,255,255,0.2)"
          strokeWidth="2"
        />

        {/* Zodiac Signs Segments */}
        {ZODIAC_SIGNS.map((sign, i) => {
          const startAngle = i * 30 - 180;
          const endAngle = (i + 1) * 30 - 180;
          const midAngle = (startAngle + endAngle) / 2;

          const x1 =
            center + outerRadius * Math.cos((startAngle * Math.PI) / 180);
          const y1 =
            center + outerRadius * Math.sin((startAngle * Math.PI) / 180);
          const x2 =
            center + outerRadius * Math.cos((endAngle * Math.PI) / 180);
          const y2 =
            center + outerRadius * Math.sin((endAngle * Math.PI) / 180);

          const tx =
            center +
            (signRingRadius + 18) * Math.cos((midAngle * Math.PI) / 180);
          const ty =
            center +
            (signRingRadius + 18) * Math.sin((midAngle * Math.PI) / 180);

          return (
            <g key={i}>
              <path
                d={`M ${center + innerRadius * Math.cos((startAngle * Math.PI) / 180)} ${center + innerRadius * Math.sin((startAngle * Math.PI) / 180)} 
                   L ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 0 1 ${x2} ${y2} 
                   L ${center + innerRadius * Math.cos((endAngle * Math.PI) / 180)} ${center + innerRadius * Math.sin((endAngle * Math.PI) / 180)} Z`}
                fill={i % 2 === 0 ? "rgba(255,255,255,0.02)" : "transparent"}
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="1"
              />
              <text
                x={tx}
                y={ty}
                className="sign-text"
                fill={
                  ELEMENT_COLORS[sign.element as keyof typeof ELEMENT_COLORS]
                }
                fontSize="11"
                fontWeight="700"
                textAnchor="middle"
                alignmentBaseline="middle"
                transform={`rotate(${midAngle + 90}, ${tx}, ${ty})`}
              >
                {sign.name.toUpperCase()}
              </text>
            </g>
          );
        })}

        {/* Aspect Lines (Placeholder logic for visual richness) */}
        {planets.slice(0, 6).map((p1, i) =>
          planets.slice(i + 1, 8).map((p2, j) => {
            const angle1 = p1.longitude - 180;
            const angle2 = p2.longitude - 180;
            if (
              Math.abs(angle1 - angle2) < 30 ||
              Math.abs(angle1 - angle2) > 150
            )
              return null;

            return (
              <line
                key={`${i}-${j}`}
                x1={
                  center +
                  innerRadius * 0.8 * Math.cos((angle1 * Math.PI) / 180)
                }
                y1={
                  center +
                  innerRadius * 0.8 * Math.sin((angle1 * Math.PI) / 180)
                }
                x2={
                  center +
                  innerRadius * 0.8 * Math.cos((angle2 * Math.PI) / 180)
                }
                y2={
                  center +
                  innerRadius * 0.8 * Math.sin((angle2 * Math.PI) / 180)
                }
                stroke="rgba(139, 92, 246, 0.15)"
                strokeWidth="1"
              />
            );
          }),
        )}

        {/* Planet Markers */}
        {planets.map((planet, idx) => {
          const angle = planet.longitude - 180;
          const px =
            center + planetRingRadius * Math.cos((angle * Math.PI) / 180);
          const py =
            center + planetRingRadius * Math.sin((angle * Math.PI) / 180);

          const lx =
            center + innerRadius * 0.9 * Math.cos((angle * Math.PI) / 180);
          const ly =
            center + innerRadius * 0.9 * Math.sin((angle * Math.PI) / 180);

          return (
            <g key={idx} className="planet-group">
              <line
                x1={px}
                y1={py}
                x2={lx}
                y2={ly}
                stroke="rgba(255,255,255,0.2)"
                strokeWidth="0.5"
              />
              <circle
                cx={px}
                cy={py}
                r="4"
                fill="var(--nebula-purple)"
                filter="url(#glow)"
              />
              <text
                x={lx}
                y={ly}
                className="planet-name-label"
                textAnchor={
                  Math.cos((angle * Math.PI) / 180) > 0 ? "start" : "end"
                }
                alignmentBaseline="middle"
                fontSize="12"
                fill="white"
                dx={Math.cos((angle * Math.PI) / 180) > 0 ? 8 : -8}
              >
                {planet.name}
              </text>
            </g>
          );
        })}

        {/* Center Void Decoration */}
        <circle
          cx={center}
          cy={center}
          r={planetRingRadius * 0.8}
          fill="rgba(0,0,0,0.3)"
          stroke="rgba(255,255,255,0.05)"
        />
        <path
          d={`M ${center - 20} ${center} L ${center + 20} ${center} M ${center} ${center - 20} L ${center} ${center + 20}`}
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="1"
        />
      </svg>

      <style>{`
        .premium-chart {
          padding: 40px !important;
          max-width: 700px !important;
          margin-bottom: 60px !important;
          background: radial-gradient(circle at center, rgba(139, 92, 246, 0.05) 0%, transparent 70%);
        }
        .natal-svg {
          filter: drop-shadow(0 0 20px rgba(0,0,0,0.5));
        }
        .sign-text {
          font-family: var(--font-display);
          letter-spacing: 1px;
          opacity: 0.8;
        }
        .planet-name-label {
          font-family: var(--font-display);
          font-weight: 500;
          pointer-events: none;
        }
        .planet-group:hover circle {
          fill: var(--gold-primary);
          r: 6;
          transition: all 0.3s ease;
        }
      `}</style>
    </div>
  );
};

const PlanetPositionsList: React.FC<{ planets: PlanetPosition[] }> = ({
  planets,
}) => {
  return (
    <div className="planet-list-container glass-card">
      <h2 className="section-card-title mb-4">Vị trí các hành tinh</h2>
      <div className="table-responsive">
        <table className="planet-table">
          <thead>
            <tr>
              <th>Hành tinh</th>
              <th>Cung</th>
              <th>Kinh độ</th>
            </tr>
          </thead>
          <tbody>
            {planets.map((planet, idx) => (
              <tr key={idx}>
                <td className="planet-name">{planet.name}</td>
                <td>
                  <span
                    className="sign-badge"
                    style={{ color: SIGN_COLORS[planet.sign] }}
                  >
                    {planet.sign}
                  </span>
                </td>
                <td className="longitude-val">
                  {planet.longitude.toFixed(2)}°
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <style>{`
        .planet-list-container {
          margin-bottom: 40px;
          padding: 32px;
        }
        .planet-table {
          width: 100%;
          border-collapse: collapse;
        }
        .planet-table th {
          text-align: left;
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: var(--white-40);
          padding: 12px;
          border-bottom: 1px solid var(--white-10);
        }
        .planet-table td {
          padding: 12px;
          border-bottom: 1px solid var(--white-05);
        }
        .planet-name {
          font-weight: 600;
          color: var(--gold-primary);
        }
        .sign-badge {
          font-size: 13px;
          font-weight: 500;
        }
        .longitude-val {
          color: var(--white-40);
          font-size: 13px;
          font-family: monospace;
        }
      `}</style>
    </div>
  );
};

const SectionCard: React.FC<{
  section: ResultSection;
  defaultExpanded?: boolean;
}> = ({ section, defaultExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div
      className={`section-collapse glass-card ${isExpanded ? "is-open" : ""}`}
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="section-trigger"
      >
        <div className="trigger-text">
          <h2 className="section-card-title">{section.title_i18n}</h2>
          <p className="section-summary">{section.summary}</p>
        </div>
        <div className="trigger-icon">
          {isExpanded ? <ChevronUp /> : <ChevronDown />}
        </div>
      </button>

      {isExpanded && (
        <div className="section-content-area">
          {section.insights.map((insight, idx) => (
            <InsightItem key={idx} insight={insight} />
          ))}
        </div>
      )}

      <style>{`
        .section-collapse {
          margin-bottom: 20px;
          padding: 0 !important;
          overflow: hidden;
        }
        .section-trigger {
          width: 100%;
          background: transparent;
          border: none;
          padding: 24px 32px;
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
          text-align: left;
        }
        .section-trigger:hover {
          background: rgba(255, 255, 255, 0.02);
        }
        .section-card-title {
          font-size: 1.5rem;
          margin-bottom: 4px;
          color: var(--gold-primary);
        }
        .section-summary {
          font-size: 14px;
          color: var(--white-40);
        }
        .trigger-icon { color: var(--white-40); }
        .section-content-area {
          padding: 0 32px 32px 32px;
          border-top: 1px solid var(--white-10);
          animation: slideDown 0.3s ease-out;
        }
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

// Centralized response mapping function
const mapCompatibilityResponse = (responseData: any) => {
  // Handle nested structure: responseData.details contains the actual compatibility data
  const details = responseData?.details || responseData;

  return {
    score: details?.score || 0,
    summary: details?.summary || "Phân tích tương hợp",
    personality: details?.personality || "Chưa có thông tin",
    love_style: details?.love_style || "Chưa có thông tin",
    career: details?.career || "Chưa có thông tin",
    relationships: details?.relationships || "Chưa có thông tin",
    advice: details?.advice || "Chưa có thông tin",
    conflict_points: details?.conflict_points || "Chưa có thông tin",
    recommended_activities: details?.recommended_activities || [],
    aspects: details?.aspects || [],
    ai_analysis: details?.ai_analysis,
    detailed_reasoning: details?.detailed_reasoning,
  };
};

import { useCompatibilityStore } from "../store/useCompatibilityStore";

const SAMPLE_PLANETS: PlanetPosition[] = [
  { name: "Mặt Trời", sign: "Libra", longitude: 189.78 },
  { name: "Mặt Trăng", sign: "Libra", longitude: 203.5 },
  { name: "Sao Thủy", sign: "Libra", longitude: 181.3 },
  { name: "Sao Kim", sign: "Scorpio", longitude: 233.94 },
  { name: "Sao Hỏa", sign: "Sagittarius", longitude: 242.82 },
  { name: "Sao Mộc", sign: "Aquarius", longitude: 312.14 },
  { name: "Sao Thổ", sign: "Aries", longitude: 17.48 },
  { name: "Thiên Vương", sign: "Aquarius", longitude: 304.79 },
  { name: "Hải Vương", sign: "Capricorn", longitude: 297.19 },
  { name: "Diêm Vương", sign: "Sagittarius", longitude: 243.52 },
  { name: "Nút Bắc", sign: "Virgo", longitude: 168.49 },
  { name: "Chiron", sign: "Scorpio", longitude: 213.69 },
];

const ResultPage: React.FC = () => {
  const data = useCompatibilityStore((state) => state.result);
  const resultType = useCompatibilityStore((state) => state.resultType);
  const reset = useCompatibilityStore((state) => state.reset);

  if (!data) return null;

  // Handle compatibility results
  if (
    resultType === "compatibility" ||
    !data.sections ||
    !Array.isArray(data.sections)
  ) {
    // Extract compatibility data
    const compatibilityData =
      typeof data === "string" ? JSON.parse(data) : data;

    console.log(
      "🔍 Raw compatibility data in ResultPage:",
      JSON.stringify(compatibilityData, null, 2),
    );

    // Map the actual response schema to frontend expectations
    const mappedData = mapCompatibilityResponse(compatibilityData);

    // Extract all available data from the mapped response
    const score = mappedData.score || 0;
    const isCompatible = score >= 50;
    const summary = mappedData.summary || "Phân tích tương hợp";
    const personality = mappedData.personality || "Chưa có thông tin";
    const loveStyle = mappedData.love_style || "Chưa có thông tin";
    const career = mappedData.career || "Chưa có thông tin";
    const relationships = mappedData.relationships || "Chưa có thông tin";
    const advice = mappedData.advice || "Chưa có thông tin";
    const conflictPoints = mappedData.conflict_points || "Chưa có thông tin";
    const recommendedActivities = mappedData.recommended_activities || [];
    const aspects = mappedData.aspects || [];

    // Extract AI analysis if available
    const aiAnalysis = mappedData.ai_analysis;
    const detailedReasoning = mappedData.detailed_reasoning;

    return (
      <div className="container section-py">
        <button className="btn-back" onClick={reset}>
          ← Quay lại
        </button>

        <div className="compatibility-result-box">
          <div className="compatibility-header">
            <h1 className="title-gradient">TƯƠNG HỢP HAI NGƯỜI</h1>
            <div className="compatibility-score">
              <div className="score-circle">
                <span className="score-number">{Math.round(score)}%</span>
                <span className="score-label">Độ hợp nhau</span>
              </div>
            </div>
          </div>

          <div className="compatibility-result">
            <div
              className={`result-badge ${isCompatible ? "compatible" : "not-compatible"}`}
            >
              {isCompatible ? "HỢP NHAU" : "KHÔNG HỢP"}
            </div>

            <div className="compatibility-summary">
              <h3>📊 Tổng Quan</h3>
              <p>{summary}</p>
            </div>

            <div className="compatibility-sections">
              <div className="section-card">
                <h4>👥 Tính Cách</h4>
                <p>{personality}</p>
              </div>

              <div className="section-card">
                <h4>💖 Phong Cách Yêu</h4>
                <p>{loveStyle}</p>
              </div>

              <div className="section-card">
                <h4>💼 Hợp Tác Công Việc</h4>
                <p>{career}</p>
              </div>

              <div className="section-card">
                <h4>🤝 Động Lực Mối Quan Hệ</h4>
                <p>{relationships}</p>
              </div>
            </div>

            <div className="compatibility-details">
              <div className="detail-card">
                <h4>💡 Lời Khuyên</h4>
                <p>{advice}</p>
              </div>

              <div className="detail-card">
                <h4>⚠️ Điểm Xung Đột</h4>
                <p>{conflictPoints}</p>
              </div>
            </div>

            {recommendedActivities.length > 0 && (
              <div className="activities-section">
                <h4>🎯 Hoạt Động Khuyến Nghị</h4>
                <ul>
                  {recommendedActivities.map(
                    (activity: string, idx: number) => (
                      <li key={idx}>{activity}</li>
                    ),
                  )}
                </ul>
              </div>
            )}

            {aspects.length > 0 && (
              <div className="aspects-section">
                <h4>🌟 Các Mặt Trời</h4>
                <div className="aspects-list">
                  {aspects.map((aspect: string, idx: number) => (
                    <div key={idx} className="aspect-item">
                      {aspect}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {aiAnalysis && (
              <div className="ai-analysis-box">
                <h3>🤖 Phân tích AI Tối Ưu</h3>
                <div className="ai-analysis-content">
                  {aiAnalysis.split("\n").map((line: string, idx: number) => (
                    <p key={idx} className="ai-analysis-line">
                      {line}
                    </p>
                  ))}
                </div>
              </div>
            )}

            {detailedReasoning && (
              <div className="detailed-reasoning-box">
                <h3>🔍 Lý Do Chi Tiết</h3>
                <div className="reasoning-content">
                  {detailedReasoning
                    .split("\n")
                    .map((line: string, idx: number) => (
                      <p key={idx} className="reasoning-line">
                        {line}
                      </p>
                    ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <style>{`
          .compatibility-result-box {
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid var(--white-10);
            border-radius: var(--radius-lg);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
          }
          
          .compatibility-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
          }
          
          .title-gradient {
            font-size: 2.5rem;
            margin: 0;
            background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
          
          .compatibility-score {
            display: flex;
            justify-content: center;
            align-items: center;
          }
          
          .score-circle {
            width: 120px;
            height: 120px;
            border: 4px solid var(--white-20);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
          }
          
          .score-circle::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border: 4px solid transparent;
            border-top-color: var(--nebula-purple);
            border-radius: 50%;
            animation: rotate 2s linear infinite;
            opacity: 0.5;
          }
          
          .score-number {
            font-size: 2rem;
            font-weight: 800;
            color: white;
            z-index: 1;
          }
          
          .score-label {
            font-size: 0.8rem;
            color: var(--white-40);
            text-transform: uppercase;
            z-index: 1;
          }
          
          .compatibility-result {
            display: flex;
            flex-direction: column;
            gap: 24px;
          }
          
          .result-badge {
            font-size: 1.5rem;
            font-weight: 800;
            padding: 12px 24px;
            border-radius: 30px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: 2px solid var(--white-20);
          }
          
          .compatible {
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
            border-color: #22c55e;
          }
          
          .not-compatible {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border-color: #ef4444;
          }
          
          .compatibility-summary {
            background: rgba(255,255,255,0.02);
            padding: 20px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-purple);
          }
          
          .compatibility-summary h3 {
            margin: 0 0 10px 0;
            color: var(--white-70);
            font-size: 1.1rem;
          }
          
          .compatibility-summary p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
          }

          .compatibility-sections {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
          }

          .section-card {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border: 1px solid var(--white-10);
          }

          .section-card h4 {
            margin: 0 0 8px 0;
            color: var(--nebula-purple);
            font-size: 1rem;
          }

          .section-card p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .compatibility-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
          }

          .detail-card {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-blue);
          }

          .detail-card h4 {
            margin: 0 0 8px 0;
            color: var(--nebula-blue);
            font-size: 1rem;
          }

          .detail-card p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .activities-section {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--gold-primary);
          }

          .activities-section h4 {
            margin: 0 0 12px 0;
            color: var(--gold-primary);
            font-size: 1rem;
          }

          .activities-section ul {
            margin: 0;
            padding-left: 20px;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .activities-section li {
            margin-bottom: 4px;
          }

          .aspects-section {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-pink);
          }

          .aspects-section h4 {
            margin: 0 0 12px 0;
            color: var(--nebula-pink);
            font-size: 1rem;
          }

          .aspects-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 8px;
          }

          .aspect-item {
            background: rgba(255,255,255,0.02);
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--white-40);
            font-size: 0.9rem;
          }

          @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          
          @media (max-width: 768px) {
            .compatibility-header {
              flex-direction: column;
              align-items: flex-start;
            }
            .score-circle {
              width: 100px;
              height: 100px;
            }
            .score-number {
              font-size: 1.5rem;
            }
            .compatibility-sections {
              grid-template-columns: 1fr;
            }
            .compatibility-details {
              grid-template-columns: 1fr;
            }
          }

          .ai-analysis-box {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid var(--nebula-purple);
          }

          .ai-analysis-box h3 {
            margin: 0 0 12px 0;
            color: var(--nebula-purple);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .ai-analysis-content {
            background: rgba(255, 255, 255, 0.02);
            padding: 16px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255, 255, 255, 0.1);
          }

          .ai-analysis-line {
            margin: 8px 0;
            color: var(--white-40);
            line-height: 1.6;
            font-style: italic;
          }

          .detailed-reasoning-box {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid var(--nebula-blue);
          }

          .detailed-reasoning-box h3 {
            margin: 0 0 12px 0;
            color: var(--nebula-blue);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .reasoning-content {
            background: rgba(255, 255, 255, 0.02);
            padding: 16px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255, 255, 255, 0.1);
          }

          .reasoning-line {
            margin: 8px 0;
            color: var(--white-40);
            line-height: 1.6;
          }
        `}</style>
      </div>
    );
  }

  // Handle Zodiac AI reports
  if (resultType === "zodiac_ai" && data.report) {
    const zodiacAIdata = data as any;
    return (
      <div className="container section-py">
        <button className="btn-back" onClick={reset}>
          ← TRỞ VỀ TRANG CHỦ
        </button>

        <ZodiacAIReportDisplay
          report={zodiacAIdata.report}
          chartData={zodiacAIdata.chart_data}
          generatedAt={zodiacAIdata.generated_at}
          placements={zodiacAIdata.placements}
        />
      </div>
    );
  }

  // Handle standard format reports
  if (resultType === "standard" && data.report) {
    const standardData = data as StandardReportResponse;
    return (
      <div className="container section-py">
        <button className="btn-back" onClick={reset}>
          ← TRỞ VỀ TRANG CHỦ
        </button>

        <StandardReportDisplay
          report={standardData.report}
          chartData={standardData.chart_data}
          generatedAt={standardData.generated_at}
        />
      </div>
    );
  }

  // Handle traditional astrology results
  const typedData = data as AstrologyResultResponse;
  const planets = typedData.meta.planets || SAMPLE_PLANETS;

  return (
    <div className="container section-py">
      <button className="btn-back" onClick={reset}>
        ← TRỞ VỀ TRANG CHỦ
      </button>

      <ResultHeader meta={typedData.meta} />

      <div className="chart-grid">
        <NatalChartSVG planets={planets} />
        <PlanetPositionsList planets={planets} />
      </div>

      <div className="result-footer">
        <p>
          Phân tích dựa trên{" "}
          {typedData.meta.chartType === "with_birth_time"
            ? "thông tin đầy đủ"
            : "thông tin cơ bản"}
          . Kết quả mang tính tham khảo và phản ánh xu hướng năng lượng chiêm
          tinh.
        </p>
      </div>

      <style>{`
        .btn-back {
          background: none;
          border: none;
          color: var(--white-40);
          cursor: pointer;
          margin-bottom: 40px;
          letter-spacing: 2px;
          font-weight: 700;
          font-family: var(--font-display);
          transition: color 0.3s;
        }
        .btn-back:hover { color: var(--nebula-pink); }
        .chart-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 30px;
          margin-bottom: 40px;
        }
        @media (max-width: 992px) {
          .chart-grid { grid-template-columns: 1fr; }
        }
        .sections-container {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .result-footer {
          margin-top: 60px;
          text-align: center;
          padding: 40px;
          border-top: 1px solid var(--white-10);
        }
        .result-footer p {
          color: var(--white-40);
          font-size: 13px;
          max-width: 600px;
          margin: 0 auto;
        }
      `}</style>
    </div>
  );
};

export default ResultPage;
