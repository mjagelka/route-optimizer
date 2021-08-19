# Route Optimizer
This is a Python mini project that works as a CLI tool for finding the optimal
route between given cities.

## Usage
To run the processing workflow:
```
$ ./cli.py [-h] --json JSON [--precision PRECISION] [--debug]
```
JSON file should contain the dictionary with cities and their GPS coordinates.
As an example you can use `cities.json` file. Be careful about the number of
cities (N) as the number of possible routes is equivalent to N!.
Debugging mode for high values of N also creates too many logs.

## Dependencies
Project uses only standard Python libraries so there is no need to install
anything additional.


## Testing
All unit tests are available in the `tests/` directory and can be run using:
```
$ python3 -m unittest discover tests
```
