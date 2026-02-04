import React, { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Select } from './ui/select'
import { fetchNatal } from '../services/api'
import { useCompatibilityStore } from '../store/useCompatibilityStore'

const defaultPerson = {
  name: '',
  gender: 'other',
  birth_date: '',
  birth_time: '',
  time_unknown: false,
  birth_place: 'Vietnam'
}

export default function SingleZodiacForm() {
  const [person, setPerson] = useState(defaultPerson)

  const setLoading = useCompatibilityStore((state) => state.setLoading)
  const setError = useCompatibilityStore((state) => state.setError)
  const setResult = useCompatibilityStore((state) => state.setResult)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = { person }
      const data = await fetchNatal(payload)
      setResult('natal', data)
    } catch (error) {
      setError(error?.response?.data?.detail || '?? c? l?i x?y ra')
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="bg-white/3">
        <CardHeader>
          <CardTitle>Th?ng tin c?a b?n</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">T?n (kh?ng b?t bu?c)</label>
              <Input
                value={person.name}
                onChange={(e) => setPerson({ ...person, name: e.target.value })}
                placeholder="V? d?: Linh"
              />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">Gi?i t?nh</label>
              <Select
                value={person.gender}
                onChange={(e) => setPerson({ ...person, gender: e.target.value })}
              >
                <option value="female">N?</option>
                <option value="male">Nam</option>
                <option value="other">Kh?c</option>
              </Select>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs uppercase tracking-wide text-white/60">Ng?y sinh</label>
                <Input
                  type="date"
                  value={person.birth_date}
                  onChange={(e) => setPerson({ ...person, birth_date: e.target.value })}
                />
              </div>
              <div>
                <label className="text-xs uppercase tracking-wide text-white/60">Gi? sinh</label>
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
                  Kh?ng r? gi? sinh
                </label>
              </div>
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-white/60">N?i sinh</label>
              <Input
                value={person.birth_place}
                onChange={(e) => setPerson({ ...person, birth_place: e.target.value })}
                placeholder="Th?nh ph?, Vietnam"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-center">
        <Button type="submit" variant="cute" className="px-10">Xem cung ho?ng ??o</Button>
      </div>
    </form>
  )
}
