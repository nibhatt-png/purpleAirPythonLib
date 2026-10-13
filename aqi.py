def pm25_to_aqi(pm25):
    conc_lo = 0
    conc_hi = 9.0
    aqi_lo = 0
    aqi_hi = 50
    
    aqi = (aqi_hi - aqi_lo) / (conc_hi - conc_lo) * (pm25 - conc_lo) + aqi_lo
    
    return round(aqi)


print(pm25_to_aqi(4.5))