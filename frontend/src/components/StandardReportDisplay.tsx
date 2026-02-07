import React from "react";

interface StandardReportDisplayProps {
  report: string;
  chartData: any;
  generatedAt: string;
}

const StandardReportDisplay: React.FC<StandardReportDisplayProps> = ({
  report,
  chartData,
  generatedAt,
}) => {
  // Parse the report text into structured sections
  const parseReport = (reportText: string) => {
    const sections = [];
    const lines = reportText.split("\n");
    let currentSection: any = null;
    let currentContent: string[] = [];

    for (const line of lines) {
      const trimmedLine = line.trim();

      // Check if this is a section header (starts with number)
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
      } else if (currentSection) {
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

  const sections = parseReport(report);

  const getSectionIcon = (title: string) => {
    if (title.includes("Tổng quan")) return "📊";
    if (title.includes("Nhân dạng")) return "👤";
    if (title.includes("Tình yêu")) return "❤️";
    if (title.includes("Thế hệ")) return "🌍";
    if (title.includes("Bài học")) return "🎓";
    if (title.includes("Kết luận")) return "🎯";
    return "📄";
  };

  return (
    <div className="standard-report-container">
      {/* Header */}
      <div className="report-header">
        <div className="header-badge">
          <span className="report-icon">📜</span>
          <span className="report-type">BÁO CÁO CHUẨN</span>
        </div>

        <h1 className="report-title">BÁO CÁO CHIẾM TINH CHUẨN</h1>

        <div className="chart-info">
          <div className="info-item">
            <label>Mặt Trời</label>
            <span>{chartData?.sun_sign || "Unknown"}</span>
          </div>
          <div className="info-item">
            <label>Mặt Trăng</label>
            <span>{chartData?.moon_sign || "Unknown"}</span>
          </div>
          <div className="info-item">
            <label>Cung Mọc</label>
            <span>{chartData?.ascendant || "Unknown"}</span>
          </div>
        </div>

        <div className="generated-info">
          <span className="generated-text">
            Generated: {new Date(generatedAt).toLocaleString("vi-VN")}
          </span>
        </div>
      </div>

      {/* Report Content */}
      <div className="report-content">
        {sections.map((section, index) => (
          <div key={index} className="report-section">
            <div className="section-header">
              <div className="section-title-wrapper">
                <span className="section-icon">
                  {getSectionIcon(section.title)}
                </span>
                <h2 className="section-title">{section.title}</h2>
              </div>
              <div className="section-number">Phần {section.id}</div>
            </div>

            <div className="section-content">
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
                    <div key={lineIndex} className="planet-header">
                      <span className="planet-symbol">
                        {line.split(" ")[0]}
                      </span>
                      <span className="planet-text">
                        {line.substring(line.indexOf(" ") + 1)}
                      </span>
                    </div>
                  );
                } else if (line.startsWith("⚠️")) {
                  return (
                    <div key={lineIndex} className="warning-block">
                      <span className="warning-icon">⚠️</span>
                      <span className="warning-text">{line.substring(2)}</span>
                    </div>
                  );
                } else if (line.startsWith("👉")) {
                  return (
                    <div key={lineIndex} className="insight-block">
                      <span className="insight-icon">👉</span>
                      <span className="insight-text">{line.substring(2)}</span>
                    </div>
                  );
                } else if (line.startsWith("-")) {
                  return (
                    <div key={lineIndex} className="bullet-point">
                      <span className="bullet">•</span>
                      <span className="bullet-text">{line.substring(2)}</span>
                    </div>
                  );
                } else if (line.includes("→")) {
                  return (
                    <div key={lineIndex} className="formula-block">
                      <span className="formula-text">{line}</span>
                    </div>
                  );
                } else {
                  return (
                    <div key={lineIndex} className="normal-line">
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
      <div className="report-footer">
        <p className="footer-note">
          Báo cáo được tạo bởi hệ thống Zodiac AI. Kết quả mang tính chất tham
          khảo và phản ánh xu hướng năng lượng chiêm tinh.
        </p>
        <div className="footer-actions">
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
        .standard-report-container {
          max-width: 800px;
          margin: 0 auto;
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 16px;
          padding: 40px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #ffffff;
        }

        .report-header {
          border-bottom: 1px solid rgba(255,255,255,0.1);
          padding-bottom: 30px;
          margin-bottom: 40px;
        }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .report-icon {
          font-size: 2rem;
        }

        .report-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 2px;
          color: #94a3b8;
          font-weight: 700;
        }

        .report-title {
          font-size: 2.5rem;
          margin-bottom: 24px;
          background: linear-gradient(to right, #ffffff, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          font-family: 'Georgia', serif;
          font-weight: 800;
        }

        .chart-info {
          display: flex;
          flex-wrap: wrap;
          gap: 32px;
          margin-bottom: 20px;
        }

        .info-item {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .info-item label {
          font-size: 11px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .info-item span {
          font-size: 1.2rem;
          font-weight: 600;
          color: #ffffff;
          font-family: 'Georgia', serif;
        }

        .generated-info {
          background: rgba(255,255,255,0.05);
          padding: 8px 16px;
          border-radius: 20px;
          display: inline-block;
        }

        .generated-text {
          font-size: 12px;
          color: #94a3b8;
        }

        .report-content {
          margin-bottom: 40px;
        }

        .report-section {
          margin-bottom: 40px;
          padding: 24px;
          background: rgba(255,255,255,0.02);
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.05);
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .section-title-wrapper {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .section-icon {
          font-size: 1.5rem;
        }

        .section-title {
          font-size: 1.5rem;
          margin: 0;
          color: #f472b6;
          font-family: 'Georgia', serif;
          font-weight: 700;
        }

        .section-number {
          font-size: 12px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
          font-weight: 700;
        }

        .section-content {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .planet-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: rgba(147, 51, 234, 0.1);
          border-left: 3px solid #9333ea;
          border-radius: 6px;
        }

        .planet-symbol {
          font-size: 1.5rem;
          font-weight: bold;
        }

        .planet-text {
          font-size: 1rem;
          font-weight: 500;
          color: #e0e7ff;
        }

        .warning-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(245, 158, 11, 0.1);
          border-left: 3px solid #f59e0b;
          border-radius: 6px;
        }

        .warning-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .warning-text {
          font-size: 0.95rem;
          color: #fde68a;
        }

        .insight-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(59, 130, 246, 0.1);
          border-left: 3px solid #3b82f6;
          border-radius: 6px;
        }

        .insight-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .insight-text {
          font-size: 0.95rem;
          color: #bfdbfe;
        }

        .bullet-point {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 8px 12px;
          margin-left: 20px;
        }

        .bullet {
          color: #9333ea;
          font-weight: bold;
          margin-top: 2px;
        }

        .bullet-text {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.5;
        }

        .formula-block {
          padding: 12px;
          background: rgba(34, 197, 94, 0.1);
          border-left: 3px solid #22c55e;
          border-radius: 6px;
          margin-left: 20px;
        }

        .formula-text {
          font-size: 0.95rem;
          color: #bbf7d0;
          font-style: italic;
        }

        .normal-line {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.6;
        }

        .report-footer {
          border-top: 1px solid rgba(255,255,255,0.1);
          padding-top: 30px;
          text-align: center;
        }

        .footer-note {
          font-size: 12px;
          color: #94a3b8;
          margin-bottom: 20px;
          line-height: 1.5;
        }

        .footer-actions {
          display: flex;
          justify-content: center;
          gap: 16px;
        }

        .btn-secondary {
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.2);
          color: white;
          padding: 8px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
        }

        .btn-secondary:hover {
          background: rgba(255,255,255,0.2);
          border-color: rgba(255,255,255,0.4);
        }

        @media (max-width: 768px) {
          .standard-report-container {
            padding: 20px;
            margin: 0 16px 40px 16px;
          }
          
          .report-title {
            font-size: 2rem;
          }
          
          .chart-info {
            gap: 16px;
          }
          
          .report-section {
            padding: 16px;
          }
          
          .section-title {
            font-size: 1.25rem;
          }
        }
      `}</style>
    </div>
  );
};

export default StandardReportDisplay;
