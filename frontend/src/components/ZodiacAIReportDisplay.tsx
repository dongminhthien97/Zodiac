import React from "react";

interface ZodiacAIReportDisplayProps {
  report: string;
  chartData: any;
  generatedAt: string;
  placements: any[];
}

const ZodiacAIReportDisplay: React.FC<ZodiacAIReportDisplayProps> = ({
  report,
  chartData,
  generatedAt,
  placements,
}) => {
  // Parse the Zodiac AI report into structured sections
  const parseZodiacAIReport = (reportText: string) => {
    const sections = [];
    const lines = reportText.split("\n");
    let currentSection: any = null;
    let currentContent: string[] = [];
    let inSection = false;

    for (const line of lines) {
      const trimmedLine = line.trim();

      // Check if this is a section header (starts with number and period)
      const sectionMatch = trimmedLine.match(/^(\d+)\.\s+(.+)$/);
      if (sectionMatch) {
        // Save previous section
        if (currentSection) {
          currentSection.content = currentContent;
          sections.push(currentSection);
        }

        // Start new section
        currentSection = {
          id: sectionMatch[1],
          title: sectionMatch[2],
          content: [],
        };
        currentContent = [];
        inSection = true;
      } else if (inSection && currentSection) {
        // Add content to current section
        if (trimmedLine) {
          currentContent.push(trimmedLine);
        }
      }
    }

    // Save the last section
    if (currentSection) {
      currentSection.content = currentContent;
      sections.push(currentSection);
    }

    return sections;
  };

  const sections = parseZodiacAIReport(report);

  const getSectionIcon = (title: string) => {
    if (title.includes("Tổng quan")) return "📊";
    if (title.includes("Nhân dạng")) return "👤";
    if (title.includes("Tình yêu")) return "❤️";
    if (title.includes("Thế hệ")) return "🌍";
    if (title.includes("Bài học")) return "🎓";
    if (title.includes("Kết luận")) return "🎯";
    return "📄";
  };

  const getSectionColor = (title: string) => {
    if (title.includes("Tổng quan")) return "#3b82f6";
    if (title.includes("Nhân dạng")) return "#10b981";
    if (title.includes("Tình yêu")) return "#ef4444";
    if (title.includes("Thế hệ")) return "#8b5cf6";
    if (title.includes("Bài học")) return "#f59e0b";
    if (title.includes("Kết luận")) return "#06b6d4";
    return "#6b7280";
  };

  return (
    <div className="zodiac-ai-container">
      {/* Header */}
      <div className="zodiac-ai-header">
        <div className="header-badge">
          <span className="ai-icon">🤖</span>
          <span className="ai-type">ZODIAC AI PROFESSIONAL</span>
        </div>

        <h1 className="ai-title">BÁO CÁO CHIẾM TINH CHUYÊN NGHIỆP</h1>

        <div className="ai-chart-info">
          <div className="info-grid">
            <div className="info-item">
              <label>Mặt Trời</label>
              <span>{chartData?.Sun?.sign || "Unknown"}</span>
            </div>
            <div className="info-item">
              <label>Mặt Trăng</label>
              <span>{chartData?.Moon?.sign || "Unknown"}</span>
            </div>
            <div className="info-item">
              <label>Sao Kim</label>
              <span>{chartData?.Venus?.sign || "Unknown"}</span>
            </div>
            <div className="info-item">
              <label>Sao Hỏa</label>
              <span>{chartData?.Mars?.sign || "Unknown"}</span>
            </div>
          </div>
        </div>

        <div className="ai-generated-info">
          <span className="generated-text">
            Generated: {new Date(generatedAt).toLocaleString("vi-VN")}
          </span>
        </div>
      </div>

      {/* Report Content */}
      <div className="zodiac-ai-content">
        {sections.map((section, index) => (
          <div
            key={index}
            className="ai-section"
            style={{ borderColor: getSectionColor(section.title) }}
          >
            <div
              className="ai-section-header"
              style={{ backgroundColor: getSectionColor(section.title) }}
            >
              <div className="section-title-wrapper">
                <span className="section-icon">
                  {getSectionIcon(section.title)}
                </span>
                <h2 className="ai-section-title">{section.title}</h2>
              </div>
              <div className="section-number">Phần {section.id}</div>
            </div>

            <div className="ai-section-content">
              {section.content.map((line: string, lineIndex: number) => {
                // Handle different line types
                if (
                  line.startsWith("☉") ||
                  line.startsWith("☽") ||
                  line.startsWith("☿") ||
                  line.startsWith("♀") ||
                  line.startsWith("♂") ||
                  line.startsWith("☊") ||
                  line.startsWith("⚷")
                ) {
                  return (
                    <div key={lineIndex} className="ai-planet-header">
                      <span className="ai-planet-symbol">
                        {line.split(" ")[0]}
                      </span>
                      <span className="ai-planet-text">
                        {line.substring(line.indexOf(" ") + 1)}
                      </span>
                    </div>
                  );
                } else if (line.startsWith("**") && line.endsWith("**")) {
                  // Bold headers
                  const content = line.slice(2, -2);
                  return (
                    <div key={lineIndex} className="ai-bold-header">
                      {content}
                    </div>
                  );
                } else if (line.startsWith("⚠️")) {
                  return (
                    <div key={lineIndex} className="ai-warning-block">
                      <span className="ai-warning-icon">⚠️</span>
                      <span className="ai-warning-text">
                        {line.substring(2)}
                      </span>
                    </div>
                  );
                } else if (line.startsWith("👉")) {
                  return (
                    <div key={lineIndex} className="ai-insight-block">
                      <span className="ai-insight-icon">👉</span>
                      <span className="ai-insight-text">
                        {line.substring(2)}
                      </span>
                    </div>
                  );
                } else if (line.startsWith("-")) {
                  return (
                    <div key={lineIndex} className="ai-bullet-point">
                      <span className="ai-bullet">•</span>
                      <span className="ai-bullet-text">
                        {line.substring(2)}
                      </span>
                    </div>
                  );
                } else if (line.includes("→")) {
                  return (
                    <div key={lineIndex} className="ai-formula-block">
                      <span className="ai-formula-text">{line}</span>
                    </div>
                  );
                } else if (line.includes(":")) {
                  // Key-value pairs
                  const [key, ...valueParts] = line.split(":");
                  const value = valueParts.join(":");
                  return (
                    <div key={lineIndex} className="ai-key-value">
                      <span className="ai-key">{key}:</span>
                      <span className="ai-value">{value}</span>
                    </div>
                  );
                } else {
                  return (
                    <div key={lineIndex} className="ai-normal-line">
                      {line}
                    </div>
                  );
                }
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="zodiac-ai-footer">
        <p className="ai-footer-note">
          Báo cáo được tạo bởi hệ thống Zodiac AI chuyên nghiệp. Kết quả mang
          tính chất tham khảo và phản ánh xu hướng năng lượng chiêm tinh.
        </p>
        <div className="ai-footer-actions">
          <button className="btn-secondary" onClick={() => window.print()}>
            In Báo Cáo
          </button>
          <button
            className="btn-secondary"
            onClick={() => {
              navigator.clipboard.writeText(report);
            }}
          >
            Sao Chép
          </button>
        </div>
      </div>

      <style>{`
        .zodiac-ai-container {
          max-width: 900px;
          margin: 0 auto;
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          border: 2px solid rgba(255,255,255,0.1);
          border-radius: 20px;
          padding: 40px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #ffffff;
          box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }

        .zodiac-ai-header {
          border-bottom: 2px solid rgba(255,255,255,0.1);
          padding-bottom: 30px;
          margin-bottom: 40px;
        }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .ai-icon {
          font-size: 2.5rem;
          filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        }

        .ai-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 3px;
          color: #94a3b8;
          font-weight: 800;
          background: linear-gradient(135deg, #ffffff, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .ai-title {
          font-size: 3rem;
          margin-bottom: 24px;
          background: linear-gradient(to right, #ffffff, #9333ea, #f59e0b);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          font-family: 'Georgia', serif;
          font-weight: 800;
          text-shadow: 0 4px 20px rgba(147, 51, 234, 0.3);
        }

        .ai-chart-info {
          margin-bottom: 20px;
        }

        .info-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
        }

        .info-item {
          background: rgba(255,255,255,0.05);
          padding: 16px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.1);
          text-align: center;
        }

        .info-item label {
          font-size: 11px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 8px;
          display: block;
        }

        .info-item span {
          font-size: 1.5rem;
          font-weight: 700;
          color: #ffffff;
          font-family: 'Georgia', serif;
        }

        .ai-generated-info {
          background: rgba(255,255,255,0.05);
          padding: 12px 20px;
          border-radius: 25px;
          display: inline-block;
          border: 1px solid rgba(255,255,255,0.2);
        }

        .ai-generated-text {
          font-size: 12px;
          color: #94a3b8;
        }

        .zodiac-ai-content {
          margin-bottom: 40px;
        }

        .ai-section {
          margin-bottom: 30px;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0,0,0,0.2);
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .ai-section:hover {
          transform: translateY(-2px);
          box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .ai-section-header {
          padding: 20px 24px;
          color: white;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-weight: 700;
          position: relative;
          overflow: hidden;
        }

        .ai-section-header::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
          pointer-events: none;
        }

        .section-title-wrapper {
          display: flex;
          align-items: center;
          gap: 12px;
          position: relative;
          z-index: 1;
        }

        .section-icon {
          font-size: 1.5rem;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        .ai-section-title {
          font-size: 1.5rem;
          margin: 0;
          font-family: 'Georgia', serif;
          font-weight: 700;
          text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .section-number {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 1px;
          font-weight: 800;
          background: rgba(255,255,255,0.2);
          padding: 6px 12px;
          border-radius: 20px;
          position: relative;
          z-index: 1;
        }

        .ai-section-content {
          padding: 24px;
          background: rgba(255,255,255,0.02);
          border-top: 1px solid rgba(255,255,255,0.1);
        }

        .ai-planet-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: rgba(147, 51, 234, 0.15);
          border-left: 4px solid #9333ea;
          border-radius: 8px;
          margin-bottom: 12px;
        }

        .ai-planet-symbol {
          font-size: 1.5rem;
          font-weight: bold;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        .ai-planet-text {
          font-size: 1rem;
          font-weight: 600;
          color: #e0e7ff;
        }

        .ai-bold-header {
          font-size: 1.1rem;
          font-weight: 700;
          color: #f8fafc;
          margin: 16px 0 8px 0;
          padding: 8px 0;
          border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .ai-warning-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(245, 158, 11, 0.15);
          border-left: 4px solid #f59e0b;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-warning-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .ai-warning-text {
          font-size: 0.95rem;
          color: #fde68a;
          font-weight: 600;
        }

        .ai-insight-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(59, 130, 246, 0.15);
          border-left: 4px solid #3b82f6;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-insight-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .ai-insight-text {
          font-size: 0.95rem;
          color: #bfdbfe;
          font-weight: 600;
        }

        .ai-bullet-point {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 8px 12px;
          margin: 8px 0;
          background: rgba(255,255,255,0.05);
          border-radius: 6px;
        }

        .ai-bullet {
          color: #9333ea;
          font-weight: bold;
          margin-top: 4px;
          font-size: 1.2rem;
        }

        .ai-bullet-text {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.5;
        }

        .ai-formula-block {
          padding: 12px;
          background: rgba(34, 197, 94, 0.15);
          border-left: 4px solid #22c55e;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-formula-text {
          font-size: 0.95rem;
          color: #bbf7d0;
          font-style: italic;
          font-weight: 600;
        }

        .ai-key-value {
          display: flex;
          gap: 12px;
          padding: 8px 0;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .ai-key {
          font-weight: 700;
          color: #9333ea;
          min-width: 120px;
          font-size: 0.9rem;
        }

        .ai-value {
          color: #e5e7eb;
          font-size: 0.95rem;
        }

        .ai-normal-line {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.6;
          margin: 8px 0;
        }

        .zodiac-ai-footer {
          border-top: 2px solid rgba(255,255,255,0.1);
          padding-top: 30px;
          text-align: center;
        }

        .ai-footer-note {
          font-size: 12px;
          color: #94a3b8;
          margin-bottom: 20px;
          line-height: 1.5;
          max-width: 700px;
          margin-left: auto;
          margin-right: auto;
        }

        .ai-footer-actions {
          display: flex;
          justify-content: center;
          gap: 16px;
        }

        .btn-secondary {
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.2);
          color: white;
          padding: 10px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
          background: rgba(255,255,255,0.2);
          border-color: rgba(255,255,255,0.4);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        @media (max-width: 768px) {
          .zodiac-ai-container {
            padding: 20px;
            margin: 0 16px 40px 16px;
          }
          
          .ai-title {
            font-size: 2.5rem;
          }
          
          .info-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
          }
          
          .ai-section {
            margin-bottom: 20px;
          }
          
          .ai-section-title {
            font-size: 1.25rem;
          }
        }
      `}</style>
    </div>
  );
};

export default ZodiacAIReportDisplay;
