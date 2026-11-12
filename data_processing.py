import csv
import os


class Table:
    """A table of rows, where each row is a dictionary."""

    def __init__(self, data):
        self.table = data

    def filter(self, condition):
        """Return a new Table with only the rows where condition(row) is True."""
        return Table([row for row in self.table if condition(row)])

    def aggregate(self, key, func):
        """Apply func to the list of values in column `key`."""
        values = [row[key] for row in self.table]
        return func(values)

    def __len__(self):
        return len(self.table)

    def __iter__(self):
        return iter(self.table)


class DataLoader:
    """Load a CSV file and convert it into a Table."""

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        location = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(location, self.filename)
        data = []
        with open(path) as f:
            for r in csv.DictReader(f):
                row = dict(r)
                row['temperature'] = float(row['temperature'])
                row['latitude'] = float(row['latitude'])
                row['longitude'] = float(row['longitude'])
                data.append(row)
        return Table(data)


def average(values):
    return sum(values) / len(values)

loader = DataLoader('Cities.csv')
cities = loader.load()

# Print first 5 cities only
print("First 5 cities:")
for city in list(cities)[:5]:
    print(city['city'])
print()

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
print(cities.aggregate('temperature', average))
print()

# Print all cities in Germany
print("All cities in Germany:")
germany = cities.filter(lambda c: c['country'] == 'Germany')
for c in germany:
    print(c['city'])
print()

# Print all cities in Spain with a temperature above 12°C
print("Cities in Spain with temperature above 12°C:")
spain_warm = cities.filter(
    lambda c: c['country'] == 'Spain' and c['temperature'] > 12
)
for c in spain_warm:
    print(c['city'], c['temperature'])
print()

# Count the number of unique countries
print("Number of unique countries:")
print(cities.aggregate('country', lambda x: len(set(x))))
print()

# Print the average temperature for all the cities in Germany
print("Average temperature in Germany:")
print(germany.aggregate('temperature', average))
print()

# Print the max temperature for all the cities in Italy
print("Max temperature in Italy:")
italy = cities.filter(lambda c: c['country'] == 'Italy')
print(italy.aggregate('temperature', max))