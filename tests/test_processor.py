import logging
from unittest import TestCase, mock

from processor import Processor


CITIES = {'A': {"latitude": 0, "longitude": 1},
          'B': {"latitude": 2, "longitude": 3},
          'C': {"latitude": 4, "longitude": 5}}
FLIGHTS = {'A-B': 314.8,
           'B-A': 314.8,
           'A-C': 629.4,
           'C-A': 629.4,
           'B-C': 314.6,
           'C-B': 314.6}
ROUTE_LIST = [('A', 'B', 'C', 'A'), ('A', 'C', 'B', 'A')]


class TestProcessor(TestCase):
    """Test Processor class."""

    logging.disable(logging.CRITICAL)

    @mock.patch('processor.Processor._read_json')
    @mock.patch('processor.Processor._create_routes')
    def test_collect_distances(self, mock_create_routes, mock_read_json):
        """Test the dictionary with distances was created."""
        mock_read_json.return_value = CITIES
        processor = Processor('json_path', 1)
        self.assertDictEqual(processor._collect_distances(), FLIGHTS)

    @mock.patch('processor.Processor._read_json')
    @mock.patch('processor.Processor._collect_distances')
    def test_create_routes(self, mock_collect_distances, mock_read_json):
        """Test all routes variations were found."""
        mock_read_json.return_value = CITIES
        processor = Processor('json_path', 1)
        self.assertListEqual(processor._create_routes(), ROUTE_LIST)

    @mock.patch('processor.Processor._read_json')
    @mock.patch('processor.Processor._collect_distances')
    @mock.patch('processor.Processor._create_routes')
    def test_get_distances(self, mock_create_routes, mock_collect_distances,
                           mock_read_json):
        """Test total and partial distances for route were derived."""
        mock_collect_distances.return_value = FLIGHTS
        route = ('A', 'C', 'B', 'A')
        processor = Processor('json_path', 1)
        total, partials = processor.get_distances(route)
        self.assertEqual(total, 1258.8)
        self.assertListEqual(partials, [629.4, 314.6, 314.8])

    @mock.patch('processor.Processor._read_json')
    @mock.patch('processor.Processor._collect_distances')
    @mock.patch('processor.Processor._create_routes')
    @mock.patch('processor.Processor.get_distances')
    def test_minimize(self, mock_get_distances, mock_create_routes,
                      mock_collect_distances, mock_read_json):
        """Test the optimal route was found."""
        mock_create_routes.return_value = [('A', 'B'), ('C', 'D'), ('E', 'F')]
        mock_get_distances.side_effect = [(10, [4, 6]), (8, [3, 5]),
                                          (12, [7, 5])]
        processor = Processor('json_path', 1)
        best_route, lowest_distance, best_partials = processor.minimize()
        self.assertTupleEqual(best_route, ('C', 'D'))
        self.assertEqual(lowest_distance, 8)
        self.assertListEqual(best_partials, [3, 5])
