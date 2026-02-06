import React, { useState } from 'react'
import { Button } from './ui/button.tsx'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card.tsx'
import { Input } from './ui/input.tsx'
import { Select } from './ui/select.tsx'
import { fetchCompatibility } from '../services/api'
import { useCompatibilityStore } from '../store/useCompatibilityStore'
import { buildBirthPlace, COUNTRY_CITY_OPTIONS, DEFAULT_COUNTRY, getDefaultCity } from '../data/locations'

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
    <Card className="bg-white/3">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4">
          <div>
            <label className="text-xs uppercase tracking-wide text-white/60">Tên (không bắt buộc)</label>
            <Input
              value={person.name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, name: e.target.value })}
              placeholder="Ví dụ: Linh"
            />
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-white/60">Giới tính</label>
            <Select
              value={person.gender}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange({ ...person, gender: e.target.value })}
            >
              <option value="female">Nữ</option>
              <option value="male">Nam</option>
              <option value="other">Khác</option>
            </Select>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Ngày sinh</label>
              <Input
                type="date"
                value={person.birth_date}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, birth_date: e.target.value })}
              />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Giờ sinh</label>
              <Input
                type="time"
                value={person.birth_time}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, birth_time: e.target.value })}
                disabled={person.time_unknown}
              />
              <label className="mt-2 flex items-center gap-2 text-xs text-white/60">
                <input
                  type="checkbox"
                  checked={person.time_unknown}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange({ ...person, time_unknown: e.target.checked })}
                />
                Không rõ giờ sinh
              </label>
            </div>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Quốc gia</label>
              <Select value={person.country} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => updateCountry(e.target.value)}>
                {countries.map((country) => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </Select>
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Thành phố</label>
              <Select value={person.city} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => updateCity(e.target.value)}>
                {cityOptions.map((city: string) => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </Select>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
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
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <PersonForm title="Người A" person={personA} onChange={setPersonA} />
        <PersonForm title="Người B" person={personB} onChange={setPersonB} />
      </div>
      <div className="flex justify-center">
        <Button type="submit" variant="cute" className="px-10">Xem độ tương hợp</Button>
      </div>
    </form>
  )
}
