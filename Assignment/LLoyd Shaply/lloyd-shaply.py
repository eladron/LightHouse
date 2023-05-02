import random
import pandas as pd
from scipy.optimize import linear_sum_assignment
import sys

def duplicate_prefs(prefs, station_counts):
    new_prefs = []
    for pref in prefs:
        new_prefs.extend([pref] * station_counts[pref-1])
    return new_prefs

if len(sys.argv) != 3:
    print("Usage: python lloyd-shaply.py <Employee_Rank>.xlsx <Station_Rank>.xlsx")
    exit(1)


# read the first table
df1 = pd.read_excel(sys.argv[1], index_col=0)
# read the second table
df2 = pd.read_excel(sys.argv[2], index_col=0)

station_counts = [1,4,2]
free_workers = list(df1.index)
assignments = {}

# Check Tables
if df1.index.tolist() != df2.columns.tolist():
    print("The two tables must have the same workers.")
    exit(1)
if df1.columns.tolist() != df2.index.tolist():
    print("The two tables must have the same stations.")
    exit(1)
if len(df1.index.to_list()) != sum(station_counts):
    print("The number of workers should be equal to the number of stations.")
    exit(1)

while free_workers:
    worker = random.choice(free_workers)
    prefs = duplicate_prefs(df1.loc[worker].tolist(), station_counts)
    free_workers.remove(worker)
    for station in prefs:
        if station not in assignments.values():
            assignments[worker] = station
            break
        elif len([s for s in assignments.values() if s == station]) < station_counts[station-1]:
            assignments[worker] = station
            break
        else:
            currents = [w for w in assignments.keys() if assignments[w] == station]
            min = 100
            min_worker = None
            for current in currents:
                if df2[current][station] < min:
                    min = df2[current][station]
                    min_worker = current
            if df2[worker][station] > min:
                assignments[worker] = station
                del assignments[min_worker]
                free_workers.append(min_worker)
                break

# print the final assignments
print("Final Assignments:")
for worker, station in assignments.items():
    print(f"{worker}: station {station}")
