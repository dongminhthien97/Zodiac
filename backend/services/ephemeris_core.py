"""Swiss Ephemeris core wrapper implementing deterministic chart calculations.

Core responsibilities:
- Initialize swisseph path from environment
- Compute julian day (UT)
- Compute geocentric tropical longitudes for required bodies
- Compute nodes and Chiron
- Detect major aspects with configurable orb
- Compute houses (Placidus) and support Whole Sign mode

This module strictly performs calculations and returns structured data.
No interpretation or prose is included.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
import os
import math
import logging
from typing import Dict, List, Tuple

try:
    import swisseph as swe
except Exception as e:
    swe = None

from models.schemas import PlanetPosition, Aspect, Houses

logger = logging.getLogger(__name__)

# Required bodies mapping to swisseph constants
_BODIES = {
    'sun': 'SUN',
    'moon': 'MOON',
    'mercury': 'MERCURY',
    'venus': 'VENUS',
    'mars': 'MARS',
    'jupiter': 'JUPITER',
    'saturn': 'SATURN',
    'uranus': 'URANUS',
    'neptune': 'NEPTUNE',
    'pluto': 'PLUTO',
}

# Extra points
_POINTS = {
    'mean_node': 'NODE',
    'true_node': 'TRUE_NODE',
    'chiron': 'CHIRON'
}

DEFAULT_ORB = 8.0


def _ensure_swe():
    if not swe:
        raise RuntimeError("Swiss Ephemeris (swisseph) is not installed or failed to import.")


def init_ephemeris(ephe_path: str | None = None) -> None:
    """Initialize swisseph path. Call once at app startup.

    If not provided, will attempt to read `EPHE_PATH` from environment.
    """
    _ensure_swe()
    path = ephe_path or os.getenv("EPHE_PATH") or "/app/ephe"
    swe.set_ephe_path(path)


def _parse_timezone_offset(tz_str: str) -> float:
    # tz_str expected like +07:00 or -05:30
    sign = 1
    if tz_str.startswith("-"):
        sign = -1
        tz_str = tz_str[1:]
    elif tz_str.startswith("+"):
        tz_str = tz_str[1:]
    hrs, mins = tz_str.split(":")
    return sign * (int(hrs) + int(mins) / 60.0)


def _to_ut_datetime(date_str: str, time_str: str | None, tz_str: str) -> datetime:
    # Produce a UTC datetime used for swe calculations (naive or tz-aware acceptable)
    dt_date = datetime.strptime(date_str, "%Y-%m-%d")
    if time_str is None:
        # default noon UT to avoid ambiguous midnight shifts; caller knows this is NO_HOUSE
        dt = datetime(dt_date.year, dt_date.month, dt_date.day, 12, 0, 0)
    else:
        hh, mm = [int(x) for x in time_str.split(":")]
        dt = datetime(dt_date.year, dt_date.month, dt_date.day, hh, mm, 0)

    tz_off = _parse_timezone_offset(tz_str)
    # Convert local time to UTC by subtracting tz offset
    utc_dt = dt - timedelta(hours=tz_off)
    return utc_dt


def _sign_and_degree(longitude: float) -> Tuple[str, float]:
    sign_names = [
        'Aries','Taurus','Gemini','Cancer','Leo','Virgo',
        'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'
    ]
    lon = longitude % 360.0
    sign_index = int(lon // 30)
    degree = lon - sign_index * 30.0
    return sign_names[sign_index], round(degree, 6)


def _julian_day_from_dt(dt: datetime) -> float:
    # Use swe.julday which expects UT
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)


def compute_planets(date: str, time: str | None, timezone: str, location: Dict[str, float]) -> Dict[str, PlanetPosition]:
    """Compute planetary positions (geocentric tropical) using Swiss Ephemeris.

    Returns dict keyed by lower-case planet name.
    """
    _ensure_swe()

    utc_dt = _to_ut_datetime(date, time, timezone)
    tjd = _julian_day_from_dt(utc_dt)

    flags = swe.FLG_SWIEPH
    results: Dict[str, PlanetPosition] = {}

    for key, const_name in _BODIES.items():
        pid = getattr(swe, const_name)
        vals = swe.calc_ut(tjd, pid, flags)
        lon = float(vals[0][0]) if isinstance(vals[0], (list, tuple)) else float(vals[0])
        sign, degree = _sign_and_degree(lon)
        results[key] = PlanetPosition(name=key, sign=sign, longitude=round(lon, 6), degree=degree)

    # Nodes and Chiron
    try:
        node_vals = swe.calc_ut(tjd, swe.NODE, flags)
        lon = float(node_vals[0][0])
        sign, degree = _sign_and_degree(lon)
        results['mean_node'] = PlanetPosition(name='mean_node', sign=sign, longitude=round(lon,6), degree=degree)
    except Exception:
        pass

    try:
        true_node_vals = swe.calc_ut(tjd, swe.TRUE_NODE, flags)
        lon = float(true_node_vals[0][0])
        sign, degree = _sign_and_degree(lon)
        results['true_node'] = PlanetPosition(name='true_node', sign=sign, longitude=round(lon,6), degree=degree)
    except Exception:
        pass

    try:
        chiron_vals = swe.calc_ut(tjd, swe.CHIRON, flags)
        lon = float(chiron_vals[0][0])
        sign, degree = _sign_and_degree(lon)
        results['chiron'] = PlanetPosition(name='chiron', sign=sign, longitude=round(lon,6), degree=degree)
    except Exception:
        pass

    return results


_ASPECTS = {
    'conjunction': 0.0,
    'sextile': 60.0,
    'square': 90.0,
    'trine': 120.0,
    'opposition': 180.0,
}


def detect_aspects(planets: Dict[str, PlanetPosition], orb: float = DEFAULT_ORB) -> List[Aspect]:
    bodies = list(planets.keys())
    aspects: List[Aspect] = []
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            b1 = bodies[i]
            b2 = bodies[j]
            lon1 = planets[b1].longitude
            lon2 = planets[b2].longitude
            diff = abs((lon1 - lon2 + 180.0) % 360.0 - 180.0)
            for name, angle in _ASPECTS.items():
                d = abs(diff - angle)
                if d <= orb:
                    aspects.append(Aspect(body1=b1, body2=b2, type=name, orb=round(d, 6)))
                    break
    return aspects


def compute_houses(date: str, time: str | None, timezone: str, location: Dict[str, float], system: str) -> Houses:
    _ensure_swe()
    if system not in {"whole_sign", "placidus"}:
        raise ValueError("Unsupported house system")

    utc_dt = _to_ut_datetime(date, time, timezone)
    tjd = _julian_day_from_dt(utc_dt)
    lat = float(location.get('lat'))
    lon = float(location.get('lon'))

    if system == "placidus":
        # swisseph expects longitude East positive, latitude North positive
        cusps, ascmc = swe.houses(tjd, lat, lon, b'P')
        # cusps is 1..12 index in returned array; ascmc[0]=ascendant, ascmc[1]=mc
        cusps_list = [round(float(x), 6) for x in cusps]
        asc = round(float(ascmc[0]), 6)
        mc = round(float(ascmc[1]), 6)
        return Houses(system="placidus", cusps=cusps_list, ascendant=asc, midheaven=mc)
    else:
        # Whole sign: determine ascendant sign and make cusps at 0° of each sign starting from asc sign
        asc_vals = swe.houses(tjd, lat, lon, b'P')[1]
        asc = float(asc_vals[0])
        asc_sign_index = int((asc % 360.0) // 30)
        cusps = []
        for i in range(12):
            cusp = ((asc_sign_index + i) * 30.0) % 360.0
            cusps.append(round(cusp, 6))
        mc = round(float(asc_vals[1]), 6)
        return Houses(system="whole_sign", cusps=cusps, ascendant=round(asc,6), midheaven=mc)
