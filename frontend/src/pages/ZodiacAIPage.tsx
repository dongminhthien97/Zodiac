import React, { useState } from "react";
import ZodiacAIReportDisplay from "../components/ZodiacAIReportDisplay";
import { fetchZodiacAIReport } from "../services/api";

interface FormData {
  datetime_utc: string;
  lat: number;
  lon: number;
}

const ZodiacAIPage: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    datetime_utc: "2023-01-15T14:30:00Z",
    lat: 21.0285, // Hanoi
    lon: 105.8542,
  });
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await fetchZodiacAIReport(formData);
      setReport(result);
    } catch (err) {
      setError("Failed to generate Zodiac AI report. Please try again.");
      console.error("Error generating report:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "lat" || name === "lon" ? parseFloat(value) : value,
    }));
  };

  return (
    <div className="zodiac-ai-page">
      <div className="page-header">
        <h1>🤖 Zodiac AI Professional Report Generator</h1>
        <p>
          Generate professional-quality astrological reports with detailed
          analysis
        </p>
      </div>

      <div className="content-container">
        {/* Form Section */}
        <div className="form-section">
          <div className="form-card">
            <h2>📝 Input Information</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="datetime_utc">Birth Date & Time (UTC)</label>
                <input
                  type="datetime-local"
                  id="datetime_utc"
                  name="datetime_utc"
                  value={formData.datetime_utc.replace("Z", "")}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      datetime_utc: e.target.value + "Z",
                    }))
                  }
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="lat">Latitude</label>
                  <input
                    type="number"
                    id="lat"
                    name="lat"
                    step="0.0001"
                    value={formData.lat}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="lon">Longitude</label>
                  <input
                    type="number"
                    id="lon"
                    name="lon"
                    step="0.0001"
                    value={formData.lon}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? "Generating..." : "Generate Zodiac AI Report"}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Report Section */}
        <div className="report-section">
          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {report && (
            <ZodiacAIReportDisplay
              report={report.report}
              chartData={report.chart_data}
              generatedAt={report.generated_at}
              placements={report.placements}
            />
          )}
        </div>
      </div>

      <style>{`
        .zodiac-ai-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 40px 20px;
        }

        .page-header {
          text-align: center;
          margin-bottom: 40px;
          color: white;
        }

        .page-header h1 {
          font-size: 3rem;
          margin-bottom: 10px;
          text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .page-header p {
          font-size: 1.2rem;
          opacity: 0.9;
          max-width: 600px;
          margin: 0 auto;
        }

        .content-container {
          max-width: 1200px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: 1fr 2fr;
          gap: 40px;
        }

        .form-section {
          background: rgba(255,255,255,0.1);
          padding: 30px;
          border-radius: 20px;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255,255,255,0.2);
        }

        .form-card h2 {
          color: white;
          margin-bottom: 24px;
          font-size: 1.5rem;
          border-bottom: 2px solid rgba(255,255,255,0.3);
          padding-bottom: 12px;
        }

        .form-group {
          margin-bottom: 20px;
        }

        .form-group label {
          display: block;
          color: rgba(255,255,255,0.8);
          margin-bottom: 8px;
          font-weight: 600;
          font-size: 0.9rem;
        }

        .form-group input {
          width: 100%;
          padding: 12px 16px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.3);
          background: rgba(255,255,255,0.1);
          color: white;
          font-size: 1rem;
          transition: all 0.3s ease;
        }

        .form-group input:focus {
          outline: none;
          border-color: rgba(255,255,255,0.8);
          box-shadow: 0 0 15px rgba(255,255,255,0.2);
          background: rgba(255,255,255,0.15);
        }

        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }

        .form-actions {
          margin-top: 30px;
          text-align: center;
        }

        .btn-primary {
          background: linear-gradient(135deg, #ffffff, #9333ea);
          border: none;
          color: #1f2937;
          padding: 14px 32px;
          border-radius: 12px;
          font-size: 1.1rem;
          font-weight: 800;
          cursor: pointer;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
          box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .btn-primary:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }

        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        .error-message {
          background: rgba(239, 68, 68, 0.15);
          border: 1px solid rgba(239, 68, 68, 0.5);
          color: #fecaca;
          padding: 16px 20px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 20px;
        }

        .error-icon {
          font-size: 1.5rem;
        }

        .report-section {
          min-height: 500px;
        }

        @media (max-width: 768px) {
          .content-container {
            grid-template-columns: 1fr;
            gap: 20px;
          }

          .page-header h1 {
            font-size: 2rem;
          }

          .form-row {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default ZodiacAIPage;
