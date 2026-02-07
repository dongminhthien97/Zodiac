import React, { useState } from 'react'
import { fetchCompatibility } from '../services/api'
import { useCompatibilityStore } from '../store/useCompatibilityStore'
import { buildBirthPlace, COUNTRY_CITY_OPTIONS, DEFAULT_COUNTRY, getDefaultCity } from '../data/locations'
import { Sparkles, Heart } from 'lucide-react'

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

const defaultCountry = DEFAULT_COUNTRY;
const defaultCity = getDefaultCity(defaultCountry);

const defaultPerson: PersonData = {
  name: '',
  gender: 'other',
  birth_date: '',
  birth_time: '',
  time_unknown: false,
  country: defaultCountry,
  city: defaultCity,
  birth_place: buildBirthPlace(defaultCountry, defaultCity)
};

function PersonForm({ title, person, onChange }: { title: string; person: PersonData; onChange: (p: PersonData) => void }) {
  const countries = Object.keys(COUNTRY_CITY_OPTIONS);
  const cityOptions = COUNTRY_CITY_OPTIONS[person.country] || [];

  const updateCountry = (country: string) => {
    const city = getDefaultCity(country)
    onChange({
      ...person,
      country,
      city,
      birth_place: buildBirthPlace(country, city)
    })
  }

  const updateCity = (city: string) => {
    onChange({
      ...person,
      city,
      birth_place: buildBirthPlace(person.country, city)
    })
  }

  return (
    <div className="glass-card person-card">
      <h3 className="card-title">
        <Sparkles className="icon-nebula" />
        {title}
      </h3>
      
      <div className="form-grid">
        <div className="form-field">
          <label>Tên (Biệt danh)</label>
          <input
            className="glass-input"
            value={person.name}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, name: e.target.value })}
            placeholder="Nhập tên..."
          />
        </div>

        <div className="form-field">
          <label>Giới tính</label>
          <select
            className="glass-input"
            value={person.gender}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange({ ...person, gender: e.target.value })}
          >
            <option value="female">Nữ</option>
            <option value="male">Nam</option>
            <option value="other">Khác</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-field">
            <label>Ngày sinh</label>
            <input
              type="date"
              className="glass-input"
              value={person.birth_date}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, birth_date: e.target.value })}
            />
          </div>
          <div className="form-field">
            <label>Giờ sinh</label>
            <input
              type="time"
              className="glass-input"
              value={person.birth_time}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, birth_time: e.target.value })}
              disabled={person.time_unknown}
            />
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={person.time_unknown}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, time_unknown: e.target.checked })}
              />
              <span>Không rõ giờ sinh</span>
            </label>
          </div>
        </div>

        <div className="form-row">
          <div className="form-field">
            <label>Quốc gia</label>
            <select className="glass-input" value={person.country} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => updateCountry(e.target.value)}>
              {countries.map((country) => (
                <option key={country} value={country}>{country}</option>
              ))}
            </select>
          </div>
          <div className="form-field">
            <label>Thành phố</label>
            <select className="glass-input" value={person.city} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => updateCity(e.target.value)}>
              {cityOptions.map((city: string) => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}

function normalizePerson(person: PersonData) {
  return {
    name: person.name,
    gender: person.gender,
    birth_date: person.birth_date,
    birth_time: person.birth_time,
    time_unknown: person.time_unknown,
    birth_place: person.birth_place
  }
}

export default function CompatibilityForm() {
  const [personA, setPersonA] = useState(defaultPerson)
  const [personB, setPersonB] = useState(defaultPerson)

  const setLoading = useCompatibilityStore((state) => state.setLoading)
  const setError = useCompatibilityStore((state) => state.setError)
  const setResult = useCompatibilityStore((state) => state.setResult)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = {
        person_a: normalizePerson(personA),
        person_b: normalizePerson(personB)
      }
      const data = await fetchCompatibility(payload)
      setResult('compatibility', data)
    } catch (error: any) {
      setError(error?.response?.data?.detail || 'Đã có lỗi xảy ra')
      setLoading(false)
    }
  }

  return (
    <div className="compatibility-form-wrapper">
      <div className="form-header">
        <h2 className="title-gradient">Kết Nối Vì Sao</h2>
        <p className="desc">
          Khám phá sự hòa hợp giữa hai tâm hồn thông qua lăng kính chiêm tinh học.
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="comp-form">
        <div className="comp-grid">
           <div className="connector-overlay">
              <div className="heart-circle">
                <Heart className="icon-heart" />
              </div>
           </div>

          <PersonForm title="Bạn" person={personA} onChange={setPersonA} />
          <PersonForm title="Đối phương" person={personB} onChange={setPersonB} />
        </div>
        
        <div className="submit-area">
          <button type="submit" className="btn-cosmic main-submit">
            Xem Kết Quả Tương Hợp
          </button>
        </div>
      </form>

      <style>{`
        .compatibility-form-wrapper {
          padding: 20px 0;
        }
        .form-header {
          text-align: center;
          margin-bottom: 50px;
        }
        .title-gradient {
          font-size: 3rem;
          margin-bottom: 12px;
          background: linear-gradient(135deg, var(--gold-primary), var(--nebula-pink));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .desc {
          color: var(--white-70);
          max-width: 600px;
          margin: 0 auto;
        }
        .comp-form {
          position: relative;
        }
        .comp-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 40px;
          position: relative;
        }
        .submit-area {
          display: flex;
          justify-content: center;
          margin-top: 50px;
        }
        .main-submit {
          min-width: 300px;
          font-size: 1.1rem;
        }
        .card-title {
          font-size: 1.5rem;
          margin-bottom: 24px;
          display: flex;
          align-items: center;
          gap: 12px;
          color: var(--gold-primary);
        }
        .icon-nebula {
          color: var(--nebula-purple);
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
        .connector-overlay {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          z-index: 5;
        }
        .heart-circle {
          width: 50px;
          height: 50px;
          background: var(--space-ink);
          border: 1px solid var(--white-10);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 0 20px var(--nebula-purple-glow);
        }
        .icon-heart {
          color: var(--nebula-pink);
          fill: rgba(217, 70, 239, 0.2);
        }

        @media (max-width: 992px) {
          .comp-grid {
            grid-template-columns: 1fr;
            gap: 24px;
          }
          .connector-overlay {
            display: none;
          }
        }
      `}</style>
    </div>
  )
}
