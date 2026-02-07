from __future__ import annotations
import logging
from datetime import datetime
from typing import Optional, List

try:
    from flatlib.chart import Chart
    from flatlib.datetime import Datetime as FlatDatetime
    from flatlib.geopos import GeoPos
except Exception:
    Chart = None
    FlatDatetime = None
    GeoPos = None

from models.schemas import PlanetPosition

logger = logging.getLogger(__name__)


class ChartService:
    """Generates basic flatlib Chart objects and extracts planet positions.

    If `flatlib` is not installed, this service returns empty results but fails gracefully.
    """

    def __init__(self) -> None:
        self._logger = logger
        if not Chart:
            self._logger.warning("flatlib not available. ChartService will be limited.")

    def build_chart(self, dt: datetime, lat: float, lon: float, tz: str = 'UTC') -> Optional[List[PlanetPosition]]:
        if not Chart or not FlatDatetime or lat is None or lon is None:
            return None

        try:
            fd = FlatDatetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tz)
            gp = GeoPos(lat, lon)
            chart = Chart(fd, gp)

            planets = []
            for body in ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']:
                obj = chart.get(body)
                if obj:
                    lon_val = float(obj.lon)
                    sign_index = int(lon_val // 30)
                    sign_names = [
                        'Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                        'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'
                    ]
                    sign = sign_names[sign_index]
                    planets.append(PlanetPosition(name=body, sign=sign, longitude=lon_val))

            return planets
        except Exception as e:
            self._logger.exception(f"flatlib chart generation failed: {e}")
            return None
