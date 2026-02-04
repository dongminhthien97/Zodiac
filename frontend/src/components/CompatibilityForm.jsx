import React, { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Select } from './ui/select'
import { fetchCompatibility } from '../services/api'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

const defaultPerson = {
  name: '',
  gender: 'other',
  birth_date: '',
  birth_time: '',
  time_unknown: false,
  birth_place: 'Vietnam'
}

function PersonForm({ title, person, onChange }) {
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
              onChange={(e) => onChange({ ...person, name: e.target.value })}
              placeholder="Ví dụ: Linh"
            />
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-white/60">Giới tính</label>
            <Select
              value={person.gender}
              onChange={(e) => onChange({ ...person, gender: e.target.value })}
            >
              <option value="female">Nữ</option>
              <option value="male">Nam</option>
              <option value="other">Khác</option>
            </Select>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Ngày sinh</label>
              <Input
                type="date"
                value={person.birth_date}
                onChange={(e) => onChange({ ...person, birth_date: e.target.value })}
              />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Giờ sinh</label>
              <Input
                type="time"
                value={person.birth_time}
                onChange={(e) => onChange({ ...person, birth_time: e.target.value })}
                disabled={person.time_unknown}
              />
              <label className="mt-2 flex items-center gap-2 text-xs text-white/60">
                <input
                  type="checkbox"
                  checked={person.time_unknown}
                  onChange={(e) => onChange({ ...person, time_unknown: e.target.checked })}
                />
                Không rõ giờ sinh
              </label>
            </div>
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-white/60">Nơi sinh</label>
            <Input
              value={person.birth_place}
              onChange={(e) => onChange({ ...person, birth_place: e.target.value })}
              placeholder="Thành phố, Vietnam"
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default function CompatibilityForm() {
  const [personA, setPersonA] = useState(defaultPerson)
  const [personB, setPersonB] = useState(defaultPerson)

  const setLoading = useCompatibilityStore((state) => state.setLoading)
  const setError = useCompatibilityStore((state) => state.setError)
  const setResult = useCompatibilityStore((state) => state.setResult)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = {
        person_a: personA,
        person_b: personB
      }
      const data = await fetchCompatibility(payload)
      setResult('compatibility', data)
    } catch (error) {
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
