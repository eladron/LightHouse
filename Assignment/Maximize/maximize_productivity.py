import pulp
import pandas as pd
import sys
import re
import random
import json

# Custom function to replace strings representing numbers with integers
def replace_string_with_integer(cell):
    if isinstance(cell, str):
        num_str = re.findall('\d+', cell)
        if num_str:
            return int(''.join(num_str))
    return cell

def insert_to_data(data: dict, station: int, worker_name: str, station_name: str):
    data[station] = {"worker": worker_name, "station": station_name}

def preprocess():
    df = pd.read_excel(sys.argv[1], index_col=0)
    df.replace("#",-1000000, inplace=True)
    df.replace("- ∞", -1000000, inplace=True)
    df = df.applymap(replace_string_with_integer)
    df.drop(columns = df.columns[-1], inplace=True)
    station_counts = list(df.iloc[-1])
    df.drop(index=df.index[-1], axis=0, inplace=True)
    workers_names = [int(x) for x in list(df.index)]
    df.index = workers_names
    stations_names = ["piston", "handle", "water", "screw"]
    return df, station_counts, workers_names, stations_names


def main():
    if len(sys.argv) != 13:
        print("Usage: python maximize_productivity.py  <input_file> <Amount1> <Amount2> <Amount3> <Amount4> <reserve1> <reserve2> <reserve3> <reserve4> <hours> <profit3> <profit4>")
        exit(1)

    df, station_counts, workers_names, stations_names  = preprocess()

    # define the problem
    problem = pulp.LpProblem("Worker_Station_Assignment", pulp.LpMaximize)

    # create the decision variables
    workers = range(len(workers_names))
    stations = range(len(stations_names))
    data = {}

    Q = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])] #  needed_amount
    P = [int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])] # reservers
    T = float(sys.argv[10])
    S = [float(sys.argv[11]), float(sys.argv[12])]
    places_for_station_water = [1, 2, 5]
    print(f"Q = {Q}")
    print(f"P = {P}")
    print(f"T = {T}")
    print(f"S = {S}")


    assign = pulp.LpVariable.dicts("Assign", (workers, stations), lowBound=0, upBound=1, cat=pulp.LpInteger)

    # define the objective function to maximize the total grade
    prod = [list(df.loc[worker]) for worker in workers_names]

    objective = pulp.lpSum(((prod[i][2] * assign[i][2] * S[0] + prod[i][3] * assign[i][3] * S[1]) * T) for i in range(20))
    problem += objective

    # add the constraints
    for w in workers:
        problem += pulp.lpSum(assign[w][s] for s in stations) == 1 # every worker is assigned to exactly one station
    for s in stations:
        problem += pulp.lpSum(assign[w][s] for w in workers) == station_counts[s] # every station has exactly the required number of workers
    for s in stations:
        tmp = Q[s] if s > 2 else Q[2]
        problem += P[s] + pulp.lpSum(assign[w][s] * prod[w][s] * T for w in workers) >= tmp # every station has at least the required amount of product
    for i in range(2):
        problem += P[i] + pulp.lpSum(assign[w][i] * prod[w][i] * T for w in workers) >= P[i+1] + pulp.lpSum(assign[w][i+1] * prod[w][i+1] * T for w in workers) # every station has at least the required amount of product
    problem += P[0] + pulp.lpSum((assign[w][0] * prod[w][0] + assign[w][2] * prod[w][2])* T for w in workers)  <= P[1] + pulp.lpSum(assign[w][1] * prod[w][1] * T * 2 for w in workers) 


    solver = pulp.PULP_CBC_CMD(msg=0)
    problem.solve(solver=solver)
    count = 0
    random_workers = random.sample(workers, 20)
    while (problem.status != pulp.LpStatusOptimal):
        print("Solution not found, removing constraint")
        problem.constraints.popitem()
        if len(problem.constraints) == 27:
            print("No solution found")
            exit(1)
        count += 1
        problem.solve(solver=solver)
    print(f"Soultion found with {count} constraints removed")
    assigned_workers = []
    print("grade achieved:", pulp.value(problem.objective))
    for i in range(1, 21):
        if i in places_for_station_water:
            for w in random_workers:
                if pulp.value(assign[w][2]) == 1 and workers_names[w] not in assigned_workers:
                    print(f"Station {i},{stations_names[2]} is assigned with worker {workers_names[w]}")
                    insert_to_data(data, i, workers_names[w], stations_names[2])
                    assigned_workers.append(workers_names[w])
                    break
        else:
            for w in random_workers:
                if workers_names[w] not in assigned_workers:
                    assigned = 0
                    for s in stations:
                        if pulp.value(assign[w][s]) == 1:
                            assigned = s
                            break
                    insert_to_data(data, i, workers_names[w], stations_names[assigned])
                    print(f"Station {i},{stations_names[assigned]} is assigned with worker {workers_names[w]}")
                    assigned_workers.append(workers_names[w])
                    break
    for s in stations:
        made = P[s] + sum(pulp.value(assign[w][s]) * prod[w][s] * T for w in workers)
        needed = Q[s] if s > 2 else Q[2]
        print(f"Station {s+1},{stations_names[s]} made {made} and needed {needed}")
    

    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()  