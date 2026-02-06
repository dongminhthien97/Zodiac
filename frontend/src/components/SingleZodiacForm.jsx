import React, { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Select } from './ui/select'
import { fetchNatal } from '../services/api'
import { useCompatibilityStore } from '../store/useCompatibilityStore'
import { buildBirthPlace, COUNTRY_CITY_OPTIONS, DEFAULT_COUNTRY, getDefaultCity } from '../data/locations'

const defaultCountry = DEFAULT_COUNTRY
const defaultCity = getDefaultCity(defaultCountry)

const defaultPerson = {
  name: '',
  gender: 'other',
  birth_date: '',
  birth_time: '',
  time_unknown: false,
  country: defaultCountry,
  city: defaultCity,
  birth_place: buildBirthPlace(defaultCountry, defaultCity)
}

export default function SingleZodiacForm() {
  const [person, setPerson] = useState(defaultPerson)

  const setLoading = useCompatibilityStore((state) => state.setLoading)
  const setError = useCompatibilityStore((state) => state.setError)
  const setResult = useCompatibilityStore((state) => state.setResult)

  const countries = Object.keys(COUNTRY_CITY_OPTIONS)
  const cityOptions = COUNTRY_CITY_OPTIONS[person.country] || []

  const updateCountry = (country) => {
    const city = getDefaultCity(country)
    setPerson({
      ...person,
      country,
      city,
      birth_place: buildBirthPlace(country, city)
    })
  }

  const updateCity = (city) => {
    setPerson({
      ...person,
      city,
      birth_place: buildBirthPlace(person.country, city)
    })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = {
        person: {
          name: person.name,
          gender: person.gender,
          birth_date: person.birth_date,
          birth_time: person.birth_time,
          time_unknown: person.time_unknown,
          birth_place: person.birth_place
        }
      }
      const data = await fetchNatal(payload)
      setResult('natal', data)
    } catch (error) {
      setError(error?.response?.data?.detail || 'Đã có lỗi xảy ra')
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="bg-white/3">
        <CardHeader>
          <CardTitle>Thông tin của bạn</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Tên (không bắt buộc)</label>
              <Input
                value={person.name}
                onChange={(e) => setPerson({ ...person, name: e.target.value })}
                placeholder="Ví dụ: Linh"
              />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Giới tính</label>
              <Select
                value={person.gender}
                onChange={(e) => setPerson({ ...person, gender: e.target.value })}
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
                  onChange={(e) => setPerson({ ...person, birth_date: e.target.value })}
                />
              </div>
              <div>
                <label className="text-xs uppercase tracking-wide text-white/60">Giờ sinh</label>
                <Input
                  type="time"
                  value={person.birth_time}
                  onChange={(e) => setPerson({ ...person, birth_time: e.target.value })}
                  disabled={person.time_unknown}
                />
                <label className="mt-2 flex items-center gap-2 text-xs text-white/60">
                  <input
                    type="checkbox"
                    checked={person.time_unknown}
                    onChange={(e) => setPerson({ ...person, time_unknown: e.target.checked })}
                  />
                  Không rõ giờ sinh
                </label>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <label className="text-xs uppercase tracking-wide text-white/60">Quốc gia</label>
                <Select value={person.country} onChange={(e) => updateCountry(e.target.value)}>
                  {countries.map((country) => (
                    <option key={country} value={country}>{country}</option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="text-xs uppercase tracking-wide text-white/60">Thành phố</label>
                <Select value={person.city} onChange={(e) => updateCity(e.target.value)}>
                  {cityOptions.map((city) => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </Select>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-center">
        <Button type="submit" variant="cute" className="px-10">Xem cung hoàng đạo</Button>
      </div>
    </form>
  )
}
