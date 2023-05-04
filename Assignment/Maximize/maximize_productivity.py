import pulp
import pandas as pd
import itertools
import sys

if len(sys.argv) != 2:
    print("Usage: python maximize_productivity.py  <input_file>")
    exit(1)

# define the problem
problem = pulp.LpProblem("Worker Station Assignment", pulp.LpMaximize)

df = pd.read_excel(sys.argv[1], index_col=0)
df.replace("- ∞",-1000000, inplace=True)
for i in range(1, 10):
    df.replace(f"{i}", i, inplace=True)

# Get the number of stations of each type
station_counts = df.iloc[0, :].tolist()
print(f"Station counts: {station_counts}")
df = df.iloc[1:]

# create the decision variables
workers_names = list(df.index)
workers = range(len(workers_names))
print(f"Workers: {workers_names}")
stations_names = list(df.columns)
stations = range(len(stations_names))
print(f"Stations: {stations_names}")
assign = pulp.LpVariable.dicts("Assign", (workers, stations), lowBound=0, upBound=1, cat=pulp.LpInteger)

# define the objective function to maximize the total grade
grades = [list(df.loc[worker]) for worker in workers_names]
print(grades)

objective = pulp.lpSum(grades[w][s] * assign[w][s] for w in workers for s in stations)
problem += objective

# add the constraints
for w in workers:
    problem += pulp.lpSum(assign[w][s] for s in stations) == 1
for s in stations:
    problem += pulp.lpSum(assign[w][s] for w in workers) == station_counts[s]

# solve the problem
problem.solve()

# print the solution
if problem.status == pulp.LpStatusOptimal:
    print("Maximum grade achieved:", pulp.value(problem.objective))
    for w in workers:
        for s in stations:
            if pulp.value(assign[w][s]) == 1:
                print("Worker", workers_names[w], "assigned to Station", stations_names[s])
else:
    print("No optimal solution found.")