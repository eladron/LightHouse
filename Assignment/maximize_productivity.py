import pandas as pd
import itertools
import sys

if len(sys.argv) != 2:
    print("Usage: python maximize_productivity.py  <input_file>")
    exit(1)

df = pd.read_excel(sys.argv[1], index_col=0)

# Get the number of stations of each type
station_counts = df.iloc[0, :].tolist()
print(f"Station counts: {station_counts}")

# Remove the first row (station counts) and transpose the data frame
df = df.iloc[1:]

stations = list(df.columns)
print(f"Stations: {stations}")
# Create a list of worker names
workers = list(df.index)
print(f"Workers: {workers}")

# Create a list of station types
station_types = []
for i, count in enumerate(station_counts):
    station_types.extend([i] * count)
# Generate all possible assignments of workers to stations
valid_assignments = []
for assignment in itertools.permutations(station_types):
    # Check if the assignment is valid
    is_valid = True
    for i, count in enumerate(station_counts):
        if assignment.count(i) > count:
            is_valid = False
            break
    if is_valid:
        valid_assignments.append(assignment)

best_assignment = None
best_score = 0

for i, assignment in enumerate(valid_assignments):
    score = sum(df.loc[worker, station+1] for worker, station in zip(workers, assignment))
    if score > best_score:
        best_score = score
        best_assignment = assignment

print("Best assignment:")
for j, worker in enumerate(workers):
    station_type = best_assignment[j]
    print(f"{worker}: station {station_type+1}")
print(f"Score: {best_score}")