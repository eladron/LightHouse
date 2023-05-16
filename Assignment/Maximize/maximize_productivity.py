import pulp
import pandas as pd
import sys

print(len(sys.argv))
if len(sys.argv) != 13:
    print("Usage: python maximize_productivity.py  <input_file> <Amount1> <Amount2> <Amount3> <Amount4> <reserve1> <reserve2> <reserve3> <reserve4> <hours> <profit3> <profit4>")
    exit(1)

# define the problem
problem = pulp.LpProblem("Worker Station Assignment", pulp.LpMaximize)

df = pd.read_excel(sys.argv[1], index_col=0)
df.replace("#",-1000000, inplace=True)
for i in range(1, 10):
    df.replace(f"{i}", i, inplace=True)

# Get the number of stations of each type
station_counts = [3,3,3,11]
print(f"Station counts: {station_counts}")

# create the decision variables
workers_names = list(df.index)
workers = range(len(workers_names))
print(f"Workers: {workers_names}")
stations_names = list(df.columns)
stations = range(len(stations_names))
print(f"Stations: {stations_names}")

Q = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])] #  needed_amount
P = [int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])] # reservers
T = float(sys.argv[10])
S = [int(sys.argv[11]), int(sys.argv[12])]


places_for_station_water = [1, 2, 5]


assign = pulp.LpVariable.dicts("Assign", (workers, stations), lowBound=0, upBound=1, cat=pulp.LpInteger)

# define the objective function to maximize the total grade
prod = [list(df.loc[worker]) for worker in workers_names]
print(prod)


objective = pulp.lpSum((prod[i][2] * assign[i][2] * S[0] + prod[i][3] * assign[i][3] * S[1])* T for i in range(20))
problem += objective

# add the constraints
for w in workers:
    problem += pulp.lpSum(assign[w][s] for s in stations) == 1 # every worker is assigned to exactly one station
for s in stations:
    problem += pulp.lpSum(assign[w][s] for w in workers) == station_counts[s] # every station has exactly the required number of workers
for i in range(4):
    problem += P[i] + pulp.lpSum(assign[w][i] * prod[w][i] * T for w in workers) >= Q[i] # every station has at least the required amount of product
for i in range(2):
    problem += P[i] + pulp.lpSum(assign[w][i] * prod[w][i] * T for w in workers) >= P[i+1] + pulp.lpSum(assign[w][i+1] * prod[w][i+1] * T for w in workers) # every station has at least the required amount of product

problem += P[0] + pulp.lpSum((assign[w][0] * prod[w][0] + assign[w][2] * prod[w][2])* T for w in workers)  <= P[1] + pulp.lpSum(assign[w][1] * prod[w][1] * T * 2 for w in workers) 


# solve the problem
problem.solve()

if problem.status == pulp.LpStatusOptimal:
    assigned_workers = []
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
                        if pulp.value(assign[w][s]) == 1:
                            assigned = s
                            break
                    print("Worker", workers_names[w], "assigned to Station",f"{i},",stations_names[assigned])
                    assigned_workers.append(workers_names[w])
                    break

else:
    print("No optimal solution found.")

