from __future__ import annotations

import os
from typing import Optional, Tuple

import httpx
from geopy.geocoders import Nominatim

class GeocodingService:
    def __init__(self) -> None:
        self._geolocator = Nominatim(user_agent="zodiac-compatibility-checker")
        self._google_key = os.getenv("GOOGLE_GEOCODING_API_KEY")

    def geocode(self, place: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        try:
            location = self._geolocator.geocode(place)
            if location:
                return location.latitude, location.longitude, location.address
        except Exception:
            pass

        if self._google_key:
            return self._geocode_google(place)

        return None, None, None

    def _geocode_google(self, place: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": place, "key": self._google_key}
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                location = result["geometry"]["location"]
                return location["lat"], location["lng"], result.get("formatted_address")
        except Exception:
            return None, None, None

        return None, None, None
