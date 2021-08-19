from math import acos, cos, radians, sin
from typing import Dict


class Flight():
    """Class defining the direct connection between two cities."""

    def __init__(self, start: str, end: str, cities: Dict,
                 precision: int) -> None:
        """
        Initialization

        Args:
            start: Starting city.
            end: Destination city.
            cities: Dictionary containing cities GPS coordinates.
            precision: Number of decimals used for rounding.
        """
        self.start = start
        self.end = end
        self.precision = precision

        self.name = self.start + '-' + self.end
        self.lat1 = radians(cities[start]["latitude"])
        self.long1 = radians(cities[start]["longitude"])
        self.lat2 = radians(cities[end]["latitude"])
        self.long2 = radians(cities[end]["longitude"])

    def calculate_distance(self) -> float:
        """
        Calculate the distance between the starting and destination city.

        Returns:
            Distance in km.
        """
        # The angular distance (alpha) between two points on the sphere is
        # calculated from equation:
        # cos(alpha) = sin(lat1)*sin(lat2) +
        #              cos(lat1)*cos(lat2)*cos(long1 - long2).
        # Distance is then calculated as d = R*alpha where alpha is in radians
        # and R is sphere radius.
        radius = 6378
        distance = acos(
            cos(self.lat1)*cos(self.lat2)*cos(self.long1 - self.long2) +
            sin(self.lat1)*sin(self.lat2))*radius
        return round(distance, self.precision)
