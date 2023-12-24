import math

import re
import solarsystem


class PlanetLongitudes:
    def __init__(self, planet_name, longitude):
        self.planet_name = planet_name
        self.longitude = longitude

def get_planet_longitudes(is_heliocentric: bool, year: int, month: int, day: int):
    planets = []
    longitudes = []
    planet_longitudes = []
    if is_heliocentric:
        system = solarsystem.Heliocentric(year, month, day, 0, 0)
        planets_dict = system.planets()
    else:
        system = solarsystem.Geocentric(year, month, day, 0, 0)
        planets_dict = system.position()
    for planet in planets_dict:
        pos = planets_dict[planet]
        # planet_longitudes.append(PlanetLongitudes(planet_name=planet,longitude=round(pos[0],2)))
        planets.append(planet)
        longitudes.append(round(planets_dict[planet][0], 2))
    planet_longitudes.append(planets)
    planet_longitudes.append(longitudes)
    return planet_longitudes


def get_values(price:int):
    values = [[j for j in range(0, i)][-360:] for i in range(360, price, 360)]
    # adding the rest values
    values.append([k for k in range(values[-1][-1] + 1,price)])
    limit = (math.ceil(price/360) * 360) - price
    # adding zeros so we can transpose later
    for ka in range(limit):
        values[-1].append(0)
    return values

def transpose_values(values:list):
    transposed = [[row[i] for row in values] for i in range(len(values[0]))]
    return transposed

def HalfRoundUp(value):
    return int(value + 0.5)