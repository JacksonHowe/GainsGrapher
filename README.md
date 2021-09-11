# GainsGrapher

Generate simple graphs for workout data collected in a third-party app (like Strong) and exported to a CSV.

## Usage
```
USAGE: gains-graph.py [-h] (-l | -e EXERCISE) [-m {1rm,weight,volume}] file
```

Pass the `-h` flag for usage information.

The examples below assume an exported CSV file called `export.csv`.

### List exercises available in the CSV
```
$ python3 gains-graph.py export.csv -l
Exercises in export.csv: Triceps Extension, One Arm Overhead Triceps Extension (Cable), Seated Calf Raise (Machine), Chest Fly (Band)...
```

### Graph an exercise
```
$ python3 gains-graph.py export.csv -e "Bench Press (Barbell) -m weight"
(Graph opens in new window)
```

#### Metrics
- `-m 1rm` - (default) 1 Rep Max (calculated with Brzycki formula)
- `-m weight` - Weight
- `-m volume` - Set volume

_Note: not affiliated with Strong, or any other workout app._
