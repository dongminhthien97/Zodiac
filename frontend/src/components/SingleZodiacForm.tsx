import React, { useState } from "react";
import { fetchNatal, fetchStandardReport } from "../services/api";
import { useCompatibilityStore } from "../store/useCompatibilityStore";
import {
  buildBirthPlace,
  COUNTRY_CITY_OPTIONS,
  DEFAULT_COUNTRY,
  getDefaultCity,
} from "../data/locations";
import { SelectLight } from "./ui/select";

interface PersonData {
  name: string;
  gender: string;
  birth_date: string;
  birth_time: string;
  time_unknown: boolean;
  country: string;
  city: string;
  birth_place: any;
}

interface StandardReportRequest {
  datetime_utc: string;
  lat: number;
  lon: number;
}

const defaultCountry = DEFAULT_COUNTRY;
const defaultCity = getDefaultCity(defaultCountry);

const defaultPerson: PersonData = {
  name: "",
  gender: "other",
  birth_date: "",
  birth_time: "",
  time_unknown: false,
  country: defaultCountry,
  city: defaultCity,
  birth_place: buildBirthPlace(defaultCountry, defaultCity),
};

export default function SingleZodiacForm() {
  const [person, setPerson] = useState(defaultPerson);

  const mode = useCompatibilityStore((state) => state.mode);
  const setLoading = useCompatibilityStore((state) => state.setLoading);
  const setError = useCompatibilityStore((state) => state.setError);
  const setResult = useCompatibilityStore((state) => state.setResult);

  const countries = Object.keys(COUNTRY_CITY_OPTIONS);
  const cityOptions = (COUNTRY_CITY_OPTIONS as any)[person.country] || [];

  const updateCountry = (country: string) => {
    const city = getDefaultCity(country);
    setPerson({
      ...person,
      country,
      city,
      birth_place: buildBirthPlace(country, city),
    });
  };

  const updateCity = (city: string) => {
    setPerson({
      ...person,
      city,
      birth_place: buildBirthPlace(person.country, city),
    });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (mode === "standard") {
        // Convert to NatalRequest format for standard endpoint
        const payload = {
          person: {
            name: person.name,
            gender: person.gender,
            birth_date: person.birth_date,
            birth_time: person.birth_time,
            time_unknown: person.time_unknown,
            birth_place: person.birth_place,
          },
        };
        const data = await fetchStandardReport(payload);
        setResult("standard", data);
      } else {
        const payload = {
          person: {
            name: person.name,
            gender: person.gender,
            birth_date: person.birth_date,
            birth_time: person.birth_time,
            time_unknown: person.time_unknown,
            birth_place: person.birth_place,
          },
        };
        const data = await fetchNatal(payload);
        setResult("natal", data);
      }
    } catch (error: any) {
      setError(error?.response?.data?.detail || "Đã có lỗi xảy ra");
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="single-form-wrapper animate-fade-in"
    >
      <div className="glass-card person-card">
        <h3 className="card-title">Hồ sơ cá nhân</h3>

        <div className="form-grid">
          <div className="form-field">
            <label>Tên (không bắt buộc)</label>
            <input
              className="glass-input"
              value={person.name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPerson({ ...person, name: e.target.value })
              }
              placeholder="Ví dụ: Linh"
            />
          </div>

          <div className="form-field">
            <label>Giới tính</label>
            <SelectLight
              value={person.gender}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                setPerson({ ...person, gender: e.target.value })
              }
            >
              <option value="female">Nữ</option>
              <option value="male">Nam</option>
              <option value="other">Khác</option>
            </SelectLight>
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Ngày sinh</label>
              <input
                type="date"
                className="glass-input"
                value={person.birth_date}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setPerson({ ...person, birth_date: e.target.value })
                }
              />
            </div>
            <div className="form-field">
              <label>Giờ sinh</label>
              <input
                type="time"
                className="glass-input"
                value={person.birth_time}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setPerson({ ...person, birth_time: e.target.value })
                }
                disabled={person.time_unknown}
              />
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={person.time_unknown}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setPerson({ ...person, time_unknown: e.target.checked })
                  }
                />
                <span>Không rõ giờ sinh</span>
              </label>
            </div>
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>Quốc gia</label>
              <SelectLight
                value={person.country}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                  updateCountry(e.target.value)
                }
              >
                {countries.map((country) => (
                  <option key={country} value={country}>
                    {country}
                  </option>
                ))}
              </SelectLight>
            </div>
            <div className="form-field">
              <label>Thành phố</label>
              <SelectLight
                value={person.city}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                  updateCity(e.target.value)
                }
              >
                {cityOptions.map((city: string) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </SelectLight>
            </div>
          </div>
        </div>
      </div>

      <div className="submit-area">
        <button type="submit" className="btn-cosmic main-submit">
          Giải Mã Bản Đồ Sao
        </button>
      </div>

      <style>{`
        .single-form-wrapper {
          max-width: 600px;
          margin: 0 auto;
        }
        .submit-area {
          display: flex;
          justify-content: center;
          margin-top: 40px;
        }
        .main-submit {
          min-width: 250px;
        }
        .card-title {
          font-size: 1.5rem;
          margin-bottom: 24px;
          color: var(--gold-primary);
          font-family: var(--font-display);
        }
        .form-grid {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .form-field {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .form-field label {
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: var(--white-40);
        }
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 8px;
          font-size: 12px;
          color: var(--white-70);
          cursor: pointer;
        }
      `}</style>
    </form>
  );
}
