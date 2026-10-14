"""
aqi.py - Convert PM2.5 concentrations to the US EPA Air Quality Index (AQI).

Uses the EPA PM2.5 breakpoints updated in 2024 (Good ends at 9.0 µg/m³).
"""

import math


PM25_BREAKPOINTS = [
    (0.0,   9.0,   0,   50,  "Good"),
    (9.1,   35.4,  51,  100, "Moderate"),
    (35.5,  55.4,  101, 150, "Unhealthy for Sensitive Groups"),
    (55.5,  125.4, 151, 200, "Unhealthy"),
    (125.5, 225.4, 201, 300, "Very Unhealthy"),
    (225.5, 325.4, 301, 500, "Hazardous"),
]


def _truncate_one_decimal(value):
    """EPA truncates PM2.5 to one decimal place (9.05 -> 9.0, not 9.1)."""
    # The tiny 1e-9 guards against float errors like 4.2 * 10 = 41.99999...
    return math.floor(value * 10 + 1e-9) / 10


def _round_half_up(value):
    """Round .5 up (Python's round() sends 2.5 to 2, which EPA doesn't do)."""
    return int(math.floor(value + 0.5))


def pm25_to_aqi(pm25):
    """
    Convert a PM2.5 concentration (µg/m³) to an AQI number.

    Returns None for missing or negative values.
    Values above 325.4 are capped at 500.
    """
    if pm25 is None or (isinstance(pm25, float) and math.isnan(pm25)) or pm25 < 0:
        return None

    pm25 = _truncate_one_decimal(pm25)

    if pm25 > PM25_BREAKPOINTS[-1][1]:
        return 500

    for conc_lo, conc_hi, aqi_lo, aqi_hi, _ in PM25_BREAKPOINTS:
        if conc_lo <= pm25 <= conc_hi:
            aqi = (aqi_hi - aqi_lo) / (conc_hi - conc_lo) * (pm25 - conc_lo) + aqi_lo
            return _round_half_up(aqi)

    return None


def aqi_category(aqi):
    """Return the category name for an AQI number, e.g. 42 -> 'Good'."""
    if aqi is None or aqi < 0:
        return None
    for _, _, aqi_lo, aqi_hi, category in PM25_BREAKPOINTS:
        if aqi_lo <= aqi <= aqi_hi:
            return category
    return "Hazardous"  # anything above 500


def pm25_to_aqi_and_category(pm25):
    """Convenience: return (aqi, category) in one call."""
    aqi = pm25_to_aqi(pm25)
    return aqi, aqi_category(aqi)
