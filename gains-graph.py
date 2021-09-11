# GainsGrapher - graph metrics recorded in a Strong-CSV export
# Jackson Howe
# Example usage: `python3 gains-graph.py export.csv -e "Bench Press (Barbell)"`

import argparse
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class GainsGrapher:
    # Supported metrics (key: readable name)
    METRICS = {
        '1rm': '1RM',
        'weight': 'Weight',
        'volume': 'Set Volume'
    }
    # Format of dates in the CSV
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filename, exercise, metric):
        assert metric in GainsGrapher.METRICS.keys()
        self.filename = filename
        self.exercise = exercise
        self.metric = metric

        try:
            with open(filename) as file:
                self.data = list(csv.DictReader(file))
        except IOError:
            raise ValueError('Unable to open file "{}".'.format(filename))

    def calc_metric(self, weight, reps):
        if self.metric == '1rm':
            # Brzycki formula (https://en.wikipedia.org/wiki/One-repetition_maximum)
            return weight * (36 / (37 - reps))
        if self.metric == 'weight':
            return weight
        if self.metric == 'volume':
            return weight * reps

    def graph(self):
        x = []
        y = []
        for row in self.data:
            if row['Exercise Name'] == self.exercise:
                x.append(datetime.strptime(row['Date'], GainsGrapher.DATE_FORMAT))
                y.append(self.calc_metric(float(row['Weight']), int(row['Reps'])))
        if not len(x) or not len(y):
            raise ValueError('Unable to find data for exercise "{}".'.format(self.exercise))
        epochs = [t.timestamp() for t in x]
        p = np.poly1d(np.polyfit(epochs, y, 1))

        plt.scatter(x, y)
        plt.title(self.exercise)
        plt.xlabel('Date')
        plt.ylabel(GainsGrapher.METRICS[self.metric])
        plt.plot(x, p(epochs), 'r--')
        plt.show()

    def list_exercises(self):
        exercises = set()
        for row in self.data:
            exercises.add(row['Exercise Name'])
        if len(exercises):
            print('Exercises in {}: {}'.format(self.filename, ', '.join(exercises)))
        else:
            print('No exercises found in {}'.format(self.filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GainsGrapher - graph metrics recorded in a Strong-CSV export')
    parser.add_argument('file', type=str, help='CSV export file path')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list', help='List exercises in the provided file', action='store_true')
    group.add_argument('-e', '--exercise', type=str, help='Exercise name to graph')
    parser.add_argument('-m', '--metric', type=str, help='Metric to graph', choices=GainsGrapher.METRICS.keys(), default='1rm')
    args = parser.parse_args()

    try:
        grapher = GainsGrapher(args.file, args.exercise, args.metric)
        if args.list:
            grapher.list_exercises()
        else:
            grapher.graph()
    except ValueError as err:
        print(str(err))
