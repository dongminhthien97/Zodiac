from __future__ import annotations
import logging
from datetime import datetime
from typing import List

try:
    import swisseph as swe
except Exception:
    swe = None

from models.schemas import PlanetPosition

logger = logging.getLogger(__name__)


class EphemerisService:
    """Minimal Swiss Ephemeris wrapper. Returns basic planet longitudes and sign names.

    Requires `pyswisseph` (provides `swisseph` module).
    """

    PLANETS = {
        'Sun': swe.SUN if swe else 0,
        'Moon': swe.MOON if swe else 1,
        'Mercury': swe.MERCURY if swe else 2,
        'Venus': swe.VENUS if swe else 3,
        'Mars': swe.MARS if swe else 4,
        'Jupiter': swe.JUPITER if swe else 5,
        'Saturn': swe.SATURN if swe else 6,
        'Uranus': swe.URANUS if swe else 7,
        'Neptune': swe.NEPTUNE if swe else 8,
        'Pluto': swe.PLUTO if swe else 9,
    }

    def __init__(self) -> None:
        self._logger = logger
        if not swe:
            self._logger.warning("Swiss Ephemeris (swisseph) not available. EphemerisService will be limited.")

    def planet_positions(self, dt: datetime, lat: float | None = None, lon: float | None = None) -> List[PlanetPosition]:
        """Return list of PlanetPosition for supported planets using UTC datetime.

        Args:
            dt: timezone-aware or naive datetime (assumed UTC)
            lat, lon: optional, not used for planet longitudes but kept for API parity
        """
        if not swe:
            return []

        tjd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)
        results: List[PlanetPosition] = []

        for name, pid in self.PLANETS.items():
            try:
                lonlat = swe.calc_ut(tjd, pid)
                longitude = float(lonlat[0][0]) if isinstance(lonlat, tuple) or isinstance(lonlat, list) else float(lonlat[0])
                sign_index = int(longitude // 30)  # 0..11
                sign_names = [
                    'Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                    'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'
                ]
                sign = sign_names[sign_index]
                results.append(PlanetPosition(name=name, sign=sign, longitude=longitude))
            except Exception as e:
                self._logger.exception(f"Error calculating {name}: {e}")

        return results
