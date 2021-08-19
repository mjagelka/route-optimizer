import logging
from itertools import permutations
from json import load
from typing import Dict, List, Tuple, Union

from flight import Flight


LOG = logging.getLogger(__name__)


class Processor():
    """Class that encapsulates main processing logic."""

    def __init__(self, json_path: str, precision: int = 3) -> None:
        """
        Initialization.

        Args:
            json_path: Path to the json file containing cities GPS coordinates.
            precision: Number of decimals used for rounding.
        """
        self.json_path = json_path
        self.precision = precision

        self.cities = self._read_json()
        self.flights = self._collect_distances()
        self.route_list = self._create_routes()

    def _read_json(self) -> Dict:
        """
        Read json file and return it as a dictionary.

        Returns:
            Extracted dictionary.
        """
        with open(self.json_path, 'r') as filename:
            cities = load(filename)
        return cities

    def _collect_distances(self) -> Dict:
        """
        Create dictionary containing distances between two cities.

        Returns:
            Dictionary with the flight name as a key and distance as a value.
        """
        flights = {}  # type: Dict[str]
        nodes = list(self.cities.keys())
        # possible combinations of flight start and destination
        partial_routes = list(permutations(nodes, 2))
        for partial_route in partial_routes:
            start, end = partial_route
            flight = Flight(start, end, self.cities, self.precision)
            distance = flight.calculate_distance()
            flights[flight.name] = distance
            LOG.debug('The flight {} has distance {} km.'
                      .format(flight.name, distance))
        return flights

    def _create_routes(self) -> List[Tuple]:
        """
        Create all possible variations of complete routes between N cities.

        Returns:
            List of routes permutations.
        """
        # As the routes are cycled, permutations will create some identical
        # routes just with a different starting city. Choosing the static
        # starting city will reduce the number of permutations for N cities by
        # N times.
        nodes = list(self.cities.keys())
        start = nodes[0]
        routes = permutations(nodes[1:])
        route_list = []  # type: List[Tuple]
        for route in list(routes):
            route_list.append((start,) + route + (start,))
        LOG.debug('{} routes exist: {}.'.format(len(route_list), route_list))
        return route_list

    def get_distances(self, route: Tuple[str]) -> Tuple[float, List[float]]:
        """
        Get total and partial distances for a given route.

        Args:
            route: Tuple of all route nodes.

        Returns:
            Total route distance and partial distances between route nodes.
        """
        # total distance
        total = 0  # type: float
        # list of partial distances
        partials = []  # type: List[float]
        for i in range(len(route) - 1):
            flight_name = route[i] + '-' + route[i + 1]
            partial = self.flights[flight_name]
            partials.append(partial)
            total += partial
        total = round(total, self.precision)
        LOG.debug('Route: {}; Distance: {} km.'
                  .format(' - '.join(route), total))
        return total, partials

    def minimize(self) -> Tuple[Tuple[str], float, List[float]]:
        """Go through all possible routes and find the optimal one."""
        lowest_distance = float('inf')  # type: float
        best_route = None  # type: Union[None, Tuple[str]]
        best_partials = None  # type: Union[List[float]]
        for route in self.route_list:
            total, partials = self.get_distances(route)
            if total < lowest_distance:
                lowest_distance = total
                best_route = route
                best_partials = partials

        LOG.info('Best route is {} with total distance {} km.'
                 .format(' - '.join(best_route), lowest_distance))
        LOG.info('Partial distances on this route are: {} km.'
                 .format(', '.join(map(str, best_partials))))
        return best_route, lowest_distance, best_partials
