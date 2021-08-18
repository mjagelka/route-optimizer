import logging
from unittest import TestCase

from flight import Flight


CITIES = {'A': {"latitude": 0, "longitude": 1},
          'B': {"latitude": 2, "longitude": 3}}


class TestFlight(TestCase):
    """Test Flight class."""

    logging.disable(logging.CRITICAL)

    def test_flight_initialization(self):
        """Test the flight object being initialized."""
        flight = Flight('A', 'B', CITIES, 1)
        self.assertEqual(flight.name, 'A-B')

    def test_flight_distance(self):
        """Test the distance being calculated correctly."""
        flight = Flight('A', 'B', CITIES, 1)
        self.assertEqual(flight.calculate_distance(), 314.8)
