from math import radians, cos, sin, asin, sqrt


def great_circle_distance(loc1, loc2):
    """
    Calculates the great circle distance bwt 2 lat, long pairs
    :param loc1: 2-tuple of latitude and longitude pair
    :param loc2: 2-tuple of latitude and longitude pair
    :return: gcd = c*r in miles
    """
    lat1, lon1, lat2, lon2 = map(radians, [loc1[0], loc1[1], loc2[0], loc2[1]])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3959.87433  # Radius of earth in miles
    return c * r
