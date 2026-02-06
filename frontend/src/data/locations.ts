export const COUNTRY_CITY_OPTIONS: Record<string, string[]> = {
  Vietnam: ['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Huế', 'Cần Thơ', 'Hải Phòng'],
  Thailand: ['Bangkok', 'Chiang Mai', 'Phuket', 'Pattaya'],
  Singapore: ['Singapore'],
  Japan: ['Tokyo', 'Osaka', 'Kyoto', 'Fukuoka'],
  'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu'],
  USA: ['New York', 'Los Angeles', 'Chicago', 'Houston'],
  France: ['Paris', 'Lyon', 'Marseille', 'Nice']
}

export const DEFAULT_COUNTRY = 'Vietnam'

export function buildBirthPlace(country: string, city: string) {
  if (!country && !city) return ''
  if (!city) return country
  return `${city}, ${country}`
}

export function getDefaultCity(country: string = DEFAULT_COUNTRY) {
  return COUNTRY_CITY_OPTIONS[country]?.[0] || ''
}
