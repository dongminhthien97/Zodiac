from __future__ import annotations

import logging
import os
from typing import Optional, Tuple

import httpx
from geopy.geocoders import Nominatim

class GeocodingService:
    def __init__(self) -> None:
        self._geolocator = Nominatim(user_agent="zodiac-compatibility-checker")
        self._google_key = os.getenv("GOOGLE_GEOCODING_API_KEY")
        self._default_country = os.getenv("DEFAULT_COUNTRY", "Vietnam")
        self._logger = logging.getLogger(__name__)

    def geocode(self, place: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        """Geocode a place name to coordinates with fallback handling."""
        place = place.strip()
        if place and self._default_country:
            lower_place = place.lower()
            lower_country = self._default_country.lower()
            if lower_country not in lower_place:
                place = f"{place}, {self._default_country}"
        
        self._logger.debug("Geocode input: %s", place)
        
        # Try Nominatim first
        try:
            location = self._geolocator.geocode(place)
            if location:
                self._logger.debug(
                    "Geocode success: %s -> lat=%s lon=%s address=%s",
                    place,
                    location.latitude,
                    location.longitude,
                    location.address,
                )
                return location.latitude, location.longitude, location.address
        except Exception as e:
            self._logger.warning("Geocode Nominatim failed for %s: %s", place, str(e))

        # Fallback to Google Geocoding API
        if self._google_key:
            return self._geocode_google(place)

        # Final fallback: return None values
        self._logger.warning("Geocoding failed for %s: no services available", place)
        return None, None, None

    def _geocode_google(self, place: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        """Geocode using Google Maps API with error handling."""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": place, "key": self._google_key}
        
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                location = result["geometry"]["location"]
                self._logger.debug(
                    "Geocode Google success: %s -> lat=%s lon=%s address=%s",
                    place,
                    location["lat"],
                    location["lng"],
                    result.get("formatted_address"),
                )
                return location["lat"], location["lng"], result.get("formatted_address")
            else:
                self._logger.warning("Google Geocoding API returned status: %s", data.get("status"))
                
        except httpx.RequestError as e:
            self._logger.warning("Google Geocoding API request failed for %s: %s", place, str(e))
        except httpx.HTTPStatusError as e:
            self._logger.warning("Google Geocoding API HTTP error for %s: %s", place, str(e))
        except Exception as e:
            self._logger.warning("Google Geocoding API unexpected error for %s: %s", place, str(e))
            
        return None, None, None
