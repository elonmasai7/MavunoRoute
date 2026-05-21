from math import sqrt


def approximate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111
