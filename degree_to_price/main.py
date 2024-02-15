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


def get_values(price: int, factor:int):
    # create factor based element chunks
    values = [[j for j in range(0, i)][-factor:] for i in range(factor, price, factor)]
    # adding the rest values between the last chunk's item till price value
    values.append([k for k in range(values[-1][-1] + 1,price)])
    limit = (math.ceil(price/factor) * factor) - price
    # adding - so we can transpose later
    for _ in range(limit):
        values[-1].append('-')
    return values

def get_only_planetary_squares(ceiled_planetary_longitudes:list,price:int,factor:int):
    limit = math.ceil(price/factor) + 1
    my_list = []
    for multiplication_factor in range(1,limit):
        my_list.append([(multiplication_factor * factor) + long for long in ceiled_planetary_longitudes])
    return my_list

def transpose_values(values:list):
    transposed = [[row[i] for row in values] for i in range(len(values[0]))]
    return transposed

def HalfRoundUp(value):
    return int(value + 0.5)



