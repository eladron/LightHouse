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

if len(workers) != sum(station_counts):
    print("The number of workers should be equal to the number of stations.")
    exit(1)

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

print(f"Number of valid assignments: {len(valid_assignments)}")

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

if problem.status == pulp.LpStatusOptimal:
    print("Maximum grade achieved:", pulp.value(problem.objective))
    for i in range(1, 21):
        if i in places_for_station_water:
            for w in workers:
                if pulp.value(assign[w][2]) == 1 and workers_names[w] not in assigned_workers:
                    print("Worker", workers_names[w], "assigned to Station",f"{i},",stations_names[2])
                    assigned_workers.append(workers_names[w])
                    break
        else:
            for w in workers:
                if workers_names[w] not in assigned_workers:
                    assigned = 0
                    for s in stations:
                        if assign[w][s] == 1:
                            assigned = s
                            break
                    print(assigned)
                    print("Worker", workers_names[w], "assigned to Station",f"{i},",stations_names[assigned])
                    assigned_workers.append(workers_names[w])
                    break

else:
    print("No optimal solution found.")